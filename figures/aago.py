import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Polygon
from itertools import groupby

df = pd.read_csv('../data/aago/summary_filtered.csv')
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


from collections import defaultdict
res= defaultdict(lambda: {"mu":[],"sigma":[],"evento":[]})
for i in range(len(data.id)):#i=0
    e = df.event_id[i]
    w = data.w_id[i]
    b = data.b_id[i]
    h = df.handicap[i]
    if not e in res[w]["evento"]:
        res[w]["mu"].append(data.w_mean[i])
        res[w]["sigma"].append(data.w_std[i])
        res[w]["evento"].append(e)
    if not e in res[b]["evento"]:
        res[b]["mu"].append(data.b_mean[i])
        res[b]["sigma"].append(data.b_std[i])
        res[b]["evento"].append(e)
    if h > 1 and (not e in res[(h,19)]["evento"]):
        res[(h,19)]["mu"].append(data.h_mean[i])
        res[(h,19)]["sigma"].append(data.h_std[i])
        res[(h,19)]["evento"].append(e)
res = dict(res)

diff = 0
for k in res:
    if not "(" in str(k):  plt.plot(res[k]["mu"])
    diff = max(abs(res[k]["mu"][-1]-res[k]["mu"][0]),diff)
    #plt.xlim(0,128)
    
for k in res:
    if "(" in str(k): plt.plot(res[k]["mu"])
    #plt.xlim(0,128)    


    
for k in res:
    if not "(" in str(k):  plt.plot(res[k]["sigma"])
    

