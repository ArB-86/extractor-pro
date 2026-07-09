from __future__ import annotations

from pathlib import Path
from typing import Any
import html


class HTMLEvaluationReport:

    def save(
        self,
        report: dict[str, Any],
        output_path: str | Path,
    ) -> Path:

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        rows = []

        for k, v in report.items():

            if isinstance(v, dict):

                rows.append(
                    f"<h2>{html.escape(k)}</h2>"
                )

                rows.append("<table>")

                for kk, vv in v.items():

                    rows.append(
                        f"<tr><td>{html.escape(str(kk))}</td><td>{html.escape(str(vv))}</td></tr>"
                    )

                rows.append("</table>")

            else:

                rows.append(
                    f"<p><b>{html.escape(k)}</b>: {html.escape(str(v))}</p>"
                )

        page = f"""
<html>
<head>
<meta charset="utf-8">
<title>Evaluation Report</title>
<style>
body {{
font-family: Arial;
margin:40px;
}}
table {{
border-collapse:collapse;
}}
td {{
border:1px solid #999;
padding:6px 10px;
}}
</style>
</head>
<body>

<h1>Extractor-Pro Evaluation Report</h1>

{''.join(rows)}

</body>
</html>
"""

        output_path.write_text(
            page,
            encoding="utf-8",
        )

        return output_path
