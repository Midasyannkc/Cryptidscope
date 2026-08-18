# CryptidScope

A Power BI dashboard analyzing Bigfoot and UFO sighting patterns across the
United States, 1995–2025. Built to answer one question: do the two datasets
show any geographic or temporal overlap, or are they independent noise?

## What's in this repo

Power BI's `.pbix` file format is a binary format only Power BI Desktop can
compile. This repo contains everything that goes *into* the `.pbix` as
plain, reviewable code and data, plus exact instructions to assemble it:

```
data/                          synthetic source CSVs (generated, not committed)
data_generation_bigfoot.py     generates data/bigfoot_sightings.csv
data_generation_ufo.py         generates data/ufo_sightings.csv
power_query/                   M code for each Power Query source query
dax/measures.dax               every DAX measure in the report
docs/data_model.md             table relationships and modeling decisions
```

## Building the .pbix locally

1. `pip install -r requirements.txt` (just needs the Python standard library, no extra deps)
2. Run `python3 data_generation_bigfoot.py` and `python3 data_generation_ufo.py` to produce the CSVs in `data/`
3. Open Power BI Desktop → Get Data → Text/CSV → load both CSVs
4. For each load, open Power Query Editor → Advanced Editor, and paste in the matching query from `power_query/` in place of the auto-generated steps
5. Add a blank query for the Date dimension, paste in `power_query/date_dimension_query.pq`
6. In Model view, mark `Date` as the official Date Table (Table tools → Mark as Date Table), then draw the two relationships described in `docs/data_model.md`
7. Add a blank table named `_Measures`, then paste each measure from `dax/measures.dax` in individually (Power BI doesn't support pasting multiple measures as a batch)
8. Build visuals against the measures: a map visual for geographic concentration, a line chart using the YoY measures for trend, and a matrix using `Sightings Correlation Index` sliced by state

## Key decisions

- **One shared Date table, not two.** Both fact tables have their own date column, but only one is marked as the model's official Date Table. This is what lets a single year slicer filter both datasets together and is required for `SAMEPERIODLASTYEAR` and the other time-intelligence measures to work at all.
- **Bigfoot and UFO stay as separate fact tables.** They could be unioned into one table with a `sighting_type` column (both source queries already produce that column to make this possible later), but forcing them together now would mean a wide table full of nulls, since `classification`/`witness_count` and `shape`/`duration_seconds` don't overlap. Full reasoning in `docs/data_model.md`.
- **Classification labels and duration bands are computed in Power Query, not DAX.** Both are static per-row values that don't change with filter context, so computing them once at load time is cheaper than recalculating them in a measure on every visual render.
- **`Sightings Correlation Index` is the actual "find a pattern" answer.** It compares each state's share of national Bigfoot sightings to its share of national UFO sightings, so a value near 1 means a state is proportionally busy (or quiet) for both, and a value far from 1 means the two are diverging, the closest thing this dataset has to a real finding.

## Stack

Power BI Desktop, Power Query (M), DAX, Python (synthetic data generation).
