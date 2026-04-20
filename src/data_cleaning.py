"""Data loading and cleaning pipeline for FAOSTAT and NASA POWER datasets."""
import csv
from pathlib import Path
from typing import List, Dict

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def read_csv(path: Path) -> List[Dict]:
    """Load CSV file into list of dictionaries."""
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_faostat_yield() -> List[Dict]:
    """Load FAOSTAT rice yield data (kg/ha by year)."""
    data = read_csv(RAW_DIR / "FAOSTAT_data_en_4-20-2026.csv")
    return data


def load_crop_data() -> List[Dict]:
    """Load FAOSTAT crop production and area data."""
    data = read_csv(RAW_DIR / "FAOSTAT_data_en_4-20-2026 (3).csv")
    return data


def load_fertilizer_data() -> List[Dict]:
    """Load FAOSTAT fertilizer use data (tonnes by year)."""
    data = read_csv(RAW_DIR / "FAOSTAT_data_en_4-20-2026 (1).csv")
    return data


def load_irrigation_data() -> List[Dict]:
    """Load FAOSTAT irrigation area data (1000 ha by year)."""
    data = read_csv(RAW_DIR / "FAOSTAT_data_en_4-20-2026 (2).csv")
    return data


def load_nasa_climate() -> List[Dict]:
    """Load daily weather data (temperature, rainfall)."""
    data = read_csv(RAW_DIR / "sri_lanka_weather_2000_2023.csv")
    return data


def clean_and_aggregate_by_year() -> Dict[int, Dict]:
    """
    Clean and aggregate all data by year.
    Returns: {year: {yield, area_harvested, fertilizer_total, irrigation_area, temp_annual, precip_annual}}
    """
    yield_data = load_faostat_yield()
    crop_data = load_crop_data()
    fertilizer_data = load_fertilizer_data()
    irrigation_data = load_irrigation_data()
    weather_data = load_nasa_climate()
    
    year_dict = {}
    
    # Load yield data (FAOSTAT format)
    for row in yield_data:
        try:
            year = int(row.get('Year') or row.get('Year Code', 0))
            if year == 0:
                continue
            yield_val = float(row.get('Value', 0))
            if year not in year_dict:
                year_dict[year] = {}
            year_dict[year]['yield_kg_ha'] = yield_val
        except (ValueError, KeyError):
            continue
    
    # Load crop area harvested (FAOSTAT format)
    for row in crop_data:
        try:
            year = int(row.get('Year') or row.get('Year Code', 0))
            if year == 0:
                continue
            area = float(row.get('Value', 0))
            if year not in year_dict:
                year_dict[year] = {}
            year_dict[year]['area_harvested_ha'] = area
        except (ValueError, KeyError):
            continue
    
    # Aggregate fertilizer by year (nitrogen only for simplicity)
    for row in fertilizer_data:
        try:
            year = int(row.get('Year') or row.get('Year Code', 0))
            if year == 0:
                continue
            value = float(row.get('Value', 0))  # tonnes
            if year not in year_dict:
                year_dict[year] = {}
            year_dict[year]['fertilizer_tonnes'] = year_dict[year].get('fertilizer_tonnes', 0) + value
        except (ValueError, KeyError):
            continue
    
    # Load irrigation area (FAOSTAT format: 1000 ha)
    for row in irrigation_data:
        try:
            year = int(row.get('Year') or row.get('Year Code', 0))
            if year == 0:
                continue
            area_1000ha = float(row.get('Value', 0))
            area_ha = area_1000ha * 1000  # Convert to ha
            if year not in year_dict:
                year_dict[year] = {}
            year_dict[year]['irrigation_area_ha'] = area_ha
        except (ValueError, KeyError):
            continue
    
    # Aggregate daily weather by year (annual mean)
    annual_climate = {}
    for row in weather_data:
        try:
            date_str = row.get('date', '')
            if len(date_str) < 4:
                continue
            year = int(date_str[:4])
            temp = float(row.get('temperature_c', 0))
            precip = float(row.get('rainfall_mm', 0))
            
            if year not in annual_climate:
                annual_climate[year] = {'temps': [], 'precips': []}
            annual_climate[year]['temps'].append(temp)
            annual_climate[year]['precips'].append(precip)
        except (ValueError, KeyError):
            continue
    
    # Compute annual means and add to year_dict
    for year, climate_data in annual_climate.items():
        if year not in year_dict:
            year_dict[year] = {}
        if climate_data['temps']:
            year_dict[year]['temp_annual_mean'] = sum(climate_data['temps']) / len(climate_data['temps'])
        if climate_data['precips']:
            year_dict[year]['precip_annual_mean'] = sum(climate_data['precips']) / len(climate_data['precips'])
    
    return year_dict
    
    return year_dict


def write_cleaned_data(data: Dict) -> None:
    """Write cleaned annual data to CSV."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    rows = []
    for year in sorted(data.keys()):
        row = {'year': year}
        row.update(data[year])
        rows.append(row)
    
    if rows:
        with (PROCESSED_DIR / "cleaned_annual.csv").open("w", newline="", encoding="utf-8") as f:
            fieldnames = list(rows[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Saved cleaned annual data: {PROCESSED_DIR / 'cleaned_annual.csv'}")


def main() -> None:
    """Run data cleaning pipeline."""
    print("Loading and cleaning data...")
    year_dict = clean_and_aggregate_by_year()
    
    print(f"Processed {len(year_dict)} years of data")
    write_cleaned_data(year_dict)
    print("Data cleaning complete.")


if __name__ == "__main__":
    main()
