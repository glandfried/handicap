import math
from numpy.random import normal, seed, randint

semilla = 99
mu = 1
dif = 4
tamanio = 50
num_partidos = 250
num_partidos_inter = 50

out_filename1 = "../archivos/aislados_comunidad_1.in"
out_filename2 = "../archivos/aislados_comunidad_2.in"
out_filename3 = "../archivos/intercomunidades" + str(num_partidos_inter) + ".txt"
out_filename_todos = "../archivos/aislados_todos_juntos_inter" + str(num_partidos_inter) + ".in"

seed(semilla)
comunidad_1 = normal(mu,scale=0.5,size=tamanio)
comunidad_2 = normal(mu+dif,scale=0.5,size=tamanio)

#Separados ------------------------------------------------------------------

with open(out_filename1, 'w') as f_out:
    f_out.write("PLAYERS\n")
    print("Pasando jugadores")
    for i in range(tamanio):
        f_out.write(str(i) + " 1d NULL NULL NULL\n")
    f_out.write("END_PLAYERS\n")
    f_out.write("GAMES\n")
    for _ in range(num_partidos):
        black = randint(tamanio)
        white = randint(tamanio)
        while white == black: white = randint(tamanio)
        black_lost = normal(comunidad_1[black], scale=0.5) < normal(comunidad_1[white], scale=0.5)
        winner = "WHITE" if black_lost else "BLACK"
        new_line = str(white) + ' ' + str(black) + ' 0 -1 ' + winner + "\n" #handicap 0, y komi -1 para que sea 0
        f_out.write(new_line)
    f_out.write("END_GAMES\n")

with open(out_filename2, 'w') as f_out:
    f_out.write("PLAYERS\n")
    print("Pasando jugadores")
    for i in range(tamanio,2*tamanio): #agrego un offset para que queden con nombres distintos a los de la comunidad 1
        f_out.write(str(i) + " 1d NULL NULL NULL\n")
    f_out.write("END_PLAYERS\n")
    f_out.write("GAMES\n")
    for _ in range(num_partidos):
        black = randint(tamanio)
        white = randint(tamanio)
        while white == black: white = randint(tamanio)
        black_lost = normal(comunidad_2[black], scale=0.5) < normal(comunidad_2[white], scale=0.5)
        winner = "WHITE" if black_lost else "BLACK"
        new_line = str(tamanio+white) + ' ' + str(tamanio+black) + ' 0 -1 ' + winner + "\n" #handicap 0, y komi -1 para que sea 0
        f_out.write(new_line)
    f_out.write("END_GAMES\n")

with open(out_filename3, 'w') as f_out:
    for _ in range(num_partidos_inter):
        black = randint(tamanio)
        white = randint(tamanio)
        black_lost = normal(comunidad_1[black], scale=0.5) < normal(comunidad_2[white], scale=0.5)
        winner = "WHITE" if black_lost else "BLACK"
        new_line = str(tamanio+white) + ' ' + str(black) + ' 0 -1 ' + winner + "\n" #handicap 0, y komi -1 para que sea 0
        f_out.write(new_line)

#Todos juntos ---------------------------------------------------------
seed(semilla) # vuelvo a setear el seed para que sean las mismas partidas
comunidad_1 = normal(mu,scale=0.5,size=tamanio)
comunidad_2 = normal(mu+dif,scale=0.5,size=tamanio)

with open(out_filename_todos, 'w') as f_out:
    f_out.write("PLAYERS\n")
    print("Pasando jugadores")
    for i in range(2*tamanio):
        f_out.write(str(i) + " 1d NULL NULL NULL\n")
    f_out.write("END_PLAYERS\n")
    f_out.write("GAMES\n")
    for _ in range(num_partidos): # partidos comunidad_1
        black = randint(tamanio)
        white = randint(tamanio)
        while white == black: white = randint(tamanio)
        black_lost = normal(comunidad_1[black], scale=0.5) < normal(comunidad_1[white], scale=0.5)
        winner = "WHITE" if black_lost else "BLACK"
        new_line = str(white) + ' ' + str(black) + ' 0 -1 ' + winner + "\n" #handicap 0, y komi -1 para que sea 0
        f_out.write(new_line)
    for _ in range(num_partidos): # partidos comunidad_2
        black = randint(tamanio)
        white = randint(tamanio)
        while white == black: white = randint(tamanio)
        black_lost = normal(comunidad_2[black], scale=0.5) < normal(comunidad_2[white], scale=0.5)
        winner = "WHITE" if black_lost else "BLACK"
        new_line = str(tamanio+white) + ' ' + str(tamanio+black) + ' 0 -1 ' + winner + "\n" #handicap 0, y komi -1 para que sea 0
        f_out.write(new_line)
    for _ in range(num_partidos_inter): # partidos intercomunidades
        black = randint(tamanio)
        white = randint(tamanio)
        black_lost = normal(comunidad_1[black], scale=0.5) < normal(comunidad_2[white], scale=0.5)
        winner = "WHITE" if black_lost else "BLACK"
        new_line = str(tamanio+white) + ' ' + str(black) + ' 0 -1 ' + winner + "\n" #handicap 0, y komi -1 para que sea 0
        f_out.write(new_line)
    f_out.write("END_GAMES\n")
