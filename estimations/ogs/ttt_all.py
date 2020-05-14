import os
name = os.path.basename(__file__).split(".py")[0]
##################
#import time
import pandas as pd
import pickle
import sys
sys.path.append('../../software/trueskill.py/')
#import numpy as np
import src as th
from importlib import reload  # Python 3.4+ only.
reload(th)
env = th.TrueSkill(draw_probability=0,tau=1,epsilon=0.1)

# Posible variable
dataset = 'ogs'

# Data
df = pd.read_csv('../../data/'+dataset+'/summary_filtered.csv')

from collections import defaultdict
prior_dict = defaultdict(lambda:env.Rating(0,25/3,0,1/100))
for h_key in set([(h,s) for h, s in zip(df.handicap, df.width) ]):
    prior_dict[h_key] 
dict(prior_dict)
results = list(df.black_win.map(lambda x: [1,0] if x else [0,1] ) )
composition = [[[w],[b]] if h<2 else [[w],[b,(h,s)]] for w, b, h, s in zip(df.white, df.black, df.handicap, df.width) ]   

history= env.history(composition, results, prior_dict=prior_dict)
#history.trueSkill()
history.through_time()
history.convergence()

with open(name+".pickle", "wb") as output_file:
    pickle.dump(history, output_file,protocol=pickle.HIGHEST_PROTOCOL)

#es.to_csv(name+".csv", index=False)