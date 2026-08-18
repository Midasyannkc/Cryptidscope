# CryptidScope — Data Model

## Tables

| Table | Grain | Role |
|---|---|---|
| `Bigfoot Sightings` | one row per reported sighting | Fact table |
| `UFO Sightings` | one row per reported sighting | Fact table |
| `Date` | one row per calendar day, 1995–2025 | Shared dimension, marked as the model's Date Table |
| `_Measures` | no rows (blank table) | Holds all DAX measures, kept separate from fact tables |

## Relationships

```
Date[Date]  1 ──────< * [report_date]  Bigfoot Sightings
Date[Date]  1 ──────< * [report_date]  UFO Sightings
```

Both relationships are single-direction (Date filters the fact tables, not
the reverse), which is the standard star-schema pattern and avoids the
ambiguous-filter-path warnings that come from marking both directions active
on two fact tables sharing one dimension.

## Why one shared Date table instead of two

Bigfoot Sightings and UFO Sightings each have their own `report_date`
column, and it would be simpler to just use each table's own date field
directly in visuals. The reason not to: a shared Date table is what makes a
single slicer ("Year: 2020") filter *both* fact tables consistently, and
it's what makes `SAMEPERIODLASTYEAR` and other time-intelligence DAX
functions work correctly. Two independent, unmarked date columns would
require two separate slicers and would break every time-intelligence
measure in this file.

## Why Bigfoot and UFO are separate fact tables, not one combined table

They could be unioned into a single "Sightings" table with a `sighting_type`
discriminator column (both source queries already produce that column,
specifically to make this optional later). They're kept separate here
because the two datasets have genuinely different attributes.
Bigfoot has `classification` and `witness_count`; UFO has `shape` and
`duration_seconds`. Forcing them into one table means either a wide table
full of nulls (Bigfoot rows with empty `shape`, UFO rows with empty
`classification`) or losing those source-specific fields entirely. Keeping
them separate, joined only through the shared Date table, preserves both
datasets' real structure while still allowing cross-dataset comparison
through measures like `Sightings Correlation Index`.
