import pandas as pd 

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


file = "../../archivos/intercomunidades/results.csv"
df = pd.read_csv(file)
plot(df, 0, 3)