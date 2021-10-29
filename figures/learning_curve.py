import matplotlib.pyplot as plt
from numpy import sqrt


def plot(df, x_label, players):
    for label, p in players:
        dfp = df[df['player'] == p]
        plt.plot(dfp[x_label], dfp['mean'], label=label)
        plt.fill_between(dfp[x_label],
                         dfp['mean'] - sqrt(dfp['variance']),
                         dfp['mean'] + sqrt(dfp['variance']),
                         alpha=0.5)
