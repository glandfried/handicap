import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

from estimations.whr_aago import EXPERIMENTS, results_path
from estimations.run_whr import parse_results

DIR = 'figures/whr/aago/'


# In [22]: df[df['log_evidence'] > -2050].sort_values('log_evidence', ascending=False)
# Out[22]:
#     handicap_elo  dynamic_factor  handicap_elo_offset  log_evidence  geometric_mean
# 75            10              36                   10  -2049.196146        0.539237
# 68            10              25                   10  -2049.260631        0.539227
# 76            10              36                   15  -2049.311771        0.539218
# 69            10              25                   15  -2049.428872        0.539199
# 74            10              36                    5  -2049.447180        0.539196
# 67            10              25                    5  -2049.466247        0.539193
def plot_property(prop, prop_title):
    df = pd.read_csv(results_path())
    for offset in list(df['handicap_elo_offset'].unique()):
        data = df[df['handicap_elo_offset'] == offset]

        fig, ax = plt.subplots(figsize=(12, 9))
        sns.heatmap(data.pivot(index='handicap_elo', columns='dynamic_factor', values=prop),
                    annot=True, fmt='g', cmap="rocket_r", ax=ax)
        ax.set_title(f"{prop_title} con respecto a hiper-parámetros de WHR", fontsize=20)
        ax.set_xlabel("Factor dinámico ($Elo^2$)", usetex=True, fontsize=12)
        ax.set_ylabel("Habilidad agregada por piedra de handicap ($Elo$)", usetex=True, fontsize=12)
        fig.savefig(os.path.join(DIR, f'{prop}_offset{offset}.pdf'))


def main():
    os.makedirs(DIR, exist_ok=True)
    plot_property('log_evidence', 'log(evidencia)')
    plot_property('geometric_mean', 'Media geométrica')


if __name__ == '__main__':
    main()
