include("../software/ttt.jl/src/TrueSkill.jl")
using .TrueSkill
global ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames

println("Opening dataset")
data = CSV.read("../data/aago/aago.csv", DataFrame)

# Index
# 1. Base (0.5689183462323528)
# 2. Handicap
# 3. Handicap and komi (0.5891943624123013)

days = Dates.value.(data.date .- Date("2001-01-01"))
results = [ r.result .== "black" ? [1.0,0.0] : [0.0,1.0]  for r in eachrow(data)]

# 1. Base

composition_base = [ [[string(r.black_player_id)],[string(r.white_player_id)]] for r in eachrow(data)]

h_base = ttt.History(composition=composition_base, results=results, times=days)
ttt.convergence(h_base, iterations=16)
exp(ttt.log_evidence(h_base)/length(h_base))

# 2. Handicap

handicaps = Set([r.handicap for r in eachrow(data)])
priors = Dict{String,ttt.Player}()
for h in handicaps
    priors["handicap"*string(h)] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
end

# 3. Handicap y Komi

priors["komi0"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
priors["komi6"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)

composition_HK = [ [[string(r.black_player_id), "handicap"*string(r.handicap)],[string(r.white_player_id), r.komi == 0.5 ? "komi0" : "komi6"]] for r in eachrow(data)]

h_HK =  ttt.History(composition=composition_HK, results=results, times=days)
ttt.convergence(h_HK, iterations=16)
exp(ttt.log_evidence(h_HK)/length(h_HK))

lc = ttt.learning_curves(h_HK)

Set(data.komi)

if false
    lc["komi6"][end][2]
    lc["komi0"][end][2]
    lc["handicap2"][end][2]
    lc["handicap3"][end][2]
    lc["handicap4"][end][2]
end


