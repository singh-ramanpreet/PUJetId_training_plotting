#!/bin/bash
echo "Starting"
source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh
chmod +x make_training_trees.py
./make_training_trees.py --era $1 --inputFiles ${@:2}
