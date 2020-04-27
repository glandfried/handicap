#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:52:44 2020

@author: mati
"""

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


def resultWohKomi(orders, outcomes, komis):
    try:
        resultado = orders[1]
        when_black_win_then_positive_else_negative = 2*resultado-1
        points = when_black_win_then_positive_else_negative*(outcomes + komis)
        if points > 0:
            result = list([1, 0])
        else:
            result = list([0, 1])
        return result
    except: 
        return orders

print("Dataframe metida")   
# %%    
df = pd.read_csv(csv_name)
df =df[['id','black','white','order','outcome','handicap','komi','width', 'annulled']]
df = df[df.annulled == False]
df = df[(df.outcome == 'Resignation') | (df.outcome == 'Timeout') | (df.outcome.str.contains(' point',na=False))]
replace_values = {' points': '', ' point': ''}
df.outcome.replace(replace_values, regex=True,inplace=True)
print("Purgacion 1 completa")
df.outcome = df.outcome.apply(lambda x: StrToFloat(x))
df.komi = df.komi.apply(lambda x: StrToFloat(x))
df.order = df.order.apply(lambda x : stringToList(x))

Type_new = df.apply(lambda x: resultWohKomi(x.order,x.outcome,x.komi), axis=1)
df.insert(2, "results",Type_new)
print("Purgacion 2 completa") 
# %%
           
df = df[['id','black','white','order','results','handicap','komi','width']]

df = df.reindex(columns = df.columns.tolist() + ['white_prior','black_prior','white_prior_woh','black_prior_woh','white_posterior'])

df.to_csv("DataFramePurge.csv", index=False)
print("Purgacion 3 completa")