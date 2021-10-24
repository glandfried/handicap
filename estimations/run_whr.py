# pip install whole-history-rating
from whr import whole_history_rating
import pandas as pd
from functools import reduce
from math import log, exp
from argparse import ArgumentParser, FileType


class WHRRunner:
    def __init__(self, dynamic_factor, handicap_elo, matches, auto_iter_rate):
        """
        @param dynamic_factor: número que indica cuanta varianza hay entre las habilidades de un jugador en el tiempo
        @param handicap_elo: número que indica la habilidad que aporta una piedra de handicap, medido en unidades de elo
        @param matches: DataFrame con columnas 'black', 'white', 'handicap', 'winner', 'day'
        """
        self.whr = whole_history_rating.Base({'w2': dynamic_factor})
        self.evidence = []
        self.handicap_elo = handicap_elo
        self.matches = matches
        self.auto_iter_rate = auto_iter_rate
    
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
            if index % self.auto_iter_rate == 0:
                self.whr.auto_iterate(time_limit=10, precision=10E-3)
        # La incertidumbre se calcula al iterar
        # Si no se itera al final, puede haber jugadores sin incertidumbre
        self.whr.auto_iterate(time_limit=10, precision=10E-3)
    
    def cross_entropy(self):
        return -self.log_evidence()/len(self.evidence)

    def geometric_mean(self):
        return exp(self.log_evidence()/len(self.evidence))
    
    def log_evidence(self):
        return reduce(lambda x, acc: x + acc, [log(e) for e in self.evidence])

    def learning_curves(self):
        data = [
            (player, day, mean, variance)
            for player in self.whr.players.keys()
            for (day, mean, variance) in self.whr.ratings_for_player(player)
        ]
        return pd.DataFrame(data, columns=['player', 'day', 'mean', 'variance'])


def read_args():
    parser = ArgumentParser(description='Corre el modelo WHR sobre un dataset en CSV.')
    parser.add_argument('dataset', type=FileType('r'), help='CSV con columnas: black, white, handicap, winner, day')
    parser.add_argument('-l', '--learning_curves', dest='learning_curves_file', type=FileType('w'), required=True)
    parser.add_argument('-r', '--results', dest='results_file', type=FileType('w'), required=True)
    parser.add_argument('-i', '--auto_iter_rate', dest='auto_iter_rate', type=int, default=100,
                        help='Cantidad de partidos entre iteraciones del algoritmo de Newton')
    return parser.parse_args()


if __name__ == "__main__":
    args = read_args()
    df = pd.read_csv(args.dataset)

    # TODO: hiperparámetros a optimizar
    DYNAMIC_FACTOR = 0.14
    HANDICAP_ELO = 50
    # TODO: el handicap lo pide en unidades de elo, hay que buscar un multiplicador que tenga sentido
    # TODO: se podría agregar komi restándolo al handicap
    runner = WHRRunner(DYNAMIC_FACTOR, HANDICAP_ELO, df, args.auto_iter_rate)
    runner.iterate()

    runner.learning_curves().to_csv(args.learning_curves_file, index=False)

    print("geometric_mean:", runner.geometric_mean(), file=args.results_file)  # 0.5369 en AAGO
    print("log_evidence:", runner.log_evidence(), file=args.results_file)  # -2081.4123902144534 en AAGO
    print("cross_entropy:", runner.cross_entropy(), file=args.results_file)  # 0.6218740335268759 en AAGO
