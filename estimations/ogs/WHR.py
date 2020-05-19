import os
name = os.path.basename(__file__).split(".py")[0]
##################
#import time
import pandas as pd
import numpy as np
from datetime import datetime

# Posible variable
dataset = 'ogs'

# Data
df = pd.read_csv('../../data/'+dataset+'/summary_filtered.csv')

days=list(map(lambda x: int(datetime.strptime(x.split("T")[0],  "%Y-%m-%d").timestamp()/(60*60*24)), df.started) )
m = min(days)
days = [(d+1)-m for d in days]
composition = [str(w)+" "+str(b)+" "+("B" if r else "W")+" "+str(d)+" "+"0"  for w, b, d, r in zip(df.white, df.black, days,df.black_win ) ]   
composition = [ c for c, rank in zip(composition,df.ranked) if rank] 

from whr import whole_history_rating
whr = whole_history_rating.Base()
whr.load_games(composition)
whr.iterate(4)

#whr.games[99].white_player.days[0].uncertainty*100
#whr.player_by_name("2100")[0]
#whr.ratings_for_player("2100")[0]

evidence = [ w.black_win_probability() if r else w.white_win_probability() for w,r in zip(whr.games,df.black_win[df.ranked])]

res = df[['id']][df.ranked].copy() 
res["evidence"] = evidence

res.to_csv(name+".csv", index=False)
