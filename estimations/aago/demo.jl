include("../software/ttt.jl/src/TrueSkill.jl")
using .TrueSkill
global ttt = TrueSkill
include("../main.jl")
using CSV
using JLD2
using Dates
using DataFrames

# curva de aprendizaje de 10 jugadores

#
