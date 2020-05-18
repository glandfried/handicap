import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
sys.path.append('../software')
import trueskill as th

from importlib import reload  # Python 3.4+ only.
reload(th)
env = th.TrueSkill(draw_probability=0)



"""
Conlusi\'on 1):
    Hay un comportamiento diferente en el uso del handicap 9, es el m\'as usado.
    Y junto a esto su valor inferiror estimado es inferior a lo esperado seg\'un
    los otros handicaps.
        El handicap 9 es el m\'aximo handicap para tableros de 9x9. Por lo que es
        asignado a jugadores que necesitan handicap de 9 hasta \infty. Por lo tanto,
        la estimaci\'on de handicap 9x9 est\'a promediando la habilidad que le agrega 
        a al conjunto de esos jugadores.
"""

df = pd.read_csv('../data/ogs/summary_filtered.csv')
tsh_ogs = pd.read_csv('../estimations/ogs/tsh.csv')
tsh_all_ogs = pd.read_csv('../estimations/ogs/tsh_all.csv')

log_evidence = np.sum(np.log(tsh_ogs[tsh_ogs.estimated].evidence))
mean_log_evidence = log_evidence/sum(tsh_ogs.estimated)
np.exp(mean_log_evidence)

log_evidence_all = np.sum(np.log(tsh_all_ogs[tsh_all_ogs.estimated].evidence))
mean_log_evidence_all = log_evidence_all/sum(tsh_all_ogs.estimated)
np.exp(mean_log_evidence_all)


evidence = list(filter(lambda x: not x is None, list(map(lambda x:  x['evidence'] if x['estimated'] else None ,games_sorted ))))
evidence_woh = list(filter(lambda x: not x is None, list(map(lambda x:  x['evidence_woh'] if x['estimated'] else None ,games_sorted ))))

plt.hist(evidence,alpha=0.3)
plt.hist(evidence_woh ,alpha=0.3)
#games_sorted[1096]

10**(np.sum(np.log10(evidence))/len(evidence))
10**(np.sum(np.log10(evidence_woh))/len(evidence_woh))
"""
Gano en todos los escenarios posibles.
Los escenarios los defino ac\'a abajo
"""

diferentes = list(filter(lambda x: x[1]>4,dif))
activos = list(filter(lambda x: x[1]>20,act))

len(diferentes )
len(activos)

jugadores = set(map(lambda x: x[0], diferentes)).intersection(set(map(lambda x: x[0], activos)))

len(jugadores)


games_jugadores = list(filter(lambda x: x['white'] in jugadores or x['black'] in jugadores ,  games_sorted))
len(games_jugadores )

evidence = sum(map(lambda x:  np.log10(x['evidence']) if x['estimated'] else 0 ,games_jugadores))
evidence_woh = sum(map(lambda x:  np.log10(x['evidence_woh']) if x['estimated'] else 0 ,games_jugadores ))
cantidad = sum(map(lambda x:  1 if x['estimated'] else 0 ,games_jugadores ))

print(10**(evidence/cantidad), 10**(evidence_woh/cantidad))


evidence = sum(map(lambda x:  np.log10(x['evidence']) if x['estimated'] else 0 ,games_sorted ))
evidence_woh = sum(map(lambda x:  np.log10(x['evidence_woh']) if x['estimated'] else 0 ,games_sorted ))
cantidad = sum(map(lambda x:  1 if x['estimated'] else 0 ,games_sorted ))

print(10**(evidence/cantidad), 10**(evidence_woh/cantidad))

#jugadores = set(map(lambda x: x['id'], games_sorted ))
#losQueJueganConHandicap =  filter(lambda x: x[1]>10, list(map(lambda j: (j,sum(map(lambda g: 1 if g['id']==j and g['handicap'] != 0 else 0 , games_sorted))) , jugadores) ))
