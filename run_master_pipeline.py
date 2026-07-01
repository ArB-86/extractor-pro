import os
import json
import torch
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from docling.document_converter import DocumentConverter

# Configuration
DATA_ROOT = Path('/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw')
OUTPUT_DIR = Path('/home/jiitcah.05/nlp_research_module/extractor_pro/output/final_clean')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# GPU Check
print(f"CUDA Available: {torch.cuda.is_available()}")
converter = DocumentConverter()

def process_chapter(pdf_path):
    try:
        result = converter.convert(pdf_path)
        extracted_data = []
        
        # Docling structure-aware extraction
        for element, _ in result.document.iterate_items():
            text = element.text.strip()
            # Strict Filtering: Only keep blocks that look like questions
            if len(text) > 30 and ('?' in text or 'find' in text.lower() or 'prove' in text.lower()):
                extracted_data.append({
                    "chapter": pdf_path.stem,
                    "question": text,
                    "quality_score": "high"
                })
        
        # Only save if quality threshold is met
        if len(extracted_data) >= 50:
            with open(OUTPUT_DIR / f"{pdf_path.stem}.json", "w") as f:
                json.dump(extracted_data, f, indent=4)
            return f"SUCCESS: {pdf_path.stem} ({len(extracted_data)} questions)"
        else:
            return f"FAIL: {pdf_path.stem} (Only {len(extracted_data)} questions)"
    except Exception as e:
        return f"ERROR: {pdf_path.stem} - {str(e)}"

# Execute in Parallel
if __name__ == "__main__":
    pdfs = list(DATA_ROOT.glob("*.pdf"))
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(executor.map(process_chapter, pdfs))
    
    for r in results:
        print(r)
