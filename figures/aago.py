import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Polygon
from itertools import groupby

df = pd.read_csv('../data/aago/summary_filtered.csv')
data = pd.read_csv('../estimations/aago/ttt_all.csv')
# Opening JSON file 
sum(df.id != data.id)

np.exp(np.sum(np.log(data.evidence))/len(data.evidence))
np.exp(np.sum(np.log(data.last_evidence))/len(data.evidence))

"""
TODO:
    1. por qu\'e last evidence es igual a evidence.
"""

df.columns 
players = list(df.black_player_id) + list(df.black_player_id)
activity = [(i, players.count(i)) for i in set(players)]

filtro = (df.white_player_id == 53) | (df.black_player_id == 53)
data[filtro]

for j,a in activity:
    filtro = (df.white_player_id == j) | (df.black_player_id == j)
    if a>20:
        curva = (df.white_player_id[filtro] == j) * data[filtro].w_mean + (df.black_player_id[filtro] == j) * data[filtro].b_mean
        plt.plot(range(len(curva )) ,curva )
    #plt.xlim(0,128)
    
filtro = (df.handicap == 3)
plt.plot(data[filtro].h_mean)

for h in range(2,10):
    filtro = (df.handicap == h)
    plt.plot(range(sum(filtro)) ,data[filtro].h_mean)
    
    