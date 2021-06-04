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
        
    plt.plot(list(map(lambda x: x.mu, handicap_history[(2,19)] )) )
    plt.plot(list(map(lambda x: x.mu, handicap_history[(3,19)] )) )
    plt.plot(list(map(lambda x: x.mu, handicap_history[(4,19)] )) )
    plt.plot(list(map(lambda x: x.mu, handicap_history[(5,19)] )) )
    plt.plot(list(map(lambda x: x.mu, handicap_history[(6,19)] )) )
    plt.plot(list(map(lambda x: x.mu, handicap_history[(7,19)] )) )
    plt.plot(list(map(lambda x: x.mu, handicap_history[(8,19)] )) )
    plt.plot(list(map(lambda x: x.mu, handicap_history[(9,19)] )) )
    
    plt.xticks(fontsize=12) # rotation=90
    plt.yticks(fontsize=12) # rotation=90
    #plt.ylim((-2.5, 5.5)) 
    
    plt.title(r"19 X 19", fontsize=16 )
    plt.xlabel("Games", fontsize=16 )
    plt.ylabel("Skill", fontsize=16 )

    
    plt.savefig("pdf/"+name+".pdf",pad_inches =0,transparent =True,frameon=True)
    bash_cmd = "pdfcrop --margins '0 0 0 0' pdf/{0}.pdf pdf/{0}.pdf".format(name)
    os.system(bash_cmd)
    
