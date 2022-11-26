#!/usr/bin/env python3

import sys
import argparse
import importlib.util
import numpy as np
import scipy.io as sio

def getValue(varNr):
  datArray = resData['dataInfo'][0][varNr]
  if datArray == 0:
    datArray = 2 # time is in the second data
  datArray = f'data_{datArray}'
  datIndex = resData['dataInfo'][1][varNr]-1
  return resData[datArray][datIndex]

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='plot a selection of modelica results')
  parser.add_argument('problemDir', help='the problem folder')
  parser.add_argument('--resFile', help='name of the result file', default='SimModel_res.mat')
  parser.add_argument('--solName', help='name of the solution variable', default='testModel.T')
  parser.add_argument('--refFunc', default='getReference', help='name of the reference solution')

  args = parser.parse_args()
  resFile = f'{args.problemDir}/{args.resFile}'
  resData = sio.loadmat(resFile, matlab_compatible=True)
  names = resData['name']
  names = [''.join(names[:,k]) for k in range(names.shape[1])]
  solIndex = names.index(args.solName)
  timeIndex = 0
  times = getValue(timeIndex)
  fmuSol = getValue(solIndex)
  spec = importlib.util.spec_from_file_location('reference', f'{args.problemDir}/reference.py')
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  refFunc = getattr(module, args.refFunc)
  rhs, sol, Tref1 = refFunc(5.0)
  refSol = sol(times)
  maxDiff = np.max(np.abs(refSol-fmuSol))
  print(f'maxDiff modelica: {maxDiff}')
  if maxDiff > 1.0e-9:
    sys.exit(1)

# vim:set et sw=2 ts=2:
