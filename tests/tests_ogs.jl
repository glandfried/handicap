include("../software/ttt.jl/src/TrueSkill.jl")
using .TrueSkill
include("../estimations/main.jl")
global ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames

println("Leyendo csv")
data = read_data("../../ogs-ii/data/archivos/sin_repetidos.csv")

println("Seteando argumentos")
days, results = set_arguments(data)
model = "h-kreg"

println("Calculando modelo")
lc, evidence, dict = lc_evidence(data, days, results, model, base)
println("Evidence h-kreg: ")
println(evidence)

println("Generando csv de salida")
generate_csv("output/aago_ttt-h-kreg.csv", dict, lc)
