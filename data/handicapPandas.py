import pandas as pd
import sys
sys.path.append('../software/')
import pickle
import skill as th
import json
from importlib import reload  # Python 3.4+ only.
reload(th)
env = th.TrueSkill(draw_probability=0)

csv_name = 'DataFramePurge.csv'
csv_name = '/home/mati/Storage/Doctorado/Licar/licar/papers/2020_Handicap/nucleo/data/DataFramePurge.csv'
 
df = pd.read_csv(csv_name)

handicap = {}
handicap_history = {}
player = {} # Player va a tener de key el id del blanco y negro y de valor su skill
player_woh = {} # woh : without handicap
player_history = {}
count = 0
games_sorted = []

# %% 



 #%%
def stringToList(x):
    if x == '[1, 0]':
        x = list([1, 0])
    elif x == '[0, 1]':
        x = list([0, 1])      
    else:
        pass
    return x
    #%%
for index in df.index:
    # Priors
    g = {}
    
    g['width'] = df.at[index, "width"]
    g['handicap'] = df.at[index, "handicap"]
    g['id'] = df.at[index, "id"]
    g['white'] = df.at[index, "white"]
    g['black'] = df.at[index, "black"]
    #player[df.at[index, "white"]] = player.get(df.at[index, "white"], env.Skill())
    #player[df.at[index, "black"]] = player.get(df.at[index, "black"], env.Skill())
    g['white_prior'] = player.get(g['white'], env.Skill())
    g['black_prior'] = player.get(g['black'], env.Skill())
    g['white_prior_woh'] = player_woh.get(g['white'] , env.Skill())
    g['black_prior_woh'] = player_woh.get(g['black'] , env.Skill())   
    # Teams
    h_key = (g['handicap'] , g['width'])
    tw = env.Team([g['white_prior']])
    tw_woh = env.Team([g['white_prior_woh']])
    tb_woh = env.Team([g['black_prior_woh']])
    # Con handicap
  
    if h_key[0] > 1:
        h_factor = handicap.get(h_key, env.Rating(0,25/3,0,1/100)) # devuelve rating
        tb = env.Team([g['black_prior'],h_factor])

    else:
        tb = env.Team([g['black_prior']])
        
    
    result = df.at[index, "results"]
    result = stringToList(result)
        #estimacion
    g['estimated'] = True
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

#%%   
with open('handicap.pickle', 'wb') as handle:
    pickle.dump(handicap, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('handicap_history.pickle', 'wb') as handle:
    pickle.dump(handicap_history, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('player_history.pickle', 'wb') as handle:
    pickle.dump(player_history, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('games_sorted.pickle', 'wb') as handle:
    pickle.dump(games_sorted, handle, protocol=pickle.HIGHEST_PROTOCOL)
     
#with open('handicap.pickle', 'wb') as handle:
#    pickle.dump(handicap, handle, protocol=pickle.HIGHEST_PROTOCOL)
#with open('handicap_history.pickle', 'wb') as handle:
#    pickle.dump(handicap_history, handle, protocol=pickle.HIGHEST_PROTOCOL)
#with open('player_history.pickle', 'wb') as handle:
#    pickle.dump(player_history, handle, protocol=pickle.HIGHEST_PROTOCOL)
#with open('player.pickle', 'wb') as handle:
#    pickle.dump(player, handle, protocol=pickle.HIGHEST_PROTOCOL)
#with open('evidence.pickle', 'wb') as handle:
#    pickle.dump(evidences, handle, protocol=pickle.HIGHEST_PROTOCOL)
#with open('evidence_woh.pickle', 'wb') as handle:
#    pickle.dump(evidences_woh, handle, protocol=pickle.HIGHEST_PROTOCOL)