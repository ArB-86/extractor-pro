from pipeline.core.stage import Stage

import hashlib
import re


def sha(text):

    return hashlib.sha256(
        text.encode("utf8")
    ).hexdigest()


def detect_class(source):

    s = source.lower()

    if "fegp" in s or "feep" in s:
        return 6

    if "gegp" in s or "gemp" in s:
        return 7

    if "hegp" in s or "heep" in s:
        return 8

    if "iemh" in s or "ieep" in s:
        return 9

    if "jemh" in s or "jeep" in s:
        return 10

    if "kemh" in s or "keep" in s:
        return 11

    return 0


class QuestionEnrichmentStage(Stage):

    def run(self, context):

        enriched = []

        counter = 1

        for q in context.questions:

            if len(q.question.strip()) < 15:
                continue

            q.class_no = detect_class(
                q.source
            )

            q.board = "CBSE"

            q.publisher = "NCERT"

            q.language = "English"

            q.parser_version = "3"

            q.content_hash = sha(
                q.question
            )

            q.question_id = (
                f"C{q.class_no}_"
                f"{counter:06d}"
            )

            words = re.findall(
                r"[A-Za-z]{4,}",
                q.question.lower()
            )

            q.keywords = sorted(
                set(words)
            )[:20]

            q.validation_score = 1.0

            q.verified = True

            enriched.append(q)

            counter += 1

        context.questions = enriched

        return context
