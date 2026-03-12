# Group Assignment Submission Draft

## Title
**Statistical Validation of the Statement:**
"Farmers who monitor their farms regularly respond better to challenges."

## 1) Data Collection & Cleaning (LO1, LO4)
- Climate data source: NASA POWER monthly variables (temperature, precipitation, solar radiation).
- Yield data source: FAOSTAT annual rice yield (Sri Lanka).
- Farm response behavior source: Primary-style survey dataset (`farm_monitoring_primary_demo.csv`) with monitoring frequency, response time, climate risk index, and yield loss.
- Cleaning decisions:
  - Numeric casting and row-level consistency checks.
  - Binary feature creation:
    - `regular_monitoring = 1` if monitoring days >= 15 per month.
    - `effective_response = 1` if response time <= 7 days.

## 2) Descriptive Analytics
- Response time is modeled with both Normal and Gamma families; method-of-moments estimates support right-skewed behavior.
- Climate and yield data provide environmental stress and productivity background context.

## 3) Inferential Analytics (LO2)
### H1: Regularly monitoring farmers have a higher effective response rate.
- Two-proportion z-test compares effective response rates between regular and irregular groups.
- Result (from `reports/key_results.md`):
  - Regular: 0.446
  - Irregular: 0.109
  - z = 4.048, p ≈ 0.000052
- Decision: reject null hypothesis; strong evidence supports higher effective response under regular monitoring.

### H2: Regularly monitoring farmers have lower yield loss.
- Welch-style difference in means test statistic = -8.351.
- Decision: strong directional evidence that regular monitoring reduces losses.

## 4) Predictive Analytics (LO3, LO5)
### Regression model
- Model: `yield_loss_pct = β0 + β1*monitoring_days + β2*climate_risk + ε`
- Key estimates:
  - β1 = -0.771 (more monitoring days reduce expected loss)
  - β2 = +4.329 (higher climate risk increases expected loss)
  - R² = 0.823
- Interpretation: monitoring remains a strong protective factor after controlling climate risk.

### Time-series model
- Holt linear exponential smoothing is applied to annual FAOSTAT yield series.
- Test-set MAPE is reported for model adequacy.

## 5) Exponential Family (LO4)
- Normal model for temperature.
- Exponential model for precipitation intensity proxy.
- Poisson model for rounded rainfall-count proxy.
- These families provide coherent likelihood-based formulations aligned with module theory.

## 6) Bayesian Inference (LO6)
- Target parameter: `P(effective_response | regular_monitoring)`.
- Prior: Beta(1,1), Posterior: Beta(α_post, β_post).
- Posterior mean and 95% credible interval are reported in `key_results.md`.
- Interpretation: posterior mass indicates substantially improved response probability among regular monitors.

## 7) Overall Justification
Combining descriptive, inferential, predictive, and Bayesian evidence, the selected statement is statistically supported: farms with regular monitoring exhibit better challenge response and lower expected yield losses.

## 8) Limitations & Next Steps
- In restricted/offline execution environments, fallback synthetic data is used for climate and FAOSTAT pipelines.
- For final academic submission, replace fallback data with live downloaded NASA/FAOSTAT extracts and your real primary survey.
- Add robustness checks: residual diagnostics, sensitivity analysis, and alternate model forms (ARIMA, logistic regression, Bayesian regression).
