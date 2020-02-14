import csv
import os
import pickle
import numpy as np

def reduce_games(game):#game=player_games[0] 
    """
    Recive a game
    Return relevant information
    """
    res = []
    res.append(('id', game['id']) )
    res.append(('annulled', game['annulled']))
    res.append(('black', int(game['black'])))
    res.append(('white', int(game['white'])))
    res.append(('order', (int(game['white_lost']),int(game['black_lost'])) ))
    res.append(('outcome', game['outcome']))
    res.append(('handicap', game['handicap']))
    res.append(('komi', game['komi']))
    res.append(('ranked', game['ranked']))
    res.append(('width', game['width']))
    res.append(('started', game['started']))
    res.append(('ended', game['ended']))
    #res['source'] = game['source']
    #res['mode'] = game['mode']
    res.append(('tournament', not game['tournament'] is None))
    return res
    

"""
Each source file have all the games played by the player.
"""
files_dir = '../results/'
listdir_ = os.listdir(files_dir ) 

"""
We will extract all games from the files.
"""
games = []
for f in range(len(listdir_)):
    #f = 0
    file_path = os.path.join(files_dir, listdir_[f])
    player_games = pickle.load(open(file_path , "rb"))
    games = games + list(map(lambda x: reduce_games(x), player_games))

"""
Note that each game we will find it twice, one for each player.
We will get the set() of games.
But the lists are not hashable. We need somnthing like tuple.
"""
games_tuple = list(map(lambda x: tuple(x) , games))
unique_games = list(set(games_tuple))
len(games ) + 1 ==2* len(unique_games)

"""
We sorted the games in temporal order.
"""
games_dict = list(map(lambda x: dict(x), unique_games))
games_sorted = sorted(games_dict, key=lambda x: (x['started'], x['id']) )

"""
We write the games
"""
keys = games_sorted[0].keys()
with open('summary.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(games_sorted)

with open('summary.pickle', 'wb') as handle:
    pickle.dump(games_sorted, handle, protocol=pickle.HIGHEST_PROTOCOL)

