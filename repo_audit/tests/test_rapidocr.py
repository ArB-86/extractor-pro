from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

result, _ = engine("debug/test/000_plain_text_0.98.png")

print("=" * 80)

if result:
    for line in result:
        print(line[1])
else:
    print("No text detected.")
