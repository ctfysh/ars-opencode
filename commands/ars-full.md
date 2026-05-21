# ars-full

Triggers the full academic research pipeline.

## Execution

```
skill(name="ars-pipeline")
```

```text
task(
  category="ultrabrain",
  load_skills=["ars-pipeline", "ars-deep-research", "ars-academic-paper", "ars-reviewer", "nature-writing", "nature-citation"],
  prompt="Run the full academic research pipeline. Start from Stage 1: RESEARCH. Assemble the research team..."
)
```
