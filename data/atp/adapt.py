import pandas as pd
from datetime import datetime

# Entrada: history.csv con columnas:
# match_id,double,round_number,w1_id,w1_name,w2_id,w2_name,l1_id,l1_name,l2_id,l2_name,
# time_start,time_end,ground,tour_id,tour_name
# Salida: DataFrame de partidas single con columnas 'black', 'white', 'handicap', 'winner', 'day'
INPUT_FILE = './history.csv'
OUTPUT_FILE = './history.adapted.csv'


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


df = pd.read_csv(INPUT_FILE, usecols=['w1_id', 'l1_id', 'double', 'time_start'])
df = df.loc[df['double'] == 'f']

df['handicap'] = [0] * len(df)
df['winner'] = ['B'] * len(df)
first_day = df['time_start'].min()
df['day'] = [days_between(first_day, day) for day in df['time_start']]

columns = ['black', 'white', 'handicap', 'winner', 'day']
(df.rename(columns={
    'w1_id': 'black',
    'l1_id': 'white',
}).sort_values('day').to_csv(OUTPUT_FILE, columns=columns, index=False))
