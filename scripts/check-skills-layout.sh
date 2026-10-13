#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fail=0

for forbidden in .cursor/skills .agents/skills; do
  if [[ -d "$ROOT/$forbidden" ]]; then
    echo "ERROR: skills must live only under .claude/skills — found $forbidden"
    fail=1
  fi
done

if [[ ! -d "$ROOT/.claude/skills" ]]; then
  echo "ERROR: missing .claude/skills"
  exit 1
fi

for skill_dir in "$ROOT"/.claude/skills/*/; do
  [[ -d "$skill_dir" ]] || continue
  name="$(basename "$skill_dir")"
  skill_file="$skill_dir/SKILL.md"
  if [[ ! -f "$skill_file" ]]; then
    echo "ERROR: missing SKILL.md in $skill_dir"
    fail=1
    continue
  fi
  front_name="$(sed -n 's/^name: *//p' "$skill_file" | head -1 | tr -d '\r')"
  if [[ "$front_name" != "$name" ]]; then
    echo "ERROR: frontmatter name '$front_name' != folder '$name'"
    fail=1
  fi
done

exit "$fail"
