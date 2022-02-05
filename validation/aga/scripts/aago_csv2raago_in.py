# recorro una vez para armar dict de id players
# recorro otra para poner los resultados
import pandas as pd
import csv
from math import floor
import math
from os import system
from datetime import date
import RAAGo.scripts.rango_aux as rango

class Player:
    def __init__(self, id, rating='1d', mu='NULL', sigma='NULL', last_date='NULL'):
        self._id = id
        self.rating = rating
        self.mu = mu
        self.sigma = sigma
        self.last_date = last_date

def run_raago(f_in, f_out):
    system(raago_filename + " < " +f_in+ " > " +f_out)

def mu2rating(mu):
    mu = float(mu)
    num = floor(abs(mu))
    letra = 'd' if mu > 0 else 'k'

    return str(num)+letra

def update_players(results_file):
    with open(results_file, 'r') as f:
        for line in f:
            [id, mu, sigma] = line.split()
            rating = mu2rating(mu)
            players_dict[id].rating = rating
            players_dict[id].mu = mu
            players_dict[id].sigma = sigma


def dict_to_str(players_d, event_id, actual_date):
    res = "PLAYERS\n"
    actual_players = event_players(event_id)
    for p in players_d.values():
        exists = p._id in actual_players
        if exists:
            days = 'NULL' if (p.last_date == 'NULL') else str((actual_date - p.last_date).days)
            rating = cat_dict[(str(event_id), p._id)]
            new_line = p._id + ' ' + rating + ' ' + p.mu + ' ' + p.sigma + ' ' + days + "\n"
            res = res + new_line
    return res+("END_PLAYERS\n")

def event_players(target_event):
    p = []
    with open(in_filename, 'r') as file:
        file.readline() #salteo el header
        for line in file:
            [black,white,_,_,_,_,_,event_id,_] = line.split(',')
            if (int(event_id) == int(target_event)):
                p.append(black)
                p.append(white)
    return p

def to_date(date_string):
    [year,month,day] = date_string.split('-')
    return date(int(year), int(month), int(day))

#agrega end_date del evento (que está en events_filename) a las partidas (de games_filename), los ordena en base a eso (event_id desempata) y lo guarda en out_filename
def create_in_file(out_filename):
    #cargo games_filename
    games = pd.read_csv(games_filename)
    #cargo events_filename
    events = pd.read_csv(events_filename)
    #joineo
    out = games.merge(events, on= 'event_id', how= 'left')
    #ordeno
    out = out.sort_values(by=['end_date','event_id'])
    #paso a csv con out_filename
    out.to_csv(out_filename, index=False)

# calcula mu y sigma iniciales de un jugador, es decir,
# para partidas en las que tienen mu y sigma = NULL
# a partir de su categoria declarada
def mu_sigma_float(player_id, ev_id):
    if players_dict[player_id].mu == 'NULL':
        assert(players_dict[player_id].sigma == 'NULL')
        rating = cat_dict[(str(ev_id), player_id)]
        rating_num = float(rating[:-1])
        rating_let = rating[-1]
        if rating_let == 'k':
            mu = -(rating_num + 0.5)
            sigma = sigma_dict[mu+1]
        elif rating_let == 'd' :
            mu = rating_num + 0.5
            sigma = sigma_dict[mu-1]
    else:
        mu = float(players_dict[player_id].mu)
        assert(players_dict[player_id].sigma != 'NULL')
        sigma = float(players_dict[player_id].sigma)
    return mu, sigma

# filenames desde este entrypoint
# games_filename = "../../handicap/data/aago/aago_raago.csv"
# game_filename = "../archivos/aago_validation/game_"
# result_filename = "../archivos/aago_validation/results_"
# final_results_fname = "../archivos/aago_validation/results_final.csv"
# raago_filename = "../../RAAGo/original-AGA-rating-system/aago-rating-calculator/raago"
# categories_filename = "../archivos/aago_validation/categories.csv"
# events_filename = "../archivos/aago_validation/events.csv"
# in_filename = "../archivos/aago_validation/in.csv"

#filenames entrando desde ../../
games_filename = "handicap/data/aago/aago_raago.csv"
game_filename = "handicap/validation/aga/archivos/aago_validation/game_"
result_filename = "handicap/validation/aga/archivos/aago_validation/results_"
final_results_fname = "handicap/validation/aga/archivos/aago_validation/results_final.csv"
raago_filename = "RAAGo/original-AGA-rating-system/aago-rating-calculator/raago"
categories_filename = "handicap/validation/aga/archivos/aago_validation/categories.csv"
events_filename = "handicap/validation/aga/archivos/aago_validation/events.csv"
in_filename = "handicap/validation/aga/archivos/aago_validation/in.csv"

create_in_file(in_filename)

#cargo todos los jugadores, inicializados en 0, etc.

print("Leyendo")
blacks = pd.read_csv(in_filename, usecols = ['black'])
whites = pd.read_csv(in_filename, usecols = ['white'])
blacks = blacks.drop_duplicates()
blacks.rename(columns = {'black':'id'}, inplace = True)
whites.rename(columns = {'white':'id'}, inplace = True)
p = pd.concat([blacks, whites])
print("Eliminando duplicados")
p = p.drop_duplicates()

#diccionario de jugadores (Player's)
players_dict = {}
for id in p['id']:
    id = str(id)
    players_dict[id] = Player(id)

#diccionario de categorias
with open(categories_filename, mode='r') as infile:
    reader = csv.reader(infile)
    cat_dict = {(rows[2],rows[3]):rows[1] for rows in reader}
    #      key: (event_id, player_id) | value: ranking (aka category)

# diccionario de sigmas iniciales
# (mind the gap, al acceder hay que offsetear el mu 1 hacia el 0)
# array obtenido del script de RAAGo, player.cpp; a su vez obtenido de Accelrat
sigma_array = [5.73781, 5.63937, 5.54098, 5.44266, 5.34439,
                    5.24619, 5.14806, 5.05000, 4.95202, 4.85412,
                    4.75631, 4.65859, 4.56098, 4.46346, 4.36606,
                    4.26878, 4.17163, 4.07462, 3.97775, 3.88104,
                    3.78451, 3.68816, 3.59201, 3.49607, 3.40037,
                    3.30492, 3.20975, 3.11488, 3.02035, 2.92617,
                    2.83240, 2.73907, 2.64622, 2.55392, 2.46221,
                    2.37118, 2.28090, 2.19146, 2.10297, 2.01556,
                    1.92938, 1.84459, 1.76139, 1.68003, 1.60078,
                    1.52398, 1.45000, 1.37931, 1.31244, 1.25000,
                    1.19269, 1.14127, 1.09659, 1.05948, 1.03078,
                    1.01119, 1.00125, 1.00000, 1.00000]
sigma_dict = { mu+0.5 : sigma_array[mu+50] for mu in range(-50, 9)}


actual_event = 1
games = "GAMES\n"
players = dict_to_str(players_dict, 1, 'NULL') #pongo 1 porque el primer evento de aago tiene id = 1
log_evidence = 0

#recorro las partidas, del archivo de entrada
with open(in_filename, 'r') as file:
    file.readline() #salteo el header
    for line in file:
        [black,white,started,black_win,width,komi,handicap,event_id,end_date] = line.split(",")
        event_id = int(event_id)

### calcular evidencia
        if black_win == 'True':
            winner_mu, winner_sigma = mu_sigma_float(black, event_id)
            loser_mu, loser_sigma = mu_sigma_float(white, event_id)
        else:
            winner_mu, winner_sigma = mu_sigma_float(white, event_id)
            loser_mu, loser_sigma = mu_sigma_float(black, event_id)
        actual_evidence = rango.win_chance_hk(winner_mu, loser_mu, winner_sigma, loser_sigma, float(handicap), float(komi))
        log_evidence += math.log(actual_evidence)
        print(log_evidence)
###


        if event_id != actual_event: #si cambié de evento
            print(actual_event)
            # cierro games
            games = games + "END_GAMES\n"
            # armo i.in con games y players
            with open(game_filename+str(actual_event)+'.in' , 'w') as out:
                out.write(players)
                out.write(games)
            # corro
            run_raago(game_filename+str(actual_event)+'.in', result_filename+str(actual_event)+'.txt')
            # leo results (si no falla por el error que puede tener fdf)
            try:
                update_players(result_filename+str(actual_event)+'.txt')
            except:
                print("Archivo inválido")
            # armo el string players para el prox antes de pisarle las dates con el siguiente evento
            players = dict_to_str(players_dict, event_id, to_date(end_date))
            # reinicio games con solo este game
            games = "GAMES\n"
            # actualizo actual_event
            actual_event = event_id
        #handicap = str(math.floor(float(handicap))) por que hacia esto?
        komi = str(floor(float(komi))) #redondeo para abajo (chequear que este bien lo de japonesas/chinas)
        winner = "BLACK" if black_win == 'True' else "WHITE"
        new_line = white + ' ' + black + ' ' + handicap + ' ' + komi + ' ' + winner + "\n"
        #agrego evento a game
        games = games + new_line
        #acá tendría que modificar el days de los jugadores implicados
        this_date = to_date(end_date)
        w_last = players_dict[white].last_date
        b_last = players_dict[black].last_date
        if (w_last == 'NULL') or (this_date > w_last) :
            players_dict[white].last_date = this_date
        if (b_last == 'NULL') or (this_date > b_last):
            players_dict[black].last_date = this_date

    #armo el ultimo games
    print(actual_event)
    games = games + "END_GAMES\n"
    with open(game_filename+str(actual_event)+'.in' , 'w') as out:
        out.write(players)
        out.write(games)
    # corro
    run_raago(game_filename+str(actual_event)+'.in', result_filename+str(actual_event)+'.txt')


with open(final_results_fname, 'w') as f:
    for p in players_dict.values():
        new_line = p._id + ',' + p.rating + ',' + p.mu + ',' + p.sigma + "\n"
        f.write(new_line)