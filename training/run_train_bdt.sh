#!/bin/bash
echo "Setting Env"
source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh

era=$1
max_N=$2
jet_type=$3
in_dir=$4
d_name="BDT_${jet_type}_${era}"
eta_bin=$5

mkdir -p output
cd output

mkdir -p $d_name

chmod +x ../train_bdt.py
../train_bdt.py --era $era --max_N $max_N --jet_type $jet_type --in_dir $in_dir --d_name $d_name --eta_bins $eta_bin

cd ../
