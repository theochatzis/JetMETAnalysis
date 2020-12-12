#!/usr/bin/env python
import os
import sys
import argparse
import ROOT
import math

from common.utils import *
from common.th1 import *
from common.efficiency import *
from common.plot import *
from common.plot_style import *

L1T_SingleJet = 'L1T_SinglePFPuppiJet200off'
L1T_HT = 'L1T_PFPuppiHT450off'

COUNTER = 0
def tmpName(increment=True):
  global COUNTER
  COUNTER += 1
  return 'tmp'+str(COUNTER)

def getRateFactor(processName):
  if   processName == 'MinBias_14TeV'             : return 1e6 * 30. # 30.903 (L1T TDR)
  elif processName == 'QCD_Pt020to030_14TeV'      : return 0.075 * 436000000.0
  elif processName == 'QCD_Pt030to050_14TeV'      : return 0.075 * 118400000.0
  elif processName == 'QCD_Pt050to080_14TeV'      : return 0.075 *  17650000.0
  elif processName == 'QCD_Pt080to120_14TeV'      : return 0.075 *   2671000.0
  elif processName == 'QCD_Pt120to170_14TeV'      : return 0.075 *    469700.0
  elif processName == 'QCD_Pt170to300_14TeV'      : return 0.075 *    121700.0
  elif processName == 'QCD_Pt300to470_14TeV'      : return 0.075 *      8251.0
  elif processName == 'QCD_Pt470to600_14TeV'      : return 0.075 *       686.4
  elif processName == 'QCD_Pt600toInf_14TeV'      : return 0.075 *       244.8
  elif processName == 'WJetsToLNu_14TeV'          : return 0.075 *     56990.0
  elif processName == 'DYJetsToLL_M010to050_14TeV': return 0.075 *     16880.0
  elif processName == 'DYJetsToLL_M050toInf_14TeV': return 0.075 *      5795.0
  else:
    raise RuntimeError(processName)

def getHistogram(tfile, key):
  h0 = tfile.Get(key)
  if not h0:
    return None

  hret = h0.Clone()
  hret.SetDirectory(0)
  hret.UseCurrentStyle()

  return hret

def getRateHistogram(h1, rateFac):
  theRateHisto = h1.Clone()

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

def getRates(fpath, processName, hltThreshold_SingleJet, hltThreshold_HT, hltThreshold_MET, hltThreshold_MET2):
  global L1T_SingleJet, L1T_HT

  ret = {}

  _tfile = ROOT.TFile.Open(fpath)
  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)

  _eventsProcessed = _tfile.Get('eventsProcessed')
  ret['v_eventsProcessed'] = _eventsProcessed.GetEntries()

  rateFactor = getRateFactor(processName) / ret['v_eventsProcessed']

  ret['t_rates'] = {}
  ret['v_rates'] = {}
  ret['v_counts'] = {}

  # SingleJet
  ret['t_rates']['l1tSlwPFPuppiJet'] = getRateHistogram(_tfile.Get('NoSelection/l1tSlwPFPuppiJetsCorrected_EtaIncl_pt0'), rateFactor)

  ret['t_rates']['hltAK4PFPuppiJet_woL1T'] = getRateHistogram(_tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_pt0'), rateFactor)
  ret['t_rates']['hltAK4PFPuppiJet'] = getRateHistogram(_tfile.Get(L1T_SingleJet+'/hltAK4PFPuppiJetsCorrected_EtaIncl_pt0'), rateFactor)

  _tmp = _tfile.Get(L1T_SingleJet+'/l1tSlwPFPuppiJetsCorrected_EtaIncl_pt0')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp_integErr)
  ret['v_rates'] [L1T_SingleJet] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts'][L1T_SingleJet] = [_tmp_integ, _tmp_integErr.value]

  _tmp = _tfile.Get(L1T_SingleJet+'/hltAK4PFPuppiJetsCorrected_EtaIncl_pt0')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(_tmp.GetXaxis().FindBin(float(hltThreshold_SingleJet)), -1, _tmp_integErr)
  ret['v_rates'] ['HLT_AK4PFPuppiJet'+str(hltThreshold_SingleJet)] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts']['HLT_AK4PFPuppiJet'+str(hltThreshold_SingleJet)] = [_tmp_integ, _tmp_integErr.value]

  # HT
  ret['t_rates']['l1tPFPuppiHT'] = getRateHistogram(_tfile.Get('NoSelection/l1tPFPuppiHT_sumEt'), rateFactor)
  ret['t_rates']['l1tPFPuppiHT_2'] = getRateHistogram(_tfile.Get('NoSelection/l1tSlwPFPuppiJetsCorrected_Eta2p4_HT'), rateFactor)

  ret['t_rates']['hltPFPuppiHT_woL1T'] = getRateHistogram(_tfile.Get('NoSelection/hltPFPuppiHT_sumEt'), rateFactor)
  ret['t_rates']['hltPFPuppiHT'] = getRateHistogram(_tfile.Get(L1T_HT+'/hltPFPuppiHT_sumEt'), rateFactor)

  _tmp = _tfile.Get(L1T_HT+'/l1tPFPuppiHT_sumEt')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp_integErr)
  ret['v_rates'] [L1T_HT] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts'][L1T_HT] = [_tmp_integ, _tmp_integErr.value]

  _tmp = _tfile.Get(L1T_HT+'/hltPFPuppiHT_sumEt')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(_tmp.GetXaxis().FindBin(float(hltThreshold_HT)), -1, _tmp_integErr)
  ret['v_rates'] ['HLT_PFPuppiHT'+str(hltThreshold_HT)] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts']['HLT_PFPuppiHT'+str(hltThreshold_HT)] = [_tmp_integ, _tmp_integErr.value]

  # MET
  ret['t_rates']['l1tPFPuppiMET'] = getRateHistogram(_tfile.Get('NoSelection/l1tPFPuppiMET_pt'), rateFactor)

  ret['t_rates']['hltPFPuppiMET_woL1T'] = getRateHistogram(_tfile.Get('NoSelection/hltPFPuppiHT_sumEt'), rateFactor)
  ret['t_rates']['hltPFPuppiMET'] = getRateHistogram(_tfile.Get('L1T_PFPuppiMET200off/hltPFPuppiMET_pt'), rateFactor)
  ret['t_rates']['hltPFPuppiMET2'] = getRateHistogram(_tfile.Get('L1T_PFPuppiMET245off/hltPFPuppiMET_pt'), rateFactor)

  _tmp = _tfile.Get('L1T_PFPuppiMET200off/l1tPFPuppiMET_pt')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp_integErr)
  ret['v_rates'] ['L1T_PFPuppiMET200off'] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts']['L1T_PFPuppiMET200off'] = [_tmp_integ, _tmp_integErr.value]

  _tmp = _tfile.Get('L1T_PFPuppiMET200off/hltPFPuppiMET_pt')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(_tmp.GetXaxis().FindBin(float(hltThreshold_MET)), -1, _tmp_integErr)
  ret['v_rates'] ['HLT_PFPuppiMET'+str(hltThreshold_MET)] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts']['HLT_PFPuppiMET'+str(hltThreshold_MET)] = [_tmp_integ, _tmp_integErr.value]

  _tmp = _tfile.Get('L1T_PFPuppiMET245off/l1tPFPuppiMET_pt')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp_integErr)
  ret['v_rates'] ['L1T_PFPuppiMET245off'] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts']['L1T_PFPuppiMET245off'] = [_tmp_integ, _tmp_integErr.value]

  if hltThreshold_MET2 != hltThreshold_MET:
    _tmp = _tfile.Get('L1T_PFPuppiMET245off/hltPFPuppiMET_pt')
    _tmp_integErr = ctypes.c_double(0.)
    _tmp_integ = _tmp.IntegralAndError(_tmp.GetXaxis().FindBin(float(hltThreshold_MET)), -1, _tmp_integErr)
    ret['v_rates'] ['HLT_PFPuppiMET'+str(hltThreshold_MET2)] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
    ret['v_counts']['HLT_PFPuppiMET'+str(hltThreshold_MET2)] = [_tmp_integ, _tmp_integErr.value]

  ## common
  for _tmp1 in ret:
    if not _tmp1.startswith('t_'):
      continue
    for _tmp2 in ret[_tmp1]:
      if ret[_tmp1][_tmp2].InheritsFrom('TH1'):
        ret[_tmp1][_tmp2].SetDirectory(0)
        ret[_tmp1][_tmp2].UseCurrentStyle()

  _tfile.Close()

  return ret

def getJetEfficiencies(fpath, hltThreshold_SingleJet):
  global L1T_SingleJet, L1T_HT

  ret = {}

  _tfile = ROOT.TFile.Open(fpath)

  _tmpRefs = [
    'GEN',
#    'Offline',
  ]

  # SingleJet
  binEdges_pT = array.array('d', [40.*_tmpIdx for _tmpIdx in range(25+1)])

  for _tmpRef in _tmpRefs:
#    _tmp_num = _tfile.Get(L1T_SingleJet+'/l1tSlwPFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
#    _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)
#
#    _tmp_den = _tfile.Get('NoSelection/l1tSlwPFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
#    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
#
#    ret['SingleJet_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
#    ret['SingleJet_L1T_wrt_'+_tmpRef].SetName('SingleJet_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_SingleJet), -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_pT)-1, tmpName(), binEdges_pT)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_pT)-1, tmpName(), binEdges_pT)

    ret['SingleJet_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['SingleJet_HLT_wrt_'+_tmpRef].SetName('SingleJet_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get(L1T_SingleJet+'/hltAK4PFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_SingleJet), -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_pT)-1, tmpName(), binEdges_pT)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_pT)-1, tmpName(), binEdges_pT)

    ret['SingleJet_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetName('SingleJet_L1TpHLT_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

def getHTEfficiencies(fpath, hltThreshold_HT):
  global L1T_SingleJet, L1T_HT

  ret = {}

  _tfile = ROOT.TFile.Open(fpath)

  _tmpRefs = [
    'GEN',
#    'Offline',
  ]

  # HT
  binEdges_HT = array.array('d', [50.*_tmpIdx for _tmpIdx in range(36+1)])

  for _tmpRef in _tmpRefs:

#    _tmp_num = _tfile.Get(L1T_HT+'/l1tSlwPFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
#    _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)
#
#    _tmp_den = _tfile.Get('NoSelection/l1tSlwPFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
#    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
#
#    ret['HT_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
#    ret['HT_L1T_wrt_'+_tmpRef].SetName('HT_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_Eta2p4_HT__vs__'+_tmpRef+'_HT')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_HT), -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_HT)-1, tmpName(), binEdges_HT)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_Eta2p4_HT__vs__'+_tmpRef+'_HT')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_HT)-1, tmpName(), binEdges_HT)

    ret['HT_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['HT_HLT_wrt_'+_tmpRef].SetName('HT_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get(L1T_HT+'/hltAK4PFPuppiJetsCorrected_Eta2p4_HT__vs__'+_tmpRef+'_HT')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_HT), -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_HT)-1, tmpName(), binEdges_HT)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_Eta2p4_HT__vs__'+_tmpRef+'_HT')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_HT)-1, tmpName(), binEdges_HT)

    ret['HT_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['HT_L1TpHLT_wrt_'+_tmpRef].SetName('HT_L1TpHLT_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

def getMETEfficiencies(fpath, hltThreshold_MET, hltThreshold_MET2):
  ret = {}

  _tfile = ROOT.TFile.Open(fpath)
  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)

  _tmpRefs = [
    'GEN',
#    'Offline',
  ]

  for _tmpRef in _tmpRefs:
    # MET
    _tmp_num = _tfile.Get('L1T_PFPuppiMET200off/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)

    _tmp_den = _tfile.Get('NoSelection/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['MET_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET_L1T_wrt_'+_tmpRef].SetName('MET_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_MET), -1)

    _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['MET_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET_HLT_wrt_'+_tmpRef].SetName('MET_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('L1T_PFPuppiMET200off/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_MET), -1)

    _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['MET_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET_L1TpHLT_wrt_'+_tmpRef].SetName('MET_L1TpHLT_wrt_'+_tmpRef)

    # MET2
    _tmp_num = _tfile.Get('L1T_PFPuppiMET245off/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)

    _tmp_den = _tfile.Get('NoSelection/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['MET2_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET2_L1T_wrt_'+_tmpRef].SetName('MET_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_MET2), -1)

    _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['MET2_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET2_HLT_wrt_'+_tmpRef].SetName('MET_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('L1T_PFPuppiMET245off/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_MET2), -1)

    _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['MET2_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET2_L1TpHLT_wrt_'+_tmpRef].SetName('MET_L1TpHLT_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

def plotJetResponse(fpath_PU140, fpath_PU200, outputName, exts):
  fpaths = {}
  fpaths['PU140'] = ROOT.TFile.Open(fpath_PU140)
  fpaths['PU200'] = ROOT.TFile.Open(fpath_PU200)

  histos = {
    'PU140': {'pt030to100': None, 'pt100to300': None, 'pt300to600': None},
    'PU200': {'pt030to100': None, 'pt100to300': None, 'pt300to600': None},
  }

  for (_etaTag, _etaLabel) in {
    'EtaIncl': '|#eta|<5.0',
    'HB': '|#eta|<1.5',
    'HGCal': '1.5<|#eta|<3.0',
    'HF': '3.0<|#eta|<5.0',
  }.items():
   for _tmp in fpaths:
    _tmpTFile = fpaths[_tmp]
    if not _tmpTFile:
      WARNING('failed to open target TFile: '+fpaths[_tmp])
      continue

    _h2tmp = getHistogram(_tmpTFile, 'NoSelection/hltAK4PFPuppiJetsCorrected_'+_etaTag+'_MatchedToGEN_pt_overGEN__vs__GEN_pt')
    histos[_tmp]['pt030to100'] = _h2tmp.ProjectionX(tmpName(), _h2tmp.GetYaxis().FindBin( 30.001), _h2tmp.GetYaxis().FindBin( 99.999))
    histos[_tmp]['pt100to300'] = _h2tmp.ProjectionX(tmpName(), _h2tmp.GetYaxis().FindBin(100.001), _h2tmp.GetYaxis().FindBin(299.999))
    histos[_tmp]['pt300to600'] = _h2tmp.ProjectionX(tmpName(), _h2tmp.GetYaxis().FindBin(300.001), _h2tmp.GetYaxis().FindBin(599.999))

   for _tmp1 in histos:
    for _tmp2 in histos[_tmp1]:
      if histos[_tmp1][_tmp2] is None: continue
      histos[_tmp1][_tmp2].SetDirectory(0)
      histos[_tmp1][_tmp2].UseCurrentStyle()
      histos[_tmp1][_tmp2].Scale(1./histos[_tmp1][_tmp2].Integral())

   canvas = ROOT.TCanvas(tmpName(), tmpName())
   canvas.cd()

   h0 = canvas.DrawFrame(0.001, 0.0001, 2.59, 0.47 if _etaTag in ['EtaIncl', 'HB'] else 0.34)

   histos['PU140']['pt030to100'].SetMarkerStyle(20)
   histos['PU140']['pt030to100'].SetMarkerSize(1.0)
   histos['PU140']['pt030to100'].SetLineWidth(2)
   histos['PU140']['pt030to100'].SetLineStyle(2)
   histos['PU140']['pt030to100'].SetLineColor(1)
   histos['PU140']['pt030to100'].SetMarkerColor(1)

   histos['PU140']['pt100to300'].SetMarkerStyle(20)
   histos['PU140']['pt100to300'].SetMarkerSize(1.0)
   histos['PU140']['pt100to300'].SetLineWidth(2)
   histos['PU140']['pt100to300'].SetLineStyle(2)
   histos['PU140']['pt100to300'].SetLineColor(2)
   histos['PU140']['pt100to300'].SetMarkerColor(2)
 
   histos['PU140']['pt300to600'].SetMarkerStyle(20)
   histos['PU140']['pt300to600'].SetMarkerSize(1.0)
   histos['PU140']['pt300to600'].SetLineWidth(2)
   histos['PU140']['pt300to600'].SetLineStyle(2)
   histos['PU140']['pt300to600'].SetLineColor(4)
   histos['PU140']['pt300to600'].SetMarkerColor(4)

   histos['PU200']['pt030to100'].SetMarkerStyle(20)
   histos['PU200']['pt030to100'].SetMarkerSize(1.0)
   histos['PU200']['pt030to100'].SetLineWidth(2)
   histos['PU200']['pt030to100'].SetLineColor(1)
   histos['PU200']['pt030to100'].SetMarkerColor(1)

   histos['PU200']['pt100to300'].SetMarkerStyle(20)
   histos['PU200']['pt100to300'].SetMarkerSize(1.0)
   histos['PU200']['pt100to300'].SetLineWidth(2)
   histos['PU200']['pt100to300'].SetLineColor(2)
   histos['PU200']['pt100to300'].SetMarkerColor(2)
 
   histos['PU200']['pt300to600'].SetMarkerStyle(20)
   histos['PU200']['pt300to600'].SetMarkerSize(1.0)
   histos['PU200']['pt300to600'].SetLineWidth(2)
   histos['PU200']['pt300to600'].SetLineColor(4)
   histos['PU200']['pt300to600'].SetMarkerColor(4)

   histos['PU140']['pt030to100'].Draw('hist,e0,same')  
   histos['PU200']['pt030to100'].Draw('hist,e0,same')  

   histos['PU140']['pt100to300'].Draw('hist,e0,same')  
   histos['PU200']['pt100to300'].Draw('hist,e0,same')  

   histos['PU140']['pt300to600'].Draw('hist,e0,same')  
   histos['PU200']['pt300to600'].Draw('hist,e0,same')  

   topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
   topLabel.SetFillColor(0)
   topLabel.SetFillStyle(1001)
   topLabel.SetTextColor(ROOT.kBlack)
   topLabel.SetTextAlign(12)
   topLabel.SetTextFont(42)
   topLabel.SetTextSize(0.035)
   topLabel.SetBorderSize(0)
   topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
   topLabel.Draw('same')

   objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
   objLabel.SetFillColor(0)
   objLabel.SetFillStyle(1001)
   objLabel.SetTextColor(ROOT.kBlack)
   objLabel.SetTextAlign(32)
   objLabel.SetTextFont(42)
   objLabel.SetTextSize(0.035)
   objLabel.SetBorderSize(0)
   objLabel.AddText('PU 140-200 (14 TeV)')
   objLabel.Draw('same')

   l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.65, 0.90, 'NDC')
   l1tRateLabel.SetFillColor(0)
   l1tRateLabel.SetFillStyle(1001)
   l1tRateLabel.SetTextColor(ROOT.kBlack)
   l1tRateLabel.SetTextAlign(12)
   l1tRateLabel.SetTextFont(42)
   l1tRateLabel.SetTextSize(0.035)
   l1tRateLabel.SetBorderSize(0)
   l1tRateLabel.AddText('AK4 PF+Puppi Jets')
   l1tRateLabel.Draw('same')

   hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.65, 0.85, 'NDC')
   hltRateLabel.SetFillColor(0)
   hltRateLabel.SetFillStyle(1001)
   hltRateLabel.SetTextColor(ROOT.kBlack)
   hltRateLabel.SetTextAlign(12)
   hltRateLabel.SetTextFont(42)
   hltRateLabel.SetTextSize(0.035)
   hltRateLabel.SetBorderSize(0)
   hltRateLabel.AddText(_etaLabel)
   hltRateLabel.Draw('same')

   aaahltRateLabel = ROOT.TPaveText(0.65, 0.80, 0.94, 0.90, 'NDC')
   aaahltRateLabel.SetFillColor(0)
   aaahltRateLabel.SetFillStyle(1001)
   aaahltRateLabel.SetTextColor(ROOT.kBlack)
   aaahltRateLabel.SetTextAlign(22)
   aaahltRateLabel.SetTextFont(42)
   aaahltRateLabel.SetTextSize(0.035)
   aaahltRateLabel.SetBorderSize(0)
   aaahltRateLabel.AddText('GEN Jet p_{T} range')
   aaahltRateLabel.Draw('same')

   leg1 = ROOT.TLegend(0.65, 0.60, 0.94, 0.80)
   leg1.SetNColumns(1)
   leg1.SetTextFont(42)
   leg1.AddEntry(histos['PU200']['pt030to100'],  '30-100 GeV', 'lepx')
   leg1.AddEntry(histos['PU200']['pt100to300'], '100-300 GeV', 'lepx')
   leg1.AddEntry(histos['PU200']['pt300to600'], '300-600 GeV', 'lepx')
   leg1.Draw('same')

   _htmpPU140 = histos['PU140']['pt030to100'].Clone()
   _htmpPU140.SetLineColor(1)
   _htmpPU140.SetLineStyle(2)

   _htmpPU200 = histos['PU200']['pt030to100'].Clone()
   _htmpPU200.SetLineColor(1)
   _htmpPU200.SetLineStyle(1)

   leg2 = ROOT.TLegend(0.75, 0.45, 0.94, 0.60)
   leg2.SetNColumns(1)
   leg2.SetTextFont(42)
   leg2.AddEntry(_htmpPU140, 'PU=140', 'l')
   leg2.AddEntry(_htmpPU200, 'PU=200', 'l')
   leg2.Draw('same')

   h0.SetTitle(';HLT Jet p_{T} response;a.u.')
   h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

   canvas.SetLogy(0)
   canvas.SetGrid(1, 1)

   for _tmpExt in exts:
     canvas.SaveAs(outputName+'_'+_etaTag+'.'+_tmpExt)

   canvas.Close()

   print '\033[1m'+outputName+'_'+_etaTag+'\033[0m'

def plotJetResolution(fpath_PU140, fpath_PU200, outputName, exts):
  fpaths = {}
  fpaths['PU140'] = ROOT.TFile.Open(fpath_PU140)
  fpaths['PU200'] = ROOT.TFile.Open(fpath_PU200)

  histos = {
    'PU140': {'HB': None, 'HGCal': None, 'HF': None},
    'PU200': {'HB': None, 'HGCal': None, 'HF': None},
  }

  pTbins = {
    'HB': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
    'HGCal': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
    'HF': [30, 40, 50, 60, 80, 120, 240, 600],
  }

  for (_puTag, _puLabel) in {
    'PU140': 'PU=140',
    'PU200': 'PU=200',
  }.items():
   _tmpTFile = fpaths[_puTag]
   if not _tmpTFile:
     WARNING('failed to open target TFile: '+fpaths[_puTag])
     continue

   for _etaTag in pTbins:
     h1vals = []
     _h2tmp = getHistogram(_tmpTFile, 'NoSelection/hltAK4PFPuppiJetsCorrected_'+_etaTag+'_MatchedToGEN_pt_overGEN__vs__GEN_pt')
     for pTbinEdge_idx in range(len(pTbins[_etaTag])-1):
       _h1tmp = _h2tmp.ProjectionX(tmpName(), _h2tmp.GetYaxis().FindBin(1.0001*pTbins[_etaTag][pTbinEdge_idx]), _h2tmp.GetYaxis().FindBin(0.9999*pTbins[_etaTag][pTbinEdge_idx+1]))
       _h1tmp_val = _h1tmp.GetRMS() / _h1tmp.GetMean() if _h1tmp.GetMean() != 0. else None
       _h1tmp_err = _h1tmp.GetRMSError() / _h1tmp.GetMean() if _h1tmp.GetMean() != 0. else None
       h1vals.append([_h1tmp_val, _h1tmp_err])

     binEdges = array.array('d', pTbins[_etaTag])
     histos[_puTag][_etaTag] = ROOT.TH1D(tmpName(), tmpName(), len(binEdges)-1, binEdges)
     histos[_puTag][_etaTag].UseCurrentStyle()
     for _binIdx in range(histos[_puTag][_etaTag].GetNbinsX()):
       if h1vals[_binIdx] != [None, None]:
         histos[_puTag][_etaTag].SetBinContent(_binIdx+1, h1vals[_binIdx][0])
         histos[_puTag][_etaTag].SetBinError(_binIdx+1, h1vals[_binIdx][1])

   for _tmp2 in histos[_puTag]:
     if histos[_puTag][_tmp2] is None: continue
     histos[_puTag][_tmp2].SetDirectory(0)
     histos[_puTag][_tmp2].UseCurrentStyle()

   canvas = ROOT.TCanvas(tmpName(), tmpName())
   canvas.cd()

   h0 = canvas.DrawFrame(30., 0.0001, 600., 0.57)

   histos[_puTag]['HB'].SetMarkerStyle(20)
   histos[_puTag]['HB'].SetMarkerSize(1.0)
   histos[_puTag]['HB'].SetLineWidth(2)
   histos[_puTag]['HB'].SetLineColor(1)
   histos[_puTag]['HB'].SetMarkerColor(1)

   histos[_puTag]['HGCal'].SetMarkerStyle(20)
   histos[_puTag]['HGCal'].SetMarkerSize(1.0)
   histos[_puTag]['HGCal'].SetLineWidth(2)
   histos[_puTag]['HGCal'].SetLineColor(2)
   histos[_puTag]['HGCal'].SetMarkerColor(2)

   histos[_puTag]['HF'].SetMarkerStyle(20)
   histos[_puTag]['HF'].SetMarkerSize(1.0)
   histos[_puTag]['HF'].SetLineWidth(2)
   histos[_puTag]['HF'].SetLineColor(4)
   histos[_puTag]['HF'].SetMarkerColor(4)

   histos[_puTag]['HB'].Draw('hist,e0,same')  
   histos[_puTag]['HGCal'].Draw('hist,e0,same')  
   histos[_puTag]['HF'].Draw('hist,e0,same')  

   topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
   topLabel.SetFillColor(0)
   topLabel.SetFillStyle(1001)
   topLabel.SetTextColor(ROOT.kBlack)
   topLabel.SetTextAlign(12)
   topLabel.SetTextFont(42)
   topLabel.SetTextSize(0.035)
   topLabel.SetBorderSize(0)
   topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
   topLabel.Draw('same')

   objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
   objLabel.SetFillColor(0)
   objLabel.SetFillStyle(1001)
   objLabel.SetTextColor(ROOT.kBlack)
   objLabel.SetTextAlign(32)
   objLabel.SetTextFont(42)
   objLabel.SetTextSize(0.035)
   objLabel.SetBorderSize(0)
   objLabel.AddText(_puLabel+' (14 TeV)')
   objLabel.Draw('same')

   l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.65, 0.90, 'NDC')
   l1tRateLabel.SetFillColor(0)
   l1tRateLabel.SetFillStyle(1001)
   l1tRateLabel.SetTextColor(ROOT.kBlack)
   l1tRateLabel.SetTextAlign(12)
   l1tRateLabel.SetTextFont(42)
   l1tRateLabel.SetTextSize(0.035)
   l1tRateLabel.SetBorderSize(0)
   l1tRateLabel.AddText('AK4 PF+Puppi Jets')
   l1tRateLabel.Draw('same')

   hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.65, 0.85, 'NDC')
   hltRateLabel.SetFillColor(0)
   hltRateLabel.SetFillStyle(1001)
   hltRateLabel.SetTextColor(ROOT.kBlack)
   hltRateLabel.SetTextAlign(12)
   hltRateLabel.SetTextFont(42)
   hltRateLabel.SetTextSize(0.035)
   hltRateLabel.SetBorderSize(0)
#   hltRateLabel.AddText(_etaLabel)
#   hltRateLabel.Draw('same')

   aaahltRateLabel = ROOT.TPaveText(0.65, 0.80, 0.94, 0.90, 'NDC')
   aaahltRateLabel.SetFillColor(0)
   aaahltRateLabel.SetFillStyle(1001)
   aaahltRateLabel.SetTextColor(ROOT.kBlack)
   aaahltRateLabel.SetTextAlign(22)
   aaahltRateLabel.SetTextFont(42)
   aaahltRateLabel.SetTextSize(0.035)
   aaahltRateLabel.SetBorderSize(0)
   aaahltRateLabel.AddText(_puLabel)
#   aaahltRateLabel.Draw('same')

   leg1 = ROOT.TLegend(0.65, 0.70, 0.94, 0.90)
   leg1.SetNColumns(1)
   leg1.SetTextFont(42)
   leg1.AddEntry(histos[_puTag]['HB']   ,     '|#eta|<1.5', 'lepx')
   leg1.AddEntry(histos[_puTag]['HGCal'], '1.5<|#eta|<3.0', 'lepx')
   leg1.AddEntry(histos[_puTag]['HF']   , '3.0<|#eta|<5.0', 'lepx')
   leg1.Draw('same')

   h0.SetTitle(';GEN Jet p_{T} [GeV];#sigma(p^{HLT}_{T} / p^{GEN}_{T}) / #LTp^{HLT}_{T} / p^{GEN}_{T}#GT')
   h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

   canvas.SetLogy(0)
   canvas.SetGrid(1, 1)

   for _tmpExt in exts:
     canvas.SaveAs(outputName+'_'+_puTag+'.'+_tmpExt)

   canvas.Close()

   print '\033[1m'+outputName+'_'+_puTag+'\033[0m'

def plotJetMatchingEff(fpath_PU140, fpath_PU200, outputName, exts):
  fpaths = {}
  fpaths['PU140'] = ROOT.TFile.Open(fpath_PU140)
  fpaths['PU200'] = ROOT.TFile.Open(fpath_PU200)

  graphs = {
    'PU140': {'HB': None, 'HGCal': None, 'HF': None},
    'PU200': {'HB': None, 'HGCal': None, 'HF': None},
  }

  for (_puTag, _puLabel) in {
    'PU140': 'PU=140',
    'PU200': 'PU=200',
  }.items():
   _tmpTFile = fpaths[_puTag]
   if not _tmpTFile:
     WARNING('failed to open target TFile: '+fpaths[_puTag])
     continue

   # HLT - MatchedToGEN
   pTbins = {
     'HB': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
     'HGCal': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
     'HF': [30, 40, 50, 60, 80, 120, 240, 600],
   }

   for _etaTag in pTbins:
     _htmpNum = getHistogram(_tmpTFile, 'NoSelection/hltAK4PFPuppiJetsCorrected_'+_etaTag+'_MatchedToGEN_pt')
     _htmpDen = getHistogram(_tmpTFile, 'NoSelection/hltAK4PFPuppiJetsCorrected_'+_etaTag+'_pt')

     _binEdges = array.array('d', pTbins[_etaTag])
     _htmpNum = _htmpNum.Rebin(len(_binEdges)-1, tmpName(), _binEdges)
     _htmpDen = _htmpDen.Rebin(len(_binEdges)-1, tmpName(), _binEdges)

     graphs[_puTag][_etaTag] = get_efficiency_graph(_htmpNum, _htmpDen)

   for _tmp2 in graphs[_puTag]:
     if graphs[_puTag][_tmp2] is None: continue
     graphs[_puTag][_tmp2].UseCurrentStyle()

   canvas = ROOT.TCanvas(tmpName(), tmpName())
   canvas.cd()

   h0 = canvas.DrawFrame(30., 0.0001, 600., 1.2)

   graphs[_puTag]['HB'].SetMarkerStyle(20)
   graphs[_puTag]['HB'].SetMarkerSize(1)
   graphs[_puTag]['HB'].SetLineWidth(2)
   graphs[_puTag]['HB'].SetLineColor(1)
   graphs[_puTag]['HB'].SetMarkerColor(1)

   graphs[_puTag]['HGCal'].SetMarkerStyle(21)
   graphs[_puTag]['HGCal'].SetMarkerSize(1)
   graphs[_puTag]['HGCal'].SetLineWidth(2)
   graphs[_puTag]['HGCal'].SetLineColor(2)
   graphs[_puTag]['HGCal'].SetMarkerColor(2)

   graphs[_puTag]['HF'].SetMarkerStyle(33)
   graphs[_puTag]['HF'].SetMarkerSize(1.5)
   graphs[_puTag]['HF'].SetLineWidth(2)
   graphs[_puTag]['HF'].SetLineColor(4)
   graphs[_puTag]['HF'].SetMarkerColor(4)

   graphs[_puTag]['HB'].Draw('lepz')
   graphs[_puTag]['HGCal'].Draw('lepz')
   graphs[_puTag]['HF'].Draw('lepz')

   topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
   topLabel.SetFillColor(0)
   topLabel.SetFillStyle(1001)
   topLabel.SetTextColor(ROOT.kBlack)
   topLabel.SetTextAlign(12)
   topLabel.SetTextFont(42)
   topLabel.SetTextSize(0.035)
   topLabel.SetBorderSize(0)
   topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
   topLabel.Draw('same')

   objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
   objLabel.SetFillColor(0)
   objLabel.SetFillStyle(1001)
   objLabel.SetTextColor(ROOT.kBlack)
   objLabel.SetTextAlign(32)
   objLabel.SetTextFont(42)
   objLabel.SetTextSize(0.035)
   objLabel.SetBorderSize(0)
   objLabel.AddText(_puLabel+' (14 TeV)')
   objLabel.Draw('same')

   l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.65, 0.90, 'NDC')
   l1tRateLabel.SetFillColor(0)
   l1tRateLabel.SetFillStyle(1001)
   l1tRateLabel.SetTextColor(ROOT.kBlack)
   l1tRateLabel.SetTextAlign(12)
   l1tRateLabel.SetTextFont(42)
   l1tRateLabel.SetTextSize(0.035)
   l1tRateLabel.SetBorderSize(0)
   l1tRateLabel.AddText('AK4 PF+Puppi Jets')
   l1tRateLabel.Draw('same')

   hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.35, 0.85, 'NDC')
   hltRateLabel.SetFillColor(0)
   hltRateLabel.SetFillStyle(1001)
   hltRateLabel.SetTextColor(ROOT.kBlack)
   hltRateLabel.SetTextAlign(12)
   hltRateLabel.SetTextFont(42)
   hltRateLabel.SetTextSize(0.035)
   hltRateLabel.SetBorderSize(0)
   hltRateLabel.AddText('p_{T}^{HLT} > 15 GeV')
   hltRateLabel.Draw('same')

   aaahltRateLabel = ROOT.TPaveText(0.65, 0.80, 0.94, 0.90, 'NDC')
   aaahltRateLabel.SetFillColor(0)
   aaahltRateLabel.SetFillStyle(1001)
   aaahltRateLabel.SetTextColor(ROOT.kBlack)
   aaahltRateLabel.SetTextAlign(22)
   aaahltRateLabel.SetTextFont(42)
   aaahltRateLabel.SetTextSize(0.035)
   aaahltRateLabel.SetBorderSize(0)
   aaahltRateLabel.AddText(_puLabel)
#   aaahltRateLabel.Draw('same')

   leg1 = ROOT.TLegend(0.60, 0.20, 0.94, 0.45)
   leg1.SetNColumns(1)
   leg1.SetTextFont(42)
   leg1.AddEntry(graphs[_puTag]['HB']   ,     '|#eta|<1.5', 'lepz')
   leg1.AddEntry(graphs[_puTag]['HGCal'], '1.5<|#eta|<3.0', 'lepz')
   leg1.AddEntry(graphs[_puTag]['HF']   , '3.0<|#eta|<5.0', 'lepz')
   leg1.Draw('same')

   hltTargetRateLine = ROOT.TLine(30, 1, 600, 1)
   hltTargetRateLine.SetLineWidth(2)
   hltTargetRateLine.SetLineStyle(2)
   hltTargetRateLine.SetLineColor(ROOT.kGray)
   hltTargetRateLine.Draw('same')

   h0.SetTitle(';HLT Jet p_{T} [GeV];GEN-Matching Efficiency')
   h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

   canvas.SetLogx(1)
   canvas.SetLogy(0)
   canvas.SetGrid(1, 1)

   h0.GetXaxis().SetNoExponent()
   h0.GetXaxis().SetMoreLogLabels()

   for _tmpExt in exts:
     canvas.SaveAs(outputName+'_hltMatchEff_'+_puTag+'.'+_tmpExt)

   canvas.Close()

   print '\033[1m'+outputName+'_hltMatchEff_'+_puTag+'\033[0m'

   # HLT - NotMatchedToGEN
   pTbins = {
     'HB': [30, 40, 50, 60, 100, 140, 200, 600],
     'HGCal': [30, 40, 50, 60, 100, 140, 200, 600],
     'HF': [30, 40, 50, 60, 100, 200, 600],
   }

   for _etaTag in pTbins:
     _htmpNum = getHistogram(_tmpTFile, 'NoSelection/hltAK4PFPuppiJetsCorrected_'+_etaTag+'_NotMatchedToGEN_pt')
     _htmpDen = getHistogram(_tmpTFile, 'NoSelection/hltAK4PFPuppiJetsCorrected_'+_etaTag+'_pt')

     _binEdges = array.array('d', pTbins[_etaTag])
     _htmpNum = _htmpNum.Rebin(len(_binEdges)-1, tmpName(), _binEdges)
     _htmpDen = _htmpDen.Rebin(len(_binEdges)-1, tmpName(), _binEdges)

     graphs[_puTag][_etaTag] = get_efficiency_graph(_htmpNum, _htmpDen)

   for _tmp2 in graphs[_puTag]:
     if graphs[_puTag][_tmp2] is None: continue
     graphs[_puTag][_tmp2].UseCurrentStyle()

   canvas = ROOT.TCanvas(tmpName(), tmpName())
   canvas.cd()

   h0 = canvas.DrawFrame(30., 0.001, 600., 2.4)

   graphs[_puTag]['HB'].SetMarkerStyle(20)
   graphs[_puTag]['HB'].SetMarkerSize(1)
   graphs[_puTag]['HB'].SetLineWidth(2)
   graphs[_puTag]['HB'].SetLineColor(1)
   graphs[_puTag]['HB'].SetMarkerColor(1)

   graphs[_puTag]['HGCal'].SetMarkerStyle(21)
   graphs[_puTag]['HGCal'].SetMarkerSize(1)
   graphs[_puTag]['HGCal'].SetLineWidth(2)
   graphs[_puTag]['HGCal'].SetLineColor(2)
   graphs[_puTag]['HGCal'].SetMarkerColor(2)

   graphs[_puTag]['HF'].SetMarkerStyle(33)
   graphs[_puTag]['HF'].SetMarkerSize(1.5)
   graphs[_puTag]['HF'].SetLineWidth(2)
   graphs[_puTag]['HF'].SetLineColor(4)
   graphs[_puTag]['HF'].SetMarkerColor(4)

   graphs[_puTag]['HB'].Draw('lepz')
   graphs[_puTag]['HGCal'].Draw('lepz')
   graphs[_puTag]['HF'].Draw('lepz')

   topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
   topLabel.SetFillColor(0)
   topLabel.SetFillStyle(1001)
   topLabel.SetTextColor(ROOT.kBlack)
   topLabel.SetTextAlign(12)
   topLabel.SetTextFont(42)
   topLabel.SetTextSize(0.035)
   topLabel.SetBorderSize(0)
   topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
   topLabel.Draw('same')

   objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
   objLabel.SetFillColor(0)
   objLabel.SetFillStyle(1001)
   objLabel.SetTextColor(ROOT.kBlack)
   objLabel.SetTextAlign(32)
   objLabel.SetTextFont(42)
   objLabel.SetTextSize(0.035)
   objLabel.SetBorderSize(0)
   objLabel.AddText(_puLabel+' (14 TeV)')
   objLabel.Draw('same')

   l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.65, 0.90, 'NDC')
   l1tRateLabel.SetFillColor(0)
   l1tRateLabel.SetFillStyle(1001)
   l1tRateLabel.SetTextColor(ROOT.kBlack)
   l1tRateLabel.SetTextAlign(12)
   l1tRateLabel.SetTextFont(42)
   l1tRateLabel.SetTextSize(0.035)
   l1tRateLabel.SetBorderSize(0)
   l1tRateLabel.AddText('AK4 PF+Puppi Jets')
   l1tRateLabel.Draw('same')

   hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.35, 0.85, 'NDC')
   hltRateLabel.SetFillColor(0)
   hltRateLabel.SetFillStyle(1001)
   hltRateLabel.SetTextColor(ROOT.kBlack)
   hltRateLabel.SetTextAlign(12)
   hltRateLabel.SetTextFont(42)
   hltRateLabel.SetTextSize(0.035)
   hltRateLabel.SetBorderSize(0)
   hltRateLabel.AddText('p_{T}^{GEN} > 20 GeV')
   hltRateLabel.Draw('same')

   aaahltRateLabel = ROOT.TPaveText(0.65, 0.80, 0.94, 0.90, 'NDC')
   aaahltRateLabel.SetFillColor(0)
   aaahltRateLabel.SetFillStyle(1001)
   aaahltRateLabel.SetTextColor(ROOT.kBlack)
   aaahltRateLabel.SetTextAlign(22)
   aaahltRateLabel.SetTextFont(42)
   aaahltRateLabel.SetTextSize(0.035)
   aaahltRateLabel.SetBorderSize(0)
#   aaahltRateLabel.AddText(_puLabel)
#   aaahltRateLabel.Draw('same')

   leg1 = ROOT.TLegend(0.60, 0.65, 0.94, 0.90)
   leg1.SetNColumns(1)
   leg1.SetTextFont(42)
   leg1.AddEntry(graphs[_puTag]['HB']   ,     '|#eta|<1.5', 'lepz')
   leg1.AddEntry(graphs[_puTag]['HGCal'], '1.5<|#eta|<3.0', 'lepz')
   leg1.AddEntry(graphs[_puTag]['HF']   , '3.0<|#eta|<5.0', 'lepz')
   leg1.Draw('same')

   hltTargetRateLine = ROOT.TLine(30, 1, 600, 1)
   hltTargetRateLine.SetLineWidth(2)
   hltTargetRateLine.SetLineStyle(2)
#   hltTargetRateLine.SetLineColor(ROOT.kGray)
#   hltTargetRateLine.Draw('same')

   h0.SetTitle(';HLT Jet p_{T} [GeV];Jet Mistag Rate')
   h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

   canvas.SetLogx(1)
   canvas.SetLogy(1)
   canvas.SetGrid(1, 1)

   h0.GetXaxis().SetNoExponent()
   h0.GetXaxis().SetMoreLogLabels()

   for _tmpExt in exts:
     canvas.SaveAs(outputName+'_hltMistagRate_'+_puTag+'.'+_tmpExt)

   canvas.Close()

   print '\033[1m'+outputName+'_hltMistagRate_'+_puTag+'\033[0m'

   # GEN - MatchedToGEN
   pTbins = {
     'HB': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
     'HGCal': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
     'HF': [30, 40, 50, 60, 80, 120, 240, 600],
   }

   for _etaTag in pTbins:
     _htmpNum = getHistogram(_tmpTFile, 'NoSelection/ak4GenJetsNoNu_'+_etaTag+'_MatchedTohltPFPuppiCorr_pt')
     _htmpDen = getHistogram(_tmpTFile, 'NoSelection/ak4GenJetsNoNu_'+_etaTag+'_pt')

     _binEdges = array.array('d', pTbins[_etaTag])
     _htmpNum = _htmpNum.Rebin(len(_binEdges)-1, tmpName(), _binEdges)
     _htmpDen = _htmpDen.Rebin(len(_binEdges)-1, tmpName(), _binEdges)

     graphs[_puTag][_etaTag] = get_efficiency_graph(_htmpNum, _htmpDen)

   for _tmp2 in graphs[_puTag]:
     if graphs[_puTag][_tmp2] is None: continue
     graphs[_puTag][_tmp2].UseCurrentStyle()

   canvas = ROOT.TCanvas(tmpName(), tmpName())
   canvas.cd()

   h0 = canvas.DrawFrame(30., 0.0001, 600., 1.2)

   graphs[_puTag]['HB'].SetMarkerStyle(20)
   graphs[_puTag]['HB'].SetMarkerSize(1)
   graphs[_puTag]['HB'].SetLineWidth(2)
   graphs[_puTag]['HB'].SetLineColor(1)
   graphs[_puTag]['HB'].SetMarkerColor(1)

   graphs[_puTag]['HGCal'].SetMarkerStyle(21)
   graphs[_puTag]['HGCal'].SetMarkerSize(1)
   graphs[_puTag]['HGCal'].SetLineWidth(2)
   graphs[_puTag]['HGCal'].SetLineColor(2)
   graphs[_puTag]['HGCal'].SetMarkerColor(2)

   graphs[_puTag]['HF'].SetMarkerStyle(33)
   graphs[_puTag]['HF'].SetMarkerSize(1.5)
   graphs[_puTag]['HF'].SetLineWidth(2)
   graphs[_puTag]['HF'].SetLineColor(4)
   graphs[_puTag]['HF'].SetMarkerColor(4)

   graphs[_puTag]['HB'].Draw('lepz')
   graphs[_puTag]['HGCal'].Draw('lepz')
   graphs[_puTag]['HF'].Draw('lepz')

   topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
   topLabel.SetFillColor(0)
   topLabel.SetFillStyle(1001)
   topLabel.SetTextColor(ROOT.kBlack)
   topLabel.SetTextAlign(12)
   topLabel.SetTextFont(42)
   topLabel.SetTextSize(0.035)
   topLabel.SetBorderSize(0)
   topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
   topLabel.Draw('same')

   objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
   objLabel.SetFillColor(0)
   objLabel.SetFillStyle(1001)
   objLabel.SetTextColor(ROOT.kBlack)
   objLabel.SetTextAlign(32)
   objLabel.SetTextFont(42)
   objLabel.SetTextSize(0.035)
   objLabel.SetBorderSize(0)
   objLabel.AddText(_puLabel+' (14 TeV)')
   objLabel.Draw('same')

   l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.65, 0.90, 'NDC')
   l1tRateLabel.SetFillColor(0)
   l1tRateLabel.SetFillStyle(1001)
   l1tRateLabel.SetTextColor(ROOT.kBlack)
   l1tRateLabel.SetTextAlign(12)
   l1tRateLabel.SetTextFont(42)
   l1tRateLabel.SetTextSize(0.035)
   l1tRateLabel.SetBorderSize(0)
   l1tRateLabel.AddText('AK4 PF+Puppi Jets')
   l1tRateLabel.Draw('same')

   hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.35, 0.85, 'NDC')
   hltRateLabel.SetFillColor(0)
   hltRateLabel.SetFillStyle(1001)
   hltRateLabel.SetTextColor(ROOT.kBlack)
   hltRateLabel.SetTextAlign(12)
   hltRateLabel.SetTextFont(42)
   hltRateLabel.SetTextSize(0.035)
   hltRateLabel.SetBorderSize(0)
   hltRateLabel.AddText('p_{T}^{HLT} > 15 GeV')
   hltRateLabel.Draw('same')

   aaahltRateLabel = ROOT.TPaveText(0.65, 0.80, 0.94, 0.90, 'NDC')
   aaahltRateLabel.SetFillColor(0)
   aaahltRateLabel.SetFillStyle(1001)
   aaahltRateLabel.SetTextColor(ROOT.kBlack)
   aaahltRateLabel.SetTextAlign(22)
   aaahltRateLabel.SetTextFont(42)
   aaahltRateLabel.SetTextSize(0.035)
   aaahltRateLabel.SetBorderSize(0)
   aaahltRateLabel.AddText(_puLabel)
#   aaahltRateLabel.Draw('same')

   leg1 = ROOT.TLegend(0.60, 0.20, 0.94, 0.45)
   leg1.SetNColumns(1)
   leg1.SetTextFont(42)
   leg1.AddEntry(graphs[_puTag]['HB']   ,     '|#eta|<1.5', 'lepz')
   leg1.AddEntry(graphs[_puTag]['HGCal'], '1.5<|#eta|<3.0', 'lepz')
   leg1.AddEntry(graphs[_puTag]['HF']   , '3.0<|#eta|<5.0', 'lepz')
   leg1.Draw('same')

   hltTargetRateLine = ROOT.TLine(30, 1, 600, 1)
   hltTargetRateLine.SetLineWidth(2)
   hltTargetRateLine.SetLineStyle(2)
   hltTargetRateLine.SetLineColor(ROOT.kGray)
   hltTargetRateLine.Draw('same')

   h0.SetTitle(';GEN Jet p_{T} [GeV];Jet-Finding Efficiency')
   h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

   canvas.SetLogx(1)
   canvas.SetLogy(0)
   canvas.SetGrid(1, 1)

   h0.GetXaxis().SetNoExponent()
   h0.GetXaxis().SetMoreLogLabels()

   for _tmpExt in exts:
     canvas.SaveAs(outputName+'_genMatchEff_'+_puTag+'.'+_tmpExt)

   canvas.Close()

   print '\033[1m'+outputName+'_genMatchEff_'+_puTag+'\033[0m'

   # GEN - NotMatchedToPFPuppiCorr
   pTbins = {
     'HB': [30, 40, 50, 60, 100, 140, 200, 300, 600],
     'HGCal': [30, 40, 50, 60, 100, 140, 200, 300, 600],
     'HF': [30, 40, 50, 60, 80, 180, 600],
   }

   for _etaTag in pTbins:
     _htmpNum = getHistogram(_tmpTFile, 'NoSelection/ak4GenJetsNoNu_'+_etaTag+'_NotMatchedTohltPFPuppiCorr_pt')
     _htmpDen = getHistogram(_tmpTFile, 'NoSelection/ak4GenJetsNoNu_'+_etaTag+'_pt')

     _binEdges = array.array('d', pTbins[_etaTag])
     _htmpNum = _htmpNum.Rebin(len(_binEdges)-1, tmpName(), _binEdges)
     _htmpDen = _htmpDen.Rebin(len(_binEdges)-1, tmpName(), _binEdges)

     graphs[_puTag][_etaTag] = get_efficiency_graph(_htmpNum, _htmpDen)

   for _tmp2 in graphs[_puTag]:
     if graphs[_puTag][_tmp2] is None: continue
     graphs[_puTag][_tmp2].UseCurrentStyle()

   canvas = ROOT.TCanvas(tmpName(), tmpName())
   canvas.cd()

   h0 = canvas.DrawFrame(30., 0.001, 600., 1.9)

   graphs[_puTag]['HB'].SetMarkerStyle(20)
   graphs[_puTag]['HB'].SetMarkerSize(1)
   graphs[_puTag]['HB'].SetLineWidth(2)
   graphs[_puTag]['HB'].SetLineColor(1)
   graphs[_puTag]['HB'].SetMarkerColor(1)

   graphs[_puTag]['HGCal'].SetMarkerStyle(21)
   graphs[_puTag]['HGCal'].SetMarkerSize(1)
   graphs[_puTag]['HGCal'].SetLineWidth(2)
   graphs[_puTag]['HGCal'].SetLineColor(2)
   graphs[_puTag]['HGCal'].SetMarkerColor(2)

   graphs[_puTag]['HF'].SetMarkerStyle(33)
   graphs[_puTag]['HF'].SetMarkerSize(1.5)
   graphs[_puTag]['HF'].SetLineWidth(2)
   graphs[_puTag]['HF'].SetLineColor(4)
   graphs[_puTag]['HF'].SetMarkerColor(4)

   graphs[_puTag]['HB'].Draw('lepz')
   graphs[_puTag]['HGCal'].Draw('lepz')
   graphs[_puTag]['HF'].Draw('lepz')

   topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
   topLabel.SetFillColor(0)
   topLabel.SetFillStyle(1001)
   topLabel.SetTextColor(ROOT.kBlack)
   topLabel.SetTextAlign(12)
   topLabel.SetTextFont(42)
   topLabel.SetTextSize(0.035)
   topLabel.SetBorderSize(0)
   topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
   topLabel.Draw('same')

   objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
   objLabel.SetFillColor(0)
   objLabel.SetFillStyle(1001)
   objLabel.SetTextColor(ROOT.kBlack)
   objLabel.SetTextAlign(32)
   objLabel.SetTextFont(42)
   objLabel.SetTextSize(0.035)
   objLabel.SetBorderSize(0)
   objLabel.AddText(_puLabel+' (14 TeV)')
   objLabel.Draw('same')

   l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.65, 0.90, 'NDC')
   l1tRateLabel.SetFillColor(0)
   l1tRateLabel.SetFillStyle(1001)
   l1tRateLabel.SetTextColor(ROOT.kBlack)
   l1tRateLabel.SetTextAlign(12)
   l1tRateLabel.SetTextFont(42)
   l1tRateLabel.SetTextSize(0.035)
   l1tRateLabel.SetBorderSize(0)
   l1tRateLabel.AddText('AK4 PF+Puppi Jets')
   l1tRateLabel.Draw('same')

   hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.35, 0.85, 'NDC')
   hltRateLabel.SetFillColor(0)
   hltRateLabel.SetFillStyle(1001)
   hltRateLabel.SetTextColor(ROOT.kBlack)
   hltRateLabel.SetTextAlign(12)
   hltRateLabel.SetTextFont(42)
   hltRateLabel.SetTextSize(0.035)
   hltRateLabel.SetBorderSize(0)
   hltRateLabel.AddText('p_{T}^{HLT} > 15 GeV')
   hltRateLabel.Draw('same')

   aaahltRateLabel = ROOT.TPaveText(0.65, 0.80, 0.94, 0.90, 'NDC')
   aaahltRateLabel.SetFillColor(0)
   aaahltRateLabel.SetFillStyle(1001)
   aaahltRateLabel.SetTextColor(ROOT.kBlack)
   aaahltRateLabel.SetTextAlign(22)
   aaahltRateLabel.SetTextFont(42)
   aaahltRateLabel.SetTextSize(0.035)
   aaahltRateLabel.SetBorderSize(0)
#   aaahltRateLabel.AddText(_puLabel)
#   aaahltRateLabel.Draw('same')

   leg1 = ROOT.TLegend(0.60, 0.65, 0.94, 0.90)
   leg1.SetNColumns(1)
   leg1.SetTextFont(42)
   leg1.AddEntry(graphs[_puTag]['HB']   ,     '|#eta|<1.5', 'lepz')
   leg1.AddEntry(graphs[_puTag]['HGCal'], '1.5<|#eta|<3.0', 'lepz')
   leg1.AddEntry(graphs[_puTag]['HF']   , '3.0<|#eta|<5.0', 'lepz')
   leg1.Draw('same')

   hltTargetRateLine = ROOT.TLine(30, 1, 600, 1)
   hltTargetRateLine.SetLineWidth(2)
   hltTargetRateLine.SetLineStyle(2)
   hltTargetRateLine.SetLineColor(ROOT.kGray)
#   hltTargetRateLine.Draw('same')

   h0.SetTitle(';GEN Jet p_{T} [GeV];% of Unreconstructed GEN Jets')
   h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

   canvas.SetLogx(1)
   canvas.SetLogy(1)
   canvas.SetGrid(1, 1)

   h0.GetXaxis().SetNoExponent()
   h0.GetXaxis().SetMoreLogLabels()

   for _tmpExt in exts:
     canvas.SaveAs(outputName+'_genMistagRate_'+_puTag+'.'+_tmpExt)

   canvas.Close()

   print '\033[1m'+outputName+'_genMistagRate_'+_puTag+'\033[0m'

#### main
if __name__ == '__main__':
  ### args ---------------
  parser = argparse.ArgumentParser(description=__doc__)

  parser.add_argument('-i', '--input', dest='inputDir', required=True, action='store', default=None,
                      help='path to input harvesting/ directory')

  parser.add_argument('-o', '--output', dest='output', action='store', default='.',
                      help='path to output directory')

  parser.add_argument('--no-plots', dest='no_plots', action='store_true',
                      help='do not create output plots')

  parser.add_argument('--minCountsForValidRate', dest='minCountsForValidRate', action='store', type=float, default=-1.0,
                      help='minimum number of counts to consider a sample valid for trigger rate estimates')

  parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['pdf', 'png'],
                      help='list of extension(s) for output file(s)')

  parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', const=1, type=int, default=0,
                      help='verbosity level')

  parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                      help='enable dry-run mode')

  opts, opts_unknown = parser.parse_known_args()
  ### --------------------

  log_prx = os.path.basename(__file__)+' -- '

  ROOT.gROOT.SetBatch() # disable interactive graphics
  ROOT.gErrorIgnoreLevel = ROOT.kError # do not display ROOT warnings

  ROOT.TH1.AddDirectory(False)

  apply_style(0)

  EXTS = list(set(opts.exts))

  ### args validation ---

  inputDir = opts.inputDir

  recoKeys = [
    'HLT_TRKv06p1_TICL',
  ]

#      print '-'*110
#      print '\033[1m{:10}\033[0m | \033[1m{:47}\033[0m | \033[1m{:47}\033[0m'.format('Rate [Hz]', '[L1T] '+_tmpL1T, '[L1T+HLT] '+_tmpHLT)
#      print '-'*110

  outputDir = opts.output
  MKDIRP(opts.output, verbose = (opts.verbosity > 0), dry_run = opts.dry_run)

  for _tmpReco in recoKeys:
    print '='*110
    print '='*110
    print '\033[1m'+_tmpReco+'\033[0m'
    print '='*110
    print '='*110

    plotJetResponse(
      fpath_PU140 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',#!!
      fpath_PU200 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',
      outputName = outputDir+'/jetResponse',
      exts = EXTS,
    )

    plotJetResolution(
      fpath_PU140 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',#!!
      fpath_PU200 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',
      outputName = outputDir+'/jetResolution',
      exts = EXTS,
    )

    plotJetMatchingEff(
      fpath_PU140 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',#!!
      fpath_PU200 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',
      outputName = outputDir+'/jetMatchingEff',
      exts = EXTS,
    )

    print '='*50
    print '='*50
    print '\033[1m'+'Efficiency Plots'+'\033[0m'
    print '='*50
    print '='*50

    effysJet = {}
    for _tmpPU in ['PU140', 'PU200']:
      effysJet[_tmpPU] = {}
      for _tmpJetThresh in ['200', '350', '500']:
        effysJet[_tmpPU][_tmpJetThresh] = getJetEfficiencies(
          fpath = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root', #!!
          hltThreshold_SingleJet = float(_tmpJetThresh),
        )

    ## SingleJet
    for _tmpRef in [
      'GEN',
#      'Offline',
    ]:
      canvas = ROOT.TCanvas(tmpName(), tmpName(False))
      canvas.cd()

      h0 = canvas.DrawFrame(100, 0.0001, 800, 1.19)

      effysJet['PU140']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
      effysJet['PU140']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
      effysJet['PU140']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(1)
      effysJet['PU140']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineColor(1)
      effysJet['PU140']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(2)
      effysJet['PU140']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

      effysJet['PU140']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
      effysJet['PU140']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
      effysJet['PU140']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(2)
      effysJet['PU140']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineColor(2)
      effysJet['PU140']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(2)
      effysJet['PU140']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

      effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
      effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
      effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(4)
      effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineColor(4)
      effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(2)
      effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

      effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
      effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
      effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(1)
      effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineColor(1)
      effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
      effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

      effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
      effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
      effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(2)
      effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineColor(2)
      effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
      effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

      effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
      effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
      effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(4)
      effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineColor(4)
      effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
      effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

      topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
      topLabel.SetFillColor(0)
      topLabel.SetFillStyle(1001)
      topLabel.SetTextColor(ROOT.kBlack)
      topLabel.SetTextAlign(12)
      topLabel.SetTextFont(42)
      topLabel.SetTextSize(0.035)
      topLabel.SetBorderSize(0)
      topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
      topLabel.Draw('same')

      objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
      objLabel.SetFillColor(0)
      objLabel.SetFillStyle(1001)
      objLabel.SetTextColor(ROOT.kBlack)
      objLabel.SetTextAlign(32)
      objLabel.SetTextFont(42)
      objLabel.SetTextSize(0.035)
      objLabel.SetBorderSize(0)
      objLabel.AddText('14 TeV')
      objLabel.Draw('same')

#      l1tRateVal = rateDict[_tmpReco][_tmp['l1tPathKey']]['MB'][0]
#      l1tRateErr = rateDict[_tmpReco][_tmp['l1tPathKey']]['MB'][1]
#
#      hltRateVal = 0.
#      hltRateErr2 = 0.
#      for _tmpSample in QCDSamples+['Wln', 'Zll']:
#        hltRateVal += rateDict[_tmpReco][_tmp['hltPathKey']][_tmpSample][0]
#        hltRateErr2 += math.pow(rateDict[_tmpReco][_tmp['hltPathKey']][_tmpSample][1], 2)

      l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.65, 0.88, 'NDC')
      l1tRateLabel.SetFillColor(0)
      l1tRateLabel.SetFillStyle(1001)
      l1tRateLabel.SetTextColor(ROOT.kBlack)
      l1tRateLabel.SetTextAlign(12)
      l1tRateLabel.SetTextFont(42)
      l1tRateLabel.SetTextSize(0.035)
      l1tRateLabel.SetBorderSize(0)
      l1tRateLabel.AddText('HLT: AK4 PF+Puppi Jets, |#eta|<5.0')
      l1tRateLabel.Draw('same')

      leg1 = ROOT.TLegend(0.60, 0.20, 0.95, 0.44)
      leg1.SetNColumns(1)
      leg1.SetTextFont(42)
      leg1.AddEntry(effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef], 'p_{T}^{HLT}>200 GeV ', 'lepx')
      leg1.AddEntry(effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef], 'p_{T}^{HLT}>350 GeV ', 'lepx')
      leg1.AddEntry(effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef], 'p_{T}^{HLT}>500 GeV ', 'lepx')
      leg1.Draw('same')

      _htmpPU140 = effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Clone()
      _htmpPU140.SetLineColor(1)
      _htmpPU140.SetLineStyle(2)

      _htmpPU200 = effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Clone()
      _htmpPU200.SetLineColor(1)
      _htmpPU200.SetLineStyle(1)

      leg2 = ROOT.TLegend(0.70, 0.44, 0.94, 0.60)
      leg2.SetNColumns(1)
      leg2.SetTextFont(42)
      leg2.AddEntry(_htmpPU140, 'PU=140', 'l')
      leg2.AddEntry(_htmpPU200, 'PU=200', 'l')
      leg2.Draw('same')

      h0.SetTitle(';'+_tmpRef+' Jet p_{T} [GeV];L1T+HLT Efficiency')
      h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

      canvas.SetLogy(0)
      canvas.SetGrid(1, 1)

      for _tmpExt in EXTS:
        canvas.SaveAs(outputDir+'/triggerEff_SingleJet_wrt'+_tmpRef+'.'+_tmpExt)

      canvas.Close()

      print '\033[1m'+outputDir+'/triggerEff_SingleJet_wrt'+_tmpRef+'\033[0m'

    ## HT
    effysHT = {}
    for _tmpPU in ['PU140', 'PU200']:
      effysHT[_tmpPU] = {}
      for _tmpHTThresh in ['600', '800', '1000']:
        effysHT[_tmpPU][_tmpHTThresh] = getHTEfficiencies(
          fpath = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root', #!!
          hltThreshold_HT = float(_tmpHTThresh),
        )

    for _tmpRef in [
      'GEN',
#      'Offline',
    ]:
      canvas = ROOT.TCanvas(tmpName(), tmpName(False))
      canvas.cd()

      h0 = canvas.DrawFrame(400, 0.0001, 1800, 1.19)

      effysHT['PU140']['600']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
      effysHT['PU140']['600']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
      effysHT['PU140']['600']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(1)
      effysHT['PU140']['600']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineColor(1)
      effysHT['PU140']['600']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(2)
      effysHT['PU140']['600']['HT_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

      effysHT['PU140']['800']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
      effysHT['PU140']['800']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
      effysHT['PU140']['800']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(2)
      effysHT['PU140']['800']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineColor(2)
      effysHT['PU140']['800']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(2)
      effysHT['PU140']['800']['HT_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

      effysHT['PU140']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
      effysHT['PU140']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
      effysHT['PU140']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(4)
      effysHT['PU140']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineColor(4)
      effysHT['PU140']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(2)
      effysHT['PU140']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

      effysHT['PU200']['600']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
      effysHT['PU200']['600']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
      effysHT['PU200']['600']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(1)
      effysHT['PU200']['600']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineColor(1)
      effysHT['PU200']['600']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
      effysHT['PU200']['600']['HT_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

      effysHT['PU200']['800']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
      effysHT['PU200']['800']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
      effysHT['PU200']['800']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(2)
      effysHT['PU200']['800']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineColor(2)
      effysHT['PU200']['800']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
      effysHT['PU200']['800']['HT_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

      effysHT['PU200']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
      effysHT['PU200']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
      effysHT['PU200']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(4)
      effysHT['PU200']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineColor(4)
      effysHT['PU200']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
      effysHT['PU200']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

      topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
      topLabel.SetFillColor(0)
      topLabel.SetFillStyle(1001)
      topLabel.SetTextColor(ROOT.kBlack)
      topLabel.SetTextAlign(12)
      topLabel.SetTextFont(42)
      topLabel.SetTextSize(0.035)
      topLabel.SetBorderSize(0)
      topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
      topLabel.Draw('same')

      objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
      objLabel.SetFillColor(0)
      objLabel.SetFillStyle(1001)
      objLabel.SetTextColor(ROOT.kBlack)
      objLabel.SetTextAlign(32)
      objLabel.SetTextFont(42)
      objLabel.SetTextSize(0.035)
      objLabel.SetBorderSize(0)
      objLabel.AddText('14 TeV')
      objLabel.Draw('same')

#      l1tRateVal = rateDict[_tmpReco][_tmp['l1tPathKey']]['MB'][0]
#      l1tRateErr = rateDict[_tmpReco][_tmp['l1tPathKey']]['MB'][1]
#
#      hltRateVal = 0.
#      hltRateErr2 = 0.
#      for _tmpSample in QCDSamples+['Wln', 'Zll']:
#        hltRateVal += rateDict[_tmpReco][_tmp['hltPathKey']][_tmpSample][0]
#        hltRateErr2 += math.pow(rateDict[_tmpReco][_tmp['hltPathKey']][_tmpSample][1], 2)

      l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.65, 0.88, 'NDC')
      l1tRateLabel.SetFillColor(0)
      l1tRateLabel.SetFillStyle(1001)
      l1tRateLabel.SetTextColor(ROOT.kBlack)
      l1tRateLabel.SetTextAlign(12)
      l1tRateLabel.SetTextFont(42)
      l1tRateLabel.SetTextSize(0.035)
      l1tRateLabel.SetBorderSize(0)
      l1tRateLabel.AddText('HLT: AK4 PF+Puppi Jets, p_{T}>30 GeV, |#eta|<2.4')
      l1tRateLabel.Draw('same')

      leg1 = ROOT.TLegend(0.60, 0.20, 0.94, 0.44)
      leg1.SetNColumns(1)
      leg1.SetTextFont(42)
      leg1.AddEntry(effysHT['PU200']['600']['HT_L1TpHLT_wrt_'+_tmpRef], 'H_{T}^{HLT}>600 GeV', 'lepx')
      leg1.AddEntry(effysHT['PU200']['800']['HT_L1TpHLT_wrt_'+_tmpRef], 'H_{T}^{HLT}>800 GeV', 'lepx')
      leg1.AddEntry(effysHT['PU200']['1000']['HT_L1TpHLT_wrt_'+_tmpRef], 'H_{T}^{HLT}>1000 GeV', 'lepx')
      leg1.Draw('same')

      _htmpPU140 = effysHT['PU140']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].Clone()
      _htmpPU140.SetLineColor(1)
      _htmpPU140.SetLineStyle(2)

      _htmpPU200 = effysHT['PU200']['1000']['HT_L1TpHLT_wrt_'+_tmpRef].Clone()
      _htmpPU200.SetLineColor(1)
      _htmpPU200.SetLineStyle(1)

      leg2 = ROOT.TLegend(0.70, 0.44, 0.94, 0.60)
      leg2.SetNColumns(1)
      leg2.SetTextFont(42)
      leg2.AddEntry(_htmpPU140, 'PU=140', 'l')
      leg2.AddEntry(_htmpPU200, 'PU=200', 'l')
      leg2.Draw('same')

      h0.SetTitle(';'+_tmpRef+' H_{T} [GeV];L1T+HLT Efficiency')
      h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

      canvas.SetLogy(0)
      canvas.SetGrid(1, 1)

      for _tmpExt in EXTS:
        canvas.SaveAs(outputDir+'/triggerEff_HT_wrt'+_tmpRef+'.'+_tmpExt)

      canvas.Close()

      print '\033[1m'+outputDir+'/triggerEff_HT_wrt'+_tmpRef+'\033[0m'









  raise SystemExit(1) #!!!!!!!!!!!!!!!!




















  hltThresholds = {

    'HLT_TRKv06p1_TICL': {

      'SingleJet': 470,
      'HT': 1000,
      'MET': 150,
      'MET2': 150,
    },
  }

  rateGroup = {

    'MB': [
      'MinBias_14TeV',
    ],

    'QCD': [
#      'QCD_Pt020to030_14TeV',
#      'QCD_Pt030to050_14TeV',
      'QCD_Pt050to080_14TeV',
      'QCD_Pt080to120_14TeV',
      'QCD_Pt120to170_14TeV',
      'QCD_Pt170to300_14TeV',
      'QCD_Pt300to470_14TeV',
      'QCD_Pt470to600_14TeV',
      'QCD_Pt600toInf_14TeV',
    ],

    'QCD_020': ['QCD_Pt020to030_14TeV'],
    'QCD_030': ['QCD_Pt030to050_14TeV'],
    'QCD_050': ['QCD_Pt050to080_14TeV'],
    'QCD_080': ['QCD_Pt080to120_14TeV'],
    'QCD_120': ['QCD_Pt120to170_14TeV'],
    'QCD_170': ['QCD_Pt170to300_14TeV'],
    'QCD_300': ['QCD_Pt300to470_14TeV'],
    'QCD_470': ['QCD_Pt470to600_14TeV'],
    'QCD_600': ['QCD_Pt600toInf_14TeV'],

    'Wln': [
      'WJetsToLNu_14TeV',
    ],
  
    'Zll': [
      'DYJetsToLL_M010to050_14TeV',
      'DYJetsToLL_M050toInf_14TeV',
    ],
  }

  QCDSamples = [
#    'QCD_020',
#    'QCD_030',
    'QCD_050',
    'QCD_080',
    'QCD_120',
    'QCD_170',
    'QCD_300',
    'QCD_470',
    'QCD_600',
  ]

  rateSamples = []
  for _tmp in rateGroup:
    rateSamples += rateGroup[_tmp]
  rateSamples = sorted(list(set(rateSamples)))

  rates = {}
  rateHistos = {}
  effys = {}
  effysJet = {}
  effysMET = {}

  rateDict = {}
  countDict = {}

  for _tmpReco in sorted(hltThresholds.keys()):
    print '='*110
    print '='*110
    print '\033[1m'+_tmpReco+'\033[0m'
    print '='*110
    print '='*110
  
    hltThresholdSingleJet = hltThresholds[_tmpReco]['SingleJet']
    hltThresholdHT = hltThresholds[_tmpReco]['HT']
    hltThresholdMET = hltThresholds[_tmpReco]['MET']
    hltThresholdMET2 = hltThresholds[_tmpReco]['MET2']
  
    hltPath_SingleJet = 'HLT_AK4PFPuppiJet'+str(hltThresholdSingleJet)
    hltPath_HT = 'HLT_PFPuppiHT'+str(hltThresholdHT)
    hltPath_MET = 'HLT_PFPuppiMET'+str(hltThresholdMET)
    hltPath_MET2 = 'HLT_PFPuppiMET'+str(hltThresholdMET2)

    rates[_tmpReco] = {}
    for _tmp in rateSamples:
      rates[_tmpReco][_tmp] = getRates(
        fpath = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_'+_tmp+'_PU200.root',
        processName = _tmp,
        hltThreshold_SingleJet = hltThresholdSingleJet,
        hltThreshold_HT = hltThresholdHT,
        hltThreshold_MET = hltThresholdMET,
        hltThreshold_MET2 = hltThresholdMET2,
      )
  
    rateDict[_tmpReco] = {}
    countDict[_tmpReco] = {}
    for _tmpTrg in [
      L1T_SingleJet,
      hltPath_SingleJet,
  
      L1T_HT,
      hltPath_HT,
  
      'L1T_PFPuppiMET200off',
      hltPath_MET,
  
      'L1T_PFPuppiMET245off',
      hltPath_MET2,
    ]:
      rateDict[_tmpReco][_tmpTrg] = {}
      countDict[_tmpReco][_tmpTrg] = {}
      for _tmp1 in rateGroup:
        theRate, theRateErr2 = 0., 0.
        theCount, theCountErr2 = 0., 0.
        for _tmp2 in rateGroup[_tmp1]:
          theRate += rates[_tmpReco][_tmp2]['v_rates'][_tmpTrg][0]
          theRateErr2 += math.pow(rates[_tmpReco][_tmp2]['v_rates'][_tmpTrg][1], 2)
          theCount += rates[_tmpReco][_tmp2]['v_counts'][_tmpTrg][0]
          theCountErr2 += math.pow(rates[_tmpReco][_tmp2]['v_counts'][_tmpTrg][1], 2)
        rateDict[_tmpReco][_tmpTrg][_tmp1] = [theRate, math.sqrt(theRateErr2)]
        countDict[_tmpReco][_tmpTrg][_tmp1] = [theCount, math.sqrt(theCountErr2)]
  
    for _tmpL1T, _tmpHLT in [
      [L1T_SingleJet, hltPath_SingleJet],
      [L1T_HT, hltPath_HT],
      ['L1T_PFPuppiMET200off', hltPath_MET],
      ['L1T_PFPuppiMET245off', hltPath_MET2],
    ]:
      print '-'*110
      print '\033[1m{:10}\033[0m | \033[1m{:47}\033[0m | \033[1m{:47}\033[0m'.format('Rate [Hz]', '[L1T] '+_tmpL1T, '[L1T+HLT] '+_tmpHLT)
      print '-'*110

      for _tmp1 in sorted(rateGroup.keys()):

        l1tRate    = rateDict[_tmpReco][_tmpL1T][_tmp1][0]
        l1tRateErr = rateDict[_tmpReco][_tmpL1T][_tmp1][1]

        hltRate    = rateDict[_tmpReco][_tmpHLT][_tmp1][0]
        hltRateErr = rateDict[_tmpReco][_tmpHLT][_tmp1][1]

        l1tCount = countDict[_tmpReco][_tmpL1T][_tmp1][0]
        hltCount = countDict[_tmpReco][_tmpHLT][_tmp1][0]

        if l1tCount < opts.minCountsForValidRate:
          l1tRate, l1tRateErr = -99., -99.

        if hltCount < opts.minCountsForValidRate:
          hltRate, hltRateErr = -99., -99.

        print '{:<10} | {:>11.2f} +/- {:>10.2f} [counts = {:9.1f}] | {:>11.2f} +/- {:>10.2f} [counts = {:9.1f}]'.format(_tmp1,
          l1tRate, l1tRateErr, l1tCount,
          hltRate, hltRateErr, hltCount
        )

    rateHistos[_tmpReco] = {}

    for _tmpVar, _tmpSamples in {
      # L1T
      'l1tSlwPFPuppiJet': ['MB'],
      'l1tPFPuppiHT'    : ['MB'],
      'l1tPFPuppiHT_2'  : ['MB'],
      'l1tPFPuppiMET'   : ['MB'],

      # HLT
      'hltAK4PFPuppiJet_woL1T': QCDSamples+['Wln', 'Zll'],
      'hltAK4PFPuppiJet'      : QCDSamples+['Wln', 'Zll'],
      'hltPFPuppiHT_woL1T'    : QCDSamples+['Wln', 'Zll'],
      'hltPFPuppiHT'          : QCDSamples+['Wln', 'Zll'],
      'hltPFPuppiMET_woL1T'   : QCDSamples+['Wln', 'Zll'],
      'hltPFPuppiMET'         : QCDSamples+['Wln', 'Zll'],
      'hltPFPuppiMET2'        : QCDSamples+['Wln', 'Zll'],
    }.items():
      rateHistos[_tmpReco][_tmpVar] = None
      for _tmp1 in _tmpSamples:
        for _tmp2 in rateGroup[_tmp1]:
          h0 = rates[_tmpReco][_tmp2]['t_rates'][_tmpVar]
          if rateHistos[_tmpReco][_tmpVar]:
            rateHistos[_tmpReco][_tmpVar].Add(h0)
          else:
            rateHistos[_tmpReco][_tmpVar] = h0.Clone()

    effysJet[_tmpReco] = getJetEfficiencies(
      fpath = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',
      hltThreshold_SingleJet = hltThresholdSingleJet,
      hltThreshold_HT = hltThresholdHT,
    )

    effysMET[_tmpReco] = getMETEfficiencies(
      fpath = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200.root',
      hltThreshold_MET = hltThresholdMET,
      hltThreshold_MET2 = hltThresholdMET2,
    )

  ### Plots
  if not opts.no_plots:

    outputDir = opts.output
    MKDIRP(opts.output, verbose = (opts.verbosity > 0), dry_run = opts.dry_run)

    canvasCount = 0

    print '='*50
    print '='*50
    print '\033[1m'+'Efficiency Plots'+'\033[0m'
    print '='*50
    print '='*50

    for _tmpReco in sorted(hltThresholds.keys()):

      hltThresholdSingleJet = hltThresholds[_tmpReco]['SingleJet']
      hltThresholdHT = hltThresholds[_tmpReco]['HT']
      hltThresholdMET = hltThresholds[_tmpReco]['MET']
      hltThresholdMET2 = hltThresholds[_tmpReco]['MET2']

      hltPath_SingleJet = 'HLT_AK4PFPuppiJet'+str(hltThresholdSingleJet)
      hltPath_HT = 'HLT_PFPuppiHT'+str(hltThresholdHT)
      hltPath_MET = 'HLT_PFPuppiMET'+str(hltThresholdMET)
      hltPath_MET2 = 'HLT_PFPuppiMET'+str(hltThresholdMET2)

      for _tmpRef in ['GEN', 'Offline']:

        for _tmp in [
          {
            'l1tPathKey': L1T_SingleJet,
            'hltPathKey': hltPath_SingleJet,
            'outputName': outputDir+'/effy_SingleJet_wrt'+_tmpRef+'_'+_tmpReco,
            'outputExts': EXTS,
            'title': ';'+_tmpRef+' Jet p_{T} [GeV];Efficiency',
            'objLabel': _tmpReco,
            'topLabel': 'QCD_PtFlat_PU200',
            'xmin': 0,
            'xmax': 1000,
            'logY': 0,
            'graphs': [
              {'graph': effysJet[_tmpReco]['SingleJet_L1T_wrt_'+_tmpRef], 'color': 2, 'legName': 'L1T'},
              {'graph': effysJet[_tmpReco]['SingleJet_HLT_wrt_'+_tmpRef], 'color': 1, 'legName': 'HLT'+str(hltThresholds[_tmpReco]['SingleJet'])},
              {'graph': effysJet[_tmpReco]['SingleJet_L1TpHLT_wrt_'+_tmpRef], 'color': 4, 'legName': 'L1T + HLT'+str(hltThresholds[_tmpReco]['SingleJet'])},
            ],
          },
          {
            'l1tPathKey': L1T_HT,
            'hltPathKey': hltPath_HT,
            'outputName': outputDir+'/effy_HT_wrt'+_tmpRef+'_'+_tmpReco,
            'outputExts': EXTS,
            'title': ';'+_tmpRef+' H_{T} [GeV];Efficiency',
            'objLabel': _tmpReco,
            'topLabel': 'QCD_PtFlat_PU200',
            'xmin': 0,
            'xmax': 2000,
            'logY': 0,
            'graphs': [
              {'graph': effysJet[_tmpReco]['HT_L1T_wrt_'+_tmpRef], 'color': 2, 'legName': 'L1T'},
              {'graph': effysJet[_tmpReco]['HT_HLT_wrt_'+_tmpRef], 'color': 1, 'legName': 'HLT'+str(hltThresholds[_tmpReco]['HT'])},
              {'graph': effysJet[_tmpReco]['HT_L1TpHLT_wrt_'+_tmpRef], 'color': 4, 'legName': 'L1T + HLT'+str(hltThresholds[_tmpReco]['HT'])},
            ],
          },
          {
            'l1tPathKey': 'L1T_PFPuppiMET200off',
            'hltPathKey': hltPath_MET,
            'outputName': outputDir+'/effy_MET_wrt'+_tmpRef+'_'+_tmpReco,
            'outputExts': EXTS,
            'title': ';'+_tmpRef+' MET [GeV];Efficiency',
            'objLabel': _tmpReco,
            'topLabel': 'VBF_HiggsToInvisible_PU200',
            'xmin': 0,
            'xmax': 600,
            'logY': 0,
            'graphs': [
              {'graph': effysMET[_tmpReco]['MET_L1T_wrt_'+_tmpRef], 'color': 2, 'legName': 'L1T'},
              {'graph': effysMET[_tmpReco]['MET_HLT_wrt_'+_tmpRef], 'color': 1, 'legName': 'HLT'+str(hltThresholds[_tmpReco]['MET'])},
              {'graph': effysMET[_tmpReco]['MET_L1TpHLT_wrt_'+_tmpRef], 'color': 4, 'legName': 'L1T + HLT'+str(hltThresholds[_tmpReco]['MET'])},
            ],
          },
          {
            'l1tPathKey': 'L1T_PFPuppiMET245off',
            'hltPathKey': hltPath_MET2,
            'outputName': outputDir+'/effy_MET2_wrt'+_tmpRef+'_'+_tmpReco,
            'outputExts': EXTS,
            'title': ';'+_tmpRef+' MET [GeV];Efficiency',
            'objLabel': _tmpReco,
            'topLabel': 'VBF_HiggsToInvisible_PU200',
            'xmin': 0,
            'xmax': 600,
            'logY': 0,
            'graphs': [
              {'graph': effysMET[_tmpReco]['MET2_L1T_wrt_'+_tmpRef], 'color': 2, 'legName': 'L1T'},
              {'graph': effysMET[_tmpReco]['MET2_HLT_wrt_'+_tmpRef], 'color': 1, 'legName': 'HLT'+str(hltThresholds[_tmpReco]['MET2'])},
              {'graph': effysMET[_tmpReco]['MET2_L1TpHLT_wrt_'+_tmpRef], 'color': 4, 'legName': 'L1T + HLT'+str(hltThresholds[_tmpReco]['MET2'])},
            ],
          },
        ]:
          canvasCount += 1
          canvasNamePostfix = '_'+str(canvasCount)

          theEffys = []
          for _tmpIdx in range(len(_tmp['graphs'])):
            g0 = _tmp['graphs'][_tmpIdx]['graph']
            g0.SetMarkerSize(0.5)
            g0.SetLineWidth(2)
            g0.SetMarkerColor(_tmp['graphs'][_tmpIdx]['color'])
            g0.SetLineColor(_tmp['graphs'][_tmpIdx]['color'])
            g0.SetName(_tmp['graphs'][_tmpIdx]['legName'])
            theEffys += [g0]

          canvas = ROOT.TCanvas('c'+canvasNamePostfix, 'c'+canvasNamePostfix)
          canvas.cd()

          h0 = canvas.DrawFrame(_tmp['xmin'], 0.0001, _tmp['xmax'], 1.19)

          for _tmp2 in theEffys:
            if _tmp2 is not None:
              _tmp2.Draw('lepz')

          topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
          topLabel.SetFillColor(0)
          topLabel.SetFillStyle(1001)
          topLabel.SetTextColor(ROOT.kBlack)
          topLabel.SetTextAlign(12)
          topLabel.SetTextFont(42)
          topLabel.SetTextSize(0.035)
          topLabel.SetBorderSize(0)
          topLabel.AddText(_tmp['topLabel'])
          topLabel.Draw('same')

          objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
          objLabel.SetFillColor(0)
          objLabel.SetFillStyle(1001)
          objLabel.SetTextColor(ROOT.kBlack)
          objLabel.SetTextAlign(32)
          objLabel.SetTextFont(42)
          objLabel.SetTextSize(0.035)
          objLabel.SetBorderSize(0)
          objLabel.AddText(_tmp['objLabel'])
          objLabel.Draw('same')

          l1tRateVal = rateDict[_tmpReco][_tmp['l1tPathKey']]['MB'][0]
          l1tRateErr = rateDict[_tmpReco][_tmp['l1tPathKey']]['MB'][1]

          hltRateVal = 0.
          hltRateErr2 = 0.
          for _tmpSample in QCDSamples+['Wln', 'Zll']:
            hltRateVal += rateDict[_tmpReco][_tmp['hltPathKey']][_tmpSample][0]
            hltRateErr2 += math.pow(rateDict[_tmpReco][_tmp['hltPathKey']][_tmpSample][1], 2)

          l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.65, 0.90, 'NDC')
          l1tRateLabel.SetFillColor(0)
          l1tRateLabel.SetFillStyle(1001)
          l1tRateLabel.SetTextColor(ROOT.kBlack)
          l1tRateLabel.SetTextAlign(12)
          l1tRateLabel.SetTextFont(42)
          l1tRateLabel.SetTextSize(0.0325)
          l1tRateLabel.SetBorderSize(0)
          l1tRateLabel.AddText('L1T Rate = {:4.1f} +/- {:4.1f} kHz (MB)'.format(l1tRateVal/1000., l1tRateErr/1000.))
          l1tRateLabel.Draw('same')

          hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.65, 0.85, 'NDC')
          hltRateLabel.SetFillColor(0)
          hltRateLabel.SetFillStyle(1001)
          hltRateLabel.SetTextColor(ROOT.kBlack)
          hltRateLabel.SetTextAlign(12)
          hltRateLabel.SetTextFont(42)
          hltRateLabel.SetTextSize(0.0325)
          hltRateLabel.SetBorderSize(0)
          hltRateLabel.AddText('L1T+HLT Rate = {:4.1f} +/- {:4.1f} Hz (QCD + V+jets)'.format(hltRateVal, math.sqrt(hltRateErr2)))
          hltRateLabel.Draw('same')

          leg = ROOT.TLegend(0.65, 0.20, 0.95, 0.40)
          leg.SetNColumns(1)
          for _tmpGr in theEffys:
            leg.AddEntry(_tmpGr, _tmpGr.GetName(), 'lepx')
          leg.Draw('same')

          h0.SetTitle(_tmp['title'])
          h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

          canvas.SetLogy(_tmp['logY'])
          canvas.SetGrid(1, 1)

          for _tmpExt in _tmp['outputExts']:
            canvas.SaveAs(_tmp['outputName']+'.'+_tmpExt)

          canvas.Close()

          print '\033[1m'+_tmp['outputName']+'\033[0m'

    raise SystemExit(1)

    print '='*50
    print '='*50
    print '\033[1m'+'Rate Plots'+'\033[0m'
    print '='*50
    print '='*50

    for _tmp in [
      {
        'l1tRateTuple': rateDict['HLT_TRKv06p1'][L1T_SingleJet]['MB'],
        'hltTargetRateHz': 75,
        'outputName': outputDir+'/rate_SingleJet',
        'outputExts': EXTS,
        'title': ';HLT PF+Puppi Jet p_{T} Threshold [GeV];L1T+HLT Rate [Hz]',
        'objLabel': '',
        'topLabel': 'MC: QCD + V+jets',
        'xmin':  400,
        'xmax':  550,
        'ymin':   11,
        'ymax':  299,
        'logY': 1,
        'histos': [
          {'histo': rateHistos['HLT_TRKv06p1']       ['hltAK4PFPuppiJet'], 'color': 1, 'lineStyle': 1, 'legName': 'TRK-v6.1 + simPF'  },
          {'histo': rateHistos['HLT_TRKv06p1_TICL']  ['hltAK4PFPuppiJet'], 'color': 2, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLold'},
          {'histo': rateHistos['HLT_TRKv06p1_TICLv2']['hltAK4PFPuppiJet'], 'color': 4, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLnew'},
          {'histo': rateHistos['HLT_TRKv07p2']       ['hltAK4PFPuppiJet'], 'color': 1, 'lineStyle': 2, 'legName': 'TRK-v7.2 + simPF'  },
          {'histo': rateHistos['HLT_TRKv07p2_TICL']  ['hltAK4PFPuppiJet'], 'color': 2, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLold'},
          {'histo': rateHistos['HLT_TRKv07p2_TICLv2']['hltAK4PFPuppiJet'], 'color': 4, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLnew'},
        ],
      },
      {
        'l1tRateTuple': rateDict['HLT_TRKv06p1'][L1T_HT]['MB'],
        'hltTargetRateHz': 75,
        'outputName': outputDir+'/rate_HT',
        'outputExts': EXTS,
        'title': ';HLT PF+Puppi H_{T} Threshold [GeV];L1T+HLT Rate [Hz]',
        'objLabel': '',
        'topLabel': 'MC: QCD + V+jets',
        'xmin':  900,
        'xmax': 1400,
        'ymin':    2,
        'ymax':  299,
        'logY': 1,
        'histos': [
          {'histo': rateHistos['HLT_TRKv06p1']       ['hltPFPuppiHT'], 'color': 1, 'lineStyle': 1, 'legName': 'TRK-v6.1 + simPF'  },
          {'histo': rateHistos['HLT_TRKv06p1_TICL']  ['hltPFPuppiHT'], 'color': 2, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLold'},
          {'histo': rateHistos['HLT_TRKv06p1_TICLv2']['hltPFPuppiHT'], 'color': 4, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLnew'},
          {'histo': rateHistos['HLT_TRKv07p2']       ['hltPFPuppiHT'], 'color': 1, 'lineStyle': 2, 'legName': 'TRK-v7.2 + simPF'  },
          {'histo': rateHistos['HLT_TRKv07p2_TICL']  ['hltPFPuppiHT'], 'color': 2, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLold'},
          {'histo': rateHistos['HLT_TRKv07p2_TICLv2']['hltPFPuppiHT'], 'color': 4, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLnew'},
        ],
      },
      {
        'l1tRateTuple': rateDict['HLT_TRKv06p1']['L1T_PFPuppiMET200off']['MB'],
        'hltTargetRateHz': 225,
        'outputName': outputDir+'/rate_MET',
        'outputExts': EXTS,
        'title': ';HLT PF+Puppi MET Threshold [GeV];L1T+HLT Rate [Hz]',
        'objLabel': '',
        'topLabel': 'MC: QCD + V+jets',
        'xmin':    0,
        'xmax':  260,
        'ymin':    2,
        'ymax': 2999,
        'logY': 1,
        'histos': [
          {'histo': rateHistos['HLT_TRKv06p1']       ['hltPFPuppiMET'], 'color': 1, 'lineStyle': 1, 'legName': 'TRK-v6.1 + simPF'  },
          {'histo': rateHistos['HLT_TRKv06p1_TICL']  ['hltPFPuppiMET'], 'color': 2, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLold'},
          {'histo': rateHistos['HLT_TRKv06p1_TICLv2']['hltPFPuppiMET'], 'color': 4, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLnew'},
          {'histo': rateHistos['HLT_TRKv07p2']       ['hltPFPuppiMET'], 'color': 1, 'lineStyle': 2, 'legName': 'TRK-v7.2 + simPF'  },
          {'histo': rateHistos['HLT_TRKv07p2_TICL']  ['hltPFPuppiMET'], 'color': 2, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLold'},
          {'histo': rateHistos['HLT_TRKv07p2_TICLv2']['hltPFPuppiMET'], 'color': 4, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLnew'},
        ],
      },
      {
        'l1tRateTuple': rateDict['HLT_TRKv06p1']['L1T_PFPuppiMET245off']['MB'],
        'hltTargetRateHz': 225,
        'outputName': outputDir+'/rate_MET2',
        'outputExts': EXTS,
        'title': ';HLT PF+Puppi MET Threshold [GeV];L1T+HLT Rate [Hz]',
        'objLabel': '',
        'topLabel': 'MC: QCD + V+jets',
        'xmin':    0,
        'xmax':  260,
        'ymin':    2,
        'ymax': 2999,
        'logY': 1,
        'histos': [
          {'histo': rateHistos['HLT_TRKv06p1']       ['hltPFPuppiMET2'], 'color': 1, 'lineStyle': 1, 'legName': 'TRK-v6.1 + simPF'  },
          {'histo': rateHistos['HLT_TRKv06p1_TICL']  ['hltPFPuppiMET2'], 'color': 2, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLold'},
          {'histo': rateHistos['HLT_TRKv06p1_TICLv2']['hltPFPuppiMET2'], 'color': 4, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLnew'},
          {'histo': rateHistos['HLT_TRKv07p2']       ['hltPFPuppiMET2'], 'color': 1, 'lineStyle': 2, 'legName': 'TRK-v7.2 + simPF'  },
          {'histo': rateHistos['HLT_TRKv07p2_TICL']  ['hltPFPuppiMET2'], 'color': 2, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLold'},
          {'histo': rateHistos['HLT_TRKv07p2_TICLv2']['hltPFPuppiMET2'], 'color': 4, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLnew'},
        ],
      },
    ]:
      canvasCount += 1
      canvasNamePostfix = '_'+str(canvasCount)

      theRates = []
      for _tmpIdx in range(len(_tmp['histos'])):
        h0 = _tmp['histos'][_tmpIdx]['histo']
        h0.SetMarkerSize(0.5)
        h0.SetLineWidth(2)
        h0.SetMarkerColor(_tmp['histos'][_tmpIdx]['color'])
        h0.SetLineColor(_tmp['histos'][_tmpIdx]['color'])
        h0.SetLineStyle(_tmp['histos'][_tmpIdx]['lineStyle'])
        h0.SetName(_tmp['histos'][_tmpIdx]['legName'])
        theRates += [h0]

      canvas = ROOT.TCanvas('c'+canvasNamePostfix, 'c'+canvasNamePostfix)
      canvas.cd()

      h0 = canvas.DrawFrame(_tmp['xmin'], _tmp['ymin'], _tmp['xmax'], _tmp['ymax'])

      for _tmp2 in theRates:
        if _tmp2 is not None:
          _tmp2.Draw('hist,e,same')

      topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
      topLabel.SetFillColor(0)
      topLabel.SetFillStyle(1001)
      topLabel.SetTextColor(ROOT.kBlack)
      topLabel.SetTextAlign(12)
      topLabel.SetTextFont(42)
      topLabel.SetTextSize(0.035)
      topLabel.SetBorderSize(0)
      topLabel.AddText(_tmp['topLabel'])
      topLabel.Draw('same')

      objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
      objLabel.SetFillColor(0)
      objLabel.SetFillStyle(1001)
      objLabel.SetTextColor(ROOT.kBlack)
      objLabel.SetTextAlign(32)
      objLabel.SetTextFont(42)
      objLabel.SetTextSize(0.035)
      objLabel.SetBorderSize(0)
      objLabel.AddText(_tmp['objLabel'])
      objLabel.Draw('same')

      l1tRateVal = _tmp['l1tRateTuple'][0]
      l1tRateErr = _tmp['l1tRateTuple'][1]

      l1tRateLabel = ROOT.TPaveText(0.50, 0.85, 0.94, 0.90, 'NDC')
      l1tRateLabel.SetFillColor(0)
      l1tRateLabel.SetFillStyle(1001)
      l1tRateLabel.SetTextColor(ROOT.kBlack)
      l1tRateLabel.SetTextAlign(12)
      l1tRateLabel.SetTextFont(42)
      l1tRateLabel.SetTextSize(0.0325)
      l1tRateLabel.SetBorderSize(0)
      l1tRateLabel.AddText('L1T Rate = {:4.1f} +/- {:4.1f} kHz (MB)'.format(l1tRateVal/1000., l1tRateErr/1000.))
      l1tRateLabel.Draw('same')

      hltTargetRateLine = ROOT.TLine(_tmp['xmin'], _tmp['hltTargetRateHz'], _tmp['xmax'], _tmp['hltTargetRateHz'])
      hltTargetRateLine.SetLineWidth(2)
      hltTargetRateLine.SetLineStyle(2)
      hltTargetRateLine.SetLineColor(ROOT.kViolet-1)
      hltTargetRateLine.Draw('same')

      hltTargetRateLabel = ROOT.TPaveText(0.50, 0.80, 0.94, 0.85, 'NDC')
      hltTargetRateLabel.SetFillColor(0)
      hltTargetRateLabel.SetFillStyle(1001)
      hltTargetRateLabel.SetTextColor(ROOT.kViolet-1)
      hltTargetRateLabel.SetTextAlign(32)
      hltTargetRateLabel.SetTextFont(42)
      hltTargetRateLabel.SetTextSize(0.0325)
      l1tRateLabel.SetBorderSize(0)
      hltTargetRateLabel.AddText('Target HLT Rate: '+str(_tmp['hltTargetRateHz'])+' Hz')
      hltTargetRateLabel.Draw('same')

      leg = ROOT.TLegend(0.165, 0.17, 0.50, 0.55)
      leg.SetNColumns(1)
      for _tmpRate in theRates:
        leg.AddEntry(_tmpRate, _tmpRate.GetName(), 'le')
      leg.Draw('same')

      h0.SetTitle(_tmp['title'])
      h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

      canvas.SetLogy(_tmp['logY'])
      canvas.SetGrid(1, 1)

      for _tmpExt in _tmp['outputExts']:
        canvas.SaveAs(_tmp['outputName']+'.'+_tmpExt)

      canvas.Close()

      print '\033[1m'+_tmp['outputName']+'\033[0m'

    print '='*50



for _tmp1 in sorted(rateDict.keys()):
  for _tmp2 in sorted(rateDict[_tmp1].keys()):
    aRate, aRateErr2 = 0., 0.
    for _tmp3 in QCDSamples+['Wln', 'Zll']:
      aRate += rateDict[_tmp1][_tmp2][_tmp3][0]
      aRateErr2 += math.pow(rateDict[_tmp1][_tmp2][_tmp3][1], 2)
    print _tmp1, '  ', _tmp2, aRate, math.sqrt(aRateErr2)

## ## Output TFile
## ofile = ROOT.TFile('tmp.root', 'recreate')
## ofile.cd()
## 
## for _tmp0 in [effysJet, effysMET]:
##   for _tmp1 in sorted(_tmp0.keys()):
##     _odir = ofile.Get(_tmp1) if ofile.Get(_tmp1) else ofile.mkdir(_tmp1)
##     _odir.cd()
##     for _tmp2 in sorted(_tmp0[_tmp1].keys()):
##       _tmp0[_tmp1][_tmp2].Write()
## 
## ofile.Close()
