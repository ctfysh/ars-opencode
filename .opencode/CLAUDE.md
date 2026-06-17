# ARS OpenCode — Master Routing

**ARS** provides academic research skills for OpenCode. 5 skills, 19 commands.

**Upstream:** v3.12.1 (Imbad0202/academic-research-skills)

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
| `/ars-3w` | ars-deep-research | Three-way scan (deep) |
| `/ars-cache-invalidate` | — | Invalidate verification cache |
| `/ars-mark-read` | — | Mark advisory findings as read |
| `/ars-rebuttal-audit` | ars-academic-paper | QA rebuttal draft (deep) |
| `/ars-revision-coach` | ars-academic-paper | Revision coaching (ultrabrain) |
| `/ars-unmark-read` | — | Revert mark-read |

## Usage

Start with: `skill(name="ars-meta")` — the meta-skill routes to the correct sub-skill based on your intent.

Or invoke directly: `skill(name="ars-<skill-name>")`
