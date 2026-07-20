from typing import List
import re

from src.schema.region import Region


class RegionMerger:

    @staticmethod
    def merge(regions: List[Region]) -> List[Region]:

        if not regions:
            return []

        merged = []
        current = regions[0]

        for nxt in regions[1:]:

            same_label = (
                current.label == nxt.label
            )

            mergeable = current.label in {
                "plain_text",
                "isolate_formula",
            }

            same_page = current.page == nxt.page

            close = (
                abs(nxt.y1 - current.y2) < 40
                or abs(nxt.y1 - current.y1) < 40
            )

            starts_new_question = False

            if nxt.text:
                starts_new_question = bool(
                    re.match(
                        r'^\s*(?:Q\.?\s*)?\d+[.)\]。．﹒․]\s+',
                        nxt.text,
                        re.I,
                    )
                )

            # ---- DEBUG: Print merge decision details ----
            print("=" * 100)
            print("MERGE DECISION")
            print(
                f"page={current.page}",
                f"same_label={same_label}",
                f"mergeable={mergeable}",
                f"same_page={same_page}",
                f"close={close}",
                f"starts_new_question={starts_new_question}",
            )
            print("CURRENT:", repr((current.text or "")[:120]))
            print("NEXT   :", repr((nxt.text or "")[:120]))
            print("=" * 100)

            if (
                same_label
                and mergeable
                and same_page
                and close
                and not starts_new_question
            ):

                if current.text and nxt.text:
                    current.text += "\n" + nxt.text
                elif nxt.text:
                    current.text = nxt.text

                current.x1 = min(current.x1, nxt.x1)
                current.y1 = min(current.y1, nxt.y1)
                current.x2 = max(current.x2, nxt.x2)
                current.y2 = max(current.y2, nxt.y2)

                continue

            merged.append(current)
            current = nxt

        merged.append(current)

        return merged
