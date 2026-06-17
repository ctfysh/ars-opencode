# ars-academic-paper

OpenCode ported skill: Academic Paper — writing, formatting, revision, citation management.

**Based on:** `academic-paper/SKILL.md` from upstream v3.12.1
**Version:** 3.2.0 (upstream)
**Status:** active
**Data access level:** verified_only
**Task type:** open-ended
**Related skills:** ars-deep-research, ars-pipeline, ars-reviewer

## Modes

| Mode | Category | Description |
|---|---|---|---|
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
| rebuttal-audit | deep | QA of existing rebuttal/response draft |

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

### Rebuttal-Audit Mode
```text
task(
  category="deep",
  load_skills=["ars-academic-paper", "ars-reviewer"],
  prompt="Run academic-paper rebuttal-audit mode. QA the author's existing rebuttal/response draft against the reviewer comments..."
)
```

## Key References

- `academic-paper/agents/` — 12 agent prompts
- `academic-paper/references/` — Writing guides, format templates, style calibration
- `shared/handoff_schemas.md` — Cross-skill data contracts
