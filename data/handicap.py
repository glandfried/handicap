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
file_path = '/home/mati/Storage/Doctorado/Licar/licar/papers/2020_Handicap/nucleo/data/summary/summaryJson.pickle'
#file_path = 'summary/summary.pickle'
with open(file_path, 'rb') as handle:
    games_sorted= pickle.load(handle)

handicap = {}
handicap_history = {}
player = {} # Player va a tener de key el id del blanco y negro y de valor su skill
player_woh = {} # woh : without handicap
player_history = {}
count = 0
# %%


for g in games_sorted :
    # Son las partidas por jugador pickleadas.
    # get devuelve el value de ese key si es que existe, y si no devuelve el segundo argumento
    # Aca player va a ser una lista de jugadres y se le ira actualizando su skill
    g['white_prior'] = player.get(g['white'] , env.Skill()) # Agrega este key
    g['black_prior'] = player.get(g['black'] , env.Skill())

    g['white_prior_woh'] = player_woh.get(g['white'] , env.Skill())
    g['black_prior_woh'] = player_woh.get(g['black'] , env.Skill())

# Solo tomo las partidas que no fueron anuladas (o none o demas que no interesa)
    if (' point' in g['outcome'] or 'Resignation' == g['outcome'] or 'Timeout'  == g['outcome']) and not g['annulled']:

        # empieza a jugar el negro
        # el blanco recibe el komi
        # el negro puede recibir el handicap
        # si recibe handicap, empeiza el blanco

        # Puntos del blanco
        result = list(g['order']) # el orden es (1,0) si gano negro, (0,1) si perdio
        # Le saca el komi basicamente, si el blanco gano por la dif de komi, pierde
        if ' point' in g['outcome']:
            # Negative komi are added to black.
            # So if balck wins, we
            when_black_win_then_positive_else_negative = 2*result[0]-1 # 1 o -1
            points =  when_black_win_then_positive_else_negative*float(g['outcome'].split(' point')[0]) + (float(g['komi']))
            # Devuelve el signo*puntos + komi
            if points > 0:
                result = [1,0]
            else:
                result = [0,1]

        # Equipo negro
        h_key = (g['handicap'] , g['width']) # width es el tamano del tablero
        tw = env.Team([g['white_prior']])
        tw_woh = env.Team([g['white_prior_woh']])
        tb_woh = env.Team([g['black_prior_woh']])

        if h_key[0] >1: # Si es que hay handicap:
            # handicap tiene com key los diferentes valores de h_key.
            h_factor = handicap.get(h_key, env.Rating(0,25/3,0,1/100)) 
            #  la primera vez tira rating.
            tb = env.Team([g['black_prior'],h_factor]) # por que solo al negro handicap?
        else:
            tb = env.Team([g['black_prior']])

        #estimacion
        g['estimated'] = True
        # Calcula Trueskill comun? osea sin que sea del tiempo
        [g['white_posterior_woh']], [g['black_posterior_woh']] = env.Game([tw_woh,tb_woh],result).posterior
        # Le agrega los teams
        [g['white_posterior']], tb_post = env.Game([tw,tb],result).posterior

        # No seria tw_woh?
        g['evidence_woh'] = env.Game([tw,tb_woh],result).evidence
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
    if g['handicap'] != 0:
        break
    print(f"Porcentaje de handicap.py es del {int(count/len(games_sorted)*100)}%", end='\r')
    count = count + 1
#handicap_matrix = np.matrix(list(map(lambda xs: [xs[0][0],xs[0][1], xs[1].mu, xs[1].sigma] , handicap.items())))
#handicap_df = pd.DataFrame(handicap_lista, columns=["Handicap", "Size", "Skill", "Uncertainty"])
#pd.DataFrame.to_csv(handicap_df,"handicap.csv")
# %%
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
