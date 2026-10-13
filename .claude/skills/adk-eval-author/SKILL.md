---
name: adk-eval-author
description: Author ADK evalset.json and eval_config.json, run adk eval with keyless metrics, and publish reports/eval.md scorecards for google-adk 2.11.0.
---

# ADK eval author

## Keyless metrics (CI)

In `eval_config.json`, keep only:

- `tool_trajectory_avg_score`
- `response_match_score`

## Live metrics (optional)

When `GOOGLE_API_KEY` or Vertex env is set, `adk-lab eval` selects `eval_config_live.json` for judge metrics (`final_response_match_v2`, `hallucinations_v1`, `safety_v1`).

## Run

```bash
uv run adk-lab eval
cat reports/eval.md
```

Direct ADK:

```bash
export PYTHONPATH=src
uv run adk eval src/adk_lab src/adk_lab/evalset.json \
  --config_file_path=src/adk_lab/eval_config.json --print_detailed_results
```

## Evalset shape

Follow Pydantic eval models (`EvalSet`, `EvalCase`) — see https://adk.dev/evaluate/ for field meanings (`conversation`, `intermediate_data.tool_uses`, `final_response`, `session_input.app_name`).
