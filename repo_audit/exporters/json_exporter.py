import json
import uuid

class JSONExporter:
    DEFAULT_MARKS = "3"
    DEFAULT_DIFFICULTY = 0.5

    def export(self, questions, output_file, class_grade: int | None = None):
        print(f"DEBUG: JSONExporter called. Received list of length: {len(questions)}")
        if len(questions) > 0:
            print(f"DEBUG: First question text: {getattr(questions[0], 'question', 'MISSING')[:50]}...")
        else:
            print("DEBUG: ALERT - Exporter received an EMPTY list of questions.")
        
        self.export_master(questions, output_file, class_grade=class_grade)

    def export_master(self, questions, output_file, class_grade: int | None = None):
        data = []
        for q in questions:
            # Handle potential attribute variations
            q_text = getattr(q, 'question', str(q))
            q_chapter = getattr(q, 'chapter', 'unknown')
            
            grade = class_grade if class_grade is not None else self._class_from_question(q)
            data.append({
                "question_id": str(uuid.uuid4()),
                "class": grade,
                "subject": "Mathematics",
                "chapter": q_chapter,
                "marks": self.DEFAULT_MARKS,
                "difficulty_index": self.DEFAULT_DIFFICULTY,
                "question_text": str(q_text).strip(),
                "has_image": False,
                "image_url": None,
            })

        with open(output_file, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"DEBUG: JSON file successfully written to {output_file}")

    def _class_from_question(self, q):
        chapter = str(getattr(q, 'chapter', "")).lower()
        for prefix, grade in (("kemh", 11), ("jemh", 10), ("iemh", 9), ("hegp", 8), ("gegp", 7), ("fegp", 6)):
            if chapter.startswith(prefix):
                return grade
        return 0
