from pathlib import Path
import argparse

from pipeline.core.context import PipelineContext
from pipeline.core.default_pipeline import build
from pipeline.core.engine import PipelineEngine


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="PDF file"
    )

    parser.add_argument(
        "--debug",
        default=None
    )

    args = parser.parse_args()

    ctx = PipelineContext(
        pdf=str(Path(args.input).resolve())
    )

    engine = PipelineEngine(build())

    engine.run(
        ctx,
        debug_dir=args.debug
    )

    print("DONE")


if __name__ == "__main__":
    main()
