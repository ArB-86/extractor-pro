import json


class JSONExporter:

    def export(self, questions, output_file):

        data = []

        for q in questions:
            data.append({
                "id": q.id,
                "source": q.source,
                "chapter": q.chapter,
                "exercise": q.exercise,
                "page_start": q.page_start,
                "page_end": q.page_end,
                "question_type": q.question_type,
                "difficulty": q.difficulty,
                "topic": q.topic,
                "question": q.question,
                "options": q.options,
                "answer": q.answer,
                "solution": q.solution
            })

        with open(output_file, "w", encoding="utf8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )