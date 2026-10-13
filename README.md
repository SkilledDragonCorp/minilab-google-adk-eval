# minilab-google-adk-eval

SkilledDragon educational minilab proving **[Google ADK](https://adk.dev/) `google-adk[eval]==2.11.0`** runs a tiny researcher agent, a deterministic local tool, and the official **`adk eval`** flow with an **Eval Scorecard** (`reports/eval.md` + JSON). This lab is about ADK evaluation mechanics — not Google Places.

Docs: [Why evaluate agents (ADK)](https://adk.dev/evaluate/) · upstream [adk-python](https://github.com/google/adk-python) at pin **2.11.0**.

## What we built

| Layer | Stack |
| --- | --- |
| Runtime | Python 3.12+, [uv](https://docs.astral.sh/uv/) |
| Agent | `LlmAgent` + `FunctionTool(lookup_local_fact)` — no network in CI |
| Keyless model | `ScriptedLlm(BaseLlm)` replays recorded `LlmResponse` turns (no FakeModel stubs) |
| Eval | `src/adk_lab/evalset.json`, `eval_config.json` (keyless metrics only) |
| CLI | `adk-lab eval` → wraps `adk eval … --print_detailed_results` |
| Live (optional) | `eval_config_live.json` gates `final_response_match_v2`, `hallucinations_v1`, `safety_v1` behind API keys |

## Setup

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --extra dev
```

Optional live judges (skipped cleanly without keys):

```bash
export GOOGLE_API_KEY=...   # or Vertex: GOOGLE_GENAI_USE_VERTEXAI=true + GOOGLE_CLOUD_PROJECT
```

## Tutorial

```bash
# Keyless eval + scorecard
uv run adk-lab eval
cat reports/eval.md

# Same as CLI (direct ADK)
export PYTHONPATH=src
uv run adk eval src/adk_lab src/adk_lab/evalset.json \
  --config_file_path=src/adk_lab/eval_config.json --print_detailed_results
```

Deploy smoke (local only — no Cloud Run unless you opt in):

```bash
export PYTHONPATH=src
uv run adk api_server src/adk_lab &
curl -sS http://127.0.0.1:8000/list-apps || true
```

Optional Docker: see `Dockerfile`.

## Skills (Claude Code / Cursor)

Only under `.claude/skills/`:

- `adk-agent-scaffold` — researcher agent + local tool pattern
- `adk-eval-author` — evalset / eval_config + scorecard workflow

## Local gate (before push)

```bash
uv sync --extra dev
uv run ruff check src tests && uv run mypy src/adk_lab && uv run pytest -q
bash scripts/check-skills-layout.sh
bash scripts/pip-audit.sh
gitleaks dir --redact --exit-code 1 .
```

## Contact

**hello@skilleddragon.com** — see [SECURITY.md](SECURITY.md).
