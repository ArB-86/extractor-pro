from __future__ import annotations

from pathlib import Path

from src.evaluation.runner import EvaluationRunner


class BenchmarkRunner:

    def run(

        self,

        predicted,

        gold,

        output,

    ):

        output = Path(output)

        output.mkdir(

            parents=True,

            exist_ok=True,

        )

        report = EvaluationRunner().run(

            predicted,

            gold,

            output,

        )

        return report
