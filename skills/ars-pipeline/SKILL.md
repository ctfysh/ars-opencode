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
