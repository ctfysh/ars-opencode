# ars-deep-research

OpenCode ported skill: Deep Research — literature search, systematic review, fact-checking, Socratic dialogue.

**Based on:** `deep-research/SKILL.md` from upstream v3.12.1
**Version:** 2.10.0 (upstream)
**Status:** active
**Data access level:** verified_only
**Task type:** open-ended
**Related skills:** ars-academic-paper, ars-pipeline

## Modes

| Mode | Category | Description |
|---|---|---|---|
| full | ultrabrain | Full multi-agent research team |
| quick | deep | Rapid brief |
| review | deep | Research quality review |
| lit-review | deep | Literature review |
| three-way-scan | deep | Rapid WHY/HOW/WHAT paper comparison |
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

### Three-Way-Scan Mode
```text
task(
  category="deep",
  load_skills=["ars-deep-research", "nature-academic-search"],
  prompt="Run deep-research three-way-scan mode. Compare these papers with WHY/HOW/WHAT analysis..."
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
