import os
name = os.path.basename(__file__).split(".py")[0]
#
import matplotlib.pyplot as plt # %matplotlib auto
##########
import sys
sys.path.append('../software/')
import skill as trueskill
import ablr # analytic-bayesian-linear-regression own package
import numpy as np
import pickle
#import numpy as np

#if (' point' in g['outcome'] or 'Resignation' == g['outcome'] or 'Timeout'  == g['outcome']) and not g['annulled']:

def games_s_h(s,h):
    return list(filter(lambda g: g['width']==s and g['handicap']==h ,games_sorted))
    

if __name__ == "__main__":

    with open("../data/games_sorted.pickle",'rb') as file:
        games_sorted = pickle.load(file)
    
    """    
    games_sorted[0].keys()
    
    #diff_prod = []
    diff_mean = []
    skill = []
    sigma = []
    handicap = []
    
    for i in range(2,6):	
        dif = list(map(lambda g: (g['black_prior_woh']-g['white_prior_woh']), games_s_h(9,i)  ))
        print(dif)
        diff_mean.append( np.mean(dif))
        #diff_prod.append(np.prod(dif))
        skill.append(diff_mean[-1].mu)
        sigma.append(diff_mean[-1].sigma)
        handicap.append(i)
    for i in range(0,4):
        plt.plot([handicap[i],handicap[i]],[skill[i]+2*sigma[i],skill[i]-2*sigma[i] ],linewidth=0.5,color='grey')
        plt.plot([handicap[i],handicap[i]],[skill[i]+sigma[i],skill[i]-sigma[i] ],linewidth=1,color='black')
        plt.scatter(handicap[i],skill[i])
    
    #dif = list(map(lambda g: (g['black_prior_woh']-g['white_prior_woh']).mu, games_s_h(13,5)  ))
    #diff_mean.append(np.mean(dif))
    #plt.hist(dif,100)
    #plt.axvline(np.mean(dif), color='black', linestyle='-')
    #plt.axvline(0, color='black', linestyle='--',alpha=0.3)
 

    # We will perform a bayesian linear regression
    
    
    
    alpha = 10**(-30) # prior precision
    beta = 1/np.mean(sigma) # Noise of target value
    t = skill
    X_vec = np.array(range(2,6)).reshape(-1, 1) 
    Phi = ablr.linear.phi(X_vec , ablr.linear.identity_basis_function)  
    
    fit_mu, fit_sigma = ablr.linear.posterior(alpha,beta,t,Phi)
    plt.plot([2,5],[fit_mu[0]+fit_mu[1]*2,fit_mu[0]+fit_mu[1]*5],alpha=0.7,color="black")    
    # END: baysian linear regression
    ###
    """
    i = 2
    dif = list(map(lambda g: (g['black_prior_woh']-g['white_prior_woh']).mu, games_s_h(19,i)  ))    
    plt.hist(dif,100)
    plt.axvline(np.mean(dif), color='black', linestyle='-')


    
    plt.xticks(fontsize=12) # rotation=90
    plt.yticks(fontsize=12) # rotation=90
    
    plt.title(r"9 X 9", fontsize=16 )
    plt.xlabel("Handicap", fontsize=16 )
    plt.ylabel("Skill difference (mean)", fontsize=16 )


    plt.savefig("pdf/"+name+".pdf",pad_inches =0,transparent =True,frameon=True)
    bash_cmd = "pdfcrop --margins '0 0 0 0' pdf/{0}.pdf pdf/{0}.pdf".format(name)
    os.system(bash_cmd)
    
