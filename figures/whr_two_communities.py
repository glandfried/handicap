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


def different_intra_experiment(max_intra, show=False):
    results = []
    for intra in range(1, max_intra+1):
        runner = WHRRunner(14.0, 0, two_communities(3, intra, 80, 20), 100000)
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
    plt.title('Partidas inter comunitarias: 8 de 10 para la mejor comunidad ', fontsize=8)
    plt.xlabel('# partidas intra comunidad')
    plt.ylabel('habilidad (elo)')
    if show:
        plt.show()
    else:
        plt.savefig('figures/two_communities.png')


if __name__ == '__main__':
    different_intra_experiment(20)
