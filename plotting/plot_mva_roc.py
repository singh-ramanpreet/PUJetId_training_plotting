#!/usr/bin/env python3

import ROOT
import os
from pyroot_cms_scripts import CMS_style

class graph_roc_mva():
    def __init__(self, mc_file, data_file, old_new, e_bin, pt_bins):
        self.mc_file = mc_file
        self.data_file = data_file
        self.old_new = old_new
        self.e_bin = e_bin
        self.pt_bins = pt_bins
        
        
    def get_mc_mva(self, key):
        mc_mva = self.mc_file.Get("mc_%s_mva_%s" % (self.old_new, key))
        return mc_mva
    
    def get_data_mva(self, key):
        data_mva = self.data_file.Get("data_%s_mva_%s" % (self.old_new, key))
        return data_mva

    def make_roc_array(self):
        k_prompt = self.e_bin + "_pt_bin_prompt"
        k_pileup = self.e_bin + "_pt_bin_pileup"

        h_prompt_ = [self.get_mc_mva(k_prompt.replace("pt_bin", p)) for p in self.pt_bins]
        h_pileup_ = [self.get_mc_mva(k_pileup.replace("pt_bin", p)) for p in self.pt_bins]

        for i, h_ in enumerate(h_prompt_):
            if i == 0:
                h_prompt = h_
            else:
                h_prompt += h_
        
        for i, h_ in enumerate(h_pileup_):
            if i == 0:
                h_pileup = h_
            else:
                h_pileup += h_
        
        assert (h_prompt.GetNbinsX() == h_pileup.GetNbinsX())

        array = []
        prompt_integral = h_prompt.Integral()
        pileup_integral = h_pileup.Integral()
        sum_prompt_bins = 0.0
        sum_pileup_bins = 0.0

        for i in range(1, h_prompt.GetNbinsX() + 1):

            sum_prompt_bins += h_prompt.GetBinContent(i)
            prompt_eff = 1 - (sum_prompt_bins/prompt_integral)

            sum_pileup_bins += h_pileup.GetBinContent(i)
            pileup_eff = 1 - (sum_pileup_bins/pileup_integral)

            assert (h_prompt.GetBinCenter(i) == h_pileup.GetBinCenter(i))

            mva_value = h_prompt.GetBinCenter(i)

            array.append([mva_value, prompt_eff, pileup_eff])
                    
        return array, h_prompt, h_pileup
    
    def make_roc_graph(self):
        graph = ROOT.TGraph()
        
        array = self.make_roc_array()[0]

        for i, (mva_value, prompt_eff, pileup_eff) in enumerate(array):
            graph.SetPoint(i, prompt_eff, pileup_eff)
            
        return graph
    
    def calc_wp(self, wp_pileup_eff):
        array = self.make_roc_array()[0]
        
        mva_value = [i[0] for i in array]
        prompt_eff = [i[1] for i in array]
        pileup_eff = [i[2] for i in array]
        
        # pileup eff is going down in array
        for j, p in enumerate(pileup_eff[:-1]):
            
            if wp_pileup_eff < pileup_eff[-1]:
                return mva_value[-1], prompt_eff[-1], pileup_eff[-1]
                
            #print(mva_value[j], prompt_eff[j], pileup_eff[j])
            if wp_pileup_eff >= pileup_eff[j + 1] and wp_pileup_eff < pileup_eff[j]:
                return mva_value[j], prompt_eff[j], pileup_eff[j]
    
    def find_eff(self, mva):
        array = self.make_roc_array()[0]
        
        mva_value = [i[0] for i in array]
        prompt_eff = [i[1] for i in array]
        pileup_eff = [i[2] for i in array]
        
        # mva values from -1 to 1
        for j, m in enumerate(mva_value):

            if mva == mva_value[j]:                
                return mva_value[j], prompt_eff[j], pileup_eff[j]


pt_bins = [
    "Pt10To20",
    "Pt20To30",
    "Pt30To40",
    "Pt40To50",
]

pt_bin_colors = [
    ROOT.kBlue,
    ROOT.kRed, 
    ROOT.kYellow + 1,
    ROOT.kCyan + 1,
]

prompt_color = ROOT.kGreen + 3
pileup_color = ROOT.kPink - 3

pt_summed_color = ROOT.kBlack

mc_file = ROOT.TFile.Open("hists_mc_pt10/hists_mc_2017full.root")
data_file = None

def plot_roc(mc_file=mc_file, e_bin="Eta0p0To2p5", leg_pos=(0.2, 0.6, 0.4, 0.9), frame=(0.04, 0.009, 1.01, 0.4)):
    
    os.makedirs("roc_mva_out", exist_ok=True)
    out_filename = "roc_mva_out/roc_%s" % e_bin
    
    CMS_style("1D")
    canvas = ROOT.TCanvas()

    canvas.DrawFrame(frame[0], frame[1], frame[2], frame[3], ";Prompt Eff.;Pileup Eff.")
    
    legend = ROOT.TLegend(leg_pos[0], leg_pos[1], leg_pos[2], leg_pos[3])
    legend.SetTextFont(42)
    legend.SetBorderSize(1)
    
    legend.SetHeader(e_bin.replace("Eta", "").replace("To", " < |#eta| #leq ").replace("p", "."))
    legend.AddEntry("", "New (Solid)", "")
    legend.AddEntry("", "Old (Dashed)", "")

    roc_mva_old = graph_roc_mva(mc_file, data_file, "old", e_bin, pt_bins=pt_bins)
    roc_mva_new = graph_roc_mva(mc_file, data_file, "new", e_bin, pt_bins=pt_bins)

    roc_graph_old = roc_mva_old.make_roc_graph()
    roc_graph_old.SetLineStyle(5)
    roc_graph_old.SetLineColor(pt_summed_color)

    roc_graph_new = roc_mva_new.make_roc_graph()
    roc_graph_new.SetLineStyle(1)
    roc_graph_new.SetLineColor(pt_summed_color)

    roc_mva_old_per_bin = []
    roc_mva_new_per_bin = []

    roc_graph_old_per_bin = []
    roc_graph_new_per_bin = []

    for j, pt_bin in enumerate(pt_bins):
        #print(pt_bin)
        roc_mva_old_per_bin.append(graph_roc_mva(mc_file, data_file, "old", e_bin, pt_bins=[pt_bin]))
        roc_mva_new_per_bin.append(graph_roc_mva(mc_file, data_file, "new", e_bin, pt_bins=[pt_bin]))

        roc_graph_old_per_bin.append(roc_mva_old_per_bin[j].make_roc_graph())
        roc_graph_old_per_bin[j].SetLineStyle(5)
        roc_graph_old_per_bin[j].SetLineColor(pt_bin_colors[j])
        roc_graph_old_per_bin[j].Draw("L")


        roc_graph_new_per_bin.append(roc_mva_new_per_bin[j].make_roc_graph())
        roc_graph_new_per_bin[j].SetLineStyle(1)
        roc_graph_new_per_bin[j].SetLineColor(pt_bin_colors[j])
        roc_graph_new_per_bin[j].Draw("L")

        legend.AddEntry(
            roc_graph_new_per_bin[j], 
            pt_bin.replace("Pt", "").replace("To", " < p_{T} #leq "),
            "f"
        )

    roc_graph_old.Draw("LP")
    roc_graph_new.Draw("LP")

    legend.AddEntry(roc_graph_new, "10 < p_{T} #leq 50", "f")

    legend.Draw()
    canvas.SetLogy()
    canvas.SetGrid()
    canvas.Draw()

    canvas.Print("%s.pdf" % out_filename)

    f = open("%s_tables.tex" % out_filename, "w+")
    print(r"\documentclass{article}", file=f)
    print(r"\begin{document}", file=f)
    print(r"\thispagestyle{empty}", file=f)

    for i in range(10):
        eff = 0.01 + i*0.01
        print(r"\begin{table}", file=f)
        print(r"\begin{tabular}{*{10}{c|}}", file=f)
        print(f"& \\multicolumn{{9}}{{c|}}{{Pileup Eff Cut {eff * 100:.2f}}}", end="\\\\ \n", file=f)
        wp = roc_mva_new.calc_wp(eff)
        wp1 = []
        wp2 = []
        for j, pt_bin in enumerate(pt_bins):
            wp1.append(roc_mva_new_per_bin[j].calc_wp(eff))
            wp2.append(roc_mva_new_per_bin[j].find_eff(wp[0]))

        print(
            f"& Pt10To50", "".join(f" & \\multicolumn{{2}}{{c|}}{{{pt_bin}}}" \
                                   for pt_bin in pt_bins),
            end="\\\\ \n", 
            file=f
        )
        print(
            f"MVA & {wp[0]:.3f} ", "".join(f"& {wp1[i][0]:.3f} & {wp2[i][0]:.3f}" \
                                           for i in range(len(pt_bins))),
            end="\\\\ \n",
            file=f
        )
        print(
            f"Prompt Eff & {wp[1] * 100:.2f} ", "".join(f"& {wp1[i][1] * 100:.2f} & {wp2[i][1] * 100:.2f} " \
                                                        for i in range(len(pt_bins))),
            end="\\\\ \n",
            file=f
        )
        print(
            f"Pileup Eff & {wp[2] * 100:.2f} ", "".join(f"& {wp1[i][2] * 100:.2f} & {wp2[i][2] * 100:.2f} " \
                                                        for i in range(len(pt_bins))),
            end="\\\\ \n",
            file=f
        )
        print(r"\end{tabular}", file=f)
        print(r"\end{table}", file=f)
    
    print(r"\end{document}", file=f)
        
    return canvas, legend

plot_roc(mc_file=mc_file, e_bin="Eta0p0To2p5", leg_pos=(0.2, 0.6, 0.4, 0.9), frame=(0.04, 0.009, 1.01, 0.4))
plot_roc(mc_file=mc_file, e_bin="Eta2p5To2p75", leg_pos=(0.2, 0.6, 0.4, 0.9), frame=(0.04, 0.009, 1.01, 0.4))
plot_roc(mc_file=mc_file, e_bin="Eta2p75To3p0", leg_pos=(0.2, 0.6, 0.4, 0.9), frame=(0.04, 0.009, 1.01, 0.4))
plot_roc(mc_file=mc_file, e_bin="Eta3p0To5p0", leg_pos=(0.2, 0.6, 0.4, 0.9), frame=(0.04, 0.009, 1.01, 0.4))


def plot_mva_hists(mc_hists_mvas=[], mc_data_hists_mva=[], e_bin="", pt_bin=""):
    canvas = ROOT.TCanvas()
    legend = ROOT.TLegend(0.7, 0.6, 0.85, 0.9)
    legend.SetTextFont(42)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)

    h_prompt_new = mc_hists_mvas[0]
    h_prompt_new.SetLineColor(prompt_color)
    h_prompt_new.SetLineStyle(1)
    h_prompt_new.SetStats(0)

    h_pileup_new = mc_hists_mvas[1]
    h_pileup_new.SetLineColor(pileup_color)
    h_pileup_new.SetLineStyle(1)
    h_pileup_new.SetStats(0)

    h_prompt_old = mc_hists_mvas[2]
    h_prompt_old.SetLineColor(prompt_color)
    h_prompt_old.SetLineStyle(5)
    h_prompt_old.SetStats(0)

    h_pileup_old = mc_hists_mvas[3]
    h_pileup_old.SetLineColor(pileup_color)
    h_pileup_old.SetLineStyle(5)
    h_pileup_old.SetStats(0)

    norm = h_prompt_new.GetNbinsX() / 2
    h_ = [h_prompt_new, h_pileup_new, h_prompt_old, h_pileup_old]
    h_ = sorted(h_, key=lambda x: x.GetMaximum()/x.GetSumOfWeights(), reverse=True)
    h_[0].GetXaxis().SetTitle("MVA Score")
    for h in h_:
        h.DrawNormalized("hist same", norm)
           
    legend.AddEntry("", e_bin.replace("Eta", "").replace("To", " < |#eta| #leq ").replace("p", "."), "")
    legend.AddEntry("", pt_bin.replace("Pt", "").replace("To", " < p_{T} < "), "")
    legend.AddEntry("", "New (Solid)", "")
    legend.AddEntry("", "Old (Dashed)", "")
    
    legend.AddEntry(h_prompt_new, "Prompt", "f")
    legend.AddEntry(h_pileup_new, "Pileup", "f")
    
    if len(mc_data_hists_mva) != 0:
        h_mc_new = mc_data_hists_mva[0]
        h_mc_new.SetLineColor(ROOT.kBlue)
        h_mc_new.SetLineStyle(1)

        h_mc_old = mc_data_hists_mva[1]
        h_mc_old.SetLineColor(ROOT.kBlue)
        h_mc_old.SetLineStyle(5)

        h_data_new = mc_data_hists_mva[2]
        h_data_new.SetLineColor(ROOT.kBlack)
        h_data_new.SetLineStyle(1)

        h_data_old = mc_data_hists_mva[3]
        h_data_old.SetLineColor(ROOT.kBlack)
        h_data_old.SetLineStyle(5)

        norm = h_mc_new.GetNbinsX() / 2
        h_ = [h_mc_new, h_mc_old, h_data_new, h_data_old]
        h_ = sorted(h_, key=lambda x: x.GetMaximum()/x.GetSumOfWeights(), reverse=True)
        for h in h_:
            h.DrawNormalized("hist same", norm)

        legend.AddEntry(h_mc_new, "MC", "f")
        legend.AddEntry(h_data_new, "Data", "f")
    
    return canvas, legend


eta_bins = [
    "Eta0p0To2p5",
    "Eta2p5To2p75",
    "Eta2p75To3p0",
    "Eta3p0To5p0",
]

for e_bin in eta_bins:
    roc_mva_old = graph_roc_mva(mc_file, data_file, "old", e_bin, pt_bins=pt_bins)
    roc_mva_new = graph_roc_mva(mc_file, data_file, "new", e_bin, pt_bins=pt_bins)
    roc_mva_old_per_bin = []
    roc_mva_new_per_bin = []
    for j, pt_bin in enumerate(pt_bins):
        roc_mva_old_per_bin.append(graph_roc_mva(mc_file1, data_file1, "old", e_bin, pt_bins=[pt_bin]))
        roc_mva_new_per_bin.append(graph_roc_mva(mc_file1, data_file1, "new", e_bin, pt_bins=[pt_bin]))

    mc_hists_mvas = [
        roc_mva_new.make_roc_array()[1], 
        roc_mva_new.make_roc_array()[2],
        roc_mva_old.make_roc_array()[1],
        roc_mva_old.make_roc_array()[2],
    ]
    pt_bin = "Pt10To50"
    c, l = plot_mva_hists(mc_hists_mvas=mc_hists_mvas, e_bin=e_bin, pt_bin=pt_bin)
    l.Draw()
    c.Draw()
    c.Print("roc_mva_out/mva_%s_%s.pdf" % (e_bin, pt_bin))

    for j, pt_bin in enumerate(pt_bins):
        mc_hists_mvas = [
            roc_mva_new_per_bin[j].make_roc_array()[1], 
            roc_mva_new_per_bin[j].make_roc_array()[2],
            roc_mva_old_per_bin[j].make_roc_array()[1],
            roc_mva_old_per_bin[j].make_roc_array()[2],
        ]

        c, l = plot_mva_hists(mc_hists_mvas=mc_hists_mvas, e_bin=e_bin, pt_bin=pt_bin)
        l.Draw()
        c.Draw()
        c.Print("roc_mva_out/mva_%s_%s.pdf" % (e_bin, pt_bin))

"""
mc_file2 = ROOT.TFile.Open("hists/hists_mc_2017full.root")
data_file2 = ROOT.TFile.Open("hists/hists_data_2017full.root")

pt_bins = [
    "Pt20To30",
    "Pt30To40",
    "Pt40To50",
]

for e_bin in eta_bins:
    
    roc_mva_old_per_bin = []
    roc_mva_new_per_bin = []
    for j, pt_bin in enumerate(pt_bins):
        roc_mva_old_per_bin.append(graph_roc_mva(mc_file2, data_file2, "old", e_bin, pt_bins=[pt_bin]))
        roc_mva_new_per_bin.append(graph_roc_mva(mc_file2, data_file2, "new", e_bin, pt_bins=[pt_bin]))

    for j, pt_bin in enumerate(pt_bins):
        mc_hists_mvas = [
            roc_mva_new_per_bin[j].make_roc_array()[1], 
            roc_mva_new_per_bin[j].make_roc_array()[2],
            roc_mva_old_per_bin[j].make_roc_array()[1],
            roc_mva_old_per_bin[j].make_roc_array()[2],
        ]
        
        mc_data_hists_mva = [
            roc_mva_new_per_bin[j].get_mc_mva(e_bin + "_" + pt_bin + "_all"),
            roc_mva_old_per_bin[j].get_mc_mva(e_bin + "_" + pt_bin + "_all"),
            roc_mva_new_per_bin[j].get_data_mva(e_bin + "_" + pt_bin),
            roc_mva_old_per_bin[j].get_data_mva(e_bin + "_" + pt_bin),
        ]

        print(mc_data_hists_mva)
        c, l = plot_mva_hists(mc_hists_mvas=mc_hists_mvas, mc_data_hists_mva=mc_data_hists_mva, e_bin=e_bin, pt_bin=pt_bin)
        l.Draw()
        c.Draw()
        c.Print("output/mva_mc_data_%s_%s.pdf" % (e_bin, pt_bin))
        
"""

input("Press any key to exit ... ")
