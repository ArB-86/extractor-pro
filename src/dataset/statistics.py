from collections import Counter


class DatasetStatistics:

    def build(self, questions):

        return {
            "total_questions": len(questions),
            "chapters": dict(
                Counter(q.chapter for q in questions)
            ),
            "difficulty": dict(
                Counter(q.difficulty for q in questions)
            ),
            "question_types": dict(
                Counter(q.question_type for q in questions)
            ),
        }
