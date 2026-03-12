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


def create_demo_monitoring_data(seed: int = 42, n_farms: int = 120) -> list[dict]:
    random.seed(seed)
    rows = []
    for i in range(1, n_farms + 1):
        monitoring_days = random.randint(2, 30)
        climate_risk = random.gauss(0, 1)
        response_time = max(1.0, 15 - 0.35 * monitoring_days + 1.8 * climate_risk + random.gauss(0, 2))
        yield_loss = min(100.0, max(0.0, 28 - 0.8 * monitoring_days + 4.5 * climate_risk + random.gauss(0, 4)))
        rows.append(
            {
                "farm_id": i,
                "monitoring_days_per_month": monitoring_days,
                "climate_risk_index": round(climate_risk, 4),
                "response_time_days": round(response_time, 4),
                "yield_loss_pct": round(yield_loss, 4),
                "regular_monitoring": 1 if monitoring_days >= 15 else 0,
                "effective_response": 1 if response_time <= 7 else 0,
            }
        )
    return rows


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

    demo = create_demo_monitoring_data()
    source_notes.append("Primary dataset: reproducible demo generator")

    write_csv(RAW_DIR / "nasa_power_sri_lanka_monthly.csv", nasa)
    write_csv(RAW_DIR / "faostat_sri_lanka_rice_yield.csv", fao)
    write_csv(RAW_DIR / "farm_monitoring_primary_demo.csv", demo)

    with (RAW_DIR / "data_sources.txt").open("w", encoding="utf-8") as f:
        for line in source_notes:
            f.write(f"- {line}\n")

    print("Saved raw datasets to data/raw")


if __name__ == "__main__":
    main()
