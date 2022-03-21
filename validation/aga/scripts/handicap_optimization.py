# Optimizar el parámetro que distribuye pesos a los distintos handicaps

from handicap.validation.aga.scripts.estimaciones import get_evidence
from scipy.optimize import minimize_scalar

result = minimize_scalar(get_evidence,options={'maxiter': 4,'disp': 3})
print(result)
