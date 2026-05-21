# ARS → OpenCode: Hybrid Fork Port Design

**Status:** Design draft (post-brainstorming, pre-implementation)
**Date:** 2026-05-21
**Target sibling repo:** `ars-opencode` (separate repo, matching existing Codex distribution pattern at `Imbad0202/academic-research-skills-codex`)
**Source upstream:** `Imbad0202/academic-research-skills` v3.9.4.2
**Scope:** Full port of all 4 skills (deep-research, academic-paper, academic-paper-reviewer, academic-pipeline) + 25 modes + 13 slash commands + session hooks + CLAUDE.md routing to OpenCode-native format. Core content (agent prompts, JSON schemas, Python scripts) copied unmodified; wrapping layer replaced with OpenCode-native dispatch.

**Out of scope:**
- Modification of agent prompt *instructional logic* (frontmatter metadata + tool-name case fixes are in-scope)
- Migration of CI/CD workflows to non-GitHub platforms
- Functional changes to the research/paper/review logic itself
- Adding new skills or modes
- Commercial licensing changes (CC-BY-NC 4.0 preserved)
- Breaking the upstream sync contract (see §7)

**Precedent docs:**
- `Imbad0202/academic-research-skills-codex` — existing Codex sibling repo, same port pattern
- `CONTRIBUTING.md` §Platform Ports — describes in-tree wrapper approach for platform ports
- `docs/ARCHITECTURE.md` — full pipeline reference
- `.claude/CLAUDE.md` — master routing document (236 lines) being adapted

---

## 1. Overall Architecture

### 1.1 Distribution Model: Sibling Repo (Hybrid Fork)

Three approaches were evaluated:

| Approach | Description | Verdict |
|---|---|---|
| In-tree wrapper (CONTRIBUTING.md pattern) | One `opencode/` dir in the main repo, auto-detected by platform | Rejected — pollutes CC repo with platform-specific files |
| Direct modification of existing files | Change CC files in-place for OpenCode compatibility | Rejected — breaks upstream sync |
| **Hybrid Fork** | Core content copied to new repo; OpenCode-native dispatch layer replaces the CC wrapping layer | **Chosen** — matches Codex sibling pattern, clean sync path |

### 1.2 Repo Structure

```
ars-opencode/
├── opencode.json                     # Plugin manifest (replaces .claude-plugin/)
├── .opencode/
│   └── CLAUDE.md                     # Master routing (replaces .claude/CLAUDE.md)
├── skills/
│   ├── ars-meta/SKILL.md             # New: meta-skill for routing
│   ├── ars-deep-research/SKILL.md    # Adapted from deep-research/SKILL.md
│   ├── ars-academic-paper/SKILL.md   # Adapted from academic-paper/SKILL.md
│   ├── ars-reviewer/SKILL.md         # Adapted from academic-paper-reviewer/SKILL.md
│   └── ars-pipeline/SKILL.md         # Adapted from academic-pipeline/SKILL.md
├── commands/                         # 13 /ars-* dispatchers (CC→OpenCode)
├── hooks/                            # Session init hooks (OpenCode-native)
├── deep-research/
│   ├── agents/*.md                   # Bodies unmodified; frontmatter + tool refs transformed
│   └── references/*.md               # Unmodified (reference files)
├── academic-paper/
│   ├── agents/*.md                   # Bodies unmodified; frontmatter + tool refs transformed
│   └── references/*.md               # Unmodified
├── academic-paper-reviewer/
│   ├── agents/*.md                   # Bodies unmodified; frontmatter + tool refs transformed
│   └── references/*.md               # Unmodified
├── academic-pipeline/
│   ├── agents/*.md                   # Bodies unmodified; frontmatter + tool refs transformed
│   └── references/*.md               # Unmodified
├── shared/
│   ├── handoff_schemas.md            # Unmodified (841 lines)
│   ├── contracts/*.json              # Unmodified (JSON Schemas)
│   └── references/*.md               # Unmodified
├── scripts/                          # Unmodified (172 Python files)
├── tests/
│   └── fixtures/                     # Unmodified
├── docs/
│   └── SETUP.md                      # OpenCode-specific setup guide
├── SYNC.md                           # Upstream sync protocol
└── README.md                         # OpenCode-native readme
```

### 1.3 Key Principle: Two Layers

```
Layer 1: OpenCode Dispatch (NEW - OpenCode-native)
  - opencode.json plugin manifest
  - skill() routing in .opencode/CLAUDE.md
  - 5 ars-* skills with task() dispatchers
  - 13 command wrappers
  - Session init hooks

Layer 2: Core ARS Content (instructional logic unmodified; frontmatter + tool-ref transforms applied)
  - Agent prompt bodies — instructional prose preserved, frontmatter `model:` fields removed,
    tool name casing updated (WebSearch→websearch, etc.) (~30 files touched, zero semantic change)
  - Python scripts (172 files) — unmodified
  - JSON schemas (15+ files) — unmodified
  - Reference materials — unmodified
  - Test fixtures — unmodified

Layer 2 is synced verbatim from upstream; the src-level transforms (frontmatter strip + tool-name case) are reapplied after each sync merge. Layer 1 is the sibling repo's unique contribution.

---

## 2. Skill Loading & Dispatch

### 2.1 Skill Renaming

| CC Skill Name | OpenCode Skill Name | Purpose |
|---|---|---|
| `deep-research` | `ars-deep-research` | Research team (13 agents, 7 modes) |
| `academic-paper` | `ars-academic-paper` | Paper writing (12 agents, 10 modes) |
| `academic-paper-reviewer` | `ars-reviewer` | Peer review (7 agents, 6 modes) |
| `academic-pipeline` | `ars-pipeline` | 10-stage orchestrator |
| (new) | `ars-meta` | Meta-skill: route user intent → sub-skill |

### 2.2 Meta-Skill Routing

`ars-meta/SKILL.md` detects user intent via trigger keywords and routes to the correct sub-skill:

```markdown
# ars-meta: ARS Router Skill

## Trigger Keywords
- Full pipeline: "write a research paper", "full pipeline", "start research"
- Research: "research topic", "literature review", "find papers"
- Writing: "write paper", "draft manuscript", "outline paper"
- Review: "review paper", "peer review", "review manuscript"
- Quick: "quick brief", "fact check", "citation check"

## Dispatch
On trigger → load the appropriate sub-skill via skill(name="ars-<skill>"):
  full pipeline → ars-pipeline
  research → ars-deep-research
  writing → ars-academic-paper
  review → ars-reviewer
  quick → sub-skill's quick mode
```

### 2.3 SKILL.md Adaptation

Each CC SKILL.md needs these changes:

| Field | CC Format | OpenCode Format |
|---|---|---|
| Frontmatter | `model: sonnet/opus` | Remove (OpenCode uses task() categories) |
| Frontmatter | `data_access_level`, `task_type` | Preserve (platform-agnostic metadata) |
| Frontmatter | `status: active` | Preserve |
| Frontmatter | `trigger_keywords` | Adapt to OpenCode skill routing format |
| Body: Dispatch | `Agent tool → synthesis_agent` | `task(category="ultrabrain", load_skills=[...], ...)` |
| Body: Tool refs | `WebSearch`, `WebFetch` | `websearch`, `webfetch` |
| Body: Tool refs | `Bash` | `bash` (no change needed) |
| Body: Tool refs | `Read`, `Write`, `Edit` | Same (OpenCode uses same names) |
| Body: Tool refs | `Glob` | `glob` |
| Body: Tool refs | `Grep` | `grep` |

**Count of files needing frontmatter model field removal:** ~30 agent files across 4 skills.
**Count of files needing tool name updates:** ~8 files with WebSearch/WebFetch references (pipeline agents primarily).

---

## 3. Tool Name Mapping

Claude Code and OpenCode share identical names for most tools. Divergences:

| Claude Code | OpenCode | Files Affected |
|---|---|---|
| `WebSearch` | `websearch` | `integrity_verification_agent.md`, `bibliography_agent.md`, others (~3-5 files) |
| `WebFetch` | `webfetch` | Same files as WebSearch (~3-5 files) |
| (no change) | (no change) | `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`, `Task` |

**Mechanical transformation:** case-only changes. These are find-and-replace in agent prompt bodies. OpenCode is case-sensitive for tool names; CC uses PascalCase.

### 3.1 Agent Tool Reference Audit

The following agents contain WebSearch/WebFetch references in their prompt bodies:

1. `academic-pipeline/agents/integrity_verification_agent.md` — WebSearch for reference verification
2. `deep-research/agents/bibliography_agent.md` — WebSearch for citation lookup
3. `deep-research/agents/literature_strategist_agent.md` — WebSearch for lit search
4. `deep-research/agents/synthesis_agent.md` — WebSearch for fact-checking
5. `academic-paper-reviewer/agents/devils_advocate_reviewer_agent.md` — WebSearch for counter-evidence
6. `academic-paper-reviewer/agents/reviewer_agent.md` — WebFetch for paper content when DOI provided

Additionally, any `model:` frontmatter field that specifies `sonnet` / `opus` / `inherit` must be removed from ~30 agent frontmatter blocks. OpenCode uses `task(category=...)` for model routing instead.

### 3.2 CC-Specific Instruction Removal

Some agents contain CC-specific meta-instructions that have no OpenCode equivalent:

- References to "Claude Code" or "Claude" as the runtime — ~10 files
- References to "the Agent tool" for sub-agent dispatch — ~15 files
- References to "ANTHROPIC_API_KEY" — replace with general "API key" or remove
- References to `model` as a dispatch property — ~30 frontmatter blocks

These are cosmetic text changes that don't affect the agent's functional logic.

---

## 4. Command Routing & Agent Dispatch

### 4.1 Command File Conversion

CC uses `/ars-*` commands with frontmatter-based model routing. OpenCode commands are skill-loaded `.md` files that use `task()` for dispatch.

| CC Command | OpenCode Equivalent | Model Routing |
|---|---|---|
| `commands/ars-full.md` | `commands/ars-full.md` | `task(category="ultrabrain", load_skills=["ars-pipeline"], ...)` |
| `commands/ars-plan.md` | `commands/ars-plan.md` | `task(category="deep", load_skills=["ars-academic-paper"], ...)` |
| `commands/ars-review.md` | `commands/ars-review.md` | `task(category="deep", load_skills=["ars-reviewer"], ...)` |
| `commands/ars-lit-review.md` | `commands/ars-lit-review.md` | `task(category="deep", load_skills=["ars-deep-research"], ...)` |
| `commands/ars-socratic.md` | `commands/ars-socratic.md` | `task(category="ultrabrain", load_skills=["ars-deep-research"], ...)` |
| `commands/ars-systematic-review.md` | `commands/ars-systematic-review.md` | `task(category="ultrabrain", load_skills=["ars-deep-research"], ...)` |
| `commands/ars-fact-check.md` | `commands/ars-fact-check.md` | `task(category="deep", load_skills=["ars-deep-research"], ...)` |
| `commands/ars-reviewer.md` | `commands/ars-reviewer.md` | `task(category="ultrabrain", load_skills=["ars-reviewer"], ...)` |
| `commands/ars-revision.md` | `commands/ars-revision.md` | `task(category="deep", load_skills=["ars-academic-paper"], ...)` |
| `commands/ars-abstract.md` | `commands/ars-abstract.md` | `task(category="deep", load_skills=["ars-academic-paper"], ...)` |
| `commands/ars-disclosure.md` | `commands/ars-disclosure.md` | `task(category="deep", load_skills=["ars-academic-paper"], ...)` |
| `commands/ars-format.md` | `commands/ars-format.md` | `task(category="quick", load_skills=["ars-academic-paper"], ...)` |
| `commands/ars-calibrate.md` | `commands/ars-calibrate.md` | `task(category="ultrabrain", load_skills=["ars-reviewer"], ...)` |

### 4.2 CC Command Frontmatter → OpenCode

CC frontmatter (example from `commands/ars-full.md`):
```yaml
---
model: opus
command: ars-full
---
```

OpenCode equivalent (no frontmatter needed; dispatch via skill content):
```markdown
# ars-full

Triggers the full academic research pipeline.

## Execution
After loading, the agent dispatches:
task(
  category="ultrabrain",
  load_skills=["ars-pipeline", "ars-deep-research", "ars-academic-paper", "ars-reviewer"],
  prompt="Run the full academic research pipeline... Start from Stage 1..."
)
```

### 4.3 Model Routing → OpenCode Categories

| CC Model | OpenCode Category | Used For |
|---|---|---|
| `opus` | `ultrabrain` | Full pipeline, revision-coach, socratic, systematic-review, reviewer, calibrate |
| `sonnet` | `deep` | Plan, review, abstract, disclosure, lit-review, fact-check, revision |
| `sonnet` (trivial) | `quick` | Format-convert, citation-check |

**Rationale:** `ultrabrain` in OpenCode is the category for hard, logic-heavy tasks (matching Opus strength). `deep` is for goal-oriented autonomous work on complex problems (matching Sonnet). `quick` is for simple, single-file tasks.

### 4.4 Sub-Agent Dispatch Refactoring

CC agent prompts use this pattern for sub-agent dispatch:
```
Dispatch the synthesis_agent via the Agent tool.
Synthesis agent instructions:
1. Review all research results...
2. Synthesize findings...
```

OpenCode equivalent:
```
Dispatch synthesis via:
task(
  category="ultrabrain",
  load_skills=["ars-deep-research", "nature-writing"],
  prompt="Synthesize the following research results... Follow the synthesis agent instructions..."
)
```

**Files affected:** ~15-20 agent files reference sub-agent dispatch primarily in the pipeline orchestrator, meta-agent files, and SKILL.md orchestration sections. The dispatch instructions are typically in `## Orchestration` or `## Agent Dispatch` H2 sections.

**Key dispatch mappings:**

| Sub-agent | CC Dispatch | OpenCode Dispatch |
|---|---|---|
| synthesis_agent | `Agent tool → synthesis_agent` | `task(category="ultrabrain", load_skills=[...])` |
| research_architect_agent | `Agent tool → research_architect_agent` | `task(category="ultrabrain", load_skills=[...])` |
| bibliography_agent | `Agent tool → bibliography_agent` | `task(category="deep", load_skills=["ars-deep-research", "nature-academic-search"])` |
| devils_advocate_reviewer_agent | `Agent tool → devils_advocate_reviewer` | `task(category="ultrabrain", load_skills=["ars-reviewer"])` |
| integrity_verification_agent | `Agent tool → integrity_verification_agent` | `task(category="ultrabrain", load_skills=["ars-pipeline"])` |
| formatter_agent | `Agent tool → formatter_agent` | `task(category="deep", load_skills=["ars-academic-paper"])` |
| collaboration_depth_agent | `Agent tool → collaboration_depth_agent` | `task(category="deep", load_skills=["ars-pipeline"])` |

---

## 5. Session Hooks & Plugin Manifest

### 5.1 Plugin Manifest: `.claude-plugin/` → `opencode.json`

| CC File | OpenCode Equivalent |
|---|---|
| `.claude-plugin/plugin.json` | `opencode.json` |
| `.claude-plugin/marketplace.json` | (deferred; OpenCode marketplace not yet defined) |
| `hooks/hooks.json` | `.opencode/init` or embedded session hooks |
| `hooks/announce-ars-loaded.sh` | OpenCode session init mechanism |

**`opencode.json` structure:**
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

### 5.2 Session Init Hook

CC uses `hooks/hooks.json` + `scripts/announce-ars-loaded.sh` bash 3.2 script to inject context on session start. OpenCode equivalent is an init hook file that the runtime loads at session start:

```
hooks/ars-init.md
→ Injected into LLM context at session start
→ Lists available ars-* commands
→ Provides token budget guidance
→ Replaces the bash-based announce script
```

### 5.3 `.opencode/CLAUDE.md` Structure

CC's `.claude/CLAUDE.md` (236 lines) is the master routing document — it defines 4-step mode classification, trigger keyword tables, and model routing per skill. In OpenCode, this routing logic is redistributed:

| CC CLAUDE.md Content | OpenCode Destination |
|---|---|
| Step 1-2: Skill activation keywords | `ars-meta/SKILL.md` trigger sections |
| Step 3-4: Mode selection logic | Per-skill `SKILL.md` mode dispatch sections |
| Model routing (opus→sonnet) | `task(category=...)` in command dispatchers + SKILL.md |
| Cross-skill references | Preserved in `.opencode/CLAUDE.md` as reference |

`.opencode/CLAUDE.md` becomes a **thin reference document** — it lists the 5 ars-* skills, points to the meta-skill for auto-routing, and documents the 13 `/ars-*` commands. The heavy routing logic moves into the skills themselves.

### 5.4 `MODE_REGISTRY.md` — Kept as Reference

The CC `MODE_REGISTRY.md` (all 25 modes across 4 skills) is copied as-is. Its routing function is superseded by the meta-skill, but it serves as a quick-reference index for users and developers.

### 5.5 Agents Directory

CC has `agents/` with symlinks to 3 shared agent files:
- `agents/synthesis_agent.md → deep-research/agents/synthesis_agent.md`
- `agents/research_architect_agent.md → deep-research/agents/research_architect_agent.md`
- `agents/report_compiler_agent.md → deep-research/agents/report_compiler_agent.md`

OpenCode does not need symlinks for sub-agent dispatch — it uses `task()` directly. The `agents/` directory can be omitted entirely from the OpenCode sibling repo.

---

## 6. Python Infra & CI

### 6.1 Platform-Agnostic Assets (Copy As-Is)

| Directory | Files | CC Dependencies | OpenCode Changes Needed |
|---|---|---|---|
| `scripts/check_*.py` | ~30 | Pure Python, no CC deps | None |
| `scripts/test_*.py` | ~57 | pytest/unittest | None |
| `shared/contracts/*.json` | ~15 | JSON Schema | None |
| `shared/handoff_schemas.md` | 1 | Platform-agnostic | None |
| `requirements-dev.txt` | 1 | pyyaml, ruamel.yaml, jsonschema | None (same deps) |
| `tests/fixtures/` | Various | Test data | None |
| `conftest.py` | 1 | pytest config | None |

### 6.2 CI Workflow Adaptation

| CC GitHub Workflow | OpenCode Adaptation | Notes |
|---|---|---|
| `spec-consistency.yml` (~30 steps) | Copy as-is | Pure GitHub Actions, no CC dependency |
| `pytest.yml` | Copy as-is | Standard Python test runner |
| `test-count-monotonic.yml` | Copy as-is | Count gate logic is CC-agnostic |
| `release-cooldown.yml` | Copy as-is | Release process gate |
| `run_codex_audit.sh` (1191 lines) | Adapt or replace | CC-specific audit orchestration; convert to standalone bash or skip |

**`run_codex_audit.sh`** is the only CI script with CC-specific logic (codex review invocation patterns, CC model routing). For OpenCode, it should be either:
1. Adapted to a generic bash audit script (replace CC-specific parts)
2. Replaced with OpenCode-native review workflow
3. Skipped entirely (optional — audit is a quality tool, not core functionality)

### 6.3 OpenCode-Specific CI Additions

- `.github/workflows/skill-syntax-check.yml` — Validate OpenCode skill frontmatter format
- `.github/workflows/command-dispatch-test.yml` — Verify command→skill routing works

---

## 7. Upstream Sync Strategy

### 7.1 Initial Fork

- Fork `Imbad0202/academic-research-skills` at tag `v3.9.4.2`
- Strip CC-specific files: `.claude-plugin/`, `hooks/hooks.json`, `hooks/announce-ars-loaded.sh`, `agents/` symlinks, `.claude/CLAUDE.md`
- Add OpenCode-native files: `opencode.json`, `.opencode/CLAUDE.md`, `skills/ars-*/SKILL.md`, `commands/ars-*.md`, `hooks/ars-init.md`, `SYNC.md`
- Apply frontmatter (remove model field) + tool name transformations to agent files

### 7.2 Sync Cadence

- Per upstream minor release (e.g., v3.9.5, v3.10.0)
- Automatable: `git remote add upstream git@github.com:Imbad0202/academic-research-skills.git && git fetch upstream && git merge upstream/v3.9.5 --allow-unrelated-histories`
- Merge strategy:
  - Auto-accept for: `scripts/`, `shared/`, `deep-research/agents/*.md`, `academic-paper/agents/*.md`, `academic-*/references/*.md`, `tests/fixtures/`, `docs/design/`
  - Manual review for: any `SKILL.md`, `commands/`, `.opencode/CLAUDE.md`, `hooks/`
- Conflict likelihood: LOW for Layer 2 (platform-agnostic), MEDIUM for SKILL.md files (frontmatter changes), NONE for unique OpenCode files

### 7.3 SYNC.md

Document the sync process explicitly:

```markdown
# Upstream Sync

## Process
1. Check upstream releases: `git fetch upstream --tags`
2. Identify new tag: `git tag | grep upstream/v | sort -V`
3. Create sync branch: `git checkout -b sync/v3.9.5`
4. Merge: `git merge upstream/v3.9.5 --allow-unrelated-histories`
5. Resolve conflicts (expected in SKILL.md and commands/)
6. Re-apply OpenCode transformations to modified agent files
7. Run tests: `python3 -m pytest scripts/ -v`
8. Create PR with `[SYNC]` prefix

## Auto-merge paths
- scripts/ (Python)
- shared/ (schemas)
- */*/agents/*.md (agent bodies)
- */*/references/*.md (references)
- tests/fixtures/ (test data)

## Manual-review paths
- */SKILL.md (frontmatter transformations)
- commands/ (dispatch logic)
```

---

## 8. Development Plan

### Phase 1: Repo Setup (estimated: 1-2 sessions)
1. Create sibling repo `ars-opencode` on GitHub
2. Clone and initialize with `opencode.json`
3. Set up `.opencode/CLAUDE.md` with basic routing — port relevant routing rules from CC CLAUDE.md
4. Create `SYNC.md`, `README.md`, `docs/SETUP.md`

### Phase 2: Core File Copy (estimated: 2 sessions)
1. Copy all 4 skill directories (agents/, references/)
2. Copy `shared/` (schemas, contracts, references, handoff schemas)
3. Copy `scripts/` (Python) + `conftest.py` + `requirements-dev.txt`
4. Copy `tests/fixtures/`
5. Copy `docs/` (ARCHITECTURE.md, PERFORMANCE.md, SETUP.md, design/)
6. Copy `MODE_REGISTRY.md` (keep as reference; meta-skill replaces its routing function)

### Phase 3: Frontmatter & Tool-Name Transformation (estimated: 1 session)
1. Remove `model:` field from ~30 agent frontmatter blocks (find-and-replace across `**/agents/*.md`)
2. Replace `WebSearch` → `websearch` in ~5-8 agent prompt bodies
3. Replace `WebFetch` → `webfetch` in ~3-5 agent prompt bodies
4. Remove CC-specific references ("Claude Code", "Agent tool") from agent bodies
5. Add OpenCode category routing hints where appropriate

### Phase 4: Skill File Creation (estimated: 2 sessions)
1. Create `skills/ars-meta/SKILL.md` — routing meta-skill
2. Create `skills/ars-deep-research/SKILL.md` — adapted from `deep-research/SKILL.md`
3. Create `skills/ars-academic-paper/SKILL.md` — adapted from `academic-paper/SKILL.md`
4. Create `skills/ars-reviewer/SKILL.md` — adapted from `academic-paper-reviewer/SKILL.md`
5. Create `skills/ars-pipeline/SKILL.md` — adapted from `academic-pipeline/SKILL.md`

### Phase 5: Command & Hook Creation (estimated: 1 session)
1. Create 13 `commands/ars-*.md` dispatcher files
2. Create `hooks/ars-init.md` session init hook
3. Test command→skill routing

### Phase 6: CI Setup (estimated: 1 session)
1. Copy CI workflows from upstream
2. Adapt `run_codex_audit.sh` or create OpenCode equivalent
3. Add OpenCode-specific workflow: `skill-syntax-check.yml`

### Phase 7: Testing & Verification (estimated: 1-2 sessions)
1. Run Python test suite (`python3 -m pytest scripts/ -v`)
2. Lint all SKILL.md files for OpenCode format compliance
3. Verify 13 command→skill routing paths
4. Verify all 25 modes accessible through meta-skill
5. End-to-end smoke test: run `/ars-plan` → confirm skill loads

**Total estimated effort:** 9-12 focused implementation sessions.

---

## 9. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Upstream SKILL.md diverges significantly | Medium | High — manual merge | Sync SYNC.md, pin semantic version for auto-merge rules |
| OpenCode API changes (tool names, categories) | Low | Medium — requires pass over agent files | Pin OpenCode version in README; track API changelog |
| Agent prompt contains undiscovered CC-specific instructions | Medium | Low — minor text mismatch | Audit pass after Phase 3; function tests catch routing errors |
| Upstream adds new agents with CC-specific patterns | Low | Medium — Phase 3 work repeats | Document transformation pattern; script the find-and-replace |
| OpenCode lacks equivalent for SessionStart hook | Medium | Low — cosmetic (no announce message) | Accept omission; announce via skill name instead |
