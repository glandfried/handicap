import pandas as pd
import subprocess
from math import floor
from dataclasses import dataclass

CATEGORIES_FILENAME = "data/aago/categories.csv"
MATCHES_FILENAME = "data/aago/aago_original_filtered.adapted.csv"
RAAGO_PATH = "../RAAGo/original-AGA-rating-system/aago-rating-calculator/raago"
PRIORS_FILENAME = "estimations/raago_tobi/priors.csv"
PRIORS_COLUMNS = ["event_id", "player_id", "category", "mu", "sigma", "age_in_days"]
LC_FILENAME = "estimations/raago_tobi/posteriors.csv"


@dataclass
class Prior:
    event_id: int
    player_id: int
    category: str
    mu: int | str = "NULL"
    sigma: int | str = "NULL"
    age_in_days: int | str = "NULL"


class EstimationHistory:
    def __init__(self):
        self.history_by_player = {}

    def add_estimation(self, player, day, event_id, estimation):
        if player not in self.history_by_player:
            self.history_by_player[player] = []

        self.history_by_player[player].append((day, event_id, estimation))

    def add_estimations(self, day, event_id, estimations):
        for (player, estimation) in estimations:
            self.add_estimation(player, day, event_id, estimation)

    def get_estimation(self, player):
        day, event_id, (mu, sigma) = "NULL", "NULL", ("NULL", "NULL")
        if player in self.history_by_player:
            day, event_id, (mu, sigma) = self.history_by_player[player][-1]
        return day, (mu, sigma)

    def export(self):
        return pd.DataFrame([
            (player, day, event_id, mu, sigma)
            for player, history in self.history_by_player.items()
            for day, event_id, (mu, sigma) in history
        ], columns=["player", "day", "event_id", "mu", "sigma"])


def load_categories():
    categories_df = pd.read_csv(CATEGORIES_FILENAME, names=["id", "ranking", "event_id", "player_id"])
    return {
        (row["event_id"], row["player_id"]): row["ranking"]
        for index, row in categories_df.iterrows()
    }


def make_priors(players, estimations, categories, day, event_id) -> list[Prior]:
    def player_prior(player):
        last_day, (mu, sigma) = estimations.get_estimation(player)
        diff_day = "NULL" if last_day == "NULL" else day - last_day
        return Prior(event_id=event_id, player_id=player, category=categories[(event_id, player)],
                     mu=mu, sigma=sigma, age_in_days=diff_day)

    return [
        player_prior(player)
        for player in players
    ]


def make_raago_in(matches, priors):
    def player_description(prior: Prior):
        return f"{prior.player_id} {prior.category} {prior.mu} {prior.sigma} {prior.age_in_days}"

    def match_description(match):
        winner = "BLACK" if match["winner"] == "B" else "WHITE"
        return f"{match['white']} {match['black']} {match['handicap']} {floor(match['komi'])} {winner}"

    return ("PLAYERS\n" + "\n".join([
        player_description(prior)
        for prior in priors
    ]) + "\nEND_PLAYERS\nGAMES\n" + "\n".join([
        match_description(match)
        for _, match in matches.iterrows()
    ]) + "\nEND_GAMES\n").encode('utf-8')


def parse_raago_out(outs):
    def player_posterior(line):
        [player_id, mu, sigma] = line.strip().split("\t")
        return int(player_id), (mu, sigma)

    return [
        player_posterior(line)
        for line in outs.strip().split("\n")
    ]


def run_raago(matches, priors):
    with subprocess.Popen(RAAGO_PATH, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as p:
        ins = make_raago_in(matches, priors)
        outs, errs = p.communicate(ins)
        return parse_raago_out(outs.decode())


def main():
    categories = load_categories()  # dado un event_id y player_id, dice la categoria declarada
    matches_df = pd.read_csv(MATCHES_FILENAME).sort_values(["day", "start_date", "event_id"])
    estimations = EstimationHistory()  # datos un jugador, da la lista de tuplas con (dia, estimacion)
    priors_list: list[Prior] = []

    for (day, start_date, event_id), event_matches in matches_df.groupby(["day", "start_date", "event_id"]):
        players = pd.concat([event_matches['black'], event_matches['white']]).unique()
        priors = make_priors(players, estimations, categories, day, event_id)
        priors_list.extend(priors)
        posteriors = run_raago(event_matches, priors)
        estimations.add_estimations(day, event_id, posteriors)
    pd.DataFrame([
        (prior.event_id, prior.player_id, prior.category, prior.mu, prior.sigma, prior.age_in_days)
        for prior in priors_list
    ], columns=PRIORS_COLUMNS).to_csv(PRIORS_FILENAME, index=False)
    estimations.export().to_csv(LC_FILENAME, index=False)


if __name__ == "__main__":
    main()
