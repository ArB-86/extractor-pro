from pathlib import Path


class CurriculumInventory:

    def scan(self, root):

        return sorted(
            Path(root).rglob("*.pdf")
        )
