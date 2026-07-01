#!/bin/bash
# batch_run.sh - Full Corpus Extraction Pipeline
# Usage: ./batch_run.sh /path/to/raw_pdfs /path/to/output_json

INPUT_DIR=$1
OUTPUT_DIR=$2
mkdir -p "$OUTPUT_DIR"

echo "Starting full batch extraction..."

# Find all PDFs recursively
find "$INPUT_DIR" -name "*.pdf" | while read -r pdf; do
    echo "----------------------------------------------------"
    echo "Processing: $(basename "$pdf")"
    
    # Run the debug_pipeline to output the JSON
    # This assumes debug_pipeline writes to output/json/ as configured
    python scripts/debug_pipeline.py --pdf "$pdf"
    
    # Consolidate output if multiple JSONs were created
    find output/json/ -name "*.json" -exec mv {} "$OUTPUT_DIR/" \; 2>/dev/null
done

echo "Batch processing complete. Master dataset stored in $OUTPUT_DIR"
