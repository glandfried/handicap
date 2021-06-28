import pandas as pd
import json

csv_name = './KGS.csv'

print("Dataframe metida")
df = pd.read_csv(csv_name)
df = df[['id', 'black', 'white', 'order', 'outcome', 'handicap', 'komi',
        'width', 'started', 'whiteRank', 'blackRank']]

print("Total: ", df.shape)
df = df[(df["width"] >= 9) & (df["width"] <= 19)]
print("Tamaño estandar: ", df.shape)
df = df[(df.order == 1) | (df.order == 0)]
print("Resultado estandar: ", df.shape)

df['black_win'] = df.order
def outcomeOutput(x):
    if 'Resign' in x:
        x = 'Resign'
    elif 'Time' in x:
        x = 'Time'
    else:
        x=x

#pongo cero en los handicap nulos
df['handicap'] = df['handicap'].map(lambda x : x if x >= 2 else 0)
#df.outcome = df.outcome.apply(lambda x: outcomeOutput(x))
df = df[['id', 'black', 'white', 'outcome', 'black_win', 'handicap', 'komi',
        'width', 'started', 'whiteRank', 'blackRank']]
# Ordeno
df = df.sort_values(by=['started', 'id'])

df = df.reset_index()
df.to_csv("./KGS_filtered.csv", index=False)
df_light = df[['black','white','started','black_win','width','komi','handicap']]
df_light.to_csv("kgs_light.csv", index=False)
