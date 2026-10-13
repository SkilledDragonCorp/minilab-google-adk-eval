# ADK pin

- **Package:** `google-adk[eval]==2.11.0`
- **Evaluate docs:** https://adk.dev/evaluate/
- **Upstream:** https://github.com/google/adk-python

The `[eval]` extra pulls trajectory/response metrics and eval CLI dependencies used by `adk eval`.

Local macOS builds may require `tool.uv.override-dependencies = ["cryptography==44.0.2"]` when older Rust cannot build newer `cryptography` sdists; Linux CI uses prebuilt wheels.
