from src.curriculum.inventory import CurriculumInventory
from src.curriculum.manifest import ManifestBuilder
from src.curriculum.duplicate_detector import DuplicateDetector
from src.curriculum.mapper import CurriculumMapper
from src.curriculum.statistics import CurriculumStatistics
from src.curriculum.report import CurriculumReport
from src.curriculum.checks import CurriculumChecks
from src.curriculum.chapter_mapper import ChapterMapper
from src.curriculum.book_index import BookIndex
from src.curriculum.coverage import CurriculumCoverage  # new import


class CurriculumAuditor:

    def __init__(self):

        self.inventory = CurriculumInventory()
        self.manifest = ManifestBuilder()
        self.duplicates = DuplicateDetector()
        self.mapper = CurriculumMapper()
        self.statistics = CurriculumStatistics()
        self.report = CurriculumReport()
        self.checks = CurriculumChecks()
        self.chapter_mapper = ChapterMapper()
        self.book_index = BookIndex()
        self.coverage = CurriculumCoverage()  # new coverage instance

    def audit(self, root):

        pdfs = self.inventory.scan(root)

        manifests = [
            self.chapter_mapper.map(
                self.mapper.map(
                    self.manifest.build(pdf)
                )
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

        # Add validation errors to the audit
        audit["errors"] = self.checks.validate(manifests)

        # Build book index from manifests
        audit["book_index"] = self.book_index.build(manifests)

        # Build curriculum coverage analysis
        audit["coverage"] = self.coverage.build(manifests)

        return audit
