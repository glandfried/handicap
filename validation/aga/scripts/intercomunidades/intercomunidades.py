#creo que no uso este exp
from os import system
from math import floor

def run_raago(f_in, f_out):
    system("../../../../../RAAGo/original-AGA-rating-system/aago-rating-calculator/raago < " +f_in+ " > " +f_out)

def mu2rating(mu):
    mu = float(mu)
    num = floor(abs(mu))
    letra = 'd' if mu > 0 else 'k'

    return str(num)+letra

def leer_log(f_in):
    res = "PLAYERS\n"
    with open(f_in, 'r') as f:
        for line in f:
            [id, mu, sigma] = line.split()
            rating = mu2rating(mu)
            res = res + (str(id) + ' ' + rating + ' ' + str(mu) + ' ' + str(sigma) + " 0\n")
    return res+("END_PLAYERS\n")

path = "../../archivos/intercomunidades/"
filename_1 = path + "separados_1_"
filename_2 = path + "separados_2_"
filename_3 = path + "separados_3_"

jugadores_1 = """PLAYERS
0 1d NULL NULL NULL
1 1d NULL NULL NULL
2 1d NULL NULL NULL
3 1d NULL NULL NULL
4 1d NULL NULL NULL
5 1d NULL NULL NULL
END_PLAYERS
"""

partidas_intra = """0 1 0 -1 WHITE
1 2 0 -1 WHITE
2 0 0 -1 WHITE
3 4 0 -1 WHITE
4 5 0 -1 WHITE
5 3 0 -1 WHITE
"""

partidas_inter_8 = """3 0 0 -1 WHITE
3 0 0 -1 WHITE
3 0 0 -1 WHITE
3 0 0 -1 WHITE
3 0 0 -1 WHITE
3 0 0 -1 WHITE
3 0 0 -1 WHITE
3 0 0 -1 WHITE
3 0 0 -1 BLACK
3 0 0 -1 BLACK
"""

print("Creando 1")
#creo un separados_1_i para i entre 1 y 20 exclusive
# i es la cantidad de partidos intra

##genero partidas intra 
for i in range(1,21): #TOBI LO HIZO CON ESTOS MISMOS?
    i = i*5
    with open(filename_1+str(i)+".in", 'w') as f:
        f.write(jugadores_1)
        f.write("GAMES\n")
        for _ in range(i):
            f.write(partidas_intra)
        f.write("END_GAMES\n")

    #corro partidas intra
    print("Corriendo el paso 1 con " + str(i) + " partidas intra")
    f_in = filename_1 + str(i) + ".in"
    f_out = path + "log_separados_1_" + str(i) + ".txt"
    run_raago(f_in, f_out)

    #genero partidas inter con 8/10, 40/50, 80/100
    jugadores_2 = leer_log(path + "log_separados_1_" + str(i) + ".txt")
    for j in [1 , 5, 10]:
        with open(filename_2+str(i)+"_"+str(8*j)+".in", 'w') as f:
            f.write(jugadores_2)
            f.write("GAMES\n")
            for _ in range(j):
                f.write(partidas_inter_8)
            f.write("END_GAMES\n")

    #corro partidas inter
    for j in [1 , 5, 10]:
        f_in = filename_2+str(i)+"_"+str(8*j)+".in"
        f_out = path + "log_separados_2_" + str(i) + "_" + str(8*j) + ".txt"
        run_raago(f_in, f_out)


    #genero partidas intra
    for j in [8, 40, 80]:
        jugadores_3 = leer_log(path + "log_separados_2_" + str(i) + "_" + str(j) + ".txt")
        with open(filename_3+str(i)+"_"+str(j)+".in", 'w') as f:
            f.write(jugadores_3)
            f.write("GAMES\n")
            for _ in range(i):
                f.write(partidas_intra)
            f.write("END_GAMES\n")

    #corro partidas intra
    for j in [8, 40, 80]:
        f_in = filename_3+str(i)+"_"+str(j)+".in"
        f_out = path + "log_separados_3_" + str(i)+"_"+str(j)+ ".txt"
        run_raago(f_in, f_out)
