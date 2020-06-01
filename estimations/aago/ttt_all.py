import os
name = os.path.basename(__file__).split(".py")[0]
##################
#import time
import pandas as pd
import sys
sys.path.append('../../software/trueskill.py/')
#import numpy as np
import src as th
from importlib import reload  # Python 3.4+ only.
reload(th)
env = th.TrueSkill(draw_probability=0,tau=1,beta=4.33,epsilon=0.1)
#import ipdb

# Posible variable
dataset = 'aago'

# Data
df = pd.read_csv('../../data/'+dataset+'/summary_filtered.csv')
#df.columns

fit_mu_handicap = [-0.53445148,  0.82848756] 
prior_dict = {}
for h_key in set([(h,19) for h in df.handicap ]):
    mu_h = fit_mu_handicap[0] + fit_mu_handicap[1]*h_key[0]
    prior_dict[h_key] = env.Rating(mu_h,0.5,0,0)

results = list(df.result.map(lambda x: [1,0] if x=="black" else [0,1] ) )
composition = [[[w],[b]] if h<2 else [[w],[b,(h,19)]] for w, b, h in zip(df.white_player_id, df.black_player_id, df.handicap) ]   
batch_number = list(df.event_id)


history= env.history(composition, results,batch_number, prior_dict=prior_dict)
#history.trueSkill()
history.through_time(online=True)
history.convergence()

#ipdb.set_trace()
#from collections import defaultdict
#res= defaultdict(lambda: ([],[]))
#for t in history.times:
#    for j in t.players:
#        res[str(j)][0].append(t.posterior(j).mu)
#        res[str(j)][1].append(t.posterior(j).sigma)

w_id = [g[0][0] for t in history.times for g in t.games_composition]
b_id = [g[1][0] for t in history.times for g in t.games_composition]
h_id = [g[1][1] if len(g[1]) > 1 else -1 for t in history.times for g in t.games_composition]
w_mean = [t.posterior(g[0][0]).mu for t in history.times for g in t.games_composition]
w_std = [t.posteriors(g[0][0]).sigma for t in history.times for g in t.games_composition]
b_mean = [t.posteriors(g[1][0]).mu for t in history.times for g in t.games_composition]
b_std = [t.posteriors(g[1][0]).sigma for t in history.times for g in t.games_composition]
h_mean = [ t.posteriors(g[1][1]).mu if len(g[1]) > 1 else 0 for t in history.times for g in t.games_composition]
h_std = [ t.posteriors(g[1][1]).sigma if len(g[1]) > 1 else 0 for t in history.times for g in t.games_composition]
evidence = [e for t in history.times for e in t.evidence]
last_evidence = [e for t in history.times for e in t.last_evidence]

res = df[['id']].copy() 
res["w_id"] = w_id 
res["b_id"] = b_id
res["h_id"] = h_id
res["w_mean"] = w_mean
res["w_std"] = w_std
res["b_mean"] = b_mean
res["b_std"] = b_std
res["h_mean"] = h_mean
res["h_std"] = h_std
res["evidence"] = evidence
res["last_evidence"] = last_evidence

res.to_csv(name+".csv", index=False)
