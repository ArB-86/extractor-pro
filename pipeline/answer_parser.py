import re


ANSWER_PATTERN = re.compile(
    r"Answer\s*:?\s*\(?([A-D])\)?",
    re.IGNORECASE
)


class AnswerParser:

    def parse(self, text):

        m = ANSWER_PATTERN.search(text)

        if m:
            return m.group(1)

        return None
