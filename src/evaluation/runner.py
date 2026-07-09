
from __future__ import annotations

from dataclasses import asdict

from src.evaluation.gold_loader import GoldLoader
from src.evaluation.aligner import QuestionAligner
from src.evaluation.question_metrics import QuestionMetrics
from src.evaluation.chapter_metrics import ChapterMetrics
from src.evaluation.exercise_metrics import ExerciseMetrics
from src.evaluation.boundary import BoundaryMetrics
from src.evaluation.ocr_metrics import OCRMetrics
from src.evaluation.error_analyzer import ErrorAnalyzer
from src.evaluation.json_report import JSONReport
from src.evaluation.regression import RegressionTracker
from src.evaluation.benchmark import BenchmarkRunner


class EvaluationRunner:

    def __init__(self):

        self.gold = GoldLoader()

        self.aligner = QuestionAligner()

        self.question = QuestionMetrics()

        self.chapter = ChapterMetrics()

        self.exercise = ExerciseMetrics()

        self.boundary = BoundaryMetrics()

        self.ocr = OCRMetrics()

        self.errors = ErrorAnalyzer()

        self.report = JSONReport()
        self.regression = RegressionTracker()
        self.benchmark = BenchmarkRunner()

    def run(
        self,
        predicted,
        gold_path,
        output_path=None,
        baseline=None,
    ):

        
        gold = self.benchmark.run(
            self.gold.load,
            gold_path,
        )["result"]["result"]


        
        alignment = self.benchmark.run(
            self.aligner.align,

            predicted,
            gold,
        )

        result = {

            "question": self.question.compute(alignment),

            "chapter": self.chapter.compute(alignment),

            "exercise": self.exercise.compute(alignment),

            "boundary": self.boundary.compute(alignment),

            "ocr": self.ocr.compute(alignment),

            "errors": self.errors.compute(alignment),

        }

        result["regression"] = self.regression.compare(
            result,
            baseline,
        )

        if output_path:

            self.report.write(
                result,
                output_path,
            )

        return result
