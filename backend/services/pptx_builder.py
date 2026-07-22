"""Executive deck builder — turns narrative slides into a .pptx (bytes)."""

from __future__ import annotations

from io import BytesIO
from typing import Any

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

WHITE = RGBColor(255, 255, 255)
NAVY = RGBColor(0x0F, 0x17, 0x2A)
MUTED = RGBColor(0x94, 0xA3, 0xB8)


def build_pptx(narrative: dict[str, Any]) -> bytes:
    """Render the narrative's slides into a downloadable PowerPoint."""

    def _set_slide_bg(slide, color):
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def _add_textbox(slide, left, top, width, height, text, *, size=18, bold=False, color=WHITE):
        box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
        frame = box.text_frame
        frame.word_wrap = True
        p = frame.paragraphs[0]
        p.text = text
        run = p.runs[0]
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color

    def _add_bullets(slide, bullets, top=2.4):
        box = slide.shapes.add_textbox(Inches(0.9), Inches(top), Inches(11.5), Inches(4.5))
        frame = box.text_frame
        frame.word_wrap = True
        for i, bullet in enumerate(bullets):
            p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
            p.text = bullet
            if p.runs:
                p.runs[0].font.size = Pt(18)
                p.runs[0].font.color.rgb = WHITE

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    for index, slide_data in enumerate(narrative.get("slides", [])):
        slide = prs.slides.add_slide(blank)
        _set_slide_bg(slide, NAVY)
        _add_textbox(
            slide, 0.9, 0.7 if index else 2.2, 11.5, 1.2,
            slide_data.get("title", ""),
            size=34 if index == 0 else 28, bold=True,
        )
        subtitle = slide_data.get("subtitle", "")
        if subtitle:
            _add_textbox(slide, 0.9, 1.5 if index == 0 else 1.55, 11.5, 0.8, subtitle, size=18, color=MUTED)
        bullets = slide_data.get("bullets") or []
        if bullets:
            _add_bullets(slide, bullets, top=2.2 if index != 0 else 3.3)
        _add_textbox(slide, 0.9, 6.9, 4, 0.3, "DeckGen AI", size=10, color=MUTED)

    buffer = BytesIO()
    prs.save(buffer)
    return buffer.getvalue()
