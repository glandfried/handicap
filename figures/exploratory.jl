using CSV
using DataFrames
using VegaLite

count(col) = (df -> combine(groupby(df, [col]), nrow => :count))
barplot(col,category=:quantitative) = (df ->
    df |> count(col) |>
    @vlplot(x=:count, y={col, type=category}) + @vlplot(mark=:bar) + @vlplot(mark={:text, align=:left, dx=4}, text=:count))
logbarplot(col,category=:quantitative) = (df ->
    df |> count(col) |>
    @vlplot(x={:count, scale={type="log",base=10}}, y={col, type=category}) + @vlplot(mark=:bar) + @vlplot(mark={:text, align=:left, dx=4}, text=:count))
verticallogbarplot(col,category=:quantitative) = (df -> 
    df |> count(col) |>
    @vlplot(:bar, x={col, type=category}, y={:count, scale={type="log",base=10}}))
heatmap(x,y) = @vlplot(x=x, y=y) + @vlplot(:rect, width={step=40}, height={step=40}, color={"count()", scale={range=["#610066", "#E6DF17"]}}) + @vlplot(mark={:text, color=:white}, text="count()")
savepdf(filename) = save(filename*".pdf")

function aagoplots()
    aago = DataFrame(CSV.File("../data/aago/aago.csv"))
    aago |> barplot(komi, :ordinal) |> savepdf("aago/komi")
    aago |> barplot(handicap, :ordinal) |> savepdf("aago/handicap")
    aago |> heatmap("komi:o", "handicap:o") |> savepdf("aago/komi-by-handicap")

    aago |> barplot(:reason) |> savepdf("aago/reason")

    aago |> barplot(:result) |> savepdf("aago/result")
    aago |> heatmap(:result, :reason) |> savepdf("aago/result-by-reason")
end
function ogsplots()
    columns = ["order", "handicap", "komi", "rules", "annulled", "ranked", "outcome"]
    ogs = DataFrame(CSV.File("../data/ogs/summary.csv";select=columns))
    filters = (0 .<= ogs.handicap .<= 9) .& (.! ogs.annulled) .& ((ogs.order .== "(1, 0)") .| (ogs.order .== "(0, 1)"))
    ogs = ogs[filters, :]
    ogs |> verticallogbarplot(:komi) |> savepdf("ogs/komi")
    ogs |> logbarplot(:handicap, :ordinal) |> savepdf("ogs/handicap")
end

function kgsplots()
    kgs = CSV.read("../data/kgs/KGS.csv", DataFrame)
end

aagoplots()
GC.gc()
ogsplots()
GC.gc()
kgsplots()
