import re


class SolutionExtractor:

    PATTERNS = [
        re.compile(r"Solution\s*[:\-]\s*(.*)", re.I | re.S),
        re.compile(r"Solutions\s*[:\-]\s*(.*)", re.I | re.S),
    ]

    def extract(self, text):

        if not text:
            return None

        for p in self.PATTERNS:

            m = p.search(text)

            if m:

                ans = m.group(1).strip()

                if len(ans) > 5:
                    return ans

        return None
