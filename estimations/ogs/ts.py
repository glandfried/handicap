import os
name = os.path.basename(__file__).split(".py")[0]
##################
#import time
import pandas as pd
import trueskill as ts
env = ts.TrueSkill(draw_probability=0)

# Posible variable
dataset = 'ogs'

# Data
df = pd.read_csv('../../data/'+dataset+'/summary_filtered.csv')

w_mean = []
w_std = []
b_mean = []
b_std = []
h_mean = []
h_std = []
estimated = []
evidence = []

# Prior data structure
from collections import defaultdict
player = defaultdict(lambda:env.Rating())

for i in df.index:#i=0            
    
    
    h_key = (df.loc[i].handicap , df.loc[i].width)    
    w_key = df.loc[i].white
    b_key=  df.loc[i].black
    prior_w = player[w_key]
    prior_b = player[b_key]
    
    if df.loc[i].ranked:
        result = [1,0] if df.loc[i].black_win else [0,1]
        
        tw = env.Team([prior_w])
        tb = env.Team([prior_b])
        game = env.Game([tw,tb],result)
        
        evidence.append(game.evidence)
        tw_post, tb_post = game.posterior
        w_mean.append(tw_post[0].mu); w_std.append(tw_post[0].sigma)
        b_mean.append(tb_post[0].mu); b_std.append(tb_post[0].sigma)
        estimated.append(True)
        
        player[w_key] = tw_post[0]
        player[b_key] = tb_post[0]
    else:
        estimated.append(False)
        evidence.append(1)
        w_mean.append(prior_w.mu); w_std.append(prior_w.sigma)
        b_mean.append(prior_b.mu); b_std.append(prior_b.sigma)
        
    print('Porcentaje:', int(i/len(df.index)*100), end='\r')

es = df[['id']].copy()
es["w_mean"] = w_mean
es["w_std"] = w_std
es["b_mean"] = b_mean
es["b_std"] = b_std
es["estimated"] = estimated
es["evidence"] = evidence
    
es.to_csv(name+".csv", index=False)