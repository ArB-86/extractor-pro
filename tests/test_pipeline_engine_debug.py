from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from pipeline.core.context import PipelineContext
from pipeline.core.engine import PipelineEngine


@dataclass
class Block:
    page: int
    text: str
    bbox: tuple[int, int, int, int]


@dataclass
class Section:
    title: str
    page_start: int
    page_end: int
    blocks: list[Block]


@dataclass
class Question:
    id: int
    source: str
    chapter: str
    exercise: str
    page_start: int
    page_end: int
    question_type: str
    question: str
    answer: str = ""


class MetadataStage:

	def run(self, context: PipelineContext) -> PipelineContext:
		context.metadata.update({"source": "NCERT", "chapter": "demo"})
		return context


class PDFParserStage:

	def run(self, context: PipelineContext) -> PipelineContext:
		context.blocks = [
			Block(1, "1. Solve x + 1 = 2", (1, 2, 3, 4)),
			Block(1, "Try This activity should not matter here", (5, 6, 7, 8)),
		]
		return context


class BlockSplitterStage:

	def run(self, context: PipelineContext) -> PipelineContext:
		context.blocks.append(Block(1, "2. Next question", (9, 10, 11, 12)))
		return context


class BlockMergerStage:

	def run(self, context: PipelineContext) -> PipelineContext:
		context.blocks[0] = Block(1, context.blocks[0].text + " merged", context.blocks[0].bbox)
		return context


class BlockNormalizerStage:

	def run(self, context: PipelineContext) -> PipelineContext:
		context.blocks = context.blocks[:2]
		return context


class LayoutCleanerStage:

	def run(self, context: PipelineContext) -> PipelineContext:
		context.blocks = context.blocks
		return context


class SectionParserStage:

	def run(self, context: PipelineContext) -> PipelineContext:
		context.metadata["sections"] = [
			Section("Exercise 1", 1, 1, context.blocks[:1]),
		]
		return context


class QuestionParserStage:

	def run(self, context: PipelineContext) -> PipelineContext:
		context.questions = [
			Question(1, "NCERT", "demo", "Exercise 1", 1, 1, "unknown", "1. Solve x + 1 = 2"),
		]
		return context


class QuestionEnrichmentStage:

	def run(self, context: PipelineContext) -> PipelineContext:
		context.questions[0].answer = "2"
		return context


def test_pipeline_engine_writes_native_debug_dumps(tmp_path: Path) -> None:
	context = PipelineContext(pdf="/tmp/sample.pdf")
	engine = PipelineEngine(
		[
			MetadataStage(),
			PDFParserStage(),
			BlockSplitterStage(),
			BlockMergerStage(),
			BlockNormalizerStage(),
			LayoutCleanerStage(),
			SectionParserStage(),
			QuestionParserStage(),
			QuestionEnrichmentStage(),
		]
	)

	output_context = engine.run(context, debug_dir=tmp_path / "debug")
	output_dir = tmp_path / "debug" / "sample"

	assert output_context.questions[0].answer == "2"
	assert sorted(path.name for path in output_dir.iterdir()) == [
		"01_MetadataStage.json",
		"02_PDFParserStage.txt",
		"03_BlockSplitterStage.txt",
		"04_BlockMergerStage.txt",
		"05_BlockNormalizerStage.txt",
		"06_LayoutCleanerStage.txt",
		"07_SectionParserStage.txt",
		"08_QuestionParserStage.json",
		"09_QuestionEnrichmentStage.json",
	]

	metadata = json.loads((output_dir / "01_MetadataStage.json").read_text(encoding="utf8"))
	blocks = json.loads((output_dir / "02_PDFParserStage.txt").read_text(encoding="utf8"))
	questions = json.loads((output_dir / "09_QuestionEnrichmentStage.json").read_text(encoding="utf8"))

	assert metadata["chapter"] == "demo"
	assert blocks[0]["text"].startswith("1. Solve x + 1 = 2")
	assert questions[0]["answer"] == "2"