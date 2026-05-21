# ars-review

Review the research quality of a paper or topic.

## Execution

```
skill(name="ars-deep-research")
```

```text
task(
  category="deep",
  load_skills=["ars-deep-research", "nature-citation"],
  prompt="Run deep-research review mode. Review the research quality of the provided topic..."
)
```
