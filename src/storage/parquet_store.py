from dataclasses import asdict
from pathlib import Path

import pandas as pd


class ParquetStore:

    def write(self, questions, output):

        output = Path(output)

        output.parent.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame(
            [asdict(q) for q in questions]
        )

        df.to_parquet(output, index=False)
