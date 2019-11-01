#!/usr/bin/env python3

import ROOT
from array import array
import argparse

parser = argparse.ArgumentParser(
    description="make TTrees for training"
    )
parser.add_argument(
    "--era", type=str, default="94X", help="MC era, like 94X, 102X"
    )
parser.add_argument(
    "--inputFiles", type=str, default=[], nargs="+", help="MC era, like 94X, 102X"
    )

args = parser.parse_args()

era = args.era
inputFiles = args.inputFiles

tChain  = ROOT.TChain("jmechs/events")
outFile = ROOT.TFile("training_trees_pt10To100_chs_%s.root" % era, "RECREATE")

for inputFile in inputFiles:
    tChain.Add(inputFile)

eta_bins = [
    "Eta0p0To2p5" ,
    "Eta2p5To2p75",
    "Eta2p75To3p0",
    "Eta3p0To5p0" ,
]

outTrees = []

for eta_bin in eta_bins:
    outTrees.append(ROOT.TTree(eta_bin + "_Prompt", eta_bin + "_Prompt"))
    
for eta_bin in eta_bins:
    outTrees.append(ROOT.TTree(eta_bin + "_Pileup", eta_bin + "_Pileup"))

def book_float_branch(ttree, branch_name, default_value=-999.0):
    branch_array = array("f", [default_value])
    ttree.Branch(branch_name, branch_array, "%s/F" % branch_name)        
    return branch_array

def book_int_branch(ttree, branch_name, default_value=-999):
    branch_array = array("i", [default_value])
    ttree.Branch(branch_name, branch_array, "%s/I" % branch_name)        
    return branch_array

NTrees = len(outTrees)

nvtx            = NTrees*[0]
rho             = NTrees*[0]
jetPt           = NTrees*[0]
jetEta          = NTrees*[0]
dR2Mean         = NTrees*[0]
majW            = NTrees*[0]
minW            = NTrees*[0]
frac01          = NTrees*[0]
frac02          = NTrees*[0]
frac03          = NTrees*[0]
frac04          = NTrees*[0]
ptD             = NTrees*[0]
beta            = NTrees*[0]
betaStar        = NTrees*[0]
pull            = NTrees*[0]
jetR            = NTrees*[0]
jetRchg         = NTrees*[0]
nParticles      = NTrees*[0]
nCharged        = NTrees*[0]
dRMatch         = NTrees*[0]
refdrjt         = NTrees*[0]
jetFlavorParton = NTrees*[0]
nTrueInt        = NTrees*[0]

for i, outTree in enumerate(outTrees):
    nvtx           [i] = book_int_branch  (outTree, "nvtx"           )
    rho            [i] = book_float_branch(outTree, "rho"            )
    jetPt          [i] = book_float_branch(outTree, "jetPt"          )
    jetEta         [i] = book_float_branch(outTree, "jetEta"         )
    dR2Mean        [i] = book_float_branch(outTree, "dR2Mean"        )
    majW           [i] = book_float_branch(outTree, "majW"           )
    minW           [i] = book_float_branch(outTree, "minW"           )
    frac01         [i] = book_float_branch(outTree, "frac01"         )
    frac02         [i] = book_float_branch(outTree, "frac02"         )
    frac03         [i] = book_float_branch(outTree, "frac03"         )
    frac04         [i] = book_float_branch(outTree, "frac04"         )
    ptD            [i] = book_float_branch(outTree, "ptD"            )
    beta           [i] = book_float_branch(outTree, "beta"           )
    betaStar       [i] = book_float_branch(outTree, "betaStar"       )
    pull           [i] = book_float_branch(outTree, "pull"           )
    jetR           [i] = book_float_branch(outTree, "jetR"           )
    jetRchg        [i] = book_float_branch(outTree, "jetRchg"        )
    nParticles     [i] = book_int_branch  (outTree, "nParticles"     )
    nCharged       [i] = book_int_branch  (outTree, "nCharged"       )
    dRMatch        [i] = book_float_branch(outTree, "dRMatch"        )
    refdrjt        [i] = book_float_branch(outTree, "refdrjt"        )
    jetFlavorParton[i] = book_int_branch  (outTree, "jetFlavorParton")
    nTrueInt       [i] = book_int_branch  (outTree, "nTrueInt"       )

for ievent, event in enumerate(tChain):
    if ievent % 10000 == 0:
        print("processing %s" % ievent)
    #if ievent > 40000: break
    
    if event.nLeptons != 2: continue

    for i in range(event.nJets):
        dRMatch_ = event.dRMatch[i]
        eta_     = event.jetEta[i]
        flavor_  = event.jetFlavorParton[i]

        if event.jetPt[i] > 100: continue
        
        isPrompt = False
        isPileup = False
        
        if (dRMatch_ <= 0.2):
            isPrompt = True
        
        if (dRMatch_ >= 0.4 and abs(flavor_) == 0 ):
            isPileup = True
            
        key = ""
        
        if (isPrompt and (        abs(eta_) <= 2.5 )) : key = 0
        if (isPrompt and ( 2.5  < abs(eta_) <= 2.75)) : key = 1
        if (isPrompt and ( 2.75 < abs(eta_) <= 3.0 )) : key = 2
        if (isPrompt and ( 3.0  < abs(eta_) <= 5.0 )) : key = 3
        
        if (isPileup and (        abs(eta_) <= 2.5 )) : key = 4
        if (isPileup and ( 2.5  < abs(eta_) <= 2.75)) : key = 5
        if (isPileup and ( 2.75 < abs(eta_) <= 3.0 )) : key = 6
        if (isPileup and ( 3.0  < abs(eta_) <= 5.0 )) : key = 7

        # nothing matched
        if key == "": continue

        outTree_toFill = outTrees[key]
        
        nvtx           [key][0] = event.npv
        rho            [key][0] = event.rho
        jetPt          [key][0] = event.jetPt[i]
        jetEta         [key][0] = event.jetEta[i]
        dR2Mean        [key][0] = event.dR2Mean[i]
        majW           [key][0] = event.majW[i]
        minW           [key][0] = event.minW[i]
        frac01         [key][0] = event.frac01[i]
        frac02         [key][0] = event.frac02[i]
        frac03         [key][0] = event.frac03[i]
        frac04         [key][0] = event.frac04[i]
        ptD            [key][0] = event.ptD[i]
        beta           [key][0] = event.beta[i]
        betaStar       [key][0] = event.betaStar[i]
        pull           [key][0] = event.pull[i]
        jetR           [key][0] = event.jetR[i]
        jetRchg        [key][0] = event.jetRchg[i]
        nParticles     [key][0] = event.nParticles[i]
        nCharged       [key][0] = event.nCharged[i]
        dRMatch        [key][0] = event.dRMatch[i]
        refdrjt        [key][0] = event.jetGenPt[i]
        jetFlavorParton[key][0] = event.jetFlavorParton[i]
        nTrueInt       [key][0] = event.nTrueInt
            
        outTree_toFill.Fill()

for outTree in outTrees:
    outTree.Write("", ROOT.TObject.kOverwrite)

outFile.Write("", ROOT.TObject.kOverwrite)
outFile.Close()
