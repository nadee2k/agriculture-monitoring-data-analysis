# Agriculture Monitoring Data Analysis (NASA + FAOSTAT)

This project validates the statement:

> **"Farms with regular irrigation and fertilizer management show better yield outcomes despite climate challenges."**

using secondary climate/yield data and processed farm management data from crop, fertilizer, pesticide, and irrigation records.
> Note: Generated files under `data/raw/`, `data/processed/`, and `reports/key_results.md` are not versioned to avoid merge conflicts. Recreate them with `./run_pipeline.sh`.


## Datasets used
- **NASA POWER** monthly climate variables for Sri Lanka (temperature, precipitation, solar radiation).
- **FAOSTAT** annual crop yield series (Rice paddy, Sri Lanka).
- **Secondary farm management data** processed from crop production, fertilizer applications, pesticide applications, and irrigation records to derive monitoring frequency and response metrics.

## Learning outcomes mapping
- **LO1**: Discrete/continuous distributions for response-time and rainfall variables.
- **LO2**: Hypothesis tests comparing regular vs irregular monitoring groups.
- **LO3**: Regression model for yield loss vs monitoring behavior and climate risk.
- **LO4**: Exponential-family parameter estimation (Normal, Poisson, Exponential).
- **LO5**: Time-series forecasting on FAOSTAT yield.
- **LO6**: Bayesian posterior inference for effective response probability.

## Project structure
- `src/data_collection.py` – downloads NASA/FAO data + processes secondary farm management data.
- `src/analysis.py` – computes LO1–LO6 analyses and writes outputs.
- `data/raw/` – raw data files (including your crop_data.csv, fertilizer_data.csv, etc.).
- `data/processed/analysis_results.csv` – combined metrics.
- `reports/key_results.md` – report-ready result summary.

## Run instructions
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/data_collection.py
python src/analysis.py
```

## Suggested presentation flow
1. Problem statement & selected hypothesis.
2. Data sources, variable dictionary, and cleaning logic.
3. Descriptive analytics (distribution plots + summary tables).
4. Inferential analytics (hypothesis tests, confidence/credible intervals).
5. Predictive analytics (regression + time-series forecast).
6. Decision justification and limitations.

## Notes
- Country/item codes can be changed in `src/data_collection.py` for different crops/countries.
- **Model Enhancements**: To address limitations regarding soil quality and pest management, the simulation in `src/data_collection.py` now extracts real Sri Lankan national averages from the provided FAOSTAT data (`Crop_data.csv`, `Fertilizer_data.csv`, `Pesticide_data.csv`). It uses these true macro-level baselines to generate realistic `soil_quality_index` and `pest_management_score` distributions for each farm, which are then modeled in the LO3 multiple regression.
- Replace `data/raw/farm_monitoring_primary_demo.csv` with your real primary survey data for final production use.

## How to get output (quick)
Run everything with one command:

```bash
./run_pipeline.sh
```

Or run step-by-step:

```bash
python src/data_collection.py
python src/analysis.py
```

Generated outputs:
- `data/raw/nasa_power_sri_lanka_monthly.csv`
- `data/raw/faostat_sri_lanka_rice_yield.csv`
- `data/raw/farm_monitoring_primary_demo.csv`
- `data/raw/data_sources.txt`
- `data/processed/analysis_results.csv`
- `reports/key_results.md`

To view outputs quickly:

```bash
cat data/raw/data_sources.txt
head -n 20 data/processed/analysis_results.csv
cat reports/key_results.md
```
\