from datetime import datetime


class CurriculumVersion:

    def build(self):

        return {
            "version": datetime.utcnow().strftime("%Y.%m.%d"),
            "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        }
