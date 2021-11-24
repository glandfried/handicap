from math import exp
import pandas as pd
import matplotlib.pyplot as plt
from bisect import bisect_left

from estimations.run_whr import WHRRunner, COLUMNS
from figures.learning_curve import plot
from figures.whr_big_community import create_community_dataset, result_logit, result_probit
from argparse import ArgumentParser

MIDDLE = 500
MAXIMUM = 800
SLOPE = 0.0075
N = 1000


def skill(experience, middle, maximum, slope):
    return maximum / (1 + exp(slope * (-experience + middle))) - maximum/2


def run(opponents_diff, repetitions, dynamic_factor, result_fn, player_matches=10):
    opponents_true_skill = range(-int(MAXIMUM * 0.7), int(MAXIMUM * 0.7), opponents_diff)
    pretrain_df = create_community_dataset(opponents_true_skill, repetitions, result_fn, player_matches)
    player_skill = [skill(i, MIDDLE, MAXIMUM, SLOPE) for i in range(N + 1)]

    def near_opponents(s):
        binary_searched = bisect_left(opponents_true_skill, s)
        return [min(binary_searched, len(opponents_true_skill)-1)]

    history = [
        ("p", f"o{o}", 0, result_fn(
            player_skill[day],
            opponents_true_skill[o]), day)
        for day in range(1, N+1)
        for o in near_opponents(player_skill[day])
    ]
    df = pd.concat([pretrain_df, pd.DataFrame(history, columns=COLUMNS)])
    runner = WHRRunner(df, 0.0, dynamic_factor)
    runner.iterate()
    lc = runner.learning_curves()

    player_lc = lc[lc['player'] == "p"].sort_values('day')
    return player_lc


def save_lcs(player_lcs, subcase):
    for run_number, lc in enumerate(player_lcs):
        lc['run_number'] = run_number
    pd.concat(player_lcs).to_csv(f'estimations/whr/skill_evolution_{subcase}.csv', index=False)


def plot_lcs(subcase):
    df = pd.read_csv(f'estimations/whr/skill_evolution_{subcase}.csv')
    plt.figure()
    plt.plot(range(1, N+1), [skill(i, MIDDLE, MAXIMUM, SLOPE) for i in range(N)], label="Habilidad real")
    for run_number, lc in df.groupby('run_number'):
        plot(lc, 'day', [('Habilidad estimada', 'p')])
    plt.grid()
    plt.savefig(f'figures/whr/skill_evolution_{subcase}.pdf')
    plt.show()


if __name__ == '__main__':
    parser = ArgumentParser(description='Corre el modelo WHR sobre un dataset en CSV.')
    parser.add_argument('-r', '--run', dest='run', default=False, action='store_true')
    parser.add_argument('-p', '--plot', dest='plot', default=False, action='store_true')
    args = parser.parse_args()
    if args.run:
        print("Running")
        for w2 in [14.0, 36.0, 64.0, 100.0]:
            save_lcs([run(20, 40, w2, result_logit) for _ in range(10)], f'dynamic_{w2}_logit')
            save_lcs([run(20, 40, w2, result_probit) for _ in range(10)], f'dynamic_{w2}_probit')
    if args.plot:
        print("Plotting")
        for w2 in [14.0, 36.0, 64.0, 100.0]:
            plot_lcs(f'dynamic_{w2}_logit')
            plot_lcs(f'dynamic_{w2}_probit')
