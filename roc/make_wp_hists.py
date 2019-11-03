#!/usr/bin/env python3

import ROOT
import numpy as np
import argparse

parser = argparse.ArgumentParser("")
parser.add_argument("--year", type=str, default="2017")

args = parser.parse_args()

eff_mva_hists = ROOT.TFile.Open(f"eff_mva_hists_{args.year}.root")
output_root_file = ROOT.TFile(f"PUJetId_wp_hists_{args.year}.root", "recreate")

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
    "Pt40To50",
]

output_root_file.cd()

make_wp_hists = """
eta_edges = [0.0] + [float(e.replace("Eta", "").replace("p", ".").split("To")[1]) for e in eta_bins]
pt_edges = [10.0] + [float(p.replace("Pt", "").replace("p", ".").split("To")[1]) for p in pt_bins]

print("Eta edges  ", eta_edges)
print("Pt edges   ", pt_edges)

# 20% to 99%
prompt_effs = [round(0.20 + i * 0.01, 2) for i in range(80)]

for prompt_eff in prompt_effs:

    name_string = f"{prompt_eff * 100:2.0f}"

    wp_hist_mva = ROOT.TH2F(
        f"prompt_eff_{name_string}_mva_score", f"MVA Score for Prompt Eff. {name_string};p_{{T}};|#eta|",
        len(pt_edges) - 1, np.array(pt_edges, dtype=np.float64),
        len(eta_edges) - 1, np.array(eta_edges, dtype=np.float64)
    )
    wp_hist_mva.SetStats(0)

    wp_hist_pileup = ROOT.TH2F(
        f"prompt_eff_{name_string}_pileup_eff", f"Pileup Eff. for Prompt Eff. {name_string};p_{{T}};|#eta|",
        len(pt_edges) - 1, np.array(pt_edges, dtype=np.float64),
        len(eta_edges) - 1, np.array(eta_edges, dtype=np.float64)
    )
    wp_hist_pileup.SetStats(0)

    for e in eta_bins:

        e_bin_edges = e.replace("Eta", "").replace("p", ".").split("To")
        e_bin_center = (float(e_bin_edges[0]) + float(e_bin_edges[1]))/2.0

        for p in pt_bins:

            p_bin_edges = p.replace("Pt", "").replace("p", ".").split("To")
            p_bin_center = (float(p_bin_edges[0]) + float(p_bin_edges[1]))/2.0

            h_prompt_eff = eff_mva_hists.Get(f"prompt_eff_new_{e}_{p}")
            h_pileup_eff = eff_mva_hists.Get(f"pileup_eff_new_{e}_{p}")

            htemp = h_prompt_eff.Clone()

            # loop over eff hist and find nearest best value
            for i in range(1, h_prompt_eff.GetNbinsX() + 1):

                bin_content = htemp.GetBinContent(i)
                if bin_content == 0.0:
                    htemp.SetBinContent(i, 1)
                else:
                    htemp.SetBinContent(i, abs(bin_content - prompt_eff))

            mva_score_bin = htemp.GetMinimumBin()

            mva_score_value = h_prompt_eff.GetBinCenter(mva_score_bin)
            pileup_eff = h_pileup_eff.GetBinContent(mva_score_bin)

            pileup_eff = round(pileup_eff * 100, 2)

            wp_hist_mva.SetBinContent(wp_hist_mva.FindBin(p_bin_center, e_bin_center), mva_score_value)
            wp_hist_pileup.SetBinContent(wp_hist_pileup.FindBin(p_bin_center, e_bin_center), pileup_eff)

    wp_hist_pileup.SetMarkerSize(1.4)

    wp_hist_mva.Write()
    wp_hist_pileup.Write()
"""

exec(make_wp_hists)

pt_bins = ["Pt10To50"]

output_root_file.mkdir("pt_bin_inclusive")
output_root_file.cd("pt_bin_inclusive")

exec(make_wp_hists)
