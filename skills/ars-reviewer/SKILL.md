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
