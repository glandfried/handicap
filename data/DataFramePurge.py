
##!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pickle
import pandas as pd
import sys
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('../software/')

csv_name = 'summary.csv'
#csv_name = '/home/mati/Storage/Doctorado/Licar/licar/papers/2020_Handicap/nucleo/data/summaryJson.csv'

## %%
print("Dataframe metida")   
df = pd.read_csv(csv_name)
df = df[['id','black','white','order','outcome','handicap','komi','width', 'annulled','ranked','started','ended']]


#plt.hist(df[df.komi<100].komi,bins=np.arange(min(df[df.komi<0].komi), max(df[df.komi<0].komi) + 1, 1))
#df[(df.komi<0)&(df.handicap<9)][['komi','handicap','white_ranking','black_ranking']]
#df[(df.komi<0)&(df.handicap==9)][['komi','handicap','order','puntos']]
#filtro = (df.ranked)&(df.komi<0)
#plt.hist(df[filtro].komi,bins=np.arange(min(df[filtro].komi), max(df[filtro].komi) + 1, 1))



DatosText = {}
DatosText['PartidasTotales']= int(df.shape[0])
DatosText['handicap1'] = int(df.handicap[df["handicap"] == 1].count())
DatosText['handicapMayor1'] = int(df.handicap[df["handicap"] > 1].count())
DatosText['handicapMayor9x9'] = int(df.handicap[(df["handicap"] > 1)&(df["width"] == 9)].count())
DatosText['handicapMayor13x13'] = int(df.handicap[(df["handicap"] > 1)&(df["width"] == 13)].count())
DatosText['handicapMayor19x19'] = int(df.handicap[(df["handicap"] > 1)&(df["width"] == 19)].count())
DatosText['handicap0'] = int(df.handicap[df["handicap"] == 0].count())
DatosText['handicapNegativa'] = int(df.handicap[df["handicap"] < 0].count())
DatosText['PartidasAnuladas'] = int(df.annulled[df["annulled"] == True].count())
DatosText['PartidasOtras'] = sum(~((df.outcome == 'Resignation') | (df.outcome == 'Timeout') | (df.outcome.str.contains(' point'))))
DatosText['PartidasPuntos'] = int(df.outcome[df.outcome.str.contains(' point',na=False)].count())
DatosText['PartidasResignacion'] = int(df.outcome[df["outcome"] == 'Resignation'].count())
DatosText['PartidasSinTiempo'] = int(df.outcome[df["outcome"] == 'Timeout'].count())
DatosText['Partidas9x9'] = int(df.width[df["width"] == 9].count())
DatosText['Partidas13x13'] = int(df.width[df["width"] == 13].count())
DatosText['Partidas19x19'] = int(df.width[df["width"] == 19].count())
DatosText['Partidas-No-9-13-19'] = int(df.width[(df["width"] != 9)&( df["width"] != 13)&(df["width"] != 19)].count())
DatosText['Rankeadas'] = sum(df.ranked)
DatosText['RankeadasResignation'] = sum(df.ranked&(df["outcome"] == 'Resignation'))/DatosText['PartidasResignacion']
DatosText['RankeadasPuntos'] = sum(df.ranked&(df.outcome.str.contains(' point',na=False)))/DatosText['PartidasPuntos']
DatosText['RankeadasSinTiempo'] =  sum(df.ranked&(df["outcome"] == 'Timeout'))/DatosText['PartidasSinTiempo']
DatosText['KomiNegativo'] = sum((df.komi<0))
DatosText['RankeadasKomiNegativo'] = sum((df.ranked)&(df.komi<0))


filtered = {}
##%% Selecciono las columnas que quiero y las filas con ciertas restricciones
filtered['Annulled'] = sum(df.annulled != False)  
df = df[df.annulled == False]
filtered['Outcomes'] = sum(~((df.outcome == 'Resignation') | (df.outcome == 'Timeout') | (df.outcome.str.contains(' point'))))
df = df[(df.outcome == 'Resignation') | (df.outcome == 'Timeout') | (df.outcome.str.contains(' point'))]
filtered['Width'] = sum(~((df["width"] >= 9) & (df["width"] <=19 )))
df = df[(df["width"] >= 9) & (df["width"] <=19 )]
filtered['Order'] = sum(~((df.order != "(0, 0)")&(df.order != "(1, 1)")))
df = df[(df.order != "(0, 0)")&(df.order != "(1, 1)")]#np.sum(df.order == "(0, 0)")

##%% Hago una columna con los puntos de las partidas ganadas como tal
replace_values = {' points': '', ' point': '','Resignation': None,'Timeout': None}
df['puntos'] = df.outcome.replace(replace_values, regex=True)
#Hago Float los puntos
df.puntos = df.puntos.map(lambda x: float(x) if isinstance(x, str) else  None )
# Los komi ya son float
#df.komi = df.komi.map(lambda x: StrToFloat(x))
##%% Hago el order con formato lista para poder luego usar como argumento de las funciones de skill
df["black_win"] = df.order.map(lambda x :  1 if x[1]=='1' else -1)
df['black_win_not_komi'] =  np.sign(df.black_win*df.puntos+(df.komi-6.5))
DatosText['PartidasGanadasPorKomi'] = int(np.sum([(~df.puntos.isnull())&(df.black_win != df.black_win_not_komi)]))
## %% Genero una lista results, la cual es order pero sin consdierar komi
df.puntos.map(lambda x: float(x) if isinstance(x, str) else  None )


df = df[['id','black','white','outcome','handicap','komi','width','puntos','ranked','started','ended']]

#import datetime
df.sort_values(by=['ended','started','id'])
#df.ended.map(lambda x: datetime.datetime(x.split('-')[0]) )
#df[~(df.ended>= df.started)][['outcome','ended','started']]

##%%
with open('descriptionDataset.txt', 'w') as file:
     file.write(json.dumps(DatosText)) # use `json.loads` to do the reverse
## %%
with open('filtered.txt', 'w') as file:
     file.write(json.dumps(filtered)) # use `json.loads` to do the reverse

#df = df[['id','black','white','order','results','handicap','komi','width']]
df = df.reset_index()
df.to_csv("summary_filtered.csv", index=False)
#df.to_pickle("DataFramePurge.pickle")
## %% 

##%%

#summary = df.to_dict('records'')#%%
#with open('summary.pickle', 'wb') as handle:
#    pickle.dump(summary, handle, protocol=pickle.HIGHEST_PROTOCOL)

