import re


class FormulaMerger:

    def merge(self, text: str):

        if not text:
            return text

        # remove isolated line breaks inside formulas

        text = re.sub(
            r'([A-Za-z0-9θαβπ])\n([A-Za-z0-9θαβπ])',
            r'\1 \2',
            text
        )

        # cos\nθ  -> cos θ

        text = re.sub(
            r'(sin|cos|tan|cot|sec|cosec)\s*\n\s*',
            r'\1 ',
            text,
            flags=re.I
        )

        # x\n2 -> x², x\n3 -> x³

        text = re.sub(
            r'([A-Za-zα-ωΑ-Ωθπ])\s*\n\s*2\b',
            r'\1²',
            text
        )

        text = re.sub(
            r'([A-Za-zα-ωΑ-Ωθπ])\s*\n\s*3\b',
            r'\1³',
            text
        )

        # merge broken fractions: a \n b \n c patterns with operators
        text = re.sub(
            r'(\d+)\s*\n\s*/\s*\n\s*(\d+)',
            r'\1/\2',
            text
        )

        return text
