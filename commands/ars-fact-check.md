# ars-fact-check

Fact-check specific claims or statements.

## Execution

```
skill(name="ars-deep-research")
```

```text
task(
  category="deep",
  load_skills=["ars-deep-research", "nature-academic-search"],
  prompt="Run deep-research fact-check mode. Verify the following claims..."
)
```
