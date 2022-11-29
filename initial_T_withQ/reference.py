import numpy as np

def getReference1(x0):
  l = 10.0
  f = lambda t, y: -l*y
  sol = lambda t: np.exp(-l*t)*x0
  yRef = lambda t: 0.0
  qRef = lambda t: -l*(yRef(t) - sol(t));
  return (f, sol, qRef, yRef)

def getReference2(x0):
  l = 10.0
  sCoeffs = [0, 10.0]
  yRef = np.polynomial.Polynomial(sCoeffs)
  f = lambda t, y: l*(yRef(t) - y)
  n = len(sCoeffs)-1 # degree
  solPCoeffs = [sCoeffs[-1]]
  solPCoeffs.append(sCoeffs[-2]-n*solPCoeffs[-1]/l)
  solPCoeffs = list(reversed(solPCoeffs))
  solP = np.polynomial.Polynomial(solPCoeffs)
  homCoeff = x0 - solP(0)
  sol = lambda t: np.exp(-l*t)*homCoeff + solP(t)
  qRef = lambda t: -l*(yRef(t) - sol(t));
  return (f, sol, qRef, yRef)

def getReference3(x0):
  l = 10.0
  sCoeffs = [20, 10.0]
  yRef = np.polynomial.Polynomial(sCoeffs)
  f = lambda t, y: l*(yRef(t) - y)
  n = len(sCoeffs)-1 # degree
  solPCoeffs = [sCoeffs[-1]]
  solPCoeffs.append(sCoeffs[-2]-n*solPCoeffs[-1]/l)
  solPCoeffs = list(reversed(solPCoeffs))
  solP = np.polynomial.Polynomial(solPCoeffs)
  homCoeff = x0 - solP(0)
  sol = lambda t: np.exp(-l*t)*homCoeff + solP(t)
  qRef = lambda t: -l*(yRef(t) - sol(t));
  return (f, sol, qRef, yRef)

def getReference4(x0):
  l = 10.0
  sCoeffs = [20]
  yRef = np.polynomial.Polynomial(sCoeffs)
  f = lambda t, y: l*(yRef(t) - y)
  solPCoeffs = [sCoeffs[-1]]
  solP = np.polynomial.Polynomial(solPCoeffs)
  homCoeff = x0 - solP(0)
  sol = lambda t: np.exp(-l*t)*homCoeff + solP(t)
  qRef = lambda t: -l*(yRef(t) - sol(t));
  return (f, sol, qRef, yRef)
