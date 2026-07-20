
from __future__ import annotations


class Report:

    def print(self, results):

        print("="*60)

        print("DATASET BENCHMARK")

        print("="*60)

        for k,v in results.items():

            print(f"{k:30} {v}")

        print("="*60)
