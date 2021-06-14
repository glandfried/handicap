include("../software/ttt.jl/src/TrueSkill.jl")
using .TrueSkill
include("../estimations/main.jl")
global ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames

function compare_csv(csv1, csv2)
    df1 = CSV.read(csv1, DataFrame)
    df2 = CSV.read(csv2, DataFrame)

    df1 == df2
end

@testset "All" begin
    data = read_data("../data/aago/aago_filtered.csv")
    days, results = set_arguments(data)

    #### Handicap ###############

    model = "h"
    lc, evidence, dict = lc_evidence(data, days, results, model)
    println("Evidence h: ")
    println(evidence)

    generate_csv("output/aago_ttt-h.csv", dict, lc)
    @testset "h" begin
        @test compare_csv("output/aago_ttt-h.csv", "expected/aago_ttt-h.csv")
    end

    #### Handicap y Komi ########

    model = "h-k"
    lc, evidence, dict = lc_evidence(data, days, results, model)
    println("Evidence h-k: ")
    println(evidence)

    generate_csv("output/aago_ttt-h-k.csv", dict, lc)
    @testset "h-k" begin
        @test compare_csv("output/aago_ttt-h-k.csv", "expected/aago_ttt-h-k.csv")
    end

    #### Handicap y Komi-con-regresion-lineal ########

    model = "h-kreg"
    lc, evidence, dict = lc_evidence(data, days, results, model)
    println("Evidence h-kreg: ")
    println(evidence)

    generate_csv("output/aago_ttt-h-kreg.csv", dict, lc)
    @testset "h-kreg" begin
        @test compare_csv("output/aago_ttt-h-kreg.csv", "expected/aago_ttt-h-komi-regression.csv")
    end

end
