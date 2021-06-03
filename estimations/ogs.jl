include("../software/ttt.jl/src/TrueSkill.jl")
using .TrueSkill
global ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames

# Conclusiones:
#   1. El komi con regresion lineal mejora la estimaci'on.
#   2. La regresi'on c'ubica se rompe cuando los komis tienen beta = 0 y el jugador que recibe un komi de 30 pierde porque 30^3 = 2700, y la aproximación de la truncada se rompe porque tanto la densidad como la acumulada en el punto -2700 es 0.
#   3. Empeora cuando usamos regresi'on lineal para el handicap. Posibles razones:
#       a. Komi según tablero.
#       b. Quizás por demasida incertidumbre cuando la regresión se aleja del 0
#       c. Quizás poque existe una interferencia entre komi y handicap (por mala asignación)

#
# TODO:
#   1. Komi según tabllero
#   2. Analizar interacción entre komi y handicap

println("Opening dataset")
data = CSV.read("../data/ogs/summary_filtered.csv", DataFrame)

days = Dates.value.(
    Date.(map(m->m.match,
        match.(r"(\d+)-(\d+)-(\d+)", data.started))
        ) .- Date("1900-01-01"))

prior_dict = Dict{String,ttt.Player}()
for h_key in Set([(row.handicap, row.width) for row in eachrow(data) ])
    prior_dict[string(h_key)] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
end

results = [row.black_win == 1 ? [0.,1.] : [1., 0.] for row in eachrow(data) ]

# gamma = 0.12; iter 4; -193062.34822408648
# gamma = 0.16; iter 4; -192830.49964918988
# gamma = 0.18; iter 4; -192991.47740192755

events = [ r.handicap<2 ? [[string(r.white)],[string(r.black)]] : [[string(r.white)],[string(r.black),string((r.handicap,r.width))]] for r in eachrow(data) ]

h = missing
GC.gc()
h = ttt.History(composition=events, results=results, times = days , priors=prior_dict, sigma=6.0,gamma=0.16)
ts_log_evidence = ttt.log_evidence(h)
ttt.convergence(h, iterations=4)
ttt_log_evidence = ttt.log_evidence(h)
println("Evidencia con handicap:")
println(ttt_log_evidence)

lc = ttt.learning_curves(h)

for (k,v) in prior_dict
    if haskey(lc,k)
        println(k,lc[k][end][2])
    end
end

#######################################
# Komi linear regression

prior_dict["_komi3_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi2_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)

# prior_dict = Dict{String,Player}()
# for h_key in Set([(row.handicap, row.width) for row in eachrow(data) ])
#     prior_dict[string(h_key)] = Player(Gaussian(0.0,6.0),0.0,0.0)
# end
# prior_dict["_komi3_"] = Player(Gaussian(0.0,6.0),0.0,0.0)
# prior_dict["_komi2_"] = Player(Gaussian(0.0,6.0),0.0,0.0)
# prior_dict["_komi1_"] = Player(Gaussian(0.0,6.0),0.0,0.0)
# prior_dict["_komi0_"] = Player(Gaussian(0.0,6.0),0.0,0.0)
# 

# 1. Pendiente y ordenada al orgien

events = [ r.handicap<2 ? [[string(r.white), "_komi1_", "_komi0_"],[string(r.black)]] : [[string(r.white), "_komi1_", "_komi0_"],[string(r.black),string((r.handicap,r.width))]] for r in eachrow(data) ]

weights = [ r.handicap<2 ? [[1.0, r.komi, 1.0],[1.0]] : [[1.0, r.komi, 1.0],[1.0,1.0]] for r in eachrow(data) ]

h = missing
GC.gc()
h = ttt.History(composition=events, results=results, times = days , priors=prior_dict, sigma=6.0,gamma=0.16,weights=weights)
ttt.convergence(h, iterations=4)
ttt.log_evidence(h) # -191775.92380327423

lc = ttt.learning_curves(h)
lc["_komi0_"][end][2]
6.5*lc["_komi1_"][end][2]
7.5*lc["_komi1_"][end][2]

# 2. Cuadrática

events = [ r.handicap<2 ? [[string(r.white), "_komi2_", "_komi1_", "_komi0_"],[string(r.black)]] : [[string(r.white), "_komi2_", "_komi1_", "_komi0_"],[string(r.black),string((r.handicap,r.width))]] for r in eachrow(data) ]

weights = [ r.handicap<2 ? [[1.0, r.komi^2, r.komi, 1.0],[1.0]] : [[1.0, r.komi^2, r.komi, 1.0],[1.0,1.0]] for r in eachrow(data) ]

h = missing
GC.gc()
h = ttt.History(composition=events, results=results, times = days , priors=prior_dict, sigma=6.0,gamma=0.16,weights=weights)
ttt.convergence(h, iterations=4)
ttt.log_evidence(h) # -Inf

# 3. Cúbica
## SE ROMPE con gamma = 0 y beta = 0 

composition = [ r.handicap<2 ? [[string(r.white), "_komi3_", "_komi2_", "_komi1_", "_komi0_"],[string(r.black)]] : [[string(r.white), "_komi3_", "_komi2_", "_komi1_", "_komi0_"],[string(r.black),string((r.handicap,r.width))]] for r in eachrow(data) ]
times = days
weights = [ r.handicap<2 ? [[1.0, r.komi^3, r.komi^2, r.komi, 1.0],[1.0]] : [[1.0, r.komi^3, r.komi^2, r.komi, 1.0],[1.0,1.0]] for r in eachrow(data) ]
priors = prior_dict
gamma = 0.16; sigma=6.0; mu=0.0; beta=1.0; p_draw=0.0
online=false

h = missing
GC.gc()
h = ttt.History(composition=composition, results=results, times = times , priors=priors , sigma=6.0,gamma=0.16,weights=weights)
ttt.convergence(h, iterations=4)
ttt.log_evidence(h) # 

# events[5605], weights[5605]
# https://stackoverflow.com/questions/56229927/with-julias-debugger-jl-how-can-i-enter-debug-mode-similar-to-pythons-pdb-se

#######################################
# Handicap y Komi linear regression

prior_dict["_komi9_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi9_0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi13_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi13_0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi19_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_komi19_0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)

prior_dict = Dict{String,ttt.Player}()
prior_dict["_handicap9_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap13_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap19_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)


events = [ [[string(r.white), r.width==9 ? "_komi9_0_" : (r.width==13 ?  "_komi13_0_" : "_komi19_0_"), r.width==9 ? "_komi9_1_" : (r.width==13 ?  "_komi13_1_" : "_komi19_1_")],[string(r.black), r.width==9 ? "_handicap9_" : (r.width==13 ?  "_handicap13_" : "_handicap19_") ]] for r in eachrow(data) ]
weights = [[[1.0, 1.0, r.komi],[1.0,  r.handicap ]] for r in eachrow(data) ]

#events = [ r.handicap<2 ? [[string(r.white), "_komi1_", "_komi0_"],[string(r.black)]] : [[string(r.white), "_komi1_", "_komi0_"],[string(r.black), r.width==9 ? "_handicap9_" : (r.width==13 ?  "_handicap13_" : "_handicap19_") ]] for r in eachrow(data) 
#weights = [ r.handicap<2 ? [[1.0, r.komi, 1.0],[1.0]] : [[1.0, r.komi, 1.0],[1.0,  r.handicap ]] for r in eachrow(data) ]

h = missing
GC.gc()
h = ttt.History(composition=events, results=results, times = days , priors=prior_dict, sigma=6.0,gamma=0.16,weights=weights)
ttt.convergence(h, iterations=4)
ttt.log_evidence(h) # -195080.19750577759

lc = ttt.learning_curves(h)
lc["_komi9_0_"][end][2]
6.5*lc["_komi9_1_"][end][2]
7.5*lc["_komi9_1_"][end][2]

lc["_komi13_0_"][end][2]
6.5*lc["_komi13_1_"][end][2]
7.5*lc["_komi13_1_"][end][2]

lc["_komi19_0_"][end][2]
6.5*lc["_komi19_1_"][end][2]
7.5*lc["_komi19_1_"][end][2]


# ATENCI'ON!:
#   El efecto del komi es negativo.

2.0*lc["_handicap9_"][end][2]
2.0*lc["_handicap19_"][end][2]

# 3. Handicap cúbico
## SE ROMPE

prior_dict["_handicap9_0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap9_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap9_2_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap9_3_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)

prior_dict["_handicap13_0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap13_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap13_2_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap13_3_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)

prior_dict["_handicap19_0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap19_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap19_2_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
prior_dict["_handicap19_3_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)


events = [ [[string(r.white), r.width==9 ? "_komi9_0_" : (r.width==13 ?  "_komi13_0_" : "_komi19_0_"),  r.width==9 ? "_komi9_1_" : (r.width==13 ?  "_komi13_1_" : "_komi19_1_")],[string(r.black),r.width==9 ? "_handicap9_0_" : (r.width==13 ?  "_handicap13_0_" : "_handicap19_0_"),r.width==9 ? "_handicap9_1_" : (r.width==13 ?  "_handicap13_1_" : "_handicap19_1_"),r.width==9 ? "_handicap9_2_" : (r.width==13 ?  "_handicap13_2_" : "_handicap19_2_"), r.width==9 ? "_handicap9_3_" : (r.width==13 ?  "_handicap13_3_" : "_handicap19_3_") ]] for r in eachrow(data) ]
weights = [[[1.0, 1.0, r.komi],[1.0, 1.0, r.handicap, r.handicap^2, r.handicap^3]] for r in eachrow(data) ]

#events = [ r.handicap<2 ? [[string(r.white), "_komi1_", "_komi0_"],[string(r.black)]] : [[string(r.white), "_komi1_", "_komi0_"],[string(r.black), r.width==9 ? "_handicap9_" : (r.width==13 ?  "_handicap13_" : "_handicap19_") ]] for r in eachrow(data) 
#weights = [ r.handicap<2 ? [[1.0, r.komi, 1.0],[1.0]] : [[1.0, r.komi, 1.0],[1.0,  r.handicap ]] for r in eachrow(data) ]

h = missing
GC.gc()
h = ttt.History(composition=events, results=results, times = days , priors=prior_dict, sigma=6.0,gamma=0.16,weights=weights)
ttt.convergence(h, iterations=4)
ttt.log_evidence(h) # 

lc = ttt.learning_curves(h)
lc["_komi0_"][end][2]
6.5*lc["_komi1_"][end][2]
7.5*lc["_komi1_"][end][2]


#######################################
# Komi a lo besti

for h_key in Set([(row.komi, row.width) for row in eachrow(data) ])
    prior_dict[string(h_key)] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
end

events = [ r.handicap<2 ? [[string(r.white), string((r.komi,r.width))],[string(r.black)]] : [[string(r.white), string((r.komi,r.width))],[string(r.black),string((r.handicap,r.width))]] for r in eachrow(data) ]

# Komi; gamma = 0.14; iter 4; -192707
# Komi; gamma = 0.16; iter 4; -192684
# Komi; gamma = 0.18; iter 4; -192828

for gamma in [0.14, 0.16, 0.18]
    h = missing
    GC.gc()
    h = ttt.History(composition=events, results=results, times = days , priors=prior_dict, sigma=10.,gamma=gamma)
    ts_log_evidence = ttt.log_evidence(h)
    ttt.convergence(h, iterations=4)
    ttt_log_evidence = ttt.log_evidence(h)
    println("Gamma:")
    println(gamma)
    println("Evidencia con handicap y komi:")
    println(ttt_log_evidence)
end

lc = ttt.learning_curves(h)
lc["(30.0, 19)"][end][2]
