from pathlib import Path
import json

from src.benchmark.alignment import AlignmentEngine
from src.document.question import Question


class BenchmarkEvaluator:

    def __init__(self):

        self.alignment = AlignmentEngine()

    def _load(self, path):

        path = Path(path)

        with open(path, encoding="utf-8") as f:

            data = json.load(f)

        questions = []

        for item in data["questions"]:

            questions.append(
                Question(
                    question_text=item["question_text"],
                    question_id=item.get("question_id", ""),
                    chapter=item.get("chapter"),
                    exercise=item.get("exercise"),
                    question_number=item.get("question_number"),
                    question_type=item.get("question_type"),
                    difficulty=item.get("difficulty"),
                )
            )

        return questions

    def evaluate(
        self,
        predicted_file,
        gold_file,
    ):

        predicted = self._load(predicted_file)

        gold = self._load(gold_file)

        return self.alignment.evaluate(
            predicted,
            gold,
        )
