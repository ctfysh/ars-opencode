# ars-revision-coach

Parse reviewer comments into a structured revision roadmap. Helps plan responses and track actions.

## Execution

```
skill(name="ars-academic-paper")
```

```text
task(
  category="ultrabrain",
  load_skills=["ars-academic-paper", "ars-reviewer"],
  prompt="Run academic-paper revision-coach mode. Parse the reviewer comments into a structured revision roadmap. Identify required changes, optional improvements, and generate a response-to-reviewers skeleton..."
)
```
