from random import random
import pandas as pd
import matplotlib.pyplot as plt

from estimations.run_whr import WHRRunner, COLUMNS
from numpy import sqrt, log, sum
from scipy.stats import norm

MAXIMUM = 400


def logistic(elo1, elo2):
    gamma1 = 10 ** (elo1/400.0)
    gamma2 = 10 ** (elo2/400.0)
    return gamma1 / (gamma1 + gamma2)


def result(elo1, elo2):
    return 'B' if random() < logistic(elo1, elo2) else 'W'


def run(opponents_diff, repetitions, player_matches=10):
    opponents_true_skill = range(-MAXIMUM, MAXIMUM, opponents_diff)
    opponents_number = len(opponents_true_skill)
    pretrain = [
        (f"o{p1}", f"o{p2}", 0, result(opponents_true_skill[p1], opponents_true_skill[p2]), 0)
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


def plot_confidence(df, col):
    stats = df.groupby('repetitions')[col].describe().reset_index()
    plt.figure()
    plt.fill_between(stats['repetitions'], stats['25%'], stats['75%'], alpha=0.5, label='Intervalo 25%/75%')
    plt.plot(stats['repetitions'], stats['50%'], label='Mediana')
    plt.legend()
    plt.xlabel('Número de repeticiones de las partidas')
    plt.ylabel(col)
    plt.savefig(f'figures/whr_big_community_{col}.pdf')


if __name__ == '__main__':
    def datum(repetitions):
        res = run(40, repetitions)
        return repetitions, ecm_sqrt(res), log_probability_skills(res)

    data = pd.DataFrame([
        datum(repetitions)
        for repetitions in range(10, 51, 10)
        for _ in range(10)
    ], columns=['repetitions', 'ecm_sqrt', 'log_probability'])

    data.to_csv('figures/whr_big_community.results.csv')

    plot_confidence(data, 'ecm_sqrt')
    plot_confidence(data, 'log_probability')
