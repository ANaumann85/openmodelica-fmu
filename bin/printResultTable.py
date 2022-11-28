#!/usr/bin/env python3

import sys
import argparse
import tabulate

if __name__ == '__main__':
  parser = argparse.ArgumentParser('table builder')
  parser.add_argument('--rowNames', nargs='+', help='names of the rows')
  parser.add_argument('--colNames', nargs='+', help='column headers')
  parser.add_argument('--data', type=int, nargs='+', help='cell values in row wise order')

  args = parser.parse_args()

  if len(args.data) != len(args.rowNames)*len(args.colNames):
    raise RuntimeError(f'number of row names {len(args.rowNames)} times number of columns {len(args.colNames)} does not match the data {len(args.data)}')
  tab = []
  nrToCol = { 0:'green', 1:'red' }
  nrToBox = { k : f'![](https://placehold.co/200x20/{val}/{val}/png)' for k,val in  nrToCol.items()}
  for rowNr, rowName in enumerate(args.rowNames):
    row = [rowName] + [nrToBox[args.data[rowNr*len(args.colNames)+k]] for k in range(len(args.colNames))]
    tab.append(row)
  print(tabulate.tabulate(tab, headers=['problem'] + args.colNames, tablefmt='github'))
# vim:set et sw=2 ts=2:
