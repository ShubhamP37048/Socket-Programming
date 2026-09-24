# Stroop Test PowerPoint

- File: `docs/stroop-test-30-slides.pptx`
- Generator: `docs/generate_stroop_ppt.py`

## How it was generated or updated

1. Install Python and `python-pptx`.
   - Tested with Python 3.12
   - `python-pptx` is not part of the Python standard library.
   - Install it into the same Python environment/interpreter that you will use to run the generator:

     ```bash
     python3 -m pip install python-pptx==1.0.2
     ```
2. Run:

   ```bash
   python3 docs/generate_stroop_ppt.py
   ```

3. The script rewrites `docs/stroop-test-30-slides.pptx` with 30 Stroop-test slides using deterministic, intentionally mismatched word/color combinations.

## How to open it

- Open `docs/stroop-test-30-slides.pptx` in Microsoft PowerPoint, LibreOffice Impress, or Google Slides.

## Notes

- The presentation uses a plain white background, bold large text, and consistent margins for visual testing.
- The generator uses a fixed random seed so future updates stay reproducible.
