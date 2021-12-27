import pandas as pd
from datetime import date

df = pd.read_csv('./aago.csv')

if not (df['komi'].isin([0.5, 6.5])).all():
    raise Exception('Existe un komi con valor distinto a 0.5 y 6.5, revisar.')

filters = (df['handicap'] >= 0) & (df['handicap'] <= 9) &\
          (df['result'].isin(['black', 'white'])) &\
          (df['reason'] != 'walkover') &\
          (df['unrated'] == 0)

df = df[filters]

df['winner'] = df['result'].apply(lambda result: 'B' if result == 'black' else 'W')
df['black'] = df['black_player_id']
df['white'] = df['white_player_id']

df['date'] = df['date'].apply(date.fromisoformat)
first_day = df['date'].min()
df['day'] = df['date'].apply(lambda d: (d - first_day).days + 1)

columns = ['id', 'black', 'white', 'handicap', 'komi', 'winner', 'day']
df.sort_values('day').to_csv('./aago.adapted.csv', columns=columns, index=False)
