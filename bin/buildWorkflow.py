#!/usr/bin/env python3

import yaml

def getJob(fname, name, probNr, omcFlags):
  testStep = { 'name' : 'run-in-the-image', 'id' : f'run-{fname}', 'uses' : './' }
  w = { 'testFolder' : fname }
  if probNr is not None:
    w['probNr'] = probNr
  if omcFlags is not None:
    w['omcFlags'] = omcFlags
  testStep['with'] = w
  steps = [ { 'name' : 'Checkout', 'uses' : 'actions/checkout@v3' } , testStep ]
  ret = { 'runs-on': 'ubuntu-latest', 'name' : name, 'steps' : steps }
  return ret

if __name__ == '__main__':
  dest = '.github/workflows/main.yml'
  tests = [('source_withQ', None), ('source_withoutQ', None)]
  tests += [('initial_T_withQ', k+1) for  k in range(4)]
  tests += [('initial_T_withoutQ', k+1) for  k in range(4)]
  indexReductionMethods = ['none', 'uode', 'dynamicStateSelection', 'dummyDerivatives']
  jobs = {}
  for t in tests:
    for indRed in indexReductionMethods:
      jKey = '-'.join([str(x) for x in filter(None, (t[0], t[1]))] + [indRed])
      omcFlags = f'--indexReductionMethod={indRed}'
      jobs[jKey] = getJob(t[0], jKey, t[1], omcFlags)
  workflow = { 'on' : ['push'], 'jobs' : jobs }
  yaml.dump(workflow, open(dest, 'w'), indent=2)
# vim:set et sw=2 ts=2:
