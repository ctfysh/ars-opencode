# Shared Infrastructure

**OVERVIEW**: Architectural spine of ARS — everything that must be consistent across all 4 skills: data contracts (handoff_schemas.md), JSON schemas (contracts/), compliance agent (agents/), pattern protection references (references/), audit template (templates/), policy data (policy_data/).

**STRUCTURE**:
- `contracts/` (20 JSON schemas: sprint, passport, audit)
- `agents/` (1 shared compliance_agent.md)
- `references/` (5 pattern-protection refs: irb, psychometric, hedging, word count, intent clarification)
- `templates/` (1 cross-model audit prompt template)
- `policy_data/` (1 nature_policy.md G4 invariant)

**WHERE TO LOOK**:
- "Find handoff data schema" → handoff_schemas.md (S1-S13)
- "Validate sprint contract" → contracts/sprint_contract.schema.json (12 allOf branches)
- "Add passport field" → contracts/passport/ (13 schemas)
- "Compliance gate rules" → agents/compliance_agent.md + compliance_checkpoint_protocol.md
- "Cross-model audit" → templates/codex_audit_multifile_template.md
- "Nature AI policy" → policy_data/nature_policy.md (G4 invariant)

**CONVENTIONS**:
- Append-only ledger pattern (compliance_history[], reset_boundary[], audit_artifact[] never overwrite, never reorder)
- LLM-optimized schemas (Markdown tables over pure JSON Schema)
- Failure-driven design (every file cites specific production incidents)
- Dual compliance frameworks (PRISMA-trAIce + RAISE with mode-based dispatch)
- Honesty infrastructure (benchmark forces caveats, reproducibility forces stochasticity declaration)

**ANTI-PATTERNS**:
- No schema commitment in discovery docs
- No mutation of G4 invariant files without updating lint
- No bypassing the 3-round override ladder in compliance_checkpoint_protocol.md