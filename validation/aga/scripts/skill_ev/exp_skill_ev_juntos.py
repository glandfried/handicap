from os import system
import csv

def run_raago(f_in, f_out):
    system("../../../../RAAGo/original-AGA-rating-system/aago-rating-calculator/raago < " + f_in + " > " + f_out)

def read_skill(filename):
    with open(filename, 'r') as f_in:
        for line in f_in:
            [id,mu,sigma] = line.split()
            if id == str(N):
                 return float(mu),float(sigma)

N = 1000
skills = []

for i in range(1,N):
    if i % 10 == 0:
        print(i)
    in_filename = "../../archivos/skill_ev/juntos" + str(i) + ".in"
    run_raago(in_filename, "log_tmp.txt")
    #extraigo la habilidad que le da a el jugador N y la cargo en un dict que será un csv
    mu,sigma = read_skill("log_tmp.txt")
    skill = {}
    skill['time'] = i
    skill['mu'] = mu
    skill['sigma'] = sigma
    skills.append(skill)

with open("../../archivos/skill_ev/log_juntos.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['time','mu','sigma'])
        writer.writeheader()
        writer.writerows(skills)

# with open('log_juntos.csv','w') as f:
#     w = csv.writer(f)
#     w.writerows(skills.items())
