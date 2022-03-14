import pandas as pd
import matplotlib.pyplot as plt
from math import log

hk = pd.read_csv('log_ev.csv')
log_ev = (hk['evidence']).apply(lambda x : log(x,10))

######FIGURA 1
plt.figure(figsize=(10,8))
plt.hist(log_ev,25, log = True)
plt.hlines(10,-75,0, colors='grey',linestyle='dotted')
plt.hlines(100,-75,0, colors='grey',linestyle='dotted')
plt.hlines(1000,-75,0, colors='grey',linestyle='dotted')
plt.savefig('evidence_histgram.png')


######FIGURA 2
plt.figure(figsize=(10,7))
plt.scatter(hk['handicap'], log_ev)
#plt.hlines(-70,9,0, colors='grey',linestyle='dotted')
#plt.hlines(-60,9,0, colors='grey',linestyle='dotted')
plt.savefig('evidence_hdcap_scatter.png')
