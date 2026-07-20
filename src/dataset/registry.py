from hashlib import sha256


class QuestionRegistry:

    def __init__(self):
        self._questions = {}

    def add(self, question):
        # Use existing sha256 if present, otherwise compute from question text and context
        key = getattr(question, "sha256", None)
        if not key:
            # Compute a stable fingerprint
            text = (question.question_text or "").strip()
            chapter = question.chapter or ""
            qnum = question.question_number or ""
            key = sha256(
                f"{chapter}|{qnum}|{text}".encode("utf-8")
            ).hexdigest()
            question.sha256 = key  # <-- assign back to question

        self._questions[key] = question

    def extend(self, questions):
        for q in questions:
            self.add(q)

    def all(self):
        return list(self._questions.values())

    def __len__(self):
        return len(self._questions)
