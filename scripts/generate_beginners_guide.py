#!/usr/bin/env python3
"""Generate Chinese beginner's guide DOCX for ars-opencode."""

from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

doc = Document()

# ── Page setup ──
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)

# ── Style helpers ──

def set_font(run, name_cn="宋体", name_en="Times New Roman", size=11, bold=False, color=None):
    run.font.size = Pt(size)
    run.font.name = name_en
    run.bold = bold
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), name_cn)
    rFonts.set(qn('w:ascii'), name_en)
    rFonts.set(qn('w:hAnsi'), name_en)
    if color:
        run.font.color.rgb = color


def add_heading_styled(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        if level == 1:
            set_font(run, "黑体", "Arial", 16, bold=True)
        elif level == 2:
            set_font(run, "黑体", "Arial", 14, bold=True)
        elif level == 3:
            set_font(run, "黑体", "Arial", 12, bold=True)
    return h


def add_para(text, bold=False, italic=False, size=11, align=None, space_after=6, first_line_indent=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_font(run, "宋体", "Times New Roman", size, bold=bold)
    run.italic = italic
    if align:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.5
    if first_line_indent:
        p.paragraph_format.first_line_indent = Cm(first_line_indent)
    return p


def add_code(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.line_spacing = 1.2
    # Add shading
    shading = OxmlElement('w:shd')
    shading.set(qn('w:val'), 'clear')
    shading.set(qn('w:color'), 'auto')
    shading.set(qn('w:fill'), 'F2F2F2')
    pPr = p._element.get_or_add_pPr()
    pPr.append(shading)
    run = p.add_run(text)
    set_font(run, "Consolas", "Consolas", 9.5)
    return p


def add_bullet(text, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.clear()
    run = p.add_run(text)
    set_font(run, "宋体", "Times New Roman", 11)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(2)
    if level > 0:
        p.paragraph_format.left_indent = Cm(1.27 * level)
    return p


def set_cell_text(cell, text, bold=False, size=10, align=None):
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(text)
    set_font(run, "宋体", "Times New Roman", size, bold=bold)
    if align:
        p.alignment = align
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.line_spacing = 1.0


def shade_cell(cell, color="D9E2F3"):
    shading = OxmlElement('w:shd')
    shading.set(qn('w:val'), 'clear')
    shading.set(qn('w:color'), 'auto')
    shading.set(qn('w:fill'), color)
    cell._element.get_or_add_tcPr().append(shading)


def add_table(headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        set_cell_text(cell, h, bold=True, size=10)
        shade_cell(cell, "4472C4")
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.color.rgb = RGBColor(255, 255, 255)
    # Data rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            set_cell_text(cell, val, size=10)
            if r_idx % 2 == 1:
                shade_cell(cell, "D9E2F3")
    # Column widths
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph()  # spacer
    return table


# ═══════════════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════════════

for _ in range(6):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Academic Research Skills (ARS)")
set_font(run, "黑体", "Arial", 24, bold=True, color=RGBColor(0x1F, 0x38, 0x64))

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("用户入门指南")
set_font(run, "黑体", "Arial", 22, bold=True)

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("OpenCode 学术研究技能套件 · 中文版")
set_font(run, "宋体", "Times New Roman", 12, color=RGBColor(0x66, 0x66, 0x66))

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("版本 3.9.4.2-oc · 2026 年 5 月")
set_font(run, "宋体", "Times New Roman", 11, color=RGBColor(0x66, 0x66, 0x66))

doc.add_page_break()

# ═══════════════════════════════════════════════
# TABLE OF CONTENTS
# ═══════════════════════════════════════════════

add_heading_styled("目录", level=1)
toc_items = [
    "1. 简介",
    "2. 安装与激活",
    "3. 快速上手",
    "4. 五大技能详解",
    "5. 25 种工作模式速查",
    "6. 管线流程概览",
    "7. 实用技巧",
    "8. 常见问题",
]
for item in toc_items:
    p = doc.add_paragraph()
    run = p.add_run(item)
    set_font(run, "宋体", "Times New Roman", 12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.8

doc.add_page_break()

# ═══════════════════════════════════════════════
# 1. 简介
# ═══════════════════════════════════════════════

add_heading_styled("1. 简介", level=1)

add_para(
    "Academic Research Skills（简称 ARS）是一套面向学术研究全流程的 AI 辅助技能套件，"
    "覆盖从文献检索、深度研究、论文写作、同行评审到最终发表的完整管线。",
    first_line_indent=0.74,
)


add_para(
    "ARS 最初是为 Claude Code 开发的插件（imbad0202/academic-research-skills），"
    "现已完整移植到 OpenCode 平台（版本号 3.9.4.2-oc）。"
    "本指南面向首次接触 ARS 的科研人员，帮助你快速上手并融入日常研究工作流。",
    first_line_indent=0.74,
)

add_para("ARS 能为你做什么？", bold=True)
bullets = [
    "输入一句话研究想法，自动生成论文大纲和写作计划",
    "输入一段文字，自动搜索并匹配 Nature/CNS 系列期刊的引用文献",
    "上传手稿（PDF/DOCX），获得多角度同行评审报告",
    "对文稿进行 Nature 风格的英文润色、改写或中译英",
    "执行 PRISMA 系统综述流程，生成结构化综述报告",
    "从论文 PDF 生成中英文对照阅读笔记（含图表提取）",
    "一键将研究数据整合为符合 Nature 要求的数据可用性声明",
    "生成 Nature 风格的学术报告 PPT（中文）",
]
for b in bullets:
    add_bullet(b)

# ═══════════════════════════════════════════════
# 2. 安装与激活
# ═══════════════════════════════════════════════

add_heading_styled("2. 安装与激活", level=1)

add_heading_styled("2.1 前提条件", level=2)
add_para("安装 ARS 之前，请确保你的环境中已有以下组件：", first_line_indent=0.74)
add_bullet("OpenCode（推荐最新版本）")
add_bullet("Python 3.9 或更高版本")
add_bullet("pip（Python 包管理器）")

add_heading_styled("2.2 安装步骤", level=2)
add_para("第一步：克隆仓库", bold=True)
add_code("git clone https://github.com/your-org/ars-opencode.git")
add_para("或者直接使用本地已部署的路径：", first_line_indent=0.74)
add_code("~/Desktop/OpenSource/ars-opencode/")

add_para("第二步：安装 Python 依赖（可选但推荐）", bold=True)
add_code("pip install -r requirements-dev.txt")
add_para(
    "部分功能（如 linter、测试工具）需要额外 Python 包。"
    "如果仅使用 LLM 驱动的技能功能，可跳过此步骤。",
    first_line_indent=0.74,
)

add_para("第三步：注册为 OpenCode 插件", bold=True)
add_para(
    "如果 ars-opencode 尚未注册为插件，请编辑 OpenCode 配置文件 "
    "（~/.config/opencode/opencode.json），在 plugin 数组中添加路径：",
    first_line_indent=0.74,
)
add_code(
    '{\n'
    '  "plugin": [\n'
    '    "...",\n'
    '    "~/Desktop/OpenSource/ars-opencode"\n'
    '  ]\n'
    '}'
)

add_para("第四步：启动新会话", bold=True)
add_para(
    "关闭当前 OpenCode 会话并重新打开。新会话启动时，ARS 技能会自动加载。"
    "你也可以通过 opencode.json 中定义的 5 个技能、13 条命令直接访问。",
    first_line_indent=0.74,
)

add_heading_styled("2.3 验证安装", level=2)
add_para("新会话启动后，输入以下任意一条命令验证 ARS 是否生效：", first_line_indent=0.74)
add_code('/ars-calibrate')
add_para("如果看到 ARS 的欢迎信息或模式列表，说明安装成功。", first_line_indent=0.74)

add_para("也可以直接加载 meta 技能：", first_line_indent=0.74)
add_code('skill(name="ars-meta")')

# ═══════════════════════════════════════════════
# 3. 快速上手
# ═══════════════════════════════════════════════

add_heading_styled("3. 快速上手", level=1)

add_para(
    "以下是三种最常用的入门方式。建议按顺序体验，逐步熟悉 ARS 的能力范围。",
    first_line_indent=0.74,
)

add_heading_styled("3.1 方式一：加载 Meta 技能（推荐起点）", level=2)
add_para(
    "Meta 技能是 ARS 的路由入口。它会根据你的描述自动判断意图，"
    "将你引导到最合适的子技能。",
    first_line_indent=0.74,
)
add_code('skill(name="ars-meta")')
add_para(
    "之后只需用自然语言描述你的需求，例如：",
    first_line_indent=0.74,
)
add_bullet('"帮我查一下深度学习中注意力机制的最新进展"')
add_bullet('"我要写一篇关于 CRISPR 基因编辑的综述论文"')
add_bullet('"帮我 review 一下这篇 manuscript"')

add_heading_styled('3.2 方式二：直接使用 /ars- 命令', level=2)
add_para("ARS 提供了 13 条预配置的快捷命令，覆盖最常见的科研场景：", first_line_indent=0.74)

add_table(
    ["命令", "用途", "典型场景"],
    [
        ["/ars-plan", "规划论文结构", "刚有一个研究想法，需要梳理框架"],
        ["/ars-lit-review \"主题\"", "快速文献综述", "需要了解某个方向的文献现状"],
        ["/ars-abstract", "撰写摘要", "论文写完，需要中英文摘要"],
        ["/ars-review", "论文评审", "需要对手稿进行同行评审"],
        ["/ars-revision", "修改回复", "收到审稿意见，需要逐条回复"],
        ["/ars-fact-check", "事实核查", "需要验证文稿中的学术声明"],
        ["/ars-format", "格式转换", "需要在 APA/MLA/Chicago 等格式间切换"],
        ["/ars-disclosure", "AI 使用声明", "生成投稿所需的 AI 辅助声明"],
        ["/ars-full", "完整管线", "从研究到定稿的端到端流程"],
    ],
    col_widths=[3.5, 4.5, 6.0],
)

add_heading_styled("3.3 方式三：直接加载子技能", level=2)
add_para("如果你明确知道自己需要哪个技能，也可以直接加载：", first_line_indent=0.74)
add_code("skill(name=\"ars-deep-research\")    # 文献检索与研究")
add_code("skill(name=\"ars-academic-paper\")   # 论文写作与润色")
add_code("skill(name=\"ars-reviewer\")         # 同行评审")
add_code("skill(name=\"ars-pipeline\")         # 完整管线编排")

# ═══════════════════════════════════════════════
# 4. 五大技能详解
# ═══════════════════════════════════════════════

add_heading_styled("4. 五大技能详解", level=1)

add_para(
    "ARS 包含 5 个核心技能（skills），每个技能下辖若干工作模式（modes），"
    "总共 25 种模式。以下逐一介绍每个技能的定位和典型用法。",
    first_line_indent=0.74,
)

# 4.1
add_heading_styled("4.1 ars-meta — 智能路由", level=2)
add_para(
    "自动分析用户意图，将请求路由到正确的子技能。"
    "作为推荐入口，适合不熟悉 ARS 各技能的初学者使用。",
    first_line_indent=0.74,
)
add_para("触发关键词：", bold=True)
add_code('"research topic", "literature review", "write paper", "review paper", "full pipeline"')

# 4.2
add_heading_styled("4.2 ars-deep-research — 深度研究", level=2)
add_para(
    "包含 7 种模式，覆盖从快速文献检索到 PRISMA 系统综述的全谱研究需求。"
    "整合了 PubMed、CrossRef、arXiv 等学术搜索引擎，支持多来源文献检索。",
    first_line_indent=0.74,
)
modes_dr = [
    ["full", "完整研究", "组建多智能体研究团队，生成 3,000-8,000 字 APA 报告"],
    ["quick", "快速简报", "500-1,500 字研究摘要，适合快速了解一个方向"],
    ["lit-review", "文献综述", "带注释的文献列表 + 综合评述"],
    ["systematic-review", "系统综述", "PRISMA 2020 规范，5,000-15,000 字报告"],
    ["fact-check", "事实核查", "逐条声明的证据等级验证"],
    ["review", "研究质量审查", "对已有文献或成果的质量评估"],
    ["socratic", "苏格拉底式引导", "通过对话引导深入研究方向"],
]
add_table(
    ["模式", "中文名称", "说明"],
    modes_dr,
    col_widths=[3.0, 3.0, 8.0],
)

# 4.3
add_heading_styled("4.3 ars-academic-paper — 学术论文", level=2)
add_para(
    "包含 10 种模式，覆盖论文从规划到发表的全过程。"
    "支持 IMRaD 结构写作、中英文摘要、文献引用格式转换（APA/Chicago/MLA/IEEE/Vancouver）、"
    "AI 使用声明生成等。",
    first_line_indent=0.74,
)
modes_ap = [
    ["full", "完整草稿", "生成 IMRaD 完整论文草稿"],
    ["plan", "规划引导", "苏格拉底式对话引导论文框架"],
    ["outline-only", "仅提纲", "详细大纲 + 证据图谱"],
    ["revision", "修改草稿", "融合审稿意见的修订版本 + 逐条回复"],
    ["revision-coach", "修改指导", "审稿意见解析 + 回复策略建议"],
    ["abstract-only", "摘要生成", "中英文双语摘要 + 关键词"],
    ["lit-review", "综述论文", "按论文格式撰写文献综述"],
    ["format-convert", "格式转换", "LaTeX / DOCX / PDF / Markdown 互转"],
    ["citation-check", "引用核查", "参考文献格式和完整性检查"],
    ["disclosure", "AI 声明", "按期刊要求生成 AI 辅助使用声明"],
]
add_table(
    ["模式", "中文名称", "说明"],
    modes_ap,
    col_widths=[3.0, 3.0, 8.0],
)

# 4.4
add_heading_styled("4.4 ars-reviewer — 同行评审", level=2)
add_para(
    "包含 6 种模式，提供多角度（方法学/统计学/伦理学/再现性/写作质量）的同行评审，"
    "含 0-100 分的结构化评分和编辑决策建议。",
    first_line_indent=0.74,
)
modes_rv = [
    ["full", "完整评审", "5 份评审报告 + 编辑决定 + 修改路线图"],
    ["re-review", "重新评审", "修订核查清单 + 遗留问题标识"],
    ["quick", "快速评审", "主编级快速评估 + 关键问题列表"],
    ["methodology-focus", "方法学专项", "深度的实验设计和方法学评审"],
    ["guided", "引导式评审", "逐问题苏格拉底式对话改进"],
    ["calibration", "校准模式", "评审准确度测量（FNR/FPR/AUC）"],
]
add_table(
    ["模式", "中文名称", "说明"],
    modes_rv,
    col_widths=[3.0, 3.0, 8.0],
)

# 4.5
add_heading_styled("4.5 ars-pipeline — 完整管线", level=2)
add_para(
    "将前 4 个技能编排为 10 阶段的端到端管线："
    "Research → Write → Integrity Check → Review → Revise → Re-review → "
    "Final Integrity → Finalize → Summary。"
    "每个阶段结束后都有质量门禁和质量检查点，确保输出质量。",
    first_line_indent=0.74,
)
add_para(
    "管线适合有完整论文写作需求的用户。典型 Token 消耗约 $4-6（15,000 词论文）。",
    first_line_indent=0.74,
)

# ═══════════════════════════════════════════════
# 5. 25 种模式速查
# ═══════════════════════════════════════════════

add_heading_styled("5. 25 种工作模式速查", level=1)

add_para("以下按技能分类列出所有 25 种模式及其适用场景：", first_line_indent=0.74)

add_heading_styled("5.1 ars-deep-research（7 种模式）", level=2)

add_table(
    ["模式", "适用场景", "输出形式", "用户参与度"],
    [
        ["full", "需要全面的研究报告", "3k-8k 字 APA 报告", "高"],
        ["quick", "快速了解某个方向", "500-1.5k 字简报", "中"],
        ["lit-review", "写综述前的文献梳理", "注释文献列表 + 综合评述", "中"],
        ["systematic-review", "系统综述/Meta 分析", "5k-15k 字 PRISMA 报告", "中"],
        ["fact-check", "验证学术声明", "逐条核查报告", "中"],
        ["review", "评估已有研究成果", "质量评估报告", "高"],
        ["socratic", "研究方向不明确时", "研究计划 + 洞察集合", "很高"],
    ],
    col_widths=[3.0, 4.0, 4.0, 2.5],
)

add_heading_styled("5.2 ars-academic-paper（10 种模式）", level=2)
add_table(
    ["模式", "适用场景", "输出形式", "用户参与度"],
    [
        ["full", "从零写论文", "完整 IMRaD 草稿", "高"],
        ["plan", "需要论文框架", "章节计划 + 洞察集合", "很高"],
        ["outline-only", "只要大纲不要正文", "详细大纲 + 证据图", "高"],
        ["revision", "修改手稿（有审稿意见）", "修订稿 + 逐条回复", "高"],
        ["revision-coach", "不知道怎么修改", "修改路线图 + 回复模板", "中"],
        ["abstract-only", "写摘要", "中英文双语 + 关键词", "中"],
        ["lit-review", "写综述论文", "论文格式的文献综述", "中"],
        ["format-convert", "格式转换", "LaTeX/DOCX/PDF/MD", "低"],
        ["citation-check", "检查引用", "引用错误报告", "低"],
        ["disclosure", "投稿前的 AI 声明", "按期刊定制的声明", "低"],
    ],
    col_widths=[3.0, 4.0, 4.0, 2.5],
)

add_heading_styled("5.3 ars-reviewer（6 种模式）", level=2)
add_table(
    ["模式", "适用场景", "输出形式", "用户参与度"],
    [
        ["full", "对手稿做完整评审", "5 份报告 + 决策 + 路线图", "高"],
        ["re-review", "核查修订是否到位", "核查清单 + 遗留问题", "中"],
        ["quick", "快速看看有没有硬伤", "主编级快速评估", "低"],
        ["methodology-focus", "重点关注方法学", "方法学深度评审", "中"],
        ["guided", "逐轮改进论文", "苏格拉底对话式", "很高"],
        ["calibration", "校准评审标准", "校准报告 + 置信度披露", "中"],
    ],
    col_widths=[3.0, 4.0, 4.0, 2.5],
)

add_heading_styled("5.4 ars-pipeline（1 种编排模式 + 恢复模式）", level=2)
add_table(
    ["模式", "说明"],
    [
        ["pipeline", "10 阶段端到端管线，串联所有技能"],
        ["resume_from_passport", "从 Material Passport 断点恢复管线执行"],
    ],
    col_widths=[4.0, 10.0],
)

# ═══════════════════════════════════════════════
# 6. 管线流程概览
# ═══════════════════════════════════════════════

add_heading_styled("6. 管线流程概览", level=1)

add_para(
    "ARS 的核心特色之一是完整的 10 阶段学术发表管线。"
    '将"研究 → 写作 → 评审 → 修改 → 定稿"的完整流程串接起来，'
    "每个阶段都有自动化的质量检查和人机协作决策点。",
    first_line_indent=0.74,
)

add_para("管线阶段总览：", bold=True)
stages = [
    ["1. RESEARCH", "深度研究，确定研究问题和研究方法", "deep-research"],
    ["2. WRITE", "论文写作，生成 IMRaD 结构草稿", "academic-paper"],
    ["2.5 INTEGRITY", "完整性检查（7 维自动检测）", "自动化"],
    ["3. REVIEW", "多角度同行评审", "reviewer"],
    ["3→4 Coaching", "修改策略引导（最多 8 轮）", "academic-paper"],
    ["4. REVISE", "根据评审意见修改", "academic-paper"],
    ["3'. RE-REVIEW", "复核修改是否到位", "reviewer"],
    ["4.5 FINAL INTEGRITY", "最终完整性检查", "自动化"],
    ["5. FINALIZE", "选择输出格式（MD/DOCX/LaTeX/PDF）", "academic-paper"],
    ["6. SUMMARY", "流程总结 + 质量评审", "pipeline"],
]
add_table(
    ["阶段", "说明", "使用技能"],
    stages,
    col_widths=[3.5, 7.5, 3.0],
)

add_para(
    '用户可以在关键决策点选择分支方向（如"接受 / 小修 / 大修 / 拒稿"），'
    "管线会根据选择自动调整后续流程。这种设计既保留了 AI 的效率，"
    "又确保了研究者在关键环节的自主权。",
    first_line_indent=0.74,
)

add_para(
    "可以通过 /ars-full 命令启动完整管线。也可以只执行其中某几个阶段，"
    "不需要每次都从头跑到尾。",
    first_line_indent=0.74,
)

# ═══════════════════════════════════════════════
# 7. 实用技巧
# ═══════════════════════════════════════════════

add_heading_styled("7. 实用技巧", level=1)

add_heading_styled("7.1 Token 预算参考", level=2)
add_table(
    ["任务类型", "预估 Token 消耗", "预估费用（USD）"],
    [
        ["完整管线（15k 词论文）", "~150k-250k", "$4-6"],
        ["单个技能（深度研究）", "~50k-100k", "$1-3"],
        ["快速任务（文献综述）", "~20k-50k", "$0.5-1"],
        ["简单任务（格式转换）", "~5k-15k", "$0.1-0.3"],
    ],
    col_widths=[5.0, 4.5, 4.0],
)

add_heading_styled("7.2 API Key 设置（可选）", level=2)
add_para("部分功能使用学术搜索引擎 API，设置 Key 可以获得更高速率限制：", first_line_indent=0.74)
add_code("export S2_API_KEY=your_semantic_scholar_key")
add_code("export CROSSREF_MAILTO=your@email.com")

add_heading_styled("7.3 依赖工具", level=2)
add_bullet("Pandoc（可选）：用于 DOCX/LaTeX 格式输出")
add_bullet("tectonic + Source Han Serif TC（可选）：用于 PDF 输出")
add_bullet("Python 3.9+：运行测试和 lint 脚本")

add_heading_styled("7.4 工作流建议", level=2)
add_bullet("新手建议从 /ars-plan 开始，先体验论文规划流程")
add_bullet("熟悉后再尝试 /ars-lit-review 进行快速文献检索")
add_bullet("有完整论文需求时使用 /ars-full 管线")
add_bullet("定期运行 python3 -m pytest scripts/ -v 检查功能完整性")

# ═══════════════════════════════════════════════
# 8. 常见问题
# ═══════════════════════════════════════════════

add_heading_styled("8. 常见问题", level=1)

faqs = [
    (
        "Q: 安装后技能没有出现怎么办？",
        "确保 opencode.json 中正确配置了 plugin 路径，然后启动全新的 OpenCode 会话"
        "（关闭当前会话后重新打开）。ARS 插件在当前会话中不会生效，"
        "需要在新的会话中自动加载。",
    ),
    (
        "Q: 命令 /ars-xxx 不识别怎么办？",
        "检查 opencode.json 的 commands 部分是否正确配置了 13 条命令的路径。"
        "确认路径相对于仓库根目录正确。另外确认 skills 部分也指向了正确的 SKILL.md 文件路径。",
    ),
    (
        "Q: 运行测试报错怎么办？",
        "确保已安装 requirements-dev.txt 中的依赖。部分测试需要网络访问权限。"
        "已知约 100 个左右的测试用例需要上游环境支持，不影响核心功能使用。",
    ),
    (
        "Q: ARS 和 Claude Code 版本有什么区别？",
        "ars-opencode 是 imbad0202/academic-research-skills v3.9.4.2 的完整移植。"
        "核心内容（Agent prompts、脚本、schemas、文档）100% 同步。"
        "差异仅在于调度层：CC 使用 Agent tool + model 字段，OC 使用 task() + category 参数。",
    ),
    (
        "Q: 如何同步上游更新？",
        "参考项目根目录的 SYNC.md。基本流程是：fetch upstream tags → "
        "merge 新版本 → 运行 transform-opencode.sh 转换脚本 → 验证测试 → 提交。",
    ),
    (
        "Q: ARS 需要联网吗？",
        "大多数功能需要联网（文献检索、引用匹配等）。"
        "论文写作、润色、格式转换等可离线操作，但需本地 LLM 支持。",
    ),
]

for q, a in faqs:
    add_para(q, bold=True, size=11)
    add_para(a, first_line_indent=0.74)

# ═══════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("— 文档结束 —")
set_font(run, "宋体", "Times New Roman", 10, color=RGBColor(0x99, 0x99, 0x99))

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Academic Research Skills v3.9.4.2-oc · CC-BY-NC 4.0")
set_font(run, "宋体", "Times New Roman", 9, color=RGBColor(0x99, 0x99, 0x99))

# ═══════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════

output_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "ars-opencode-用户入门指南.docx",
)
doc.save(output_path)
print(f"✅ Saved: {output_path}")
