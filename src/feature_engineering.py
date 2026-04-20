"""Feature engineering: create monitoring_index and other analytical features."""
import csv
import math
from pathlib import Path
from typing import List, Dict

PROCESSED_DIR = Path("data/processed")


def load_cleaned_data() -> List[Dict]:
    """Load cleaned annual data from data_cleaning.py output."""
    with (PROCESSED_DIR / "cleaned_annual.csv").open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def engineer_features(data: List[Dict]) -> List[Dict]:
    """
    Engineer analytical features from cleaned data.
    
    Core Features:
    - monitoring_index: (fertilizer_intensity + irrigation_ratio) / 2
    - climate_risk: normalized temperature and precipitation anomaly
    - yield_loss_pct: deviation from expected yield
    - response_time: proxy based on monitoring intensity
    """
    
    # Calculate expected yield (baseline)
    yields = []
    for row in data:
        try:
            if 'yield_kg_ha' in row and row['yield_kg_ha']:
                yields.append(float(row['yield_kg_ha']))
        except (ValueError, TypeError):
            continue
    expected_yield = sum(yields) / len(yields) if yields else 0
    
    # Calculate climate statistics for normalization
    temps = []
    precips = []
    for row in data:
        try:
            if 'temp_annual_mean' in row and row['temp_annual_mean']:
                temps.append(float(row['temp_annual_mean']))
            if 'precip_annual_mean' in row and row['precip_annual_mean']:
                precips.append(float(row['precip_annual_mean']))
        except (ValueError, TypeError):
            continue
    
    temp_mean = sum(temps) / len(temps) if temps else 27.0
    temp_std = (sum((t - temp_mean) ** 2 for t in temps) / len(temps)) ** 0.5 if temps else 1.0
    precip_mean = sum(precips) / len(precips) if precips else 4.0
    precip_std = (sum((p - precip_mean) ** 2 for p in precips) / len(precips)) ** 0.5 if precips else 1.0
    
    # Calculate average area for fertilizer intensity
    areas = []
    for row in data:
        try:
            if 'area_harvested_ha' in row and row['area_harvested_ha']:
                areas.append(float(row['area_harvested_ha']))
        except (ValueError, TypeError):
            continue
    avg_area = sum(areas) / len(areas) if areas else 1066403  # Default Sri Lanka rice area
    
    # Engineer features
    featured_data = []
    for row in data:
        featured_row = dict(row)
        
        # Extract values with fallbacks
        yield_val = float(row.get('yield_kg_ha', expected_yield))
        area_ha = float(row.get('area_harvested_ha', avg_area))
        fert_tonnes = float(row.get('fertilizer_tonnes', 0))
        irrig_ha = float(row.get('irrigation_area_ha', 0))
        temp_val = float(row.get('temp_annual_mean', temp_mean))
        precip_val = float(row.get('precip_annual_mean', precip_mean))
        
        # 1. Monitoring Index: (fertilizer_intensity + irrigation_ratio) / 2
        fertilizer_intensity = (fert_tonnes * 1000 / area_ha) if area_ha > 0 else 0  # kg/ha
        irrigation_ratio = (irrig_ha / area_ha) if area_ha > 0 else 0  # proportion
        monitoring_index = (fertilizer_intensity / 100 + irrigation_ratio) / 2  # normalized scale
        featured_row['monitoring_index'] = round(monitoring_index, 4)
        
        # 2. Binary monitoring classification
        featured_row['regular_monitoring'] = 1 if monitoring_index >= 0.15 else 0
        
        # 3. Climate Risk Index: (temp_anomaly + precip_coefficient) normalized
        temp_anomaly = (temp_val - temp_mean) / temp_std if temp_std > 0 else 0
        precip_anomaly = (precip_val - precip_mean) / precip_std if precip_std > 0 else 0
        climate_risk = (abs(temp_anomaly) + abs(precip_anomaly)) / 2
        featured_row['climate_risk_index'] = round(climate_risk, 4)
        
        # 4. Yield Loss: deviation from expected
        yield_loss = max(0, ((expected_yield - yield_val) / expected_yield * 100)) if expected_yield > 0 else 0
        featured_row['yield_loss_pct'] = round(yield_loss, 4)
        
        # 5. Response Time Proxy: inversely related to monitoring
        # Lower monitoring → higher response time
        response_time = max(1.0, 15 - (monitoring_index * 20) + (climate_risk * 10))
        featured_row['response_time_days'] = round(response_time, 4)
        featured_row['effective_response'] = 1 if response_time <= 7 else 0
        
        # 6. Additional calculated fields
        featured_row['fertilizer_intensity_kg_ha'] = round(fertilizer_intensity, 4)
        featured_row['irrigation_ratio'] = round(irrigation_ratio, 4)
        
        featured_data.append(featured_row)
    
    return featured_data


def write_engineered_data(data: List[Dict]) -> None:
    """Write engineered features to CSV."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    if data:
        with (PROCESSED_DIR / "final_dataset.csv").open("w", newline="", encoding="utf-8") as f:
            fieldnames = list(data[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Saved engineered features: {PROCESSED_DIR / 'final_dataset.csv'}")


def print_feature_summary(data: List[Dict]) -> None:
    """Print summary statistics of engineered features."""
    print("\n=== Feature Engineering Summary ===")
    print(f"Records: {len(data)}")
    
    if data:
        # Extract monitoring indices
        monitoring_indices = []
        climate_risks = []
        yield_losses = []
        
        for row in data:
            try:
                if 'monitoring_index' in row:
                    monitoring_indices.append(float(row['monitoring_index']))
                if 'climate_risk_index' in row:
                    climate_risks.append(float(row['climate_risk_index']))
                if 'yield_loss_pct' in row:
                    yield_losses.append(float(row['yield_loss_pct']))
            except (ValueError, TypeError):
                continue
        
        if monitoring_indices:
            print(f"\nMonitoring Index:")
            print(f"  Min: {min(monitoring_indices):.4f}")
            print(f"  Max: {max(monitoring_indices):.4f}")
            print(f"  Mean: {sum(monitoring_indices) / len(monitoring_indices):.4f}")
        
        if climate_risks:
            print(f"\nClimate Risk Index:")
            print(f"  Min: {min(climate_risks):.4f}")
            print(f"  Max: {max(climate_risks):.4f}")
            print(f"  Mean: {sum(climate_risks) / len(climate_risks):.4f}")
        
        if yield_losses:
            print(f"\nYield Loss (%):")
            print(f"  Min: {min(yield_losses):.4f}")
            print(f"  Max: {max(yield_losses):.4f}")
            print(f"  Mean: {sum(yield_losses) / len(yield_losses):.4f}")


def main() -> None:
    """Run feature engineering pipeline."""
    print("Loading cleaned data...")
    cleaned_data = load_cleaned_data()
    
    print("Engineering features...")
    featured_data = engineer_features(cleaned_data)
    
    print("Writing engineered data...")
    write_engineered_data(featured_data)
    print_feature_summary(featured_data)
    
    print("\nFeature engineering complete.")


if __name__ == "__main__":
    main()
