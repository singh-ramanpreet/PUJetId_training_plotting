#!/usr/bin/env python3

import ROOT
import argparse

parser = argparse.ArgumentParser("")
parser.add_argument("--year", type=str, default="2017")

args = parser.parse_args()

mc_file = ROOT.TFile.Open(f"dy_madgraph_10_mc_{args.year}full.root")
eta_bin = "Eta0p0To2p5"
pt_bin = "Pt10To20"

pt_inclusive_bin = False
inclusive_bins = []
inclusive_bin_name = ""

make_eff_mva_hists = """
bare_hist = mc_file.Get("mc_new_mva_Eta0p0To2p5_Pt10To20_prompt").Clone()
bare_hist.Reset()

if pt_inclusive_bin:
    pt_bin = inclusive_bin_name
    h_prompt = bare_hist.Clone()
    h_pileup = bare_hist.Clone()

    for i_bin in inclusive_bins:
        h_prompt += mc_file.Get(f"mc_new_mva_{eta_bin}_{i_bin}_prompt")
        h_pileup += mc_file.Get(f"mc_new_mva_{eta_bin}_{i_bin}_pileup")

else:
    h_prompt = mc_file.Get(f"mc_new_mva_{eta_bin}_{pt_bin}_prompt")
    h_pileup = mc_file.Get(f"mc_new_mva_{eta_bin}_{pt_bin}_pileup")

h_prompt_eff = bare_hist.Clone(f"prompt_eff_new_{eta_bin}_{pt_bin}")
h_prompt_eff.SetTitle(";MVA Score;Prompt Efficiency")

h_pileup_eff = bare_hist.Clone(f"pileup_eff_new_{eta_bin}_{pt_bin}")
h_pileup_eff.SetTitle(";MVA Score;Pileup Efficiency")

n_bins = h_prompt.GetNbinsX()

prompt_area = h_prompt.Integral()
pileup_area = h_pileup.Integral()

sum_prompt_bins = 0.0
sum_pileup_bins = 0.0

for i in range(1, n_bins + 1):

    sum_prompt_bins += h_prompt.GetBinContent(i)
    sum_pileup_bins += h_pileup.GetBinContent(i)

    prompt_eff = 1 - (sum_prompt_bins / prompt_area)
    pileup_eff = 1 - (sum_pileup_bins / pileup_area)

    h_prompt_eff.SetBinContent(i, prompt_eff)
    h_pileup_eff.SetBinContent(i, pileup_eff)
"""

eta_bins = [
    "Eta0p0To2p5",
    "Eta2p5To2p75",
    "Eta2p75To3p0",
    "Eta3p0To5p0",
]

pt_bins = [
    "Pt10To20",
    "Pt20To30",
    "Pt30To40",
    "Pt40To50",
    "Pt50To100"
]

eff_out_file = ROOT.TFile(f"eff_mva_hists_{args.year}.root", "recreate")

for category in ["old", "new"]:

    for e in eta_bins:
    
        for p in pt_bins:

            eta_bin = e
            pt_bin = p

            exec(make_eff_mva_hists.replace("new", category))

            eff_out_file.cd()
            h_prompt_eff.Write()
            h_pileup_eff.Write()


for category in ["old", "new"]:

    for e in eta_bins:

        eta_bin = e
        pt_inclusive_bin = True
        inclusive_bin_name = "Pt10To50"
        inclusive_bins = ["Pt10To20", "Pt20To30", "Pt30To40", "Pt40To50"]

        exec(make_eff_mva_hists.replace("new", category))

        eff_out_file.cd()
        h_prompt_eff.Write()
        h_pileup_eff.Write()
