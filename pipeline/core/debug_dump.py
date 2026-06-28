from __future__ import annotations

import json
import shutil
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Callable


def _metadata_snapshot(context) -> Any:
	return context.metadata


def _blocks_snapshot(context) -> Any:
	return context.blocks


def _sections_snapshot(context) -> Any:
	return context.metadata.get("sections", [])


def _questions_snapshot(context) -> Any:
	return context.questions


STAGE_FILES: dict[str, tuple[str, Callable[[Any], Any]]] = {
	"MetadataStage": ("01_MetadataStage.json", _metadata_snapshot),
	"PDFParserStage": ("02_PDFParserStage.txt", _blocks_snapshot),
	"BlockSplitterStage": ("03_BlockSplitterStage.txt", _blocks_snapshot),
	"BlockMergerStage": ("04_BlockMergerStage.txt", _blocks_snapshot),
	"BlockNormalizerStage": ("05_BlockNormalizerStage.txt", _blocks_snapshot),
	"LayoutCleanerStage": ("06_LayoutCleanerStage.txt", _blocks_snapshot),
	"SectionParserStage": ("07_SectionParserStage.txt", _sections_snapshot),
	"QuestionParserStage": ("08_QuestionParserStage.json", _questions_snapshot),
	"QuestionEnrichmentStage": ("09_QuestionEnrichmentStage.json", _questions_snapshot),
}


class PipelineDebugger:

	def __init__(self, debug_root: Path, pdf_path: str):
		self.output_dir = debug_root / Path(pdf_path).stem
		if self.output_dir.exists():
			shutil.rmtree(self.output_dir)
		self.output_dir.mkdir(parents=True, exist_ok=True)

	def dump(self, stage, context) -> None:
		stage_name = stage.__class__.__name__
		spec = STAGE_FILES.get(stage_name)
		if spec is None:
			return

		filename, snapshot = spec
		path = self.output_dir / filename
		path.write_text(
			json.dumps(serialize(snapshot(context)), indent=2, ensure_ascii=False),
			encoding="utf8",
		)


def serialize(value: Any) -> Any:
	if is_dataclass(value):
		return asdict(value)

	if isinstance(value, dict):
		return {key: serialize(item) for key, item in value.items()}

	if isinstance(value, (list, tuple)):
		return [serialize(item) for item in value]

	if isinstance(value, Path):
		return str(value)

	return value