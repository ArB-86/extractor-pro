import argparse

from src.extractor.extractor import Extractor
from src.curriculum.run import CurriculumRunner


def main():

    parser = argparse.ArgumentParser()

    sub = parser.add_subparsers(dest="command", required=True)

    extract = sub.add_parser("extract")
    extract.add_argument("pdf")
    extract.add_argument("-o", "--output", required=True)

    curriculum = sub.add_parser("curriculum")
    curriculum.add_argument("root")
    curriculum.add_argument("-o", "--output", required=True)

    args = parser.parse_args()

    if args.command == "extract":
        Extractor().extract(
            pdf_path=args.pdf,
            output_dir=args.output,
        )

    elif args.command == "curriculum":
        CurriculumRunner().run(
            root=args.root,
            output=args.output,
        )


if __name__ == "__main__":
    main()
