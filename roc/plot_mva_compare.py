#!/usr/bin/env python3

import ROOT
import os
from pyroot_cms_scripts import CMS_style

ROOT.gROOT.SetBatch(ROOT.kTRUE)

mc_files = {
    "UL17": ROOT.TFile.Open(f"dy_madgraph_10_mc_2017full.root"),
    "UL18": ROOT.TFile.Open(f"dy_madgraph_10_mc_2018full.root"),
    "UL16": ROOT.TFile.Open(f"dy_madgraph_10_mc_UL16full.root"),
    "UL16APV": ROOT.TFile.Open(f"dy_madgraph_10_mc_UL16APVfull.root"),
}

colors = {
    "UL17": {"prompt": ROOT.kGreen, "pileup": ROOT.kPink},
    "UL18": {"prompt": ROOT.kGreen + 1, "pileup": ROOT.kPink + 1},
    "UL16": {"prompt": ROOT.kGreen + 2, "pileup": ROOT.kPink + 2},
    "UL16APV": {"prompt": ROOT.kGreen + 3, "pileup": ROOT.kPink + 3},
}

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

        h_prompt = {}
        h_pileup = {}
        for i,era in enumerate(mc_files):
            h_prompt[era] = mc_files[era].Get(f"mc_new_mva_{e}_{p}_prompt")
            h_prompt[era].SetLineColor(colors[era]["prompt"])
            h_prompt[era].SetLineStyle(1)

            h_pileup[era] = mc_files[era].Get(f"mc_new_mva_{e}_{p}_pileup")
            h_pileup[era].SetLineColor(colors[era]["pileup"])
            h_pileup[era].SetLineStyle(1)

            CMS_style.SetLabelSize(0.04)
            CMS_style.cd()
            ROOT.gROOT.ForceStyle()

            canvas = ROOT.TCanvas()

            h_prompt[era].Scale(100/h_prompt[era].Integral())
            h_pileup[era].Scale(100/h_pileup[era].Integral())
            #h_prompt[era].Rebin(4)
            #h_pileup[era].Rebin(4)

        maxY = max(max(h_prompt[x].GetMaximum() for x in h_prompt), max(h_pileup[x].GetMaximum() for x in h_pileup))

        legend = ROOT.TLegend(0.5, 0.7, 0.7, 0.9)
        legend.SetTextFont(42)
        legend.SetBorderSize(0)

        legend.SetHeader(f"{e.replace('Eta', '').replace('p', '.').replace('To', ' < |#eta| <')}")
        legend.AddEntry("", f"{p.replace('Pt', '').replace('To', ' < p_{T} < ')}", "")

        for i,era in enumerate(h_prompt):
            legend.AddEntry(h_prompt[era], f"Prompt {era}", "f")
            legend.AddEntry(h_pileup[era], f"Pileup {era}", "f")

            if i == 0:
                h_prompt[era].SetMaximum(maxY * 1.2)
                h_prompt[era].SetTitle(";MVA Score; a.u.")
                h_prompt[era].Draw("hist")
                h_pileup[era].Draw("hist same")
            else:
                h_prompt[era].Draw("hist same")
                h_pileup[era].Draw("hist same")


        legend.Draw()
        canvas.Draw()
        plot_dir = "plt_mva_compare"
        plot_filename = f"mva_{e}_{p}"
        os.makedirs(f"{plot_dir}", exist_ok=True)
        canvas.Print(f"{plot_dir}/{plot_filename}.pdf")
        os.popen(f"convert -density 150 -antialias {plot_dir}/{plot_filename}.pdf -trim {plot_dir}/{plot_filename}.png 2> /dev/null")
