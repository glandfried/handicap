import ast
import pandas as pd
import dateutil
from os import listdir
files = ["kdd-basketball.txt","kdd-chess-small.txt","kdd-football.txt","kdd-tennis.txt"]
for s in files:
    list_of_dict = []
    with open('./data/{}'.format(s)) as f:
        for line in f:
            line = line.replace(', "bonus": null,', ', "bonus": None,')
            line = line.replace(': false,', ': False,')
            line = line.replace(': true,', ': True,')
            list_of_dict.append(ast.literal_eval(line))

    df = pd.DataFrame(list_of_dict)
    n = s.split(".")[0]
    df.to_csv("{}.csv".format(n))

