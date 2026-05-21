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
