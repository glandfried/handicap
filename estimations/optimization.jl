include("../software/ttt.jl/src/TrueSkill.jl")
using .TrueSkill
include("./main.jl")
global ttt = TrueSkill
using CSV
using JLD2
using Dates
using DataFrames
using Optim

function objective(gamma, data, days, results, model)
    prior_dict = init_priors(data, model)
    events, weights = events_weights(data, model)
    sigma = 6.0
    iterations = 16

    lc, evidence, dict = run_and_converge(events, results, days, prior_dict, sigma, gamma, iterations, weights, model)
    println("Gamma:")
    println(gamma)
    println(-evidence)
    return (-evidence) #porque minimizo
end

data = read_data("../data/aago/aago_filtered.csv")
days, results = set_arguments(data)
model = "hreg-kreg"
result = optimize(g->objective(g, data, days, results, model), 0.0, 5.0)
println(result)
println("El mejor gamma es:")
min = Optim.minimizer(result)
println(min)


prior_dict = init_priors(data, model)
events, weights = events_weights(data, model)
sigma = 6.0
iterations = 16

lc, evidence, dict = run_and_converge(events, results, days, prior_dict, sigma, min, iterations, weights, model)
generate_csv("lc_aago_ttt-hreg-kreg.csv", prior_dict, lc)

df = DataFrame(player = String[], time = Int64[], mu = Float64[], sigma = Float64[])
for (time, skill) in lc["222"]
    push!(df,("222", time, skill.mu, skill.sigma))
end
for (time, skill) in lc["176"]
    push!(df,("176", time, skill.mu, skill.sigma))
end
for (time, skill) in lc["218"]
    push!(df,("218", time, skill.mu, skill.sigma))
end
CSV.write("lc_players.csv", df; header=true)