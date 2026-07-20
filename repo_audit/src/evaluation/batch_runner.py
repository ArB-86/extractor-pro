from __future__ import annotations

from pathlib import Path

from src.evaluation.runner import EvaluationRunner


class BatchEvaluationRunner:

    def run(

        self,

        datasets,

        output,

    ):

        output=Path(output)

        output.mkdir(

            parents=True,

            exist_ok=True,

        )

        results=[]

        runner=EvaluationRunner()

        for pred,gold,name in datasets:

            report=runner.run(

                pred,

                gold,

                output/name,

            )

            results.append(

                (

                    name,

                    report,

                )

            )

        return results
