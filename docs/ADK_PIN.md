# ADK pin

- **Package:** `google-adk[eval]==2.11.0`
- **Evaluate docs:** https://adk.dev/evaluate/
- **Upstream:** https://github.com/google/adk-python

The `[eval]` extra pulls trajectory/response metrics and eval CLI dependencies used by `adk eval`.

`tool.uv.override-dependencies` bumps `cryptography`, `litellm`, and `nltk` within what ADK 2.11.0 allows. `scripts/pip-audit.sh` ignores a handful of OSV entries whose listed fix versions are not yet on PyPI for this stack (upstream ADK transitive deps).
