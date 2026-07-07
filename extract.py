from src.extractor.extractor import Extractor

extractor = Extractor()

extractor.extract(
    pdf_path="/home/jiitcah.05/nlp_research_module/datasets/raw_docs/gegp1dd/gegp101.pdf",
    output_dir="debug/full_book",
)