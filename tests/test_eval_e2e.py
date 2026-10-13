import pytest

from adk_lab.cli import run_eval


@pytest.mark.e2e
def test_keyless_adk_eval_passes() -> None:
    summary = run_eval()
    assert summary.failed == 0
    assert summary.passed >= 1
    names = {str(m["name"]) for m in summary.metrics}
    assert "tool_trajectory_avg_score" in names
    assert "response_match_score" in names
