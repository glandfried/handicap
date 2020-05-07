import os
name = os.path.basename(__file__).split(".py")[0]
############
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import pandas as pd
import numpy as np
import pickle


csv_name = '../data/summary_filtered.csv'
#csv_name = '/home/mati/Storage/Doctorado/Licar/licar/papers/2020_Handicap/nucleo/data/DataFramePurge.csv'
 
df = pd.read_csv(csv_name)

fig, ax = plt.subplots()
filtro = (df.komi !=6.5)&(df.ranked)
ax.hist(df[filtro].komi,bins=np.arange(min(df[filtro].komi), max(df[filtro].komi) + 1, 1))
#ax.set_ylim((0,1))
#ix = year
#iy = handicap_relevance_history
#verts = [(ix[0], 0), *zip(ix, iy), (ix[-1], 0)]
#poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
#ax.add_patch(poly)
plt.xticks(fontsize=12) # rotation=90
plt.yticks(fontsize=12) # rotation=90
plt.title(r"", fontsize=16 )
plt.xlabel("Komi", fontsize=16 )
plt.ylabel("Proportion", fontsize=16 )

plt.savefig("pdf/"+name+".pdf",pad_inches =0,transparent =True,frameon=True)
bash_cmd = "pdfcrop --margins '0 0 0 0' pdf/{0}.pdf pdf/{0}.pdf".format(name)
os.system(bash_cmd)