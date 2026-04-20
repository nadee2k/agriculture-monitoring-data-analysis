"""Evaluation and diagnostics for model outputs."""
import csv
from pathlib import Path
from typing import List, Dict

RESULTS_DIR = Path("results/model_outputs")


def load_modeling_results() -> Dict:
    """Load modeling results from CSV."""
    results = {}
    try:
        with (RESULTS_DIR / "modeling_results.csv").open("r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    results[row['metric']] = float(row['value'])
                except ValueError:
                    # Store string values as-is (e.g., error messages)
                    results[row['metric']] = row['value']
    except FileNotFoundError:
        print("Modeling results not found. Run modeling.py first.")
    
    return results


def print_summary() -> None:
    """Print summary of modeling results."""
    results = load_modeling_results()
    
    if not results:
        print("No results to evaluate.")
        return
    
    print("\n" + "="*60)
    print("MODEL EVALUATION SUMMARY")
    print("="*60)
    
    # LO1
    print("\n[LO1] Distributions:")
    print(f"  Response Time Mean: {results.get('LO1_distributions.normal_mean_response_time', 'N/A')}")
    print(f"  Response Time SD: {results.get('LO1_distributions.normal_sd_response_time', 'N/A')}")
    
    # LO2
    print("\n[LO2] Hypothesis Testing:")
    print(f"  Regular Monitoring Yield Loss: {results.get('LO2_hypothesis_testing.regular_mean_yield_loss', 'N/A')}")
    print(f"  Irregular Monitoring Yield Loss: {results.get('LO2_hypothesis_testing.irregular_mean_yield_loss', 'N/A')}")
    print(f"  Welch t-statistic: {results.get('LO2_hypothesis_testing.welch_t_statistic', 'N/A')}")
    
    # LO3
    print("\n[LO3] Regression Model:")
    print(f"  Monitoring Index Coefficient: {results.get('LO3_regression.beta_monitoring_index', 'N/A')}")
    print(f"  Climate Risk Coefficient: {results.get('LO3_regression.beta_climate_risk', 'N/A')}")
    print(f"  R-squared: {results.get('LO3_regression.r_squared', 'N/A')}")
    print(f"  MAE: {results.get('LO3_regression.mae', 'N/A')}")
    
    # LO5
    print("\n[LO5] Time Series Forecasting:")
    print(f"  Training Set Size: {results.get('LO5_time_series.train_size', 'N/A')}")
    print(f"  Test Set Size: {results.get('LO5_time_series.test_size', 'N/A')}")
    print(f"  MAPE (%): {results.get('LO5_time_series.mape_percent', 'N/A')}")
    
    # LO6
    print("\n[LO6] Bayesian Inference:")
    print(f"  Posterior Mean: {results.get('LO6_bayesian.posterior_mean', 'N/A')}")
    print(f"  95% Credible Interval: [{results.get('LO6_bayesian.credible_interval_95_low', 'N/A')}, {results.get('LO6_bayesian.credible_interval_95_high', 'N/A')}]")
    
    print("\n" + "="*60)


def main() -> None:
    """Run evaluation."""
    print_summary()


if __name__ == "__main__":
    main()
