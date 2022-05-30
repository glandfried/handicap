import pandas as pd
import math
from tqdm import tqdm
import numpy as np
from datetime import date

from estimations.raago_tobi.evidence import evidence
from estimations.raago_tobi.run_default import load_categories, LC_FILENAME, MATCHES_FILENAME

ESTIMATIONS_FILENAME = LC_FILENAME
EVIDENCE_FILENAME = "estimations/raago_tobi/evidence_dynamic_time.csv"
EVENTS_FILENAME = "data/aago/events.csv"

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


class PriorsDict:
    def __init__(self):
        self.categories = load_categories()

        estimations_df = pd.read_csv(ESTIMATIONS_FILENAME)
        # estimations_df = pd.read_csv("data/aago/raago.csv", names=["id", "mu", "sigma", "event_id", "player"])
        self.estimations = {
            (row["event_id"], row["player"]): (row["mu"], row["sigma"])
            for rid, row in estimations_df.iterrows()
        }
        self.events_by_player = {}

        events = pd.read_csv(EVENTS_FILENAME)
        events['date'] = events['end_date'].apply(date.fromisoformat)
        first_day = events['date'].min()
        events['day'] = events['date'].apply(lambda d: (d - first_day).days + 1)
        self.day_by_event = {
            row["event_id"]: row["day"]
            for _, row in events.iterrows()
        }

    def get_prior(self, player, event_id):
        if player in self.events_by_player and self.events_by_player[player][-1] != event_id:
            # Si ya jugo en algun evento, y el ultimo evento no es el actual, uso el ultimo evento
            prior = self.estimations[(self.events_by_player[player][-1], player)]
            days = self.day_by_event[event_id] - self.day_by_event[self.events_by_player[player][-1]]
            self.events_by_player[player].append(event_id)
            prior = prior[0], math.sqrt(prior[1]**2 + (0.0005 ** 2) * (days**2))
        elif player in self.events_by_player and len(self.events_by_player[player]) > 1:
            # Si ya jugo mas de un partido y el ultimo evento es el actual, uso el anteultimo
            prior = self.estimations[(self.events_by_player[player][-2], player)]
            days = self.day_by_event[event_id] - self.day_by_event[self.events_by_player[player][-2]]
            prior = prior[0], math.sqrt(prior[1]**2 + (0.0005 ** 2) * (days**2))
        else:
            # Si nunca jugo en un evento, o jugo en uno solo y es el actual
            prior = prior_by_category(self.categories[(event_id, player)])
            if player not in self.events_by_player:
                self.events_by_player[player] = [event_id]
        return prior


def main():
    matches_df = pd.read_csv(MATCHES_FILENAME)
    priors = PriorsDict()

    def match_evidence(match, event_id):
        mu_black, sigma_black = priors.get_prior(match['black'], event_id)
        mu_white, sigma_white = priors.get_prior(match['white'], event_id)
        return evidence(mu_black, sigma_black, mu_white, sigma_white,
                        match['komi'], match['handicap'], match["winner"])

    evidence_df = pd.DataFrame([
        (day, event_id, match["black"], match["white"], match_evidence(match, event_id))
        for day, day_matches in tqdm(matches_df.groupby('day'), desc="Day", position=0)
        for event_id, event_matches in day_matches.groupby('event_id')
        for _, match in event_matches.iterrows()
    ], columns=["day", "event_id", "black", "white", "evidence"])
    evidence_df.to_csv(EVIDENCE_FILENAME, index=False)
    print(f"Evidencia: {np.log(evidence_df['evidence']).sum()}")
    print(f"Media geometrica: {math.exp(np.log(evidence_df['evidence']).mean())}")


if __name__ == "__main__":
    main()
