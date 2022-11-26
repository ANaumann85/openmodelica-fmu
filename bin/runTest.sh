#!/usr/bin/env bash

probFolder="$1"
cd $probFolder
omc buildFMU.mos
omc simulate.mos
cd ..
bin/compareModelica.py ${probFolder}
if test $? -ne 0 ; then
  echo "comparison with modelica simulation went wrong"
  exit 1
fi
bin/compareFMU.py ${probFolder}
if test $? -ne 0 ; then
  echo "comparison with FMU simulation went wrong"
  exit 1
fi
