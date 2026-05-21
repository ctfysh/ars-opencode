# Setup

## Prerequisites

- Python 3.9+ with `pip`
- Optional: Pandoc for DOCX output
- Optional: tectonic + Source Han Serif TC for PDF output

## Install the suite

Clone the repo:
```bash
git clone https://github.com/your-org/ars-opencode.git
```

OpenCode auto-discovers `opencode.json` at the repo root — skills and commands are available immediately.

## Python dependencies

Some lint scripts and tests require Python packages:
```bash
pip install -r requirements-dev.txt
```

## API keys (optional)

Some features (Semantic Scholar API, Crossref) benefit from API keys for higher rate limits. Set them as environment variables:
```bash
export S2_API_KEY=your_key_here
export CROSSREF_MAILTO=your@email.com
export ARS_CROSS_MODEL=true
```

See upstream `docs/SETUP.md` for full API key documentation.
