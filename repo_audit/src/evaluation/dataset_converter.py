from __future__ import annotations

import json
import csv
from pathlib import Path


class DatasetConverter:

    def json_to_jsonl(

        self,

        src,

        dst,

    ):

        rows=json.loads(

            Path(src).read_text(

                encoding="utf-8"

            )

        )

        with open(

            dst,

            "w",

            encoding="utf-8",

        ) as f:

            for r in rows:

                f.write(

                    json.dumps(

                        r,

                        ensure_ascii=False,

                    )

                )

                f.write("\\n")


    def csv_to_json(

        self,

        src,

        dst,

    ):

        rows=[]

        with open(

            src,

            newline="",

            encoding="utf-8",

        ) as f:

            for row in csv.DictReader(f):

                rows.append(row)

        Path(dst).write_text(

            json.dumps(

                rows,

                indent=2,

                ensure_ascii=False,

            ),

            encoding="utf-8",

        )
