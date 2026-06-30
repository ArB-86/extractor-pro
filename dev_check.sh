#!/bin/bash
set -e

python -m compileall pipeline parsers
pytest tests/unit -q
python scripts/benchmark_splitter.py
