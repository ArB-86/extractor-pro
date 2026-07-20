from pathlib import Path


class FigureLinker:

    def link(self, questions, figures):

        by_page = {}

        for f in figures:
            by_page.setdefault(f["page"], []).append(f)

        for q in questions:

            page = q.page_start

            q.figure = None

            if page in by_page:

                q.figure = by_page[page][0]["path"]

        return questions
