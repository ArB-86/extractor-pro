from __future__ import annotations

from .question_metrics import QuestionMetrics
from .boundary import BoundaryMetrics
from .chapter_metrics import ChapterMetrics
from .exercise_metrics import ExerciseMetrics
from .ocr_metrics import OCRMetrics


class MetricsEngine:

    def compute(

        self,

        alignment,

    ):

        return {

            "question_metrics":

                alignment.question_metrics.to_dict(),

            "boundary_metrics":

                alignment.boundary_metrics.to_dict(),

        }

    def empty(self):

        return {

            "question_metrics":

                QuestionMetrics().to_dict(),

            "boundary_metrics":

                BoundaryMetrics().to_dict(),

            "chapter_metrics":

                ChapterMetrics().to_dict(),

            "exercise_metrics":

                ExerciseMetrics().to_dict(),

            "ocr_metrics":

                OCRMetrics().to_dict(),

        }
