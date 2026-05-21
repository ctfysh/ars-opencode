# Scripts Agent Knowledge Base

**OVERVIEW**: This is the project's spec-execution engine — Python scripts that lint agent prompts, validate schemas, orchestrate CI, and run tests. NOT a standard python package (no setup.py, no __init__.py).

**STRUCTURE**:
- adapters/ (4 adapter scripts + 11 tests + golden fixtures)
- fixtures/ (synthetic test fixtures)
- tests/ (adapter test conftest)

**FILE PATTERNS**:
- check_*.py (33 lint scripts, version-prefixed)
- test_*.py (57 test files, co-located with source)
- _*.py (6 private helpers with dual-path import pattern)
- Migration scripts
- API clients (Semantic Scholar, OpenAlex, Crossref)
- run_codex_audit.sh (1191-line bash audit wrapper)
- announce-ars-loaded.sh (108-line session hook)

**WHERE TO LOOK**:
| Task | Location |
|------|----------|
| Run all CI tests | scripts/run_ci_pytest_manifest.py |
| Find lint for version X | scripts/check_vX_*.py |
| Add new adapter | scripts/adapters/README.md |
| Debug CI failure | .github/workflows/spec-consistency.yml |

**CONVENTIONS**:
- Dual-path import (try/except ImportError for both direct CLI run and package import)
- Tests use subprocess-based golden file pattern with clean_timestamps fixture
- Mixed unittest.TestCase + pytest functions
- TOML-based CI test manifest
- API clients use pure urllib (no requests dep)

**ANTI-PATTERNS**:
- Don't add __init__.py
- Don't use requests library (use urllib)
- Don't bypass the CI pytest manifest with direct pytest calls