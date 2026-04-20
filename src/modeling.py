"""Statistical modeling: regression, time-series, and Bayesian inference."""
import csv
import math
import random
from pathlib import Path
from typing import List, Dict, Tuple

PROCESSED_DIR = Path("data/processed")
RESULTS_DIR = Path("results/model_outputs")


def load_engineered_data() -> List[Dict]:
    """Load engineered features from feature_engineering.py output."""
    with (PROCESSED_DIR / "final_dataset.csv").open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def lo1_distributions(data: List[Dict]) -> Dict:
    """LO1: Compute probability distributions for response time and rainfall."""
    response_times = []
    precips = []
    
    for row in data:
        try:
            if 'response_time_days' in row and row['response_time_days']:
                response_times.append(float(row['response_time_days']))
            if 'precip_annual_mean' in row and row['precip_annual_mean']:
                precips.append(float(row['precip_annual_mean']))
        except (ValueError, TypeError):
            continue
    
    # Normal distribution for response time
    if response_times:
        mean_rt = sum(response_times) / len(response_times)
        var_rt = sum((x - mean_rt) ** 2 for x in response_times) / max(1, len(response_times) - 1)
        sd_rt = math.sqrt(var_rt)
    else:
        mean_rt = sd_rt = 0
    
    # Gamma distribution (method of moments)
    if response_times and sd_rt > 0:
        k_gamma = (mean_rt / sd_rt) ** 2
        theta_gamma = (sd_rt ** 2) / mean_rt
    else:
        k_gamma = theta_gamma = 0
    
    return {
        "normal_mean_response_time": round(mean_rt, 6),
        "normal_sd_response_time": round(sd_rt, 6),
        "gamma_shape_estimate": round(k_gamma, 6),
        "gamma_scale_estimate": round(theta_gamma, 6),
    }


def lo2_hypothesis_tests(data: List[Dict]) -> Dict:
    """LO2: Hypothesis testing comparing regular vs irregular monitoring groups."""
    regular = [float(row['yield_loss_pct']) for row in data if row.get('regular_monitoring') == '1' and row.get('yield_loss_pct')]
    irregular = [float(row['yield_loss_pct']) for row in data if row.get('regular_monitoring') == '0' and row.get('yield_loss_pct')]
    
    if not regular or not irregular:
        return {"error": "Insufficient data for hypothesis testing"}
    
    mean_reg = sum(regular) / len(regular)
    mean_irreg = sum(irregular) / len(irregular)
    
    # Variance
    var_reg = sum((x - mean_reg) ** 2 for x in regular) / max(1, len(regular) - 1)
    var_irreg = sum((x - mean_irreg) ** 2 for x in irregular) / max(1, len(irregular) - 1)
    
    # Welch t-test
    se = math.sqrt(var_reg / len(regular) + var_irreg / len(irregular)) if var_reg > 0 or var_irreg > 0 else 1e-9
    t_stat = (mean_reg - mean_irreg) / se if se > 0 else 0
    
    # Proportion test (effective response)
    reg_effect = [int(row.get('effective_response', 0)) for row in data if row.get('regular_monitoring') == '1']
    irreg_effect = [int(row.get('effective_response', 0)) for row in data if row.get('regular_monitoring') == '0']
    
    p_reg = sum(reg_effect) / len(reg_effect) if reg_effect else 0
    p_irreg = sum(irreg_effect) / len(irreg_effect) if irreg_effect else 0
    
    return {
        "regular_mean_yield_loss": round(mean_reg, 4),
        "irregular_mean_yield_loss": round(mean_irreg, 4),
        "welch_t_statistic": round(t_stat, 6),
        "regular_effective_rate": round(p_reg, 4),
        "irregular_effective_rate": round(p_irreg, 4),
    }


def lo3_regression(data: List[Dict]) -> Dict:
    """LO3: Regression model: yield_loss ~ monitoring_index + climate_risk."""
    x1_vals = []  # monitoring_index
    x2_vals = []  # climate_risk_index
    y_vals = []   # yield_loss_pct
    
    for row in data:
        try:
            x1 = float(row.get('monitoring_index', 0))
            x2 = float(row.get('climate_risk_index', 0))
            y = float(row.get('yield_loss_pct', 0))
            x1_vals.append(x1)
            x2_vals.append(x2)
            y_vals.append(y)
        except (ValueError, TypeError):
            continue
    
    if len(x1_vals) < 3:
        return {"error": "Insufficient data for regression"}
    
    n = len(y_vals)
    sum_x1 = sum(x1_vals)
    sum_x2 = sum(x2_vals)
    sum_y = sum(y_vals)
    sum_x1x1 = sum(v ** 2 for v in x1_vals)
    sum_x2x2 = sum(v ** 2 for v in x2_vals)
    sum_x1x2 = sum(a * b for a, b in zip(x1_vals, x2_vals))
    sum_x1y = sum(a * b for a, b in zip(x1_vals, y_vals))
    sum_x2y = sum(a * b for a, b in zip(x2_vals, y_vals))
    
    # Normal equations: solve 3x3 system
    det = (n * (sum_x1x1 * sum_x2x2 - sum_x1x2 ** 2) - 
           sum_x1 * (sum_x1 * sum_x2x2 - sum_x1x2 * sum_x2) + 
           sum_x2 * (sum_x1 * sum_x1x2 - sum_x1x1 * sum_x2))
    
    if abs(det) < 1e-10:
        return {"error": "Singular matrix in regression"}
    
    # Solve for intercept, beta1, beta2
    b0 = ((sum_y * (sum_x1x1 * sum_x2x2 - sum_x1x2 ** 2) - 
           sum_x1y * (sum_x1 * sum_x2x2 - sum_x1x2 * sum_x2) + 
           sum_x2y * (sum_x1 * sum_x1x2 - sum_x1x1 * sum_x2)) / det)
    
    b1 = ((n * (sum_x1y * sum_x2x2 - sum_x2y * sum_x1x2) - 
           sum_x1 * (sum_y * sum_x2x2 - sum_x2y * sum_x2) + 
           sum_x2 * (sum_y * sum_x1x2 - sum_x1y * sum_x2)) / det)
    
    b2 = ((n * (sum_x1x1 * sum_x2y - sum_x1y * sum_x1x2) - 
           sum_x1 * (sum_x1 * sum_x2y - sum_x1y * sum_x2) + 
           sum_y * (sum_x1 * sum_x1x2 - sum_x1x1 * sum_x2)) / det)
    
    # Predictions and R²
    preds = [b0 + b1 * a + b2 * c for a, c in zip(x1_vals, x2_vals)]
    y_mean = sum_y / n
    ss_tot = sum((y - y_mean) ** 2 for y in y_vals)
    ss_res = sum((y - p) ** 2 for y, p in zip(y_vals, preds))
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
    mae = sum(abs(y - p) for y, p in zip(y_vals, preds)) / n
    
    return {
        "intercept": round(b0, 6),
        "beta_monitoring_index": round(b1, 6),
        "beta_climate_risk": round(b2, 6),
        "r_squared": round(r2, 6),
        "mae": round(mae, 6),
    }


def lo5_time_series(data: List[Dict]) -> Dict:
    """LO5: Time series forecasting on yield with Holt-Winters smoothing."""
    yields = []
    
    for row in sorted(data, key=lambda x: int(x.get('year', 0))):
        try:
            y = float(row.get('yield_kg_ha', 0))
            if y > 0:
                yields.append(y)
        except (ValueError, TypeError):
            continue
    
    if len(yields) < 7:
        return {"error": "Insufficient data for time series"}
    
    train = yields[:-5]
    test = yields[-5:]
    
    # Holt-Winters: exponential smoothing
    alpha = 0.35
    level = train[0]
    trend = train[1] - train[0] if len(train) > 1 else 0
    
    for t in range(1, len(train)):
        prev_level = level
        level = alpha * train[t] + (1 - alpha) * (level + trend)
        trend = alpha * (level - prev_level) + (1 - alpha) * trend
    
    # Forecast
    forecasts = [level + (i + 1) * trend for i in range(len(test))]
    
    # MAPE
    mape = 100 * sum(abs((a - f) / a) for a, f in zip(test, forecasts)) / len(test) if test else 0
    
    return {
        "train_size": len(train),
        "test_size": len(test),
        "mape_percent": round(mape, 4),
        "last_forecast_kg_ha": round(forecasts[-1], 2) if forecasts else 0,
    }


def lo6_bayesian(data: List[Dict]) -> Dict:
    """LO6: Bayesian inference on monitoring effect probability."""
    reg_data = [row for row in data if row.get('regular_monitoring') == '1']
    if not reg_data:
        return {"error": "No regular monitoring data"}
    
    successes = sum(int(row.get('effective_response', 0)) for row in reg_data)
    n = len(reg_data)
    
    # Beta-Binomial conjugate prior
    a_prior, b_prior = 1, 1
    a_post = a_prior + successes
    b_post = b_prior + (n - successes)
    
    # Posterior mean and credible interval (simulation)
    random.seed(42)
    samples = [random.betavariate(a_post, b_post) for _ in range(10000)]
    samples.sort()
    
    ci_low = samples[int(0.025 * len(samples))]
    ci_high = samples[int(0.975 * len(samples))]
    
    return {
        "posterior_alpha": a_post,
        "posterior_beta": b_post,
        "posterior_mean": round(a_post / (a_post + b_post), 6),
        "credible_interval_95_low": round(ci_low, 6),
        "credible_interval_95_high": round(ci_high, 6),
    }


def save_results(results: Dict) -> None:
    """Save results to CSV."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    with (RESULTS_DIR / "modeling_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for section, metrics in results.items():
            for k, v in metrics.items():
                writer.writerow([f"{section}.{k}", v])
    
    print(f"Saved modeling results: {RESULTS_DIR / 'modeling_results.csv'}")


def main() -> None:
    """Run all modeling tasks."""
    print("Loading engineered data...")
    data = load_engineered_data()
    
    print("Running LO1: Distributions...")
    lo1 = lo1_distributions(data)
    print(f"  {lo1}")
    
    print("Running LO2: Hypothesis Testing...")
    lo2 = lo2_hypothesis_tests(data)
    print(f"  {lo2}")
    
    print("Running LO3: Regression...")
    lo3 = lo3_regression(data)
    print(f"  {lo3}")
    
    print("Running LO5: Time Series...")
    lo5 = lo5_time_series(data)
    print(f"  {lo5}")
    
    print("Running LO6: Bayesian...")
    lo6 = lo6_bayesian(data)
    print(f"  {lo6}")
    
    results = {
        "LO1_distributions": lo1,
        "LO2_hypothesis_testing": lo2,
        "LO3_regression": lo3,
        "LO5_time_series": lo5,
        "LO6_bayesian": lo6,
    }
    
    save_results(results)
    print("\nModeling complete.")


if __name__ == "__main__":
    main()
