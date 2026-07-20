from pipeline.models.question import Question
from pipeline.question_parser_v3.state import ParserState
from pipeline.question_parser_v3.detectors import *

import hashlib


class QuestionParserV3:

    def parse(self, lines, tracker, pdf):

        state = ParserState()

        for line in lines:

            tracker.update(line)

            text = line.text.strip()

            if not text:
                continue

            if PAGE.match(text):
                continue

            if FIGURE.match(text):
                continue

            if EXERCISE.match(text) or SECTION.match(text) or SUMMARY.match(text):

                if state.current_question:
                    state.questions.append(state.current_question)
                    state.current_question=None

                continue

            if QUESTION.match(text):

                if state.current_question:
                    state.questions.append(state.current_question)

                q = Question()

                q.question_no = text.split(".")[0]

                q.question_id = hashlib.sha1(
                    f"{pdf}-{line.page}-{q.question_no}".encode()
                ).hexdigest()[:16]

                q.source = pdf
                q.chapter = tracker.section
                q.section = tracker.section
                q.exercise = tracker.exercise
                q.page_start = line.page
                q.page_end = line.page
                q.question = text

                state.current_question = q
                continue

            if state.current_question is None:
                continue

            state.current_question.page_end = line.page

            # Always append every non-header line.
            state.current_question.question += "\n" + text

        if state.current_question:
            state.questions.append(state.current_question)

        return state.questions
