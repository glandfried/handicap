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
ts_ogs = pd.read_csv('../estimations/ogs/ts.csv')
ts_all_ogs = pd.read_csv('../estimations/ogs/ts_all.csv')
ttt_ogs = pd.read_csv('../estimations/ogs/ttt.csv')


log_evidence_ts = np.sum(np.log(ts_ogs[ts_ogs.estimated].evidence))
mean_log_evidence_ts = log_evidence_ts/sum(ts_ogs.estimated)
np.exp(mean_log_evidence_ts)

log_evidence_ts_all = np.sum(np.log(ts_all_ogs[ts_all_ogs.estimated].evidence))
mean_log_evidence_ts_all = log_evidence_ts_all/sum(ts_all_ogs.estimated)
np.exp(mean_log_evidence_ts_all) 

log_evidence = np.sum(np.log(tsh_ogs[tsh_ogs.estimated].evidence))
mean_log_evidence = log_evidence/sum(tsh_ogs.estimated)
np.exp(mean_log_evidence)

log_evidence_all = np.sum(np.log(tsh_all_ogs[tsh_all_ogs.estimated].evidence))
mean_log_evidence_all = log_evidence_all/sum(tsh_all_ogs.estimated)
np.exp(mean_log_evidence_all)

log_evidence_ttt = np.sum(np.log(ttt_ogs.evidence))
mean_log_evidence_ttt = log_evidence_ttt/len(ttt_ogs.evidence)
np.exp(mean_log_evidence_ttt)

log_evidence_ttt - log_evidence_ts
log_evidence_ttt - log_evidence

log_evidence_all-log_evidence_ts_all

####
# ONly handicap 

log_evidence_ts_oh = np.sum(np.log(ts_ogs[ts_ogs.estimated&(df.handicap>1)].evidence))
mean_log_evidence_ts_oh = log_evidence_ts_oh/sum(ts_ogs.estimated&(df.handicap>1))
np.exp(mean_log_evidence_ts_oh)

log_evidence_oh = np.sum(np.log(tsh_ogs[tsh_ogs.estimated&(df.handicap>1)].evidence))
mean_log_evidence_oh = log_evidence_oh/sum(tsh_ogs.estimated&(df.handicap>1))
np.exp(mean_log_evidence_oh)



