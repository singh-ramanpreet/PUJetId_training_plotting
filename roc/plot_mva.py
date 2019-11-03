#!/usr/bin/env python3

import ROOT
import os
from pyroot_cms_scripts import CMS_style
import argparse

parser = argparse.ArgumentParser("")
parser.add_argument("--year", type=str, default="2017")

args = parser.parse_args()

mc_file = ROOT.TFile.Open(f"dy_madgraph_10_mc_{args.year}full.root")

eta_bins = [
    "Eta0p0To2p5",
    "Eta2p5To2p75",
    "Eta2p75To3p0",
    "Eta3p0To5p0"
]

pt_bins = [
    "Pt10To20",
    "Pt20To30",
    "Pt30To40",
    "Pt40To50"
]

for e in eta_bins:

    for p in pt_bins:

        h_prompt_new = mc_file.Get(f"mc_new_mva_{e}_{p}_prompt")
        h_prompt_new.SetLineColor(ROOT.kGreen + 3)
        h_prompt_new.SetLineStyle(1)

        h_pileup_new = mc_file.Get(f"mc_new_mva_{e}_{p}_pileup")
        h_pileup_new.SetLineColor(ROOT.kPink - 3)
        h_pileup_new.SetLineStyle(1)

        h_prompt_old = mc_file.Get(f"mc_old_mva_{e}_{p}_prompt")
        h_prompt_old.SetLineColor(ROOT.kGreen + 3)
        h_prompt_old.SetLineStyle(8)

        h_pileup_old = mc_file.Get(f"mc_old_mva_{e}_{p}_pileup")
        h_pileup_old.SetLineColor(ROOT.kPink - 3)
        h_pileup_old.SetLineStyle(8)


        CMS_style.SetLabelSize(0.04)
        CMS_style.cd()
        ROOT.gROOT.ForceStyle()

        canvas = ROOT.TCanvas()

        h_prompt_new.Scale(100/h_prompt_new.Integral())
        h_pileup_new.Scale(100/h_pileup_new.Integral())
        h_prompt_old.Scale(100/h_prompt_old.Integral())
        h_pileup_old.Scale(100/h_pileup_old.Integral())

        maxY = max(
            h_prompt_new.GetMaximum(),
            h_pileup_new.GetMaximum(),
            h_prompt_old.GetMaximum(),
            h_pileup_old.GetMaximum()
        )

        legend = ROOT.TLegend(0.5, 0.7, 0.7, 0.9)
        legend.SetTextFont(42)
        legend.SetBorderSize(0)

        legend.SetHeader(f"{e.replace('Eta', '').replace('p', '.').replace('To', ' < |#eta| <')}")
        legend.AddEntry("", "Solid (New)", "")
        legend.AddEntry("", "Dashed (Old)", "")
        legend.AddEntry("", f"{p.replace('Pt', '').replace('To', ' < p_{T} < ')}", "")

        h_prompt_new.SetMaximum(maxY * 1.2)
        h_prompt_new.SetTitle(";MVA Score; a.u.")

        h_prompt_new.Draw("hist")
        h_pileup_new.Draw("hist same")
        h_prompt_old.Draw("hist same")
        h_pileup_old.Draw("hist same")

        legend.AddEntry(h_prompt_new, "Prompt", "f")
        legend.AddEntry(h_pileup_new, "Pileup", "f")

        legend.Draw()
        canvas.Draw()
        os.makedirs(f"plt_mva_{args.year}", exist_ok=True)
        canvas.Print(f"plt_mva_{args.year}/mva_{e}_{p}.pdf")
