// Power Query (M) — Bigfoot Sightings source query
// Paste into Power BI Desktop: Home > Transform Data > New Source > Blank Query,
// then open Advanced Editor and replace with this.

let
    Source = Csv.Document(
        File.Contents("C:\CryptidScope\data\bigfoot_sightings.csv"),
        [Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),

    // Explicit typing rather than relying on auto-detect -- auto-detect
    // misreads report_id (e.g. "BF00001") as a truncated number on a fresh
    // load, which silently corrupts the join key against other tables.
    TypedColumns = Table.TransformColumnTypes(PromotedHeaders, {
        {"report_id", type text},
        {"report_date", type date},
        {"year", Int64.Type},
        {"month", Int64.Type},
        {"state", type text},
        {"classification", type text},
        {"latitude", type number},
        {"longitude", type number},
        {"conditions", type text},
        {"environment", type text},
        {"witness_count", Int64.Type}
    }),

    // Classification is a single letter (A/B/C) in the source. Expanding it
    // to a readable label here, once, means every visual and tooltip in the
    // report shows the same wording instead of each visual re-implementing
    // its own lookup or switch statement.
    AddClassificationLabel = Table.AddColumn(TypedColumns, "ClassificationLabel", each
        if [classification] = "A" then "A - Clear Sighting"
        else if [classification] = "B" then "B - Possible Sighting"
        else "C - Unverified Report",
        type text
    ),

    // A dedicated cryptid_type column, hardcoded here rather than inferred,
    // exists so this table can be appended to the UFO table later (Append
    // Queries) if a combined "all sightings" view is ever needed -- the
    // discriminator column has to already exist before the append, not be
    // patched in afterward.
    AddSourceType = Table.AddColumn(AddClassificationLabel, "sighting_type", each "Bigfoot", type text)
in
    AddSourceType
