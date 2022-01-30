from os import system
from math import floor

#inter_filename = "intercomunidades.txt"
#todos_filename = "aislados_todos_juntos.in"
inter_filename = "intercomunidades50.txt"
todos_filename = "aislados_todos_juntos_inter50.in"

#obtiene el rating (p. ej. 2d, 5k) correspondiente a un valor de habilidad
def mu2rating(mu):
    mu = float(mu)
    num = floor(abs(mu))
    letra = 'd' if mu > 0 else 'k'

    return str(num)+letra

system("./raago < " + todos_filename " > log_todos_juntos.txt")

system("./raago < aislados_comunidad_1.in > log1.txt")
system("./raago < aislados_comunidad_2.in > log2.txt")

#con log1 y log2 creo un aislados_ambas.in con los jugadores de ambas comunidades
#y de intercomunidades traigo partidas entre comunidades
jugadores = {}
with open("aislados_ambas.in", 'w') as f_out:
    with open("log1.txt", 'r') as log1:
        f_out.write("PLAYERS\n")
        for line in log1:
            [id, mu, sigma] = line.split()
            rating = mu2rating(mu)
            f_out.write(str(id) + ' ' + rating + ' ' + str(mu) + ' ' + str(sigma) + " 0\n")
    with open("log2.txt", 'r') as log2:
        for line in log2:
            [id, mu, sigma] = line.split()
            rating = mu2rating(mu)
            f_out.write(str(id) + ' ' + rating + ' ' + str(mu) + ' ' + str(sigma) + " 0\n")
    f_out.write("END_PLAYERS\n")
    f_out.write("GAMES\n")
    with open(inter_filename, 'r') as log3:
        for line in log3:
            f_out.write(line)
    f_out.write("END_GAMES\n")


system("./raago < aislados_ambas.in > log_separados.txt")
