import matplotlib.pyplot as plt
import pandas as pd
import os

from estimations.whr_aago import lc_path
from figures.learning_curve import plot

DIR = 'figures/whr/aago/'
PLAYERS = [222, 176, 218]


def create_plot(handicap_elo, dynamic_factor, handicap_elo_offset):
    df = pd.read_csv(lc_path(handicap_elo, dynamic_factor, handicap_elo_offset))
    sorted_players = list(df.sort_values('mean')['player'].unique())
    players = PLAYERS + sorted_players[:3] + sorted_players[-3:]
    print(players)
    plot(df, 'day', zip(map(str, players), players))
    plt.legend()
    plt.show()


def main():
    os.makedirs(DIR, exist_ok=True)
    create_plot(0, 36, 0)
    create_plot(20, 36, 0)
    create_plot(40, 36, 0)


if __name__ == '__main__':
    main()
