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

df.columns

from collections import defaultdict
prior_dict = defaultdict(lambda:env.Rating(0,25/3,0,1/100))
for h_key in set([(h,19) for h in df.handicap ]):
    prior_dict[h_key] 
dict(prior_dict)
results = list(df.result.map(lambda x: [1,0] if x=="black" else [0,1] ) )
composition = [[[w],[b]] if h<2 else [[w],[b,(h,19)]] for w, b, h in zip(df.white_player_id, df.black_player_id, df.handicap) ]   

history= env.history(composition, results, prior_dict=prior_dict)
#history.trueSkill()
history.through_time(online=True)
history.convergence()
    
w_mean = [ t.posteriors[w].mu for t,w,b in zip(history.times,df.white[df.ranked],df.black[df.ranked]) ]                                                            
b_mean = [ t.posteriors[b].mu for t,w,b in zip(history.times,df.white[df.ranked],df.black[df.ranked]) ]                                                            
w_std = [ t.posteriors[w].sigma for t,w,b in zip(history.times,df.white[df.ranked],df.black[df.ranked]) ]                                                          
b_std = [ t.posteriors[b].sigma for t,w,b in zip(history.times,df.white[df.ranked],df.black[df.ranked]) ]    
h_mean = [  t.posteriors[(h,w)].mu if h > 1 else 0 for t,h,w in zip(history.times,df.handicap[df.ranked],df.width[df.ranked]) ]
h_std = [  t.posteriors[(h,w)].sigma if h > 1 else 0 for t,h,w in zip(history.times,df.handicap[df.ranked],df.width[df.ranked]) ] 
evidence = [  t.evidence[0] for t in history.times] 
last_evidence = [  t.last_evidence[0] for t in history.times] 

res = df[['id']][df.ranked].copy() 
res["w_mean"] = w_mean
res["w_std"] = w_std
res["b_mean"] = b_mean
res["b_std"] = b_std
res["h_mean"] = h_mean
res["h_std"] = h_std
res["evidence"] = evidence
res["last_evidence"] = last_evidence

res.to_csv(name+".csv", index=False)
