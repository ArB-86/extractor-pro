from pathlib import Path

from src.curriculum.auditor import CurriculumAuditor
from src.curriculum.report import CurriculumReport


class CurriculumRunner:

    def run(self, root, output):

        audit = CurriculumAuditor().audit(root)

        CurriculumReport().save(
            audit,
            Path(output) / "curriculum_audit.json",
        )

        return audit
