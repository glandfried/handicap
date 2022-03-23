# Optimizar el parámetro que distribuye pesos a los distintos handicaps

from handicap.validation.aga.scripts.estimaciones import get_evidence
from scipy.optimize import minimize

initial_parameters = [0.04264, 1.05801, 1, 1, 0]
result = minimize(get_evidence,initial_parameters,method='Nelder-Mead',tol=250, options={'disp' : True})
print(result)
