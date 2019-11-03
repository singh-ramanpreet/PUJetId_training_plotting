#!/bin/bash

source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh

era="102X"
#data_type="mc"
data_type="data"
year="2018"
#period="full"
period="D"
lumi=59.96
N_mc=100194597
xs=5321.0
#input_filename="/eos/user/s/singhr/jme_ntuples/dy_inc_${year}/cut_pt20/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/mc_flatTree_1.root"
#input_filename="/eos/user/s/singhr/jme_ntuples/dy_inc_${year}/cut_pt10/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/mc_flatTree_1.root"
input_filename="/eos/user/s/singhr/jme_ntuples/Data_${year}/DoubleMuon_${period}/data_flatTree_1.root"
output_filename="output_hists_${data_type}_${year}${period}.root"

./analyze_make_hists.py \
--era=$era \
--data_type=$data_type \
--year=$year \
--period=$period \
--lumi=$lumi \
--N_mc=$N_mc \
--input_filename $input_filename \
--output_filename $output_filename
