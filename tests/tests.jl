include("../software/ttt.jl/src/TrueSkill.jl")
using .TrueSkill
include("../estimations/main.jl")
global ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames

data = read_data("../data/ogs/summary_filtered.csv")
println("Data loaded")

days = get_days(data)
prior_dict = init_priors(data)
results = get_results(data)
sigma = 6.0
gamma = 0.16
iterations = 16
model = "h"
println("Arguments setted")

lc, evidence = lc_evidence(data, days, prior_dict, results, sigma, gamma, iterations, model)
println("Evidence: ")
println(evidence)

#generate_csv("output/ogs_ttt-h.csv", prior_dict, lc)
