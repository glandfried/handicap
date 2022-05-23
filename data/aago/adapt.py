import pandas as pd
from datetime import date

df = pd.read_csv('./aago_original_filtered.csv')

df['id'] = range(len(df))
df['winner'] = df['black_win'].apply(lambda black_win: 'B' if black_win else 'W')

df['date'] = df['end_date'].apply(date.fromisoformat)
first_day = df['date'].min()
df['day'] = df['date'].apply(lambda d: (d - first_day).days + 1)

columns = ['id', 'black', 'white', 'handicap', 'komi', 'winner', 'day', 'event_id']
df.sort_values('day').to_csv('./aago_original_filtered.adapted.csv', columns=columns, index=False)
