import numpy as np

def getReference(x0):
  l = 10.0
  sCoeffs = [0.0, 20]
  yRef = np.polynomial.Polynomial(sCoeffs)
  f = lambda t, y: l*yRef(t)
  sol = (l*yRef).integ(k=[x0])
  qSol = l*(yRef-sol)
  return (f, sol, qSol, yRef)
