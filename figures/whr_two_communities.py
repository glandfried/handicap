import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser

from estimations.run_whr import WHRRunner, COLUMNS
from figures.learning_curve import plot as plot_lc

inter_community_matches = [(8, 2), (80, 20), (800, 200)]


def two_communities(players, intra_matches_number, inter_matches_first_community, inter_matches_second_community):
    intra_matches = [
        (f"c{community}p{player}", f"c{community}p{(player + 1) % players}", 0, "B", 1)
        for community in range(2)
        for _ in range(intra_matches_number)
        for player in range(players)
    ]
    inter_matches = [
        (f"c0p0", f"c1p0", 0, result, 1)
        for result in (['B'] * inter_matches_first_community + ['W'] * inter_matches_second_community)
    ]
    return pd.DataFrame(intra_matches + inter_matches, columns=COLUMNS)


def different_intra_experiment(max_intra, inter_first, inter_second, show=False):
    results = []
    intra_range = range(1, max_intra+1)
    for intra in intra_range:
        dataset = two_communities(3, intra, inter_first, inter_second)
        runner = WHRRunner(dataset, 0, 14.0, len(dataset))
        runner.iterate()
        lc = runner.learning_curves()
        lc['intra'] = [intra] * len(lc)
        results.append(lc)
    return pd.concat(results)


def plot(df, inter_first, inter_second):
    players = [
        ("Representante mejor comunidad", "c0p0"),
        ("Otro mejor comunidad", "c0p1"),
        ("Representante peor comunidad", "c1p0"),
        ("Otro peor comunidad", "c1p1")
    ]
    plt.figure()
    plot_lc(df, 'intra', players)
    plt.legend()
    plt.grid()
    plt.suptitle('Estimación de habilidad con distinta cantidad de partidas intra comunitarias', fontsize=12)
    plt.title(f'Partidas inter comunitarias: {inter_first} de {inter_first + inter_second} para la mejor comunidad ',
              fontsize=8)
    plt.xlabel('# partidas intra comunidad')
    plt.ylabel('habilidad (elo)')
    plt.ylim([-250, 250])
    plt.savefig(f'figures/whr/two_communities_{inter_first}-{inter_first + inter_second}.pdf')


def run_all():
    for inter_first, inter_second in inter_community_matches:
        different_intra_experiment(40, inter_first, inter_second)\
            .to_csv(f'estimations/whr/two_communities_{inter_first}-{inter_second}.csv')


def plot_all():
    for inter_first, inter_second in inter_community_matches:
        df = pd.read_csv(f'estimations/whr/two_communities_{inter_first}-{inter_second}.csv')
        plot(df, inter_first, inter_second)


if __name__ == '__main__':
    parser = ArgumentParser(description='Corre el modelo WHR sobre un dataset en CSV.')
    parser.add_argument('-r', '--run', dest='run', default=False, action='store_true')
    parser.add_argument('-p', '--plot', dest='plot', default=False, action='store_true')
    args = parser.parse_args()
    if args.run:
        print("Running")
        run_all()
    if args.plot:
        print("Plotting")
        plot_all()
