using CSV
using DataFrames

kgs = CSV.read("../data/kgs/KGS.csv", DataFrame)
ogs = CSV.read("../data/ogs/summary_filtered.csv", DataFrame)
puente = CSV.read("../data/aago/aago_kgs_ogs.csv", DataFrame)

#names(kgs)

kgs = dropmissing(kgs, :white)
kgs = dropmissing(kgs, :black)

i = 28
sum(puente[i,"KGS"] .== kgs.white) + sum(puente[i,"KGS"] .== kgs.black)

for i in 1:28
    println(sum(puente[i,"OGS"] .== ogs.white) + sum(puente[i,"OGS"] .== ogs.black))
end
