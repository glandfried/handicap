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
import ipdb

# Posible variable
dataset = 'aago'

# Data
df = pd.read_csv('../../data/'+dataset+'/summary_filtered.csv')
#df.columns

fit_mu_handicap = [-0.53445148,  0.82848756] 
prior_dict = {}
for h_key in set([(h,19) for h in df.handicap ]):
    mu_h = fit_mu_handicap[0] + fit_mu_handicap[1]*h_key[0]
    prior_dict[h_key] = env.Rating(mu_h,1,0,0)

results = list(df.result.map(lambda x: [1,0] if x=="black" else [0,1] ) )
composition = [[[w],[b]] if h<2 else [[w],[b,(h,19)]] for w, b, h in zip(df.white_player_id, df.black_player_id, df.handicap) ]   
batch_number = list(df.event_id)


history= env.history(composition, results,batch_number, prior_dict=prior_dict)
#history.trueSkill()
history.through_time(online=False)
history.convergence()

ipdb.set_trace()

res= defaultdict(lambda: ([],[]))
for t in history.times:
    for j in t.players:
        res[j][0].append(t.posterior(j).mu)
        res[j][1].append(t.posterior(j).sigma)

import json
with open(name+'.json', 'w') as file:
     file.write(json.dumps(res)) # use `json.loads` to do the reverse
