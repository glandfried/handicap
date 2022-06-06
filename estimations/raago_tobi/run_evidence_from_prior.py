import pandas as pd
import numpy as np
from math import sqrt, isnan, exp
from tqdm import tqdm
from estimations.raago_tobi.run_default import PRIORS_FILENAME, MATCHES_FILENAME
from estimations.raago_tobi.evidence import evidence

EVIDENCE_FILENAME = "estimations/raago_tobi/prior_evidence_dynamic_time.csv"

sigma_priors = [5.73781, 5.63937, 5.54098, 5.44266, 5.34439,
                5.24619, 5.14806, 5.05000, 4.95202, 4.85412,
                4.75631, 4.65859, 4.56098, 4.46346, 4.36606,
                4.26878, 4.17163, 4.07462, 3.97775, 3.88104,
                3.78451, 3.68816, 3.59201, 3.49607, 3.40037,
                3.30492, 3.20975, 3.11488, 3.02035, 2.92617,
                2.83240, 2.73907, 2.64622, 2.55392, 2.46221,
                2.37118, 2.28090, 2.19146, 2.10297, 2.01556,
                1.92938, 1.84459, 1.76139, 1.68003, 1.60078,
                1.52398, 1.45000, 1.37931, 1.31244, 1.25000,
                1.19269, 1.14127, 1.09659, 1.05948, 1.03078,
                1.01119, 1.00125, 1.00000, 1.00000]


def prior_by_category(category):
    num = int(category[:-1])
    rank = category[-1]
    if rank.lower() == "k":
        return -(num + 0.5), sigma_priors[50 - num]
    if rank.lower() == "d":
        return num + 0.5, sigma_priors[49 + num]


def get_prior(df_priors, event_id, player_id):
    prior = df_priors.loc[event_id].loc[player_id]
    if prior["mu"] == "NULL" or isnan(prior["mu"]):
        return prior_by_category(prior["category"])
    else:
        return prior["mu"], sqrt(prior["sigma"]**2 + (0.0005 ** 2) * (prior["age_in_days"]**2))


def get_evidence(df_priors, match_info):
    black_mu, black_sigma = get_prior(df_priors, match_info["event_id"], match_info["black"])
    white_mu, white_sigma = get_prior(df_priors, match_info["event_id"], match_info["white"])
    return evidence(black_mu, black_sigma, white_mu, white_sigma,
                    match_info["komi"], match_info["handicap"], match_info["winner"])


def main():
    df_priors = pd.read_csv(PRIORS_FILENAME, index_col=["event_id", "player_id"])
    df_matches = pd.read_csv(MATCHES_FILENAME)

    df_evidence = pd.DataFrame([
        (match_info["id"], get_evidence(df_priors, match_info))
        for _, match_info in tqdm(df_matches.iterrows())
    ], columns=["match_id", "evidence"])
    df_evidence.to_csv(EVIDENCE_FILENAME, index=False)
    print(f"Evidencia: {np.log(df_evidence['evidence']).sum()}")
    print(f"Media geometrica: {exp(np.log(df_evidence['evidence']).mean())}")


if __name__ == "__main__":
    main()
