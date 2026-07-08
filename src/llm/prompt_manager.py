from pathlib import Path


class PromptManager:

    def __init__(self, root="src/prompts"):
        self.root = Path(root)

    def load(self, relative_path: str) -> str:
        path = self.root / relative_path
        return path.read_text(encoding="utf-8")
