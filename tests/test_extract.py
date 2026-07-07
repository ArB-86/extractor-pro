from src.extractor.extractor import Extractor

extractor = Extractor()

pages = extractor.extract(
    "/home/jiitcah.05/nlp_research_module/datasets/raw_docs/gegp1dd/gegp101.pdf",
    "debug/full_book",
)

print("=" * 80)
print("Pages:", len(pages))