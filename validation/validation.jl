include("../software/trueSkill.jl/src/TrueSkill.jl")
using .TrueSkill
global const ttt = TrueSkill
using Test
using CSV
#using JLD2
#using Dates
#using DataFrames

@testset "Tests" begin
    data = CSV.read("../data/ogs/summary_filtered.csv")    
    
    prior_dict = Dict{String,ttt.Rating}()
    for h_key in Set([(row.handicap, row.width) for row in eachrow(data) ])
        prior_dict[string(h_key)] = ttt.Rating(0.,25.0/3.,0.,1.0/100)
    end
    results = [row.black_win == 1 ? [1,0] : [0, 1] for row in eachrow(data) ]
    events = [ r.handicap<2 ? [[string(r.white)],[string(r.black)]] : [[string(r.white)],[string(r.black),string((r.handicap,r.width))]] for r in eachrow(data) ]   
    #times = [0 for _ in 1:length(events)] # To test batch performance
    times = Vector{Int64}()
    
    println(now())
    
    h = ttt.History(events, results, times , prior_dict)
    
    ts_log_evidence = ttt.log_evidence(h)
    
    println(now())
    
    ttt.convergence(h)
    
    ttt_log_evidence = ttt.log_evidence(h)
    
    println(now())
    
    print("TS-h: ", ts_log_evidence, ", TTT-h:", ttt_log_evidence)
    
    @testset "TTT-h vs TrueSkill-h" begin
        @test ts_log_evidence < ttt_log_evidence
    end
    
    
    events = [  [[string(r.white)],[string(r.black)]] for r in eachrow(data) ]   
    
    println(now())
    
    h = ttt.History(events, results, times)
    
    ts_log_evidence_with_out_handicap = ttt.log_evidence(h)
    
    println(now())
    
    ttt.convergence(h)
    
    ttt_log_evidence_with_out_handicap = ttt.log_evidence(h)
    
    println(now())
    
    print("TS-h: ", ts_log_evidence, ", TS:", ts_log_evidence_with_out_handicap)
    print("TTT-h: ", ttt_log_evidence, ", TTT:", ttt_log_evidence_with_out_handicap)
    
    
    @testset "TS-h vs TS" begin
        @test ts_log_evidence > ts_log_evidence_with_out_handicap
    end
    @testset "TTT-h vs TTT" begin
        @test ttt_log_evidence > ts_log_evidence_with_out_handicap
    end
    
    
end
