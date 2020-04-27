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
#csv_name = '/home/mati/Storage/Doctorado/Licar/licar/papers/2020_Handicap/nucleo/data/DataFramePurge.csv'
 
df = pd.read_csv(csv_name)

handicap = {}
handicap_history = {}
player = {}
player_woh = {}  # woh : without handicap
player_history = {}
evidences = []
evidences_woh = []
count = 0


 #%%

for index in df.index:
    # Priors
    player[df.at[index, "white"]] = player.get(df.at[index, "white"], env.Skill())
    player[df.at[index, "black"]] = player.get(df.at[index, "black"], env.Skill())
    player_woh[df.at[index, "white"]] = player_woh.get(df.at[index, "white"] , env.Skill())
    player_woh[df.at[index, "black"]] = player_woh.get(df.at[index, "black"] , env.Skill())   
    # Teams
    h_key = (df.at[index,'handicap'] , df.at[index,'width'])
    tw = env.Team([player[df.at[index, "white"]]])
    tw_woh = env.Team([player_woh[df.at[index, "white"]]])
    tb_woh = env.Team([player_woh[df.at[index, "black"]]])
    # Con handicap
    if h_key[0] > 1:
        h_factor = handicap.get(h_key, env.Rating(0,25/3,0,1/100)) # devuelve rating
        tb = env.Team([player[df.at[index, "black"]],h_factor])
        # Posterior
        [player[df.at[index, "white"]]], tb_post = env.Game([tw,tb],df.at[index, "results"]).posterior
        evidences.append(env.Game([tw,tb],df.at[index, "results"]).evidence)
        [player[df.at[index, "black"]], handicap[h_key]] = tb_post
        # Sin handicap
        [player_woh[df.at[index, "white"]]], [player_woh[df.at[index, "black"]]] = env.Game([tw_woh,tb_woh],df.at[index, "results"]).posterior
        evidences_woh.append(env.Game([tw,tb_woh],df.at[index, "results"]).evidence)
       
        if h_key in handicap_history:
            handicap_history[h_key].append(handicap[h_key] )
        else:
            handicap_history[h_key] = [handicap[h_key]]
    # Sin handicap        
    else:
        tb = env.Team([player[df.at[index, "black"]]])
        [player[df.at[index, "white"]]], tb_post = env.Game([tw,tb],df.at[index, "results"]).posterior
        evidences.append(env.Game([tw,tb],df.at[index, "results"]).evidence)
        [player[df.at[index, "black"]]] = tb_post
        [player_woh[df.at[index, "white"]]], [player_woh[df.at[index, "black"]]] = env.Game([tw_woh,tb_woh],df.at[index, "results"]).posterior
        evidences_woh.append(env.Game([tw,tb_woh],df.at[index, "results"]).evidence)
    
    # Guardo el historial tanto con como sin handicap
    if df.at[index, "white"] in player_history:
        player_history[df.at[index, "white"]].append([df.at[index, "id"], player[df.at[index, "white"]], player_woh[df.at[index, "white"]]] )
    else:      
        player_history[df.at[index, "white"]] = [df.at[index, "id"], player[df.at[index, "white"]], player_woh[df.at[index, "white"]]]

    if df.at[index, "black"] in player_history:
        player_history[df.at[index, "black"]].append([df.at[index, "id"], player[df.at[index, "black"]],player_woh[df.at[index, "black"]]] )
    else:      
        player_history[df.at[index, "black"]] = [df.at[index, "id"], player[df.at[index, "black"]],player_woh[df.at[index, "black"]]]


    print(f"Porcentaje de handicap.py es del {int(count/len(df.index)*100)}%", end='\r')
    count = count + 1

#%%   
     
with open('handicap.pickle', 'wb') as handle:
    pickle.dump(handicap, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('handicap_history.pickle', 'wb') as handle:
    pickle.dump(handicap_history, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('player_history.pickle', 'wb') as handle:
    pickle.dump(player_history, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('player.pickle', 'wb') as handle:
    pickle.dump(player, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('evidence.pickle', 'wb') as handle:
    pickle.dump(evidences, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('evidence_woh.pickle', 'wb') as handle:
    pickle.dump(evidences_woh, handle, protocol=pickle.HIGHEST_PROTOCOL)