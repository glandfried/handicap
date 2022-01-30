import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

from estimations.whr_aago import EXPERIMENTS, results_path
from estimations.run_whr import parse_results

DIR = 'figures/whr/aago/'


def plot_property(prop, prop_title):
    data = pd.read_csv(results_path())

    fig, ax = plt.subplots(figsize=(12, 9))
    sns.heatmap(data.pivot(index='handicap_elo', columns='dynamic_factor', values=prop),
                annot=True, fmt='g', cmap="rocket_r", ax=ax)
    ax.set_title(f"{prop_title} con respecto a hiper-parámetros de WHR", fontsize=20)
    ax.set_xlabel("Factor dinámico ($Elo^2$)", usetex=True, fontsize=12)
    ax.set_ylabel("Habilidad agregada por piedra de handicap ($Elo$)", usetex=True, fontsize=12)
    fig.savefig(os.path.join(DIR, f'{prop}.pdf'))


def main():
    os.makedirs(DIR, exist_ok=True)
    plot_property('log_evidence', 'log(evidencia)')
    plot_property('geometric_mean', 'Media geométrica')


if __name__ == '__main__':
    main()
