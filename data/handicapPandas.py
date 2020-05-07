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
    d = df.iloc[i]
    
    es.iloc[i].w_mean_tsh, es.iloc[i].w_std_tsh = player[df.iloc[i].white]
    es.iloc[i].b_mean_tsh, es.iloc[i].b_std_tsh = player[df.iloc[i].black]
        
    if df.iloc[i].ranked:
        es.iloc[i].estimated = True        
        # Teams
        tw = env.Team(player[df.iloc[i].white])
        # Con handicap
        if df.iloc[i].handiicap > 1:
            h_key = ( , g['width'])
            h_factor = handicap.get(h_key, env.Rating(0,25/3,0,1/100)) # devuelve rating
            tb = env.Team([g['black_prior'],h_factor])
        else:
            tb = env.Team([g['black_prior']])
            
        result = df.at[index, "results"]
        
        # Calcula Trueskill comun? osea sin que sea del tiempo
        [g['white_posterior_woh']], [g['black_posterior_woh']] = env.Game([tw_woh,tb_woh],result).posterior
            # Le agrega los teams
        [g['white_posterior']], tb_post = env.Game([tw,tb],result).posterior
            # No seria tw_woh?   
        
        g['evidence_woh'] =env.Game([tw_woh,tb_woh],result).evidence
        g['evidence'] = env.Game([tw,tb],result).evidence
            # Equipo negro, le mete la info del handicap y sus posteriores
        if h_key[0] >1:
            g['handicap_prior'] = tb[1]
            g['black_posterior'], g['handicap_posterior']  = tb_post
            handicap[h_key] = g['handicap_posterior']
    
            if h_key in handicap_history:
                handicap_history[h_key].append(g['handicap_posterior'] )
            else:
                handicap_history[h_key] = [g['handicap_posterior'] ]
    
        else:
            [g['black_posterior']] = tb_post
            g['handicap_prior'] = None     
    
        player[g['white']] = g['white_posterior']
        player[g['black']] = g['black_posterior']
    
        player_woh[g['white']] = g['white_posterior_woh']
        player_woh[g['black']] = g['black_posterior_woh']
            
    else:
        g['estimated'] = False
        
        g['white_posterior'] = g['white_prior'] 
        g['black_posterior'] = g['black_prior'] 
        g['white_posterior_woh'] = g['white_prior_woh'] 
        g['black_posterior_woh'] = g['black_prior_woh'] 
        
                
    # Guardo el historial tanto con como sin handicap
    if g['white'] in player_history:
        player_history[g['white']].append((g['id'], g['white_posterior'],g['white_posterior_woh'] ))
    else:
        player_history[g['white']] = [(g['id'], g['white_posterior'],g['white_posterior_woh'])]

    if g['black'] in player_history:
        player_history[g['black']].append((g['id'], g['black_posterior'],g['black_posterior_woh']))
    else:
        player_history[g['black']] = [(g['id'], g['black_posterior'],g['black_posterior_woh'])]

    dictionary_copy = g.copy()
    games_sorted.append(dictionary_copy)
    print(f"Porcentaje de handicap.py es del {int(count/len(df.index)*100)}%", end='\r')
    count = count + 1
    #if count > 5000 & h_key[0]>1:
     #   break
     
df.to_csv("trueskill.csv", index=False)
