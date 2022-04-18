# pip install whole-history-rating
from whr import whole_history_rating
from estimations.whr_prior import playerday as prior
import pandas as pd
from functools import reduce
from math import log, exp, inf, sqrt
from argparse import ArgumentParser, FileType
from sys import stdin
from scipy.stats import norm
from datetime import datetime as dt

COLUMNS = ['black', 'white', 'handicap', 'winner', 'day']


def natural_rating2_to_elo2(nr):
    return nr * ((400 / log(10)) ** 2)


def logistic_likelihood(diff_elo):
    return 1 / (1 + 10 ** (-diff_elo / 400))


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


class WHRRunner:
    def __init__(self, matches, handicap_elo=0.0, dynamic_factor=14.0,
                 auto_iter_rate=inf, auto_iter_time=inf, day_batch=False, handicap_elo_offset=0.0):
        """
        @param dynamic_factor: número que indica cuanta varianza hay entre las habilidades de un jugador en el tiempo
        @param handicap_elo: número que indica la habilidad que aporta una piedra de handicap, medido en unidades de elo
        @param matches: DataFrame con columnas 'id', 'black', 'white', 'handicap', 'winner', 'day'
        @param auto_iter_rate: número de partidas antes de volver a converger. Ignorado si day_batch es verdadero
        @param auto_iter_time: tiempo que se le da a WHR para converger
        @param day_batch: si es verdadero, se convergerá una vez por día de juego
        """
        self.whr = whole_history_rating.Base({'w2': dynamic_factor})
        self.evidence = []
        self.priors = []
        self.handicap_elo = handicap_elo
        self.handicap_elo_offset = handicap_elo_offset
        self.matches = matches
        self.auto_iter_rate = auto_iter_rate
        self.auto_iter_time = auto_iter_time
        self.day_batch = day_batch

    def match_evidence(self, match):
        black_estimate = self.player_estimate(match['black'])
        white_estimate = self.player_estimate(match['white'])

        mean = black_estimate['mean'] - white_estimate['mean'] \
               + match['handicap'] * self.handicap_elo + self.handicap_elo_offset
        stddev = sqrt(black_estimate['variance'] + white_estimate['variance'])
        black_probability = integrate(mean, stddev, logistic_likelihood)
        return black_probability if match['winner'] == 'B' else 1 - black_probability

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
        self.priors.append((self.player_estimate(match['black']), self.player_estimate(match['white'])))
        self.whr.create_game(match['black'], match['white'], match['winner'],
                             match['day'], match['handicap'] * self.handicap_elo + self.handicap_elo_offset)

    def cross_entropy(self):
        return -self.log_evidence() / len(self.evidence)

    def geometric_mean(self):
        return exp(self.log_evidence() / len(self.evidence))

    def log_evidence(self):
        return reduce(lambda x, acc: x + acc, [log(e) for e in self.evidence])

    def player_estimate(self, name):
        player = self.whr.player_by_name(name)
        player.update_uncertainty()
        if len(player.days) > 0:
            estimate = player.days[-1]
        else:
            estimate = prior
        return {'mean': estimate.elo, 'variance': natural_rating2_to_elo2(estimate.uncertainty)}

    def learning_curves(self):
        data = [
            (name, d.day, d.elo, natural_rating2_to_elo2(d.uncertainty))
            for name, player in self.whr.players.items()
            for d in player.days
        ]
        return pd.DataFrame(data, columns=['player', 'day', 'mean', 'variance'])

    def matches_evidence(self):
        data = [
            (match['id'], black['mean'], black['variance'], white['mean'], white['variance'], evidence)
            for ((_, match), (black, white), evidence) in zip(self.matches.iterrows(), self.priors, self.evidence)
        ]
        columns = ['id', 'black_mean', 'black_variance', 'white_mean', 'white_variance', 'evidence']
        return pd.DataFrame(data, columns=columns)


def read_args():
    parser = ArgumentParser(description='Corre el modelo WHR sobre un dataset en CSV.')
    parser.add_argument('dataset', type=FileType('r'), default=stdin, nargs='?',
                        help='CSV con columnas: black, white, handicap, winner, day')
    parser.add_argument('-l', '--learning_curves', dest='learning_curves_file', type=FileType('w'), required=True)
    parser.add_argument('-r', '--results', dest='results_file', type=FileType('w'), required=True)
    parser.add_argument('-d', '--dynamic_factor', dest='dynamic_factor', type=float, default=14.0,
                        help='Factor dinámico que indica cuánto puede cambiar la habilidad en el tiempo,'
                             ' en unidades de Elo^2/dia')
    parser.add_argument('-e', '--handicap_elo', dest='handicap_elo', type=float, default=50.0,
                        help='Habilidad agregada por cada piedra de handicap a favor, en unidades de Elo')
    parser.add_argument('-i', '--auto_iter_rate', dest='auto_iter_rate', type=int, default=100,
                        help='Cantidad de partidos entre iteraciones del algoritmo de Newton')
    parser.add_argument('-t', '--auto_iter_time', dest='auto_iter_time', type=float, default=inf,
                        help='Tiempo que se le da para converger (por defecto, infinito)')
    parser.add_argument('-b', '--day_batch', dest='day_batch', action='store_true',
                        help='Cantidad de partidos entre iteraciones del algoritmo de Newton')
    return parser.parse_args()


def run(dataset, handicap_elo=0.0, dynamic_factor=14.0,
        auto_iter_rate=inf, auto_iter_time=inf, day_batch=False, handicap_elo_offset=0.0):
    df = pd.read_csv(dataset)

    runner = WHRRunner(df,
                       handicap_elo=handicap_elo,
                       dynamic_factor=dynamic_factor,
                       auto_iter_rate=auto_iter_rate,
                       auto_iter_time=auto_iter_time,
                       day_batch=day_batch,
                       handicap_elo_offset=handicap_elo_offset)
    start_time = dt.now()
    runner.iterate()
    end_time = dt.now()

    return runner, (end_time - start_time).total_seconds()


def save_results(file, runner, runtime):
    print("geometric_mean:", runner.geometric_mean(), file=file)  # 0.5369 en AAGO
    print("log_evidence:", runner.log_evidence(), file=file)  # -2081.4123902144534 en AAGO
    print("cross_entropy:", runner.cross_entropy(), file=file)  # 0.6218740335268759 en AAGO
    print("runtime:", runtime, file=file)


def parse_results(file):
    res = dict()
    for line in file.readlines():
        parsed = line.replace('\n', '').split(': ')
        res[parsed[0]] = parsed[1]
    return res


def main():
    args = read_args()
    print("Argumentos:")
    for arg in vars(args):
        print(f"{arg}: {getattr(args, arg)}")
    runner, runtime = run(**vars(args))

    runner.learning_curves().to_csv(args.learning_curves_file, index=False)
    save_results(args.results_file, runner, runtime)


if __name__ == "__main__":
    main()
