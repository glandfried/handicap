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
df_r = df[df.ranked].copy()
df_r = df_r.reset_index()

tsh_ogs = pd.read_csv('../estimations/ogs/tsh.csv')
tsh_all_ogs = pd.read_csv('../estimations/ogs/tsh_all.csv')
ts_ogs = pd.read_csv('../estimations/ogs/ts.csv')
ts_all_ogs = pd.read_csv('../estimations/ogs/ts_all.csv')
ttt_ogs = pd.read_csv('../estimations/ogs/ttt.csv')
whr_ogs = pd.read_csv('../estimations/ogs/WHR.csv')

np.exp(np.sum(np.log(whr_ogs.evidence))/len(whr_ogs.evidence))
plt.hist(whr_ogs.evidence)

if False:
    """
    Curva de aprendizaje de un jugador.
    Va del m\'inimo (-5) al m\'aximo (5) de una partida a otra.
    """
    lc = [ rb if b == 2100 else rw for rw, rb, w, b in zip(whr_ogs.w_mean,whr_ogs.b_mean,df_r.white,df_r.black ) if b == 2100 or w ==2100 ]
    plt.plot(np.log(lc) )

np.min(np.log(whr_ogs.w_mean))


log_evidence_ts = np.sum(np.log(ts_ogs[ts_ogs.estimated].evidence))
mean_log_evidence_ts = log_evidence_ts/sum(ts_ogs.estimated)
np.exp(mean_log_evidence_ts)

log_evidence_ts_all = np.sum(np.log(ts_all_ogs[ts_all_ogs.estimated].evidence))
mean_log_evidence_ts_all = log_evidence_ts_all/sum(ts_all_ogs.estimated)
np.exp(mean_log_evidence_ts_all) 

log_evidence = np.sum(np.log(tsh_ogs[tsh_ogs.estimated].evidence))
mean_log_evidence = log_evidence/sum(tsh_ogs.estimated)
np.exp(mean_log_evidence)

log_evidence - log_evidence_ts

log_evidence_all = np.sum(np.log(tsh_all_ogs[tsh_all_ogs.estimated].evidence))
mean_log_evidence_all = log_evidence_all/sum(tsh_all_ogs.estimated)
np.exp(mean_log_evidence_all)

log_evidence_ttt = np.sum(np.log(ttt_ogs.evidence))
mean_log_evidence_ttt = log_evidence_ttt/len(ttt_ogs.evidence)
np.exp(mean_log_evidence_ttt)

log_evidence_ttt - log_evidence_ts
log_evidence_ttt - log_evidence

log_evidence_all-log_evidence_ts_all

(mean_log_evidence_ts - mean_log_evidence)*sum(ts_ogs.estimated)


np.exp(mean_log_evidence_ttt) - np.exp(mean_log_evidence)

plt.hist(ts_ogs[ts_ogs.estimated].evidence-tsh_ogs[tsh_ogs.estimated].evidence,bins=np.arange(-0.05,0.05,0.001))
plt.axvline(x=0,color="black")

plt.hist(ttt_ogs.evidence-tsh_ogs[tsh_ogs.estimated].evidence,bins=np.arange(-1,1,0.05))
plt.axvline(x=0,color="black")

plt.hist(ttt_ogs.evidence)
plt.hist(tsh_ogs[tsh_ogs.estimated].evidence)

####
# ONly handicap 

log_evidence_ts_oh = np.sum(np.log(ts_ogs[ts_ogs.estimated&(df.handicap>1)].evidence))
mean_log_evidence_ts_oh = log_evidence_ts_oh/sum(ts_ogs.estimated&(df.handicap>1))
np.exp(mean_log_evidence_ts_oh)

log_evidence_oh = np.sum(np.log(tsh_ogs[tsh_ogs.estimated&(df.handicap>1)].evidence))
mean_log_evidence_oh = log_evidence_oh/sum(tsh_ogs.estimated&(df.handicap>1))
np.exp(mean_log_evidence_oh)

log_evidence_ttt_oh = np.sum(np.log(ttt_ogs.evidence[df_r.handicap>1]))
mean_log_evidence_ttt_oh = log_evidence_ttt_oh/len(ttt_ogs.evidence[df_r.handicap>1])
np.exp(mean_log_evidence_ttt_oh)

log_evidence_ttt_oh - log_evidence_oh 
log_evidence_ttt_oh - log_evidence_ts_oh 

###
# TTT: revisiting the history f chess

chess_games  = 3505366

chess_l_ttt = -3953997
mean_chess_l_ttt  =  chess_l_ttt/chess_games  
np.exp( mean_chess_l_ttt  )

chess_l_naive = -4228005
mean_chess_l_naive =  chess_l_naive /chess_games  
np.exp(mean_chess_l_naive )

np.exp( mean_chess_l_ttt  )- np.exp(mean_chess_l_naive )

chess_l_tttd = -3661813
mean_chess_l_tttd  =  chess_l_tttd/chess_games  
np.exp(mean_chess_l_tttd  )

np.exp(mean_chess_l_tttd  )-np.exp(mean_chess_l_naive )
np.exp(mean_chess_l_tttd  ) - np.exp( mean_chess_l_ttt  )