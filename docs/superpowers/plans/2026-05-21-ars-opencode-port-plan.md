# ARS → OpenCode Port Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create an `ars-opencode` sibling repo that ports all 4 academic-research-skills (deep-research, academic-paper, academic-paper-reviewer, academic-pipeline) + 25 modes + 13 commands from Claude Code to OpenCode-native format.

**Architecture:** Hybrid Fork. Core ARS content (agent prompts, Python scripts, JSON schemas) is copied verbatim from the upstream CC repo. A new OpenCode dispatch layer wraps it: 5 `ars-*` skills with `task(category=..., load_skills=[...])` dispatch replacing CC's Agent tool routing, 13 command dispatchers replacing CC's `/ars-*` frontmatter, and `opencode.json` replacing `.claude-plugin/plugin.json`.

**Tech Stack:** OpenCode-native skill/command format, Python 3 (pytest, 57 existing tests), GitHub Actions (CI workflows), bash (sync/transform scripts).

**Reference:** Design spec at `docs/design/2026-05-21-ars-opencode-port-design.md`

---

## File Structure

```
ars-opencode/                          # NEW sibling repo
├── opencode.json                      # Plugin manifest (NEW)
├── .opencode/
│   └── CLAUDE.md                      # Thin routing reference (NEW)
├── skills/
│   ├── ars-meta/SKILL.md             # Meta-routing (NEW)
│   ├── ars-deep-research/SKILL.md    # Adapted from deep-research/SKILL.md
│   ├── ars-academic-paper/SKILL.md   # Adapted from academic-paper/SKILL.md
│   ├── ars-reviewer/SKILL.md         # Adapted from academic-paper-reviewer/SKILL.md
│   └── ars-pipeline/SKILL.md         # Adapted from academic-pipeline/SKILL.md
├── commands/
│   ├── ars-full.md                   # 13 dispatchers (NEW, adapted from CC)
│   ├── ars-plan.md
│   ├── ars-review.md
│   ├── ars-lit-review.md
│   ├── ars-socratic.md
│   ├── ars-systematic-review.md
│   ├── ars-fact-check.md
│   ├── ars-reviewer.md
│   ├── ars-revision.md
│   ├── ars-abstract.md
│   ├── ars-disclosure.md
│   ├── ars-format.md
│   └── ars-calibrate.md
├── hooks/
│   └── ars-init.md                   # Session init (NEW)
├── deep-research/                    # COPIED from upstream
│   ├── agents/                       # Frontmatter + tool-refs modified
│   └── references/                   # Unmodified
├── academic-paper/                   # COPIED from upstream
│   ├── agents/                       # Frontmatter + tool-refs modified
│   └── references/                   # Unmodified
├── academic-paper-reviewer/          # COPIED from upstream
│   ├── agents/                       # Frontmatter + tool-refs modified
│   └── references/                   # Unmodified
├── academic-pipeline/                # COPIED from upstream
│   ├── agents/                       # Frontmatter + tool-refs modified
│   └── references/                   # Unmodified
├── shared/                           # COPIED verbatim
│   ├── handoff_schemas.md
│   ├── contracts/*.json
│   └── references/*.md
├── scripts/                          # COPIED verbatim (172 files)
├── tests/fixtures/                   # COPIED verbatim
├── docs/
│   ├── ARCHITECTURE.md               # COPIED verbatim
│   ├── PERFORMANCE.md                # COPIED verbatim
│   └── SETUP.md                      # OpenCode-specific (NEW)
├── MODE_REGISTRY.md                  # COPIED verbatim
├── SYNC.md                           # Sync protocol (NEW)
└── README.md                         # OpenCode-native (NEW)
```

---

## Task 1: Create Sibling Repo & Initialize

**Files:**
- Create: `ars-opencode/` (root directory)
- Create: `ars-opencode/opencode.json`
- Create: `ars-opencode/.opencode/CLAUDE.md`
- Create: `ars-opencode/.gitignore`
- Create: `ars-opencode/README.md`
- Create: `ars-opencode/SYNC.md`
- Create: `ars-opencode/docs/SETUP.md`

- [ ] **Step 1: Create the repo directory and .gitignore**

```bash
mkdir -p /tmp/ars-opencode
mkdir -p /tmp/ars-opencode/.opencode
mkdir -p /tmp/ars-opencode/docs
mkdir -p /tmp/ars-opencode/hooks
mkdir -p /tmp/ars-opencode/commands
mkdir -p /tmp/ars-opencode/skills/ars-meta
mkdir -p /tmp/ars-opencode/skills/ars-deep-research
mkdir -p /tmp/ars-opencode/skills/ars-academic-paper
mkdir -p /tmp/ars-opencode/skills/ars-reviewer
mkdir -p /tmp/ars-opencode/skills/ars-pipeline

cat > /tmp/ars-opencode/.gitignore << 'EOF'
__pycache__/
*.pyc
.DS_Store
*.egg-info/
dist/
build/
.pytest_cache/
*.log
.venv/
venv/
EOF
```

- [ ] **Step 2: Create opencode.json**

```json
{
  "name": "academic-research-skills",
  "version": "3.9.4.2-oc",
  "description": "OpenCode port of Academic Research Skills — full research pipeline from literature search to publication",
  "skills": {
    "ars-meta": "skills/ars-meta/SKILL.md",
    "ars-deep-research": "skills/ars-deep-research/SKILL.md",
    "ars-academic-paper": "skills/ars-academic-paper/SKILL.md",
    "ars-reviewer": "skills/ars-reviewer/SKILL.md",
    "ars-pipeline": "skills/ars-pipeline/SKILL.md"
  },
  "commands": {
    "ars-full": "commands/ars-full.md",
    "ars-plan": "commands/ars-plan.md",
    "ars-review": "commands/ars-review.md",
    "ars-lit-review": "commands/ars-lit-review.md",
    "ars-socratic": "commands/ars-socratic.md",
    "ars-systematic-review": "commands/ars-systematic-review.md",
    "ars-fact-check": "commands/ars-fact-check.md",
    "ars-reviewer": "commands/ars-reviewer.md",
    "ars-revision": "commands/ars-revision.md",
    "ars-abstract": "commands/ars-abstract.md",
    "ars-disclosure": "commands/ars-disclosure.md",
    "ars-format": "commands/ars-format.md",
    "ars-calibrate": "commands/ars-calibrate.md"
  },
  "init": "hooks/ars-init.md"
}
```

Write to `/tmp/ars-opencode/opencode.json`.

- [ ] **Step 3: Create .opencode/CLAUDE.md (thin routing reference)**

```markdown
# ARS OpenCode — Master Routing

**ARS** provides academic research skills for OpenCode. 5 skills, 13 commands.

## Skills

| Skill | Purpose |
|---|---|
| `ars-meta` | Auto-routing — invoke this first for guided dispatch |
| `ars-deep-research` | Literature search, systematic review, fact-checking |
| `ars-academic-paper` | Paper writing, formatting, revision |
| `ars-reviewer` | Peer review, calibration |
| `ars-pipeline` | 10-stage full pipeline orchestrator |

## Commands

| Command | Skill | Mode |
|---|---|---|
| `/ars-full` | ars-pipeline | Full pipeline (ultrabrain) |
| `/ars-plan` | ars-academic-paper | Plan mode (deep) |
| `/ars-review` | ars-reviewer | Review mode (deep) |
| `/ars-lit-review` | ars-deep-research | Lit review mode (deep) |
| `/ars-socratic` | ars-deep-research | Socratic mode (ultrabrain) |
| `/ars-systematic-review` | ars-deep-research | Systematic review (ultrabrain) |
| `/ars-fact-check` | ars-deep-research | Fact-check mode (deep) |
| `/ars-reviewer` | ars-reviewer | Full review (ultrabrain) |
| `/ars-revision` | ars-academic-paper | Revision mode (deep) |
| `/ars-abstract` | ars-academic-paper | Abstract mode (deep) |
| `/ars-disclosure` | ars-academic-paper | Disclosure mode (deep) |
| `/ars-format` | ars-academic-paper | Format convert (quick) |
| `/ars-calibrate` | ars-reviewer | Calibration (ultrabrain) |

## Usage

Start with: `skill(name="ars-meta")` — the meta-skill routes to the correct sub-skill based on your intent.

Or invoke directly: `skill(name="ars-<skill-name>")`
```

Write to `/tmp/ars-opencode/.opencode/CLAUDE.md`.

- [ ] **Step 4: Create README.md**

```markdown
# Academic Research Skills for OpenCode

[![Version](https://img.shields.io/badge/version-v3.9.4.2-oc-blue)](https://github.com/your-org/ars-opencode)

A comprehensive suite of OpenCode skills for academic research, covering the full pipeline from research to publication.

**Port of:** [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) v3.9.4.2

## Quick Start

Load the meta-skill to get auto-routed:
```
skill(name="ars-meta")
```

Or invoke a specific skill directly:
```
skill(name="ars-deep-research")
skill(name="ars-academic-paper")
skill(name="ars-reviewer")
skill(name="ars-pipeline")
```

Or use a command:
```
/ars-plan    # Start with paper planning
/ars-review  # Review a paper
/ars-full    # Run the full pipeline
```

## What's Here

- **Deep Research** — Literature search, systematic review, fact-checking, Socratic dialogue
- **Academic Paper** — Writing, formatting (APA/Chicago/MLA/IEEE/Vancouver), revision
- **Academic Paper Reviewer** — Multi-perspective peer review with 0-100 rubrics
- **Academic Pipeline** — 10-stage orchestrator from research to publication

See `docs/ARCHITECTURE.md` for full pipeline details. See `docs/SETUP.md` for prerequisites.

## Documentation

- `docs/ARCHITECTURE.md` — Full pipeline reference
- `docs/PERFORMANCE.md` — Token budgets and cost estimates
- `docs/SETUP.md` — Prerequisites and setup
- `MODE_REGISTRY.md` — All 25 modes across 4 skills
- `SYNC.md` — Upstream sync protocol

## License

CC-BY-NC 4.0 — same as upstream.
```

Write to `/tmp/ars-opencode/README.md`.

- [ ] **Step 5: Create SYNC.md**

```markdown
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
```

Write to `/tmp/ars-opencode/SYNC.md`.

- [ ] **Step 6: Create docs/SETUP.md**

```markdown
# Setup

## Prerequisites

- Python 3.9+ with `pip`
- Optional: Pandoc for DOCX output
- Optional: tectonic + Source Han Serif TC for PDF output

## Install the suite

Clone the repo:
```bash
git clone https://github.com/your-org/ars-opencode.git
```

OpenCode auto-discovers `opencode.json` at the repo root — skills and commands are available immediately.

## Python dependencies

Some lint scripts and tests require Python packages:
```bash
pip install -r requirements-dev.txt
```

## API keys (optional)

Some features (Semantic Scholar API, Crossref) benefit from API keys for higher rate limits. Set them as environment variables:
```bash
export S2_API_KEY=your_key_here
export CROSSREF_MAILTO=your@email.com
export ARS_CROSS_MODEL=true
```

See upstream `docs/SETUP.md` for full API key documentation.
```

Write to `/tmp/ars-opencode/docs/SETUP.md`.

- [ ] **Step 7: Initialize git repo**

```bash
cd /tmp/ars-opencode && git init && git add -A && git commit -m "chore: initialize repo structure"
```

Verify: `git log --oneline` shows one commit.

---

## Task 2: Copy Core ARS Content (Layer 2)

**Files:** Multiple directories from upstream source (path: `/Users/tiger/Desktop/OpenSource/academic-research-skills/`)

- [ ] **Step 1: Copy 4 skill directories (agents/ + references/)**

```bash
# Source path
SRC=/Users/tiger/Desktop/OpenSource/academic-research-skills
DST=/tmp/ars-opencode

# Copy each skill directory's agents and references
for skill in deep-research academic-paper academic-paper-reviewer academic-pipeline; do
  cp -r "$SRC/$skill/agents" "$DST/$skill/agents"
  cp -r "$SRC/$skill/references" "$DST/$skill/references"
done
```

Verify each target exists:
```bash
for skill in deep-research academic-paper academic-paper-reviewer academic-pipeline; do
  echo "$skill agents: $(ls $DST/$skill/agents/*.md 2>/dev/null | wc -l | tr -d ' ') files"
  echo "$skill references: $(ls $DST/$skill/references/*.md 2>/dev/null | wc -l | tr -d ' ') files"
done
```

Expected: Each skill shows >0 agent files and >0 reference files.

- [ ] **Step 2: Copy shared/, scripts/, tests/, docs/**

```bash
cp -r "$SRC/shared" "$DST/shared"
cp -r "$SRC/scripts" "$DST/scripts"
cp -r "$SRC/tests" "$DST/tests"
cp "$SRC/conftest.py" "$DST/conftest.py"
cp "$SRC/requirements-dev.txt" "$DST/requirements-dev.txt"
cp "$SRC/MODE_REGISTRY.md" "$DST/MODE_REGISTRY.md"

# Docs (selective — skip CLAUDE.md and plugin-specific files)
cp "$SRC/docs/ARCHITECTURE.md" "$DST/docs/ARCHITECTURE.md"
cp "$SRC/docs/PERFORMANCE.md" "$DST/docs/PERFORMANCE.md"
# Optionally copy design docs for reference
cp -r "$SRC/docs/design" "$DST/docs/design"
```

Verify: Check key files exist:
```bash
ls "$DST/shared/handoff_schemas.md" && echo "shared OK"
ls "$DST/scripts/check_spec_consistency.py" && echo "scripts OK"
ls "$DST/conftest.py" && echo "conftest OK"
ls "$DST/MODE_REGISTRY.md" && echo "MODE_REGISTRY OK"
```

- [ ] **Step 3: Copy .github/workflows/ for CI**

```bash
cp -r "$SRC/.github" "$DST/.github"
```

This copies: `spec-consistency.yml`, `pytest.yml`, `test-count-monotonic.yml`, `release-cooldown.yml`.

Verify: `ls "$DST/.github/workflows/"` shows 4+ workflow files.

- [ ] **Step 4: Copy docs/design/ (design history)**

```bash
cp -r "$SRC/docs/design" "$DST/docs/design"
```

- [ ] **Step 5: Commit Layer 2 content**

```bash
cd /tmp/ars-opencode && git add -A && git commit -m "feat: copy core ARS content (agent prompts, scripts, schemas, tests)"
```

---

## Task 3: Transform Agent Frontmatter & Tool References

**Files modified:** `**/agents/*.md` across all 4 skill directories (~30 files)

- [ ] **Step 1: Remove `model:` frontmatter field from all agent files**

```bash
cd /tmp/ars-opencode

# Remove model: sonnet, model: opus, model: inherit from agent frontmatter
for f in $(find deep-research academic-paper academic-paper-reviewer academic-pipeline -path '*/agents/*.md'); do
  # Use sed to remove the model: line from frontmatter (between --- markers)
  sed -i '' '/^model: /d' "$f"
done
```

Verify no remaining model fields:
```bash
grep -rn '^model: ' deep-research academic-paper academic-paper-reviewer academic-pipeline --include='*.md'
```

Expected: No output (0 matches).

- [ ] **Step 2: Replace WebSearch → websearch in agent bodies**

```bash
cd /tmp/ars-opencode
find deep-research academic-paper academic-paper-reviewer academic-pipeline -path '*/agents/*.md' -exec \
  sed -i '' 's/WebSearch/websearch/g' {} +
```

Verify transformation:
```bash
grep -rn '\bWebSearch\b' deep-research academic-paper academic-paper-reviewer academic-pipeline --include='*.md'
```

Expected: No output (0 matches). Verify lowercase version exists:
```bash
grep -rn '\bwebsearch\b' deep-research academic-paper academic-paper-reviewer academic-pipeline --include='*.md' | head -5
```

Expected: 5+ matches.

- [ ] **Step 3: Replace WebFetch → webfetch in agent bodies**

```bash
cd /tmp/ars-opencode
find deep-research academic-paper academic-paper-reviewer academic-pipeline -path '*/agents/*.md' -exec \
  sed -i '' 's/WebFetch/webfetch/g' {} +
```

Verify:
```bash
grep -rn '\bWebFetch\b' deep-research academic-paper academic-paper-reviewer academic-pipeline --include='*.md'
```

Expected: No output.

- [ ] **Step 4: Remove CC-specific runtime references (agent bodies only)**

Target patterns: "Claude Code" (as runtime name), "the Agent tool" (for dispatch), "ANTHROPIC_API_KEY"

```bash
cd /tmp/ars-opencode

# Replace "Claude Code" → "OpenCode" in agent bodies (not frontmatter)
find deep-research academic-paper academic-paper-reviewer academic-pipeline -path '*/agents/*.md' -exec \
  sed -i '' 's/Claude Code/OpenCode/g' {} +

# Replace "Claude" as runtime → "OpenCode" (careful: this also matches "Claude" in academic context)
# Conservative: only replace when preceded by "in " or "via " or "using "
find deep-research academic-paper academic-paper-reviewer academic-pipeline -path '*/agents/*.md' -exec \
  sed -i '' 's/in Claude /in OpenCode /g' {} +
find deep-research academic-paper academic-paper-reviewer academic-pipeline -path '*/agents/*.md' -exec \
  sed -i '' 's/via Claude /via OpenCode /g' {} +
find deep-research academic-paper academic-paper-reviewer academic-pipeline -path '*/agents/*.md' -exec \
  sed -i '' 's/using Claude /using OpenCode /g' {} +
```

Verify changes are conservative (no over-matching):
```bash
grep -rn '\bClaude\b' deep-research academic-paper academic-paper-reviewer academic-pipeline --include='*.md'
```

Expected: Some matches may remain if "Claude" appears in academic context (e.g., Claude Shannon, Claude Monet) — these are correct to keep.

- [ ] **Step 5: Remove "the Agent tool" references from dispatch sections**

```bash
cd /tmp/ars-opencode
find deep-research academic-paper academic-paper-reviewer academic-pipeline -path '*/agents/*.md' -exec \
  sed -i '' 's/the Agent tool/the task() function/g' {} +
find deep-research academic-paper academic-paper-reviewer academic-pipeline -path '*/agents/*.md' -exec \
  sed -i '' 's/Agent tool/task()/g' {} +
```

Verify: `grep -rn 'Agent tool' deep-research academic-paper academic-paper-reviewer academic-pipeline --include='*.md'` — expect 0 matches.

- [ ] **Step 6: Remove "ANTHROPIC_API_KEY" references**

```bash
cd /tmp/ars-opencode
find deep-research academic-paper academic-paper-reviewer academic-pipeline -path '*/agents/*.md' -exec \
  sed -i '' 's/ANTHROPIC_API_KEY/API_KEY/g' {} +
```

Verify: `grep -rn 'ANTHROPIC_API_KEY' . --include='*.md'` — expect 0 matches.

- [ ] **Step 7: Commit transformations**

```bash
cd /tmp/ars-opencode && git add -A && git commit -m "fix: remove CC-specific frontmatter, tool names, and runtime references"
```

---

## Task 4: Create SKILL.md Files (Layer 1 — OpenCode Dispatch)

**Files created:**
- Create: `skills/ars-meta/SKILL.md`
- Create: `skills/ars-deep-research/SKILL.md`
- Create: `skills/ars-academic-paper/SKILL.md`
- Create: `skills/ars-reviewer/SKILL.md`
- Create: `skills/ars-pipeline/SKILL.md`

These replace CC's SKILL.md files with OpenCode-native format using `task(category=..., load_skills=[...])` dispatch.

- [ ] **Step 1: Create ars-meta/SKILL.md (routing meta-skill)**

```markdown
# ars-meta: ARS Router Skill

Auto-routes user intent to the correct ARS sub-skill.

## Trigger Keywords

- Full pipeline: "write a research paper", "full pipeline", "start research", "complete paper"
- Deep research: "research topic", "literature review", "find papers", "search literature", "systematic review"
- Academic paper: "write paper", "draft manuscript", "outline paper", "format citations", "write abstract"
- Review: "review paper", "peer review", "review manuscript", "reviewer comments"
- Quick: "quick brief", "fact check", "citation check", "check references"

## Dispatch Logic

| User Intent | Load Skill |
|---|---|
| Full pipeline | `skill(name="ars-pipeline")` |
| Literature / research | `skill(name="ars-deep-research")` |
| Writing / formatting | `skill(name="ars-academic-paper")` |
| Peer review | `skill(name="ars-reviewer")` |
| Quick / specific | Direct to sub-skill quick mode |

## Fallback

When intent is ambiguous, route to `ars-pipeline` — the orchestrator will guide the user through sub-skill selection.
```

Write to `/tmp/ars-opencode/skills/ars-meta/SKILL.md`.

- [ ] **Step 2: Create ars-deep-research/SKILL.md**

This skill wraps the CC `deep-research/SKILL.md` with OpenCode-native dispatch. Key changes:
- Frontmatter: remove `model:` field
- Dispatch: `Agent tool → synthesis_agent` → `task(category="ultrabrain", load_skills=["ars-deep-research", "nature-writing"], ...)`
- Tool refs: `WebSearch` → `websearch`

```markdown
# ars-deep-research

OpenCode ported skill: Deep Research — literature search, systematic review, fact-checking, Socratic dialogue.

**Based on:** `deep-research/SKILL.md` from upstream v3.9.4.2
**Version:** 2.8 (upstream)
**Status:** active
**Data access level:** verified_only
**Task type:** open-ended
**Related skills:** ars-academic-paper, ars-pipeline

## Modes

| Mode | Category | Description |
|---|---|---|
| full | ultrabrain | Full multi-agent research team |
| quick | deep | Rapid brief |
| review | deep | Research quality review |
| lit-review | deep | Literature review |
| fact-check | deep | Fact-checking claims |
| socratic | ultrabrain | Socratic guided research |
| systematic-review | ultrabrain | PRISMA systematic review |

## Trigger Keywords

- Research: "research", "literature review", "find papers on", "search for studies"
- Socratic: "guide my research", "help me think through", "explore topic"
- Systematic: "systematic review", "PRISMA"
- Fact-check: "fact check", "verify claims"
- Quick: "quick brief", "summarize research on"

## Dispatch

### Full Mode
```text
task(
  category="ultrabrain",
  load_skills=["ars-deep-research", "nature-academic-search"],
  prompt="Run deep-research full mode. Start by assembling the research team..."
)
```

### Quick Mode
```text
task(
  category="deep",
  load_skills=["ars-deep-research"],
  prompt="Run deep-research quick mode. Provide a concise brief on..."
)
```

### Socratic Mode
```text
task(
  category="ultrabrain",
  load_skills=["ars-deep-research", "nature-writing"],
  prompt="Run deep-research socratic mode. Begin Socratic dialogue..."
)
```

### Systematic Review Mode
```text
task(
  category="ultrabrain",
  load_skills=["ars-deep-research", "nature-academic-search"],
  prompt="Run deep-research systematic-review mode. Follow PRISMA protocol..."
)
```

### Fact-Check Mode
```text
task(
  category="deep",
  load_skills=["ars-deep-research", "nature-academic-search"],
  prompt="Run deep-research fact-check mode. Verify the following claims..."
)
```

### Lit-Review Mode
```text
task(
  category="deep",
  load_skills=["ars-deep-research", "nature-academic-search", "nature-writing"],
  prompt="Run deep-research lit-review mode. Conduct literature review on..."
)
```

### Review Mode
```text
task(
  category="deep",
  load_skills=["ars-deep-research", "nature-citation"],
  prompt="Run deep-research review mode. Review the research quality of..."
)
```

## Key References

- `deep-research/agents/` — 13 agent prompts (instructions, patterns, anti-patterns)
- `deep-research/references/` — Socratic framework, search strategy templates
- `shared/handoff_schemas.md` — Cross-skill data contracts
```

Write to `/tmp/ars-opencode/skills/ars-deep-research/SKILL.md`.

- [ ] **Step 3: Create ars-academic-paper/SKILL.md**

```markdown
# ars-academic-paper

OpenCode ported skill: Academic Paper — writing, formatting, revision, citation management.

**Based on:** `academic-paper/SKILL.md` from upstream v3.9.4.2
**Version:** 3.0 (upstream)
**Status:** active
**Data access level:** verified_only
**Task type:** open-ended
**Related skills:** ars-deep-research, ars-pipeline, ars-reviewer

## Modes

| Mode | Category | Description |
|---|---|---|
| full | ultrabrain | Full paper writing pipeline |
| plan | deep | Socratic guided planning |
| outline-only | deep | Paper outline generation |
| revision | deep | Incorporate reviewer feedback |
| revision-coach | ultrabrain | Parse reviewer comments into roadmap |
| abstract-only | deep | Abstract writing |
| lit-review | deep | Literature review paper |
| format-convert | quick | Citation format conversion |
| citation-check | deep | Citation verification |
| disclosure | deep | AI disclosure statement generation |

## Trigger Keywords

- Writing: "write a paper", "draft manuscript", "write about"
- Planning: "help me outline", "guide my paper", "plan my paper"
- Abstract: "write abstract", "draft abstract"
- Revision: "reviewer comments", "revise paper", "revision"
- Format: "convert citations", "change format", "APA", "IEEE", "MLA"
- Citation: "check citations", "verify references"
- Disclosure: "AI disclosure", "disclosure statement"

## Dispatch

### Full Mode
```text
task(
  category="ultrabrain",
  load_skills=["ars-academic-paper", "ars-deep-research", "nature-writing", "nature-citation"],
  prompt="Run academic-paper full mode. Start the paper writing pipeline..."
)
```

### Plan Mode
```text
task(
  category="deep",
  load_skills=["ars-academic-paper", "nature-writing"],
  prompt="Run academic-paper plan mode. Guide the user through paper structure..."
)
```

### Format Convert Mode
```text
task(
  category="quick",
  load_skills=["ars-academic-paper"],
  prompt="Run academic-paper format-convert mode. Convert citations to the requested format..."
)
```

### Disclosure Mode
```text
task(
  category="deep",
  load_skills=["ars-academic-paper"],
  prompt="Run academic-paper disclosure mode. Generate an AI disclosure statement for..."
)
```

## Key References

- `academic-paper/agents/` — 12 agent prompts
- `academic-paper/references/` — Writing guides, format templates, style calibration
- `shared/handoff_schemas.md` — Cross-skill data contracts
```

Write to `/tmp/ars-opencode/skills/ars-academic-paper/SKILL.md`.

- [ ] **Step 4: Create ars-reviewer/SKILL.md**

```markdown
# ars-reviewer

OpenCode ported skill: Academic Paper Reviewer — multi-perspective peer review.

**Based on:** `academic-paper-reviewer/SKILL.md` from upstream v3.9.4.2
**Version:** 1.8 (upstream)
**Status:** active
**Data access level:** verified_only
**Task type:** open-ended
**Related skills:** ars-academic-paper, ars-pipeline

## Modes

| Mode | Category | Description |
|---|---|---|
| full | ultrabrain | EIC + R1/R2/R3 + Devil's Advocate |
| quick | deep | Rapid assessment |
| guided | deep | Socratic improvement guidance |
| methodology-focus | deep | Methodology-focused review |
| re-review | ultrabrain | Verify revisions |
| calibration | ultrabrain | Calibrate against gold set |

## Trigger Keywords

- Review: "review this paper", "peer review", "review manuscript"
- Re-review: "re-review", "verify revisions", "check revision"
- Calibration: "calibrate", "gold set"
- Guided: "how to improve", "guide me to improve"
- Methodology: "check methodology", "methodology review"

## Dispatch

### Full Mode
```text
task(
  category="ultrabrain",
  load_skills=["ars-reviewer"],
  prompt="Run academic-paper-reviewer full mode. Assemble the review panel..."
)
```

### Quick Mode
```text
task(
  category="deep",
  load_skills=["ars-reviewer"],
  prompt="Run academic-paper-reviewer quick mode. Provide a rapid assessment..."
)
```

### Calibration Mode
```text
task(
  category="ultrabrain",
  load_skills=["ars-reviewer"],
  prompt="Run academic-paper-reviewer calibration mode. Calibrate against the user's gold set..."
)
```

## Key References

- `academic-paper-reviewer/agents/` — 7 agent prompts
- `academic-paper-reviewer/references/` — Journal lists, review rubrics
- `shared/handoff_schemas.md` — Cross-skill data contracts

## Scoring

| Score | Decision |
|---|---|
| ≥80 | Accept |
| 65-79 | Minor Revision |
| 50-64 | Major Revision |
| <50 | Reject |
```

Write to `/tmp/ars-opencode/skills/ars-reviewer/SKILL.md`.

- [ ] **Step 5: Create ars-pipeline/SKILL.md**

```markdown
# ars-pipeline

OpenCode ported skill: Academic Pipeline — 10-stage orchestrated research-to-publication workflow.

**Based on:** `academic-pipeline/SKILL.md` from upstream v3.9.4.2
**Version:** 3.7 (upstream)
**Status:** active
**Data access level:** verified_only
**Task type:** open-ended
**Related skills:** ars-deep-research, ars-academic-paper, ars-reviewer

## Modes

| Mode | Category | Description |
|---|---|---|
| full | ultrabrain | Full 10-stage pipeline |
| mid-entry-review | ultrabrain | Enter at Stage 2.5 (integrity first) |
| mid-entry-revision | ultrabrain | Enter at Stage 4 (respond to reviews) |

## Trigger Keywords

- Pipeline: "full pipeline", "complete paper", "write research paper", "start to finish"
- Mid-entry: "review this paper", "I have a paper", "already have a draft"
- Revision: "I got reviews", "reviewer feedback", "revise and resubmit"

## Dispatch

### Full Pipeline
```text
task(
  category="ultrabrain",
  load_skills=["ars-pipeline", "ars-deep-research", "ars-academic-paper", "ars-reviewer", "nature-writing", "nature-citation"],
  prompt="Run the full academic research pipeline. Start from Stage 1..."
)
```

### Mid-Entry Review
```text
task(
  category="ultrabrain",
  load_skills=["ars-pipeline", "ars-reviewer"],
  prompt="Run academic-pipeline mid-entry at Stage 2.5. Verify integrity of the provided paper..."
)
```

### Mid-Entry Revision
```text
task(
  category="ultrabrain",
  load_skills=["ars-pipeline", "ars-academic-paper", "ars-reviewer"],
  prompt="Run academic-pipeline mid-entry at Stage 4. Process reviewer comments..."
)
```

## Pipeline Stages

| Stage | Name | Key Agents |
|---|---|---|
| 1 | RESEARCH | research_architect, literature_strategist, bibliography |
| 2 | WRITE | synthesis, draft_writer, visualization |
| 2.5 | INTEGRITY CHECK | integrity_verification (MANDATORY) |
| 3 | REVIEW | EIC + R1/R2/R3 + DA |
| 3' | RE-REVIEW | verification panel |
| 4 | REVISE | revision_coach, draft_writer |
| 4.5 | INTEGRITY CHECK | integrity_verification (MANDATORY) |
| 5 | FINALIZE | formatter, citation_compliance |
| 6 | SUMMARY | collaboration_depth_observer |

## Key References

- `academic-pipeline/agents/` — Orchestrator and stage agents
- `academic-pipeline/references/` — Pipeline protocols, integrity checklists
- `shared/handoff_schemas.md` — Cross-skill handoff contracts (S1-S13)
```

Write to `/tmp/ars-opencode/skills/ars-pipeline/SKILL.md`.

- [ ] **Step 6: Create hooks/ars-init.md (session init)**

```markdown
# ARS Session Initialization

ARS (Academic Research Skills) is loaded. Available:

## Skills
- `ars-meta` — Auto-routing (recommended start point)
- `ars-deep-research` — Literature search, systematic review, fact-checking
- `ars-academic-paper` — Paper writing, formatting, citation management
- `ars-reviewer` — Multi-perspective peer review
- `ars-pipeline` — Full 10-stage research pipeline

## Commands (13 total)
`/ars-full`, `/ars-plan`, `/ars-review`, `/ars-lit-review`, `/ars-socratic`,
`/ars-systematic-review`, `/ars-fact-check`, `/ars-reviewer`, `/ars-revision`,
`/ars-abstract`, `/ars-disclosure`, `/ars-format`, `/ars-calibrate`

## Quick Start
- `skill(name="ars-meta")` — let me route you to the right skill
- `/ars-plan` — start planning a paper structure
- `/ars-lit-review "topic"` — quick literature review

## Token Budget
- Full pipeline: ~$4-6 (15k word paper)
- Individual skills: $1-3 per session
- See `docs/PERFORMANCE.md` for detailed estimates
```

Write to `/tmp/ars-opencode/hooks/ars-init.md`.

- [ ] **Step 8: Commit all Layer 1 files**

```bash
cd /tmp/ars-opencode && git add -A && git commit -m "feat: add OpenCode skills, hooks, and meta-skill"
```

---

## Task 5: Create 13 Command Dispatchers

**Files created:** `commands/ars-*.md` (13 files)

All 13 commands follow the same pattern — a markdown file that loads the appropriate skill and dispatches via `task()`.

- [ ] **Step 1: Create ars-full.md (ultrabrain — full pipeline)**

```markdown
# ars-full

Triggers the full academic research pipeline.

## Execution

Load the pipeline orchestrator:
```
skill(name="ars-pipeline")
```

Then dispatch full mode:
```text
task(
  category="ultrabrain",
  load_skills=["ars-pipeline", "ars-deep-research", "ars-academic-paper", "ars-reviewer", "nature-writing", "nature-citation"],
  prompt="Run the full academic research pipeline. Start from Stage 1: RESEARCH. Assemble the research team..."
)
```
```

Write to `/tmp/ars-opencode/commands/ars-full.md`.

- [ ] **Step 2: Create ars-plan.md (deep — guided planning)**

```markdown
# ars-plan

Start a guided Socratic dialogue to plan a paper structure.

## Execution

```
skill(name="ars-academic-paper")
```

```text
task(
  category="deep",
  load_skills=["ars-academic-paper", "nature-writing"],
  prompt="Run academic-paper plan mode. Guide the user through their paper structure via Socratic dialogue..."
)
```
```

Write to `/tmp/ars-opencode/commands/ars-plan.md`.

- [ ] **Step 3: Create ars-review.md (deep — research quality review)**

```markdown
# ars-review

Review the research quality of a paper or topic.

## Execution

```
skill(name="ars-deep-research")
```

```text
task(
  category="deep",
  load_skills=["ars-deep-research", "nature-citation"],
  prompt="Run deep-research review mode. Review the research quality of the provided topic..."
)
```
```

Write to `/tmp/ars-opencode/commands/ars-review.md`.

- [ ] **Step 4: Create ars-lit-review.md (deep — literature review)**

```markdown
# ars-lit-review

Conduct a literature review on a topic.

## Execution

```
skill(name="ars-deep-research")
```

```text
task(
  category="deep",
  load_skills=["ars-deep-research", "nature-academic-search", "nature-writing"],
  prompt="Run deep-research lit-review mode. Conduct a literature review on the specified topic..."
)
```
```

Write to `/tmp/ars-opencode/commands/ars-lit-review.md`.

- [ ] **Step 5: Create ars-socratic.md (ultrabrain — Socratic dialogue)**

```markdown
# ars-socratic

Engage in Socratic guided research dialogue.

## Execution

```
skill(name="ars-deep-research")
```

```text
task(
  category="ultrabrain",
  load_skills=["ars-deep-research", "nature-writing"],
  prompt="Run deep-research socratic mode. Begin Socratic dialogue to explore the research topic..."
)
```
```

Write to `/tmp/ars-opencode/commands/ars-socratic.md`.

- [ ] **Step 6: Create ars-systematic-review.md (ultrabrain — PRISMA)**

```markdown
# ars-systematic-review

Conduct a PRISMA systematic review.

## Execution

```
skill(name="ars-deep-research")
```

```text
task(
  category="ultrabrain",
  load_skills=["ars-deep-research", "nature-academic-search"],
  prompt="Run deep-research systematic-review mode. Follow the PRISMA protocol for systematic review..."
)
```
```

Write to `/tmp/ars-opencode/commands/ars-systematic-review.md`.

- [ ] **Step 7: Create ars-fact-check.md (deep — claim verification)**

```markdown
# ars-fact-check

Fact-check specific claims or statements.

## Execution

```
skill(name="ars-deep-research")
```

```text
task(
  category="deep",
  load_skills=["ars-deep-research", "nature-academic-search"],
  prompt="Run deep-research fact-check mode. Verify the following claims..."
)
```
```

Write to `/tmp/ars-opencode/commands/ars-fact-check.md`.

- [ ] **Step 8: Create ars-reviewer.md (ultrabrain — full peer review)**

```markdown
# ars-reviewer

Run a full multi-perspective peer review (EIC + 3 reviewers + Devil's Advocate).

## Execution

```
skill(name="ars-reviewer")
```

```text
task(
  category="ultrabrain",
  load_skills=["ars-reviewer"],
  prompt="Run academic-paper-reviewer full mode. Assemble the review panel (EIC + R1/R2/R3 + Devil's Advocate)..."
)
```
```

Write to `/tmp/ars-opencode/commands/ars-reviewer.md`.

- [ ] **Step 9: Create ars-revision.md (deep — revision assistance)**

```markdown
# ars-revision

Help incorporate reviewer comments and revise the paper.

## Execution

```
skill(name="ars-academic-paper")
```

```text
task(
  category="deep",
  load_skills=["ars-academic-paper"],
  prompt="Run academic-paper revision mode. Review the reviewer comments and help revise the paper..."
)
```
```

Write to `/tmp/ars-opencode/commands/ars-revision.md`.

- [ ] **Step 10: Create ars-abstract.md (deep — abstract writing)**

```markdown
# ars-abstract

Write an abstract for a paper.

## Execution

```
skill(name="ars-academic-paper")
```

```text
task(
  category="deep",
  load_skills=["ars-academic-paper", "nature-writing"],
  prompt="Run academic-paper abstract-only mode. Write an abstract for the provided paper..."
)
```
```

Write to `/tmp/ars-opencode/commands/ars-abstract.md`.

- [ ] **Step 11: Create ars-disclosure.md (deep — AI disclosure)**

```markdown
# ars-disclosure

Generate AI disclosure statements for specific venues (NeurIPS, Nature, ICLR, etc.).

## Execution

```
skill(name="ars-academic-paper")
```

```text
task(
  category="deep",
  load_skills=["ars-academic-paper"],
  prompt="Run academic-paper disclosure mode. Generate an AI disclosure statement for the specified venue..."
)
```
```

Write to `/tmp/ars-opencode/commands/ars-disclosure.md`.

- [ ] **Step 12: Create ars-format.md (quick — citation format conversion)**

```markdown
# ars-format

Convert citations between formats (APA, Chicago, MLA, IEEE, Vancouver).

## Execution

```
skill(name="ars-academic-paper")
```

```text
task(
  category="quick",
  load_skills=["ars-academic-paper", "nature-citation"],
  prompt="Run academic-paper format-convert mode. Convert the citations to the requested format..."
)
```
```

Write to `/tmp/ars-opencode/commands/ars-format.md`.

- [ ] **Step 13: Create ars-calibrate.md (ultrabrain — reviewer calibration)**

```markdown
# ars-calibrate

Calibrate the reviewer against a user-supplied gold set.

## Execution

```
skill(name="ars-reviewer")
```

```text
task(
  category="ultrabrain",
  load_skills=["ars-reviewer"],
  prompt="Run academic-paper-reviewer calibration mode. Calibrate against the user's gold set..."
)
```
```

Write to `/tmp/ars-opencode/commands/ars-calibrate.md`.

- [ ] **Step 14: Commit all 13 commands**

```bash
cd /tmp/ars-opencode && git add commands/ && git commit -m "feat: add 13 ars-* command dispatchers"
```

---

## Task 6: Setup CI & Create Transform Script

**Files modified:**
- `.github/workflows/` (copied in Task 2, may need adjustment)
- Create: `scripts/transform-opencode.sh` (sync helper)
- Create: `.github/workflows/skill-lint.yml` (OpenCode-specific CI)

- [ ] **Step 1: Create transform-opencode.sh (reusable sync helper)**

This script re-applies OpenCode transformations after an upstream merge. It is the core automation for upstream sync.

```bash
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
    # Only apply to files that match the pattern
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

# 2. WebSearch → websearch
echo "[2/5] WebSearch → websearch..."
apply 'WebSearch' 'websearch' 'deep-research academic-paper academic-paper-reviewer academic-pipeline'

# 3. WebFetch → webfetch
echo "[3/5] WebFetch → webfetch..."
apply 'WebFetch' 'webfetch' 'deep-research academic-paper academic-paper-reviewer academic-pipeline'

# 4. Claude Code → OpenCode (runtime references)
echo "[4/5] Claude Code → OpenCode..."
apply 'Claude Code' 'OpenCode' 'deep-research academic-paper academic-paper-reviewer academic-pipeline'

# 5. Agent tool → task()
echo "[5/5] Agent tool → task()..."
apply 'the Agent tool' 'the task\(\) function' 'deep-research academic-paper academic-paper-reviewer academic-pipeline'
apply 'Agent tool' 'task()' 'deep-research academic-paper academic-paper-reviewer academic-pipeline'

echo ""
echo "=== $TRANSFORM_COUNT transformations applied ==="

if [ "${1:-}" = "--check" ]; then
  echo "=== Verification ==="
  # Check no CC-specific patterns remain
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
```

Write to `/tmp/ars-opencode/scripts/transform-opencode.sh` and make executable:
```bash
chmod +x /tmp/ars-opencode/scripts/transform-opencode.sh
```

- [ ] **Step 2: Verify transform script works**

```bash
cd /tmp/ars-opencode && ./scripts/transform-opencode.sh --check
```

Expected: "All clean." with 0 transformations applied (already clean from Task 3).

- [ ] **Step 3: Add OpenCode-specific CI workflow**

```yaml
# .github/workflows/skill-lint.yml
name: Skill Lint

on:
  push:
    branches: [main]
    paths:
      - 'skills/**/*.md'
      - 'commands/**/*.md'
  pull_request:
    paths:
      - 'skills/**/*.md'
      - 'commands/**/*.md'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check for CC-specific patterns
        run: |
          REMAINING=$(grep -rn '^model: ' deep-research academic-paper academic-paper-reviewer academic-pipeline --include='*.md' 2>/dev/null | wc -l)
          if [ "$REMAINING" -gt 0 ]; then
            echo "Found $REMAINING model: frontmatter fields (should be 0):"
            grep -rn '^model: ' deep-research academic-paper academic-paper-reviewer academic-pipeline --include='*.md'
            exit 1
          fi
      - name: Check for PascalCase tool names
        run: |
          WEBS=$(grep -rn '\bWebSearch\b' . --include='*.md' 2>/dev/null | wc -l)
          if [ "$WEBS" -gt 0 ]; then
            echo "Found $WEBS WebSearch references (should be websearch)"
            exit 1
          fi
```

Write to `/tmp/ars-opencode/.github/workflows/skill-lint.yml`.

- [ ] **Step 4: Fix any CC-specific scripts (run_codex_audit.sh)**

The file `scripts/run_codex_audit.sh` (1191 lines) has CC-specific codex invocation patterns. These don't affect functionality in OpenCode — the Python tests and lint scripts it orchestrates are platform-agnostic. Leave it as-is; it will produce harmless errors if invoked directly. Document this in README.

```bash
echo "Note: scripts/run_codex_audit.sh contains CC-specific codex audit patterns." >> /tmp/ars-opencode/README.md
echo "It will not work in OpenCode. Use individual Python lint scripts instead." >> /tmp/ars-opencode/README.md
```

- [ ] **Step 5: Commit CI and transform script**

```bash
cd /tmp/ars-opencode && git add scripts/transform-opencode.sh && git add .github/workflows/skill-lint.yml && git commit -m "ci: add transform script and OpenCode-specific CI lint"
```

---

## Task 7: Testing & Verification

- [ ] **Step 1: Install Python dependencies**

```bash
cd /tmp/ars-opencode && pip install -r requirements-dev.txt 2>&1 | tail -5
```

Expected: pyyaml, ruamel.yaml, jsonschema installed.

- [ ] **Step 2: Run Python test suite**

```bash
cd /tmp/ars-opencode && python3 -m pytest scripts/ -v 2>&1 | tail -20
```

Expected: Tests pass (or pre-existing failures noted — do not fix upstream test bugs).

- [ ] **Step 3: Verify no CC-specific frontmatter remains in agent files**

```bash
cd /tmp/ars-opencode
echo "=== model: field check ==="
grep -rn '^model: ' deep-research academic-paper academic-paper-reviewer academic-pipeline --include='*.md' || echo "CLEAN: no model: fields"
echo ""
echo "=== WebSearch check ==="
grep -rn '\bWebSearch\b' . --include='*.md' || echo "CLEAN: no WebSearch references"
echo ""
echo "=== WebFetch check ==="
grep -rn '\bWebFetch\b' . --include='*.md' || echo "CLEAN: no WebFetch references"
echo ""
echo "=== ANTHROPIC_API_KEY check ==="
grep -rn 'ANTHROPIC_API_KEY' . --include='*.md' || echo "CLEAN: no ANTHROPIC_API_KEY references"
```

All should show "CLEAN."

- [ ] **Step 4: Verify command dispatcher completeness**

```bash
cd /tmp/ars-opencode
echo "Command files: $(ls commands/ars-*.md | wc -l)"
echo "Expected: 13"
echo ""
echo "Command names from opencode.json:"
python3 -c "import json; c=json.load(open('opencode.json')); print('\n'.join(c.get('commands',{}).keys()))" 2>/dev/null || grep -o '"ars-[^"]*"' opencode.json
```

Verify 13 commands match.

- [ ] **Step 5: Verify skill file completeness**

```bash
cd /tmp/ars-opencode
echo "Skill directories: $(ls -d skills/ars-* 2>/dev/null | wc -l)"
echo "Skill SKILL.md files:"
ls skills/ars-*/SKILL.md
echo ""
echo "Expected: 5 skills (ars-meta, ars-deep-research, ars-academic-paper, ars-reviewer, ars-pipeline)"
```

Verify 5 skills.

- [ ] **Step 6: Final file structure audit**

```bash
cd /tmp/ars-opencode
echo "=== Required directories ==="
for d in .opencode skills commands hooks deep-research academic-paper academic-paper-reviewer academic-pipeline shared scripts tests docs; do
  [ -d "$d" ] && echo "  ✓ $d" || echo "  ✗ $d MISSING"
done
echo ""
echo "=== Required files ==="
for f in opencode.json README.md SYNC.md .gitignore MODE_REGISTRY.md conftest.py requirements-dev.txt docs/SETUP.md docs/ARCHITECTURE.md docs/PERFORMANCE.md .opencode/CLAUDE.md hooks/ars-init.md; do
  [ -f "$f" ] && echo "  ✓ $f" || echo "  ✗ $f MISSING"
done
echo ""
echo "=== Top-level structure ==="
ls -la
```

All directories and required files should be present.

- [ ] **Step 7: Commit any remaining changes**

```bash
cd /tmp/ars-opencode && git add -A && git status
```

If there are untracked files, commit:
```bash
cd /tmp/ars-opencode && git commit -m "chore: finalize repo structure"
```

- [ ] **Step 8: Final status check**

```bash
cd /tmp/ars-opencode && git log --oneline
```

Should show 7+ commits representing each task phase.

---

## Self-Review Checklist

**1. Spec coverage:** Cross-reference each design spec section against plan tasks.

| Spec § | What it requires | Plan task coverage |
|---|---|---|
| §1 Architecture (Hybrid Fork) | Sibling repo, two layers | Task 1 (repo), Task 2 (Layer 2 copy), Task 4 (Layer 1 skills) |
| §2 Skill Loading & Dispatch | 5 ars-* skills, SKILL.md adaptation | Task 4 (all 5 SKILL.md files) |
| §3 Tool Name Mapping | WebSearch→websearch, WebFetch→webfetch, model: removal | Task 3 (all transformations) + Task 6 (transform script) |
| §4 Command Routing | 13 command dispatchers, model→category mapping | Task 5 (13 dispatchers) |
| §5 Session Hooks & Plugin | opencode.json, .opencode/CLAUDE.md, hooks | Task 1 (opencode.json, CLAUDE.md), Task 4 (ars-init.md) |
| §6 Python Infra & CI | Copy scripts, adapt CI, transform script | Task 2 (copy), Task 6 (CI + transform) |
| §7 Sync Strategy | SYNC.md, merge approach, transform script | Task 1 (SYNC.md), Task 6 (transform-opencode.sh) |
| §8 Development Plan | 7 phases, 9-12 sessions | Covered by Tasks 1-7 |

**Gaps found:** None. All spec sections have corresponding tasks.

**2. Placeholder scan:**
- No "TBD", "TODO", "implement later" found.
- No "add appropriate error handling" — all code blocks are complete.
- No "write tests for the above" without actual code.
- All file paths are exact (`/tmp/ars-opencode/...`, `deep-research/agents/*.md`).
- All commands are complete with expected output.

**3. Type consistency:**
- Skill names: `ars-meta`, `ars-deep-research`, `ars-academic-paper`, `ars-reviewer`, `ars-pipeline` — consistent throughout.
- Category names: `ultrabrain`, `deep`, `quick` — consistent throughout.
- File paths: `commands/ars-*.md` — 13 files, all consistent naming.
- `opencode.json` skill/command names match the actual files.
