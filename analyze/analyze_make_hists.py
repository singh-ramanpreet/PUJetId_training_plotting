#!/usr/bin/env python3

import ROOT
import os
import sys
from array import array
import argparse

ROOT.gROOT.SetBatch(True)

if "HOME" not in os.environ:
    os.environ["HOME"] = "" # needed for condor batch mode

parser = argparse.ArgumentParser(
    description="analyze and make hists from JME flat ntuple"
    )
parser.add_argument(
    "--era", type=str, default="94X", help="data Era, default=%(default)s"
    )
parser.add_argument(
    "--data_type", type=str, default="mc", help="data or mc, default=%(default)s"
    )
parser.add_argument(
    "--year", type=str, default="2017",
    help="Data year: 2017 or 2018, default=%(default)s"
    )
parser.add_argument(
    "--period", type=str, default="F",
    help="Data period: A,B,C,D... , default=%(default)s"
    )
parser.add_argument(
    "--lumi", type=float, default=13.54,
    help="Data integrated lumi (1/fb) , default=%(default)s"
    )
parser.add_argument(
    "--N_mc", type=int, default=48675378,
    help="# of generated evts of MC sample, default=%(default)s"
    )
parser.add_argument(
    "--xs", type=float, default=5343.0,
    help="Cross Section (pb) of MC sample, default=%(default)s"
    )
parser.add_argument(
    "--input_filename", type=str, help="input root file location"
    )
parser.add_argument(
    "--output_filename", type=str, help="output root file name"
    )

args = parser.parse_args()

era = args.era
data_type = args.data_type
year = args.year
period = args.period
lumi = args.lumi
N_mc = args.N_mc
xs = args.xs
input_filename = args.input_filename
output_filename = args.output_filename

xs_weight = lumi * xs * 1000 / N_mc

print("====================")
print("DataSet:\t", data_type)
print("Era, Year, Period:\t", era, year, period)
print("====================")
print("XS Weight: %s (1/fb) * 1000 * %s (pb) / (%s) = %s" % (lumi, xs, N_mc, xs_weight))
print("====================")
print("Input File:\t", input_filename)
print("Output File:\t", output_filename)

input_tree = "jmechs/events"

input_file = ROOT.TFile.Open(input_filename)
events = input_file.Get(input_tree)

eta_bins = [
    "Eta0p0To2p5",
    "Eta2p5To2p75",
    "Eta2p75To3p0",
    "Eta3p0To5p0"
]

f_eta_bins = [
    tuple(float(x) for x in eta_bin.replace("Eta", "").replace("p", ".").split("To")) for eta_bin in eta_bins
]

pt_bins = [
    "Pt10To20",
    "Pt20To30",
    "Pt30To40",
    "Pt40To50",
    "Pt50To100",
]

f_pt_bins = [
    tuple(float(x) for x in pt_bin.replace("Pt", "").split("To")) for pt_bin in pt_bins
]

tmva_weight_filenames = [
    "tmva_weights/pileupJetId_%s_%s_chs_BDT.weights.xml" % (era, i) for i in eta_bins
]

# uncomment below for testing old training,
# and comment above ones

#tmva_weight_filenames = [
#    "old_training_files/pileupJetId_80XvarFix_Eta0to2p5_BDT.weights.xml",
#    "old_training_files/pileupJetId_80XvarFix_Eta2p5to2p75_BDT.weights.xml",
#    "old_training_files/pileupJetId_80XvarFix_Eta2p75to3_BDT.weights.xml",
#    "old_training_files/pileupJetId_80XvarFix_Eta3to5_BDT.weights.xml",
#]

tmva_s_jetPt = array("f", [-999])
tmva_s_jetEta = array("f", [-999])

tmva_spectators = [
    ("jetPt", tmva_s_jetPt),
    ("jetEta", tmva_s_jetEta),
]

tmva_v_nvtx = array("f", [-999])
tmva_v_beta = array("f", [-999])
tmva_v_dR2Mean = array("f", [-999])
tmva_v_frac01 = array("f", [-999])
tmva_v_frac02 = array("f", [-999])
tmva_v_frac03 = array("f", [-999])
tmva_v_frac04 = array("f", [-999])
tmva_v_majW = array("f", [-999])
tmva_v_minW = array("f", [-999])
tmva_v_jetR = array("f", [-999])
tmva_v_jetRchg = array("f", [-999])
tmva_v_nParticles = array("f", [-999])
tmva_v_nCharged = array("f", [-999])
tmva_v_ptD = array("f", [-999])
tmva_v_pull = array("f", [-999])

tmva_variables = [
    ("nvtx" , tmva_v_nvtx),
    ("beta", tmva_v_beta),
    ("dR2Mean", tmva_v_dR2Mean),
    ("frac01", tmva_v_frac01),
    ("frac02", tmva_v_frac02),
    ("frac03", tmva_v_frac03),
    ("frac04", tmva_v_frac04),
    ("majW", tmva_v_majW),
    ("minW", tmva_v_minW),
    ("jetR", tmva_v_jetR),
    ("jetRchg", tmva_v_jetRchg),
    ("nParticles", tmva_v_nParticles),
    ("nCharged", tmva_v_nCharged),
    ("ptD", tmva_v_ptD),
    ("pull", tmva_v_pull),
]

# uncomment below for testing old training,
# and comment above ones

#tmva_variables = [
#    ("nvtx" , tmva_v_nvtx),
#    ("dR2Mean", tmva_v_dR2Mean),
#    ("nParticles", tmva_v_nParticles),
#    ("nCharged", tmva_v_nCharged),
#    ("majW", tmva_v_majW),
#    ("minW", tmva_v_minW),
#    ("frac01", tmva_v_frac01),
#    ("frac02", tmva_v_frac02),
#    ("frac03", tmva_v_frac03),
#    ("frac04", tmva_v_frac04),
#    ("ptD", tmva_v_ptD),
#    ("beta", tmva_v_beta),
#    ("pull", tmva_v_pull),
#    ("jetR", tmva_v_jetR),
#    ("jetRchg", tmva_v_jetRchg),
#]

tmva_readers = []

for i, eta_bin in enumerate(eta_bins):
    
    tmva_readers.append(ROOT.TMVA.Reader())
    
    for spec_name, spec_address in tmva_spectators:
        
        tmva_readers[i].AddSpectator(spec_name, spec_address)
    
    for var_name, var_address in tmva_variables:
        
        if eta_bin == "Eta3p0To5p0":
            if var_name == "beta": continue
            if var_name == "jetRchg": continue
            if var_name == "nCharged": continue
        tmva_readers[i].AddVariable(var_name, var_address)
    
    tmva_readers[i].BookMVA("BDT", tmva_weight_filenames[i])

# some helping functions
def dphi(phi1, phi2):
    dphi = phi1 - phi2
    Pi = ROOT.TMath.Pi()
    if dphi > Pi:
        dphi -= 2 * Pi
    elif dphi <= -Pi:
        dphi += 2 * Pi
    return dphi

# book histograms
class book_hist_dict:
    def __init__(self, xbins, xlow, xup, titleX, units="", name="", 
                 keys=["main"], keys_sub=["sub_category"]):
        self.xbins = xbins
        self.xlow = xlow
        self.xup = xup
        self.titleX = titleX
        self.units = units
        self.name = name
        self.keys = keys
        self.keys_sub = keys_sub
    
    def hist_1D(self):
        variable = ROOT.TH1F("", "", self.xbins, self.xlow, self.xup)
        bw = variable.GetBinWidth(1)
        
        titleX = self.titleX
        titleY = "Enteries/%s" % bw
        
        if self.units != "":
            titleX = self.titleX + " [" + self.units + "]"
            titleY = titleY + " " + self.units
        
        variable.SetTitle("%s;%s;%s" % (titleX, titleX, titleY))
        
        if self.name != "":
            variable.SetName(self.name)
        else:
            variable.SetName(self.titleX)
        
        return variable
    
    def clone(self):
        hist_dict = {}
        
        for key in self.keys:
            name_ = key + "_" + self.hist_1D().GetName()
            hist_dict[key] = self.hist_1D().Clone()
            hist_dict[key].SetName(name_)

            for key_sub in self.keys_sub:
                name = name_ + "_" + key_sub
                hist_dict[key + "_" + key_sub] = self.hist_1D().Clone()
                hist_dict[key + "_" + key_sub].SetName(name)
                
        return hist_dict

# keys for per event histograms
# should be just one element which is "mc" or "data", hardcoded
h_keys1 = [data_type]

h_nvtx = book_hist_dict(100, 0, 100, "nvtx", keys=h_keys1).clone()

h_z_mass = book_hist_dict(40, 70, 110, "Z_mass", keys=h_keys1).clone()
h_z_pt = book_hist_dict(60, 0, 300, "Z_pt", keys=h_keys1).clone()
h_z_phi = book_hist_dict(32, -3.2, 3.2, "Z_phi", keys=h_keys1).clone()
h_z_rapidity = book_hist_dict(30, -3.0, 3.0, "Z_rapidity", keys=h_keys1).clone()

h_lept_pt1 = book_hist_dict(50, 0, 250, "lept_pt1", keys=h_keys1).clone()
h_lept_pt2 = book_hist_dict(50, 0, 250, "lept_pt2", keys=h_keys1).clone()
h_lept_eta1 = book_hist_dict(60, -3.0, 3.0, "lept_eta1", keys=h_keys1).clone()
h_lept_eta2 = book_hist_dict(60, -3.0, 3.0, "lept_eta2", keys=h_keys1).clone()
h_lept_phi1 = book_hist_dict(64, -3.2, 3.2, "lept_phi1", keys=h_keys1).clone()
h_lept_phi2 = book_hist_dict(64, -3.2, 3.2, "lept_phi2", keys=h_keys1).clone()

h_dphi_zj = book_hist_dict(64, -3.2, 3.2, "dphi_zj", keys=h_keys1).clone()
h_n_jets = book_hist_dict(40, 0, 40, "n_jets", keys=h_keys1).clone()
    
# keys for per jet histograms
h_keys2 = eta_bins

h_keys3 = [
    eta_bin + "_" + pt_bin for eta_bin in eta_bins for pt_bin in pt_bins
]

if data_type == "mc":

    jet_tags = ["all", "prompt", "pileup", "rest"]

    h_keys2 = [
        i + "_" + j for i in h_keys2 for j in jet_tags
    ]

    h_keys3 = [
        i + "_" + j for i in h_keys3 for j in jet_tags
    ]

h_keys4 = h_keys2 + h_keys3

h_jet_pt = book_hist_dict(100, 0.0, 100.0, "jet_pt", units="GeV", keys=h_keys1, keys_sub=h_keys4).clone()
h_jet_eta = book_hist_dict(50, -5.0, 5.0, "jet_eta", keys=h_keys1, keys_sub=h_keys4).clone()
h_jet_energy = book_hist_dict(100, 0.0, 500.0, "jet_energy", units="GeV", keys=h_keys1, keys_sub=h_keys4).clone()
h_jet_phi = book_hist_dict(64, -3.2, 3.2, "jet_phi", keys=h_keys1, keys_sub=h_keys4).clone()
# min dR jet and genjet
if data_type == "mc":
    h_jet_dR = book_hist_dict(250, 0.0, 5.0, "jet_dR", keys=h_keys1, keys_sub=h_keys4).clone()
#chargedHadronEnergyFraction
h_jet_chf= book_hist_dict(52, -0.02, 1.02, "jet_chf", keys=h_keys1, keys_sub=h_keys4).clone()
#chargedEmEnergyFraction
h_jet_cemf = book_hist_dict(52, -0.02, 1.02, "jet_cemf", keys=h_keys1, keys_sub=h_keys4).clone()
#neutralHadronEnergyFraction
h_jet_nhf = book_hist_dict(52, -0.02, 1.02, "jet_nhf", keys=h_keys1, keys_sub=h_keys4).clone()
#neutralEmEnergyFraction
h_jet_nemf = book_hist_dict(52, -0.02, 1.02, "jet_nemf", keys=h_keys1, keys_sub=h_keys4).clone()
#photonEnergyFraction
h_jet_phf = book_hist_dict(52, -0.02, 1.02, "jet_phf", keys=h_keys1, keys_sub=h_keys4).clone()
#muonEnergyFraction
h_jet_muf = book_hist_dict(52, -0.02, 1.02, "jet_muf", keys=h_keys1, keys_sub=h_keys4).clone()
#electronEnergyFraction
h_jet_elf = book_hist_dict(52, -0.02, 1.02, "jet_elf", keys=h_keys1, keys_sub=h_keys4).clone()
#neutralMultiplicity
h_jet_npr = book_hist_dict(60, 0, 60, "jet_npr", keys=h_keys1, keys_sub=h_keys4).clone()
#chargedHadronMultiplicity
h_jet_chm = book_hist_dict(40, 0, 40, "jet_chm", keys=h_keys1, keys_sub=h_keys4).clone()
#neutralHadronMultiplicity
h_jet_nhm = book_hist_dict(10, 0, 10, "jet_nhm", keys=h_keys1, keys_sub=h_keys4).clone()
#photonMultiplicity
h_jet_phm = book_hist_dict(40, 0, 40, "jet_phm", keys=h_keys1, keys_sub=h_keys4).clone()
#muonMultiplicity
h_jet_mum = book_hist_dict(5, 0, 5, "jet_mum", keys=h_keys1, keys_sub=h_keys4).clone()
#electronMultiplicity
h_jet_elm = book_hist_dict(5, 0, 5, "jet_elm", keys=h_keys1, keys_sub=h_keys4).clone()
# ------------
# BDT variables
h_jet_beta = book_hist_dict(52, -0.02, 1.02, "beta", keys=h_keys1, keys_sub=h_keys4).clone()
h_dR2Mean = book_hist_dict(60, -0.01, 0.11, "dR2Mean", keys=h_keys1, keys_sub=h_keys4).clone()
h_frac01 = book_hist_dict(52, -0.02, 1.02, "frac01", keys=h_keys1, keys_sub=h_keys4).clone()
h_frac02 = book_hist_dict(52, -0.02, 1.02, "frac02", keys=h_keys1, keys_sub=h_keys4).clone()
h_frac03 = book_hist_dict(52, -0.02, 1.02, "frac03", keys=h_keys1, keys_sub=h_keys4).clone()
h_frac04 = book_hist_dict(52, -0.02, 1.02, "frac04", keys=h_keys1, keys_sub=h_keys4).clone()
h_jetRchg = book_hist_dict(52, -0.02, 1.02, "jetRchg", keys=h_keys1, keys_sub=h_keys4).clone()
h_jetR = book_hist_dict(52, -0.02, 1.02, "jetR", keys=h_keys1, keys_sub=h_keys4).clone()
h_majW = book_hist_dict(60, 0.0, 0.3, "majW", keys=h_keys1, keys_sub=h_keys4).clone()
h_minW = book_hist_dict(40, 0.0, 0.2, "minW", keys=h_keys1, keys_sub=h_keys4).clone()
h_nCharged = book_hist_dict(40, 0, 40, "nCharged", keys=h_keys1, keys_sub=h_keys4).clone()
h_nParticles = book_hist_dict(60, 0, 60, "nParticles", keys=h_keys1, keys_sub=h_keys4).clone()
h_ptD = book_hist_dict(50, 0.0, 1.0, "ptD", keys=h_keys1, keys_sub=h_keys4).clone()
h_pull = book_hist_dict(50, 0.0, 0.025, "pull", keys=h_keys1, keys_sub=h_keys4).clone()

h_old_mva = book_hist_dict(200, -1.0, 1.0, "old_mva", keys=h_keys1, keys_sub=h_keys4).clone()
h_new_mva = book_hist_dict(200, -1.0, 1.0, "new_mva", keys=h_keys1, keys_sub=h_keys4).clone()


control_wp_keys = [
    "pass_wp1", "fail_wp1", 
    "pass_wp2", "fail_wp2",
    "pass_wp3", "fail_wp3",
]

h_control_jet_pt = book_hist_dict(80, 20, 100, "control_jet_pt", keys=["tight", "loose"], keys_sub=control_wp_keys).clone()
h_control_jet_eta = book_hist_dict(50, -5.0, 5.0, "control_jet_eta", keys=["tight", "loose"], keys_sub=control_wp_keys).clone()

h_dphi_zj_ptj_z_ = ROOT.TH2F("dphi_zj_ptj_z", "dphi_zj_ptj_z", 64, -3.2, 3.2, 100, 0, 10)

if data_type == "mc":
    h_dphi_zj_ptj_z = {key: h_dphi_zj_ptj_z_.Clone(f"{key}_dphi_zj_ptj_z") for key in ["prompt", "pileup"]}

else:
    h_dphi_zj_ptj_z = {key: h_dphi_zj_ptj_z_.Clone(f"{key}_dphi_zj_ptj_z") for key in ["data"]}

    
def write_hists(k=""):
    # per event
    if k in h_nvtx: h_nvtx[k].Write()
    if k in h_z_mass: h_z_mass[k].Write()
    if k in h_z_pt: h_z_pt[k].Write()
    if k in h_z_phi: h_z_phi[k].Write()
    if k in h_z_rapidity: h_z_rapidity[k].Write()
    if k in h_lept_pt1: h_lept_pt1[k].Write()
    if k in h_lept_pt2: h_lept_pt2[k].Write()
    if k in h_lept_eta1: h_lept_eta1[k].Write()
    if k in h_lept_eta2: h_lept_eta2[k].Write()
    if k in h_lept_phi1: h_lept_phi1[k].Write()
    if k in h_lept_phi2: h_lept_phi2[k].Write()
    if k in h_dphi_zj: h_dphi_zj[k].Write()
    if k in h_n_jets: h_n_jets[k].Write()
    
    # per jet
    if k in h_jet_pt: h_jet_pt[k].Write()
    if k in h_jet_eta: h_jet_eta[k].Write()
    if k in h_jet_phi: h_jet_phi[k].Write()
    if k in h_jet_energy: h_jet_energy[k].Write()
    if data_type == "mc":
        if k in h_jet_dR: h_jet_dR[k].Write()
    if k in h_jet_chf: h_jet_chf[k].Write()
    if k in h_jet_cemf: h_jet_cemf[k].Write()
    if k in h_jet_nhf: h_jet_nhf[k].Write()
    if k in h_jet_nemf: h_jet_nemf[k].Write()
    if k in h_jet_phf: h_jet_phf[k].Write()
    if k in h_jet_muf: h_jet_muf[k].Write()
    if k in h_jet_elf: h_jet_elf[k].Write()
    if k in h_jet_npr: h_jet_npr[k].Write()
    if k in h_jet_chm: h_jet_chm[k].Write()
    if k in h_jet_nhm: h_jet_nhm[k].Write()
    if k in h_jet_phm: h_jet_phm[k].Write()
    if k in h_jet_mum: h_jet_mum[k].Write()
    if k in h_jet_elm: h_jet_elm[k].Write()
    if k in h_jet_beta: h_jet_beta[k].Write()
    if k in h_dR2Mean: h_dR2Mean[k].Write()
    if k in h_frac01: h_frac01[k].Write()
    if k in h_frac02: h_frac02[k].Write()
    if k in h_frac03: h_frac03[k].Write()
    if k in h_frac04: h_frac04[k].Write()
    if k in h_jetRchg: h_jetRchg[k].Write()
    if k in h_jetR: h_jetR[k].Write()
    if k in h_majW: h_majW[k].Write()
    if k in h_minW: h_minW[k].Write()
    if k in h_nCharged: h_nCharged[k].Write()
    if k in h_nParticles: h_nParticles[k].Write()
    if k in h_ptD: h_ptD[k].Write()
    if k in h_pull: h_pull[k].Write()
    if k in h_old_mva: h_old_mva[k].Write()
    if k in h_new_mva: h_new_mva[k].Write()

    return 0


# pileup weight

f_pu_weights = ROOT.TFile.Open(f"pu_weights_{year}.root")
h_pu_weights = f_pu_weights.Get("weights")

def process_event(e):
    
    weight = 1.0
    if data_type == "mc":
        weight = weight * xs_weight

    gen_weight = 1.0
    pu_weight = 1.0

    if data_type == "mc":

        if e.genEvtWeight_ < 0:
            gen_weight = -1.0

        npu = e.npu_
        pu_weight = h_pu_weights.GetBinContent(npu)

        
    weight = weight * gen_weight * pu_weight

    nvtx = e.nVtx_

    lept_pt1 = e.lepPt[0]
    lept_eta1 = e.lepEta[0]
    lept_phi1 = e.lepPhi[0]

    lept_pt2 = e.lepPt[1]
    lept_eta2 = e.lepEta[1]
    lept_phi2 = e.lepPhi[1]

    z_mass = e.llMass
    z_pt = e.llPt
    z_phi = e.llPhi
    z_rapidity = e.llRapidity

    n_jets = len(e.jetPt)
    assert (n_jets == e.nJets)

    dphi_zj = dphi(z_phi, e.phi[0])

    def fill_hist_per_event(k=""):
        h_nvtx[k].Fill(nvtx, weight)

        h_z_mass[k].Fill(z_mass, weight)
        h_z_pt[k].Fill(z_pt, weight)
        h_z_phi[k].Fill(z_phi, weight)
        h_z_rapidity[k].Fill(z_rapidity, weight)

        h_lept_pt1[k].Fill(lept_pt1, weight)
        h_lept_pt2[k].Fill(lept_pt2, weight)
        h_lept_eta1[k].Fill(lept_eta1, weight)
        h_lept_eta2[k].Fill(lept_eta2, weight)
        h_lept_phi1[k].Fill(lept_phi1, weight)
        h_lept_phi2[k].Fill(lept_phi2, weight)

        h_dphi_zj[k].Fill(dphi_zj, weight)
        h_n_jets[k].Fill(n_jets, weight)

        return 0

    e_new_mva = []

    for i in range(n_jets):

        jet_pt = e.jetPt[i]
        jet_eta = e.jetEta[i]
        jet_phi = e.phi[i]
        jet_mass = e.mass[i]
        jet_energy = e.energy[i]

        jet_chf = e.chf[i]
        jet_cemf = e.cemf[i]
        jet_nemf = e.nemf[i]
        jet_nhf = e.nhf[i]
        jet_phf = e.phf[i]
        jet_muf = e.muf[i]
        jet_elf = e.elf[i]

        jet_npr = e.npr[i]
        jet_chm = e.chm[i]
        jet_nhm = e.nhm[i]
        jet_phm = e.phm[i]
        jet_mum = e.mum[i]
        jet_elm = e.elm[i]

        if data_type == "mc":
            jet_dR = e.dRMatch[i]
            jet_flavor = e.jetFlavorParton[i]

        tmva_s_jetPt[0] = jet_pt
        tmva_s_jetEta[0] = jet_eta

        tmva_v_nvtx[0] = nvtx
        tmva_v_beta[0] = e.beta[i]
        tmva_v_dR2Mean[0] = e.dR2Mean[i]
        tmva_v_frac01[0] = e.frac01[i]
        tmva_v_frac02[0] = e.frac02[i]
        tmva_v_frac03[0] = e.frac03[i]
        tmva_v_frac04[0] = e.frac04[i]
        tmva_v_majW[0] = e.majW[i]
        tmva_v_minW[0] = e.minW[i]
        tmva_v_jetR[0] = e.jetR[i]
        tmva_v_jetRchg[0] = e.jetRchg[i]
        tmva_v_nParticles[0] = e.nParticles[i]
        tmva_v_nCharged[0] = e.nCharged[i]
        tmva_v_ptD[0] = e.ptD[i]
        tmva_v_pull[0] = e.pull[i]

        old_mva = e.pumva[i]
        new_mva = "something"

        for i, f_eta in enumerate(f_eta_bins):

            if abs(jet_eta) > f_eta[0] and abs(jet_eta) <= f_eta[1]:

                new_mva = tmva_readers[i].EvaluateMVA("BDT")

        assert (new_mva != "something")

        e_new_mva.append(new_mva)

        def fill_hist_per_jet(k=""):
            h_jet_pt[k].Fill(jet_pt, weight)
            h_jet_eta[k].Fill(jet_eta, weight)
            h_jet_phi[k].Fill(jet_phi, weight)
            h_jet_energy[k].Fill(jet_energy, weight)

            if data_type == "mc": h_jet_dR[k].Fill(jet_dR, weight)

            h_jet_chf[k].Fill(jet_chf, weight)
            h_jet_cemf[k].Fill(jet_cemf, weight)
            h_jet_nhf[k].Fill(jet_nhf, weight)
            h_jet_nemf[k].Fill(jet_nemf, weight)
            h_jet_phf[k].Fill(jet_phf, weight)
            h_jet_muf[k].Fill(jet_muf, weight)
            h_jet_elf[k].Fill(jet_elf, weight)
            h_jet_npr[k].Fill(jet_npr, weight)
            h_jet_chm[k].Fill(jet_chm, weight)
            h_jet_nhm[k].Fill(jet_nhm, weight)
            h_jet_phm[k].Fill(jet_phm, weight)
            h_jet_mum[k].Fill(jet_mum, weight)
            h_jet_elm[k].Fill(jet_elm, weight)

            h_jet_beta[k].Fill(tmva_v_beta[0], weight)
            h_dR2Mean[k].Fill(tmva_v_dR2Mean[0], weight)
            h_frac01[k].Fill(tmva_v_frac01[0], weight)
            h_frac02[k].Fill(tmva_v_frac02[0], weight)
            h_frac03[k].Fill(tmva_v_frac03[0], weight)
            h_frac04[k].Fill(tmva_v_frac04[0], weight)
            h_jetRchg[k].Fill(tmva_v_jetRchg[0], weight)
            h_jetR[k].Fill(tmva_v_jetR[0], weight)
            h_majW[k].Fill(tmva_v_majW[0], weight)
            h_minW[k].Fill(tmva_v_minW[0], weight)
            h_nCharged[k].Fill(tmva_v_nCharged[0], weight)
            h_nParticles[k].Fill(tmva_v_nParticles[0], weight)
            h_ptD[k].Fill(tmva_v_ptD[0], weight)
            h_pull[k].Fill(tmva_v_pull[0], weight)

            h_old_mva[k].Fill(old_mva, weight)
            h_new_mva[k].Fill(new_mva, weight)

            return 0

        fill_hist_per_jet(k=h_keys1[0])

        if data_type =="mc":
            if jet_dR < 0.2:
                jet_type = "prompt"

            elif jet_dR > 0.4 and abs(jet_flavor) == 0:
                jet_type = "pileup"

            else:
                jet_type = "rest"

        for i, f_eta in enumerate(f_eta_bins):

            if abs(jet_eta) > f_eta[0] and abs(jet_eta) <= f_eta[1]:
                key_eta = eta_bins[i]

                if data_type == "mc":
                    k1 = "%s_%s_%s" % (h_keys1[0], key_eta, "all")
                    k2 = "%s_%s_%s" % (h_keys1[0], key_eta, jet_type)
                    fill_hist_per_jet(k1)
                    fill_hist_per_jet(k2)

                if data_type == "data":
                    k1 = "%s_%s" % (h_keys1[0], key_eta)
                    fill_hist_per_jet(k1)


                for j, f_pt in enumerate(f_pt_bins):

                    if jet_pt > f_pt[0] and jet_pt <= f_pt[1]:
                        key_pt = pt_bins[j]

                        if data_type == "mc":
                            k1 = "%s_%s_%s_%s" % (h_keys1[0], key_eta, key_pt, "all")
                            k2 = "%s_%s_%s_%s" % (h_keys1[0], key_eta, key_pt, jet_type)
                            fill_hist_per_jet(k1)
                            fill_hist_per_jet(k2)

                        if data_type == "data":
                            k1 = "%s_%s_%s" % (h_keys1[0], key_eta, key_pt)
                            fill_hist_per_jet(k1)


    if data_type == "mc":
        if e.dRMatch[0] < 0.2:
            h_dphi_zj_ptj_z["prompt"].Fill(dphi_zj, float(e.jetPt[0]/e.llPt), weight)

        elif e.dRMatch[0] > 0.4 and abs(e.jetFlavorParton[0]) == 0:
            h_dphi_zj_ptj_z["pileup"].Fill(dphi_zj, float(e.jetPt[0]/e.llPt), weight)

    elif data_type == "data":
        h_dphi_zj_ptj_z["data"].Fill(dphi_zj, float(e.jetPt[0]/e.llPt), weight)

    fill_hist_per_event(k=h_keys1[0])

    for i in range(n_jets):

        pt_zj_ratio = e.jetPt[0]/e.llPt

        if (abs(dphi_zj) > 2.5) and (pt_zj_ratio > 0.5) and (pt_zj_ratio < 1.5):

            key = "tight"

            if e_new_mva[i] > mva_wp1:
                h_control_jet_pt[f"{key}_pass_wp1"].Fill(e.jetPt[i], weight)
                h_control_jet_eta[f"{key}_pass_wp1"].Fill(e.jetEta[i], weight)

            else:
                h_control_jet_pt[f"{key}_fail_wp1"].Fill(e.jetPt[i], weight)
                h_control_jet_eta[f"{key}_fail_wp1"].Fill(e.jetEta[i], weight)

            if e_new_mva[i] > mva_wp2:
                h_control_jet_pt[f"{key}_pass_wp2"].Fill(e.jetPt[i], weight)
                h_control_jet_eta[f"{key}_pass_wp2"].Fill(e.jetEta[i], weight)

            else:
                h_control_jet_pt[f"{key}_fail_wp2"].Fill(e.jetPt[i], weight)
                h_control_jet_eta[f"{key}_fail_wp2"].Fill(e.jetEta[i], weight)

            if e_new_mva[i] > mva_wp3:
                h_control_jet_pt[f"{key}_pass_wp3"].Fill(e.jetPt[i], weight)
                h_control_jet_eta[f"{key}_pass_wp3"].Fill(e.jetEta[i], weight)

            else:
                h_control_jet_pt[f"{key}_fail_wp3"].Fill(e.jetPt[i], weight)
                h_control_jet_eta[f"{key}_fail_wp3"].Fill(e.jetEta[i], weight)

        if abs(dphi_zj) < 1.5:

            key = "loose"

            if e_new_mva[i] > mva_wp1:
                h_control_jet_pt[f"{key}_pass_wp1"].Fill(e.jetPt[i], weight)
                h_control_jet_eta[f"{key}_pass_wp1"].Fill(e.jetEta[i], weight)

            else:
                h_control_jet_pt[f"{key}_fail_wp1"].Fill(e.jetPt[i], weight)
                h_control_jet_eta[f"{key}_fail_wp1"].Fill(e.jetEta[i], weight)

            if e_new_mva[i] > mva_wp2:
                h_control_jet_pt[f"{key}_pass_wp2"].Fill(e.jetPt[i], weight)
                h_control_jet_eta[f"{key}_pass_wp2"].Fill(e.jetEta[i], weight)

            else:
                h_control_jet_pt[f"{key}_fail_wp2"].Fill(e.jetPt[i], weight)
                h_control_jet_eta[f"{key}_fail_wp2"].Fill(e.jetEta[i], weight)

            if e_new_mva[i] > mva_wp3:
                h_control_jet_pt[f"{key}_pass_wp3"].Fill(e.jetPt[i], weight)
                h_control_jet_eta[f"{key}_pass_wp3"].Fill(e.jetEta[i], weight)

            else:
                h_control_jet_pt[f"{key}_fail_wp3"].Fill(e.jetPt[i], weight)
                h_control_jet_eta[f"{key}_fail_wp3"].Fill(e.jetEta[i], weight)


total_events = events.GetEntries()

mva_wp1 = -0.21
mva_wp2 = 0.65
mva_wp3 = 0.98

for i, event in enumerate(events):

    if i%1000 == 0:
        print("processing event:   %s/%s" % (i, total_events))

    process_event(event)
    
# output file for histograms
output_file = ROOT.TFile(output_filename, "RECREATE")

write_hists(h_keys1[0])

for k in h_keys4:
    write_hists(h_keys1[0] + "_" + k)

for k in ["data", "prompt", "pileup"]:
    if k in h_dphi_zj_ptj_z:
        h_dphi_zj_ptj_z[k].Write()
        
for k in ["tight", "loose"]:
    
    for j in control_wp_keys:
        k_ = k + "_" + j
        
        if k_ in h_control_jet_pt:
            h_control_jet_pt[k_].Write()
        if k_ in h_control_jet_eta:
            h_control_jet_eta[k_].Write()


output_file.cd()
output_file.Write()
output_file.Close()
