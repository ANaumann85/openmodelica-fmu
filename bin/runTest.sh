#!/usr/bin/env bash

probFolder="$1"

if test -f "${probFolder}/simulate.mos"; then
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
else
  cd $probFolder
  omc buildFMU.mos
  for d in $(ls simulate*.mos) ; do 
    omc $d
  done
  cd ..
  for d in $(ls ${probFolder}/simulate*.mos) ; do 
    k=$(basename $d | sed 's:simulate\(.\)\.mos:\1:')  
    resFile="SimModel${k}_res.mat"
    refFunc="getReference${k}"
    bin/compareModelica.py ${probFolder} --resFile ${resFile} --refFunc ${refFunc}
    if test $? -ne 0 ; then
      echo "comparison with modelica simulation ${k} went wrong"
      exit 1
    fi
    bin/compareFMU.py ${probFolder} --refFunc ${refFunc}
    if test $? -ne 0 ; then
      echo "comparison with FMU simulation ${k} went wrong"
      exit 1
    fi
  done
fi
