#!/usr/bin/env bash
set -euo pipefail

python src/data_cleaning.py
python src/feature_engineering.py
python src/modeling.py
python src/evaluation.py

echo
echo "Done. Generated files:"
echo "- data/processed/cleaned_annual.csv"
echo "- data/processed/final_dataset.csv"
echo "- results/model_outputs/modeling_results.csv"
echo "- results/graphs/"
