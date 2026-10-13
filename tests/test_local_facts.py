from adk_lab.local_facts import lookup_local_fact


def test_lookup_exact_key() -> None:
    assert "scorecard" in lookup_local_fact("adk_minilab_motto").lower()


def test_lookup_fallback() -> None:
    assert lookup_local_fact("unknown topic")
