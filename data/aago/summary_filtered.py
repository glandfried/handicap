# -*- coding: utf-8 -*-
import pandas as pd
import sys
import json
import numpy as np
sys.path.append('../software/')

csv_name = 'aago.csv'

df = pd.read_csv(csv_name)
sum(df.event_id>0)

filtered = {}
##%% Selecciono las columnas que quiero y las filas con ciertas restricciones
filtered['Result'] = sum(~ ((df.result=="black") | (df.result=="white")))
df = df[((df.result=="black") | (df.result=="white"))]
filtered['Reason'] = sum(~((df.reason== "resignation") | (df.reason== "points") | (df.reason== "timeout") | (df.reason== "unknown")))
df = df[((df.reason== "resignation") | (df.reason== "points") | (df.reason== "timeout") | (df.reason== "unknown"))]
filtered['Unrated'] = sum((df.unrated!=0))
df = df[df.unrated==0]

df = df.reset_index()
df.to_csv("aago_filtered.csv", index=False)
