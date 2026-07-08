from hashlib import sha256
from pathlib import Path


class ManifestBuilder:

    def build(self, pdf):

        pdf = Path(pdf)

        digest = sha256(
            pdf.read_bytes()
        ).hexdigest()

        return {
            "file": str(pdf),
            "name": pdf.name,
            "sha256": digest,
            "size": pdf.stat().st_size,
        }
