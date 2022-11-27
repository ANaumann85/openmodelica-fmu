#!/usr/bin/env bash

probFolder="$1"
probNr="$2"
OMCFlags="$3"

if test -z "$probNr" ; then
  cd $probFolder
  omc --showErrorMessages $OMCFlags buildFMU.mos
  omc --showErrorMessages $OMCFlags simulate.mos
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
else
  cd $probFolder
  omc buildFMU.mos
  omc simulate${probNr}.mos
  cd ..
  resFile="SimModel${probNr}_res.mat"
  refFunc="getReference${probNr}"
  bin/compareModelica.py ${probFolder} --resFile ${resFile} --refFunc ${refFunc}
  if test $? -ne 0 ; then
    echo "comparison with modelica simulation ${probNr} went wrong"
    exit 1
  fi
  bin/compareFMU.py ${probFolder} --refFunc ${refFunc}
  if test $? -ne 0 ; then
    echo "comparison with FMU simulation ${probNr} went wrong"
    exit 1
  fi
fi
