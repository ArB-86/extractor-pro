
from __future__ import annotations


class PromptManager:

    def ocr_repair(self, text):

        return f"""
You are an expert OCR correction system.

Correct OCR errors.

Rules:

- Do not change mathematical meaning.
- Preserve numbering.
- Preserve equations.
- Preserve formatting.
- Return only corrected text.

TEXT:

{text}
"""

    def formula_repair(self, formula):

        return f"""
You are an expert mathematical OCR system.

Repair this mathematical expression.

Return ONLY the corrected expression.

Expression:

{formula}
"""

    def figure_understanding(self, question):

        return f"""
Analyze the attached mathematical figure.

Question:

{question}

Return JSON with:

description
objects
labels
geometry
"""
