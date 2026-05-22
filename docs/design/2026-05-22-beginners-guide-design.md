# Beginner's Guide Design

**Date:** 2026-05-22
**Type:** design
**Status:** approved

## Goal

Create a Chinese-language beginner's guide (用户入门指南) for the `ars-opencode` project, output as DOCX.

## Target Audience

Chinese-speaking academic researchers (graduate students, postdocs, early-career researchers) who are new to ARS and want to start using it for their research workflow.

## Document Structure

| # | Section | Content |
|---|---------|---------|
| 1 | 简介 | What is ARS, origin (CC port), what problems it solves |
| 2 | 安装与激活 | Clone repo, OpenCode auto-discovery, verify installation |
| 3 | 快速上手 | 3 entry points: /ars-plan, /ars-lit-review, skill(name="ars-meta") |
| 4 | 五大技能详解 | ars-meta, ars-deep-research, ars-academic-paper, ars-reviewer, ars-pipeline |
| 5 | 25 种模式速查表 | Table by skill, each mode with Chinese description |
| 6 | 管线流程概览 | 10-stage pipeline concept diagram + explanation |
| 7 | 实用技巧 | Token budget, API keys, Pandoc, workflow tips |
| 8 | 常见问题 | Troubleshooting common issues |

## Formatting

- Title: 黑体 22pt, centered
- H1 headings: 黑体 16pt
- H2 headings: 黑体 14pt
- Body: 宋体 11pt, 1.5 line spacing
- Code: Consolas 9.5pt, light gray background
- Tables: professional styling with header shading
- Page numbers: bottom center
- Table of contents page

## Output

- File: `ars-opencode-用户入门指南.docx`
- Location: project root
