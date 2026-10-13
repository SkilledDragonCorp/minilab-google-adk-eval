"""Keyless LLM double: pre-recorded ``LlmResponse`` turns (no provider API)."""

from __future__ import annotations

from collections.abc import AsyncGenerator, Sequence
from typing import TYPE_CHECKING

from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.genai import types
from pydantic import Field, PrivateAttr

if TYPE_CHECKING:
    from google.adk.models.llm_request import LlmRequest


class ScriptedLlm(BaseLlm):
    """Deterministic ``BaseLlm`` that replays scripted responses in FIFO order."""

    model: str = "scripted-research-v1"
    responses: Sequence[LlmResponse] = Field(default_factory=list)
    _index: int = PrivateAttr(default=0)

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        del llm_request, stream
        if self._index >= len(self.responses):
            yield LlmResponse(
                content=types.Content(role="model", parts=[types.Part(text="")]),
                turn_complete=True,
            )
            return
        response = self.responses[self._index]
        self._index += 1
        yield response

    def reset(self) -> None:
        """Rewind the script (useful in tests)."""
        self._index = 0


def tool_call_response(*, tool_name: str, args: dict[str, object]) -> LlmResponse:
    return LlmResponse(
        content=types.Content(
            role="model",
            parts=[
                types.Part(
                    function_call=types.FunctionCall(name=tool_name, args=args),
                )
            ],
        ),
        turn_complete=True,
    )


def text_response(text: str) -> LlmResponse:
    return LlmResponse(
        content=types.Content(role="model", parts=[types.Part(text=text)]),
        turn_complete=True,
    )


def build_research_script() -> list[LlmResponse]:
    """Script aligned with ``evalset.json`` (one tool turn + one answer turn)."""
    motto = (
        "Measure the trajectory, then the answer — ADK eval is the scorecard."
    )
    return [
        tool_call_response(
            tool_name="lookup_local_fact",
            args={"topic": "adk_minilab_motto"},
        ),
        text_response(motto),
    ]
