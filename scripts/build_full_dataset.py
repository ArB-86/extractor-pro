from __future__ import annotations

import sys
from pathlib import Path
import os   # added

# ---- Add project root to Python path ----
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import traceback
import time

from src.pipeline.production_pipeline import ProductionPipeline

# ---------------------------------------------------------------------
# PDF ROOT – CHANGE IF DIFFERENT
# ---------------------------------------------------------------------
PDF_ROOT = Path.home() / "nlp_research_module" / "datasets" / "raw_docs"
OUTPUT_ROOT = Path("datasets")

# ---- Prefix filter from environment ----
PREFIX = os.environ.get("BOOK_PREFIX")


def discover_books():
    pdfs = sorted(PDF_ROOT.rglob("*.pdf"))
    if not pdfs:
        raise RuntimeError(f"No PDF files found under {PDF_ROOT.resolve()}")
    return pdfs


def build_book(pipeline: ProductionPipeline, pdf: Path):
    relative = pdf.relative_to(PDF_ROOT)
    out_dir = OUTPUT_ROOT / relative.with_suffix("")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 100)
    print(f"BOOK : {relative}")
    print("=" * 100)

    start = time.time()
    pipeline.run(pdf_path=pdf, output_dir=out_dir, gold_path=None)
    elapsed = time.time() - start
    print(f"Finished in {elapsed:.1f}s")


def main():
    pipeline = ProductionPipeline()
    books = discover_books()

    # ---- Apply prefix filter ----
    if PREFIX:
        print(f"Filtering books with prefix: {PREFIX}")
        books = [b for b in books if b.stem.startswith(PREFIX)]
    else:
        print("No prefix filter applied (processing all books)")

    print("=" * 100)
    print(f"TOTAL BOOKS TO PROCESS: {len(books)}")
    print("=" * 100)

    success = 0
    skipped = 0
    failed = []

    for pdf in books:

        relative = pdf.relative_to(PDF_ROOT)
        out_dir = OUTPUT_ROOT / relative.with_suffix("")
        existing = out_dir / "master_dataset.jsonl"

        # ---- SKIP if already processed ----
        if existing.exists():
            print(f"[SKIP] {relative}")
            skipped += 1
            continue

        # ---- Process book ----
        try:
            build_book(pipeline, pdf)
            success += 1
        except Exception:
            traceback.print_exc()
            failed.append(pdf)
            continue

    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print("SUCCESS :", success)
    print("SKIPPED :", skipped)
    print("FAILED  :", len(failed))
    if failed:
        print("\nFAILED BOOKS\n")
        for f in failed:
            print(f)


if __name__ == "__main__":
    main()
