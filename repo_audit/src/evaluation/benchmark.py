
from __future__ import annotations

import time


class BenchmarkRunner:

    def run(self, fn, *args, **kwargs):

        start = time.perf_counter()

        result = fn(*args, **kwargs)

        elapsed = time.perf_counter() - start

        return {
            "result": result,
            "runtime_seconds": round(elapsed, 4),
        }
