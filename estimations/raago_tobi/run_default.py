import pandas as pd
import subprocess
from math import floor

CATEGORIES_FILENAME = "data/aago/categories.csv"
MATCHES_FILENAME = "data/aago/aago_original_filtered.adapted.csv"
RAAGO_PATH = "../RAAGo/original-AGA-rating-system/aago-rating-calculator/raago"
LC_FILENAME = "estimations/raago_tobi/posteriors.csv"


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


def make_raago_in(day, event, estimations, categories, matches):
    players = pd.concat([matches['black'], matches['white']]).unique()

    def player_description(player):
        last_day, estimation = estimations.get_estimation(player)
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
        return int(player_id), (mu, sigma)

    return [
        player_posterior(line)
        for line in outs.strip().split("\n")
    ]


def run_raago(matches, day, event, estimations, categories):
    with subprocess.Popen(RAAGO_PATH, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as p:
        ins = make_raago_in(day, event, estimations, categories, matches)
        outs, errs = p.communicate(ins)
        return parse_raago_out(outs.decode())


def main():
    categories = load_categories()  # dado un event_id y player_id, dice la categoria declarada
    matches_df = pd.read_csv(MATCHES_FILENAME)
    estimations = EstimationHistory()  # datos un jugador, da la lista de tuplas con (dia, estimacion)

    for day, day_matches in matches_df.groupby('day'):
        for event_id, event_matches in day_matches.groupby('event_id'):
            posteriors = run_raago(event_matches, day, event_id, estimations, categories)
            estimations.add_estimations(day, event_id, posteriors)
    estimations.export().to_csv(LC_FILENAME, index=False)


if __name__ == "__main__":
    main()
