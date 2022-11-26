#!/usr/bin/env python3

import sys
from argparse import ArgumentParser
import importlib.util
import numpy as np
from scipy import integrate
import fmpy
from tabulate import tabulate

def getFMUSol(nInter, Tref1, x0, fmuFile):
  outputs = ['time', 'pipe1Q', 'Tref1', 'T', 'der(T)']
  tEnd = 0.2
  inSigDtype = [('time', np.double), ('Tref1', np.double)]
  sigTime = np.linspace(0, tEnd, nInter)
  inSig = np.array([ (t, Tref1(t)) for t in sigTime], dtype=inSigDtype) # piecewise linear
  resFMU = fmpy.simulate_fmu(fmuFile,start_values={'T0' : x0 }, start_time=0.0, stop_time=tEnd, step_size=0.02, input=inSig, output=outputs, output_interval=tEnd/nInter)
  return resFMU

def compare(problem, fmuFile):
  x0 = 5.0
  _, sol, Tref1 = problem(x0)
  diff = []
  for k in range(10):
    nInter = 10*(2**k)
    fmuSol = getFMUSol(nInter, Tref1, x0, fmuFile)
    refSol = sol(fmuSol['time'])
    curDiff = float(np.max(np.abs(fmuSol['T']-refSol)))
    diff.append((nInter, curDiff))
  print(tabulate(diff, headers=['nInter', 'maxDiff']))
  return curDiff

if __name__ == '__main__':
  parser = ArgumentParser('compares the results from an FMU (in cs mode) with analytic solutions')
  parser.add_argument('problemDir', help='the problem folder')
  parser.add_argument('--fmuFile', default='testModel_cs.fmu', help='fmu file name in the folder')
  parser.add_argument('--refFunc', default='getReference', help='name of the reference solution')
  args = parser.parse_args()
  spec = importlib.util.spec_from_file_location('reference', f'{args.problemDir}/reference.py')
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  fmuFile = f'{args.problemDir}/{args.fmuFile}'
  refFunc = getattr(module, args.refFunc)
  maxDiff = compare(refFunc, fmuFile)
  if maxDiff > 1.0e-3:
    sys.exit(1)
# vim:set et sw=2 ts=2:
