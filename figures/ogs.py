import os
name = os.path.basename(__file__).split(".py")[0]
#
import matplotlib.patches as mpatches
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

import matplotlib.pyplot as plt

patch_ttt_h = mpatches.Patch(color=colors[0], label='ttt_h')
patch_ttt_h_k = mpatches.Patch(color=colors[1], label='ttt_h_k')
patch_ttt_hr_kr = mpatches.Patch(color=colors[2], label='ttt_hr_kr')
patch_ttt_h_kr = mpatches.Patch(color=colors[3], label='ttt_h_kr')

# HANDICAP 19

filtro = ttt_h["s"] == 19
mu = np.array([x for y, x in sorted(zip(ttt_h["h"][filtro],ttt_h.loc[filtro,:].mu)) if y < 9 ])
sigma = np.array([x for y, x in sorted(zip(ttt_h["h"][filtro],ttt_h.loc[filtro,:].sigma)) if y < 9 ])

plt.plot(range(2,9), mu,color=colors[0])
plt.xlabel("Handicap", size=16)
plt.ylabel("Skill", size=16)
plt.scatter(range(2,9), mu,color=colors[0]) 
for i in range(len(mu)):
    plt.plot([i+2,i+2], [mu[i]-sigma[i],mu[i]+sigma[i]], color=colors[0])

name = "ogs/ogs_estimado_handicap.pdf"
plt.savefig(name,pad_inches =0,transparent =True,frameon=True)
bash_cmd = "pdfcrop --margins '0 0 0 0' {0} {0}".format(name)
os.system(bash_cmd)

filtro = (ttt_h_k["s"] == 19) & (ttt_h_k["t"] == "h")
mu = np.array([x for y, x in sorted(zip(ttt_h_k["h"][filtro],ttt_h_k.loc[filtro,:].mu)) if y < 9 ])
sigma = np.array([x for y, x in sorted(zip(ttt_h_k["h"][filtro],ttt_h_k.loc[filtro,:].sigma)) if y < 9 ])

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


filtro = [ True if  ("19)" in h) and int(h.split(",")[0].split("(")[1]) < 9 else False for h in ttt_h_kr.id]
sorted(ttt_h_kr.id[filtro], key= lambda x: int(x.split(",")[0].split("(")[1]) )
mu = np.array([x for y, x in sorted(zip(ttt_h_kr.id[filtro],ttt_h_kr.loc[filtro,:].mu),  key= lambda x: int(x[0].split(",")[0].split("(")[1]))])
sigma = np.array([x for y, x in sorted(zip(ttt_h_kr.id[filtro],ttt_h_kr.loc[filtro,:].sigma), key= lambda x: int(x[0].split(",")[0].split("(")[1]))])

plt.plot(range(2,9), mu,color=colors[3]) 
plt.scatter(range(2,9), mu,color=colors[3]) 
for i in range(len(mu)):
    plt.plot([i+2,i+2], [mu[i]-sigma[i],mu[i]+sigma[i]], color=colors[3])


plt.legend(handles=[patch_ttt_h, patch_ttt_h_k, patch_ttt_hr_kr, patch_ttt_h_kr])

#plt.show()

name = "ogs/ogs_estimado_handicap_con_komi.pdf"
plt.savefig(name,pad_inches =0,transparent =True,frameon=True)
bash_cmd = "pdfcrop --margins '0 0 0 0' {0} {0}".format(name)
os.system(bash_cmd)


# Komi 19

plt.close()
komi = np.arange(0,10)+0.5

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


filtro = (ttt_h_k["s"] == 19) & (ttt_h_k["t"] == "k")
np.array([y for y, x in sorted(zip(ttt_h_k["h"][filtro],ttt_h_k.loc[filtro,:].mu)) if (y in komi) ])
mu = np.array([x for y, x in sorted(zip(ttt_h_k["h"][filtro],ttt_h_k.loc[filtro,:].mu)) if (y in komi)])
sigma = np.array([x for y, x in sorted(zip(ttt_h_k["h"] [filtro],ttt_h_k.loc[filtro,:].sigma)) if (y in komi) ])
plt.plot(komi , mu, color=colors[1]) 
plt.xlabel("Komi", size=16)
plt.ylabel("Skill", size=16)
plt.scatter(komi , mu,color=colors[1]) 
for i in range(len(komi)):
    plt.plot([komi[i],komi[i]], [mu[i]-sigma[i],mu[i]+sigma[i]], color=colors[1])



plt.axhline(y=0.0, color='gray', linestyle='-')
plt.legend(handles=[patch_ttt_h_k, patch_ttt_hr_kr, patch_ttt_h_kr])

#plt.show()

name = "ogs/ogs_estimado_komi.pdf"
plt.savefig(name,pad_inches =0,transparent =True,frameon=True)
bash_cmd = "pdfcrop --margins '0 0 0 0' {0} {0}".format(name)
os.system(bash_cmd)


###--------------
