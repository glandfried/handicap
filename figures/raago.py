import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from figures.learning_curve import plot
from os.path import join
from os import makedirs
from estimations.raago_tobi.evidence import evidence
import numpy as np
from datetime import date, timedelta

LC_FILENAME = "estimations/raago_tobi/posteriors.csv"
ORIGINAL_FILENAME = "data/aago/aago_original_filtered.csv"
OUT_DIR = "figures/raago/"

LAPLAGNE_ID = 7
GUTIERREZ_ID = 13
PLAYER_IDS = [LAPLAGNE_ID, GUTIERREZ_ID]


def main():
    # plt.rcParams["date.autoformatter.day"] = "%Y-%m-%d"
    makedirs(OUT_DIR, exist_ok=True)
    df = pd.read_csv(LC_FILENAME)
    first_day = date.fromisoformat(pd.read_csv(ORIGINAL_FILENAME)["end_date"].min())
    df["date"] = df["day"].apply(lambda day: first_day + timedelta(days=day-1))
    plot_lcs(df)
    plot_probability(df)


def plot_probability(df):
    gutierrez_lc = df[df["player"] == GUTIERREZ_ID][["day", "mu", "sigma"]].set_index("day").sort_index()
    laplagne_lc = df[df["player"] == LAPLAGNE_ID][["day", "mu", "sigma"]].set_index("day").sort_index()
    join_lc = gutierrez_lc.join(laplagne_lc, how="outer", lsuffix="_gutierrez", rsuffix="_laplagne")
    inter = join_lc.interpolate("index").reset_index()

    def get_evidence(row):
        return evidence(row["mu_laplagne"], row["sigma_laplagne"], row["mu_laplagne"], row["sigma_laplagne"], 0, 0, 'B')

    inter["evidence"] = inter.apply(get_evidence, axis=1)
    first_day = date.fromisoformat(pd.read_csv(ORIGINAL_FILENAME)["end_date"].min())
    inter["date"] = inter["day"].apply(lambda day: first_day + timedelta(days=day-1))
    inter['date'] = pd.to_datetime(inter['date'], format='%Y-%m-%d')
    plt.figure()
    plt.grid()
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.ylim(0, 1)
    plt.title("Probabilidad de que Laplagne gane en una partida frente a Gutierrez")
    plt.ylabel("Probabilidad")
    plt.xlabel("Tiempo")
    plt.xticks(rotation=30)
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    plt.plot(inter["date"], inter["evidence"], marker='.')
    plt.savefig(join(OUT_DIR, "laplagne_gutierrez_probability.pdf"))


def plot_lcs(df):
    df["mean"] = df["mu"]
    df["variance"] = df["sigma"]**2
    players_lc = df[df["player"].isin(PLAYER_IDS)]
    plt.figure()
    plt.axhspan(1, -1, color="grey")
    plot(players_lc, "date", [("Laplagne", LAPLAGNE_ID), ("Gutierrez", GUTIERREZ_ID)])
    plt.title("Curvas de aprendizaje de jugadores, con área de un desvio estándar")
    plt.ylabel("Habilidad (escala RAAGo con kyu/dan)")
    plt.xlabel("Tiempo")
    plt.legend()
    plt.xticks(rotation=30)
    plt.grid()
    plt.yticks(range(-5, 4))
    plt.show()
    plt.savefig(join(OUT_DIR, "laplagne_gutierrez_lc.pdf"))


if __name__ == "__main__":
    main()
