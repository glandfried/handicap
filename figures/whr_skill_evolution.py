from math import exp
from random import random
import pandas as pd
import matplotlib.pyplot as plt
from bisect import bisect_left

from estimations.run_whr import WHRRunner, COLUMNS
from figures.learning_curve import plot

MIDDLE = 500
MAXIMUM = 800
SLOPE = 0.0075
N = 1000
PERFORMANCE_SCALE = 160


def skill(experience, middle, maximum, slope):
    return maximum / (1 + exp(slope * (-experience + middle))) - maximum/2


# def performance(skills, size=1):
#     return normal(scale=PERFORMANCE_SCALE, size=size) + skills
def logistic(elo1, elo2):
    gamma1 = 10 ** (elo1/400.0)
    gamma2 = 10 ** (elo2/400.0)
    return gamma1 / (gamma1 + gamma2)


def result(elo1, elo2):
    # return 'B' if performance(skill1) > performance(skill2) else 'W'
    return 'B' if random() < logistic(elo1, elo2) else 'W'


def run(opponents_diff, repetitions, dynamic_factor, player_matches=10):
    opponents_true_skill = range(-int(MAXIMUM * 0.7), int(MAXIMUM * 0.7), opponents_diff)
    opponents_number = len(opponents_true_skill)
    pretrain = [
        (f"o{p1}", f"o{p2}", 0, result(opponents_true_skill[p1], opponents_true_skill[p2]), 0)
        for p1 in range(opponents_number)
        for p2 in range(p1 + 1, min(p1 + 1 + player_matches, opponents_number))
        for _ in range(repetitions)
        if p1 != p2
    ]
    player_skill = [skill(i, MIDDLE, MAXIMUM, SLOPE) for i in range(N + 1)]

    def near_opponents(s):
        binary_searched = bisect_left(opponents_true_skill, s)
        return [min(binary_searched, len(opponents_true_skill)-1)]

    history = [
        ("p", f"o{o}", 0, result(
            player_skill[day],
            opponents_true_skill[o]), day)
        for day in range(1, N+1)
        for o in near_opponents(player_skill[day])
    ]
    df = pd.DataFrame(pretrain + history, columns=COLUMNS)
    runner = WHRRunner(df, 0.0, dynamic_factor)
    runner.iterate()
    lc = runner.learning_curves()
    # opponents_lc = lc[lc['player'] != "p"]
    player_lc = lc[lc['player'] == "p"].sort_values('day')
    return player_lc


def plot_lcs(player_lcs, subcase):
    plt.figure()
    plt.plot(range(1, N+1), [skill(i, MIDDLE, MAXIMUM, SLOPE) for i in range(N)], label="Habilidad real")
    for lc in player_lcs:
        plot(lc, 'day', [('Habilidad estimada', 'p')])
    plt.grid()
    plt.savefig(f'figures/whr_skill_evolution_{subcase}.pdf')
    plt.show()


if __name__ == '__main__':
    plot_lcs([run(20, 40, 14.0) for _ in range(10)], 'dynamic_14')
    plot_lcs([run(20, 40, 36.0) for _ in range(10)], 'dynamic_36')
    plot_lcs([run(20, 40, 64.0) for _ in range(10)], 'dynamic_64')
