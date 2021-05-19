include("../software/ttt.jl/src/TrueSkill.jl")
using .TrueSkill
global const ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames

println("Opening dataset")
data = CSV.read("../data/ogs/summary_filtered.csv")    

days = Dates.value.(
    Date.(map(m->m.match,
        match.(r"(\d+)-(\d+)-(\d+)", data.started))
        ) .- Date("1900-01-01"))

prior_dict = Dict{String,ttt.Player}()
for h_key in Set([(row.handicap, row.width) for row in eachrow(data) ])
    prior_dict[string(h_key)] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
end

results = [row.black_win == 1 ? [0.,1.] : [1., 0.] for row in eachrow(data) ]

events = [ r.handicap<2 ? [[string(r.white)],[string(r.black)]] : [[string(r.white)],[string(r.black),string((r.handicap,r.width))]] for r in eachrow(data) ]   

# gamma = 0.12; iter 4; -193062.34822408648
# gamma = 0.16; iter 4; -192830.49964918988
# gamma = 0.18; iter 4; -192991.47740192755

h = missing 
GC.gc()
h = ttt.History(composition=events, results=results, times = days , priors=prior_dict, sigma=10.,gamma=0.18)
ts_log_evidence = ttt.log_evidence(h)
ttt.convergence(h, iterations=4)
ttt_log_evidence = ttt.log_evidence(h)

lc = ttt.learning_curves(h)

for (k,v) in prior_dict
    if haskey(lc,k)
        println(k,lc[k][end][2])
    end
end    


for h_key in Set([(row.komi, row.width) for row in eachrow(data) ])
    prior_dict[string(h_key)] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
end

events = [ r.handicap<2 ? [[string(r.white), string((r.komi,r.width))],[string(r.black)]] : [[string(r.white), string((r.komi,r.width))],[string(r.black),string((r.handicap,r.width))]] for r in eachrow(data) ]   


# Komi; gamma = 0.16; iter 4; -192684

h = missing 
GC.gc()
h = ttt.History(composition=events, results=results, times = days , priors=prior_dict, sigma=10.,gamma=0.16)
ts_log_evidence = ttt.log_evidence(h)
ttt.convergence(h, iterations=4)
ttt_log_evidence = ttt.log_evidence(h)

lc = ttt.learning_curves(h)
lc["(30.0, 19)"][end][2] 
