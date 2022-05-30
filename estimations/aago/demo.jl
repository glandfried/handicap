include("../../software/ttt.jl/src/TrueSkill.jl")
using .TrueSkill
global ttt = TrueSkill
include("../main.jl")
using CSV
using JLD2
using Dates
using DataFrames

# curva de aprendizaje de 10 jugadores
base = "aago"
data = read_data("../../data/aago/aago_filtered.csv")
days, results = set_arguments(data)
model = "hreg-kreg"
lc, evidence, dict = lc_evidence(data, days, results, model, base)
#
# print(dict)
# println("-----------------------------------")
# print(lc)
lc_df = DataFrame(id=String[], day=Int[], mu=Float64[], sigma=Float64[])

for (jugador, evolucion) in lc
    for estimacion in evolucion
        push!(lc_df, (jugador, estimacion[1], estimacion[2].mu, estimacion[2].sigma))
    end
end
#
# CSV.write("./output_demo/dict.csv", dict)
CSV.write("./output_demo/lc2.csv", lc_df)
# open("./output_demo/dict2.csv", "w") do file
#     write(file, dict)
# end
#
# open("./output_demo/lc2.csv", "w") do file
#     write(file, lc)
# end
#

#
