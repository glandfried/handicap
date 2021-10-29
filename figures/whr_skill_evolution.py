from math import exp
from numpy.random import normal
import pandas as pd
import matplotlib.pyplot as plt
from estimations.run_whr import WHRRunner, COLUMNS
from bisect import bisect_left
from learning_curve import plot

MIDDLE = 500
MAXIMUM = 800
SLOPE = 0.0075
N = 1000
PERFORMANCE_SCALE = 160


def skill(experience, middle, maximum, slope):
    return maximum / (1 + exp(slope * (-experience + middle))) - maximum/2


def performance(skills, size=1):
    return normal(scale=PERFORMANCE_SCALE, size=size) + skills


def result(skill1, skill2):
    # TODO: probar usando logit en vez de probit, viendo el calculo exacto que hace el paquete
    return 'B' if performance(skill1) > performance(skill2) else 'W'


def main(opponents_diff, repetitions):
    opponents_true_skill = range(-MAXIMUM//2, MAXIMUM//2, opponents_diff)
    opponents_number = len(opponents_true_skill)
    pretrain = [
        (f"o{p1}", f"o{p2}", 0, result(opponents_true_skill[p1], opponents_true_skill[p2]), 0)
        for p1 in range(opponents_number)
        for p2 in range(opponents_number)
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
    runner = WHRRunner(df, 0.0, 14.0, 10000)
    runner.iterate()
    lc = runner.learning_curves()
    opponents_lc = lc[lc['player'] != "p"]
    player_lc = lc[lc['player'] == "p"].sort_values('day')
    # print(opponents_lc.sort_values('mean'))
    plt.figure()
    plt.plot(range(1, N+1), [skill(i, MIDDLE, MAXIMUM, SLOPE) for i in range(N)], label="Habilidad real")
    plot(player_lc, 'day', [('Habilidad estimada', 'p')])
    plt.grid()
    plt.legend()
    plt.savefig('figures/whr_skill_evolution.pdf')
    plt.show()


if __name__ == '__main__':
    main(20, 4)
