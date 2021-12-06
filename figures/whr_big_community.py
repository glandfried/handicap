from random import random, seed
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from numpy import sqrt
import math
from numpy.random import normal
from scipy.stats import norm
from argparse import ArgumentParser

from estimations.run_whr import WHRRunner, COLUMNS

MAXIMUM = 400
PERFORMANCE_SCALE = 200

EXPERIMENTS_PARAMS = [
    (r, i)
    for r in range(10, 101, 10)
    for i in range(20)
]


def save_file_name(model, repetitions, i):
    return f'estimations/whr/big_community/{model}_rep{repetitions}_{i}.csv'


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


def create_community_dataset(opponents_true_skill, repetitions, result_fn, player_matches=10):
    opponents_number = len(opponents_true_skill)
    pretrain = [
        (f"o{p1}", f"o{p2}", 0, result_fn(opponents_true_skill[p1], opponents_true_skill[p2]), 0)
        for p1 in range(opponents_number)
        for p2 in range(p1+1, min(p1+1+player_matches, opponents_number))
        for _ in range(repetitions)
        if p1 != p2
    ]

    return pd.DataFrame(pretrain, columns=COLUMNS)


def run(opponents_diff, repetitions, result_fn, player_matches=10):
    opponents_true_skill = range(-MAXIMUM, MAXIMUM + 1, opponents_diff)
    df = create_community_dataset(opponents_true_skill, repetitions, result_fn, player_matches)
    runner = WHRRunner(df)
    runner.iterate()
    lc = runner.learning_curves()
    lc['skill'] = opponents_true_skill

    return lc


def ecm_sqrt(df):
    return sqrt(((df['skill'] - df['mean']) ** 2).mean())


def neigh_distances(df):
    def distance(p1, p2):
        return df[df['player'] == p2]['mean'].iloc[0] - df[df['player'] == p1]['mean'].iloc[0]

    return [
        distance(f"o{i}", f"o{i+1}")
        for i in range(len(df)-1)
    ]


def plot_confidence(df, col, model):
    stats = df.groupby('repetitions')[col].describe().reset_index()
    plt.figure()
    plt.fill_between(stats['repetitions'], stats['25%'], stats['75%'], alpha=0.5, label='Intervalo 25%/75%')
    plt.plot(stats['repetitions'], stats['50%'], label='Mediana')
    plt.legend()
    plt.xlabel('Número de repeticiones de las partidas')
    plt.ylabel(col)
    plt.savefig(f'figures/whr/big_community_{col}_{model}.pdf')


def histogram(df, col, model):
    df_filter = (df['repetitions'] % 30) == 10
    axs = df[df_filter].hist(column=col, by='repetitions', layout=(2, 2),
                             sharex=True, density=True).ravel()
    for ax in axs:
        ax.grid(True, axis='x')
        ax.xaxis.set_major_locator(ticker.MultipleLocator(40))
        ax.yaxis.set_ticks([])
    axs[0].get_figure().savefig(f'figures/whr/big_community_{col}_{model}.pdf')


def real_estimated_skills(dfs, model):
    # Cada fila tiene 'skill' la habilidad real, 'mean' y 'variance' de la normal estimada
    fig, axs = plt.subplots(len(dfs), sharex=True, figsize=(12, 12))
    for (rep, df), ax in zip(dfs, axs):
        for i, row in df.iterrows():
            loc = row['mean']
            scale = math.sqrt(row['variance'])
            d = 3 * scale
            x = range(int(loc - d), int(loc + d))
            line, = ax.plot(x, norm.pdf(x, loc, scale))
            ax.axvline(row['skill'], color=line.get_color())
            ax.set_title(rep)
    fig.savefig(f'figures/whr/big_community_estimations_{model}.pdf')


def run_all(result_fn, model):
    for repetitions, i in EXPERIMENTS_PARAMS:
        run(40, repetitions, result_fn).to_csv(save_file_name(model, repetitions, i), index=False)


def plot_all(model):
    dfs = [
        (repetitions, pd.read_csv(save_file_name(model, repetitions, i)))
        for repetitions, i in EXPERIMENTS_PARAMS
    ]
    re_dfs = [
        (repetitions, df[df['player'].isin([f'o{i}' for i in range(0, 20, 2)])])
        for i, (repetitions, df) in enumerate(dfs)
        if (repetitions % 30) == 10 and (i % 20) == 0
    ]
    real_estimated_skills(re_dfs, model)

    ecm_dfs = pd.DataFrame([
        (repetitions, ecm_sqrt(df))
        for repetitions, df in dfs
    ], columns=['repetitions', 'ecm_sqrt'])
    plot_confidence(ecm_dfs, 'ecm_sqrt', model)

    neigh_distance_dfs = pd.DataFrame([
        (repetitions, d)
        for repetitions, df in dfs
        for d in neigh_distances(df)
    ], columns=['repetitions', 'neigh_distance'])
    histogram(neigh_distance_dfs, 'neigh_distance', model)


if __name__ == '__main__':
    seed(1234)
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
