import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.core.context import PipelineContext
from pipeline.core.default_pipeline import build
from pipeline.core.engine import PipelineEngine


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Dump intermediate outputs for one PDF through the extractor pipeline.",
	)
	parser.add_argument("--pdf", required=True, help="Path to the PDF to debug.")
	return parser.parse_args()


def run_debug_pipeline(pdf_path: Path) -> Path:
	if not pdf_path.exists():
		raise FileNotFoundError(str(pdf_path))

	context = PipelineContext(pdf=str(pdf_path))
	debug_root = PROJECT_ROOT / "debug"
	PipelineEngine(build()).run(context, debug_dir=debug_root)
	return debug_root / pdf_path.stem


def main() -> None:
	args = parse_args()
	output_dir = run_debug_pipeline(Path(args.pdf).expanduser().resolve())
	print(output_dir)


if __name__ == "__main__":
	main()
