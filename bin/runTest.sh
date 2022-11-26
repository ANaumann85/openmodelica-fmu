#!/usr/bin/env bash

probFolder="$1"
cd $probFolder
omc buildFMU.mos
omc simulate.mos
cd ..
bin/compareFMU.py ${probFolder}
bin/compareModelica.py ${probFolder}
