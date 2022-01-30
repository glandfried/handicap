import pandas as pd
import csv
import math
import RAAGo.scripts.rango_aux as rango

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
def mu_sigma(player_id, ev_id):
    rating = cat_dict[(str(ev_id), player_id)]
    rating_num = float(rating[:-1])
    rating_let = rating[-1]
    if rating_let == 'k':
        mu = -(rating_num + 0.5)
        sigma = sigma_dict[mu+1]
    elif rating_let == 'd' :
        mu = rating_num + 0.5
        sigma = sigma_dict[mu-1]

    return float(mu), float(sigma)


games_filename = "handicap/data/aago/aago_raago.csv"
categories_filename = "aga-validation/archivos/aago_validation/categories.csv"
estimations_filename = "aga-validation/archivos/aago_validation/raago.csv"
events_filename = "aga-validation/archivos/aago_validation/events.csv"
in_filename = "aga-validation/archivos/aago_validation/in.csv"

create_in_file(in_filename)

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

with open(estimations_filename, mode='r') as infile:
    reader = csv.reader(infile)
    estimations_dict = {(rows[3],rows[4]):(rows[1], rows[2]) for rows in reader}
    #      key: (event_id, player_id) | value: (mu, sigma)


#creo diccionario players vacio
players = {}
# a medida que aparecen en alguna partida:
#   calculo la evidencia tomando
#                               - (1era vez) el prior a partir de los mu y sigma declarados
#                               - (dsps) la estimacion guardada en este dict
#   lo defino en el dicc a partir del resultado en estimations_filename
log_evidence = 0

with open(in_filename, 'r') as file:
    file.readline()
    for line in file:
        [black,white,started,black_win,width,komi,handicap,event_id,end_date] = line.split(",")
        if not (black in players):
            players[black] = mu_sigma(black, event_id)
        if not (white in players):
            players[white] = mu_sigma(white, event_id)
        # a esta altura ambos estan definidos en players
        # obtengo mus y sigmas
        if black_win:
            winner_mu, winner_sigma = players[black]
            loser_mu, loser_sigma = players[white]
        else:
            winner_mu, winner_sigma = players[white]
            loser_mu, loser_sigma = players[black]
        #calculo evidencia
        actual_evidence = rango.win_chance_hk(winner_mu, loser_mu, winner_sigma, loser_sigma, float(handicap), float(komi))
        log_evidence += math.log(actual_evidence)
        print(log_evidence)
        # actualizo players con la estimacion de raago posterior a esta partida
        b_mu, b_sigma = estimations_dict[event_id, black]
        players[black] = float(b_mu), float(b_sigma)
        w_mu, w_sigma = estimations_dict[event_id, white]
        players[white] = float(w_mu), float(w_sigma)
