# pip install whole-history-rating
from whr import whole_history_rating
import pandas as pd
from functools import reduce
from math import log, exp, inf
from argparse import ArgumentParser, FileType
from sys import stdin

COLUMNS = ['black', 'white', 'handicap', 'winner', 'day']


class WHRRunner:
    def __init__(self, matches, handicap_elo=0.0, dynamic_factor=14.0,
                 auto_iter_rate=inf, auto_iter_time=inf, day_batch=False):
        """
        @param dynamic_factor: número que indica cuanta varianza hay entre las habilidades de un jugador en el tiempo
        @param handicap_elo: número que indica la habilidad que aporta una piedra de handicap, medido en unidades de elo
        @param matches: DataFrame con columnas 'black', 'white', 'handicap', 'winner', 'day'
        @param auto_iter_rate: número de partidas antes de volver a converger. Ignorado si day_batch es verdadero
        @param auto_iter_time: tiempo que se le da a WHR para converger
        @param day_batch: si es verdadero, se convergerá una vez por día de juego
        """
        self.whr = whole_history_rating.Base({'w2': dynamic_factor})
        self.evidence = []
        self.handicap_elo = handicap_elo
        self.matches = matches
        self.auto_iter_rate = auto_iter_rate
        self.auto_iter_time = auto_iter_time
        self.day_batch = day_batch
    
    def match_evidence(self, match):
        black_probability, white_probability = self.whr.probability_future_match(match['black'], match['white'],
                                                                                 match['handicap'] * self.handicap_elo)
        return black_probability if match['winner'] == 'B' else white_probability
    
    def optimize_players(self, match):
        self.optimize_player(match['black'])
        self.optimize_player(match['white'])
    
    def optimize_player(self, player):
        self.whr.player_by_name(player).run_one_newton_iteration()
    
    def iterate(self, new_matches=None):
        if new_matches is None:
            new_matches = self.matches
        else:
            self.matches.append(new_matches)

        if self.day_batch:
            self.day_batch_iterate(new_matches)
        else:
            self.periodic_iterate(new_matches)
        # La incertidumbre se calcula al iterar
        # Si no se itera al final, puede haber jugadores sin incertidumbre
        self.converge()

    def converge(self):
        self.whr.auto_iterate(time_limit=self.auto_iter_time, precision=10E-3)

    def day_batch_iterate(self, matches):
        previous_day = 0
        for index, match in matches.iterrows():
            if previous_day != match['day']:
                self.converge()
            previous_day = match['day']

            self.process_match(match)

    def periodic_iterate(self, matches):
        for index, match in matches.iterrows():
            self.optimize_players(match)
            self.process_match(match)
            self.optimize_players(match)
            if index % self.auto_iter_rate == 0:
                self.converge()

    def process_match(self, match):
        self.evidence.append(self.match_evidence(match))
        self.whr.create_game(match['black'], match['white'], match['winner'],
                             match['day'], match['handicap'] * self.handicap_elo)
    
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
            (name, d.day, d.elo, natural_rating2_to_elo2(d.uncertainty))
            for name, player in self.whr.players.items()
            for d in player.days
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
