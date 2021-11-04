# pip install whole-history-rating
from whr import whole_history_rating
import pandas as pd
from functools import reduce
from math import log, exp, inf
from argparse import ArgumentParser, FileType
from sys import stdin

COLUMNS = ['black', 'white', 'handicap', 'winner', 'day']


class WHRRunner:
    def __init__(self, matches, handicap_elo=0.0, dynamic_factor=14.0, auto_iter_rate=inf, auto_iter_time=inf):
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
        self.auto_iter_time = auto_iter_time
    
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
        self.whr.auto_iterate(time_limit=self.auto_iter_time, precision=10E-3)
    
    def cross_entropy(self):
        return -self.log_evidence()/len(self.evidence)

    def geometric_mean(self):
        return exp(self.log_evidence()/len(self.evidence))
    
    def log_evidence(self):
        return reduce(lambda x, acc: x + acc, [log(e) for e in self.evidence])

    def learning_curves(self):
        def natural_rating2_to_elo2(nr):
            return nr * ((400 / log(10))**2)

        data = [
            (player, day, mean, natural_rating2_to_elo2(variance / 100))
            for player in self.whr.players.keys()
            for (day, mean, variance) in self.whr.ratings_for_player(player)
        ]
        return pd.DataFrame(data, columns=['player', 'day', 'mean', 'variance'])


def read_args():
    parser = ArgumentParser(description='Corre el modelo WHR sobre un dataset en CSV.')
    parser.add_argument('dataset', type=FileType('r'), default=stdin, nargs='?',
                        help='CSV con columnas: black, white, handicap, winner, day')
    parser.add_argument('-l', '--learning_curves', dest='learning_curves_file', type=FileType('w'), required=True)
    parser.add_argument('-r', '--results', dest='results_file', type=FileType('w'), required=True)
    parser.add_argument('-i', '--auto_iter_rate', dest='auto_iter_rate', type=int, default=100,
                        help='Cantidad de partidos entre iteraciones del algoritmo de Newton')
    parser.add_argument('-d', '--dynamic_factor', dest='dynamic_factor', type=float, default=14.0,
                        help='Factor dinámico que indica cuánto puede cambiar la habilidad en el tiempo,'
                             ' en unidades de Elo^2/dia')
    parser.add_argument('-e', '--handicap_elo', dest='handicap_elo', type=float, default=50.0,
                        help='Habilidad agregada por cada piedra de handicap a favor, en unidades de Elo')
    return parser.parse_args()


if __name__ == "__main__":
    args = read_args()
    df = pd.read_csv(args.dataset)

    runner = WHRRunner(df, args.handicap_elo, args.dynamic_factor, args.auto_iter_rate)
    runner.iterate()

    runner.learning_curves().to_csv(args.learning_curves_file, index=False)

    print("geometric_mean:", runner.geometric_mean(), file=args.results_file)  # 0.5369 en AAGO
    print("log_evidence:", runner.log_evidence(), file=args.results_file)  # -2081.4123902144534 en AAGO
    print("cross_entropy:", runner.cross_entropy(), file=args.results_file)  # 0.6218740335268759 en AAGO
