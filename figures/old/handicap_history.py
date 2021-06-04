import os
name = os.path.basename(__file__).split(".py")[0]
#
import matplotlib.pyplot as plt
##########
import sys
import numpy as np
import pandas as pd
#import numpy as np


df = pd.read_csv('../data/ogs/summary_filtered.csv')
tsh_ogs = pd.read_csv('../estimations/ogs/tsh.csv')
tsh_all_ogs = pd.read_csv('../estimations/ogs/tsh_all.csv')
ttt_ogs = pd.read_csv('../estimations/ogs/ttt.csv')
df_r = df[df.ranked].copy()
df_r = df_r.reset_index()


"El ID es el mismo"
assert list(df.id[df.ranked]) ==  list(ttt_ogs.id)
assert sum(df.id != tsh_ogs.id)==0

"""
plt.plot(range(sum((df_r.handicap==2)&(df_r.width==9))),ttt_ogs[(df_r.handicap==2)&(df_r.width==9)].h_mean)
plt.plot(range(sum((df_r.handicap==3)&(df_r.width==9))),ttt_ogs[(df_r.handicap==3)&(df_r.width==9)].h_mean)
plt.plot(range(sum((df_r.handicap==4)&(df_r.width==9))),ttt_ogs[(df_r.handicap==4)&(df_r.width==9)].h_mean)
"""
plt.plot(range(sum((df_r.handicap==2)&(df_r.width==19))),ttt_ogs[(df_r.handicap==2)&(df_r.width==19)].h_mean)
plt.plot(range(sum((df_r.handicap==3)&(df_r.width==19))),ttt_ogs[(df_r.handicap==3)&(df_r.width==19)].h_mean)
plt.plot(range(sum((df_r.handicap==4)&(df_r.width==19))),ttt_ogs[(df_r.handicap==4)&(df_r.width==19)].h_mean)
plt.plot(range(sum((df_r.handicap==5)&(df_r.width==19))),ttt_ogs[(df_r.handicap==5)&(df_r.width==19)].h_mean)
plt.plot(range(sum((df_r.handicap==6)&(df_r.width==19))),ttt_ogs[(df_r.handicap==6)&(df_r.width==19)].h_mean)
#plt.plot(range(sum((df_r.handicap==7)&(df_r.width==19))),ttt_ogs[(df_r.handicap==7)&(df_r.width==19)].h_mean)
#plt.plot(range(sum((df_r.handicap==8)&(df_r.width==19))),ttt_ogs[(df_r.handicap==8)&(df_r.width==19)].h_mean)
#plt.plot(range(sum((df_r.handicap==9)&(df_r.width==19))),ttt_ogs[(df_r.handicap==9)&(df_r.width==19)].h_mean)



plt.xticks(fontsize=12) # rotation=90
plt.yticks(fontsize=12) # rotation=90
#plt.ylim((-2.5, 5.5)) 

plt.title(r"19 X 19", fontsize=16 )
plt.xlabel("Games", fontsize=16 )
plt.ylabel("Skill", fontsize=16 )

plt.savefig("pdf/"+name+".pdf",pad_inches =0,transparent =True,frameon=True)
bash_cmd = "pdfcrop --margins '0 0 0 0' pdf/{0}.pdf pdf/{0}.pdf".format(name)
os.system(bash_cmd)

