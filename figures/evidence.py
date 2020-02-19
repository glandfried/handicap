import pickle
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('../software')
import trueskill as th

from importlib import reload  # Python 3.4+ only.
reload(th)
env = th.TrueSkill(draw_probability=0)

with open("../data/handicap.pickle",'rb') as file:
    handicap = pickle.load(file)
with open("../data/handicap_history.pickle",'rb') as file:
    handicap_history = pickle.load(file)

"""
Conlusi\'on 1):
    Hay un comportamiento diferente en el uso del handicap 9, es el m\'as usado.
    Y junto a esto su valor inferiror estimado es inferior a lo esperado seg\'un
    los otros handicaps.
    Hip\'otesis A):
        El estimador perdi\'o incertidumbre, solo 0.080, y por lo tanto se se qued\'o
        clavado en ~4.
        Soluci\'on:
            Modificar el parametro tau que agrega incertidumbre luego de cada estimaci\'on
    Hip\'otesis B):
        El handicap 9 es el m\'aximo handicap para tableros de 9x9. Por lo que es
        asignado a jugadores que necesitan handicap de 9 hasta \infty. Por lo tanto,
        la estimaci\'on de handicap 9x9 est\'a promediando la habilidad que le agrega 
        a al conjunto de esos jugadores.
        
    
"""

key_h= sorted(handicap , key= lambda x: (x[1],x[0]))

for h in range(2,10):
    plt.scatter(h,handicap[(h,19)].mu)
    
plt.plot(list(map(lambda x: x.mu, handicap_history[(2,19)] )) )
plt.plot(list(map(lambda x: x.mu, handicap_history[(3,19)] )) )
plt.plot(list(map(lambda x: x.mu, handicap_history[(4,19)] )) )
plt.plot(list(map(lambda x: x.mu, handicap_history[(5,19)] )) )
plt.plot(list(map(lambda x: x.mu, handicap_history[(6,19)] )) )
plt.plot(list(map(lambda x: x.mu, handicap_history[(7,19)] )) )
plt.plot(list(map(lambda x: x.mu, handicap_history[(8,19)] )) )
plt.plot(list(map(lambda x: x.mu, handicap_history[(9,19)] )) )


with open("../data/player_history.pickle",'rb') as file:
    player_history = pickle.load(file)

dif = list( map(lambda k: (k, max(map(lambda x: abs(x[1].mu-x[2].mu),player_history[k])) ), player_history))
act = list( map(lambda k: (k, len(player_history[k])), player_history))

player_history = None

with open("games_sorted.pickle",'rb') as file:
    games_sorted = pickle.load(file)

evidence = list(filter(lambda x: not x is None, list(map(lambda x:  x['evidence'] if x['estimated'] else None ,games_sorted ))))
evidence_woh = list(filter(lambda x: not x is None, list(map(lambda x:  x['evidence_woh'] if x['estimated'] else None ,games_sorted ))))

plt.hist(evidence,alpha=0.3)
plt.hist(evidence_woh ,alpha=0.3)
#games_sorted[1096]

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
