from __future__ import annotations


REQUIRED = (

    "question_text",

    "chapter",

    "exercise",

    "question_number",

)


class GoldDatasetValidator:

    def validate(self,data):

        errors=[]

        for i,row in enumerate(data):

            for key in REQUIRED:

                if not row.get(key):

                    errors.append(

                        f"{i}: missing {key}"

                    )

        return (

            len(errors)==0,

            errors,

        )
