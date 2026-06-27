import json


class DatasetValidator:

    def validate(self, json_file):

        with open(json_file, encoding="utf8") as f:
            data = json.load(f)

        errors = []

        for q in data:

            required = [
                "id",
                "source",
                "chapter",
                "exercise",
                "page_start",
                "page_end",
                "question_type",
                "question",
            ]

            for field in required:

                if field not in q:
                    errors.append(
                        f'Question {q.get("id")} missing "{field}"'
                    )

            if not q.get("question", "").strip():
                errors.append(
                    f'Question {q.get("id")} has empty question'
                )

            if q.get("question_type") == "mcq":

                if len(q.get("options", {})) < 2:
                    errors.append(
                        f'MCQ {q.get("id")} missing options'
                    )

        return errors
