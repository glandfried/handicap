from math import exp, floor
from numpy.random import normal, seed


def mu2rating(mu):
    mu = float(mu)
    num = floor(abs(mu))
    letra = 'd' if mu > 0 else 'k'

    return str(num)+letra

seed(99)
N = 1000
out_filename = "../../archivos/skill_ev/juntos"

def skill(experience, middle, maximum, slope):
    return maximum/(1+exp(slope*(-experience+middle)))

target = [skill(i, 500, 2, 0.0075) for i in range(N)]
opponents = normal(target,scale=0.5)

#composition = [[["a"], [str(i)]] for i in range(N)]
results = ['WHITE' if normal(target[i]) > normal(opponents[i]) else 'BLACK' for i in range(N)]
#times = [i for i in range(N)]
#priors = dict([(str(i), Player(Gaussian(opponents[i], 0.2))) for i in range(N)])

def write_players(f_out):
    f_out.write("PLAYERS\n")
    print("Pasando jugadores")
    f_out.write(str(N) + ' 1d NULL NULL NULL\n') #el jugador N es al que voy a seguir. empieza desconocido
    for i in range(1,N):
        mu = opponents[i] + (1 if opponents[i] > 0 else -1)
        mu = str(mu)
        sigma = '0.2'
        id = str(i)
        rating = mu2rating(mu)
        f_out.write(id + ' ' + rating + ' ' + mu + ' ' + sigma + ' 0\n')
    f_out.write("END_PLAYERS\n")


for j in range(1,N):
    with open(out_filename+str(j)+'.in', 'w') as f_out:
        write_players(f_out)
        f_out.write("GAMES\n")
        for i in range(1,j+1):
            new_line = str(N) + ' ' + str(i) + ' 0 -1 ' + results[i] + "\n"
            f_out.write(new_line)
        f_out.write("END_GAMES\n")
