#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:52:44 2020

@author: mati
"""
import os
import pickle
import pandas as pd
import sys
import json
sys.path.append('../software/')

#csv_name = './summary/summaryJson.csv'
csv_name = '/home/mati/Storage/Doctorado/Licar/licar/papers/2020_Handicap/nucleo/data/summaryJson.csv'


def StrToFloat(x):
    try:
        return float(x)
    except:
        return x

ValoresOrderIncorrectos = 0
def stringToList(x):
    global lista
    if x == '(1, 0)':
        x = list([1, 0])
    elif x == '(0, 1)':
        x = list([0, 1])      
    else:
        ValoresOrderIncorrectos = ValoresOrderIncorrectos + 1
    return x


PartidasCambiadasKomi = 0
def resultWoKomi(orders, puntos, komis):
    global PartidasCambiadasKomi
    if puntos != None:
        resultado = orders[0]
        when_black_win_then_positive_else_negative = 2*resultado-1
        points = when_black_win_then_positive_else_negative*puntos + komis
        if points > 0:
            result = list([1, 0])
            if resultado < 1:
                PartidasCambiadasKomi = PartidasCambiadasKomi + 1
        else:
            result = list([0, 1])
        return result


print("Dataframe metida")   
 # %%
df = pd.read_csv(csv_name)
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
DatosText['PartidasPuntos'] = int(df.outcome[df.outcome.str.contains(' point',na=False)].count())
DatosText['PartidasResignacion'] = int(df.outcome[df["outcome"] == 'Resignation'].count())
DatosText['PartidasSinTiempo'] = int(df.outcome[df["outcome"] == 'Timeout'].count())
DatosText['Partidas9x9'] = int(df.width[df["width"] == 9].count())
DatosText['Partidas13x13'] = int(df.width[df["width"] == 13].count())
DatosText['Partidas19x19'] = int(df.width[df["width"] == 19].count())


#%% Selecciono las columnas que quiero y las filas con ciertas restricciones
df = df[['id','black','white','order','outcome','handicap','komi','width', 'annulled','started']]
df = df[df.annulled == False]
df = df[(df.outcome == 'Resignation') | (df.outcome == 'Timeout') | (df.outcome.str.contains(' point',na=False))]
df = df[(df["width"] >= 9) & (df["width"] <=19 )]
df = df[df.order.str.contains("(1, 0)|(0, 1)",na=False)]
#%% Hago una columna con los puntos de las partidas ganadas como tal
replace_values = {' points': '', ' point': '','Resignation': None,'Timeout': None}
df['puntos'] = df.outcome.replace(replace_values, regex=True,inplace=False)
#Hago Float tanto los puntos como el komi
df.puntos = df.puntos.map(lambda x: StrToFloat(x))
df.komi = df.komi.map(lambda x: StrToFloat(x))
#%% Hago el order con formato lista para poder luego usar como argumento de las funciones de skill
df.order = df.order.map(lambda x : stringToList(x))
# %% Genero una lista results, la cual es order pero sin consdierar komi
df['results'] = df.apply(lambda x: resultWoKomi(x.order,x.puntos,x.komi), axis=1)
#Guardo la info de cuantas partidas se ganaron por el komi
for index in df.index:
    resultWohKomi(df.at[index, "order"],df.at[index, "outcome"],df.at[index, "komi"])
DatosText['PartidasGanadasPorKomi'] = int(PartidasCambiadasKomi)
#%%
with open('DatosText.txt', 'w') as file:
     file.write(json.dumps(DatosText)) 
# %%

df = df[['id','black','white','order','results','handicap','komi','width']]
df = df.reset_index()
df.to_csv("DataFramePurge.csv", index=False)
df.to_pickle("DataFramePurge.pickle")
# %% 

#%%
#summary = df.to_dict('records'')#%%
#with open('summary.pickle', 'wb') as handle:
#    pickle.dump(summary, handle, protocol=pickle.HIGHEST_PROTOCOL)
int(df.width[df["komi"] <6].count())
