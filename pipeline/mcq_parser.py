import re


OPTION_PATTERN = re.compile(
    r"\(([A-D])\)\s*(.*?)(?=(\([A-D]\)|$))",
    re.DOTALL
)


class MCQParser:

    def parse(self, text):

        options = {}

        for m in OPTION_PATTERN.finditer(text):

            key = m.group(1)

            value = m.group(2).strip()

            options[key] = value

        return options
