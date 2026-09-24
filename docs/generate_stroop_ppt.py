from __future__ import annotations

import random
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


WORDS = [
    "RED",
    "BLUE",
    "GREEN",
    "YELLOW",
    "PINK",
    "PURPLE",
    "BLACK",
    "ORANGE",
]

COLORS = {
    "RED": RGBColor(192, 0, 0),
    "BLUE": RGBColor(0, 102, 204),
    "GREEN": RGBColor(0, 153, 0),
    "YELLOW": RGBColor(204, 153, 0),
    "PINK": RGBColor(204, 0, 102),
    "PURPLE": RGBColor(102, 0, 153),
    "BLACK": RGBColor(0, 0, 0),
    "ORANGE": RGBColor(230, 120, 0),
}

LAYOUTS = [
    (6, 6),
    (5, 7),
    (4, 8),
    (7, 5),
    (3, 10),
    (8, 4),
]


def build_deck() -> Presentation:
    rng = random.Random(37048)
    presentation = Presentation()
    presentation.slide_width = Inches(13.333)
    presentation.slide_height = Inches(7.5)

    blank = presentation.slide_layouts[6]

    for slide_number in range(30):
        rows, columns = LAYOUTS[slide_number % len(LAYOUTS)]
        slide = presentation.slides.add_slide(blank)
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = RGBColor(255, 255, 255)

        slide.shapes.add_textbox(Inches(0.5), Inches(0.18), Inches(5.5), Inches(0.4))
        title_frame = slide.shapes[-1].text_frame
        title_frame.text = f"STROOP TEST {slide_number + 1:02d}"
        title_run = title_frame.paragraphs[0].runs[0]
        title_run.font.bold = True
        title_run.font.size = Pt(18)
        title_run.font.color.rgb = RGBColor(90, 90, 90)

        left = 0.7
        top = 0.75
        usable_width = 11.9
        usable_height = 6.1
        cell_width = usable_width / columns
        cell_height = usable_height / rows

        for row in range(rows):
            for column in range(columns):
                word = WORDS[(row * columns + column + slide_number) % len(WORDS)]
                color_choices = [name for name in COLORS if name != word]
                font_color_name = color_choices[rng.randrange(len(color_choices))]

                x = Inches(left + column * cell_width)
                y = Inches(top + row * cell_height)
                width = Inches(cell_width)
                height = Inches(cell_height)

                textbox = slide.shapes.add_textbox(x, y, width, height)
                frame = textbox.text_frame
                frame.clear()
                paragraph = frame.paragraphs[0]
                paragraph.alignment = PP_ALIGN.CENTER
                run = paragraph.add_run()
                run.text = word
                run.font.bold = True
                run.font.size = Pt(26 if columns <= 6 else 22)
                run.font.name = "Arial"
                run.font.color.rgb = COLORS[font_color_name]

                if (slide_number + row + column) % 5 == 0:
                    shape = slide.shapes.add_shape(
                        MSO_AUTO_SHAPE_TYPE.RECTANGLE,
                        x,
                        y,
                        width,
                        height,
                    )
                    shape.fill.background()
                    shape.line.color.rgb = RGBColor(235, 235, 235)
                    slide.shapes._spTree.remove(shape._element)
                    slide.shapes._spTree.insert(2, shape._element)

        footer = slide.shapes.add_textbox(Inches(11.9), Inches(7.0), Inches(0.9), Inches(0.25))
        footer_frame = footer.text_frame
        footer_frame.text = str(slide_number + 1)
        footer_paragraph = footer_frame.paragraphs[0]
        footer_paragraph.alignment = PP_ALIGN.RIGHT
        footer_run = footer_paragraph.runs[0]
        footer_run.font.size = Pt(11)
        footer_run.font.color.rgb = RGBColor(120, 120, 120)

    return presentation


def main() -> None:
    output_path = Path(__file__).with_name("stroop-test-30-slides.pptx")
    presentation = build_deck()
    presentation.save(output_path)
    print(f"Generated {output_path}")
    print(f"Slides: {len(presentation.slides)}")


if __name__ == "__main__":
    main()
