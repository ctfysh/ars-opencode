# ars-rebuttal-audit

Audit an existing rebuttal/response-to-reviewers draft for coverage, tone, and evidence.

## Execution

```
skill(name="ars-academic-paper")
```

```text
task(
  category="deep",
  load_skills=["ars-academic-paper", "ars-reviewer"],
  prompt="Run academic-paper rebuttal-audit mode. Given the reviewer comments and the author's existing rebuttal draft, produce a per-comment coverage table, gap list, risk flags for tone/evidence/misread, and improvement suggestions (advisory only — do not write or rewrite the response)..."
)
```
