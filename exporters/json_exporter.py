import json


class JSONExporter:

    DEFAULT_MARKS = "3"
    DEFAULT_DIFFICULTY = 0.5

    def export(self, questions, output_file, class_grade: int | None = None):

        self.export_master(questions, output_file, class_grade=class_grade)

    def export_master(self, questions, output_file, class_grade: int | None = None):

        import uuid

        data = []

        for q in questions:

            grade = class_grade if class_grade is not None else self._class_from_question(q)

            data.append(
                {
                    "question_id": str(uuid.uuid4()),
                    "class": grade,
                    "subject": "Mathematics",
                    "chapter": q.chapter,
                    "marks": self.DEFAULT_MARKS,
                    "difficulty_index": self.DEFAULT_DIFFICULTY,
                    "question_text": q.question.strip(),
                    "has_image": False,
                    "image_url": None,
                }
            )

        with open(output_file, "w", encoding="utf8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )

    def _class_from_question(self, q):

        chapter = (q.chapter or "").lower()

        for prefix, grade in (
            ("feep", 6),
            ("gemp", 7),
            ("heep", 8),
            ("ieep", 9),
            ("jeep", 10),
            ("keep", 11),
            ("fegp", 6),
            ("gegp", 7),
            ("hegp", 8),
            ("iemh", 9),
            ("jemh", 10),
            ("kemh", 11),
        ):
            if chapter.startswith(prefix):
                return grade

        return 0
