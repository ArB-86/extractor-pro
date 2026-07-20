from src.ocr.surya_ocr import SuryaOCR

ocr = SuryaOCR()

text = ocr.recognize(
    "debug/pipeline/000_plain_text_0.98.png"
)

print("=" * 80)
print(text)
