#!/usr/bin/env python3

import sys
import ROOT
from pyroot_cms_scripts import CMS_style, CMS_text

import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--mc_hist_file", type=str, default="hists/hists_mc_2017full.root",
    help="mc histogram root file, default=%(default)s"
    )

parser.add_argument(
    "--data_hist_file", type=str, default="hists/hists_data_2017full.root",
    help="mc histogram root file, default=%(default)s"
    )

parser.add_argument(
    "--variable", type=str, default="Z_mass",
    help="name of the varaible, default=%(default)s"
    )

parser.add_argument(
    "--units", type=str, default="GeV",
    help="variable units, default=%(default)s"
    )

parser.add_argument(
    "--title_x", type=str, default="m_{Z}",
    help="X axis title, default=%(default)s"
    )

parser.add_argument(
    "--title_y", type=str, default="",
    help="Y axis title, default=Events/ (bw) (units)"
    )

parser.add_argument(
    "--show_bw", action="store_false",
    help="show bin width in Y axis title, default=%(default)s"
    )

parser.add_argument(
    "--leg_pos", type=float, nargs=4,
    default=[0.7, 0.8, 0.9, 0.9],
    help="legend position x1, y1, x2, y2, default=%(default)s"
    )

parser.add_argument(
    "--eta_bin", type=str, default="",
    help="eta bin of variable, default=%(default)s"
    )

parser.add_argument(
    "--pt_bin", type=str, default="",
    help="pt bin of variable, default=%(default)s"
    )

args = parser.parse_args()

# assign arguments
# ================
mc_hist_file = args.mc_hist_file
data_hist_file = args.data_hist_file
variable = args.variable
units = args.units
title_x = args.title_x
title_y = args.title_y
show_bw = args.show_bw
leg_pos = args.leg_pos
eta_bin = args.eta_bin
pt_bin = args.pt_bin

if units != "":
    title_x = f"{title_x} ({units})"

if title_y == "":
    title_y = "Events"
        
mc_hist_file = ROOT.TFile.Open(mc_hist_file)
data_hist_file = ROOT.TFile.Open(data_hist_file)

# make stack of mc samples
# overlay data with points
# ========================
ROOT.TGaxis().SetMaxDigits(4)
CMS_style.cd()
ROOT.gROOT.ForceStyle()

legend = ROOT.TLegend(leg_pos[0], leg_pos[1], leg_pos[2], leg_pos[3])
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.SetTextFont(42)
legend.SetTextSize(0.03)

h_data = data_hist_file.Get(f"data_{variable}")
h_mc = mc_hist_file.Get(f"mc_{variable}")

h_data.SetMarkerStyle(8)
h_data.SetMarkerColor(ROOT.kBlack)
legend.AddEntry(h_data, "Data", "pe")

h_mc.SetLineColor(ROOT.kBlue + 1)
legend.AddEntry(h_mc, "MC (All)", "f")

bw = h_data.GetBinWidth(1)

if show_bw:
    title_y = f"{title_y} / {bw} {units}"

h_data.SetTitle(f";{title_x};{title_y}")
h_mc.SetTitle(f";{title_x};{title_y}")

maxY = max(h_data.GetMaximum(), h_mc.GetMaximum())
minY = min(h_data.GetMinimum(), h_mc.GetMinimum())
    
if minY == 0.0:
    minY = 0.01
    
h_mc.SetMaximum(maxY * 1.15)
h_data.SetMaximum(maxY * 1.15)

diff = h_data.Integral() / h_mc.Integral()

h_mc.SetStats(0)
h_data.SetStats(0)

# ------------------
canvas = ROOT.TCanvas()

left_margin = canvas.GetLeftMargin()
right_margin = canvas.GetRightMargin()

ratio = ROOT.TRatioPlot(h_data, h_mc)

ratio.SetH1DrawOpt("x0e1")
ratio.SetH2DrawOpt("hist")
ratio.SetGraphDrawOpt("PZ")

ratio.SetSeparationMargin(0.0)
ratio.SetLeftMargin(left_margin)
ratio.SetRightMargin(right_margin)
ratio.SetUpTopMargin(0.075)
ratio.SetLowBottomMargin(0.40)

ratio.Draw("grid hideup")

graph_ref = ratio.GetLowerRefGraph()
graph_ref.SetMarkerStyle(7)
graph_ref.SetMaximum(1.5)
graph_ref.SetMinimum(1.1)

ratio.GetLowYaxis().SetNdivisions(502)

upper_pad = ratio.GetUpperPad()
upper_pad.cd()
CMS_text(
    upper_pad,
    cms_text_scale=1.4,
    draw_lumi_text=True,
    lumi_text="#scale[1.2]{41.54 fb^{-1} (13 TeV)}",
)

canvas.SaveAs(f"{variable}.pdf")

input("Press any key to exit")
