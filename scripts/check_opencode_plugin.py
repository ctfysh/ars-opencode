#!/usr/bin/env python3
"""Validate the OpenCode plugin structure for ars-opencode.

Checks:
  1. All 13 commands registered in opencode.json point to existing files.
  2. All 5 skills registered in opencode.json have existing SKILL.md files.
  3. .opencode/CLAUDE.md lists the same commands and skills.
  4. No orphaned command files exist (every commands/*.md is registered).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COMMANDS = [
    "ars-full", "ars-plan", "ars-review", "ars-lit-review",
    "ars-socratic", "ars-systematic-review", "ars-fact-check",
    "ars-reviewer", "ars-revision", "ars-abstract", "ars-disclosure",
    "ars-format", "ars-calibrate",
]
EXPECTED_SKILLS = [
    "ars-meta", "ars-deep-research", "ars-academic-paper",
    "ars-reviewer", "ars-pipeline",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []

    # ── opencode.json ──────────────────────────────────────
    oc_json = ROOT / "opencode.json"
    if not oc_json.is_file():
        errors.append(f"{oc_json}: not found")
        return 1

    cfg = load_json(oc_json)

    # commands
    registered_cmds = set(cfg.get("commands", {}))
    for cmd in EXPECTED_COMMANDS:
        if cmd not in registered_cmds:
            errors.append(f"opencode.json: missing command '{cmd}'")
            continue
        entry = cfg["commands"][cmd]
        path_val = entry if isinstance(entry, str) else entry.get("template", "")
        cmd_path = ROOT / path_val
        if not cmd_path.is_file():
            errors.append(f"opencode.json: command '{cmd}' file not found: {cmd_path}")

    for cmd in registered_cmds - set(EXPECTED_COMMANDS):
        errors.append(f"opencode.json: unexpected extra command '{cmd}'")

    # skills
    registered_skills = set(cfg.get("skills", {}))
    for skill in EXPECTED_SKILLS:
        if skill not in registered_skills:
            errors.append(f"opencode.json: missing skill '{skill}'")
            continue
        skill_cfg = cfg["skills"][skill]
        skill_md = ROOT / skill_cfg
        if not skill_md.is_file():
            errors.append(f"opencode.json: skill '{skill}' file not found: {skill_md}")

    for skill in registered_skills - set(EXPECTED_SKILLS):
        errors.append(f"opencode.json: unexpected extra skill '{skill}'")

    # ── .opencode/CLAUDE.md ────────────────────────────────
    claude_md = ROOT / ".opencode" / "CLAUDE.md"
    if not claude_md.is_file():
        errors.append(f"{claude_md}: not found")
    else:
        text = claude_md.read_text(encoding="utf-8")
        for cmd in EXPECTED_COMMANDS:
            if f"/{cmd}" not in text:
                errors.append(f"{claude_md}: missing command '/{cmd}'")
        for skill in EXPECTED_SKILLS:
            if skill not in text:
                errors.append(f"{claude_md}: missing skill '{skill}'")

    # ── No orphan commands ──────────────────────────────────
    cmd_dir = ROOT / "commands"
    if cmd_dir.is_dir():
        actual_cmd_files = {p.stem for p in cmd_dir.glob("ars-*.md")}
        registered_names = set(EXPECTED_COMMANDS)
        orphaned = actual_cmd_files - registered_names
        for cmd in sorted(orphaned):
            errors.append(f"commands/{cmd}.md exists but is not registered in opencode.json")
        # Extra: all registered names should have a file
        missing = registered_names - actual_cmd_files
        for cmd in sorted(missing):
            errors.append(f"commands/{cmd}.md is registered but file not found")

    # ── Report ─────────────────────────────────────────────
    if errors:
        print("OpenCode plugin validation failed:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("OpenCode plugin validation passed: 13 commands, 5 skills, all files present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
