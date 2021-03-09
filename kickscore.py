       
import kickscore as ks
from datetime import datetime
import time

observations = list()
clock = time.time() 

teams = [['1','2'],['1','3'],['2','3']]
results = [[0,1],[1,0],[0,1]]


for i in range(len(teams)):
    if int(results[i][0]) < int(results[i][1]):
        observations.append({ "winners": [teams[i][0]], "losers": [teams[i][1]], "t": clock +i})
    else:
        observations.append({ "winners": [teams[i][1]], "losers": [teams[i][0]], "t": clock +i})

seconds_in_year = 365.25 * 24 * 60 * 60

model = ks.BinaryModel()
kernel = (ks.kernel.Constant(var=0.03) + ks.kernel.Matern32(var=0.138, lscale=1.753*seconds_in_year))

for team in range(1,4):
    model.add_item(str(team), kernel=kernel)

for obs in observations:
    model.observe(**obs)

start_time = time.time()
converged = model.fit()
if converged:
    print("Model has converged.")
elapsed_time = time.time() - start_time
# 30 segundos, 3 partidas

model.item['1'].scores[1]
model.item['2'].scores[1]
model.item['3'].scores[1]

model.plot_scores(['1'], figsize=(14, 5));
model.plot_scores(['2'], figsize=(14, 5));
model.log_likelihood
import numpy as np
np.exp(model.log_likelihood/3)
