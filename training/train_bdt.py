#!/usr/bin/env python3

import ROOT
import os
import argparse

ROOT.gROOT.SetBatch(True)

if "HOME" not in os.environ:
    os.environ["HOME"] = "" # needed for condor batch mode

parser = argparse.ArgumentParser(
    description="train BDT PU JeT ID"
    )
parser.add_argument(
    "--era", type=str, default="94X", help="MC era, like 94X, 102X"
    )
parser.add_argument(
    "--max_N", type=int, default=200000, help="max N entries for testing and training"
    )
parser.add_argument(
    "--jet_type", type=str, default="chs", help="chs or puppi"
    )
parser.add_argument(
    "--in_dir", type=str, default="", help="directory of root file"
    )
parser.add_argument(
    "--d_name", type=str, default="BDT_chs_94X", help="dataloader name"
    )
parser.add_argument(
    "--eta_bins", type=str, nargs="+", default=[], help="eta bins names in input tree"
    )

args = parser.parse_args()

era = args.era
jet_type = args.jet_type
max_N = args.max_N
in_dir = args.in_dir
d_name = args.d_name
eta_bins = args.eta_bins

input_file = ROOT.TFile.Open(
    in_dir + "training_trees_pt10To100_%s_%s.root" % (jet_type, era)
)

for eta_bin in eta_bins:
    print("===================")
    print(".")
    print(".")
    print("Starting")
    print("eta bin:" + eta_bin)
    print(".")
    print(".")
    print("===================")
    PromptTree = input_file.Get(eta_bin + "_Prompt")
    PileupTree = input_file.Get(eta_bin + "_Pileup")

    output_file = ROOT.TFile(
        d_name + "/" + "tmva_output_Pt10To100_" + eta_bin + "_" + jet_type + ".root",
        "RECREATE"
    )

    N = min(PromptTree.GetEntries(), PileupTree.GetEntries())
    N = min(N, max_N)
    N = int(N/2)
    
    #-----------------------------------------------------------
    factory = ROOT.TMVA.Factory(
        "pileupJetId_" + era + "_" + eta_bin + "_" + jet_type,
        output_file,
        "!V:!Silent:Color:DrawProgressBar:Transformations=I;G:AnalysisType=Classification"
    )

    # --------------SET 1 For ETA < 3----------------------
    var_set1 = [
        ("nvtx"      , "I"),
        ("beta"      , "F"),
        ("dR2Mean"   , "F"),
        ("frac01"    , "F"),
        ("frac02"    , "F"),
        ("frac03"    , "F"),
        ("frac04"    , "F"),
        ("majW"      , "F"),
        ("minW"      , "F"),
        ("jetR"      , "F"),
        ("jetRchg"   , "F"),
        ("nParticles", "F"),
        ("nCharged"  , "F"),
        ("ptD"       , "F"),
        ("pull"      , "F"),
    ]
    
    # --------------SET 2 For ETA > 3----------------------
    var_set2 = [
        ("nvtx"      , "I"),
        #("beta"      , "F"),
        ("dR2Mean"   , "F"),
        ("frac01"    , "F"),
        ("frac02"    , "F"),
        ("frac03"    , "F"),
        ("frac04"    , "F"),
        ("majW"      , "F"),
        ("minW"      , "F"),
        ("jetR"      , "F"),
        #("jetRchg"   , "F"),
        ("nParticles", "F"),
        #("nCharged"  , "F"),
        ("ptD"       , "F"),
        ("pull"      , "F"),
    ]
    
    variables = var_set1
    spectator = [
        ("jetPt" , "F"),
        ("jetEta", "F"),
    ]
    
    if eta_bin == "Eta3p0To5p0":
        variables = var_set2
    
    loader = ROOT.TMVA.DataLoader(d_name)
    
    for var, var_type in variables:
        loader.AddVariable(var, var_type)
    
    for spec, spec_type in spectator:
        loader.AddSpectator(spec, spec_type)
    
    loader.AddTree(PromptTree, "Signal")
    loader.AddTree(PileupTree, "Background")
    
    loader.PrepareTrainingAndTestTree(
        ROOT.TCut(''),
        "SplitMode=Random:NormMode=NumEvents:!V:"
        + "nTrain_Signal=%d:nTest_Signal=%d:" % (N, N)
        + "nTrain_Background=%d:nTest_Background=%d:" % (N, N)
    )
    
    #-------------------------------------------------------------------
    factory.BookMethod(
        loader,
        ROOT.TMVA.Types.kBDT,
        "BDT",
        "!H:!V:NTrees=500:BoostType=Grad:Shrinkage=0.1:DoBoostMonitor"
    )
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()
    
    output_file.cd()
    output_file.Close()
