#!/usr/bin/env python3

import yaml

def getCheckout():
  return { 'name' : 'Checkout', 'uses' : 'actions/checkout@v3' }

def getJob(fname, name, probNr, omcFlags):
  testStep = { 'name' : 'run-test', 'id' : f'run-{fname}', 'uses' : './.github/actions/' }
  w = { 'testFolder' : fname }
  if probNr is not None:
    w['probNr'] = probNr
  if omcFlags is not None:
    w['omcFlags'] = omcFlags
  testStep['with'] = w
  exportStep = { 'name' : 'exportResults', 'id' : 'exportResults', 'run' : 'cat result.txt >> $GITHUB_OUTPUT\ncat result.txt\n'}
  steps = [ getCheckout() , testStep, exportStep ]
  outputs = { 'modelica' : '${{ steps.exportResults.outputs.modelica }}', 'fmuT' : '${{ steps.exportResults.outputs.fmuT }}', 'fmuQ' : '${{ steps.exportResults.outputs.fmuQ }}'}
  ret = { 'runs-on': 'ubuntu-latest', 'name' : name, 'outputs' : outputs, 'steps' : steps }
  return ret

def getTable(head, rowNames, colNames, data):
  headStep = {'run' : f'echo "# {head}" >> $GITHUB_STEP_SUMMARY'}
  tabStep = {'name' : head, 'run' : f'bin/printResultTable.py --rowNames {rowNames} --colNames {colNames} --data {data} >> $GITHUB_STEP_SUMMARY'}
  return [headStep, tabStep]

def getSummary(jobNames, rowNames, colNames):
  ret = {'name' : 'summary', 'runs-on' : 'ubuntu-latest' }
  ret['needs'] = jobNames
  fmuTData = ' '.join(f'${{{{ needs.{job}.outputs.fmuT }}}}' for job in jobNames)
  printFMUT = getTable('FMU-T(t)', rowNames, colNames, fmuTData)
  fmuQData = ' '.join(f'${{{{ needs.{job}.outputs.fmuQ }}}}' for job in jobNames)
  printFMUQ = getTable('FMU-q(t)', rowNames, colNames, fmuQData)
  modelicaData = ' '.join(f'${{{{ needs.{job}.outputs.modelica }}}}' for job in jobNames)
  printModelica = getTable('omc', rowNames, colNames, modelicaData)
  steps = [getCheckout(), {'run':'pip3 install tabulate'}] + printFMUT + printFMUQ + printModelica
  ret['steps'] = steps
  return ret

if __name__ == '__main__':
  dest = '.github/workflows/main.yml'
  tests = [('source_withQ', None), ('source_withoutQ', None)]
  tests += [('initial_T_withQ', k+1) for  k in range(4)]
  tests += [('initial_T_withoutQ', k+1) for  k in range(4)]
  indexReductionMethods = ['none', 'uode', 'dynamicStateSelection', 'dummyDerivatives']
  jobs = {}
  jobNr = 0
  jobNames = []
  for t in tests:
    for indRed in indexReductionMethods:
      jName = '-'.join([str(x) for x in filter(None, (t[0], t[1]))] + [indRed])
      jKey = f'job{jobNr}'
      omcFlags = f'--indexReductionMethod={indRed}'
      jobs[jKey] = getJob(t[0], jName, t[1], omcFlags)
      jobNr += 1
      jobNames.append(jKey)
  rowNames = ['-'.join([str(x) for x in filter(None, (t[0], t[1]))]) for t in tests]
  rowNames = ' '.join(rowNames)
  colNames = ' '.join(indexReductionMethods)
  jobs['summary'] = getSummary(jobNames, rowNames, colNames)
  workflow = { 'on' : ['push'], 'jobs' : jobs }
  yaml.dump(workflow, open(dest, 'w'), indent=2)
# vim:set et sw=2 ts=2:
