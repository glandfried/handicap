import csv
import os
import pickle
import numpy as np
import truehandicap as th
from importlib import reload  # Python 3.4+ only.
reload(th)
env = th.TrueSkill(draw_probability=0)

def reduce_games(game):
    #game =player_games[0] 
    res = {}
    res['id'] = game['id']
    res['annulled'] = game['annulled']
    res['black'] = int(game['black'])
    res['white'] = int(game['white'])
    res['order'] = [int(game['white_lost']),int(game['black_lost'])]
    res['outcome'] = game['outcome']
    res['handicap'] = game['handicap']
    res['komi'] = game['komi']
    res['ranked'] = game['ranked']
    res['width'] = game['width']
    res['started'] = game['started']
    res['ended'] = game['ended']
    #res['source'] = game['source']
    #res['mode'] = game['mode']
    res['tournament'] = not game['tournament'] is None
    return res
    
files_dir = 'all-games-before-oct-2013-raw/'
listdir_ = sorted(os.listdir(files_dir ))
games = []
for f in range(len(listdir_)):
    #f = 0
    file_path = os.path.join(files_dir, listdir_[f])
    player_games = pickle.load(open(file_path , "rb"))
    
    games = games + list(map(lambda x: reduce_games(x), player_games))

games_tuple = list(map(lambda x: tuple([ (i[0], tuple(i[1])) if isinstance(i[1], list) else (i[0], i[1]) for i in x.items()]) , games))
unique_games = list(set(games_tuple  ))
len(games ) + 1 ==2* len(unique_games) 
games_dict = list(map(lambda x: dict(x), unique_games))
games_sorted = sorted(games_dict, key=lambda x: (x['started'], x['id']) )

keys = games_sorted[0].keys()
with open('all_games_before_oct_2013.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(games_sorted)

with open('all_games_before_oct_2013.pickle', 'wb') as handle:
    pickle.dump(games_sorted, handle, protocol=pickle.HIGHEST_PROTOCOL)

