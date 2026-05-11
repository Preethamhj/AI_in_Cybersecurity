from __future__ import annotations

import html
import re
import textwrap
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "LAB_MANUAL.md"
TARGET = ROOT / "LAB_MANUAL.pdf"

DOCUMENT_TITLE = "AI in Cyber Security Laboratory Manual"
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = inch
CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN)

DARK_BLUE = colors.HexColor("#123B63")
CODE_BACKGROUND = colors.HexColor("#F0F0F0")
TERMINAL_BACKGROUND = colors.HexColor("#F7F7F7")
BODY_TEXT = colors.HexColor("#1F1F1F")
MUTED_TEXT = colors.HexColor("#666666")


def clean_text(text: str) -> str:
    replacements = {
        "âœ…": "[OK]",
        "âš ï¸": "[Warning]",
        "âš ": "[Warning]",
        "ðŸ”¥": "[High]",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text.strip()


def markdown_to_plain(text: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"\1", text)
    text = re.sub(r"\[`?([^`\]]+)`?\]\(([^)]+)\)", r"\1 (\2)", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    text = text.replace("`", "")
    return clean_text(text)


def escape_para(text: str) -> str:
    return html.escape(markdown_to_plain(text))


def wrap_monospace(text: str, max_chars: int = 88) -> str:
    wrapped_lines: list[str] = []
    for raw_line in text.rstrip("\n").splitlines():
        line = raw_line.rstrip()
        if not line:
            wrapped_lines.append("")
            continue
        indent = re.match(r"^\s*", line).group(0)
        continuation_indent = indent + "    "
        chunks = textwrap.wrap(
            line,
            width=max_chars,
            initial_indent="",
            subsequent_indent=continuation_indent,
            replace_whitespace=False,
            drop_whitespace=False,
            break_long_words=True,
            break_on_hyphens=False,
            tabsize=4,
        )
        wrapped_lines.extend(chunks or [""])
    return "\n".join(wrapped_lines)


class LabManualDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            text = flowable.getPlainText()
            style_name = flowable.style.name
            if style_name == "ProgramTitle":
                self.notify("TOCEntry", (0, text, self.page))


def build_styles():
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "ManualTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            textColor=DARK_BLUE,
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "program": ParagraphStyle(
            "ProgramTitle",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=23,
            textColor=DARK_BLUE,
            alignment=TA_LEFT,
            spaceBefore=14,
            spaceAfter=12,
            keepWithNext=True,
        ),
        "subheading": ParagraphStyle(
            "Subheading",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=DARK_BLUE,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=7,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=BODY_TEXT,
            alignment=TA_JUSTIFY,
            spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=BODY_TEXT,
            leftIndent=14,
            firstLineIndent=-8,
            spaceAfter=5,
        ),
        "path": ParagraphStyle(
            "FilePath",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=12,
            textColor=MUTED_TEXT,
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "caption": ParagraphStyle(
            "ImageCaption",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=BODY_TEXT,
            alignment=TA_CENTER,
            spaceBefore=8,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "code": ParagraphStyle(
            "Code",
            fontName="Courier",
            fontSize=8,
            leading=9.8,
            textColor=colors.HexColor("#222222"),
            leftIndent=0,
            rightIndent=0,
        ),
        "terminal": ParagraphStyle(
            "Terminal",
            fontName="Courier",
            fontSize=8,
            leading=9.8,
            textColor=colors.HexColor("#222222"),
            leftIndent=0,
            rightIndent=0,
        ),
    }
    return styles


def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(MARGIN, PAGE_HEIGHT - 0.5 * inch, DOCUMENT_TITLE)
    canvas.drawCentredString(
        PAGE_WIDTH / 2,
        0.45 * inch,
        f"{DOCUMENT_TITLE} | Page {doc.page}",
    )
    canvas.restoreState()


def add_heading(story: list, text: str, styles: dict):
    story.append(Paragraph(escape_para(text), styles["program"]))
    story.append(Spacer(1, 4))


def add_subheading(story: list, text: str, styles: dict):
    label = "Terminal Output" if text.strip().lower() == "output" else text
    story.append(Paragraph(escape_para(label), styles["subheading"]))


def add_monospace_block(
    story: list,
    text: str,
    style: ParagraphStyle,
    background,
    border,
    max_lines_per_chunk: int = 58,
):
    wrapped = wrap_monospace(text)
    lines = wrapped.splitlines() or [""]
    for start in range(0, len(lines), max_lines_per_chunk):
        chunk = "\n".join(lines[start : start + max_lines_per_chunk])
        block = Preformatted(html.escape(chunk), style, maxLineLength=88)
        story.append(
            Table(
                [[block]],
                colWidths=[CONTENT_WIDTH],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), background),
                        ("BOX", (0, 0), (-1, -1), 0.25, border),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 7),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ]
                ),
            )
        )
        story.append(Spacer(1, 6 if start + max_lines_per_chunk < len(lines) else 10))


def add_code_block(story: list, code: str, styles: dict):
    add_monospace_block(
        story,
        code,
        styles["code"],
        CODE_BACKGROUND,
        colors.HexColor("#D0D0D0"),
    )


def add_terminal_output(story: list, output: str, styles: dict):
    add_monospace_block(
        story,
        output,
        styles["terminal"],
        TERMINAL_BACKGROUND,
        colors.HexColor("#DDDDDD"),
    )


def add_image(story: list, image_path: Path, caption: str, styles: dict):
    if not image_path.exists():
        story.append(Paragraph(f"Image not found: {escape_para(str(image_path))}", styles["body"]))
        return

    image = Image(str(image_path))
    max_width = CONTENT_WIDTH
    max_height = PAGE_HEIGHT - (2 * MARGIN) - 90
    scale = min(max_width / image.imageWidth, max_height / image.imageHeight, 1)
    image.drawWidth = image.imageWidth * scale
    image.drawHeight = image.imageHeight * scale
    image.hAlign = "CENTER"

    story.append(
        KeepTogether(
            [
                Paragraph(escape_para(caption), styles["caption"]),
                image,
                Spacer(1, 12),
            ]
        )
    )


def add_paragraph(story: list, text: str, styles: dict):
    if not text.strip():
        story.append(Spacer(1, 6))
        return
    if text.startswith("- "):
        story.append(Paragraph(f"- {escape_para(text[2:])}", styles["bullet"]))
    elif text.startswith("File:"):
        story.append(Paragraph(escape_para(text), styles["path"]))
    elif text.startswith("Terminal output file:"):
        story.append(Paragraph(escape_para(text), styles["path"]))
    else:
        story.append(Paragraph(escape_para(text), styles["body"]))


def make_toc(styles: dict):
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            "TOCProgram",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            leftIndent=12,
            firstLineIndent=-12,
            textColor=BODY_TEXT,
        )
    ]
    return [
        Paragraph("Table of Contents", styles["subheading"]),
        toc,
        PageBreak(),
    ]


def parse_markdown(styles: dict) -> list:
    story: list = []
    in_code = False
    code_language = ""
    code_lines: list[str] = []
    current_section = ""
    first_program_seen = False

    lines = SOURCE.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in lines:
        stripped = line.rstrip()

        if stripped.startswith("```"):
            if in_code:
                content = "\n".join(code_lines)
                if code_language.lower() in {"text", "terminal", "output"} or current_section == "Output":
                    add_terminal_output(story, content, styles)
                else:
                    add_code_block(story, content, styles)
                code_lines = []
                code_language = ""
                in_code = False
            else:
                in_code = True
                code_language = stripped.strip("`").strip()
            continue

        if in_code:
            code_lines.append(line)
            continue

        image_match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if image_match:
            caption = image_match.group(1)
            rel_path = image_match.group(2)
            add_image(story, ROOT / rel_path, caption, styles)
            continue

        heading_match = re.match(r"^(#{1,3})\s+(.*)", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            text = clean_text(heading_match.group(2))
            current_section = text
            if level == 1:
                story.append(Paragraph(escape_para(text), styles["title"]))
                story.extend(make_toc(styles))
            elif level == 2 and text.lower().startswith("program"):
                if first_program_seen:
                    story.append(PageBreak())
                first_program_seen = True
                add_heading(story, text, styles)
            elif level in {2, 3}:
                add_subheading(story, text, styles)
            else:
                add_paragraph(story, text, styles)
            continue

        add_paragraph(story, stripped, styles)

    return story


def convert():
    styles = build_styles()
    doc = LabManualDocTemplate(
        str(TARGET),
        pagesize=A4,
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title=DOCUMENT_TITLE,
        author="AI in Cyber Security Laboratory",
    )
    story = parse_markdown(styles)
    doc.multiBuild(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"Created {TARGET}")


if __name__ == "__main__":
    convert()
