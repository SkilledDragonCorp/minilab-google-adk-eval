"""CLI: run ADK eval and write Eval Scorecard reports."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent
REPO_ROOT = PKG_DIR.parent.parent
AGENT_DIR = PKG_DIR
EVALSET = PKG_DIR / "evalset.json"
EVAL_CONFIG_KEYLESS = PKG_DIR / "eval_config.json"
EVAL_CONFIG_LIVE = PKG_DIR / "eval_config_live.json"
REPORTS_DIR = REPO_ROOT / "reports"


@dataclass(frozen=True)
class EvalSummary:
    eval_set_id: str
    passed: int
    failed: int
    metrics: list[dict[str, str | float | None]]
    raw_log: str


def _has_live_credentials() -> bool:
    if os.environ.get("GOOGLE_API_KEY"):
        return True
    if os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "").lower() in {"1", "true", "yes"}:
        return True
    return bool(os.environ.get("GOOGLE_CLOUD_PROJECT"))


def _pick_config_path() -> Path:
    if _has_live_credentials() and EVAL_CONFIG_LIVE.is_file():
        return EVAL_CONFIG_LIVE
    return EVAL_CONFIG_KEYLESS


def _parse_eval_summary(output: str) -> EvalSummary:
    set_match = re.search(r"Eval Set Id:\s*(\S+)", output)
    eval_set_id = set_match.group(1) if set_match else "unknown"
    passed = int(re.search(r"Tests passed:\s*(\d+)", output).group(1))  # type: ignore[union-attr]
    failed = int(re.search(r"Tests failed:\s*(\d+)", output).group(1))  # type: ignore[union-attr]
    metrics: list[dict[str, str | float | None]] = []
    for line in output.splitlines():
        if line.startswith("Metric:"):
            # Metric: tool_trajectory_avg_score, Status: PASSED, Score: 1.0, Threshold: 1.0
            parts = [p.strip() for p in line.split(",")]
            name = parts[0].removeprefix("Metric:").strip()
            status = parts[1].removeprefix("Status:").strip() if len(parts) > 1 else ""
            score_part = next((p for p in parts if p.startswith("Score:")), "Score: None")
            threshold_part = next(
                (p for p in parts if p.startswith("Threshold:")), "Threshold: None"
            )
            score_raw = score_part.removeprefix("Score:").strip()
            threshold_raw = threshold_part.removeprefix("Threshold:").strip()
            metrics.append(
                {
                    "name": name,
                    "status": status,
                    "score": None if score_raw == "None" else float(score_raw),
                    "threshold": None if threshold_raw == "None" else float(threshold_raw),
                }
            )
    return EvalSummary(
        eval_set_id=eval_set_id,
        passed=passed,
        failed=failed,
        metrics=metrics,
        raw_log=output,
    )


def run_eval(*, print_detailed: bool = True) -> EvalSummary:
    config_path = _pick_config_path()
    cmd = [
        "adk",
        "eval",
        str(AGENT_DIR),
        str(EVALSET),
        f"--config_file_path={config_path}",
    ]
    if print_detailed:
        cmd.append("--print_detailed_results")
    env = os.environ.copy()
    env.setdefault("PYTHONPATH", str(REPO_ROOT / "src"))
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
        cwd=REPO_ROOT,
        env=env,
    )
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        raise RuntimeError(
            f"adk eval failed (exit {proc.returncode}). Output:\n{combined[-4000:]}"
        )
    summary = _parse_eval_summary(combined)
    write_scorecard(summary, config_path=config_path)
    return summary


def write_scorecard(summary: EvalSummary, *, config_path: Path) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "adk_version": "2.11.0",
        "docs": "https://adk.dev/evaluate/",
        "eval_set_id": summary.eval_set_id,
        "config_file": str(config_path.relative_to(REPO_ROOT)),
        "live_metrics_enabled": config_path.name == "eval_config_live.json",
        "tests_passed": summary.passed,
        "tests_failed": summary.failed,
        "metrics": summary.metrics,
    }
    json_path = REPORTS_DIR / "eval.json"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# ADK Eval Scorecard",
        "",
        f"- **Eval set:** `{summary.eval_set_id}`",
        f"- **Config:** `{config_path.relative_to(REPO_ROOT)}`",
        "- **ADK pin:** `google-adk[eval]==2.11.0` "
        "([evaluate docs](https://adk.dev/evaluate/))",
        f"- **Generated:** {payload['generated_at']}",
        "",
        "## Results",
        "",
        f"- Tests passed: **{summary.passed}**",
        f"- Tests failed: **{summary.failed}**",
        "",
        "| Metric | Status | Score | Threshold |",
        "| --- | --- | --- | --- |",
    ]
    for metric in summary.metrics:
        lines.append(
            f"| {metric['name']} | {metric['status']} | {metric['score']} | {metric['threshold']} |"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Keyless CI uses `tool_trajectory_avg_score` and `response_match_score` only.",
            "- Live judge metrics require `GOOGLE_API_KEY` or Vertex env.",
            "",
        ]
    )
    md_path = REPORTS_DIR / "eval.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run ADK eval and write reports/eval.md+json.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("eval", help="Run adk eval with scorecard output")
    args = parser.parse_args(argv)
    if args.command == "eval":
        summary = run_eval()
        print(f"Scorecard written to {REPORTS_DIR / 'eval.md'} ({summary.passed} passed)")
        if summary.failed:
            sys.exit(1)


if __name__ == "__main__":
    main()
