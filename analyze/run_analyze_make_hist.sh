#!/bin/bash

source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh

era=$1
data_type=$2
year=$3
period=$4
lumi=$5
N_mc=$6
xs=$7
input_filename=$8
output_filename=$9

./analyze_make_hists.py \
--era=$era \
--data_type=$data_type \
--year=$year \
--period=$period \
--lumi=$lumi \
--N_mc=$N_mc \
--input_filename $input_filename \
--output_filename $output_filename

mkdir -p output
mv $output_filename output/$output_filename
