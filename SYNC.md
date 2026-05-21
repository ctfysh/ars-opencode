# Upstream Sync Protocol

**Source:** `Imbad0202/academic-research-skills`
**Current base:** v3.9.4.2

## Process

1. Check for new upstream tags:
   ```bash
   git remote add upstream git@github.com:Imbad0202/academic-research-skills.git
   git fetch upstream --tags
   ```

2. Identify new version:
   ```bash
   git tag | grep upstream/v | sort -V
   ```

3. Create sync branch:
   ```bash
   git checkout -b sync/v3.9.5
   git merge upstream/v3.9.5 --allow-unrelated-histories
   ```

4. Resolve conflicts:
   - **Auto-accept for:** `scripts/`, `shared/`, `deep-research/agents/*.md`, `academic-paper/agents/*.md`, `academic-*/references/*.md`, `tests/fixtures/`, `docs/design/`, `MODE_REGISTRY.md`
   - **Manual review for:** `*/SKILL.md`, `commands/`, `.opencode/CLAUDE.md`, `hooks/`

5. Re-apply OpenCode transformations (run `scripts/transform-opencode.sh`):
   - Remove `model:` frontmatter from agent files
   - `WebSearch` → `websearch` in agent bodies
   - `WebFetch` → `webfetch` in agent bodies

6. Verify:
   ```bash
   python3 -m pytest scripts/ -v
   python3 scripts/check_skippable.py  # OpenCode-specific lint
   ```

7. Commit and PR:
   ```bash
   git add -A
   git commit -m "[SYNC] v3.9.5 upstream merge"
   git push origin sync/v3.9.5
   ```
