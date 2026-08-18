// Power Query (M) — UFO Sightings source query

let
    Source = Csv.Document(
        File.Contents("C:\CryptidScope\data\ufo_sightings.csv"),
        [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),

    TypedColumns = Table.TransformColumnTypes(PromotedHeaders, {
        {"report_id", type text},
        {"report_date", type date},
        {"year", Int64.Type},
        {"month", Int64.Type},
        {"state", type text},
        {"shape", type text},
        {"duration_seconds", Int64.Type},
        {"latitude", type number},
        {"longitude", type number}
    }),

    // Bucketing duration into a readable band at ingestion time, not in a
    // DAX measure, since this value doesn't change per filter context --
    // computing it once in Power Query is cheaper than recomputing it on
    // every visual render.
    AddDurationBand = Table.AddColumn(TypedColumns, "duration_band", each
        if [duration_seconds] <= 30 then "Under 30 sec"
        else if [duration_seconds] <= 300 then "30 sec - 5 min"
        else if [duration_seconds] <= 1800 then "5 - 30 min"
        else "Over 30 min",
        type text
    ),

    AddSourceType = Table.AddColumn(AddDurationBand, "sighting_type", each "UFO", type text)
in
    AddSourceType
