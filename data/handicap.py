import pandas as pd
import getpass
import sys
sys.path.append('../software/')
import os
import pickle
import numpy as np
import skill as th
from importlib import reload  # Python 3.4+ only.
reload(th)
env = th.TrueSkill(draw_probability=0)

with open('summary/summary.pickle', 'rb') as handle:
    games_sorted= pickle.load(handle)

handicap = {}
handicap_history = {}
player = {}
player_woh = {} # woh : without handicap
player_history = {}
for g in games_sorted :
    #g = games_sorted [0]
    g['white_prior'] = player.get(g['white'] , env.Skill())
    g['black_prior'] = player.get(g['black'] , env.Skill())
    
    g['white_prior_woh'] = player_woh.get(g['white'] , env.Skill())
    g['black_prior_woh'] = player_woh.get(g['black'] , env.Skill())
    
    if (' point' in g['outcome'] or 'Resignation' == g['outcome'] or 'Timeout'  == g['outcome']) and not g['annulled']:
        
        # empieza a jugar el negro
        # el blanco recibe el komi
        # el negro puede recibir el handicap
        # si recibe handicap, empeiza el blanco
        
        # Puntos del blanco
        result = list(g['order'])
        if ' point' in g['outcome']:
            # Negative komi are added to black.
            # So if balck wins, we 
            when_black_win_then_positive_else_negative = 2*result[0]-1
            points =  when_black_win_then_positive_else_negative*float(g['outcome'].split(' point')[0]) + (float(g['komi']))
            if points > 0:
                result = [1,0]
            else:
                result = [0,1]
        
        # Equipo negro
        h_key = (g['handicap'] , g['width'])
        tw = env.Team([g['white_prior']])
	tw_woh = env.Team([g['white_prior_woh']])
        tb_woh = env.Team([g['black_prior_woh']])
        
        if h_key[0] >1:
            h_factor = handicap.get(h_key, env.Rating(0,25/3,0,1/100))
            tb = env.Team([g['black_prior'],h_factor]) 
        else:
            tb = env.Team([g['black_prior']])
        
        #estimacion
        g['estimated'] = True
        [g['white_posterior_woh']], [g['black_posterior_woh']] = env.Game([tw_woh,tb_woh],result).posterior
        [g['white_posterior']], tb_post = env.Game([tw,tb],result).posterior
        
        
        g['evidence_woh'] = env.Game([tw,tb_woh],result).evidence
        g['evidence'] = env.Game([tw,tb],result).evidence
        # Equipo negro
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
        
    else:
        g['estimated'] = False
        g['white_posterior'], g['black_posterior'] = g['white_prior'], g['black_prior']
        g['white_posterior_woh'], g['black_posterior_woh'] =  g['white_prior_woh'], g['black_prior_woh']

    
    player[g['white']] = g['white_posterior']
    player[g['black']] = g['black_posterior']

    player_woh[g['white']] = g['white_posterior_woh']
    player_woh[g['black']] = g['black_posterior_woh']

    if g['white'] in player_history:
        player_history[g['white']].append((g['id'], g['white_posterior'],g['white_posterior_woh'] ))
    else:
        player_history[g['white']] = [(g['id'], g['white_posterior'],g['white_posterior_woh'])]
    
    if g['black'] in player_history:
        player_history[g['black']].append((g['id'], g['black_posterior'],g['black_posterior_woh']))
    else:
        player_history[g['black']] = [(g['id'], g['black_posterior'],g['black_posterior_woh'])]

#handicap_matrix = np.matrix(list(map(lambda xs: [xs[0][0],xs[0][1], xs[1].mu, xs[1].sigma] , handicap.items())))
#handicap_df = pd.DataFrame(handicap_lista, columns=["Handicap", "Size", "Skill", "Uncertainty"])
#pd.DataFrame.to_csv(handicap_df,"handicap.csv")

with open('handicap.pickle', 'wb') as handle:
    pickle.dump(handicap, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('handicap_history.pickle', 'wb') as handle:
    pickle.dump(handicap_history, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('player_history.pickle', 'wb') as handle:
    pickle.dump(player_history, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('games_sorted.pickle', 'wb') as handle:
    pickle.dump(games_sorted, handle, protocol=pickle.HIGHEST_PROTOCOL)

"""
handicap_sorted = sorted(handicap.items(),key=lambda x: (x[0][1], x[0][0]) )

handicap_9_x = [h[0][0] for h in handicap_sorted if h[0][1]==9]
handicap_9_mu = [h[1].mu for h in handicap_sorted if h[0][1]==9]
handicap_9_sigma = [1/h[1].sigma for h in handicap_sorted if h[0][1]==9]





player = {}
player_woh = {} # woh : without handicap
player_history = {}
for g in games_sorted :
    #g = games_sorted [0]
    g['white_prior'] = player.get(g['white'] , env.Skill())
    g['black_prior'] = player.get(g['black'] , env.Skill())
    
    g['white_prior_woh'] = player_woh.get(g['white'] , env.Skill())
    g['black_prior_woh'] = player_woh.get(g['black'] , env.Skill())
    
    if (' point' in g['outcome'] or 'Resignation' == g['outcome'] or 'Timeout'  == g['outcome']) and not g['annulled']:
        
        # empieza a jugar el negro
        # el blanco recibe el komi
        # el negro puede recibir el handicap
        # si recibe handicap, empeiza el blanco
        
        # Puntos del blanco
        result = list(g['order'])
        if ' point' in g['outcome']:
            # Negative komi are added to black.
            # So if balck wins, we 
            when_black_win_then_positive_else_negative = 2*result[0]-1
            points =  when_black_win_then_positive_else_negative*float(g['outcome'].split(' point')[0]) + (float(g['komi']))
            if points > 0:
                result = [1,0]
            else:
                result = [0,1]
        
        # Equipo negro
        h_key = (g['handicap'] , g['width'])
        tw = env.Team([g['white_prior']])
        tb_woh = env.Team([g['black_prior']])
        
        if h_key[0] >1:
            h_factor = handicap.get(h_key, env.Rating(0,25/3,0,1/100))
            tb = env.Team([g['black_prior'],h_factor]) 
        else:
            tb = env.Team([g['black_prior']])
        
        #estimacion
        g['estimated'] = True
        [g['white_posterior_woh']], [g['black_posterior_woh']] = env.Game([tw,tb_woh],result).posterior
        [g['white_posterior']], tb_post = env.Game([tw,tb],result).posterior
        
        g['evidence_woh'] = env.Game([tw,tb_woh],result).evidence
        g['evidence'] = env.Game([tw,tb],result).evidence
        
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
        
    else:
        g['estimated'] = False
        g['white_posterior'], g['black_posterior'] = g['white_prior'], g['black_prior']
        g['white_posterior_woh'], g['black_posterior_woh'] =  g['white_prior_woh'], g['black_prior_woh']

    
    player[g['white']] = g['white_posterior']
    player[g['black']] = g['black_posterior']

    player_woh[g['white']] = g['white_posterior_woh']
    player_woh[g['black']] = g['black_posterior_woh']

    if g['white'] in player_history:
        player_history[g['white']].append((g['id'], g['white_posterior'],g['white_posterior_woh'] ))
    else:
        player_history[g['white']] = [(g['id'], g['white_posterior'],g['white_posterior_woh'])]
    
    if g['black'] in player_history:
        player_history[g['black']].append((g['id'], g['black_posterior'],g['black_posterior_woh']))
    else:
        player_history[g['black']] = [(g['id'], g['black_posterior'],g['black_posterior_woh'])]


with open('handicap_1.pickle', 'wb') as handle:
    pickle.dump(handicap, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('handicap_history_1.pickle', 'wb') as handle:
    pickle.dump(handicap_history, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('player_history_1.pickle', 'wb') as handle:
    pickle.dump(player_history, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('games_sorted_1.pickle', 'wb') as handle:
    pickle.dump(games_sorted, handle, protocol=pickle.HIGHEST_PROTOCOL)
"""





