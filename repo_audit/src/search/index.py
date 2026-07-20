from collections import defaultdict


class SearchIndex:

    def build(self, questions):

        index = defaultdict(list)

        for q in questions:

            if q.chapter:
                index[q.chapter].append(q.question_id)

            if q.question_type:
                index[q.question_type].append(q.question_id)

        return dict(index)
