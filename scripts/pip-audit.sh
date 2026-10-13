#!/usr/bin/env bash
# Audit google-adk runtime deps (not the local adk-lab package).
# Some advisories reference fix versions not yet published for all platforms;
# see docs/ADK_PIN.md.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
REQ="$(mktemp)"
uv export --format requirements.txt --no-dev --no-emit-project -o "$REQ"
uv run pip-audit -r "$REQ" \
  --ignore-vuln PYSEC-2026-3552 \
  --ignore-vuln PYSEC-2026-3553 \
  --ignore-vuln PYSEC-2026-3554 \
  --ignore-vuln GHSA-537c-gmf6-5ccf \
  --ignore-vuln PYSEC-2026-3740
rm -f "$REQ"
