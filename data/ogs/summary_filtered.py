# -*- coding: utf-8 -*-
import pandas as pd
import sys
import json
import numpy as np
sys.path.append('../software/')

csv_name = 'summary.csv'

print("Dataframe metida")
df = pd.read_csv(csv_name)
df = df[['id','black','white','order','outcome','handicap','komi','width','height', 'annulled','ranked','started','ended']]

filtro = (df.annulled != False) | (~((df.outcome == 'Resignation') | (df.outcome == 'Timeout') | (df.outcome.str.contains(' point')))) | (df.height!=df.width) | (~((df["width"] >= 9) & (df["width"] <=19 ))) | (~((df.order != "(0, 0)")&(df.order != "(1, 1)"))) | (df.white == df.black)
fd = df[filtro]

filtered = {}
##%% Selecciono las columnas que quiero y las filas con ciertas restricciones
filtered['Annulled'] = sum(df.annulled != False)
df = df[df.annulled == False]
filtered['Outcomes'] = sum(~((df.outcome == 'Resignation') | (df.outcome == 'Timeout') | (df.outcome.str.contains(' point'))))
df = df[(df.outcome == 'Resignation') | (df.outcome == 'Timeout') | (df.outcome.str.contains(' point'))]
filtered['Squared'] = sum(df.height!=df.width)
df = df[df.height==df.width]
filtered['Width'] = sum(~((df["width"] >= 9) & (df["width"] <=19 )))
df = df[(df["width"] >= 9) & (df["width"] <=19 )]
filtered['Order'] = sum(~((df.order != "(0, 0)")&(df.order != "(1, 1)")))
df = df[(df.order != "(0, 0)")&(df.order != "(1, 1)")]#np.sum(df.order == "(0, 0)")
filtered['Itself'] = sum(df.white == df.black)
df = df[df.white != df.black]

# Hago una columna con los puntos de las partidas ganadas como tal
replace_values = {' points': '', ' point': '','Resignation': None,'Timeout': None}
# Hago Float los puntos
df['points'] = df.outcome.replace(replace_values, regex=True)
df.points = df.points.map(lambda x: float(x) if isinstance(x, str) else  None )
df.outcome[df.outcome.str.contains(' point',na=False)] = "Points"
# Hago el order con formato lista para poder luego usar como argumento de las funciones de skill
df["black_win"] = df.order.map(lambda x :  1 if x[1]=='1' else 0)

df['started'] = df.started.map(lambda x : x[:10])

df = df[['id','black','white','outcome','black_win','black_win_not_komi','handicap','komi', 'width','points','ranked','started','ended']]
# Ordeno
df.sort_values(by=['ended','started','id'])

# Escribo los
with open('filtered.json', 'w') as file:
     file.write(json.dumps(filtered)) # use `json.loads` to do the reverse

fd.to_csv("filtered_data.csv", index=False)

df = df.reset_index()
df.to_csv("summary_filtered.csv", index=False)
df_light = df[['black','white','started','black_win','width','komi','handicap']]
df_light.to_csv("ogs_light.csv", index=False)
