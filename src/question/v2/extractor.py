from __future__ import annotations

import re

from src.document.document import Document

from src.question.v2.context import ContextManager
from src.question.v2.numbering import NumberingDetector
from src.question.v2.boundary import BoundaryDetector
from src.question.v2.assembler import QuestionAssembler
from src.question.v2.classifier import QuestionClassifier
from src.question.v2.validator import QuestionValidator
from src.question.v2.converter import CandidateConverter
from src.question.v2.statistics import ExtractionStats
from src.question.postprocess.teacher_guide_filter import TeacherGuideFilter
from src.question.postprocess.ocr_repair import OCRRepair
from src.question.postprocess.question_cleaner import QuestionCleaner
from src.question.postprocess.near_duplicate_filter import NearDuplicateFilter  # new


class QuestionExtractorV2:

    def __init__(self):

        self.context = ContextManager()

        self.numbering = NumberingDetector()

        self.boundary = BoundaryDetector()

        self.assembler = QuestionAssembler()

        self.classifier = QuestionClassifier()

        self.validator = QuestionValidator()

        self.converter = CandidateConverter()

        self.stats = ExtractionStats()

        self.teacher_filter = TeacherGuideFilter()

        self.ocr_repair = OCRRepair()

        self.question_cleaner = QuestionCleaner()

        self.near_duplicate_filter = NearDuplicateFilter()  # new

    def extract(
        self,
        document: Document,
    ):

        state = self.context.state

        # ---- DEBUG: Print region order ----
        for i, region in enumerate(document.regions):
            self.stats.total_regions += 1

            print("=" * 100)
            print(f"REGION {i}")
            print(f"label: {region.label}")
            print(f"page : {region.page}")
            print(f"bbox : {getattr(region, 'bbox', None)}")
            print(f"text : {repr(region.text[:80])}")
            print("-" * 80)

            if not region.text:
                print("SKIP (empty text)")
                self.stats.skipped_regions += 1
                continue

            state = self.context.update(region)

            print(f"CHAPTER AFTER UPDATE: {state.chapter}")
            print(f"SECTION AFTER UPDATE: {state.section}")
            print(f"ZONE AFTER UPDATE  : {state.zone}")
            print("=" * 100)

            # ---- Use region.text, not accumulated metadata ----
            current_text = region.text or ""

            # Temporary debug
            print("=" * 80)
            print("SPLIT INPUT")
            print(repr(current_text[:300]))
            print("=" * 80)

            for chunk in self._split_questions(current_text):
                text = chunk.strip()
                if not text:
                    continue

                signal = self.numbering.read(text)

                boundary = self.boundary.classify(
                    text=text,
                    state=state,
                    signal=signal,
                )

                # DEBUG: print boundary, signal, and first 80 chars of text
                print(
                    f"[DBG] boundary={boundary} "
                    f"signal={signal.kind} "
                    f"text={text[:80]!r}"
                )

                # ADDED: Assembler state debug
                print(
                    f"[ASM] "
                    f"qno={state.question_number!r} "
                    f"open={state.question_open} "
                    f"boundary={boundary.value} "
                    f"signal={signal.kind!r}"
                )

                self.assembler.consume(
                    text=text,
                    state=state,
                    boundary=boundary,
                    signal=signal,
                )

        questions = self.assembler.finalize(
            state,
        )

        self.stats.candidates = len(questions)

        # ---- DEBUG 1: After assembler ----
        print("\n" + "=" * 100)
        print("AFTER ASSEMBLER")
        print("=" * 100)

        for q in questions:
            print(
                q.number,
                "|",
                q.context.chapter,
                "|",
                repr(q.text[:80]),
            )
        print("-" * 100)

        print(
            f"[QuestionExtractor] assembled {self.stats.candidates} candidates"
        )

        questions = self.classifier.classify(
            questions,
        )

        questions = self.validator.validate(
            questions,
        )

        self.stats.validated = len(questions)

        # ---- DEBUG 2: After validator ----
        print("\n" + "=" * 100)
        print("AFTER VALIDATOR")
        print("=" * 100)
        for q in questions:
            print(
                q.number,
                "|",
                q.context.chapter,
                "|",
                repr(q.text[:60])
            )
        print("-" * 100)

        # ---- Convert to Question objects ----
        questions = self.converter.convert(
            questions,
        )

        print("=" * 80)
        print("AFTER CONVERTER")
        print("len(questions) =", len(questions))
        print("=" * 80)

        print("=" * 80)
        print("BEFORE TEACHER FILTER:", len(questions))

        # ---- Apply teacher guide filter ----
        questions = self.teacher_filter.process(
            questions,
        )

        print("AFTER TEACHER FILTER :", len(questions))
        print("=" * 80)

        # ---- Apply near-duplicate filter ----
        before = len(questions)
        questions = self.near_duplicate_filter.process(
            questions,
        )
        print(
            f"Near duplicates removed: {before - len(questions)}"
        )
        print("=" * 80)

        # ---- Apply OCR repair ----
        questions = self.ocr_repair.process(
            questions,
        )

        # ---- Apply question cleaner ----
        questions = self.question_cleaner.process(
            questions,
        )

        self.stats.converted = len(questions)

        print(
            f"[QuestionExtractor] converted {self.stats.converted} questions"
        )

        # ---- Print statistics report ----
        print("\n" + "=" * 80)
        print("EXTRACTION STATISTICS")
        print("=" * 80)
        print(f"Total regions      : {self.stats.total_regions}")
        print(f"Skipped regions    : {self.stats.skipped_regions}")
        print(f"Candidates         : {self.stats.candidates}")
        print(f"Validated          : {self.stats.validated}")
        print(f"Converted          : {self.stats.converted}")
        print(f"Duplicates         : {self.stats.duplicates}")
        print("=" * 80)

        return questions

    @staticmethod
    def _split_questions(text: str) -> list[str]:

        if not text:
            return []

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        lines = [
            x.strip()
            for x in text.split("\n")
            if x.strip()
        ]

        if not lines:
            return []

        # ---- Preprocess: split lines that contain embedded question numbers ----
        embedded = re.compile(
            r"""
            (?<!^)
            (?=
                (?:Question\s+|Q\.?\s*)?
                [1-9]\d*
                [.)。．﹒․]
                \s+
            )
            """,
            re.I | re.X,
        )

        expanded = []
        for line in lines:
            expanded.extend(
                x.strip()
                for x in embedded.split(line)
                if x.strip()
            )

        starts = re.compile(
            r"""
            ^
            (?:Question\s+|Q\.?\s*)?
            ([1-9]\d*)
            [.)。．﹒․]
            \s+
            """,
            re.I | re.X,
        )

        good = {
            "what",
            "why",
            "which",
            "who",
            "where",
            "when",
            "how",
            "find",
            "draw",
            "write",
            "state",
            "show",
            "calculate",
            "determine",
            "prove",
            "construct",
            "identify",
            "observe",
            "complete",
            "fill",
            "choose",
            "match",
            "can",
            "is",
            "are",
            "do",
            "does",
        }

        bad = (
            "table",
            "figure",
            "fig",
            "example",
            "activity",
            "solution",
            "answer",
            "summary",
            "chapter",
            "section",
        )

        chunks = []
        current = []

        for line in expanded:

            m = starts.match(line)

            if m:

                remainder = line[m.end():].strip()

                first = (
                    remainder.split(maxsplit=1)[0].lower()
                    if remainder
                    else ""
                )

                if (
                    first in good
                    and not remainder.lower().startswith(bad)
                ):

                    if current:
                        chunks.append(
                            "\n".join(current).strip()
                        )

                    current = [line]

                    continue

            if current:
                current.append(line)
            else:
                current = [line]

        if current:
            chunks.append(
                "\n".join(current).strip()
            )

        return chunks
