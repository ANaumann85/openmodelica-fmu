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
  modRes=$?
  if test ${modRes} -ne 0 ; then
    echo "comparison with modelica simulation went wrong"
  #  exit 1
  fi
  bin/compareFMU.py ${probFolder} fmuRes.txt
  fmuRes=$?
  if test ${fmuRes} -ne 0 ; then
    echo "comparison with FMU simulation went wrong"
    # there was an error, so both went wrong
    echo "1" > fmuRes.txt
    echo "1" >> fmuRes.txt
    # exit 1
  fi
else
  cd $probFolder
  omc --showErrorMessages $OMCFlags buildFMU.mos
  omc --showErrorMessages $OMCFlags simulate${probNr}.mos
  cd ..
  resFile="SimModel${probNr}_res.mat"
  refFunc="getReference${probNr}"
  bin/compareModelica.py ${probFolder} --resFile ${resFile} --refFunc ${refFunc}
  modRes=$?
  if test ${modRes} -ne 0 ; then
    echo "comparison with modelica simulation ${probNr} went wrong"
    exit 1
  fi
  bin/compareFMU.py ${probFolder} fmuRes.txt --refFunc ${refFunc}
  fmuRes=$?
  if test ${fmuRes} -ne 0 ; then
    echo "comparison with FMU simulation ${probNr} went wrong"
    # there was an error, so both went wrong
    echo "1" > fmuRes.txt
    echo "1" >> fmuRes.txt
    # exit 1
  fi
fi
fmuT=`head -n 1 fmuRes.txt`
fmuQ=`tail -n 1 fmuRes.txt`
echo -e "modelica=${modRes}\nfmuT=${fmuT}\nfmuQ=${fmuQ}" > result.txt
cat result.txt
