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
