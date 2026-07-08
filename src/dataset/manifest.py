from datetime import datetime


class DatasetManifest:

    def build(self, questions):

        return {
            "dataset_version": datetime.utcnow().strftime("%Y.%m.%d"),
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "total_questions": len(questions),
        }
