include("../software/ttt.jl/src/TrueSkill.jl")
using .TrueSkill
global ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames
using ArgParse

#TODO:
#   - armar tests
#   - definir events_weights para los demás modelos
#   - funciones que armen figuras (en pdf)

function parse_commandline()
    s = ArgParseSettings()
    @add_arg_table s begin
        "--source", "-s"
            help = "La base de datos a ser usada. Puede ser 'ogs', 'kgs', 'aago', o la dirección del archivo"
        "--model", "-m"
            help = "El modelo a ser aplicado. Puede ser 'all', 'ttt', 'ttt-h' " #definir abreviaciones (e.g. ttt, ttt-h, etc.)
            required = true
    end
    return parse_args(s)
end

function read_data(args)
    data = CSV.read(source, DataFrame)
    data
end

function get_days(data)
    days = Dates.value.(data.started .- Date("2001-01-01"))
    days
end

function init_priors(data)
    prior_dict = Dict{String,ttt.Player}()
    for h_key in Set([(row.handicap, row.width) for row in eachrow(data) ])
        prior_dict[string(h_key)] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
    end
    prior_dict
end

function get_results(data)
    results = [row.black_win == 1 ? [0.,1.] : [1., 0.] for row in eachrow(data) ]
    results
end

function events_weights(data, model)

    if model == "ttt-h"
        events = [ [[string(r.white)], r.handicap<2 ? [string(r.black)] : [string(r.black),string((r.handicap,r.width))] ] for r in eachrow(data) ]
        weights = [ [[1.0], r.handicap<2 ? [1.0] : [1.0,1.0] ] for r in eachrow(data) ] #neutro
    end
    return events, weights
end

function lc_evidence(data, days, prior_dict, results, sigma, gamma, iterations, model)

    events, weights = events_weights(data, model)

    h = missing
    GC.gc()
    h = ttt.History(composition=events, results=results, times = days , priors=prior_dict, sigma=sigma,gamma=gamma)
    ttt.convergence(h, epsilon=0.01, iterations=iterations)
    ttt_log_evidence = ttt.log_evidence(h)
    lc = ttt.learning_curves(h)

    return lc, ttt_log_evidence
end

function generate_csv(output, prior_dict, lc)
    df = DataFrame(id = String[], mu = Float64[], sigma = Float64[])
    for (k,v) in prior_dict
        if haskey(lc,k)
            N = lc[k][end][2]
            push!(df,[k,N.mu,N.sigma])
        end
    end
    CSV.write(output, df; header=true)
end

args = parse_commandline()

if args["source"] == "ogs"
    source = "../data/ogs/summary_filtered.csv"
elseif args["source"] == "kgs"
    source = "../data/kgs/KGS_filtered.csv"
elseif args["source"] == "aago"
    source = "../data/aago/aago.csv"
else
    source = args["source"]
end

data = read_data(source)
days = get_days(data)
prior_dict = init_priors(data)
results = get_results(data)

sigma = 6.0
gamma = 0.16
iterations = 16
model = args["model"]
lc, evidence = lc_evidence(data, days, prior_dict, results, sigma, gamma, iterations, model)
generate_csv("output/ogs_ttt-h.csv", prior_dict, lc)


##############################################################################

println("Opening dataset")
data = CSV.read(source, DataFrame)

# days = Dates.value.(
#     Date.(map(m->m.match,
#         match.(r"(\d+)-(\d+)-(\d+)", data.started))
#         ) .- Date("1900-01-01"))
days = Dates.value.(data.started .- Date("2001-01-01"))

prior_dict = Dict{String,ttt.Player}()
for h_key in Set([(row.handicap, row.width) for row in eachrow(data) ])
    prior_dict[string(h_key)] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
end

results = [row.black_win == 1 ? [0.,1.] : [1., 0.] for row in eachrow(data) ]

# sigma = 10.; gamma = 0.12; iter 4; -193062.34822408648
# sigma = 6.; gamma = 0.16; iter 4; -192006.29855472202 (0.6287623)
# sigma = 6.; gamma = 0.16; iter 16; -191501.00772558292
# sigma = 10; gamma = 0.16; iter 16: -192364.54726513493
# sigma = 10.; gamma = 0.18; iter 4; -192991.47740192755

events = [ r.handicap<2 ? [[string(r.white)],[string(r.black)]] : [[string(r.white)],[string(r.black),string((r.handicap,r.width))]] for r in eachrow(data) ]

h = missing
GC.gc()
h = ttt.History(composition=events, results=results, times = days , priors=prior_dict, sigma=6.0,gamma=0.16)
ts_log_evidence = ttt.log_evidence(h)
ttt.convergence(h, epsilon=0.01, iterations=16)
ttt_log_evidence = ttt.log_evidence(h)
println("Evidencia con handicap:")
println(ttt_log_evidence)

lc = ttt.learning_curves(h)

df = DataFrame(id = String[], mu = Float64[], sigma = Float64[])
for (k,v) in prior_dict
    if haskey(lc,k)
        N = lc[k][end][2]
        push!(df,[k,N.mu,N.sigma])
    end
end

CSV.write("output/ogs_ttt-h.csv", df; header=true)

#######################################
# Komi linear regression (BIEN CALCULADO: un factor por cada tipo de tablero)

prior_dict = Dict{String,ttt.Player}()
for h_key in Set([(row.handicap, row.width) for row in eachrow(data) ])
    prior_dict[string(h_key)] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
end
prior_dict["_komi9_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi9_0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi13_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi13_0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi19_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi19_0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)

function k0(w)
    return w==9 ? "_komi9_0_" : (w==13 ?  "_komi13_0_" : "_komi19_0_")
end
function k1(w)
    return w==9 ? "_komi9_1_" : (w==13 ?  "_komi13_1_" : "_komi19_1_")
end

# Sin filtro
events = [ [[string(r.white), k1(r.width), k0(r.width)], r.handicap<2 ? [string(r.black)] : [string(r.black),string((r.handicap,r.width))]] for r in eachrow(data) ]

weights = [ [[1.0, r.komi, 1.0], r.handicap<2 ? [1.0] :[1.0,1.0] ] for r in eachrow(data) ]

h = missing
GC.gc()
h = ttt.History(composition=events, results=results, times = days , priors=prior_dict, sigma=6.0,gamma=0.16,weights=weights)
ttt.convergence(h, iterations=16)
ttt.log_evidence(h) # iter 16: -191178 iter 10: -191341;  iter 4: -192285
exp(ttt.log_evidence(h)/length(h)) # iter 16: 0.63002099; iter 10: 0.62977333; iter 4: 0.628339033

lc = ttt.learning_curves(h)
if false
    lc["_komi19_0_"][end][2]
    6.5*lc["_komi19_1_"][end][2]
    7.5*lc["_komi19_1_"][end][2]
    10.5*lc["_komi19_1_"][end][2] # 10.5 La equivalencia en 19

    lc["_komi13_0_"][end][2] # UN EFECTO MUY GRANDE
    6.5*lc["_komi13_1_"][end][2] # 6.5 La equivalencia en 13
    7.5*lc["_komi13_1_"][end][2]

    lc["_komi9_0_"][end][2] # Apenas duplica el efecto de 19
    5.5*lc["_komi9_1_"][end][2] # 5.5 La equivalencia en 9
    6.5*lc["_komi9_1_"][end][2]
    7.5*lc["_komi9_1_"][end][2]
end

df = DataFrame(id = String[], mu = Float64[], sigma = Float64[])
for (k,v) in prior_dict
    if haskey(lc,k)
        N = lc[k][end][2]
        push!(df,[k,N.mu,N.sigma])
    end
end

CSV.write("output/ogs_ttt-h-komi-regression.csv", df; header=true)

#######################################
# Handicap y Komi linear regression

prior_dict = Dict{String,ttt.Player}()
prior_dict["_komi9_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi9_0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi13_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi13_0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi19_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi19_0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap9_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap13_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap19_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)

events = [ [[string(r.white), k0(r.width), k1(r.width)],[string(r.black), r.width==9 ? "_handicap9_1_" : (r.width==13 ?  "_handicap13_1_" : "_handicap19_1_") ]] for r in eachrow(data) ]
weights = [[[1.0, 1.0, r.komi],[1.0,  r.handicap ]] for r in eachrow(data) ]

h = missing
GC.gc()
h = ttt.History(composition=events, results=results, times = days , priors=prior_dict, sigma=6.0,gamma=0.16,weights=weights)
ttt.convergence(h, iterations=16)
ttt.log_evidence(h) # Iter 16 -191218;

lc = ttt.learning_curves(h)
if false
    lc["_komi9_0_"][end][2]
    5.5*lc["_komi9_1_"][end][2]
    6.5*lc["_komi9_1_"][end][2]

    lc["_komi13_0_"][end][2]
    5.5*lc["_komi13_1_"][end][2]
    6.5*lc["_komi13_1_"][end][2]
    7.5*lc["_komi13_1_"][end][2]

    lc["_komi19_0_"][end][2]
    6.5*lc["_komi19_1_"][end][2]
    7.5*lc["_komi19_1_"][end][2]
    10.5*lc["_komi19_1_"][end][2]
end

df = DataFrame(id = String[], mu = Float64[], sigma = Float64[])
for (k,v) in prior_dict
    if haskey(lc,k)
        N = lc[k][end][2]
        push!(df,[k,N.mu,N.sigma])
    end
end

CSV.write("output/ogs_ttt-h_regression-komi-regression.csv", df; header=true)

#######################################
# Komi a lo bestia

prior_dict = Dict{String,ttt.Player}()
for h_key in Set([(row.handicap, row.width) for row in eachrow(data) ])
    prior_dict[string(h_key)] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
end
for h_key in Set([(row.komi, row.width) for row in eachrow(data) ])
    prior_dict[string(h_key)] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
end

events = [ r.handicap<2 ? [[string(r.white), string((r.komi,r.width))],[string(r.black)]] : [[string(r.white), string((r.komi,r.width))],[string(r.black),string((r.handicap,r.width))]] for r in eachrow(data) ]

# Komi; sigma = 6.0; gamma = 0.14; iter 4; -191779.79446627648
# Komi; sigma = 6.0; gamma = 0.16; iter 4; -191788.50468685792; 0.62909338
# Komi; sigma = 6.0; gamma = 0.18; iter 4; -191966.61722868486

for gamma in [0.16]#gamma = 0.16
    h = missing
    GC.gc()
    h = ttt.History(composition=events, results=results, times = days , priors=prior_dict, sigma=6.0,gamma=gamma)
    ts_log_evidence = ttt.log_evidence(h)
    ttt.convergence(h, iterations=16)
    ttt_log_evidence = ttt.log_evidence(h) # Iter 16 -191294
    println("Gamma:")
    println(gamma)
    println("Evidencia con handicap y komi:")
    println(ttt_log_evidence, ", ", exp(ttt_log_evidence/length(h)))
end

lc = ttt.learning_curves(h)
if false
    lc["(0.5, 19)"][end][2]
    lc["(5.5, 19)"][end][2]
    lc["(6.5, 19)"][end][2]
    lc["(7.5, 19)"][end][2]
    lc["(9.5, 19)"][end][2]

    lc["(0.5, 13)"][end][2]
    lc["(5.5, 13)"][end][2]
    lc["(6.5, 13)"][end][2]

    lc["(0.5, 9)"][end][2]
    lc["(5.5, 9)"][end][2]
    lc["(6.5, 9)"][end][2]
    lc["(7.5, 9)"][end][2]

    lc["(2, 19)"][end][2]
    lc["(2, 9)"][end][2]
end

df = DataFrame(id = String[], mu = Float64[], sigma = Float64[])
for (k,v) in prior_dict
    if haskey(lc,k)
        N = lc[k][end][2]
        push!(df,[k,N.mu,N.sigma])
    end
end

CSV.write("output/ogs_ttt-h-k.csv", df; header=true)
