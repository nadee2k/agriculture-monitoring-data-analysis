#!/usr/bin/env bash
set -euo pipefail

python src/data_collection.py
python src/analysis.py

echo
echo "Done. Generated files:"
echo "- data/raw/"
echo "- data/processed/analysis_results.csv"
echo "- reports/key_results.md"
echo "- reports/assignment_submission.md"

echo
echo "Top 10 lines of analysis results:"
head -n 10 data/processed/analysis_results.csv
