from pathlib import Path

from src.llm.qwen_client import QwenClient

text = Path("debug/page.md").read_text(encoding="utf-8")

client = QwenClient()

prompt = f"""
You are correcting OCR output from a CBSE NCERT Mathematics textbook.

Rules:

1. Preserve ALL information.
2. Do NOT summarize.
3. Do NOT rewrite.
4. Preserve headings.
5. Preserve paragraph boundaries.
6. Fix OCR mistakes only.
7. Join broken words.
8. Remove duplicated words.
9. Return ONLY corrected markdown.

{text}
"""

result = client.chat(prompt)

print("=" * 80)
print(result)

Path("debug/page_clean.md").write_text(
    result,
    encoding="utf-8"
)

print("\nSaved -> debug/page_clean.md")