# -*- coding: utf-8 -*-
import pandas as pd
import sys
import json
import csv
import numpy as np
sys.path.append('../software/')

csv_name = 'summary_filtered.csv'

df = pd.read_csv(csv_name)

data = {}
data['games']= df.shape[0]
data['games_9x9'] = sum(df.width == 9)
data['games_13x13'] = sum(df.width == 13)
data['games_19x19'] = sum(df.width == 19)
data['handicap'] = sum(df.handicap > 1)
data['handicap_9x9'] = sum((df.handicap > 1)&(df.width == 9))
data['handicap_13x13'] = sum((df.handicap > 1)&(df.width == 13))
data['handicap_19x19'] = sum((df.handicap > 1)&(df.width == 19))
data['handicap_0'] = sum(df.handicap == 0)
data['handicap_1'] = sum(df.handicap == 1)
data['handicap_-1'] = sum(df.handicap == -1)
data['handicap_negative'] = sum(df.handicap < -1)
data['outcome_points'] = sum(df.outcome == "Points")
data['outcome_resignation'] = sum(df.outcome == 'Resignation')
data['outcome_timeout'] = sum(df.outcome == 'Timeout')
data['komi_negativo'] = sum(df.komi<0)

data['games_ranked']= sum(df.ranked)
data['games_9x9_ranked'] = sum(df.ranked & (df.width == 9))
data['games_13x13_ranked'] = sum(df.ranked & (df.width == 13))
data['games_19x19_ranked'] = sum(df.ranked & (df.width == 19))
data['handicap_ranked'] = sum(df.ranked & (df.handicap > 1))
data['handicap_9x9_ranked'] = sum(df.ranked & ((df.handicap > 1)&(df.width == 9)))
data['handicap_13x13_ranked'] = sum(df.ranked & ((df.handicap > 1)&(df.width == 13)))
data['handicap_19x19_ranked'] = sum(df.ranked & ((df.handicap > 1)&(df.width == 19)))
data['handicap_0_ranked'] = sum(df.ranked & (df.handicap == 0))
data['handicap_1_ranked'] = sum(df.ranked & (df.handicap == 1))
data['handicap_-1_ranked'] = sum(df.ranked & (df.handicap == -1))
data['handicap_negative_ranked'] = sum(df.ranked & (df.handicap < -1))
data['outcome_points_ranked'] = sum(df.ranked & (df.outcome == "Points"))
data['outcome_resignation_ranked'] = sum(df.ranked & (df.outcome == 'Resignation'))
data['outcome_timeout_ranked'] = sum(df.ranked & (df.outcome == 'Timeout'))
data['komi_negativo_ranked'] = sum(df.ranked & (df.komi<0))

data['proportion_outcome_resignation_ranked'] = data['outcome_resignation_ranked'] / data['outcome_resignation']
data['proportion_outcome_points_ranked'] = data['outcome_points_ranked'] / data['outcome_points']
data['proportion_outcome_timeout_ranked'] =  data['outcome_timeout_ranked'] / data['outcome_timeout']




with open('dataDescritor.json', 'w') as file:
     file.write(json.dumps(data)) # use `json.loads` to do the reverse
