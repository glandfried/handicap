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
sys.path.append('../software/')

#csv_name = './summary/summaryJson.csv'
csv_name = '/home/mati/Storage/Doctorado/Licar/licar/papers/2020_Handicap/nucleo/data/summaryJson.csv'


def StrToFloat(x):
    try:
        return float(x)
    except:
        return str(x)


def stringToList(x):
    if x == '(1, 0)':
        x = list([1, 0])
    elif x == '(0, 1)':
        x = list([0, 1])      
    else:
        pass
    return x

PartidasCambiadasKomi = 0
def resultWohKomi(orders, outcomes, komis):
    global PartidasCambiadasKomi
    try:
        resultado = orders[0]
        when_black_win_then_positive_else_negative = 2*resultado-1
        points = when_black_win_then_positive_else_negative*outcomes + komis
        if points > 0:
            result = list([1, 0])
            if resultado < 1:
                PartidasCambiadasKomi = PartidasCambiadasKomi + 1
        else:
            result = list([0, 1])
        return result
    except:
        return orders

print("Dataframe metida")   
 # %%
df = pd.read_csv(csv_name)
# %%
for index in df.index:
    resultWohKomi(df.at[index, "order"],df.at[index, "outcome"],df.at[index, "komi"])
print(PartidasCambiadasKomi)
#%%
handicap1 = df.handicap[df["handicap"]==1].count()
handicapMayor1 = df.handicap[df["handicap"]>1].count()
handicapMayor9x9 = df.handicap[(df["handicap"]>1)&(df["width"]== 9)].count()
handicapMayor13x13 = df.handicap[(df["handicap"]>1)&(df["width"]== 13)].count()
handicapMayor19x19 = df.handicap[(df["handicap"]>1)&(df["width"]== 19)].count()

df["width"].loc[df["width"]< 9]
handicap0 = df.handicap[df["handicap"]==0].count()
handicapNegativa = df.handicap[df["handicap"]<0].count()
PartidasAnuladas = df.annulled[df["annulled"]==True].count()
PartidasPuntos = df.outcome[df.outcome.str.contains(' point',na=False)].count()
PartidasResignacion = df.outcome[df["outcome"]== 'Resignation'].count()
PartidasSinTiempo = df.outcome[df["outcome"]== 'Timeout'].count()
Partidas9x9 = df.width[df["width"]== 9].count()
Partidas13x13 = df.width[df["width"]== 13].count()
Partidas19x19 = df.width[df["width"]== 19].count()
# %%
df =df[['id','black','white','order','outcome','handicap','komi','width', 'annulled','started']]

df = df[df.annulled == False]

df = df[(df.outcome == 'Resignation') | (df.outcome == 'Timeout') | (df.outcome.str.contains(' point',na=False))]
df = df[(df["width"]>=9)&(df["width"]<=19)]
replace_values = {' points': '', ' point': ''}
df.outcome.replace(replace_values, regex=True,inplace=True)
print("Purgacion 1 completa")

df.outcome = df.outcome.map(lambda x: StrToFloat(x))

df.komi = df.komi.map(lambda x: StrToFloat(x))

df.order = df.order.map(lambda x : stringToList(x))
# %%
df['results'] = df.apply(lambda x: resultWohKomi(x.order,x.outcome,x.komi), axis=1)

print("Purgacion 2 completa") 
# %%

df = df[['id','black','white','order','results','handicap','komi','width']]
df = df.reset_index()
# %% 
df.to_csv("DataFramePurge.csv", index=False)
df.to_pickle("DataFramePurge.pickle")
print("Purgacion 3 completa")

#%%
#summary = df.to_dict('records'')#%%
#with open('summary.pickle', 'wb') as handle:
#    pickle.dump(summary, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
