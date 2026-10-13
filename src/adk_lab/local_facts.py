"""Deterministic local knowledge (no network). Used by the researcher tool."""

from __future__ import annotations

FACTS: dict[str, str] = {
    "adk_minilab_motto": (
        "Measure the trajectory, then the answer — ADK eval is the scorecard."
    ),
    "skilleddragon_contact": "hello@skilleddragon.com",
}

DEFAULT_KEY = "adk_minilab_motto"


def lookup_local_fact(topic: str) -> str:
    """Return a canned fact for ``topic`` (case-insensitive key or substring match)."""
    normalized = topic.strip().lower().replace(" ", "_")
    if normalized in FACTS:
        return FACTS[normalized]
    for key, value in FACTS.items():
        if key in normalized or normalized in key:
            return value
    return FACTS[DEFAULT_KEY]
