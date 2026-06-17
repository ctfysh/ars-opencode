# ars-3w

Quick WHY/HOW/WHAT paper comparison and triage.

## Execution

```
skill(name="ars-deep-research")
```

```text
task(
  category="deep",
  load_skills=["ars-deep-research", "nature-academic-search"],
  prompt="Run deep-research three-way-scan mode. Compare the provided papers using WHY/HOW/WHAT analysis. Produce a per-paper shortlist plus cross-paper synthesis (common WHY, divergent HOW, strongest WHAT, unresolved gap)..."
)
```
