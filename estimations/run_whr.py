# pip install whole-history-rating
from whr import whole_history_rating
import pandas as pd
from functools import reduce
from math import log, exp
from argparse import ArgumentParser, FileType


class WHRRunner:
    def __init__(self, dynamic_factor, handicap_elo, matches):
        """
        @param dynamic_factor: número que indica cuanta varianza hay entre las habilidades de un jugador en el tiempo
        @param handicap_elo: número que indica la habilidad que aporta una piedra de handicap, medido en unidades de elo
        @param matches: DataFrame con columnas 'black', 'white', 'handicap', 'winner', 'day'
        """
        self.whr = whole_history_rating.Base({'w2': dynamic_factor})
        self.evidence = []
        self.handicap_elo = handicap_elo
        self.matches = matches
    
    def match_evidence(self, match):
        black_probability, white_probability = self.whr.probability_future_match(match['black'], match['white'],
                                                                                 match['handicap'] * self.handicap_elo)
        return black_probability if match['winner'] == 'B' else white_probability
    
    def optimize_players(self, match):
        self.optimize_player(match['black'])
        self.optimize_player(match['white'])
    
    def optimize_player(self, player):
        self.whr.player_by_name(player).run_one_newton_iteration()
    
    def iterate(self):
        for index, match in self.matches.iterrows():
            self.optimize_players(match)
            self.evidence.append(self.match_evidence(match))
            self.whr.create_game(match['black'], match['white'], match['winner'],
                                 match['day'], match['handicap'] * self.handicap_elo)
            self.optimize_players(match)
            if index % 1 == 0:
                self.whr.auto_iterate(time_limit=10, precision=10E-3)
    
    def cross_entropy(self):
        return -self.log_evidence()/len(self.evidence)

    def geometric_mean(self):
        return exp(self.log_evidence()/len(self.evidence))
    
    def log_evidence(self):
        return reduce(lambda x, acc: x + acc, [log(e) for e in self.evidence])


parser = ArgumentParser(description='Corre el modelo WHR sobre un dataset en CSV.')
parser.add_argument('dataset', type=FileType('r'), help='CSV con columnas: black, white, handicap, winner, day')
# parser.add_argument('-o', '--output', dest='output_file', type=FileType('w'), required=True)
parser.add_argument('-l', '--log', dest='log_file', type=FileType('w'), required=True)
args = parser.parse_args()
if __name__ == "__main__":
    df = pd.read_csv(args.dataset)

    # TODO: hiperparámetros a optimizar
    DYNAMIC_FACTOR = 0.14
    HANDICAP_ELO = 50
    # TODO: el handicap lo pide en unidades de elo, hay que buscar un multiplicador que tenga sentido
    # TODO: se podría agregar komi restándolo al handicap
    runner = WHRRunner(DYNAMIC_FACTOR, HANDICAP_ELO, df)
    runner.iterate()

    print("geometric_mean:", runner.geometric_mean(), file=args.log_file)  # 0.5369 en AAGO
    print("log_evidence:", runner.log_evidence(), file=args.log_file)  # -2081.4123902144534 en AAGO
    print("cross_entropy:", runner.cross_entropy(), file=args.log_file)  # 0.6218740335268759 en AAGO
