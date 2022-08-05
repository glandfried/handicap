import pandas as pd
import matplotlib.pyplot as plt
from numpy import sqrt

def plot(data, inter_first, inter_second):
    players = [
        ("Representante mejor comunidad", "0"),
        ("Otro mejor comunidad", "1"),
        ("Otro mejor comunidad", "2"),
        ("Representante peor comunidad", "3"),
        ("Otro peor comunidad", "4"),
        ("Otro peor comunidad", "5")
    ]
    plt.figure()
    df = data[data['inters'] == inter_first]
    plot_lc(df, 'intras', players)
    plt.legend()
    plt.grid()
    plt.suptitle('Estimación de habilidad con distinta cantidad de partidas intra comunitarias', fontsize=12)
    plt.title(f'Partidas inter comunitarias: {inter_first} de {inter_first + inter_second} para la mejor comunidad ',
              fontsize=8)
    plt.xlabel('# partidas intra comunidad')
    plt.ylabel('habilidad')
    #plt.ylim([-250, 250])
    print("aca si ")
    plt.show()
    plt.savefig('../../archivos/intercomunidades/results_'+str(inter_first)+'.pdf')
    print("aca tambien")


def plot_lc(df, x_label, players):
    for label, p in players:
        dfp = df[df['id'] == p]
        plt.plot(dfp[x_label], dfp['mu'], label=label, marker='.')
        plt.fill_between(dfp[x_label],
                             dfp['mu'] - sqrt(dfp['sigma']),
                             dfp['mu'] + sqrt(dfp['sigma']),
                             alpha=0.5)


#file = "../../archivos/intercomunidades/results.csv"
file = "./results.csv"
data = pd.read_csv(file)
plot(data, 8, 10)
plot(data, 40, 50)
plot(data, 80, 100)
