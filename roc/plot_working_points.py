#!/usr/bin/env python3

import ROOT

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

hist_file = ROOT.TFile.Open("PUJetId_wp_hists.root")

for i in range(80, 100):

    eff_plot_binned = hist_file.Get(f"prompt_eff_{i}_pileup_eff")
    eff_plot_binned.SetMarkerSize(2.7)
    
    eff_plot_inc = hist_file.Get(f"pt_bin_inclusive/prompt_eff_{i}_pileup_eff")
    eff_plot_inc.SetMarkerSize(2.7)
    
    eff_plot_binned.Draw("coltext89")
    canvas.Draw()
    canvas.Print(f"working_points/prompt_eff_{i}_binned.pdf")
    
    eff_plot_inc.Draw("coltext89")
    canvas.Draw()
    canvas.Print(f"working_points/prompt_eff_{i}_inc.pdf")
