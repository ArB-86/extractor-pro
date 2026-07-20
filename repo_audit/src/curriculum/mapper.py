from pathlib import Path
import re


class CurriculumMapper:

    CLASS_PATTERN = re.compile(r"class[_ ]?(\d+)", re.IGNORECASE)

    def map(self, manifest):

        path = Path(manifest["file"])

        text = str(path).lower()

        cls = None

        m = self.CLASS_PATTERN.search(text)

        if m:
            cls = int(m.group(1))

        manifest["class"] = cls

        if "exemplar" in text:
            manifest["book_type"] = "exemplar"

        elif "sample" in text:
            manifest["book_type"] = "sample_paper"

        else:
            manifest["book_type"] = "ncert"

        return manifest
