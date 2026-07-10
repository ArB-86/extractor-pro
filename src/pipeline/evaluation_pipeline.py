from pathlib import Path

from src.evaluation.runner import EvaluationRunner


class EvaluationPipeline:

    def __init__(self):

        self.runner = EvaluationRunner()

    def run(
        self,
        extraction_result,
        gold_path=None,
    ):

        if not gold_path:
            return extraction_result

        print(f"[EvaluationPipeline] predicted: {len(extraction_result.questions)}")

        report = self.runner.run(
            predicted=extraction_result.questions,
            gold_path=gold_path,
            output_path=Path(
                extraction_result.output_directory
            ) / "evaluation.json",
        )

        extraction_result.evaluation = report

        return extraction_result
