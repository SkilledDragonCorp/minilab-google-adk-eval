---
name: adk-agent-scaffold
description: Scaffold a keyless Google ADK researcher agent with one deterministic local tool and ScriptedLlm(BaseLlm) for CI-safe runs at google-adk 2.11.0.
---

# ADK agent scaffold (SkilledDragon minilab)

Use when adding or extending the researcher agent in `src/adk_lab/`.

## Pattern

1. **Tool** — pure Python, no network (`lookup_local_fact` in `local_facts.py`).
2. **Model** — `ScriptedLlm` subclasses `google.adk.models.base_llm.BaseLlm` and yields pre-built `LlmResponse` objects in FIFO order.
3. **Agent** — `LlmAgent(name=..., model=scripted_model, tools=[FunctionTool(...)])`.
4. **Module export** — `src/adk_lab/__init__.py` exposes `root_agent` and `agent` submodule with `reset_data()` to rewind scripts between eval cases.

## ADK CLI paths

- Agent directory: `src/adk_lab/` (contains `__init__.py` loaded as module `agent`).
- Docs: https://adk.dev/evaluate/

## Pin

`google-adk[eval]==2.11.0` — see `pyproject.toml` and `docs/ADK_PIN.md`.
