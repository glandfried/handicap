#filtro basado en el que usan en AAGo:
# https://github.com/elsantodel90/RAAGo/blob/master/aago_ranking/games/models.py
# particularmente la función _rated_query
import pandas as pd

aago_name = 'aago.csv'
events_filename = 'events.csv'

df = pd.read_csv(aago_name)
print('original')
print(len(df))

#quizás no sea la forma más eficiente
#para trabajar con aago no importa, para ogs quizás sí?
df = df[df['handicap'] >= 0]
print('han may')
print(len(df))

df = df[df['handicap'] <= 9]
print('han men')
print(len(df))

df = df[(df['result'] == 'black') | (df['result'] == 'white')]
print('res')
print(len(df))

df = df[df['reason'] != 'walkover']
print('reason')
print(len(df))

df = df[df['unrated'] == False]
print('unrated')
print(len(df))

#print(df['komi'].apply(lambda x : str(x).endswith('.5')))
df = df[df['komi'].apply(lambda x : str(x).endswith('.5'))]
print('komi ends')
print(len(df))

df = df[( (df['handicap']<2) & ( (df['komi']<=20) & (df['komi']>= -20) ) ) | ( (df['komi']<=10) & (df['komi']>= -10) )]
print('komi range')
print(len(df))

#para que quede compatible con los otros
df.rename(columns = {'date': 'started'}, inplace = True)
df['black_win'] = df['result'] == "black"
df.rename(columns = {'black_player_id': 'black'}, inplace = True)
df.rename(columns = {'white_player_id': 'white'}, inplace = True)
df['width'] = 19

df = df[['black','white','started','black_win','width','komi','handicap','event_id']]
#df = df.sort_values(by='event_id') lo ordené por end_date - event_id al principio

#cargo events_filename
events = pd.read_csv(events_filename)
#joineo
defe = df.merge(events, on='event_id', how='left')
#ordeno
df = defe.sort_values(by=['end_date', 'start_date', 'event_id'])


df.to_csv("aago_original_filtered.csv", index=False)

#komi_check = Q(handicap__lt=2, komi__range=(-20, 20))
#komi_check |= Q(komi__range=(-10, 10))
