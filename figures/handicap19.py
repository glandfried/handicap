import os
name = os.path.basename(__file__).split(".py")[0]
#
import matplotlib.pyplot as plt
##########
import sys
sys.path.append('../software')
import trueskill
import ablr # analytic-bayesian-linear-regression own package
import numpy as np
import pickle
#import numpy as np


"""
Conlusi\'on 1):
    Hay un comportamiento diferente en el uso del handicap 9, es el m\'as usado.
    Y junto a esto su valor inferiror estimado es inferior a lo esperado seg\'un
    los otros handicaps.
    Hip\'otesis A):
        El estimador perdi\'o incertidumbre, solo 0.080, y por lo tanto se se qued\'o
        clavado en ~4.
        Soluci\'on:
            Modificar el parametro tau que agrega incertidumbre luego de cada estimaci\'on
    Hip\'otesis B):
        El handicap 9 es el m\'aximo handicap para tableros de 9x9. Por lo que es
        asignado a jugadores que necesitan handicap de 9 hasta \infty. Por lo tanto,
        la estimaci\'on de handicap 9x9 est\'a promediando la habilidad que le agrega 
        a al conjunto de esos jugadores.
        Soluci\'on:
            Estimar el handicap 9 separando en poblaciones de 
        
    
"""

if __name__ == "__main__":

    with open("../data/handicap.pickle",'rb') as file:
        handicap = pickle.load(file)
    with open("../data/handicap_history.pickle",'rb') as file:
        handicap_history = pickle.load(file)

    skill = []
    sigma = []
    handicap19 = []
    for i in range(2,10):
        skill.append(handicap[(i,19)].mu)
        sigma.append(handicap[(i,19)].sigma)
        handicap19.append(i)
        plt.plot([handicap19[-1],handicap19[-1]],[skill[-1]+2*sigma[-1],skill[-1]-2*sigma[-1] ],linewidth=0.5,color='grey')
        plt.plot([handicap19[-1],handicap19[-1]],[skill[-1]+sigma[-1],skill[-1]-sigma[-1] ],linewidth=1,color='black')
    
    plt.scatter(handicap19,skill, color='black',s=40)
    
    ####
    # We will perform a bayesian linear regression
    alpha = 10**(-30) # prior precision
    beta = 1/np.mean(sigma[0:7]) # Noise of target value
    t = skill[0:7]
    X_vec = np.array(handicap19[0:7]).reshape(-1, 1) 
    Phi = ablr.linear.phi(X_vec , ablr.linear.identity_basis_function)  
    
    fit_mu, fit_sigma = ablr.linear.posterior(alpha,beta,t,Phi)
    plt.plot([2,8],[fit_mu[0]+fit_mu[1]*2,fit_mu[0]+fit_mu[1]*8])    
    # END: baysian linear regression
    ###
    
    plt.xticks(fontsize=12) # rotation=90
    plt.yticks(fontsize=12) # rotation=90
    
    plt.title(r"19 X 19", fontsize=16 )
    plt.xlabel("Handicap", fontsize=16 )
    plt.ylabel("Skill", fontsize=16 )
    
    plt.savefig("pdf/"+name+".pdf",pad_inches =0,transparent =True,frameon=True)
    bash_cmd = "pdfcrop --margins '0 0 0 0' pdf/{0}.pdf pdf/{0}.pdf".format(name)
    os.system(bash_cmd)
    
