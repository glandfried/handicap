from estimations.run_whr import WHRRunner, COLUMNS
import pandas as pd
import matplotlib.pyplot as plt
from learning_curve import plot


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
    df = pd.concat(results)
    players = [
        ("Representante mejor comunidad", "c0p0"),
        ("Otro mejor comunidad", "c1p0"),
        ("Representante peor comunidad", "c0p1"),
        ("Otro peor comunidad", "c1p1")
    ]
    plt.figure()
    plot(df, 'intra', players)
    plt.legend()
    plt.grid()
    plt.suptitle('Estimación de habilidad con distinta cantidad de partidas intra comunitarias', fontsize=12)
    plt.title(f'Partidas inter comunitarias: {inter_first} de {inter_first + inter_second} para la mejor comunidad ',
              fontsize=8)
    plt.xlabel('# partidas intra comunidad')
    plt.ylabel('habilidad (elo)')
    plt.xticks(intra_range)
    plt.ylim([-150, 150])
    if show:
        plt.show()
    else:
        plt.savefig(f'figures/two_communities_{inter_first}-{inter_first + inter_second}.pdf')


if __name__ == '__main__':
    different_intra_experiment(20, 8, 2)
    different_intra_experiment(20, 80, 20)
