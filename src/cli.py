import argparse

from src.extractor.extractor import Extractor


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("pdf")

    parser.add_argument("-o", "--output", required=True)

    args = parser.parse_args()

    Extractor().extract(
        pdf_path=args.pdf,
        output_dir=args.output,
    )


if __name__ == "__main__":
    main()
