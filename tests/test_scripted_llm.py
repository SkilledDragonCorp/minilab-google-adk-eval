import pytest
from google.adk.models.llm_request import LlmRequest
from google.genai import types

from adk_lab.scripted_llm import ScriptedLlm, build_research_script, text_response


@pytest.mark.asyncio
async def test_scripted_llm_fifo() -> None:
    llm = ScriptedLlm(responses=[text_response("one"), text_response("two")])
    req = LlmRequest(
        model="x",
        contents=[types.Content(role="user", parts=[types.Part(text="hi")])],
    )
    first = [r async for r in llm.generate_content_async(req)]
    second = [r async for r in llm.generate_content_async(req)]
    assert first[0].content and first[0].content.parts[0].text == "one"
    assert second[0].content and second[0].content.parts[0].text == "two"


def test_research_script_length() -> None:
    assert len(build_research_script()) == 2
