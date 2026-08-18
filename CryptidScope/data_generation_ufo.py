"""
Generates a synthetic UFO sightings dataset for CryptidScope.

Modeled on the shape of the real NUFORC (National UFO Reporting Center) public
dataset: date/time, city/state, shape description, and duration. Built as a
separate table from Bigfoot sightings deliberately -- they share a date and
geography grain, which lets the Power BI data model join them on a shared
Date and Location dimension rather than merging two unrelated fact tables
into one.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(23)

OUTPUT_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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

SHAPES = ["Light", "Triangle", "Circle", "Disk", "Fireball", "Sphere", "Oval", "Cylinder", "Formation", "Unknown"]


def generate_sightings(n=1400):
    rows = []
    start_date = datetime(1995, 1, 1)
    end_date = datetime(2025, 12, 31)
    span_days = (end_date - start_date).days

    for i in range(1, n + 1):
        state = random.choice(list(STATE_BOUNDS.keys()))
        lat_min, lat_max, lon_min, lon_max = STATE_BOUNDS[state]
        report_date = start_date + timedelta(days=random.randint(0, span_days))
        duration_seconds = random.choice([5, 10, 30, 60, 120, 300, 600, 1800, 3600])

        rows.append({
            "report_id": f"UFO{i:05d}",
            "report_date": report_date.strftime("%Y-%m-%d"),
            "year": report_date.year,
            "month": report_date.month,
            "state": state,
            "shape": random.choice(SHAPES),
            "duration_seconds": duration_seconds,
            "latitude": round(random.uniform(lat_min, lat_max), 4),
            "longitude": round(random.uniform(lon_min, lon_max), 4),
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
        OUTPUT_DIR / "ufo_sightings.csv",
        ["report_id", "report_date", "year", "month", "state", "shape",
         "duration_seconds", "latitude", "longitude"],
    )
