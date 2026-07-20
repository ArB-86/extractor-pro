
class PipelineReport:

    def print(self, context):

        print()

        print("="*70)

        print("PIPELINE REPORT")

        print("="*70)

        for stage,time in context.metrics.get(
            "stage_times",
            {}
        ).items():

            print(f"{stage:35} {time:.4f}s")

        print()

        print(
            "Questions:",
            len(context.questions)
        )

        print(
            "Figures:",
            len(context.figures)
        )

        print(
            "Errors:",
            len(context.errors)
        )

        print("="*70)
