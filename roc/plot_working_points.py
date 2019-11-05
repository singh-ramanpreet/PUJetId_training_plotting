#!/usr/bin/env python3

import ROOT
import os
import argparse

parser = argparse.ArgumentParser("")
parser.add_argument("--year", type=str, default="2017")
parser.add_argument("--batch", action="store_true")

args = parser.parse_args()

print(args.batch)
if args.batch:
    ROOT.gROOT.SetBatch(1)

ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

ROOT.gStyle.SetTitleSize(0.05, "XY")
ROOT.gStyle.SetTitleOffset(1.0, "X")

ROOT.gStyle.SetPadRightMargin(0.02)
ROOT.gStyle.SetPadBottomMargin(0.12)

ROOT.gStyle.SetOptStat(0)

ROOT.gStyle.SetPalette(ROOT.kBeach)

ROOT.gROOT.ForceStyle()

canvas = ROOT.TCanvas()

hist_file = ROOT.TFile.Open(f"PUJetId_wp_hists_{args.year}.root")

os.makedirs(f"working_points_{args.year}", exist_ok=True)

for i in range(80, 100):

    eff_plot_binned = hist_file.Get(f"prompt_eff_{i}_pileup_eff")
    eff_plot_binned.SetMarkerSize(2.7)
    
    eff_plot_inc = hist_file.Get(f"pt_bin_inclusive/prompt_eff_{i}_pileup_eff")
    eff_plot_inc.SetMarkerSize(2.7)
    
    eff_plot_binned.Draw("coltext")
    canvas.Draw()
    canvas.Print(f"working_points_{args.year}/prompt_eff_{i}_binned.pdf")
    
    eff_plot_inc.Draw("coltext")
    canvas.Draw()
    canvas.Print(f"working_points_{args.year}/prompt_eff_{i}_inc.pdf")
