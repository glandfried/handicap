import os
name = os.path.basename(__file__).split(".py")[0]
##################
#import time
import kickscore as ks
import pandas as pd
import pickle
import sys
sys.path.append('../../software/trueskill.py/')
#import numpy as np
import src as th
from importlib import reload  # Python 3.4+ only.
reload(th)
env = th.TrueSkill(draw_probability=0,tau=1,beta=4.33,epsilon=0.1)
#import ipdb


# Posible variable
dataset = 'ogs'

# Data
df = pd.read_csv('../../data/'+dataset+'/summary_filtered.csv')


from datetime import datetime
timestamp=list(map(lambda x: int(datetime.strptime(x.split("T")[0],  "%Y-%m-%d").timestamp()), df.started) )

kernel_const = ks.kernel.Constant(var=1.0)
#kernel_exp = ks.kernel.Exponential(var=1.0, lscale=1.0)
#kernel_52 = ks.kernel.Matern52(var=0.5, lscale=1.0)
seconds_in_year = 365.25 * 24 * 60 * 60
kernel_smooth = (ks.kernel.Constant(var=0.03)
        + ks.kernel.Matern32(var=0.138, lscale=1.753*seconds_in_year))

model = ks.BinaryModel()
list(map(lambda j: model.add_item(j, kernel=kernel_smooth), set(pd.concat([df.white[df.ranked],df.black[df.ranked]]) ) ))
list(map(lambda h: model.add_item(h, kernel=kernel_const) if h[0] > 1 else None, set(zip(df.handicap[df.ranked],df.width[df.ranked])) ))

for w, b, d, o, h, s, r in zip(df.white, df.black, timestamp, df.black_win, df.handicap, df.width, df.ranked ):
    if r and o and h>1:
        model.observe(winners=[b,(h,s)], losers=[w], t=d)
    elif r and o and h<=1:
        model.observe(winners=[b], losers=[w], t=d)
    elif r and (not o) and h > 1:
        model.observe(winners=[w], losers=[b,(h,s)], t=d)
    elif r and (not o) and h <= 1:
        model.observe(winners=[w], losers=[b], t=d)

model.fit(verbose=True)

if False:
    log_evidence = model.log_likelihood

    import matplotlib.pyplot as plt
    import math
    math.exp(log_evidence/sum(df.ranked))
    
    df_r = df[df.ranked].copy()
    df_r = df_r.reset_index()
    
    jugadores = list(set(df_r.white))[0:100]
    model.plot_scores([(2,19), (3,19), (4,19),(5,19),(6,19)], figsize=(14, 5));
    
    j = jugadores[0] 
    for i in jugadores:
        lc = model.item[i].predict(model.item[i].scores[0])[0]
        plt.plot(lc )
    
with open(name+'.pickle', 'wb') as handle:
    pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)