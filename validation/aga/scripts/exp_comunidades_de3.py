from os import system
from math import floor

def run_raago(f_in, f_out):
    system("./raago < " +f_in+ " > " +f_out)

def mu2rating(mu):
    mu = float(mu)
    num = floor(abs(mu))
    letra = 'd' if mu > 0 else 'k'

    return str(num)+letra

def leer_log(in):
    res = "PLAYERS\n"
    with open(in, 'r') as f:
        for line in f:
            [id, mu, sigma] = line.split()
            rating = mu2rating(mu)
            res = res + (str(id) + ' ' + rating + ' ' + str(mu) + ' ' + str(sigma) + " 0\n")
    return res+("END_PLAYERS\n")

path = "../archivos/tres_aislados/"
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
"""

partida_inter_8 = """3 1 0 -1 WHITE
3 1 0 -1 WHITE
3 1 0 -1 WHITE
3 1 0 -1 WHITE
3 1 0 -1 WHITE
3 1 0 -1 WHITE
3 1 0 -1 WHITE
3 1 0 -1 WHITE
3 1 0 -1 BLACK
3 1 0 -1 BLACK
"""

print("Creando 1")
#creo un separados_1_i para i entre 1 y 20 exclusive
# i es la cantidad de partidos intra
for i in range(1,20):
    with open(filename_1+str(i)+".in", 'w') as f:
        f.write(jugadores_1)
        f_out.write("GAMES\n")
        for _ in range(i):
            f.write(partidas_intra)
        f_out.write("END_GAMES\n")

print("Corriendo 1")
#corro raago para todos esos, guardo en log+...
for i in range(1,20):
    f_in = filename_1 + str(i) + ".in"
    f_out = path + "log_separados_1_" + str(i) + ".txt"
    run_raago(f_in, f_out)

#leo los log y los uso como jugadores_2 para escribir los
# separados_2_i_j para i entre 1 y 20, j 8 y 80 (1 y 10)
# j es la cantidad de partidos inter
for i in range(1,20):
    jugadores_2 = leer_log(path + "log_separados_1_" + str(i) + ".txt")
    for j in [1,10]:
        with open(filename_2+str(i)+"_"+str(8*j)+".in", 'w') as f:
            f.write(jugadores_2)
            f_out.write("GAMES\n")
            for _ in range(j):
                f.write(partidas_inter_8)
            f_out.write("END_GAMES\n")


#corro raago para todos esos, guardo en log+...
for i in range(1,20):
    for j in [1,10]:
        f_in = filename_2+str(i)+"_"+str(8*j)+".in"
        f_out = path + "log_separados_2_" + str(i) + "_" + str(8*j) + ".txt"
        run_raago(f_in, f_out)


#same con 3
for i in range(1,20):
    for j in [8,80]:
        jugadores_3 = leer_log(path + "log_separados_2_" + str(i) + "_" + str(j) + ".txt")
        for k in range(20-i+1):
            with open(filename_3+str(i)+"_"+str(j)+"_"+str(k)+".in", 'w') as f:
                f.write(jugadores_3)
                f_out.write("GAMES\n")
                for _ in range(k):
                    f.write(partidas_intra)
                f_out.write("END_GAMES\n")

for i in range(1,20):
    for j in [8,80]:
        for k in range(20-i+1):
            f_in = filename_3+str(i)+"_"+str(j)+"_"+str(k)+".in"
            f_out = path + "log_separados_3_" + str(i)+"_"+str(j)+"_"+str(k)+ ".txt"
            run_raago(f_in, f_out)
