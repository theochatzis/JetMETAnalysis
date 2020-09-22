#!/usr/bin/env python
import os
import sys
import argparse
import ROOT

from common.utils import *
from common.th1 import *
from common.efficiency import *
from common.plot import *
from common.plot_style import *

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

def getRateHistogram(h1):
   theRateHisto = h1.Clone()

   rateFac = 30.903 * 1e3 / h1.GetEntries()

   theRateHisto_name = h1.GetName()+'_rate'
   theRateHisto.SetTitle(theRateHisto_name)
   theRateHisto.SetName(theRateHisto_name)
   theRateHisto.SetDirectory(0)
   theRateHisto.UseCurrentStyle()

   for _tmp_bin_i in range(1, 1+h1.GetNbinsX()):
      _err = ctypes.c_double(0.)
      theRateHisto.SetBinContent(_tmp_bin_i, h1.IntegralAndError(_tmp_bin_i, -1, _err))
      theRateHisto.SetBinError(_tmp_bin_i, _err.value)

   theRateHisto.Scale(rateFac)

   return theRateHisto

apply_style(0)

file0 = ROOT.TFile.Open(sys.argv[1])
file1 = ROOT.TFile.Open(sys.argv[2])

for puTag in ['']:

    for regTag in ['']:

        h0 = file0.Get('l1tPFMET_pt')
        h1 = file0.Get('l1tPFMET_pt')
        h2 = file0.Get('l1tPFPuppiMET_pt')

        h00 = getRateHistogram(h0)
        h01 = getRateHistogram(h1)
        h02 = getRateHistogram(h2)

        h00.SetLineColor(1)
        h01.SetLineColor(2)
        h02.SetLineColor(4)

        h00.SetLineStyle(1)
        h01.SetLineStyle(1)
        h02.SetLineStyle(1)
    
        h00.SetLineWidth(2)
        h01.SetLineWidth(2)
        h02.SetLineWidth(2)

        h00.SetMarkerSize(0)
        h01.SetMarkerSize(0)
        h02.SetMarkerSize(0)

        canv = ROOT.TCanvas()

#       canv.SetRightMargin(0.05)
#       canv.SetLeftMargin(0.12)

        canv.cd()
        canv.SetLogy()

        h00.Draw('hist,e0')
#       h01.Draw('hist,e0,same')
        h02.Draw('hist,e0,same')

        h00.SetTitle(';L1T MET Threshold [GeV];Rate [kHz]')
        h00.GetYaxis().SetRangeUser(0.01, 1e5)

        leg = ROOT.TLegend(0.65, 0.70, 0.95, 0.90)
        leg.SetNColumns(1)
        leg.AddEntry(h00, 'L1T MET PF', 'le')
#       leg.AddEntry(h01, 'L1T MET PF', 'le')
        leg.AddEntry(h02, 'L1T MET PF+Puppi', 'le')
        leg.Draw('same')

        l1tPFPuppiMET_tdrRate = ROOT.TLine(0, 18, 500, 18)
        l1tPFPuppiMET_tdrRate.SetLineWidth(2)
        l1tPFPuppiMET_tdrRate.SetLineStyle(2)
        l1tPFPuppiMET_tdrRate.SetLineColor(ROOT.kBlue-1)
        l1tPFPuppiMET_tdrRate.Draw('same')

        l1tPFPuppiMET_tdrRateTxt = ROOT.TPaveText(0.175, 0.42, 0.325, 0.52, 'NDC')
        l1tPFPuppiMET_tdrRateTxt.SetTextSize(0.035)
        l1tPFPuppiMET_tdrRateTxt.SetFillColor(0)
        l1tPFPuppiMET_tdrRateTxt.SetFillStyle(3000)
        l1tPFPuppiMET_tdrRateTxt.SetTextColor(ROOT.kBlue-1)
        l1tPFPuppiMET_tdrRateTxt.SetTextFont(42)
        l1tPFPuppiMET_tdrRateTxt.AddText('[18 kHz]')
        l1tPFPuppiMET_tdrRateTxt.Draw('same')

        l1tPFPuppiMET_thresh = ROOT.TLine(136, 0.01, 136, 18)
        l1tPFPuppiMET_thresh.SetLineWidth(2)
        l1tPFPuppiMET_thresh.SetLineStyle(2)
        l1tPFPuppiMET_thresh.SetLineColor(ROOT.kBlue-1)
        l1tPFPuppiMET_thresh.Draw('same')

        mcSampleTxt = ROOT.TPaveText(0.10, 0.92, 0.65, 0.99, 'NDC')
        mcSampleTxt.SetTextSize(0.035)
        mcSampleTxt.SetFillColor(0)
        mcSampleTxt.SetFillStyle(3000)
        mcSampleTxt.SetTextColor(ROOT.kBlack)
        mcSampleTxt.SetTextFont(42)
        mcSampleTxt.AddText('MinBias PU200 [11_1_X]')
        mcSampleTxt.Draw('same')

        canv.SaveAs('tmp.pdf')
        canv.Close()














        h0 = file0.Get('hltPFMET_pt')
        h1 = file0.Get('hltPFPuppiMET_pt')
        h2 = file0.Get('offlinePFMET_Raw_pt')
        h3 = file0.Get('offlinePFPuppiMET_Raw_pt')
        h4 = file0.Get('offlinePFPuppiMET_Type1_pt')

        h00 = getRateHistogram(h0)
        h01 = getRateHistogram(h1)
        h02 = getRateHistogram(h2)
        h03 = getRateHistogram(h3)
        h04 = getRateHistogram(h4)

        h00.SetLineColor(1)
        h01.SetLineColor(4)
        h02.SetLineColor(2)
        h03.SetLineColor(ROOT.kViolet)
        h04.SetLineColor(ROOT.kOrange)

        h00.SetLineStyle(1)
        h01.SetLineStyle(1)
        h02.SetLineStyle(1)
        h03.SetLineStyle(1)
        h04.SetLineStyle(1)

        h00.SetLineWidth(2)
        h01.SetLineWidth(2)
        h02.SetLineWidth(2)
        h03.SetLineWidth(2)
        h04.SetLineWidth(2)

        h00.SetMarkerSize(0)
        h01.SetMarkerSize(0)
        h02.SetMarkerSize(0)
        h03.SetMarkerSize(0)
        h04.SetMarkerSize(0)

        canv = ROOT.TCanvas()

#       canv.SetRightMargin(0.05)
#       canv.SetLeftMargin(0.12)

        canv.cd()
        canv.SetLogy()

        h00.Draw('hist,e0')
        h01.Draw('hist,e0,same')
        h02.Draw('hist,e0,same')
        h03.Draw('hist,e0,same')
        h04.Draw('hist,e0,same')

        h00.SetTitle(';HLT/Offline MET Threshold [GeV];Rate [kHz]')
        h00.GetYaxis().SetRangeUser(0.01, 1e5)

        leg = ROOT.TLegend(0.65, 0.55, 0.95, 0.90)
        leg.SetNColumns(1)
        leg.AddEntry(h00, 'HLT MET PF', 'le')
        leg.AddEntry(h01, 'HLT MET PF+Puppi', 'le')
        leg.AddEntry(h02, 'Offl MET PF', 'le')
        leg.AddEntry(h03, 'Offl MET PF+Puppi', 'le')
        leg.AddEntry(h04, 'Offl MET PF+Puppi (Type-1)', 'le')
        leg.Draw('same')

#        l1tPFPuppiMET_tdrRate = ROOT.TLine(0, 18, 500, 18)
#        l1tPFPuppiMET_tdrRate.SetLineWidth(2)
#        l1tPFPuppiMET_tdrRate.SetLineStyle(2)
#        l1tPFPuppiMET_tdrRate.SetLineColor(ROOT.kBlue-1)
#        l1tPFPuppiMET_tdrRate.Draw('same')
#
#        l1tPFPuppiMET_tdrRateTxt = ROOT.TPaveText(0.175, 0.42, 0.325, 0.52, 'NDC')
#        l1tPFPuppiMET_tdrRateTxt.SetTextSize(0.035)
#        l1tPFPuppiMET_tdrRateTxt.SetFillColor(0)
#        l1tPFPuppiMET_tdrRateTxt.SetFillStyle(3000)
#        l1tPFPuppiMET_tdrRateTxt.SetTextColor(ROOT.kBlue-1)
#        l1tPFPuppiMET_tdrRateTxt.SetTextFont(42)
#        l1tPFPuppiMET_tdrRateTxt.AddText('[18 kHz]')
#        l1tPFPuppiMET_tdrRateTxt.Draw('same')
#
#        l1tPFPuppiMET_thresh = ROOT.TLine(136, 0.01, 136, 18)
#        l1tPFPuppiMET_thresh.SetLineWidth(2)
#        l1tPFPuppiMET_thresh.SetLineStyle(2)
#        l1tPFPuppiMET_thresh.SetLineColor(ROOT.kBlue-1)
#        l1tPFPuppiMET_thresh.Draw('same')

        mcSampleTxt = ROOT.TPaveText(0.10, 0.92, 0.65, 0.99, 'NDC')
        mcSampleTxt.SetTextSize(0.035)
        mcSampleTxt.SetFillColor(0)
        mcSampleTxt.SetFillStyle(3000)
        mcSampleTxt.SetTextColor(ROOT.kBlack)
        mcSampleTxt.SetTextFont(42)
        mcSampleTxt.AddText('MinBias PU200 [11_1_X]')
        mcSampleTxt.Draw('same')

        canv.SaveAs('tmp2.pdf')
        canv.Close()












#        h0 = file0.Get('l1tPFPuppiMET_pt__hltPFPuppiMET_pt')
#
#        eff_den = h0.ProjectionY('den', 0, -1)
#        eff_num = h0.ProjectionY('num', h0.GetXaxis().FindBin(136.1), -1)
#
#        met_binning = [0, 30, 60, 90, 100, 110, 120, 130, 140,150,160,170,180,200,220,240,260,280,300,340,380,440,500]
#
#        eff_den2 = get_rebinned_histo(eff_den, met_binning)
#        eff_num2 = get_rebinned_histo(eff_num, met_binning)
#
#        geff = get_efficiency_graph(eff_num2, eff_den2)
#
#        geff.SetLineColor(4)
#        geff.SetLineStyle(1)
#        geff.SetLineWidth(2)
#        geff.SetMarkerSize(0.5)
#
#        canv = ROOT.TCanvas()
#
##       canv.SetRightMargin(0.05)
##       canv.SetLeftMargin(0.12)
#
#        canv.cd()
#
#        geff.Draw('alp')
#
#        geff.SetTitle(';Offline PF+Puppi MET (Raw) [GeV];Efficiency')
##        geff.GetYaxis().SetRangeUser(0.01, 1e5)
#
##        leg = ROOT.TLegend(0.65, 0.70, 0.95, 0.90)
##        leg.SetNColumns(1)
##        leg.AddEntry(h00, 'L1T MET PF', 'le')
###       leg.AddEntry(h01, 'L1T MET PF', 'le')
##        leg.AddEntry(h02, 'L1T MET PF+Puppi', 'le')
##        leg.Draw('same')
##
##        l1tPFPuppiMET_tdrRate = ROOT.TLine(0, 18, 500, 18)
##        l1tPFPuppiMET_tdrRate.SetLineWidth(2)
##        l1tPFPuppiMET_tdrRate.SetLineStyle(2)
##        l1tPFPuppiMET_tdrRate.SetLineColor(ROOT.kBlue-1)
##        l1tPFPuppiMET_tdrRate.Draw('same')
##
##        l1tPFPuppiMET_tdrRateTxt = ROOT.TPaveText(0.175, 0.42, 0.325, 0.52, 'NDC')
##        l1tPFPuppiMET_tdrRateTxt.SetTextSize(0.035)
##        l1tPFPuppiMET_tdrRateTxt.SetFillColor(0)
##        l1tPFPuppiMET_tdrRateTxt.SetFillStyle(3000)
##        l1tPFPuppiMET_tdrRateTxt.SetTextColor(ROOT.kBlue-1)
##        l1tPFPuppiMET_tdrRateTxt.SetTextFont(42)
##        l1tPFPuppiMET_tdrRateTxt.AddText('[18 kHz]')
##        l1tPFPuppiMET_tdrRateTxt.Draw('same')
##
##        l1tPFPuppiMET_thresh = ROOT.TLine(136, 0.01, 136, 18)
##        l1tPFPuppiMET_thresh.SetLineWidth(2)
##        l1tPFPuppiMET_thresh.SetLineStyle(2)
##        l1tPFPuppiMET_thresh.SetLineColor(ROOT.kBlue-1)
##        l1tPFPuppiMET_thresh.Draw('same')
#
#        canv.SaveAs('tmp2.pdf')
#        canv.Close()

        h0 = file1.Get('NoSelection/l1tAK4PFJetsCorrected_Eta2p4_HT')
        h2 = file1.Get('NoSelection/l1tAK4PFPuppiJetsCorrected_Eta2p4_HT')

        h00 = getRateHistogram(h0)
        h02 = getRateHistogram(h2)

        h00.SetLineColor(1)
        h02.SetLineColor(4)

        h00.SetLineStyle(1)
        h02.SetLineStyle(1)
    
        h00.SetLineWidth(2)
        h02.SetLineWidth(2)

        h00.SetMarkerSize(0)
        h02.SetMarkerSize(0)

        canv = ROOT.TCanvas()

#       canv.SetRightMargin(0.05)
#       canv.SetLeftMargin(0.12)

        canv.cd()
        canv.SetLogy()

        h00.Draw('hist,e0')
        h02.Draw('hist,e0,same')

        h00.SetTitle(';L1T H_{T} Threshold [GeV];Rate [kHz]')
        h00.GetYaxis().SetRangeUser(0.01, 1e5)

        leg = ROOT.TLegend(0.65, 0.70, 0.95, 0.90)
        leg.SetNColumns(1)
        leg.AddEntry(h00, 'L1T H_{T}(Jets) PF', 'le')
        leg.AddEntry(h02, 'L1T H_{T}(Jets) PF+Puppi', 'le')
        leg.Draw('same')

#        l1tPFPuppiMET_tdrRate = ROOT.TLine(0, 18, 500, 18)
#        l1tPFPuppiMET_tdrRate.SetLineWidth(2)
#        l1tPFPuppiMET_tdrRate.SetLineStyle(2)
#        l1tPFPuppiMET_tdrRate.SetLineColor(ROOT.kBlue-1)
#        l1tPFPuppiMET_tdrRate.Draw('same')
#
#        l1tPFPuppiMET_tdrRateTxt = ROOT.TPaveText(0.175, 0.42, 0.325, 0.52, 'NDC')
#        l1tPFPuppiMET_tdrRateTxt.SetTextSize(0.035)
#        l1tPFPuppiMET_tdrRateTxt.SetFillColor(0)
#        l1tPFPuppiMET_tdrRateTxt.SetFillStyle(3000)
#        l1tPFPuppiMET_tdrRateTxt.SetTextColor(ROOT.kBlue-1)
#        l1tPFPuppiMET_tdrRateTxt.SetTextFont(42)
#        l1tPFPuppiMET_tdrRateTxt.AddText('[18 kHz]')
#        l1tPFPuppiMET_tdrRateTxt.Draw('same')
#
#        l1tPFPuppiMET_thresh = ROOT.TLine(136, 0.01, 136, 18)
#        l1tPFPuppiMET_thresh.SetLineWidth(2)
#        l1tPFPuppiMET_thresh.SetLineStyle(2)
#        l1tPFPuppiMET_thresh.SetLineColor(ROOT.kBlue-1)
#        l1tPFPuppiMET_thresh.Draw('same')

        mcSampleTxt = ROOT.TPaveText(0.10, 0.92, 0.65, 0.99, 'NDC')
        mcSampleTxt.SetTextSize(0.035)
        mcSampleTxt.SetFillColor(0)
        mcSampleTxt.SetFillStyle(3000)
        mcSampleTxt.SetTextColor(ROOT.kBlack)
        mcSampleTxt.SetTextFont(42)
        mcSampleTxt.AddText('MinBias PU200 [11_1_X]')
        mcSampleTxt.Draw('same')

        canv.SaveAs('tmp3.pdf')
        canv.Close()




file0.Close()
