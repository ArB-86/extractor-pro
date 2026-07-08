from src.curriculum.inventory import CurriculumInventory
from src.curriculum.manifest import ManifestBuilder
from src.curriculum.duplicate_detector import DuplicateDetector
from src.curriculum.mapper import CurriculumMapper
from src.curriculum.statistics import CurriculumStatistics  # new import
from src.curriculum.report import CurriculumReport  # new import


class CurriculumAuditor:

    def __init__(self):

        self.inventory = CurriculumInventory()
        self.manifest = ManifestBuilder()
        self.duplicates = DuplicateDetector()
        self.mapper = CurriculumMapper()
        self.statistics = CurriculumStatistics()  # new statistics instance
        self.report = CurriculumReport()  # new report instance

    def audit(self, root):

        pdfs = self.inventory.scan(root)

        manifests = [
            self.mapper.map(
                self.manifest.build(pdf)
            )
            for pdf in pdfs
        ]

        duplicates = self.duplicates.detect(manifests)

        stats = self.statistics.build(manifests)

        audit = {
            "total_pdfs": len(pdfs),
            "duplicates": duplicates,
            "statistics": stats,
            "manifests": manifests,
        }

        return audit
