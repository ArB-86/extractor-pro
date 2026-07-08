from dataclasses import asdict
from pathlib import Path

import pandas as pd
import sqlite3


class SQLiteStore:

    def write(self, questions, output):

        output = Path(output)

        output.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(output)

        pd.DataFrame(
            [asdict(q) for q in questions]
        ).to_sql(
            "questions",
            conn,
            if_exists="replace",
            index=False,
        )

        conn.close()
