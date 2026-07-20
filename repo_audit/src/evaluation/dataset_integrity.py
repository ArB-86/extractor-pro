from __future__ import annotations

from hashlib import sha256


class DatasetIntegrity:

    def duplicates(

        self,

        rows,

    ):

        seen={}

        dup=[]

        for r in rows:

            h=sha256(

                " ".join(

                    r["question_text"].lower().split()

                ).encode()

            ).hexdigest()

            if h in seen:

                dup.append(r)

            else:

                seen[h]=1

        return dup

    def statistics(

        self,

        rows,

    ):

        return {

            "questions":len(rows),

            "duplicates":len(

                self.duplicates(rows)

            ),

        }
