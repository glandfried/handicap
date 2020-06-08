import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Polygon
from itertools import groupby
import sys
sys.path.append('../software/trueskill.py/')
import src as th
env = th.TrueSkill(draw_probability=0,tau=1,beta=4.33,epsilon=0.1)


df = pd.read_csv('../data/aago/summary_filtered.csv')
#df.columns
data = pd.read_csv('../estimations/aago/ttt_all.csv')
# Opening JSON file 
sum(df.id != data.id)
sum(df.white_player_id != data.w_id)


def evidencia_promedio(xs):
    return np.exp(np.sum(np.log(xs))/len(xs))

evidencia_promedio(data.evidence)
evidencia_promedio(data.last_evidence)
evidencia_promedio(data.evidence[df.handicap>1])
evidencia_promedio(data.last_evidence[df.handicap>1])

"""
Resumen:
"""

from collections import defaultdict
res= defaultdict(lambda: {"mu":[],"sigma":[],"evento":[], "mu_p":[], "sigma_p":[]} )
for i in range(len(data.id)):#i=0
    e = df.event_id[i]
    w = data.w_id[i]
    b = data.b_id[i]
    h = df.handicap[i]
    if not e in res[w]["evento"]:
        res[w]["mu"].append(data.w_mean[i])
        res[w]["sigma"].append(data.w_std[i])
        res[w]["mu_p"].append(data.w_mean_prior[i])
        res[w]["sigma_p"].append(data.w_std_prior[i])
        res[w]["evento"].append(e)
    if not e in res[b]["evento"]:
        res[b]["mu"].append(data.b_mean[i])
        res[b]["sigma"].append(data.b_std[i])
        res[b]["mu_p"].append(data.b_mean_prior[i])
        res[b]["sigma_p"].append(data.b_std_prior[i])
        res[b]["evento"].append(e)
    if h > 1 and (not e in res[(h,19)]["evento"]):
        res[(h,19)]["mu"].append(data.h_mean[i])
        res[(h,19)]["sigma"].append(data.h_std[i])
        res[(h,19)]["mu_p"].append(data.h_mean_prior[i])
        res[(h,19)]["sigma_p"].append(data.h_std_prior[i])
        res[(h,19)]["evento"].append(e)
res = dict(res)

"""
Visualizaci\'on de curvas de aprendizaje
"""

diff = 0
for k in res:
    if not "(" in str(k):  plt.plot(res[k]["mu"])
    diff = max(abs(res[k]["mu"][-1]-res[k]["mu"][0]),diff)
    #plt.xlim(0,128)

for k in res:
    if not "(" in str(k):  plt.plot(res[k]["mu_p"])

    
for k in res:
    if "(" in str(k): plt.plot(res[k]["mu"])
    #plt.xlim(0,128)    



for k in res:
    if not "(" in str(k):  plt.plot(res[k]["sigma_p"])


"""
TODO:
    evidencia a priori en paquete    
"""
results = list(df.result.map(lambda x: [1,0] if x=="black" else [0,1] ) )
evidence_forward_prior = []
for i in range(len(df.id)):
    tw = env.Team([env.Rating(data.w_mean_prior[i],data.w_std_prior[i])])
    tb = [env.Rating(data.b_mean_prior[i],data.b_std_prior[i])]
    if df.handicap[i] > 1:
        tb = env.Team(tb)
    else:
        tb = tb + [env.Rating(data.h_mean_prior[i],data.h_std_prior[i],beta=0,noise=0)]
        tb = env.Team(tb)
    evidence_forward_prior.append(env.Game([tw,tb],results[i]).evidence)
     
plt.plot(np.exp(np.cumsum(np.log(evidence_forward_prior))/np.arange(1,len(evidence_forward_prior)+1)))
evidencia_promedio(evidence_forward_prior)

"""
Pregunta:
    Est\'an bien elegidos los handicap?
"""
filtro = (df.handicap>1) & (data.w_std_prior < 5) & (data.b_std_prior < 5)

sum(df[filtro].result=="white")/sum(filtro)


fit_handicap = [-0.53445148,  0.82848756] 
hs = fit_handicap[0] + fit_handicap[1]*np.arange(0,10) 
h_option = np.arange(0,10)
def mi_seleccion_de_handicap(ws,uw,bs,ub):
    tw = env.Team([env.Rating(ws,uw)])
    tb = env.Team([env.Rating(bs,ub)]) 
    game = env.Game([tw,tb],[0,1])
    
    res = h_option[np.argmin(np.abs(ws-(bs+hs)))]
    return res
    

results = list(df[filtro].result.map(lambda x: [1,0] if x=="black" else [0,1] ) )
ws = np.array(data[filtro].w_mean_prior)
uw = np.array(data[filtro].w_std_prior)
bs = np.array(data[filtro].b_mean_prior)
ub = np.array(data[filtro].b_std_prior)

selection = np.array([mi_seleccion_de_handicap(wm,ws,bm,bs) for wm,ws,bm,bs in zip(ws,uw,bs,ub)])

plt.hist(selection,bins=np.arange(0,11)-0.5,alpha=0.5)
plt.hist(df[filtro].handicap,bins=np.arange(0,11)-0.5,alpha=0.5)

set(df[filtro].handicap)
selection - df[filtro].handicap