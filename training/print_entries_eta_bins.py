#!/usr/bin/env python3

import ROOT

tFile = ROOT.TFile.Open("input/training_trees_pt10To100_chs_94X.root")

trees_name = [tFile.GetListOfKeys()[i].GetName() for i in range(len(tFile.GetListOfKeys()))]

tags = ["Prompt", "Pileup"]

eta_bins = list(set([i.split("_")[0] for i in trees_name]))

e_bins = [i.split("_")[0].replace("Eta", "").replace("To", " < $|\\eta|$ < ").replace("p", ".") for i in eta_bins]

print("$\\eta$ bin", end="\t & ")
for tag in tags:
    print(tag, end="\t & ")
print(" ", end="\\\\ \n")
for e_bin, eta_bin in zip(e_bins, eta_bins):
    
    print(e_bin, end="\t & ")
    
    for tag in tags:
        
        nevents = tFile.Get(eta_bin + "_" + tag).GetEntries()
        print(nevents, end="\t & ")
    print(" ", end="\\\\ \n")
    
