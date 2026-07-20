import pandas as pd
from pathlib import Path


class ParquetExporter:

    def export(self, questions, output_path):

        output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        pd.DataFrame(questions).to_parquet(
            output_path,
            index=False,
        )
