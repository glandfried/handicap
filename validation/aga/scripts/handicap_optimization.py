# Optimizar el parámetro que distribuye pesos a los distintos handicaps

from handicap.validation.aga.scripts.estimaciones import get_evidence
from scipy.optimize import minimize

initial_parameters = [0.035]
result = minimize(get_evidence,initial_parameters,method='Nelder-Mead',tol=0.01, options={'disp' : True})
print(result)
