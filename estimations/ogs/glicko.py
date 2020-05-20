import os
name = os.path.basename(__file__).split(".py")[0]
##################
#import time
import pandas as pd
import sys
sys.path.append('../../software/glicko2/')
sys.path.append('../../software/trueskill.py/')
import src as th
import math
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from glicko2 import Glicko2, WIN, DRAW, LOSS
env = Glicko2(tau=0.5)

# Posible variable
dataset = 'ogs'

# Data
df = pd.read_csv('../../data/'+dataset+'/summary_filtered.csv')

w_mean = []
w_std = []
w_vol = []
b_mean = []
b_std = []
b_vol = []
estimated = []
evidence = []

# Prior data structure
from collections import defaultdict
handicap = defaultdict(lambda:env.create_rating())
player = defaultdict(lambda:env.create_rating())

def erfc(x):
        """Complementary error function (via `http://bit.ly/zOLqbc`_)"""
        z = abs(x)
        t = 1. / (1. + z / 2.)
        r = t * math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (
            0.37409196 + t * (0.09678418 + t * (-0.18628806 + t * (
                0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (
                    -0.82215223 + t * 0.17087277
                )))
            )))
        )))
        return 2. - r if x < 0 else r
    
def cdf(x, mu=0, sigma=1):
    return 0.5 * erfc(-(x - mu) / (sigma * math.sqrt(2)))

def marginal_likelihood(r1,r2):
    """
    Este n\'umero es bastante aproximado al likelihood marginal del modelo Zermelo. 
    """
    dm = r1.mu - r2.mu    
    ds = np.sqrt(r1.phi**2 + r2.phi**2 + r1.sigma**2 + r2.sigma**2)
    return 1-cdf(0,dm,ds)
    
    
for i in df.index:#i=0            
    
    #h_key = (df.loc[i].handicap , df.loc[i].width)    
    w_key = df.loc[i].white
    b_key=  df.loc[i].black
    #prior_h = handicap[h_key]
    prior_w = player[w_key]
    prior_b = player[b_key]
    
    if df.loc[i].ranked:
        result = WIN if df.loc[i].black_win else LOSS
        
        tb_post = env.rate(prior_b, [(result , prior_w)])
        tw_post = env.rate(prior_w, [(1-result , prior_b)])
        
        evidence.append(marginal_likelihood(prior_b,prior_w))
        
        w_mean.append(tw_post.mu); w_std.append(tw_post.phi); w_vol.append(tw_post.sigma)
        b_mean.append(tb_post.mu); b_std.append(tb_post.phi); b_vol.append(tb_post.sigma)
        
        estimated.append(True)
        
        player[w_key] = tw_post
        player[b_key] = tb_post
        
    else:
        estimated.append(False)
        evidence.append(1)
        w_mean.append(prior_w.mu); w_std.append(prior_w.phi); w_vol.append(prior_w.sigma)
        b_mean.append(prior_b.mu); b_std.append(prior_b.phi); b_vol.append(prior_b.sigma)
        
    print('Porcentaje:', int(i/len(df.index)*100), end='\r')

es = df[['id']].copy()
es["w_mean"] = w_mean
es["w_std"] = w_std
es["b_mean"] = b_mean
es["b_std"] = b_std
es["w_vol"] = w_vol
es["b_vol"] = b_vol
es["estimated"] = estimated
es["evidence"] = evidence
    
es.to_csv(name+".csv", index=False)