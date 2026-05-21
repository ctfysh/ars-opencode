#!/bin/bash
# transform-opencode.sh: Re-apply OpenCode transformations after upstream merge
# Usage: ./scripts/transform-opencode.sh [--check]

set -euo pipefail

TRANSFORM_COUNT=0

apply() {
  local pattern=$1
  local replacement=$2
  local paths=$3
  local files=$(find $paths -type f -name '*.md' 2>/dev/null)
  local count=0
  for f in $files; do
    if grep -q "$pattern" "$f" 2>/dev/null; then
      sed -i '' "s/$pattern/$replacement/g" "$f"
      count=$((count + 1))
    fi
  done
  echo "  $replacement: $count files"
  TRANSFORM_COUNT=$((TRANSFORM_COUNT + count))
}

echo "=== OpenCode Transform ==="

# 1. Remove model: frontmatter
echo "[1/5] Removing model: frontmatter..."
for f in $(find deep-research academic-paper academic-paper-reviewer academic-pipeline -path '*/agents/*.md'); do
  sed -i '' '/^model: /d' "$f"
done

# 2. WebSearch -> websearch
echo "[2/5] WebSearch -> websearch..."
apply 'WebSearch' 'websearch' 'deep-research academic-paper academic-paper-reviewer academic-pipeline'

# 3. WebFetch -> webfetch
echo "[3/5] WebFetch -> webfetch..."
apply 'WebFetch' 'webfetch' 'deep-research academic-paper academic-paper-reviewer academic-pipeline'

# 4. Claude Code -> OpenCode (runtime references)
echo "[4/5] Claude Code -> OpenCode..."
apply 'Claude Code' 'OpenCode' 'deep-research academic-paper academic-paper-reviewer academic-pipeline'

# 5. Agent tool -> task()
echo "[5/5] Agent tool -> task()..."
apply 'the Agent tool' 'the task\(\) function' 'deep-research academic-paper academic-paper-reviewer academic-pipeline'
apply 'Agent tool' 'task()' 'deep-research academic-paper academic-paper-reviewer academic-pipeline'

echo ""
echo "=== $TRANSFORM_COUNT transformations applied ==="

if [ "${1:-}" = "--check" ]; then
  echo "=== Verification ==="
  REMAINING=$(grep -rn '^model: ' deep-research academic-paper academic-paper-reviewer academic-pipeline --include='*.md' 2>/dev/null | wc -l | tr -d ' ')
  echo "  model: fields remaining: $REMAINING"
  WEBS=$(grep -rn '\bWebSearch\b' deep-research academic-paper academic-paper-reviewer academic-pipeline --include='*.md' 2>/dev/null | wc -l | tr -d ' ')
  echo "  WebSearch remaining: $WEBS"
  WEBF=$(grep -rn '\bWebFetch\b' deep-research academic-paper academic-paper-reviewer academic-pipeline --include='*.md' 2>/dev/null | wc -l | tr -d ' ')
  echo "  WebFetch remaining: $WEBF"
  if [ "$REMAINING" -gt 0 ] || [ "$WEBS" -gt 0 ] || [ "$WEBF" -gt 0 ]; then
    echo "  WARNING: Some CC patterns remain!"
    exit 1
  fi
  echo "  All clean."
fi
