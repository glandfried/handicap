import matplotlib.pyplot as plt
import kickscore as ks
import numpy as np
import pandas as pd
import sys
sys.path.append('../software/trueskill.py/')
import trueskill as ts
import src as th
import pickle
from importlib import reload  # Python 3.4+ only.
reload(th)
env = ts.TrueSkill(draw_probability=0)
env_h = th.TrueSkill(draw_probability=0,beta=0)



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
ttt_all_ogs = pd.read_csv('../estimations/ogs/ttt_all.csv')
whr_ogs = pd.read_csv('../estimations/ogs/WHR.csv')
glicko_ogs = pd.read_csv('../estimations/ogs/glicko.csv')
with open('../estimations/ogs/ks.pickle', 'rb') as handle:
    ks_ogs = pickle.load(handle)

np.exp(np.sum(np.log(whr_ogs.evidence))/len(whr_ogs.evidence))
plt.hist(whr_ogs.evidence)

if False:
    """
    La evidencia de WHR integrando todas las hipótesis usando el modelo genertivo Thurstone (Trueskill)
    Conlcusi\'on:
        Es mucho m\'as grande que la que calcula WHR (el paquete es correcto en este punto).
    """
    env_h = th.TrueSkill(draw_probability=0,beta=0)
    data = zip(np.log(whr_ogs.w_mean[0:1000]),np.log(whr_ogs.b_mean[0:1000]),np.sqrt(whr_ogs.w_std[0:1000]),np.sqrt(whr_ogs.b_std[0:1000]),df_r.black_win[0:1000])
    games = [env_h.Game([env_h.Team([env_h.Rating(wm,ws)]),env_h.Team([env_h.Rating(bm,bs)])],[r,1-r])  for wm, bm, ws, bs, r in data]
    evidence_whr = [g.evidence for g in games ]
    """
    Marginal likelihood de WHR
    Conlcusi\'on:
        Es menor que el likelihood reportado en WHR
    """
    wm = np.log(whr_ogs.w_mean[0])
    bm = np.log(whr_ogs.b_mean[0])
    ws = np.sqrt(whr_ogs.w_std[0])
    bs = np.sqrt(whr_ogs.b_std[0])
    r = df_r.black_win[0]
    
    p_w = np.exp(wm)/(np.exp(wm)+np.exp(bm)) 
    p_b = 1-p_w 
    
    d = np.arange(-4,4,0.05)
    np.exp(wm)/(np.exp(wm)+np.exp(bm)) 
    
    dm = bm-wm
    ds = np.sqrt(ws**2 + bs**2)
    0.99999< 1-env_h.Rating(dm,ds).cdf(0,dm,ds)
    
    1/(1+np.exp(-dm)) == whr_ogs.evidence[0]
    
    d = np.arange(-4,4,0.01)
    import scipy.stats as stats
    MAP = d[np.argmax((1/(1+np.exp(-d))) * stats.norm.pdf(d,dm,ds))]
    marginal_likelihhod_whr = np.sum((1/(1+np.exp(-d))) * stats.norm.pdf(d,dm,ds))*0.05
    marginal_likelihhod_whr < whr_ogs.evidence[0]
    #eviddencia, Es menor que el likelihood reportado en WHR
    
    def evidence_whr(wm,bm,ws,bs,r):
        dm = bm-wm if r else wm - bm
        ds = np.sqrt(ws**2 + bs**2)
        d = np.arange(-4,4,0.05)
        return np.sum((1/(1+np.exp(-d))) * stats.norm.pdf(d,dm,ds))*0.05
    
    data = zip(np.log(whr_ogs.w_mean[0:1000]),np.log(whr_ogs.b_mean[0:1000]),np.sqrt(whr_ogs.w_std[0:1000]),np.sqrt(whr_ogs.b_std[0:1000]),df_r.black_win[0:1000])
    marginal_likelihhod_whr_1000 = [ evidence_whr(wm,bm,ws,bs,r)  for wm, bm, ws, bs, r in data ]
    sum(np.array(marginal_likelihhod_whr_1000) > whr_ogs.evidence[0:1000])
    sum(whr_ogs.evidence[0:1000] < 0.5)
    
    
    """
    Curva de aprendizaje de un jugador.
    Va del m\'inimo (-5) al m\'aximo (5) de una partida a otra.
    """
    jugadores = list(set(df_r.white))[0:100]
    for i in jugadores:
        lc = [ rb if b == i else rw for rw, rb, w, b in zip(whr_ogs.w_mean,whr_ogs.b_mean,df_r.white,df_r.black ) if b == i or w ==i ]
        plt.plot(np.log(lc) )
        
    for i in jugadores:
        lc = [ rb if b == i else rw for rw, rb, w, b in zip(ttt_ogs.w_mean,ttt_ogs.b_mean,df_r.white,df_r.black ) if b == i or w ==i ]
        plt.plot(lc )
    
    for i in jugadores:
        lc = [ rb if b == i else rw for rw, rb, w, b in zip(ttt_all_ogs.w_mean,ttt_all_ogs.b_mean,df.white,df.black ) if b == i or w ==i ]
        plt.plot(lc )
    
    
    for i in jugadores:
        lc = [ rb if b == i else rw for rw, rb, w, b in zip(glicko_ogs.w_mean,glicko_ogs.b_mean,df_r.white,df_r.black ) if b == i or w ==i ]
        plt.plot(lc )
    
    for i in jugadores:
        days = ks_ogs.item[i].scores[0]
        lc = ks_ogs.item[i].predict(days)[0]
        plt.plot(lc )
    
    plt.plot(ks_ogs.item[2100].scores[0])
    plt.plot(ks_ogs.item[2100].scores[1])
    plt.plot(ks_ogs.item[2100].predict(ks_ogs.item[2100].scores[0])[0])
    
    
    sum(df.white == df.black)
    df[ttt_all_ogs.w_std<3]
    
    jugadores = list(set(df[ttt_all_ogs.w_std<3].white))[0:100]
    for j in jugadores:
        filtro = (df.white == j) | (df.black == j)
        if sum(filtro)>128:
            curva = (df.white[filtro] == j) * ttt_all_ogs[filtro].w_mean + (df.black[filtro] == j) * ttt_all_ogs[filtro].b_mean
            plt.plot(range(len(curva )) ,curva )
        plt.xlim(0,128)
            
    """
    Separa demasiado en la primera partida 
    """
    import matplotlib.pyplot as plt
    import scipy
    
    s = np.arange(-3,3,0.01)
    plt.plot(s,scipy.stats.norm.pdf(s,np.log(whr_ogs.w_mean[1]),np.sqrt(whr_ogs.w_std[1]) ))
    plt.plot(s,scipy.stats.norm.pdf(s,np.log(whr_ogs.b_mean[1]),np.sqrt(whr_ogs.b_std[1])))
    

log_evidence_glicko = np.sum(np.log([e if b else 1-e for e,b,r in zip(glicko_ogs.evidence,df.black_win,df.ranked) if r]))

log_evidence_ks = ks_ogs.log_likelihood
mean_log_evidence_ks = log_evidence_ks/sum(df_r.ranked)
np.exp(mean_log_evidence_ks )

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

log_evidence_ttt = np.sum(np.log(ttt_ogs.evidence))
mean_log_evidence_ttt = log_evidence_ttt/len(ttt_ogs.evidence)
np.exp(mean_log_evidence_ttt)

log_evidence_ttt_last = np.sum(np.log(ttt_ogs.last_evidence))
mean_log_evidence_ttt_last = log_evidence_ttt_last/len(ttt_ogs.last_evidence)
np.exp(mean_log_evidence_ttt_last)

log_evidence_ttt_all_last = np.sum(np.log(ttt_all_ogs.last_evidence))
mean_log_evidence_ttt_all_last = log_evidence_ttt_all_last /len(ttt_all_ogs.last_evidence)
np.exp(mean_log_evidence_ttt_all_last)




log_evidence_ttt_last - log_evidence
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