#!/usr/bin/env python3

import ROOT
import os
from pyroot_cms_scripts import CMS_style
import argparse

parser = argparse.ArgumentParser("")
parser.add_argument("--year", type=str, default="2017")

args = parser.parse_args()

eff_mva_hists = ROOT.TFile.Open(f"eff_mva_hists_{args.year}.root")

eta_bin = "Eta0p0To2p5"
pt_bin = "Pt10To20"

plot_roc = """
h_prompt_eff = eff_mva_hists.Get(f"prompt_eff_new_{eta_bin}_{pt_bin}")
h_pileup_eff = eff_mva_hists.Get(f"pileup_eff_new_{eta_bin}_{pt_bin}")

roc_graph = ROOT.TGraph()

n_bins = h_prompt_eff.GetNbinsX()

for i in range(1, n_bins + 1):
    
    prompt_eff = h_prompt_eff.GetBinContent(i)
    pileup_eff = h_pileup_eff.GetBinContent(i)

    roc_graph.SetPoint(i - 1, prompt_eff, pileup_eff)
    
#roc_graph.Draw("l")
"""

eta_bins = [
    ("Eta0p0To2p5", (0.04, 0.009, 1.01, 0.4)),
    ("Eta2p5To2p75", (0.04, 0.009, 1.01, 0.4)),
    ("Eta2p75To3p0", (0.04, 0.009, 1.01, 0.4)),
    ("Eta3p0To5p0", (0.01, 0.05, 1.01, 0.6))
]

pt_bins = [
    ("Pt10To20", ROOT.kBlue),
    ("Pt20To30", ROOT.kRed),
    ("Pt30To40", ROOT.kYellow + 1),
    ("Pt40To50", ROOT.kCyan + 1),
    ("Pt10To50", ROOT.kBlack),
]

for e in eta_bins:

    eta_bin = e[0]
    frame = e[1]

    CMS_style.SetLabelSize(0.04)
    CMS_style.cd()
    ROOT.gROOT.ForceStyle()

    canvas = ROOT.TCanvas()
    canvas.SetGrid()
    canvas.SetLogy()
    canvas.DrawFrame(frame[0], frame[1], frame[2], frame[3], ";Prompt Efficiency;Pileup Efficiency")

    legend = ROOT.TLegend(0.2, 0.6, 0.4, 0.9)
    legend.SetTextFont(42)
    legend.SetBorderSize(1)

    legend.SetHeader(f"{eta_bin.replace('Eta', '').replace('p', '.').replace('To', ' < |#eta| <')}")
    legend.AddEntry("", "Solid (New)", "")
    legend.AddEntry("", "Dashed (Old)", "")
    
    rocs = []

    for p in pt_bins:

        pt_bin = p[0]
        color = p[1]

        exec(plot_roc)
        roc_graph.SetLineColor(color)
        roc_graph.SetLineStyle(1)

        rocs.append(roc_graph.Clone(f"new_{eta_bin}_{pt_bin}"))
        legend.AddEntry(rocs[-1], f"{pt_bin.replace('Pt', '').replace('To', ' < p_{T} < ')}", "f")

        exec(plot_roc.replace("new", "old"))
        roc_graph.SetLineColor(color)
        roc_graph.SetLineStyle(8)
        
        rocs.append(roc_graph.Clone(f"old_{eta_bin}_{pt_bin}"))

    for roc in rocs:
        roc.Draw("l")

    legend.Draw()

    canvas.Draw()
    os.makedirs(f"plt_roc_{args.year}", exist_ok=True)
    canvas.Print(f"plt_roc_{args.year}/roc_{eta_bin}.pdf")
