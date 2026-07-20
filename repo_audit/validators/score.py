
class DatasetScore:

    def compute(self, report):

        total = 0
        errors = 0

        for result in report.values():

            total += 1

            if result:
                errors += 1

        passed = total - errors

        if total == 0:
            score = 100.0
        else:
            score = round(
                passed / total * 100,
                2
            )

        return {

            "score": score,
            "passed": passed,
            "errors": errors

        }
