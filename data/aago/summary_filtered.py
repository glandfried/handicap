# -*- coding: utf-8 -*-
import pandas as pd
import sys
import json
import numpy as np
sys.path.append('../software/')

csv_name = 'aago.csv'

df = pd.read_csv(csv_name)
sum(df.event_id>0) #qué hace esto?

filtered = {}
##%% Selecciono las columnas que quiero y las filas con ciertas restricciones
filtered['Result'] = sum(~ ((df.result=="black") | (df.result=="white")))
df = df[((df.result=="black") | (df.result=="white"))]
filtered['Reason'] = sum(~((df.reason== "resignation") | (df.reason== "points") | (df.reason== "timeout") | (df.reason== "unknown")))
df = df[((df.reason== "resignation") | (df.reason== "points") | (df.reason== "timeout") | (df.reason== "unknown"))]
filtered['Unrated'] = sum((df.unrated!=0))
df = df[df.unrated==0]

#para que quede compatible con los otros
df.rename(columns = {'date': 'started'}, inplace = True)
df['black_win'] = df['result'] == "black"
df.rename(columns = {'black_player_id': 'black'}, inplace = True)
df.rename(columns = {'white_player_id': 'white'}, inplace = True)
df['width'] = 19

df = df.reset_index()
df.to_csv("aago_filtered.csv", index=False)
df_light = df[['black','white','started','black_win','width','komi','handicap']]
df_light.to_csv("aago_light.csv", index=False)
