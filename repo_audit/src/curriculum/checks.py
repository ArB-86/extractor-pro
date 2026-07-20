class CurriculumChecks:

    def validate(self, manifests):

        errors = []

        for m in manifests:

            if m.get("class") is None:
                errors.append(
                    {
                        "file": m["file"],
                        "error": "Class not detected",
                    }
                )

            if m.get("book_type") is None:
                errors.append(
                    {
                        "file": m["file"],
                        "error": "Book type not detected",
                    }
                )

        return errors
