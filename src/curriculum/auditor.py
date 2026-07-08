from src.curriculum.inventory import CurriculumInventory
from src.curriculum.manifest import ManifestBuilder
from src.curriculum.duplicate_detector import DuplicateDetector


class CurriculumAuditor:

    def __init__(self):

        self.inventory = CurriculumInventory()
        self.manifest = ManifestBuilder()
        self.duplicates = DuplicateDetector()

    def audit(self, root):

        pdfs = self.inventory.scan(root)

        manifests = [
            self.manifest.build(pdf)
            for pdf in pdfs
        ]

        duplicates = self.duplicates.detect(manifests)

        return {
            "total_pdfs": len(pdfs),
            "duplicates": duplicates,
            "manifests": manifests,
        }
