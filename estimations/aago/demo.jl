include("../../software/ttt.jl/src/TrueSkill.jl")
using .TrueSkill
global ttt = TrueSkill
include("../main.jl")
using CSV
using JLD2
using Dates
using DataFrames

base = "aago"
data = read_data("../../data/aago/aago_filtered.csv")
days, results = set_arguments(data)
model = "hreg-kreg"
lc, evidence, dict = lc_evidence(data, days, results, model, base)
print(lc)

lc_df = DataFrame(id=String[], day=Int[], mu=Float64[], sigma=Float64[])

for (jugador, evolucion) in lc
    for estimacion in evolucion
        push!(lc_df, (jugador, estimacion[1], estimacion[2].mu, estimacion[2].sigma))
    end
end

# CSV.write("./output_demo/dict.csv", dict)
CSV.write("./output_demo/lc2.csv", lc_df)


laplagne_id = "7" #Santiago Laplagne
gutierrez_id = "13" #Agustin Santiago Gutierrez

lc_laplagne = lc[laplagne_id]
lc_gutierrez = lc[gutierrez_id]

#el primer día es 5656 para ambos, el ultimo 7055
#cantidad de partidas: laplagne 112, gut 65
compare_dict = Dict()
last_laplagne = lc_laplagne[1][2]
last_gutierrez = lc_gutierrez[1][2]
beta = 0.0
i = 1
j = 1

while (i<112 && j<65)
    global i
    global j
    global last_laplagne
    global last_gutierrez
    if lc_laplagne[i][1] < lc_gutierrez[j][1] #si el prox partido es de laplagne
        day = lc_laplagne[i][1]
        last_laplagne = lc_laplagne[i][2]
        i = min(i + 1, 112)
    elseif lc_laplagne[i][1] > lc_gutierrez[j][1]
        day = lc_gutierrez[j][1]
        last_gutierrez = lc_gutierrez[j][2]
        j = min(j + 1, 65)
    else
        day = lc_gutierrez[j][1]
        last_laplagne = lc_laplagne[i][2]
        i = min(i + 1, 112)
        last_gutierrez = lc_gutierrez[j][2]
        j = min(j + 1, 65)
    end
    win_prob = ttt.cdf(last_gutierrez - last_laplagne, -beta) #prob de ganar de laplagne
    compare_dict[day] = win_prob
end
CSV.write("./output_demo/compare_dict.csv", compare_dict)
