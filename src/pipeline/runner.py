
from dataclasses import dataclass

from src.extractor.extractor import Extractor


@dataclass(slots=True)
class RunConfig:

    pdf: str

    output: str

    gold: str | None = None


class ProductionRunner:

    def __init__(self):

        self.extractor = Extractor()

    def run(
        self,
        config: RunConfig,
    ):

        return self.extractor.extract(
            pdf_path=config.pdf,
            output_dir=config.output,
            gold_path=config.gold,
        )
