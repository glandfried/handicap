from random import random
import pandas as pd
import matplotlib.pyplot as plt
from numpy import sqrt, log, sum
from scipy.stats import norm
from numpy.random import normal
from argparse import ArgumentParser

from estimations.run_whr import WHRRunner, COLUMNS

MAXIMUM = 400
PERFORMANCE_SCALE = 200


def performance_probit(skills, size=1):
    return normal(scale=PERFORMANCE_SCALE, size=size) + skills


def result_probit(elo1, elo2):
    return 'B' if performance_probit(elo1) > performance_probit(elo2) else 'W'


def logistic(elo1, elo2):
    gamma1 = 10 ** (elo1/400.0)
    gamma2 = 10 ** (elo2/400.0)
    return gamma1 / (gamma1 + gamma2)


def result_logit(elo1, elo2):
    return 'B' if random() < logistic(elo1, elo2) else 'W'


def run(opponents_diff, repetitions, result_fn, player_matches=10):
    opponents_true_skill = range(-MAXIMUM, MAXIMUM, opponents_diff)
    opponents_number = len(opponents_true_skill)
    pretrain = [
        (f"o{p1}", f"o{p2}", 0, result_fn(opponents_true_skill[p1], opponents_true_skill[p2]), 0)
        for p1 in range(opponents_number)
        for p2 in range(p1+1, min(p1+1+player_matches, opponents_number))
        for _ in range(repetitions)
        if p1 != p2
    ]

    df = pd.DataFrame(pretrain, columns=COLUMNS)
    runner = WHRRunner(df, 0.0, 14.0)
    runner.iterate()
    lc = runner.learning_curves()
    lc['skill'] = opponents_true_skill

    return lc


def ecm_sqrt(df):
    return sqrt(((df['skill'] - df['mean']) ** 2).mean())


def log_probability_skills(df):
    evidence_skills = [
        norm.pdf(row['skill'],
                 loc=row['mean'],
                 scale=sqrt(row['variance']))
        for _, row in df.iterrows()
    ]
    return sum(log(evidence_skills))


def plot_confidence(df, col, model):
    stats = df.groupby('repetitions')[col].describe().reset_index()
    plt.figure()
    plt.fill_between(stats['repetitions'], stats['25%'], stats['75%'], alpha=0.5, label='Intervalo 25%/75%')
    plt.plot(stats['repetitions'], stats['50%'], label='Mediana')
    plt.legend()
    plt.xlabel('Número de repeticiones de las partidas')
    plt.ylabel(col)
    plt.savefig(f'figures/whr_big_community_{col}_{model}.pdf')


def run_all(result_fn, model):
    def datum(repetitions):
        res = run(40, repetitions, result_fn)
        return repetitions, ecm_sqrt(res), log_probability_skills(res)

    pd.DataFrame([
        datum(repetitions)
        for repetitions in range(10, 81, 10)
        for _ in range(10)
    ], columns=['repetitions', 'ecm_sqrt', 'log_probability'])\
        .to_csv(f'estimations/whr_big_community_{model}.csv')


def plot_all(model):
    df = pd.read_csv(f'estimations/whr_big_community_{model}.csv')
    plot_confidence(df, 'ecm_sqrt', model)
    plot_confidence(df, 'log_probability', model)


if __name__ == '__main__':
    parser = ArgumentParser(description='Corre el modelo WHR sobre un dataset en CSV.')
    parser.add_argument('-r', '--run', dest='run', default=False, action='store_true')
    parser.add_argument('-p', '--plot', dest='plot', default=False, action='store_true')
    args = parser.parse_args()
    if args.run:
        print("Running")
        run_all(result_logit, 'logit')
        run_all(result_probit, 'probit')
    if args.plot:
        print("Plotting")
        plot_all('logit')
        plot_all('probit')
