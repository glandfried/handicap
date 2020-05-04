import csv
import os
import json
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
    players = game['historical_ratings'].keys()
    res.append(('black_rating', game['historical_ratings']['black']['ratings']['overall']['rating'] if 'black' in players else None))
    res.append(('white_rating', game['historical_ratings']['white']['ratings']['overall']['rating'] if 'white' in players else None))
    res.append(('black_deviation', game['historical_ratings']['black']['ratings']['overall']['deviation'] if 'black' in players else None))
    res.append(('white_deviation', game['historical_ratings']['white']['ratings']['overall']['deviation'] if 'white' in players else None))
    res.append(('black_volatility', game['historical_ratings']['black']['ratings']['overall']['volatility'] if 'black' in players else None))
    res.append(('white_volatility', game['historical_ratings']['white']['ratings']['overall']['volatility'] if 'white' in players else None))
    res.append(('black_ranking', game['historical_ratings']['black']['ranking'] if 'black' in players else None))
    res.append(('white_ranking', game['historical_ratings']['white']['ranking'] if 'white' in players else None))
    res.append(('tournament', not game['tournament'] is None))
    return res

"""
Each source file have all the games played by the player.
"""
#files_dir = '/home/mati/Storage/Doctorado/Licar/licar/papers/2020_Handicap/nucleo/data/resultsJson/'
files_dir = '../resultsJson/'
listdir_ = os.listdir(files_dir ) # Crea una lista de todos los archivos dentro de esa carpeta

"""
We will extract all games from the files.
"""
games = []
count = 0
for f in range(len(listdir_)):
    #f = 3
    #print(f"Porcentaje de sumaryJson.py es del {int(count/len(listdir_)*100)}%",end='\r')
    count = count + 1
    file_path = os.path.join(files_dir, listdir_[f]) # Genera el path completo de un archivo
    player_games = json.load(open(file_path , "r")) # abre el archivo, r de read and write, b de binary
    games = games + list(map(reduce_games, player_games))


#%%
#map() le das una funcion y con que iterar.
#lambda es para generar funciones cortas, le pasas las variables y con  dos puntos : la funciones


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
with open('summaryJson.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(games_sorted)
with open('summaryJson.pickle', 'wb') as handle:
    pickle.dump(games_sorted, handle, protocol=pickle.HIGHEST_PROTOCOL)
