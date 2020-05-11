import pandas as pd
import sys
sys.path.append('../software/')
import numpy as np
import skill as th
#from importlib import reload  # Python 3.4+ only.
#reload(th)
env = th.TrueSkill(draw_probability=0)

# Data
df = pd.read_csv('summary_filtered.csv')
es = pd.read_csv('estimations.csv')

# TrueSkill - handicap [only ranked]
es["w_mean_tsh"] = np.nan
es["w_std_tsh"] = np.nan
es["b_mean_tsh"] = np.nan
es["b_std_tsh"] = np.nan
es["h_mean_tsh"] = np.nan
es["h_std_tsh"] = np.nan
es["estimated_tsh"] = np.nan
es["evidence_tsh"] = np.nan

# Prior data structure
from collections import defaultdict
handicap = defaultdict(lambda:env.Rating(0,25/3,0,1/100))
player = defaultdict(lambda:env.skill())

for i in df.index:#i=0    
        
    if df.iloc[i].ranked:
        es.iloc[i].estimated = True        
        # Teams
        tw = env.Team([player[df.iloc[i].white]])
        # Con handicap
        h_key = (df.iloc[i].handicap , df.iloc[i].width)
        if h_key[0] > 1:
            tb = env.Team([player[df.iloc[i].black],handicap[h_key]])
        else:
            tb = env.Team([player[df.iloc[i].black]])
        
        result = [1,0] if df.iloc[i].black_win else [0,1]
        
        game = env.Game([tw,tb],result)
        es.evidence_tsh = game.evidence
        tw_post, tb_post = game.posterior
        
        es.iloc[i].w_mean_tsh, es.iloc[i].w_std_tsh = tw_post[0]
        es.iloc[i].b_mean_tsh, es.iloc[i].b_std_tsh = tb_post[0]
        es.iloc[i].h_mean_tsh, es.iloc[i].h_std_tsh = tb_post[1] if h_key[0] >1 else handicap[h_key]
        
        player[df.iloc[i].white] = tw_post[0]
        player[df.iloc[i].black] = tb_post[0]
        handicap[h_key] = tb_post[1] if h_key[0] >1 else handicap[h_key]
        
    else:
        es.iloc[i].estimated_tsh = False
        es.iloc[i].w_mean_tsh, es.iloc[i].w_std_tsh = player[df.iloc[i].white]
        es.iloc[i].b_mean_tsh, es.iloc[i].b_std_tsh = player[df.iloc[i].black]    
                
    print(f"Porcentaje de handicap.py es del {int(i/len(df.index)*100)}%", end='\r')
     
df.to_csv("estimated.csv", index=False)
