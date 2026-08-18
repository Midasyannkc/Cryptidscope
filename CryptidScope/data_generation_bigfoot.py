"""
Generates a synthetic Bigfoot sightings dataset for CryptidScope.

Modeled on the shape of the real BFRO (Bigfoot Field Researchers Organization)
public dataset: report date, state/county, a classification (A/B/C, reflecting
report reliability), and rough conditions at the time of the sighting.
Coordinates are randomized within each state's approximate bounding box, not
geocoded precisely, since exact geocoding isn't the point of this exercise --
state/region-level pattern-finding is.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(11)

OUTPUT_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Rough bounding boxes (lat_min, lat_max, lon_min, lon_max) for a spread of states
STATE_BOUNDS = {
    "Washington": (45.5, 49.0, -124.7, -117.0),
    "Oregon": (42.0, 46.2, -124.5, -116.5),
    "California": (32.5, 42.0, -124.4, -114.1),
    "Ohio": (38.4, 42.0, -84.8, -80.5),
    "Texas": (25.8, 36.5, -106.6, -93.5),
    "Pennsylvania": (39.7, 42.3, -80.5, -74.7),
    "Michigan": (41.7, 48.3, -90.4, -82.4),
    "Florida": (24.5, 31.0, -87.6, -80.0),
    "New York": (40.5, 45.0, -79.8, -71.9),
    "Illinois": (37.0, 42.5, -91.5, -87.0),
}

CLASSIFICATIONS = {
    "A": 0.35,  # clear sighting, best conditions
    "B": 0.45,  # possible sighting, secondhand or unclear
    "C": 0.20,  # third-hand or unverifiable report
}

CONDITIONS = ["Clear", "Overcast", "Rain", "Fog", "Snow", "Dusk", "Night", "Dawn"]
ENVIRONMENTS = ["Dense Forest", "Open Field", "Near Road", "Riverbank", "Rural Residential", "Mountain Trail"]


def weighted_choice(weighted_dict):
    items, weights = zip(*weighted_dict.items())
    return random.choices(items, weights=weights, k=1)[0]


def generate_sightings(n=850):
    rows = []
    start_date = datetime(1995, 1, 1)
    end_date = datetime(2025, 12, 31)
    span_days = (end_date - start_date).days

    for i in range(1, n + 1):
        state = random.choice(list(STATE_BOUNDS.keys()))
        lat_min, lat_max, lon_min, lon_max = STATE_BOUNDS[state]
        report_date = start_date + timedelta(days=random.randint(0, span_days))

        rows.append({
            "report_id": f"BF{i:05d}",
            "report_date": report_date.strftime("%Y-%m-%d"),
            "year": report_date.year,
            "month": report_date.month,
            "state": state,
            "classification": weighted_choice(CLASSIFICATIONS),
            "latitude": round(random.uniform(lat_min, lat_max), 4),
            "longitude": round(random.uniform(lon_min, lon_max), 4),
            "conditions": random.choice(CONDITIONS),
            "environment": random.choice(ENVIRONMENTS),
            "witness_count": random.choices([1, 2, 3, 4], weights=[0.55, 0.25, 0.13, 0.07])[0],
        })
    return rows


def write_csv(rows, path, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {path}")


if __name__ == "__main__":
    sightings = generate_sightings()
    write_csv(
        sightings,
        OUTPUT_DIR / "bigfoot_sightings.csv",
        ["report_id", "report_date", "year", "month", "state", "classification",
         "latitude", "longitude", "conditions", "environment", "witness_count"],
    )
