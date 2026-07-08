import re
from pathlib import Path


class ChapterMapper:

    CHAPTER = re.compile(r"chapter[_ -]?(\d+)", re.IGNORECASE)

    def map(self, manifest):

        path = Path(manifest["file"])

        m = self.CHAPTER.search(str(path))

        manifest["chapter"] = (
            int(m.group(1))
            if m else None
        )

        return manifest
