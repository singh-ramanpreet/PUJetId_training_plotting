#!/bin/bash
echo "Setting Env"
source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh

era="94X"
max_N=500000
jet_type="chs"
in_dir="/afs/cern.ch/work/s/singhr/jets_study/PUJetId_training_plotting/training/input/"
d_name="BDT_${jet_type}_${era}"

mkdir -p output
cd output

mkdir -p $d_name

chmod +x ../train_bdt.py
../train_bdt.py --era $era --max_N $max_N --jet_type $jet_type --in_dir $in_dir --d_name $d_name --eta_bins $1

cd ../
