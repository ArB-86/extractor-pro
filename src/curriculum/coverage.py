from collections import defaultdict


class CurriculumCoverage:

    def build(self, manifests):

        coverage = defaultdict(set)

        for m in manifests:

            cls = m.get("class")
            chapter = m.get("chapter")

            if cls is None or chapter is None:
                continue

            coverage[cls].add(chapter)

        return {
            cls: sorted(chapters)
            for cls, chapters in coverage.items()
        }
