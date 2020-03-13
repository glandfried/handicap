import os
name = os.path.basename(__file__).split(".py")[0]
############
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import pickle

with open('../data/summary/summary.pickle', 'rb') as handle:
    games_sorted= pickle.load(handle)

handicap_relevance_overall = sum(map(lambda g: int(g['handicap']!=0) ,games_sorted))/sum(map(lambda g: 1 ,games_sorted))


handicap_relevance_history = []
activity = []
year = []
for y in range(2006,2014):
    activity.append(sum(map(lambda g: int(int(g['started'].split('-')[0]) == y) ,games_sorted)))
    handicap_relevance_history.append(sum(map(lambda g: int(g['handicap']!=0 and int(g['started'].split('-')[0]) == y) ,games_sorted))/activity[-1] )
    year.append(y)

fig, ax = plt.subplots()
ax.plot(year,handicap_relevance_history)
ax.set_ylim((0,1))

ix = year
iy = handicap_relevance_history
verts = [(ix[0], 0), *zip(ix, iy), (ix[-1], 0)]
poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
ax.add_patch(poly)

plt.xticks(fontsize=12) # rotation=90
plt.yticks(fontsize=12) # rotation=90

plt.title(r"Handicap relevance", fontsize=16 )
plt.xlabel("Time", fontsize=16 )
plt.ylabel("Proportion", fontsize=16 )

plt.savefig("pdf/"+name+".pdf",pad_inches =0,transparent =True,frameon=True)
bash_cmd = "pdfcrop --margins '0 0 0 0' pdf/{0}.pdf pdf/{0}.pdf".format(name)
os.system(bash_cmd)