from pathlib import Path
import hashlib
import fitz
import pandas as pd

ROOTS = [
    ("/home/jiitcah.05/nlp_research_module/datasets/raw_docs", "NCERT"),
    ("/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw", "EXEMPLAR"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


rows = []

for root, source in ROOTS:

    for pdf in sorted(Path(root).rglob("*.pdf")):

        try:

            doc = fitz.open(pdf)

            rows.append({

                "source": source,

                "filename": pdf.name,

                "relative_path": str(pdf.relative_to(root)),

                "absolute_path": str(pdf),

                "pages": len(doc),

                "sha256": sha256(pdf),

                "title": doc.metadata.get("title", ""),

                "author": doc.metadata.get("author", "")

            })

            doc.close()

        except Exception as e:

            print(pdf, e)

df = pd.DataFrame(rows)

Path("datasets/manifests").mkdir(parents=True, exist_ok=True)

df.to_parquet(
    "datasets/manifests/pdf_manifest.parquet",
    index=False
)

df.to_csv(
    "datasets/manifests/pdf_manifest.csv",
    index=False
)

print(df.head())

print()

print("TOTAL PDFs =", len(df))
