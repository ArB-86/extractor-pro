
class SchemaValidator:

    REQUIRED = [

        "id",
        "source",
        "chapter",
        "exercise",
        "page_start",
        "page_end",
        "question",
        "question_type",
        "difficulty",
        "topic",
        "options",
        "answer",
        "solution"

    ]

    def validate(self, q):

        missing=[]

        for field in self.REQUIRED:

            if field not in q:

                missing.append(field)

        return missing
