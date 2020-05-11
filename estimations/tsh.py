import os
name = os.path.basename(__file__).split(".py")[0]
##################
import pandas as pd
import sys
sys.path.append('../software/')
import numpy as np
import skill as th
#from importlib import reload  # Python 3.4+ only.
#reload(th)
env = th.TrueSkill(draw_probability=0)

# Posible variable
dataset = 'ogs'

# Data
df = pd.read_csv('../data/'+dataset+'/summary_filtered.csv')

es = df[['id']].copy()
es["w_mean"] = np.nan
es["w_std"] = np.nan
es["b_mean"] = np.nan
es["b_std"] = np.nan
es["h_mean"] = np.nan
es["h_std"] = np.nan
es["estimated"] = np.nan
es["evidence"] = np.nan

# Prior data structure
from collections import defaultdict
handicap = defaultdict(lambda:env.Rating(0,25/3,0,1/100))
player = defaultdict(lambda:env.skill())

for i in df.index:#i=0            
    
    h_key = (df.loc[i].handicap , df.loc[i].width)    
    
    if df.loc[i].ranked:
        es.loc[i,'estimated'] = True        
        # Teams
        tw = env.Team([player[df.loc[i].white]])
        # Con handicap    
        if h_key[0] > 1:
            tb = env.Team([player[df.loc[i].black],handicap[h_key]])
        else:
            tb = env.Team([player[df.loc[i].black]])
        
        result = [1,0] if df.loc[i].black_win else [0,1]
        
        game = env.Game([tw,tb],result)
        es.evidence_tsh = game.evidence
        tw_post, tb_post = game.posterior
        
        es.loc[i,'w_mean'], es.loc[i,'w_std'] = tw_post[0]
        es.loc[i,'b_mean'], es.loc[i,'b_std'] = tb_post[0]
        es.loc[i,'h_mean'], es.loc[i,'h_std'] = tb_post[1] if h_key[0] >1 else handicap[h_key]
        
        player[df.loc[i].white] = tw_post[0]
        player[df.loc[i].black] = tb_post[0]
        handicap[h_key] = tb_post[1] if h_key[0] >1 else handicap[h_key]
        
    else:
        es.iloc[i].estimated_tsh = False
        es.loc[i,'w_mean'], es.loc[i,'w_std'] = player[df.iloc[i].white]
        es.loc[i,'b_mean'], es.loc[i,'b_std'] = player[df.iloc[i].black]    
        es.loc[i,'h_mean'], es.loc[i,'h_std'] = handicap[h_key]
                    
    print(f"Porcentaje de "+name+".py es del {int(i/len(df.index)*100)}%", end='\r')
     
df.to_csv(name+".csv", index=False)
