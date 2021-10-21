import pandas as pd
from datetime import date

df = pd.read_csv('./aago.csv')

df['winner'] = df['result'].apply(lambda result: 'B' if result == 'black' else 'W')
df['black'] = df['black_player_id']
df['white'] = df['white_player_id']

df['date'] = df['date'].apply(date.fromisoformat)
first_day = df['date'].min()
df['day'] = df['date'].apply(lambda d: (d - first_day).days + 1)

columns = ['black', 'white', 'handicap', 'komi', 'winner', 'day']
df.sort_values('day').to_csv('./aago.adapted.csv', columns=columns, index=False)
