import sqlite3
from pathlib import Path
import pandas as pd


class SQLiteExporter:

    def export(self, questions, output_path):

        output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(output_path)

        pd.DataFrame(questions).to_sql(
            "questions",
            conn,
            if_exists="replace",
            index=False,
        )

        conn.close()
