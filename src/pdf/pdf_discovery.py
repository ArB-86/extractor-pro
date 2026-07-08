from pathlib import Path


class PDFDiscovery:

    def __init__(self, root):

        self.root = Path(root)

    def discover(self):

        return sorted(
            self.root.rglob("*.pdf")
        )
