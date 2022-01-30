from math import exp, floor
from numpy.random import normal, seed
from os import system
import csv

def run_raago(f_in, f_out):
    system("../../../../RAAGo/original-AGA-rating-system/aago-rating-calculator/raago < " + f_in + " > " + f_out)


def mu2rating(mu):
    mu = float(mu)
    num = floor(abs(mu))
    letra = 'd' if mu > 0 else 'k'

    return str(num)+letra

def read_skill(filename):
    with open(filename, 'r') as f_in:
        for line in f_in:
            [id,mu,sigma] = line.split()
            if id == str(N):
                 return float(mu),float(sigma)
def skill(experience, middle, maximum, slope):
    return maximum/(1+exp(slope*(-experience+middle)))


seed(99)
N = 1000
days = '0'
out_filename = "../../archivos/skill_ev/separados_"


target = [skill(i, 500, 2, 0.0075) for i in range(N)]
opponents = normal(target,scale=0.5)

#composition = [[["a"], [str(i)]] for i in range(N)]
results = ['WHITE' if normal(target[i]) > normal(opponents[i]) else 'BLACK' for i in range(N)]
#times = [i for i in range(N)]
#priors = dict([(str(i), Player(Gaussian(opponents[i], 0.2))) for i in range(N)])
skills = []

def write_players(f_out,game):
    f_out.write("PLAYERS\n")
    if game % 10 == 0:
        print(game)
    if game == 1:
        f_out.write(str(N) + ' 1d NULL NULL NULL\n') #el jugador N es al que voy a seguir. empieza desconocido
    else:
        run_raago(out_filename+str(game-1)+".in","log_tmp.txt") #leo el resultado del partido anterior
        mu,sigma = read_skill("log_tmp.txt")
        rating = mu2rating(mu)
        line = str(N) + ' ' + rating + ' ' + str(mu) + ' ' + str(sigma) + ' ' + days+'\n'
        f_out.write(line)
        skill = {}
        skill['time'] = game-1
        skill['mu'] = mu
        skill['sigma'] = sigma
        skills.append(skill)

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
        write_players(f_out,j)
        f_out.write("GAMES\n")
        new_line = str(N) + ' ' + str(j) + ' 0 -1 ' + results[j] + "\n"
        f_out.write(new_line)
        f_out.write("END_GAMES\n")

with open("../../archivos/skill_ev/log_separados.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['time','mu','sigma'])
        writer.writeheader()
        writer.writerows(skills)
