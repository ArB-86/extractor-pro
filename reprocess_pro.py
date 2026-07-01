# Save as reprocess_pro.py
from docling.document_converter import DocumentConverter
import json

converter = DocumentConverter()
# Replace with the path to one of your real NCERT PDFs
pdf_path = "datasets/exemplar_raw/jeep206.pdf" 
result = converter.convert(pdf_path)

# Extract and structure strictly
data = []
for element, _ in result.document.iterate_items():
    # Only capture blocks that look like questions (contain numbers or question marks)
    text = element.text
    if len(text) > 20 and any(char.isdigit() for char in text[:5]):
        data.append({
            "chapter": "jeep206",
            "question": text.strip(),
            "grade": "10",
            "source": "NCERT-Exemplar"
        })

with open("output/jeep206_verified.json", "w") as f:
    json.dump(data, f, indent=4)
