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

base = "aago"

@testset "All" begin
    data = read_data("../data/aago/aago_filtered.csv")
    days, results = set_arguments(data)

    expected_days = Dates.value.(data.started .- Date("2001-01-01"))
    @testset "days" begin
        @test expected_days == days
    end

    expected_results = [row.black_win == 1 ? [0.,1.] : [1., 0.] for row in eachrow(data) ]
    @testset "results" begin
        @test expected_results == results
    end

    #### Handicap ###############

    model = "h"
    # println("----------------------------------------------------------------------------------------------entrando: ")
    lc, evidence, dict = lc_evidence(data, days, results, model, base)
    println("Evidence h: ")
    println(evidence)

    generate_csv("output/aago_ttt-h.csv", dict, lc)
    @testset "h" begin
        @test compare_csv("output/aago_ttt-h.csv", "expected/aago_ttt-h.csv")
    end

    #### Handicap y Komi ########

    model = "h-k"
    lc, evidence, dict = lc_evidence(data, days, results, model, base)
    println("Evidence h-k: ")
    println(evidence)

    generate_csv("output/aago_ttt-h-k.csv", dict, lc)
    @testset "h-k" begin
        @test compare_csv("output/aago_ttt-h-k.csv", "expected/aago_ttt-h-k.csv")
    end

    #### Handicap y Komi-con-regresion-lineal ########

    model = "h-kreg"
    lc, evidence, dict = lc_evidence(data, days, results, model, base)
    println("Evidence h-kreg: ")
    println(evidence)

    generate_csv("output/aago_ttt-h-kreg.csv", dict, lc)
    @testset "h-kreg" begin
        @test compare_csv("output/aago_ttt-h-kreg.csv", "expected/aago_ttt-h-komi-regression.csv")
    end

    #### Handicap y Komi, ambos con regresion lineal ########

    model = "hreg-kreg"
    lc, evidence, dict = lc_evidence(data, days, results, model, base)
    println("Evidence hreg-kreg: ")
    println(evidence)

    generate_csv("output/aago_ttt-hreg-kreg.csv", dict, lc)
    @testset "hreg-kreg" begin
        @test compare_csv("output/aago_ttt-hreg-kreg.csv", "expected/aago_ttt-h_regression-komi-regression.csv")
    end

    #### Un test más pormenorizado #########
    @testset "Por separado" begin
        model = "h-kreg"

        width = 19
        expected_prior_dict = Dict{String,ttt.Player}()
        for h_key in Set([(row.handicap, width) for row in eachrow(data) ])
            expected_prior_dict[string(h_key)] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
        end

        expected_prior_dict["_komi19_1_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)
        expected_prior_dict["_komi19_0_"] = ttt.Player(ttt.Gaussian(0.0,6.0),0.0,0.0)

        prior_dict = init_priors(data, model)

        @testset "initial priors" begin
            @test prior_dict == expected_prior_dict
        end

        expected_events = [ [[string(r.white), k1(width), k0(width)], r.handicap<2 ? [string(r.black)] : [string(r.black),string((r.handicap,width))]] for r in eachrow(data) ]
        expected_weights = [ [[1.0, r.komi, 1.0], r.handicap<2 ? [1.0] : [1.0,1.0] ] for r in eachrow(data) ]

        events, weights = events_weights(data, model)

        @testset "events" begin
            @test events == expected_events
        end
        @testset "weights" begin
            @test weights == expected_weights
        end

        h = missing
        GC.gc()
        h = ttt.History(composition=expected_events, results=expected_results, times = expected_days , priors=expected_prior_dict, sigma=6.0,gamma=0.16,weights=expected_weights)
        ttt.convergence(h, iterations=16)
        expected_evidence = ttt.log_evidence(h)
        expected_lc = ttt.learning_curves(h)

        sigma, gamma, iterations = default_config(base)
        @testset "arguments" begin
            @test (sigma == 6.0) && (gamma == 0.16) && (iterations == 16)
        end

        lc, evidence, dict = run_and_converge(events, results, days, prior_dict, sigma, gamma, iterations, weights, model)

        @testset "evidence" begin
            @test evidence == expected_evidence
        end
        @testset "lc" begin
            @test lc == expected_lc
        end
        @testset "final priors" begin
            @test dict == expected_prior_dict
        end
    end

end
