using CSV
using DataFrames
using VegaLite

df = CSV.read("../data/ogs/summary_filtered.csv", DataFrame)

handicap_count = combine(groupby(df, [:handicap]), nrow => :count)

plot_handicap_count = handicap_count |> @vlplot(
    mark=:bar,
    x=:handicap,
    y={:count},
)
save("./handicap-count.png", plot_handicap_count)

plot_handicap_count_log = handicap_count |> @vlplot(
    mark=:bar,
    x=:handicap,
    y={:count, scale={type="log",base=10}},
)
save("./handicap-count-log.png", plot_handicap_count_log)

komi_count = combine(groupby(df, [:komi]), nrow => :count)
make_plot_komi_count = @vlplot(
    width=500,
    height=500,
    mark=:bar,
    x=:komi,
    y={:count, scale={type="log",base=10}},
    tooltip=:komi,
)

plot_komi_count_log = komi_count |> make_plot_komi_count
save("./komi-count-log.png", plot_komi_count_log)

plot_komi_positive_count_log =
	filter(row -> row.komi >= 0, komi_count) |> make_plot_komi_count
save("./komi-positive-count-log.png", plot_komi_positive_count_log)
