using TrueSkillThroughTime
global ttt = TrueSkillThroughTime
include("./main.jl")
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

data = read_data("../data/aago/aago_original_filtered.csv")
days, results = set_arguments(data)
#model = "hreg-kreg"
#for model in ["h-k","h-kreg","hreg-kreg","h"]
for model in ["h", "h-k", "hreg", "hreg-kreg"]
    result = optimize(g->objective(g, data, days, results, model), 0.0, 5.0)
    println(result)
    println("El mejor gamma es:")
    min = Optim.minimizer(result)
    println(min)
    println("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
end
