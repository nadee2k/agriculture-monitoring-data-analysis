# 🌾 Agricultural Monitoring & Yield Loss Analysis (Sri Lanka)

A data-driven statistical analysis of how **monitoring practices and climate risk influence rice yield loss** in Sri Lanka using FAOSTAT and NASA POWER datasets.

---

## 📌 Project Overview

This project investigates a key question:

> **Can agricultural monitoring systems reduce yield loss under climate variability?**

Using 24 years (2000–2023) of real-world data, the analysis integrates:

* Agricultural production indicators (FAOSTAT)
* Climate variables (NASA POWER)
* Statistical modeling (regression, hypothesis testing, forecasting, Bayesian inference)

---

## 📊 Dataset Description

The project uses **real, country-level datasets**:

### 🌱 Agricultural Data (FAOSTAT)

* Rice Yield (kg/ha)
* Fertilizer Use
* Irrigated Area
* Harvested Area

### 🌦️ Climate Data (NASA POWER)

* Temperature
* Precipitation

### 🔧 Engineered Features

* **Monitoring Index**
  Combines fertilizer intensity and irrigation ratio
* **Climate Risk Index**
  Derived from temperature and rainfall anomalies
* **Yield Loss (%)**
  Relative deviation from expected yield

Final merged dataset:
📁 `data/processed/final_dataset.csv`

---

## 🎯 Objectives

* Quantify the impact of monitoring practices on yield loss
* Evaluate climate risk influence on agricultural outcomes
* Apply statistical methods aligned with course learning outcomes
* Generate interpretable and reproducible insights

---

## 🧠 Methodology (Aligned with Learning Outcomes)

### 🔹 LO1 — Distribution Analysis

* Modeled response time using:

  * **Gamma Distribution**
  * Normal approximation
* Mean ≈ 9.09 days, SD ≈ 3.50

📌 Insight: Agricultural response times exhibit **right-skewed behavior**, typical of real-world intervention delays.

---

### 🔹 LO2 — Hypothesis Testing

* Compared:

  * **Regular Monitoring vs Irregular Monitoring**

| Group     | Mean Yield Loss |
| --------- | --------------- |
| Regular   | 3.72%           |
| Irregular | 4.64%           |

* Effective response rate:

  * Regular: 83.3%
  * Irregular: 0%

* Welch’s t-test:

  * t ≈ -0.37, p > 0.05

📌 Insight:
Monitoring shows **clear practical improvement**, but statistical significance is limited due to small sample size.

---

### 🔹 LO3 — Regression Analysis

Model: OLS Regression

[
YieldLoss = \beta_0 + \beta_1(Monitoring) + \beta_2(ClimateRisk) + \epsilon
]

| Variable         | Coefficient | Interpretation       |
| ---------------- | ----------- | -------------------- |
| Monitoring Index | -0.95       | Reduces yield loss   |
| Climate Risk     | +2.06       | Increases yield loss |

* R² ≈ 0.021
* MAE ≈ 4.40

📌 Insight:
Model confirms expected relationships, but **low explanatory power indicates missing variables**.

---

### 🔹 LO5 — Time Series Forecasting

* Model: Holt-Winters Exponential Smoothing

* Train: 19 years | Test: 5 years

* MAPE ≈ 20.78%

* Forecast (2024):

  * ≈ **3313 kg/ha**

📌 Insight:
Model achieves **moderate forecasting accuracy** for annual agricultural data.

---

### 🔹 LO6 — Bayesian Inference

* Model: Beta-Binomial

| Metric                | Value        |
| --------------------- | ------------ |
| Posterior Mean        | 0.786        |
| 95% Credible Interval | [0.55, 0.95] |

📌 Insight:
There is strong probabilistic evidence that **monitoring interventions are effective**.

---

## 📈 Key Findings

* Monitoring reduces yield loss **in practice**, though statistical significance is limited
* Climate risk consistently **increases yield loss**
* Regression confirms direction of effects but lacks explanatory strength
* Forecasting provides **usable medium-term predictions**
* Bayesian analysis supports **high probability of monitoring effectiveness**

---

## ⚠️ Limitations

* Small sample size (annual data only)
* Missing variables (soil quality, policy changes, pest outbreaks)
* Low regression R²
* Aggregated national-level data reduces variability

---

## 🚀 Future Improvements

* Include district-level or seasonal data
* Add soil, pest, and economic variables
* Improve regression with feature engineering
* Apply advanced models (Random Forest, XGBoost)
* Expand time series with monthly resolution

---

## 📁 Project Structure

```
agriculture-monitoring-data-analysis/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
├── src/
├── results/
│
├── final_dataset.csv
├── README.md
└── requirements.txt
```

---

## 🛠️ Tech Stack

* Python (Pandas, NumPy)
* Statsmodels / Scipy
* Matplotlib / Seaborn
* Time Series Models
* Bayesian Statistics

---

## 📌 Conclusion

This project demonstrates that:

> **Agricultural monitoring systems contribute to improved resilience against yield loss, even under climate stress.**

While statistical strength is moderate, **consistent directional evidence across multiple methods** supports the value of monitoring systems in Sri Lanka’s rice sector.

---

## ⭐ If you found this useful

Consider giving this repo a star ⭐ and sharing feedback!
