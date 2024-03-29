import os
name = os.path.basename(__file__).split(".py")[0]
#
import matplotlib.pyplot as plt
##########
import sys
sys.path.append('../software/')
import pandas as pd
#import src as trueskill
import ablr # analytic-bayesian-linear-regression own package
import numpy as np
#import numpy as np

#sum(df[df.handicap >1].black_win)/sum(df.handicap >1)

df = pd.read_csv('../data/ogs/summary_filtered.csv')
tsh_ogs = pd.read_csv('../estimations/ogs/tsh.csv')
tsh_ogs = tsh_ogs[tsh_ogs.id.isin(df.id)].copy() # xq fueron corridos antes del ultimo filtro
tsh_ogs  = tsh_ogs.reset_index() # xq fueron corridos antes del ultimo filtro
tsh_all_ogs = pd.read_csv('../estimations/ogs/tsh_all.csv')
tsh_all_ogs = tsh_all_ogs[tsh_all_ogs.id.isin(df.id)].copy() # xq fueron corridos antes del ultimo filtro
tsh_all_ogs  = tsh_all_ogs.reset_index() # xq fueron corridos antes del ultimo filtro
ttt_ogs = pd.read_csv('../estimations/ogs/ttt.csv')
ttt_all_ogs = pd.read_csv('../estimations/ogs/ttt_all.csv')
df_r = df[df.ranked].copy()
df_r = df_r.reset_index()

"El ID es el mismo"
assert list(df.id[df.ranked]) ==  list(ttt_ogs.id)
assert sum(df.id != tsh_ogs.id)==0

log_evidence_ttt = np.sum(np.log(ttt_ogs.evidence))
mean_log_evidence_ttt = log_evidence_ttt/len(ttt_ogs.id)
np.exp(mean_log_evidence_ttt)

log_evidence = np.sum(np.log(tsh_ogs[tsh_ogs.estimated].evidence))
mean_log_evidence = log_evidence/sum(tsh_ogs.estimated)
np.exp(mean_log_evidence)

model_selection = log_evidence_ttt - log_evidence 

skill9_ttt = [ttt_ogs[(df_r.handicap==i)&(df_r.width==9)].iloc[-1].h_mean for i in range(2,6)]
sigma9_ttt = [ttt_ogs[(df_r.handicap==i)&(df_r.width==9)].iloc[-1].h_std for i in range(2,6)]
skill13_ttt= [ttt_ogs[(df_r.handicap==i)&(df_r.width==13)].iloc[-1].h_mean for i in range(2,8)]
sigma13_ttt = [ttt_ogs[(df_r.handicap==i)&(df_r.width==13)].iloc[-1].h_std for i in range(2,8)]
skill19_ttt = [ttt_ogs[(df_r.handicap==i)&(df_r.width==19)].iloc[-1].h_mean for i in range(2,10)]
sigma19_ttt = [ttt_ogs[(df_r.handicap==i)&(df_r.width==19)].iloc[-1].h_std for i in range(2,10)]


skill19_ttt_all = np.array([ttt_all_ogs[(df.handicap==i)&(df.width==19)].iloc[-1].h_mean for i in range(2,10)])
sigma19_ttt_all = np.array([ttt_all_ogs[(df.handicap==i)&(df.width==19)].iloc[-1].h_std for i in range(2,10)])
handicap = np.array(list(range(2,10)))

def plot(handicap, skill, sigma, algorithm,plot=False):
    plt.close()
    plt.plot([handicap,handicap] ,[skill+2*sigma,skill-2*sigma],linewidth=0.5,color='grey')
    plt.plot([handicap,handicap] ,[skill+1*sigma,skill-1*sigma],linewidth=1,color='black')
    plt.scatter(handicap ,skill)
    
    X_vec = 0
    t = 0
    Phi = 0
    beta = 0
    alpha = 10**(-30) # prior precision
    beta = 1/np.mean(sigma) # Noise of target value
    
    t = skill
    X_vec = np.array(handicap).reshape(-1, 1) 
    Phi = ablr.linear.phi(X_vec , ablr.linear.identity_basis_function)  
    fit_mu, fit_sigma = ablr.linear.posterior(alpha,beta,t,Phi)
    plt.plot([min(handicap),max(handicap)],[fit_mu[0]+fit_mu[1]*2,fit_mu[0]+fit_mu[1]*9],color="black")    
    
    if plot:
        plt.tight_layout()
        plt.xlabel("Handicap", fontsize=16 )
        plt.ylabel("Skill", fontsize=16 )
        plt.savefig("pdf/"+name+"_"+algorithm+".pdf",bbox_inches='tight')
        plt.savefig("png/"+name+"_"+algorithm+".png",bbox_inches='tight', transparent=True)
        

skill = np.array([ttt_all_ogs[(df.handicap==i)&(df.width==19)].iloc[-1].h_mean for i in range(2,10)])
sigma = np.array([ttt_all_ogs[(df.handicap==i)&(df.width==19)].iloc[-1].h_std for i in range(2,10)])
handicap = np.array(list(range(2,10)))
plot(handicap, skill, sigma, "ttt_all",True)

skill = np.array([tsh_all_ogs[(df.handicap==i)&(df.width==19)].iloc[-1].h_mean for i in range(2,10)])
sigma = np.array([tsh_all_ogs[(df.handicap==i)&(df.width==19)].iloc[-1].h_std for i in range(2,10)])
handicap = np.array(list(range(2,10)))
plot(handicap, skill, sigma, "tsh_all", True)

if False: 
    plt.plot(skill19_ttt_all ); plt.plot(skill19_ttt)


if False:
    
    handicaps = list(set(zip(df_r.handicap,df_r.width)))
    for h in handicaps:
        if h[0]>1 and h[1]==19 and h[0]<=9:
            filtro = (df_r.handicap == h[0]) & (df_r.width == h[1])
            curva = ttt_ogs[filtro].h_mean
            plt.plot(range(len(curva )) ,curva )
    
    
    handicaps = list(set(zip(df.handicap,df.width)))
    for h in handicaps:
        if h[0]>1 and h[1]==19 and h[0]<=9:
            filtro = (df.handicap == h[0]) & (df.width == h[1])
            curva = ttt_all_ogs[filtro].h_mean
            plt.plot(range(len(curva )) ,curva )
        
    handicaps = list(range(2,10))
    skills = skill19_ttt_all 
    sigmas = sigma19_ttt_all 
    for i in range(len(handicaps)):
        plt.plot([handicaps[i],handicaps[i]],[skills[i]+2*sigmas[i], skills[i]-2*sigmas[i] ],linewidth=0.5,color='grey')
        plt.plot([handicaps[i],handicaps[i]],[skills[i]+sigmas[i], skills[i]-sigmas[i] ],linewidth=1,color='black')
        plt.scatter(handicaps[i],skills[i])
    
    
    X_vec = 0
    t = 0
    Phi = 0
    beta = 0
    alpha = 10**(-30) # prior precision
    beta = 1/np.mean(sigmas) # Noise of target value
    
    t = skills
    X_vec = np.array(handicaps).reshape(-1, 1) 
    Phi = ablr.linear.phi(X_vec , ablr.linear.identity_basis_function)  

    
    fit_mu, fit_sigma = ablr.linear.posterior(alpha,beta,t,Phi)
    plt.plot([min(handicaps),max(handicaps)],[fit_mu[0]+fit_mu[1]*2,fit_mu[0]+fit_mu[1]*9],color="black")    
    # END: baysian linear regression
    print(fit_mu, fit_sigma )
    
    
    

"""
Observaci\'on:
    Las estimaciones finales del TTT en general son muy parecidas a las de trueskill.
    En este caso tambi\'en son parecidas para los handicap 
"""

if False:

    skill9 = [tsh_ogs[(df.handicap==i)&(df.width==9)].iloc[-1].h_mean for i in range(2,6)]
    sigma9 = [tsh_ogs[(df.handicap==i)&(df.width==9)].iloc[-1].h_std for i in range(2,6)]
    skill13= [tsh_ogs[(df.handicap==i)&(df.width==13)].iloc[-1].h_mean for i in range(2,8)]
    sigma13 = [tsh_ogs[(df.handicap==i)&(df.width==13)].iloc[-1].h_std for i in range(2,8)]
    skill19 = [tsh_ogs[(df.handicap==i)&(df.width==19)].iloc[-1].h_mean for i in range(2,10)]
    sigma19 = [tsh_ogs[(df.handicap==i)&(df.width==19)].iloc[-1].h_std for i in range(2,10)]
    handicap9 = list(range(2,6))
    handicap13 = list(range(2,8))
    handicap19 = list(range(2,10))
    
    #plt.plot(skill19_ttt);plt.plot(skill19)
    
            
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
    
