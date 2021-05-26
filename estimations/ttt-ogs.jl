using CSV
using DataFrames
using Dates
include("../software/ttt.jl/src/TrueSkill.jl")
using .TrueSkill
using VegaLite

df = CSV.read("../data/ogs/summary_filtered.csv", DataFrame)

days = Dates.value.(
    Date.(map(m->m.match,
        match.(r"(\d+)-(\d+)-(\d+)", df[:,"started"]))
        ) .- Date("1900-01-01"))

composition = [
    match.order == "(1, 0)" ?
    [[string(match.black)],[string(match.white)]] :
    [[string(match.white)],[string(match.black)]]
    for match in eachrow(df)]

function fit(gamma)
    h = TrueSkill.History(
        composition=composition,
        times = days,
        sigma = 10.0,
        gamma = gamma)
    TrueSkill.convergence(h,epsilon=0.01, iterations=10)
    return h
end

handicap_id(handicap) :: String = "handicap_"*string(handicap)
handicap_player(match) :: Vector{String} = match.handicap > 0 ? [handicap_id(match.handicap)] : []
black_team(match) :: Vector{String} = vcat([string(match.black)], handicap_player(match))

composition_with_handicaps = [
    match.order == "(1, 0)" ?
    [black_team(match), [string(match.white)]] :
    [[string(match.white)], black_team(match)]
    for match in eachrow(df)]

handicap_priors = Dict([
    (handicap_id(n), TrueSkill.Player(prior=TrueSkill.Gaussian(mu=0.0,sigma=10.0), gamma=0.0))
    for n=1:15
])
function fit_with_handicaps(gamma)
    h = TrueSkill.History(
        composition=composition_with_handicaps,
        priors = handicap_priors,
        times = days,
        sigma = 10.0,
        gamma = gamma)
    TrueSkill.convergence(h,epsilon=0.01, iterations=10)
    return h
end
rgamma = range(0.15, step=0.002, stop=0.18)

evidences = [(
    gamma=gamma,
    log_evidence=TrueSkill.log_evidence(fit(gamma))
    ) for gamma=rgamma
]
handicap_evidences = [(
    gamma=gamma,
    log_evidence=TrueSkill.log_evidence(fit_with_handicaps(gamma))
    ) for gamma=rgamma
]

plot(title) = @vlplot(
    title=title,
    mark={
        type=:line,
        point={
            filled= false,
            fill= "white"
    }},
    width=400,
    height=300,
    x={
        :gamma,
        scale={
            zero=false
        }
    },
    y={
        :log_evidence,
        scale={
            zero=false
        }
    })

DataFrame(evidences) |>
plot("Evidencia en función del gamma, modelo TTT sin handicap ni komi") |>
save("../figures/ttt-gamma-log-evidence.png")

DataFrame(handicap_evidences) |>
plot("Evidencia en función del gamma, modelo TTT con handicap, sin komi") |>
save("../figures/ttt-handicaps-gamma-log-evidence.png")

evidence_list(history) = [
    (evidence=e.evidence,)
    for b in history.batches
    for e in b.events
]

evidence_histogram(gamma, fit_function) = evidence_list(fit_function(gamma)) |> @vlplot(
    :bar,
    x={:evidence, bin=true},
    y="count()")

evidence_histogram(0.164, fit) |>
    save("../figures/ttt-best-gamma-evidence-histogram.png")

evidence_histogram(0.158, fit_with_handicaps) |>
    save("../figures/ttt-handicaps-best-gamma-evidence-histogram.png")
