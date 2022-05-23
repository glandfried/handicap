import pandas as pd
import subprocess
from math import floor

CATEGORIES_FILENAME = "data/aago/categories.csv"
MATCHES_FILENAME = "data/aago/aago_original_filtered.adapted.csv"
RAAGO_PATH = "../RAAGo/original-AGA-rating-system/aago-rating-calculator/raago"


class EstimationHistory:
    def __init__(self):
        self.history_by_player = {}

    def add_estimation(self, player, day, estimation):
        if player not in self.history_by_player:
            self.history_by_player[player] = []

        self.history_by_player[player].append((day, estimation))

    def add_estimations(self, day, estimations):
        for (player, estimation) in estimations:
            self.add_estimation(player, day, estimation)

    def get_estimation(self, player):
        if player in self.history_by_player:
            return self.history_by_player[player][-1]
        else:
            return "NULL", ("NULL", "NULL")


def load_categories():
    categories_df = pd.read_csv(CATEGORIES_FILENAME, names=["id", "ranking", "event_id", "player_id"])
    return {
        (event_id, player_id): ranking
        for index, (row_id, ranking, event_id, player_id) in categories_df.iterrows()
    }


def make_raago_in(day, event, priors, categories, matches):
    players = pd.concat([matches['black'], matches['white']]).unique()

    def player_description(player):
        last_day, estimation = priors.get_estimation(player)
        diff_day = "NULL" if last_day == "NULL" else day - last_day
        return f"{player} {categories[(event, player)]} {estimation[0]} {estimation[1]} {diff_day}"

    def match_description(match):
        winner = "BLACK" if match["winner"] == "B" else "WHITE"
        return f"{match['white']} {match['black']} {match['handicap']} {floor(match['komi'])} {winner}"

    return ("PLAYERS\n" + "\n".join([
        player_description(player)
        for player in players
    ]) + "\nEND_PLAYERS\nGAMES\n" + "\n".join([
        match_description(match)
        for _, match in matches.iterrows()
    ]) + "\nEND_GAMES\n").encode('utf-8')


def parse_raago_out(outs):
    def player_posterior(line):
        [player_id, mu, sigma] = line.strip().split("\t")
        return player_id, (mu, sigma)

    return [
        player_posterior(line)
        for line in outs.strip().split("\n")
    ]


def run_raago(matches, day, event, priors, categories):
    with subprocess.Popen(RAAGO_PATH, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as p:
        ins = make_raago_in(day, event, priors, categories, matches)
        outs, errs = p.communicate(ins)
        return parse_raago_out(outs.decode())


def main():
    categories = load_categories()  # dado un event_id y player_id, dice la categoria declarada
    matches_df = pd.read_csv(MATCHES_FILENAME)
    estimations = EstimationHistory()  # datos un jugador, da la lista de tuplas con (dia, estimacion)

    for day, day_matches in matches_df.groupby('day'):
        for event_id, event_matches in day_matches.groupby('event_id'):
            posteriors = run_raago(event_matches, day, event_id, estimations, categories)
            estimations.add_estimations(day, posteriors)
    estimations.print()


if __name__ == "__main__":
    main()
