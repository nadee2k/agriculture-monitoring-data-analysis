# Agricultural Monitoring and Farm Resilience Analysis (Sri Lanka)

## Problem Statement

This project investigates the critical hypothesis:

> **"Farms with regular irrigation and fertilizer management show better yield outcomes despite climate challenges."**

### Context
- Sri Lankan agriculture faces significant climate variability (rainfall, temperature fluctuations)
- Farm management intensity (monitoring frequency, input application) affects resilience
- Understanding the monitoring-yield relationship informs policy on farm resilience strategies

---

## Dataset Sources

### 1. **FAOSTAT Data** (Production & Inputs)
- **Rice Yield**: Annual yield (kg/ha) for Sri Lanka, 2000-2024
- **Fertilizer Use**: Annual nitrogen, phosphate, potash application (tonnes), 2020-2023
- **Irrigation Area**: Land area equipped for irrigation (1000 ha), 2020-2023
- Source: FAO Statistical Database (FAOSTAT)

### 2. **NASA POWER Data** (Climate)
- **Temperature**: Monthly mean temperature (°C), 2000-2024
- **Precipitation**: Monthly total rainfall (mm/day), 2000-2024
- **Solar Radiation**: Monthly solar irradiance (MJ/m²/day), 2000-2024
- Location: Sri Lanka (7.8731°N, 80.7718°E)
- Source: NASA POWER API (Agro-Climatic Data)

---

## Methodology

### Step 1: Data Loading & Exploration
- Load FAOSTAT crop, fertilizer, irrigation data
- Load NASA POWER climate data
- Validate data consistency, identify missing values

### Step 2: Data Cleaning
- Handle missing values (forward-fill, interpolation)
- Standardize units (e.g., fertilizer tonnes → kg/ha)
- Align temporal dimensions (annual vs. monthly aggregation)

### Step 3: Feature Engineering
**Core Feature: Monitoring Index**
```
monitoring_index = (fertilizer_intensity + irrigation_ratio) / 2

where:
  fertilizer_intensity = (total_fertilizer_use) / area_harvested
  irrigation_ratio = irrigation_area / area_harvested
```

**Climate Risk Index**
```
climate_risk = normalize(mean_temp_anomaly + precip_coefficient)
```

**Response Quality**
```
effective_response = 1 if yield_growth > expected_given_climate else 0
```

### Step 4: Exploratory Data Analysis (EDA)
- Distributions of monitoring index, yield, climate variables
- Correlation heatmaps
- Time-series trends

### Step 5: Hypothesis Testing
- **H1**: Farms with high monitoring index have lower yield variance
- **H2**: Monitoring effect persists after climate control

### Step 6: Regression Modeling
```
yield ~ monitoring_index + temperature + rainfall + year
```
- Ordinary Least Squares (OLS) estimation
- Model diagnostics (R², residuals, collinearity)

### Step 7: Time Series Forecasting
- Holt-Winters exponential smoothing on annual yield
- MAPE evaluation on held-out test set

### Step 8: Bayesian Inference
- Prior: Beta(1, 1) for P(monitoring benefit)
- Likelihood: observed success rate
- Posterior: credible interval for effect size

---

## Repository Structure

```
agriculture-monitoring-data-analysis/
│
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
│
├── data/
│   ├── raw/
│   │   ├── faostat_sri_lanka_rice_yield.csv      # Annual yield
│   │   ├── Crop_data.csv                         # FAOSTAT crop data
│   │   ├── Fertilizer_data.csv                   # Fertilizer use
│   │   ├── Irrigation_data.csv                   # Irrigation area
│   │   ├── nasa_power_sri_lanka_monthly.csv      # Climate data
│   │   └── Pesticide_data.csv                    # Pesticide use
│   │
│   └── processed/
│       ├── final_dataset.csv                      # Engineered features
│       └── analysis_results.csv                   # LO1-LO6 metrics
│
├── notebooks/
│   ├── 01_data_exploration.ipynb      # EDA: distributions, correlations
│   ├── 02_descriptive_analysis.ipynb  # LO1: Probability distributions
│   ├── 03_hypothesis_testing.ipynb    # LO2: Significance tests
│   ├── 04_regression_model.ipynb      # LO3: Regression modeling
│   ├── 05_time_series.ipynb           # LO5: ARIMA forecasting
│   └── 06_bayesian_analysis.ipynb     # LO6: Posterior inference
│
├── src/
│   ├── data_cleaning.py               # Load, validate, clean data
│   ├── feature_engineering.py         # Create monitoring_index, etc.
│   ├── modeling.py                    # Regression, time-series, Bayesian
│   └── evaluation.py                  # Metrics, diagnostics
│
└── results/
    ├── graphs/                        # EDA plots, model diagnostics
    └── model_outputs/                 # Regression summaries, forecasts
```

---

## Key Features

### 1. **Monitoring Index (Real Feature Engineering)**
Replaces synthetic "monitoring_days" with:
```python
monitoring_index = (fertilizer_use_kg_ha + irrigation_area_ratio) / 2
```
Derived directly from FAOSTAT agricultural inputs.

### 2. **Climate-Controlled Analysis**
- Temperature and rainfall included as covariates
- Isolates monitoring effect from climate confounding

### 3. **Multi-Faceted Evidence**
- Descriptive: Yield distribution by monitoring level
- Inferential: Hypothesis tests with p-values
- Predictive: Regression R² and time-series MAPE
- Bayesian: Credible interval for monitoring benefit

---

## Results Summary

### Key Findings
| Learning Outcome | Metric | Interpretation |
|---|---|---|
| **LO1** | Response Time Distribution | Normal fit with variability |
| **LO2** | Hypothesis Test | Monitoring effect on yield |
| **LO3** | Regression Coefficient | Positive yield impact |
| **LO4** | Exponential Family | Climate data fit |
| **LO5** | Time Series MAPE | Forecast accuracy ~7% |
| **LO6** | Posterior Credible Interval | Effect size uncertainty |

### Conclusion
Monitoring has a **positive yield effect**, though with modest explanatory power due to limited sample size. **Recommend extending dataset to 10+ years and multiple regions for stronger inference.**

---

## Technologies & Libraries

| Purpose | Library |
|---|---|
| Data manipulation | Pandas |
| Numerical computing | NumPy |
| Visualization | Matplotlib, Seaborn |
| Statistical modeling | StatsModels, Scikit-learn |
| Notebooks | Jupyter |

---

## How to Run

### 1. Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Data Pipeline
```bash
python src/data_cleaning.py
python src/feature_engineering.py
```

### 3. Run Analysis Notebooks
```bash
jupyter lab notebooks/
```

### 4. View Results
```bash
ls -la results/graphs/
cat data/processed/analysis_results.csv
```

---

## Viva Defense

> *"This project was redesigned from synthetic variables into a structured, production-quality data pipeline using verified FAOSTAT and NASA datasets. We replaced generic monitoring metrics with a real monitoring index engineered from fertilizer intensity and irrigation area—both derived directly from official FAO statistics. The pipeline follows a clean data → feature engineering → analysis → evaluation workflow, making every step reproducible. Across six learning outcomes, we provide descriptive, inferential, and predictive evidence that monitoring correlates with yield resilience, even after controlling for climate variables."*

---

## License

Educational use. Data sources: FAOSTAT (public), NASA POWER (public).