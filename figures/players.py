import pickle
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('../software')
import trueskill as th

from importlib import reload  # Python 3.4+ only.
reload(th)
env = th.TrueSkill(draw_probability=0)

"""
Observaci\'on: 
    Se da m\'as handicap a gente nueva que nunca jug\'o antes, que a gente que
    viene juugando.
Consecuencia:
    Esto har\'ia m\'as dif\'ícil estimar el handicap.
"""

with open("../data/player_history.pickle",'rb') as file:
    player_history = pickle.load(file)


last_dif_active_non0 = list(filter(lambda x: x[1]!= 0, last_dif_active  ))

last_dif = list( map(lambda k: (k, player_history[k][-1][1].mu-player_history[k][-1][2].mu,len(player_history[k]),player_history[k][-1][1].sigma-player_history[k][-1][2].sigma,player_history[k][-1][2].sigma), player_history))

last_dif_estimated = list(filter(lambda x: x[-1]< 2, last_dif ))
last_dif_active = list(filter(lambda x: x[2]> 20, last_dif ))
len(last_dif_active )

len(last_dif_estimated )
len(last_dif_estimated )
len(last_dif )

player_summary = np.array(last_dif)

last_dif_active_non0 = list(filter(lambda x: x[1]!= 0, last_dif_active  ))

len(last_dif_active_non0 )/len(last_dif_active )