from pathlib import Path

from parsers.pdf_parser import PDFParser
from pipeline.layout.line_extractor import LineExtractor
from pipeline.features.statistics import LayoutStatistics


def analyze(pdf_path: str):

    blocks = PDFParser(pdf_path).extract()
    lines = LineExtractor().extract(blocks)

    stats = LayoutStatistics().compute(lines)

    print("=" * 70)
    print("PDF :", Path(pdf_path).name)
    print("=" * 70)
    print(f"Pages              : {stats.total_pages}")
    print(f"Lines              : {stats.total_lines}")
    print(f"Body Font          : {stats.body_font}")
    print(f"Body Font Size     : {stats.body_font_size}")
    print(f"Median Font Size   : {stats.median_font_size}")
    print(f"Largest Font Size  : {stats.largest_font_size}")
    print(f"Smallest Font Size : {stats.smallest_font_size:.2f}")
    print(f"Average Indent     : {stats.average_indent:.2f}")
    print("=" * 70)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")

    args = parser.parse_args()

    analyze(args.pdf)
