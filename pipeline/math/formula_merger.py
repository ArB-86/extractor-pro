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

        # x\n2 -> x²

        text = re.sub(
            r'([A-Za-zα-ωΑ-Ωθπ])\s*\n\s*2\b',
            r'\1²',
            text
        )

        return text
