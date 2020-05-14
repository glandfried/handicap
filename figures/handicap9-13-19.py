#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 10:32:51 2020

@author: mati
"""
import os
name = os.path.basename(__file__).split(".py")[0]
#
import matplotlib.pyplot as plt


##########
#import sys
#sys.path.append('../software/trueskill.py/')
import pandas as pd
#import src as trueskill
#import ablr # analytic-bayesian-linear-regression own package
import numpy as np
#import numpy as np

df = pd.read_csv('../data/ogs/summary_filtered.csv')
tsh_ogs = pd.read_csv('../estimations/ogs/tsh.csv')

"El ID es el mismo"
assert sum(df.id != tsh_ogs.id)==0

log_evidence = np.sum(np.log(tsh_ogs[tsh_ogs.estimated].evidence))
mean_log_evidence = log_evidence/sum(tsh_ogs.estimated)
np.exp(mean_log_evidence)

skill9 = [tsh_ogs[(df.handicap==i)&(df.width==9)].iloc[-1].h_mean for i in range(2,6)]
sigma9 = [tsh_ogs[(df.handicap==i)&(df.width==9)].iloc[-1].h_std for i in range(2,6)]
skill13= [tsh_ogs[(df.handicap==i)&(df.width==13)].iloc[-1].h_mean for i in range(2,8)]
sigma13 = [tsh_ogs[(df.handicap==i)&(df.width==13)].iloc[-1].h_std for i in range(2,8)]
skill19 = [tsh_ogs[(df.handicap==i)&(df.width==19)].iloc[-1].h_mean for i in range(2,10)]
sigma19 = [tsh_ogs[(df.handicap==i)&(df.width==19)].iloc[-1].h_std for i in range(2,10)]
handicap9 = list(range(2,6))
handicap13 = list(range(2,8))
handicap19 = list(range(2,10))
        
width= [9,13,19]
handicaps = [handicap9,handicap13,handicap19] 
skills = [skill9,skill13,skill19]
sigmas = [sigma9,sigma13,sigma19]
FitHarcodeado = [5,8,8]

for j in range(3):
    for i in range(len(handicaps[j])):
        plt.figure(j)
        plt.plot([handicaps[j][i],handicaps[j][i]],[skills[j][i]+2*sigmas[j][i], skills[j][i]-2*sigmas[j][i] ],linewidth=0.5,color='grey')
        plt.plot([handicaps[j][i],handicaps[j][i]],[skills[j][i]+sigmas[j][i], skills[j][i]-sigmas[j][i] ],linewidth=1,color='black')
        plt.scatter(handicaps[j][i],skills[j][i])
    """
    X_vec = 0
    t = 0
    Phi = 0
    beta = 0
    alpha = 10**(-30) # prior precision
    beta = 1/np.mean(sigmas[j]) # Noise of target value
    
    t = skills[j]
    X_vec = np.array(handicaps[j]).reshape(-1, 1) 
    Phi = ablr.linear.phi(X_vec , ablr.linear.identity_basis_function)  

    
    fit_mu, fit_sigma = ablr.linear.posterior(alpha,beta,t,Phi)
    plt.plot([min(handicaps[j]),max(handicaps[j])],[fit_mu[0]+fit_mu[1]*2,fit_mu[0]+fit_mu[1]*FitHarcodeado[j]],color="black")    
    # END: baysian linear regression
    print(fit_mu, fit_sigma )
    """
###
    
    plt.xticks(fontsize=12) # rotation=90
    plt.yticks(fontsize=12) # rotation=90
    
    plt.title(rf"{width[j]}X{width[j]}", fontsize=16 )
    plt.xlabel("Handicap", fontsize=16 )
    plt.ylabel("Skill", fontsize=16 )
    
    plt.savefig("pdf/"+name+str(width[j])+".pdf",pad_inches =0,transparent =True,frameon=True)
    bash_cmd = "pdfcrop --margins '0 0 0 0' pdf/{0}.pdf pdf/{0}.pdf".format(name+str(width[j]))
    os.system(bash_cmd)

