"""Statistical analysis pipeline covering LO1-LO6 with standard library only."""
from __future__ import annotations

import csv
import math
import random
import statistics
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
REPORT_DIR = Path("reports")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def variance(xs: list[float]) -> float:
    if len(xs) <= 1:
        return 0.0
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def normal_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def lo1_distributions(demo: list[dict]) -> dict:
    vals = [float(r["response_time_days"]) for r in demo]
    mu = mean(vals)
    sd = math.sqrt(variance(vals))

    # Method-of-moments for gamma: k = (mu/sd)^2, theta = sd^2/mu
    k = (mu / sd) ** 2 if sd > 0 else 0.0
    theta = (sd**2) / mu if mu > 0 else 0.0
    return {"normal_mean": mu, "normal_sd": sd, "gamma_shape_mom": k, "gamma_scale_mom": theta}


def lo2_hypothesis_tests(demo: list[dict]) -> dict:
    reg = [r for r in demo if int(r["regular_monitoring"]) == 1]
    irr = [r for r in demo if int(r["regular_monitoring"]) == 0]

    p1 = mean([float(r["effective_response"]) for r in reg])
    p2 = mean([float(r["effective_response"]) for r in irr])
    n1, n2 = len(reg), len(irr)
    p_pool = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2)) if p_pool not in (0, 1) else 1e-9
    z = (p1 - p2) / se
    p_two = 2 * (1 - normal_cdf(abs(z)))

    loss_reg = [float(r["yield_loss_pct"]) for r in reg]
    loss_irr = [float(r["yield_loss_pct"]) for r in irr]
    t_num = mean(loss_reg) - mean(loss_irr)
    t_den = math.sqrt(variance(loss_reg) / n1 + variance(loss_irr) / n2)
    t_stat = t_num / t_den if t_den else 0.0

    return {
        "regular_effective_rate": p1,
        "irregular_effective_rate": p2,
        "two_prop_z": z,
        "two_prop_p_approx": p_two,
        "welch_t_stat": t_stat,
    }


def lo3_regression(demo: list[dict]) -> dict:
    x1 = [float(r["monitoring_days_per_month"]) for r in demo]
    x2 = [float(r["climate_risk_index"]) for r in demo]
    x3 = [float(r.get("soil_quality_index", 1.0)) for r in demo]
    x4 = [float(r.get("pest_management_score", 1.0)) for r in demo]
    y = [float(r["yield_loss_pct"]) for r in demo]

    # Solve OLS for y = b0 + b1*x1 + b2*x2 + b3*x3 + b4*x4 via normal equations
    n = len(y)
    X = [[1.0, a, b, c, d] for a, b, c, d in zip(x1, x2, x3, x4)]
    
    vars_count = 5
    A = [[0.0] * vars_count for _ in range(vars_count)]
    b = [0.0] * vars_count
    
    for i in range(vars_count):
        for j in range(vars_count):
            A[i][j] = sum(X[k][i] * X[k][j] for k in range(n))
        b[i] = sum(X[k][i] * y[k] for k in range(n))

    # Gaussian elimination
    for i in range(vars_count):
        pivot = A[i][i] if A[i][i] != 0 else 1e-9
        for j in range(i, vars_count):
            A[i][j] /= pivot
        b[i] /= pivot
        for k in range(vars_count):
            if k == i:
                continue
            factor = A[k][i]
            for j in range(i, vars_count):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    b0, b1, b2, b3, b4 = b
    preds = [b0 + b1 * row[1] + b2 * row[2] + b3 * row[3] + b4 * row[4] for row in X]
    y_bar = mean(y)
    ss_tot = sum((yy - y_bar) ** 2 for yy in y)
    ss_res = sum((yy - pp) ** 2 for yy, pp in zip(y, preds))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    mae = mean([abs(yy - pp) for yy, pp in zip(y, preds)])

    return {
        "intercept": b0,
        "beta_monitoring": b1,
        "beta_climate_risk": b2,
        "beta_soil_quality": b3,
        "beta_pest_management": b4,
        "r2": r2,
        "mae": mae
    }


def lo4_exponential_family(nasa: list[dict]) -> dict:
    rain = [max(1e-6, float(r["precip_mm_day"])) for r in nasa]
    temp = [float(r["temperature_c"]) for r in nasa]

    lam_exp = 1 / mean(rain)
    rain_count = [round(r) for r in rain]
    lam_poi = mean([float(x) for x in rain_count])
    return {
        "exponential_lambda": lam_exp,
        "poisson_lambda_proxy": lam_poi,
        "normal_temp_mean": mean(temp),
        "normal_temp_sd": statistics.stdev(temp),
    }


def lo5_time_series(fao: list[dict]) -> dict:
    series = [float(r["yield_hg_ha"]) for r in sorted(fao, key=lambda x: int(x["year"]))]
    train, test = series[:-5], series[-5:]

    alpha = 0.35
    level = train[0]
    trend = train[1] - train[0]
    for t in range(1, len(train)):
        prev_level = level
        level = alpha * train[t] + (1 - alpha) * (level + trend)
        trend = alpha * (level - prev_level) + (1 - alpha) * trend

    forecasts = [level + (i + 1) * trend for i in range(len(test))]
    mape = 100 * mean([abs((a - f) / a) for a, f in zip(test, forecasts)])
    return {"train_n": len(train), "test_n": len(test), "mape_pct": mape, "last_forecast_hg_ha": forecasts[-1]}


def lo6_bayesian(demo: list[dict]) -> dict:
    reg = [r for r in demo if int(r["regular_monitoring"]) == 1]
    success = sum(int(r["effective_response"]) for r in reg)
    n = len(reg)
    a_post = 1 + success
    b_post = 1 + n - success
    random.seed(2025)

    samples = [random.betavariate(a_post, b_post) for _ in range(20000)]
    samples.sort()
    ci_low = samples[int(0.025 * len(samples))]
    ci_high = samples[int(0.975 * len(samples))]

    return {
        "posterior_alpha": a_post,
        "posterior_beta": b_post,
        "posterior_mean": a_post / (a_post + b_post),
        "credible_interval_95_low": ci_low,
        "credible_interval_95_high": ci_high,
    }


def main() -> None:
    nasa = read_csv(RAW_DIR / "nasa_power_sri_lanka_monthly.csv")
    fao = read_csv(RAW_DIR / "faostat_sri_lanka_rice_yield.csv")
    demo = read_csv(RAW_DIR / "farm_monitoring_primary_demo.csv")

    results = {
        "LO1_distributions": lo1_distributions(demo),
        "LO2_hypothesis_testing": lo2_hypothesis_tests(demo),
        "LO3_regression": lo3_regression(demo),
        "LO4_exponential_family": lo4_exponential_family(nasa),
        "LO5_time_series": lo5_time_series(fao),
        "LO6_bayesian": lo6_bayesian(demo),
    }

    with (PROCESSED_DIR / "analysis_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for section, metrics in results.items():
            for k, v in metrics.items():
                writer.writerow([f"{section}.{k}", v])

    with (REPORT_DIR / "key_results.md").open("w", encoding="utf-8") as f:
        f.write("# Key Statistical Results\n\n")
        for section, metrics in results.items():
            f.write(f"## {section}\n")
            for k, v in metrics.items():
                f.write(f"- **{k}**: {v}\n")
            f.write("\n")

    print("Saved data/processed/analysis_results.csv and reports/key_results.md")


if __name__ == "__main__":
    main()
