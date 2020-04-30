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
import sys
sys.path.append('../software')
import trueskill
import ablr # analytic-bayesian-linear-regression own package
import numpy as np
import pickle
#import numpy as np
with open("/home/mati/Storage/Doctorado/Licar/licar/papers/2020_Handicap/nucleo/data/handicap.pickle",'rb') as file:
    handicap = pickle.load(file)
with open("/home/mati/Storage/Doctorado/Licar/licar/papers/2020_Handicap/nucleo/data/handicap_history.pickle",'rb') as file:
    handicap_history = pickle.load(file)
#%%
skill9 = []
sigma9 = []
skill13= []
sigma13 = []
skill19 = []
sigma19 = []
handicap9 = []
handicap13 = []
handicap19 = []

#%%
for i in handicap: # i es el key
    if (i[1] == 9) & (i[0]>1) & (i[0]<6):
        handicap9.append(i[0])
        skill9.append(handicap[i].mu)
        sigma9.append(handicap[i].sigma)
  
    elif (i[1] == 13) & (i[0]>1) & (i[0]<8):
        handicap13.append(i[0])
        skill13.append(handicap[i].mu)
        sigma13.append(handicap[i].sigma) 
     
    elif (i[1] == 19) & (i[0]>1) & (i[0]<9):
        handicap19.append(i[0])
        skill19.append(handicap[i].mu)
        sigma19.append(handicap[i].sigma)
        
handicap9 = np.array(handicap9)
skill9 = np.array(skill9)
sigma9 = np.array(sigma9)
idx9   = np.argsort(handicap9)
handicap9 = np.array(handicap9)[idx9]
skill9 = np.array(skill9)[idx9]
sigma9 = np.array(sigma9)[idx9]

handicap13 = np.array(handicap13)
skill13 = np.array(skill13)
sigma13 = np.array(sigma13)
idx13  = np.argsort(handicap13)
handicap13 = np.array(handicap13)[idx13]
skill13 = np.array(skill13)[idx13]
sigma13 = np.array(sigma13)[idx13]

handicap19 = np.array(handicap19)
skill19 = np.array(skill19)
sigma19 = np.array(sigma19)
idx19  = np.argsort(handicap19)
handicap19 = np.array(handicap19)[idx19]
skill19 = np.array(skill19)[idx19]
sigma19 = np.array(sigma19)[idx19]


width = [9,13,19]
handicaps = [handicap9,handicap13,handicap19] 
skills = [skill9,skill13,skill19]
sigmas = [sigma9,sigma13,sigma19]
FitHarcodeado = [5,8,8]
#%%
for j in range(3):
    for i in range(len(handicaps[j])):
        plt.figure(j)
        plt.plot([handicaps[j][i],handicaps[j][i]],[skills[j][i]+2*sigmas[j][i], skills[j][i]-2*sigmas[j][i] ],linewidth=0.5,color='grey')
        plt.plot([handicaps[j][i],handicaps[j][i]],[skills[j][i]+sigmas[j][i], skills[j][i]-sigmas[j][i] ],linewidth=1,color='black')
        plt.scatter(handicaps[j][i],skills[j][i])
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
###
    
    plt.xticks(fontsize=12) # rotation=90
    plt.yticks(fontsize=12) # rotation=90
    
    plt.title(rf"{width[j]}X{width[j]}", fontsize=16 )
    plt.xlabel("Handicap", fontsize=16 )
    plt.ylabel("Skill", fontsize=16 )
    
#%%
