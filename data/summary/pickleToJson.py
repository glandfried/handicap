#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transforma los datos crudos en formato pickle a formato json
@author: mati
"""

import json
import os
import pickle
import numpy as np


files_dir = '../results/'
listdir_ = os.listdir(files_dir )
files_dir_json = '../resultsJson/'

count = 0
for f in range(len(listdir_)):

        
    file_path = os.path.join(files_dir, listdir_[f])
    player_games = pickle.load(open(file_path , "rb"))
    listdir_json = listdir_[f].replace('.pickle', '.json')
    file_path_json = os.path.join(files_dir_json, listdir_json)
    
    with open(file_path_json, 'w') as fout:
        json.dump(player_games , fout)
    
    print(f"Porcentaje {int(count/len(listdir_)*100)}%", end='\r')
    count = count + 1
