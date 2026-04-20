import csv
from pathlib import Path

def get_baselines():
    raw_dir = Path("data/raw")
    crop_path = raw_dir / "Crop_data.csv"
    fert_path = raw_dir / "Fertilizer_data.csv"
    pest_path = raw_dir / "Pesticide_data.csv"

    area_ha = 1_000_000
    try:
        if crop_path.exists():
            with open(crop_path, 'r', encoding='utf-8') as f:
                r = list(csv.DictReader(f))
                areas = [float(row["Value"]) for row in r if row["Element"] == "Area harvested"]
                if areas:
                    area_ha = sum(areas) / len(areas)
    except Exception as e:
        print(f"Crop parsing error: {e}")

    fert_kg = 384.0
    try:
        if fert_path.exists():
            with open(fert_path, 'r', encoding='utf-8') as f:
                r = list(csv.DictReader(f))
                fert_total_t = sum(float(row["Value"]) for row in r)
                # This sum over 4 years gives total fertilizer across 4 years.
                # Average per year
                years = set(row["Year"] for row in r)
                fert_avg_t_yr = fert_total_t / len(years) if years else 0
                fert_kg = (fert_avg_t_yr * 1000) / area_ha if area_ha else 384.0
    except Exception as e:
        print(f"Fert parsing error: {e}")

    pest_kg = 2.4
    try:
        if pest_path.exists():
            with open(pest_path, 'r', encoding='utf-8') as f:
                r = list(csv.DictReader(f))
                pest_total_t = sum(float(row["Value"]) for row in r)
                years = set(row["Year"] for row in r)
                pest_avg_t_yr = pest_total_t / len(years) if years else 0
                pest_kg = (pest_avg_t_yr * 1000) / area_ha if area_ha else 2.4
    except Exception as e:
        print(f"Pest parsing error: {e}")

    return fert_kg, pest_kg

print(get_baselines())
