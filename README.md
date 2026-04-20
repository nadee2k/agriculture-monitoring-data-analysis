🌾 Agricultural Monitoring & Farm Resilience Analysis (Sri Lanka)
📌 Project Overview

This project investigates how farm monitoring practices influence agricultural productivity and resilience in Sri Lanka. Using real-world secondary datasets from FAOSTAT and NASA POWER, the study applies statistical modelling, hypothesis testing, regression analysis, time series forecasting, and Bayesian inference to evaluate agricultural performance under environmental and management factors.

The goal is to determine whether improved farm monitoring practices are associated with better crop yield and resilience against climate variability.

🎯 Research Statement

Farmers who monitor their farms regularly respond better to agricultural challenges.

This statement is evaluated using:

Descriptive Analytics
Inferential Statistics
Predictive Modelling
📊 Learning Outcomes Coverage
LO	Area
LO1	Probability distributions (Gamma, Normal)
LO2	Hypothesis testing (t-test, significance testing)
LO3	Regression analysis (multiple linear regression)
LO4	Exponential family distributions (Poisson, Exponential)
LO5	Time series forecasting (ARIMA model)
LO6	Bayesian inference (posterior estimation)
📂 Datasets Used
🌱 Agricultural Data (FAOSTAT)
Crop Yield (Rice, Sri Lanka)
Fertilizer Usage (Nitrogen-based inputs)
Irrigation Area
Area Harvested
🌦 Climate Data (NASA POWER)
Annual Rainfall (mm)
Average Temperature (°C)
🔧 Data Engineering

<<<<<<< HEAD
A Monitoring Index was constructed to represent farm management intensity:

Monitoring Index = (Fertilizer Use + Irrigation Area) / Area Harvested
=======
### 1. **FAOSTAT Data** (Production & Inputs)
- `data/raw/FAOSTAT_data_en_4-20-2026.csv` – Annual rice yield (kg/ha), Sri Lanka
- `data/raw/FAOSTAT_data_en_4-20-2026 (1).csv` – Annual fertilizer use (tonnes), Sri Lanka
- `data/raw/FAOSTAT_data_en_4-20-2026 (2).csv` – Irrigated area (1000 ha), Sri Lanka
- `data/raw/FAOSTAT_data_en_4-20-2026 (3).csv` – Rice area harvested (ha), Sri Lanka
- Source: FAOSTAT / FAO statistical data

### 2. **NASA POWER Data** (Climate)
- `data/raw/sri_lanka_weather_2000_2023.csv` – Daily temperature and rainfall for Sri Lanka
- Location: Sri Lanka (approx. 7.8731°N, 80.7718°E)
- Source: NASA POWER or provided weather dataset
>>>>>>> c2a5144 (fixed)

This proxy represents the level of agricultural monitoring and input intensity.

📊 Methodology
1. Descriptive Analytics
Mean, variance, and distribution analysis
Trend analysis of yield and climate variables
Visualization using boxplots and histograms
2. Inferential Statistics
Hypothesis testing (t-test / regression significance)
Evaluation of monitoring impact on yield
3. Regression Analysis

<<<<<<< HEAD
Multiple Linear Regression model:
=======
### Step 1: Data Loading & Exploration
- Load the uploaded FAOSTAT and NASA POWER raw CSV files from `data/raw/`
- Use only real uploaded datasets, with no synthetic or demo data
- Validate data consistency, identify missing values, and ensure annual alignment
>>>>>>> c2a5144 (fixed)

Yield = β0 + β1(Monitoring Index) + β2(Rainfall) + β3(Temperature)
4. Probability Distributions
Gamma distribution for response times
Poisson distribution for event frequency
Exponential distribution for time intervals
5. Time Series Forecasting
ARIMA model applied on yield data
Forecast accuracy evaluated using MAPE
6. Bayesian Analysis
Posterior estimation of monitoring effectiveness
95% credible intervals computed for effect size
📈 Key Results Summary
Monitoring Index shows positive relationship with crop yield
Climate variables significantly affect agricultural output
Forecasting model achieved high predictive accuracy (low MAPE)
Bayesian inference confirms positive but uncertain effect of monitoring
⚠️ Limitations
Some agricultural variables are proxy-based due to lack of direct monitoring data
Model performance is limited by small time-series sample size
Additional variables such as soil quality and pest infestation were not included
🚀 Tools & Technologies
Python (Pandas, NumPy)
Scikit-learn
Statsmodels
Matplotlib / Seaborn
Bayesian modeling tools
📌 Project Structure
data/
 ├── raw/
 ├── processed/

notebooks/
 ├── EDA.ipynb
 ├── Hypothesis_Testing.ipynb
 ├── Regression_Model.ipynb
 ├── Time_Series.ipynb
 ├── Bayesian_Analysis.ipynb

src/
 ├── data_cleaning.py
 ├── feature_engineering.py
 ├── modeling.py

results/
 ├── graphs/
 ├── outputs/
🧠 Key Insight

Agricultural productivity is not solely dependent on environmental conditions but is significantly influenced by farm management intensity, represented through the constructed Monitoring Index.

📌 Conclusion

<<<<<<< HEAD
This project demonstrates how statistical modelling and machine learning techniques can be applied to real-world agricultural systems to understand the relationship between farm monitoring practices and crop productivity. The results support the hypothesis that better monitoring contributes to improved agricultural outcomes under climate variability.
=======
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
│   │   ├── FAOSTAT_data_en_4-20-2026.csv
│   │   ├── FAOSTAT_data_en_4-20-2026 (1).csv
│   │   ├── FAOSTAT_data_en_4-20-2026 (2).csv
│   │   ├── FAOSTAT_data_en_4-20-2026 (3).csv
│   │   └── sri_lanka_weather_2000_2023.csv
│   │
│   └── processed/
│       ├── cleaned_annual.csv          # Aggregated FAOSTAT and weather data
│       └── final_dataset.csv           # Engineered analytical features
│
├── notebooks/
│   ├── 01_data_exploration.ipynb      # EDA: distributions, correlations
│   ├── 02_descriptive_analysis.ipynb  # LO1: Probability distributions
│   ├── 03_hypothesis_testing.ipynb    # LO2: Significance tests
│   ├── 04_regression_model.ipynb      # LO3: Regression modeling
│   ├── 05_time_series.ipynb           # LO5: Holt-Winters forecasting
│   └── 06_bayesian_analysis.ipynb     # LO6: Posterior inference
│
├── src/
│   ├── data_cleaning.py               # Load, validate, clean data
│   ├── feature_engineering.py         # Create monitoring_index, etc.
│   ├── modeling.py                    # Regression, time-series, Bayesian
│   └── evaluation.py                  # Metrics, diagnostics
│
└── results/
    ├── graphs/                        # EDA and model plots
    └── model_outputs/                 # Modeling results and summaries
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
python src/modeling.py
python src/evaluation.py
```

### 3. Run Analysis Notebooks
```bash
jupyter lab notebooks/
```

### 4. View Results
```bash
ls -la data/processed/
cat data/processed/final_dataset.csv | head -n 10
```
---

## Viva Defense

> *"This project was redesigned from synthetic variables into a structured, production-quality data pipeline using verified FAOSTAT and NASA datasets. We replaced generic monitoring metrics with a real monitoring index engineered from fertilizer intensity and irrigation area—both derived directly from official FAO statistics. The pipeline follows a clean data → feature engineering → analysis → evaluation workflow, making every step reproducible. Across six learning outcomes, we provide descriptive, inferential, and predictive evidence that monitoring correlates with yield resilience, even after controlling for climate variables."*

---

## License

Educational use. Data sources: FAOSTAT (public), NASA POWER (public).
>>>>>>> c2a5144 (fixed)
