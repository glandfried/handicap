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


#if (' point' in g['outcome'] or 'Resignation' == g['outcome'] or 'Timeout'  == g['outcome']) and not g['annulled']:

if __name__ == "__main__":

    with open("../data/games_sorted.pickle",'rb') as file:
        games_sorted = pickle.load(file)
    
    games_sorted[0].keys()
    def games_s_h(s,h):
        return list(filter(lambda g: g['width']==s and g['handicap']==h ,games_sorted))
    
    diff_mean = []
    for i in range(2,10):
        #dif = list(map(lambda g: (g['black_prior_woh']-g['white_prior_woh']).mu, games_s_h(19,i)  ))
        dif = list(map(lambda g: (g['black_prior_woh']-g['white_prior_woh']), games_s_h(19,i)  ))
        np.sum(dif)/len(dif)
        #plt.hist(dif,100)
        #plt.axvline(np.mean(dif), color='black', linestyle='-')
        #plt.axvline(0, color='black', linestyle='--',alpha=0.3)
        diff_mean.append(np.mean(dif))
    
    plt.scatter(range(2,10),diff_mean)

    # We will perform a bayesian linear regression
    alpha = 10**(-30) # prior precision
    beta = 1/0.3 # Noise of target value
    t = diff_mean[0:7]
    X_vec = np.array(range(2,9)).reshape(-1, 1) 
    Phi = ablr.linear.phi(X_vec , ablr.linear.identity_basis_function)  
    
    fit_mu, fit_sigma = ablr.linear.posterior(alpha,beta,t,Phi)
    plt.plot([2,8],[fit_mu[0]+fit_mu[1]*2,fit_mu[0]+fit_mu[1]*8],alpha=0.7,color="black")    
    # END: baysian linear regression
    ###
    
    plt.xticks(fontsize=12) # rotation=90
    plt.yticks(fontsize=12) # rotation=90
    
    plt.title(r"19 X 19", fontsize=16 )
    plt.xlabel("Handicap", fontsize=16 )
    plt.ylabel("Skill difference (mean)", fontsize=16 )


    plt.savefig("pdf/"+name+".pdf",pad_inches =0,transparent =True,frameon=True)
    bash_cmd = "pdfcrop --margins '0 0 0 0' pdf/{0}.pdf pdf/{0}.pdf".format(name)
    os.system(bash_cmd)
    
