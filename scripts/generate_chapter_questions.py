import argparse
import json

from pipeline.ai.factory import create_model
from pipeline.generation.chapter_generator import ChapterGenerator


def main():

    ap=argparse.ArgumentParser()

    ap.add_argument("--chapter_pdf",required=True)
    ap.add_argument("--ncert",required=True)
    ap.add_argument("--exemplar",required=True)
    ap.add_argument("--output",required=True)

    args=ap.parse_args()

    model=create_model()

    generator=ChapterGenerator(model)

    with open(args.ncert,"r",encoding="utf8") as f:
        ncert=json.load(f)

    with open(args.exemplar,"r",encoding="utf8") as f:
        exemplar=json.load(f)

    generated=generator.generate(
        chapter_pdf=args.chapter_pdf,
        extracted_questions=ncert,
        exemplar_questions=exemplar,
    )

    with open(args.output,"w",encoding="utf8") as f:
        json.dump(
            generated,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print("Generated:",len(generated))


if __name__=="__main__":
    main()
