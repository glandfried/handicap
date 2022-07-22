from os import system
from math import floor

def run_raago(f_in, f_out):
    system("../../../RAAGo/original-AGA-rating-system/aago-rating-calculator/raago < " +f_in+ " > " +f_out)


path = "../archivos/tres_aislados/"
filename = path + "juntos_"

jugadores = """PLAYERS
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



#leo los log y los uso como jugadores_2 para escribir los
# separados_2_i_j para i entre 1 y 20, j 8 y 80 (1 y 10)
# j es la cantidad de partidos inter
for i in range(1,21):
    for j in [1,10]:
        with open(filename+str(i)+"_"+str(8*j)+".in", 'w') as f:
            f.write(jugadores)
            f.write("GAMES\n")
            for _ in range(i):
                f.write(partidas_intra)
            for _ in range(j):
                f.write(partidas_inter_8)
            f.write("END_GAMES\n")


#corro raago para todos esos, guardo en log+...
for i in range(1,21):
    for j in [8,80]:
        f_in = filename+str(i)+"_"+str(j)+".in"
        f_out = path + "log_juntos_" + str(i) + "_" + str(j) + ".txt"
        run_raago(f_in, f_out)
