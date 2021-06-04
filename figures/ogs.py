import os
name = os.path.basename(__file__).split(".py")[0]
#
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
###--------------
import sys
import numpy as np
import pandas as pd
from ast import literal_eval

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

ttt_h = pd.read_csv('../estimations/output/ogs_ttt-h.csv')
vectors = [ literal_eval(x) for x in ttt_h.iloc[:,0]]
ttt_h["h"] = np.array([ v[0] for v in vectors])
ttt_h["s"] = np.array([ v[1] for v in vectors])

ttt_h_k = pd.read_csv('../estimations/output/ogs_ttt-h-k.csv')
vectors = [ literal_eval(x) for x in ttt_h_k.iloc[:,0]]
ttt_h_k["t"] = [ "k" if ("." in x) else "h" for x in ttt_h_k.iloc[:,0]]
ttt_h_k["h"] = np.array([ v[0] for v in vectors])
ttt_h_k["s"] = np.array([ v[1] for v in vectors])

ttt_hr_kr = pd.read_csv('../estimations/output/ogs_ttt-h_regression-komi-regression.csv')

ttt_h_kr = pd.read_csv('../estimations/output/ogs_ttt-h-komi-regression.csv')

# HANDICAP 19

filtro = ttt_h["s"] == 19
mu = np.array([x for y, x in sorted(zip(ttt_h["h"][filtro],ttt_h.loc[filtro,:].mu)) if y < 9 ])
sigma = np.array([x for y, x in sorted(zip(ttt_h["h"][filtro],ttt_h.loc[filtro,:].sigma)) if y < 9 ])

plt.plot(range(2,9), mu,color=colors[0]) 
plt.scatter(range(2,9), mu,color=colors[0]) 
for i in range(len(mu)):
    plt.plot([i+2,i+2], [mu[i]-sigma[i],mu[i]+sigma[i]], color=colors[0])

filtro = (ttt_h_k["s"] == 19) & (ttt_h_k["t"] == "h")
mu = np.array([x for y, x in sorted(zip(ttt_h_k["h"][filtro],ttt_h_k.loc[filtro,:].mu)) if y < 9 ])
sigma = np.array([x for y, x in sorted(zip(ttt_h_k["h" [filtro],ttt_h_k.loc[filtro,:].sigma)) if y < 9 ])

plt.plot(range(2,9), mu,color=colors[1]) 
plt.scatter(range(2,9), mu,color=colors[1]) 
for i in range(len(mu)):
    plt.plot([i+2,i+2], [mu[i]-sigma[i],mu[i]+sigma[i]], color=colors[1])

filtro = ttt_hr_kr.id == "_handicap19_1_" 
mu = [ i*float(ttt_hr_kr[filtro].mu) for i in range(2,9)]
sigma = [ i*float(ttt_hr_kr[filtro].sigma) for i in range(2,9)]
plt.plot(range(2,9), mu,color=colors[2]) 
plt.scatter(range(2,9), mu,color=colors[2]) 
for i in range(len(mu)):
    plt.plot([i+2,i+2], [mu[i]-sigma[i],mu[i]+sigma[i]], color=colors[2])

plt.show()

# Komi 19

komi = np.arange(0,10)+0.5

filtro = (ttt_h_k["s"] == 19) & (ttt_h_k["t"] == "k")
np.array([y for y, x in sorted(zip(ttt_h_k["h"][filtro],ttt_h_k.loc[filtro,:].mu)) if (y in komi) ])
mu = np.array([x for y, x in sorted(zip(ttt_h_k["h"][filtro],ttt_h_k.loc[filtro,:].mu)) if (y in komi)])
sigma = np.array([x for y, x in sorted(zip(ttt_h_k["h"] [filtro],ttt_h_k.loc[filtro,:].sigma)) if (y in komi) ])
plt.plot(komi , mu, color=colors[1]) 
plt.scatter(komi , mu,color=colors[1]) 
for i in range(len(komi)):
    plt.plot([komi[i],komi[i]], [mu[i]-sigma[i],mu[i]+sigma[i]], color=colors[1])

filtro = ttt_hr_kr.id == "_komi19_1_" 
mu1 = np.array([ (i+0.5)*float(ttt_hr_kr[filtro].mu) for i in range(0,10)])
sigma1 = np.array([ (i+0.5)*float(ttt_hr_kr[filtro].sigma) for i in range(0,10)])
filtro = ttt_hr_kr.id == "_komi19_0_" 
mu0 = float(ttt_hr_kr[filtro].mu)
sigma0 = float(ttt_hr_kr[filtro].sigma)
sigma = np.sqrt(sigma1**2+sigma0)
mu=mu1+mu0
plt.plot(komi , mu, color=colors[2]) 
plt.scatter(komi , mu,color=colors[2]) 
for i in range(len(komi)):
    plt.plot([komi[i],komi[i]], [mu[i]-sigma[i],mu[i]+sigma[i]], color=colors[2])


filtro = ttt_h_kr.id == "_komi19_1_" 
mu1 = np.array([ (i+0.5)*float(ttt_h_kr[filtro].mu) for i in range(0,10)])
sigma1 = np.array([ (i+0.5)*float(ttt_h_kr[filtro].sigma) for i in range(0,10)])
filtro = ttt_h_kr.id == "_komi19_0_" 
mu0 = float(ttt_h_kr[filtro].mu)
sigma0 = float(ttt_h_kr[filtro].sigma)
sigma = np.sqrt(sigma1**2+sigma0)
mu=mu1+mu0
plt.plot(komi , mu, color=colors[3]) 
plt.scatter(komi , mu,color=colors[3]) 
for i in range(len(komi)):
    plt.plot([komi[i],komi[i]], [mu[i]-sigma[i],mu[i]+sigma[i]], color=colors[3])


plt.axhline(y=0.0, color='gray', linestyle='-')
plt.show()

###--------------
plt.savefig("pdf/"+name+".pdf",pad_inches =0,transparent =True,frameon=True)
bash_cmd = "pdfcrop --margins '0 0 0 0' pdf/{0}.pdf pdf/{0}.pdf".format(name)
os.system(bash_cmd)
