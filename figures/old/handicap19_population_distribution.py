import os
name = os.path.basename(__file__).split(".py")[0]
#
import matplotlib.pyplot as plt
#%matplotlib auto
##########
import sys
sys.path.append('../software/')
import trueskill
import ablr # analytic-bayesian-linear-regression own package
import numpy as np
import pickle
#import numpy as np

"""

    HAY QUE TERMINAR DE HACER LOS GRAFICOS USANDO 
    DISTRIBUCIONES DE CREENCIAS


"""
#if (' point' in g['outcome'] or 'Resignation' == g['outcome'] or 'Timeout'  == g['outcome']) and not g['annulled']:

def games_s_h(s,h):
    return list(filter(lambda g: g['width']==s and g['handicap']==h ,games_sorted))
    

if __name__ == "__main__":

    with open("../data/games_sorted.pickle",'rb') as file:
        games_sorted = pickle.load(file)
    

    
    i=2
    dif = list(map(lambda g: (g['black_prior_woh']-g['white_prior_woh']).mu, games_s_h(19,i)  ))
    #diff_mean.append(np.mean(dif))
    plt.hist(dif,100)
    plt.axvline(np.mean(dif), color='black', linestyle='-')
    #plt.axvline(0, color='black', linestyle='--',alpha=0.3)
 
    
    plt.xticks(fontsize=12) # rotation=90
    plt.yticks(fontsize=12) # rotation=90
    
    plt.title(r"19 X 19", fontsize=16 )
    plt.ylabel("", fontsize=16 )
    plt.xlabel("Skill difference", fontsize=16 )


    plt.savefig("pdf/"+name+".pdf",pad_inches =0,transparent =True,frameon=True)
    bash_cmd = "pdfcrop --margins '0 0 0 0' pdf/{0}.pdf pdf/{0}.pdf".format(name)
    os.system(bash_cmd)
    
