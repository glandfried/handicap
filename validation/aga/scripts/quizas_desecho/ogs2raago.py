# recorro una vez para armar dict de id players
# recorro otra para poner los resultados
import pandas as pd
import math

#in_filename = "../archivos/splitteados/splitteado_0.csv"
in_filename = "../archivos/cincomil_example.csv"
out_filename = "../archivos/cincomil_prueba.in"

print("Leyendo")
blacks = pd.read_csv(in_filename, usecols = ['black'])
whites = pd.read_csv(in_filename, usecols = ['white'])
blacks.to_csv("blacks.csv")
whites.to_csv("whites.csv")
blacks = blacks.drop_duplicates()
blacks.rename(columns = {'black':'id'}, inplace = True)
whites.rename(columns = {'white':'id'}, inplace = True)
players = pd.concat([blacks, whites])
players.to_csv("players.csv")


print("Eliminando duplicados")
players = players.drop_duplicates()

with open(out_filename, 'w') as f_out:
    f_out.write("PLAYERS\n")
    print("Pasando jugadores")
    for p in players['id']:
        f_out.write(str(p) + " 1d NULL NULL NULL\n")
    f_out.write("END_PLAYERS\n")
    f_out.write("GAMES\n")
    with open(in_filename, 'r') as f_in:
        f_in.readline() #me salteo el header
        print("Pasando juegos")
        for line in f_in:
            [id,black,white,started,black_lost,width,komi,handicap] = line.split(',')
            winner = "WHITE" if black_lost == '1' else "BLACK"
            #KOMI REDONDEO PARA ABAJO O PARA ARRIBA? DEPENDE DE JAPONESAS/CHINAS? :O
            new_line = white + ' ' + black + ' ' + str(math.floor(float(handicap))) + ' ' + str(math.floor(float(komi))) + ' ' + winner + "\n"
            f_out.write(new_line)
    f_out.write("END_GAMES\n")
