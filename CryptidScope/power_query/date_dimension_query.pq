// Power Query (M) — Date dimension table
// A single shared Date table, marked as the Date Table in Power BI's model
// view, so both sightings tables filter against one calendar rather than
// each table bringing its own disconnected date column.

let
    StartDate = #date(1995, 1, 1),
    EndDate = #date(2025, 12, 31),
    DayCount = Duration.Days(EndDate - StartDate) + 1,
    DateList = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
    ToTable = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}),
    TypedDate = Table.TransformColumnTypes(ToTable, {{"Date", type date}}),

    AddYear = Table.AddColumn(TypedDate, "Year", each Date.Year([Date]), Int64.Type),
    AddMonthNum = Table.AddColumn(AddYear, "MonthNumber", each Date.Month([Date]), Int64.Type),
    AddMonthName = Table.AddColumn(AddMonthNum, "MonthName", each Date.ToText([Date], "MMMM"), type text),
    AddQuarter = Table.AddColumn(AddMonthName, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    AddYearMonth = Table.AddColumn(AddQuarter, "YearMonth", each Date.ToText([Date], "yyyy-MM"), type text)
in
    AddYearMonth
