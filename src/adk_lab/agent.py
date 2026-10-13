"""Researcher agent: one local tool + keyless scripted model."""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools.function_tool import FunctionTool

from adk_lab.local_facts import lookup_local_fact
from adk_lab.scripted_llm import ScriptedLlm, build_research_script

APP_NAME = "adk_researcher_lab"

scripted_model = ScriptedLlm(responses=build_research_script())

root_agent = LlmAgent(
    name="researcher",
    model=scripted_model,
    description="Answers SkilledDragon lore using a deterministic local fact tool.",
    instruction=(
        "You are a research assistant for the SkilledDragon ADK minilab. "
        "When the user asks for the minilab motto or similar lore, call "
        "`lookup_local_fact` with a short topic key, then answer in one sentence."
    ),
    tools=[FunctionTool(lookup_local_fact)],
)


def reset_data() -> None:
    """Rewind scripted LLM turns between eval cases."""
    scripted_model.reset()
