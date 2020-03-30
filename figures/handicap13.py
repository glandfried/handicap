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

if __name__ == "__main__":

    with open("../data/handicap.pickle",'rb') as file:
        handicap = pickle.load(file)
    with open("../data/handicap_history.pickle",'rb') as file:
        handicap_history = pickle.load(file)

    skill = []
    sigma = []
    handicap13 = []
    for i in range(2,10):
        skill.append(handicap[(i,13)].mu)
        sigma.append(handicap[(i,13)].sigma)
        handicap13.append(i)
        plt.plot([handicap13[-1],handicap13[-1]],[skill[-1]+2*sigma[-1],skill[-1]-2*sigma[-1] ],linewidth=0.5,color='grey')
        plt.plot([handicap13[-1],handicap13[-1]],[skill[-1]+sigma[-1],skill[-1]-sigma[-1] ],linewidth=1,color='black')
        plt.scatter(i,handicap[(i,13)].mu)
    
    #plt.scatter(handicap13,skill, color='black',s=40)
    
    ####
    # We will perform a bayesian linear regression
    alpha = 10**(-30) # prior precision
    beta = 1/np.mean(sigma[0:7]) # Noise of target value
    t = skill[0:7]
    X_vec = np.array(handicap13[0:7]).reshape(-1, 1) 
    Phi = ablr.linear.phi(X_vec , ablr.linear.identity_basis_function)  
    
    fit_mu, fit_sigma = ablr.linear.posterior(alpha,beta,t,Phi)
    plt.plot([2,8],[fit_mu[0]+fit_mu[1]*2,fit_mu[0]+fit_mu[1]*8])    
    # END: baysian linear regression
    ###
    
    plt.xticks(fontsize=12) # rotation=90
    plt.yticks(fontsize=12) # rotation=90
    
    plt.title(r"13 X 13", fontsize=16 )
    plt.xlabel("Handicap", fontsize=16 )
    plt.ylabel("Skill", fontsize=16 )
    
    plt.savefig("pdf/"+name+".pdf",pad_inches =0,transparent =True,frameon=True)
    bash_cmd = "pdfcrop --margins '0 0 0 0' pdf/{0}.pdf pdf/{0}.pdf".format(name)
    os.system(bash_cmd)
    