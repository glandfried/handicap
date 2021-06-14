using CSV
using DataFrames
using VegaLite

aago = CSV.read("../data/aago/aago.csv", DataFrame)
ogs = CSV.read("../data/ogs/summary.csv", DataFrame)[!, ["order", "handicap", "komi", "rules", "annulled", "ranked", "outcome"]]
kgs = CSV.read("../data/kgs/KGS.csv", DataFrame)

count(col) = (df -> combine(groupby(df, [col]), nrow => :count))
barplot(x) = @vlplot(x="count()", y=x) + @vlplot(mark=:bar) + @vlplot(mark={:text, align=:left, dx=4}, text="count()")
logbarplot(x) = @vlplot(x={"count()", scale={type="log",base=10}}, y=x) + @vlplot(mark=:bar) + @vlplot(mark={:text, align=:left, dx=4}, text="count()")
verticallogbarplot(col) = (df -> 
    df |> count(col) |>
    @vlplot(:bar, x=col, y={:count, scale={type="log",base=10}}))
heatmap(x,y) = @vlplot(x=x, y=y) + @vlplot(:rect, width={step=40}, height={step=40}, color={"count()", scale={range=["#610066", "#E6DF17"]}}) + @vlplot(mark={:text, color=:white}, text="count()")
savepdf(filename) = save(filename*".pdf")

aago |> barplot("komi:o") |> savepdf("aago/komi")
aago |> barplot("handicap:o") |> savepdf("aago/handicap")
aago |> heatmap("komi:o", "handicap:o") |> savepdf("aago/komi-by-handicap")

aago |> barplot(:reason) |> savepdf("aago/reason")

aago |> barplot(:result) |> savepdf("aago/result")
aago |> heatmap(:result, :reason) |> savepdf("aago/result-by-reason")

ogs |> verticallogbarplot(:komi) |> savepdf("ogs/komi")
ogs |> verticallogbarplot(:handicap) |> savepdf("ogs/handicap")
