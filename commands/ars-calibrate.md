# ars-calibrate

Calibrate the reviewer against a user-supplied gold set.

## Execution

```
skill(name="ars-reviewer")
```

```text
task(
  category="ultrabrain",
  load_skills=["ars-reviewer"],
  prompt="Run academic-paper-reviewer calibration mode. Calibrate against the user's gold set..."
)
```
