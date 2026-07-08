class DuplicateDetector:

    def detect(self, manifests):

        seen = {}

        duplicates = []

        for m in manifests:

            key = m["sha256"]

            if key in seen:
                duplicates.append(m)

            else:
                seen[key] = m

        return duplicates
