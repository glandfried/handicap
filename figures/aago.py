import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Polygon

import json

df = pd.read_csv('../data/aago/summary_filtered.csv')
# Opening JSON file 
f = open('../estimations/aago/ttt_all.json',) 
data = json.load(f) 


for j in data:
    
    if (not "(" in j) and len(data[j][0])//2 > 20:
        m = data[j][0][0:(len(data[j][0])//2)]
        plt.plot(m)

for j in data:    
    if (not "(" in j) and len(data[j][0])//2 > 1 and  len(data[j][0])//2 < 8:
        m = data[j][0][0:(len(data[j][0])//2)]
        plt.plot(m)

for j in data:
    if "(" in j:
        m = data[j][0][0:(len(data[j][0])//2)]
        plt.plot(m)
        
        x = list(range(len(data[j][0])//2))
        x = x+ list(reversed(x))
        y = m + 1* np.array(data[j][1][0:(len(data[j][0])//2)] )
        y = list(y) + list(reversed(m - 1* np.array(data[j][1][0:(len(data[j][0])//2)] )))
        plt.plot(m,color="black")
        plt.fill(x,y)
    


"""        
for j in data:
    
    if (not "(" in j) and len(data[j][0])//2 > 20:
        m = data[j][0][0:(len(data[j][0])//2)]
        plt.plot(m,color="black")
        
        x = list(range(len(data[j][0])//2))
        x = x+ list(reversed(x))
        y = m + 1* np.array(data[j][1][0:(len(data[j][0])//2)] )
        y = list(y) + list(reversed(m - 1* np.array(data[j][1][0:(len(data[j][0])//2)] )))
        plt.plot(m,color="black")
        plt.fill(x,y)
    
        
for j in data:
    if (not "(" in j) and len(data[j][0])//2 > 20:
        eventos = list(set(list(df.event_id[(df.white_player_id == int(j)) | (df.black_player_id == int(j))])))
        plt.plot(eventos, data[j][0][0:(len(data[j][0])//2)])


"""