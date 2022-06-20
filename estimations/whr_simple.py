# pip install whole-history-rating
from whr import whole_history_rating
from whr_prior import prior
import pandas as pd
from math import log, inf, sqrt
from scipy.stats import norm


def natural_rating2_to_elo2(nr):
    return nr * ((400 / log(10)) ** 2)


def logistic_likelihood(diff_elo):
    return 1 / (1 + 10 ** (-diff_elo / 400))


def player_estimate(whr, player, day=0, dynamic_factor=0.0):
    player = whr.player_by_name(player)
    player.update_uncertainty()
    dt = 0
    if len(player.days) > 0:
        estimate = player.days[-1]
        dt = day - estimate.day
    else:
        estimate = prior
    return {'mean': estimate.elo, 'variance': natural_rating2_to_elo2(estimate.uncertainty) + dt * dynamic_factor}


def run_by_event(matches, handicap_elo=0.0, offset_elo=0.0, dynamic_factor=14.0):
    whr = whole_history_rating.Base({'w2': dynamic_factor})
    priors = {}
    posteriors = {}
    sorted_matches = matches.sort_values(["day", "start_date", "event_id"])
    for (day, _, event_id), event_matches in sorted_matches.groupby(["day", "start_date", "event_id"]):
        players = pd.concat([event_matches['black'], event_matches['white']]).unique()
        for player in players:
            priors[(event_id, player)] = player_estimate(whr, player, day, dynamic_factor)
        for _, match in event_matches.iterrows():
            whr.create_game(match['black'], match['white'], match['winner'],
                            day, match['handicap'] * handicap_elo + offset_elo)
        whr.auto_iterate(time_limit=inf, precision=10E-3)
        for player in players:
            posteriors[(event_id, player)] = player_estimate(whr, player)

    return learning_curves(whr), matches_evidence(matches, priors, handicap_elo, offset_elo)


def integrate(mean, stddev, likelihood, steps=51, sigmas=6):
    A = -steps // 2
    B = A + steps
    total_p = 0.0
    dx = 2 * sigmas * stddev / float(steps)
    ret = 0.0
    for i in range(A, B):
        mu = mean + i * dx
        p = norm.pdf(mu, mean, stddev) * dx
        total_p += p
        ret += p * likelihood(mu)
    # assert(abs(1.0 - total_p) < 10e-8)
    return ret


def learning_curves(whr):
    data = [
        (name, d.day, d.elo, natural_rating2_to_elo2(d.uncertainty))
        for name, player in whr.players.items()
        for d in player.days
    ]
    return pd.DataFrame(data, columns=['player', 'day', 'mean', 'variance'])


def matches_evidence(matches, priors, handicap_elo=0.0, offset_elo=0.0):
    evidence_dict = {}
    for _, match in matches.iterrows():
        black_estimate = priors[(match["event_id"], match["black"])]
        white_estimate = priors[(match["event_id"], match["white"])]

        mean = black_estimate["mean"] - white_estimate["mean"] + match['handicap'] * handicap_elo + offset_elo
        stddev = sqrt(black_estimate["variance"] + white_estimate["variance"])
        black_probability = integrate(mean, stddev, logistic_likelihood)
        evidence_dict[match["id"]] = black_probability if match['winner'] == 'B' else 1 - black_probability
    return pd.DataFrame([(i, evidence) for i, evidence in evidence_dict.items()], columns=["id", "evidence"])

