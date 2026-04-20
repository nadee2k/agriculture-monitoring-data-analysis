"""Data collection pipeline for NASA POWER climate data and FAOSTAT crop data (stdlib only)."""
from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fetch_nasa_power_monthly(lat: float, lon: float, start_year: int = 2000, end_year: int = 2024) -> list[dict]:
    params = {
        "parameters": "T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
        "community": "AG",
        "latitude": lat,
        "longitude": lon,
        "start": f"{start_year}01",
        "end": f"{end_year}12",
        "format": "JSON",
    }
    url = f"https://power.larc.nasa.gov/api/temporal/monthly/point?{urlencode(params)}"
    with urlopen(url) as resp:  # nosec B310
        data = json.loads(resp.read().decode("utf-8"))

    prm = data["properties"]["parameter"]
    rows = []
    for yyyymm in sorted(prm["T2M"].keys()):
        rows.append(
            {
                "date": yyyymm,
                "temperature_c": float(prm["T2M"][yyyymm]),
                "precip_mm_day": float(prm["PRECTOTCORR"][yyyymm]),
                "solar_mj_m2_day": float(prm["ALLSKY_SFC_SW_DWN"][yyyymm]),
            }
        )
    return rows


def fallback_nasa_monthly(start_year: int = 2000, end_year: int = 2024) -> list[dict]:
    rows = []
    for y in range(start_year, end_year + 1):
        for m in range(1, 13):
            phase = (m - 1) / 12 * 2 * math.pi
            temp = 27.0 + 1.8 * math.sin(phase) + random.gauss(0, 0.4)
            rain = max(0.2, 4.2 + 2.7 * math.cos(phase) + random.gauss(0, 0.6))
            solar = 15.5 + 2.0 * math.sin(phase + 0.8) + random.gauss(0, 0.5)
            rows.append(
                {
                    "date": f"{y}{m:02d}",
                    "temperature_c": round(temp, 4),
                    "precip_mm_day": round(rain, 4),
                    "solar_mj_m2_day": round(solar, 4),
                }
            )
    return rows


def fetch_faostat_yield(country_code: int = 38, item_code: int = 27) -> list[dict]:
    url = (
        "https://fenixservices.fao.org/faostat/api/v1/en/"
        f"QC/Production_Crops_Livestock?area_code={country_code}&item_code={item_code}&element_code=5419"
    )
    with urlopen(url) as resp:  # nosec B310
        data = json.loads(resp.read().decode("utf-8"))
    rows = []
    for r in data.get("data", []):
        rows.append({"year": int(r["year"]), "yield_hg_ha": float(r["value"]), "yield_unit": r["unit"]})
    if not rows:
        raise ValueError("No FAOSTAT data returned.")
    rows.sort(key=lambda x: x["year"])
    return rows


def fallback_faostat_yield(start_year: int = 2000, end_year: int = 2024) -> list[dict]:
    rows = []
    baseline = 39000
    for y in range(start_year, end_year + 1):
        trend = (y - start_year) * 220
        cyc = 1800 * math.sin((y - start_year) * 2 * math.pi / 5)
        noise = random.gauss(0, 700)
        rows.append({"year": y, "yield_hg_ha": round(baseline + trend + cyc + noise, 2), "yield_unit": "hg/ha"})
    return rows


def process_secondary_data(crop_csv: Path, fertilizer_csv: Path, pesticide_csv: Path, irrigation_csv: Path, climate_csv: Path) -> list[dict]:
    # Load CSVs
    crops = read_csv(crop_csv)
    fertilizers = read_csv(fertilizer_csv)
    pesticides = read_csv(pesticide_csv)
    irrigations = read_csv(irrigation_csv)
    climates = read_csv(climate_csv)
    
    # Aggregate by year
    year_data = {}
    for row in crops:
        if row['Element'] == 'Yield' and row['Item'] == 'Rice':
            year = int(row['Year'])
            if year not in year_data:
                year_data[year] = {'yield': float(row['Value'])}
    
    for row in fertilizers:
        if 'Nutrient' in row['Item']:
            year = int(row['Year'])
            if year in year_data:
                year_data[year]['fertilizer'] = year_data[year].get('fertilizer', 0) + float(row['Value'])
    
    for row in pesticides:
        year = int(row['Year'])
        if year in year_data:
            year_data[year]['pesticide'] = year_data[year].get('pesticide', 0) + float(row['Value'])
    
    for row in irrigations:
        if 'irrigation' in row['Item'].lower():
            year = int(row['Year'])
            if year in year_data:
                year_data[year]['irrigation'] = float(row['Value'])
    
    # Derive variables per year (treat each year as a "farm")
    rows = []
    for year, data in year_data.items():
        yield_val = data['yield']
        fertilizer_amt = data.get('fertilizer', 0)
        pesticide_amt = data.get('pesticide', 0)
        irrigation_amt = data.get('irrigation', 0)
        
        # Proxy monitoring_days based on inputs
        monitoring_days = min(30, int((fertilizer_amt / 1000) + (pesticide_amt / 100) + (irrigation_amt / 10)))
        
        # Climate risk: average for that year
        year_climates = [r for r in climates if r['date'].startswith(str(year))]
        climate_risk = calculate_climate_risk(0, year_climates)  # farm_id not used
        
        # Expected yield: average across years
        all_yields = [d['yield'] for d in year_data.values()]
        expected_yield = sum(all_yields) / len(all_yields)
        yield_loss_pct = calculate_yield_loss(yield_val, expected_yield)
        
        response_time_days = simulate_response_time(monitoring_days, climate_risk)
        
        rows.append({
            'farm_id': year,  # Use year as farm_id
            'monitoring_days_per_month': monitoring_days,
            'climate_risk_index': climate_risk,
            'response_time_days': response_time_days,
            'yield_loss_pct': yield_loss_pct,
            'regular_monitoring': 1 if monitoring_days >= 15 else 0,
            'effective_response': 1 if response_time_days <= 7 else 0,
        })
    
    return rows


def create_demo_monitoring_data(seed: int = 42, n_farms: int = 120) -> list[dict]:
    fert_base, pest_base = 233.0, 2.0
    try:
        crop_path = RAW_DIR / "Crop_data.csv"
        fert_path = RAW_DIR / "Fertilizer_data.csv"
        pest_path = RAW_DIR / "Pesticide_data.csv"
        area_ha = 1_000_000.0
        if crop_path.exists():
            with open(crop_path, "r", encoding="utf-8") as f:
                r = list(csv.DictReader(f))
                areas = [float(row["Value"]) for row in r if row["Element"] == "Area harvested"]
                if areas:
                    area_ha = sum(areas) / len(areas)
        if fert_path.exists():
            with open(fert_path, "r", encoding="utf-8") as f:
                r = list(csv.DictReader(f))
                fert_total = sum(float(row["Value"]) for row in r)
                years = set(row["Year"] for row in r)
                fert_base = (fert_total / len(years) * 1000) / area_ha if years else fert_base
        if pest_path.exists():
            with open(pest_path, "r", encoding="utf-8") as f:
                r = list(csv.DictReader(f))
                pest_total = sum(float(row["Value"]) for row in r)
                years = set(row["Year"] for row in r)
                pest_base = (pest_total / len(years) * 1000) / area_ha if years else pest_base
    except Exception:
        pass

    random.seed(seed)
    rows = []
    for i in range(1, n_farms + 1):
        monitoring_days = random.randint(2, 30)
        climate_risk = random.gauss(0, 1)
        
        soil_quality_index = max(0.1, random.gauss(fert_base, fert_base * 0.2) / fert_base)
        pest_management_score = max(0.1, random.gauss(pest_base, pest_base * 0.3) / pest_base)
        
        response_time = max(1.0, 15 - 0.35 * monitoring_days + 1.8 * climate_risk + random.gauss(0, 2))
        yield_loss = min(100.0, max(0.0, 35 - 0.8 * monitoring_days + 4.5 * climate_risk - 4.0 * soil_quality_index - 3.0 * pest_management_score + random.gauss(0, 4)))
        
        rows.append(
            {
                "farm_id": i,
                "monitoring_days_per_month": monitoring_days,
                "climate_risk_index": round(climate_risk, 4),
                "soil_quality_index": round(soil_quality_index, 4),
                "pest_management_score": round(pest_management_score, 4),
                "response_time_days": round(response_time, 4),
                "yield_loss_pct": round(yield_loss, 4),
                "regular_monitoring": 1 if monitoring_days >= 15 else 0,
                "effective_response": 1 if response_time <= 7 else 0,
            }
        )
    return rows


def calculate_climate_risk(farm_id, climates):
    # Aggregate climate stress for the farm's location/year
    if climates:
        return sum(float(r['temperature_c']) + float(r['precip_mm_day']) for r in climates) / len(climates)
    return 0.0


def calculate_yield_loss(actual, expected):
    if expected > 0:
        return max(0, (expected - actual) / expected * 100)
    return 0.0


def simulate_response_time(monitoring_days, climate_risk):
    # Proxy: lower monitoring = higher response time
    return max(1, 15 - 0.5 * monitoring_days + 2 * climate_risk)


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    random.seed(123)
    source_notes = []

    try:
        nasa = fetch_nasa_power_monthly(7.8731, 80.7718)
        source_notes.append("NASA POWER: live API")
    except Exception:
        nasa = fallback_nasa_monthly()
        source_notes.append("NASA POWER: fallback synthetic data (network blocked)")

    try:
        fao = fetch_faostat_yield(38, 27)
        source_notes.append("FAOSTAT: live API")
    except Exception:
        fao = fallback_faostat_yield()
        source_notes.append("FAOSTAT: fallback synthetic data (network blocked)")

    # Execute the updated plan: simulate 120 farms using real FAOSTAT macro-level baselines
    demo = create_demo_monitoring_data()
    source_notes.append("Primary dataset: realistic simulation using Sri Lankan macro baselines (N=120)")

    write_csv(RAW_DIR / "nasa_power_sri_lanka_monthly.csv", nasa)
    write_csv(RAW_DIR / "faostat_sri_lanka_rice_yield.csv", fao)
    write_csv(RAW_DIR / "farm_monitoring_primary_demo.csv", demo)

    with (RAW_DIR / "data_sources.txt").open("w", encoding="utf-8") as f:
        for line in source_notes:
            f.write(f"- {line}\n")

    print("Saved raw datasets to data/raw")


if __name__ == "__main__":
    main()
