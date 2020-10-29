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

COUNTER = 0
def tmpName():
  global COUNTER
  COUNTER += 1
  return 'tmp'+str(COUNTER)

def getRateFactor(processName):
  if   processName == 'MinBias_14TeV'             : return 30.903 * 1e6
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
  ret['t_rates']['hltAK4PFPuppiJet'] = getRateHistogram(_tfile.Get('L1T_SinglePFPuppiJet200off/hltAK4PFPuppiJetsCorrected_EtaIncl_pt0'), rateFactor)

  _tmp = _tfile.Get('L1T_SinglePFPuppiJet200off/l1tSlwPFPuppiJetsCorrected_EtaIncl_pt0')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp_integErr)
  ret['v_rates'] ['L1T_SinglePFPuppiJet200off'] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts']['L1T_SinglePFPuppiJet200off'] = [_tmp_integ, _tmp_integErr.value]

  _tmp = _tfile.Get('L1T_SinglePFPuppiJet200off/hltAK4PFPuppiJetsCorrected_EtaIncl_pt0')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(_tmp.GetXaxis().FindBin(float(hltThreshold_SingleJet)), -1, _tmp_integErr)
  ret['v_rates'] ['HLT_AK4PFPuppiJet'+str(hltThreshold_SingleJet)] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts']['HLT_AK4PFPuppiJet'+str(hltThreshold_SingleJet)] = [_tmp_integ, _tmp_integErr.value]

  # HT
  ret['t_rates']['l1tPFPuppiHT'] = getRateHistogram(_tfile.Get('NoSelection/l1tPFPuppiHT_sumEt'), rateFactor)
  ret['t_rates']['l1tPFPuppiHT_2'] = getRateHistogram(_tfile.Get('NoSelection/l1tSlwPFPuppiJetsCorrected_Eta2p4_HT'), rateFactor)

  ret['t_rates']['hltPFPuppiHT_woL1T'] = getRateHistogram(_tfile.Get('NoSelection/hltPFPuppiHT_sumEt'), rateFactor)
  ret['t_rates']['hltPFPuppiHT'] = getRateHistogram(_tfile.Get('L1T_PFPuppiHT450off/hltPFPuppiHT_sumEt'), rateFactor)

  _tmp = _tfile.Get('L1T_PFPuppiHT450off/l1tPFPuppiHT_sumEt')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp_integErr)
  ret['v_rates'] ['L1T_PFPuppiHT450off'] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts']['L1T_PFPuppiHT450off'] = [_tmp_integ, _tmp_integErr.value]

  _tmp = _tfile.Get('L1T_PFPuppiHT450off/hltPFPuppiHT_sumEt')
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

def getJetEfficiencies(fpath, hltThreshold_SingleJet, hltThreshold_HT):
  ret = {}

  _tfile = ROOT.TFile.Open(fpath)

  # SingleJet
  for _tmpRef in ['GEN', 'Offline']:
    _tmp_num = _tfile.Get('L1T_SinglePFPuppiJet200off/l1tSlwPFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)

    _tmp_den = _tfile.Get('NoSelection/l1tSlwPFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['SingleJet_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['SingleJet_L1T_wrt_'+_tmpRef].SetName('SingleJet_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_SingleJet), -1)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['SingleJet_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['SingleJet_HLT_wrt_'+_tmpRef].SetName('SingleJet_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('L1T_SinglePFPuppiJet200off/hltAK4PFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_SingleJet), -1)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['SingleJet_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetName('SingleJet_L1TpHLT_wrt_'+_tmpRef)

  # HT
  for _tmpRef in ['GEN', 'Offline']:

    _tmp_num = _tfile.Get('L1T_PFPuppiHT450off/l1tSlwPFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)

    _tmp_den = _tfile.Get('NoSelection/l1tSlwPFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['HT_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['HT_L1T_wrt_'+_tmpRef].SetName('HT_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_HT), -1)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['HT_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['HT_HLT_wrt_'+_tmpRef].SetName('HT_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('L1T_PFPuppiHT450off/hltAK4PFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_HT), -1)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['HT_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['HT_L1TpHLT_wrt_'+_tmpRef].SetName('HT_L1TpHLT_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

def getMETEfficiencies(fpath, hltThreshold_MET, hltThreshold_MET2):
  ret = {}

  _tfile = ROOT.TFile.Open(fpath)
  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)

  for _tmpRef in ['GEN', 'Offline']:
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

#### main
if __name__ == '__main__':
  ### args ---------------
  parser = argparse.ArgumentParser(description=__doc__)

  parser.add_argument('-i', '--input', dest='inputDir', required=True, action='store', default=None,
                      help='path to input harvesting/ directory')

  parser.add_argument('-o', '--output', dest='output', action='store', default='.',
                      help='path to output directory')

  parser.add_argument('--no-efficiencies', dest='no_efficiencies', action='store_true',
                      help='do not output efficiency plots')

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

  apply_style(0)

  EXTS = list(set(opts.exts))

  ### args validation ---

  inputDir = opts.inputDir

  hltThresholds = {
  
    'HLT_TRKv06p1': {
  
      'SingleJet': 470,
      'HT': 970,
      'MET': 120,
      'MET2': 120,
    },
  
    'HLT_TRKv07p2': {
  
      'SingleJet': 480,
      'HT': 1020,
      'MET': 120,
      'MET2': 120,
    },

    'HLT_TRKv06p1_TICL': {

      'SingleJet': 470,
      'HT': 1000,
      'MET': 150,
      'MET2': 150,
    },

    'HLT_TRKv07p2_TICL': {

      'SingleJet': 490,
      'HT': 1370,
      'MET': 230,
      'MET2': 230,
    },

    'HLT_TRKv06p1_TICLv2': {

      'SingleJet': 470,
      'HT': 980,
      'MET': 120,
      'MET2': 120,
    },

    'HLT_TRKv07p2_TICLv2': {

      'SingleJet': 480,
      'HT': 1030,
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
      'L1T_SinglePFPuppiJet200off',
      hltPath_SingleJet,
  
      'L1T_PFPuppiHT450off',
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
      ['L1T_SinglePFPuppiJet200off', hltPath_SingleJet],
      ['L1T_PFPuppiHT450off', hltPath_HT],
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
  
  ### ## Output TFile
  ### ofile = ROOT.TFile('tmp.root', 'recreate')
  ### ofile.cd()
  ### 
  ### for _tmp0 in [effysJet, effysMET]:
  ###   for _tmp1 in sorted(_tmp0.keys()):
  ###     _odir = ofile.Get(_tmp1) if ofile.Get(_tmp1) else ofile.mkdir(_tmp1)
  ###     _odir.cd()
  ###     for _tmp2 in sorted(_tmp0[_tmp1].keys()):
  ###       _tmp0[_tmp1][_tmp2].Write()
  ### 
  ### ofile.Close()
  
  ### Plots
  
  #for puTag in ['']:
  #
  #    for regTag in ['']:
  #
  #        h0 = file0.Get('l1tPFMET_pt')
  #        h1 = file0.Get('l1tPFMET_pt')
  #        h2 = file0.Get('l1tPFPuppiMET_pt')
  #
  #        h00 = getRateHistogram(h0)
  #        h01 = getRateHistogram(h1)
  #        h02 = getRateHistogram(h2)
  #
  #        h00.SetLineColor(1)
  #        h01.SetLineColor(2)
  #        h02.SetLineColor(4)
  #
  #        h00.SetLineStyle(1)
  #        h01.SetLineStyle(1)
  #        h02.SetLineStyle(1)
  #    
  #        h00.SetLineWidth(2)
  #        h01.SetLineWidth(2)
  #        h02.SetLineWidth(2)
  #
  #        h00.SetMarkerSize(0)
  #        h01.SetMarkerSize(0)
  #        h02.SetMarkerSize(0)
  #
  #        canv = ROOT.TCanvas()
  #
  ##       canv.SetRightMargin(0.05)
  ##       canv.SetLeftMargin(0.12)
  #
  #        canv.cd()
  #        canv.SetLogy()
  #
  #        h00.Draw('hist,e0')
  ##       h01.Draw('hist,e0,same')
  #        h02.Draw('hist,e0,same')
  #
  #        h00.SetTitle(';L1T MET Threshold [GeV];Rate [kHz]')
  #        h00.GetYaxis().SetRangeUser(0.01, 1e5)
  #
  #        leg = ROOT.TLegend(0.65, 0.70, 0.95, 0.90)
  #        leg.SetNColumns(1)
  #        leg.AddEntry(h00, 'L1T MET PF', 'le')
  ##       leg.AddEntry(h01, 'L1T MET PF', 'le')
  #        leg.AddEntry(h02, 'L1T MET PF+Puppi', 'le')
  #        leg.Draw('same')
  #
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
  #
  #        mcSampleTxt = ROOT.TPaveText(0.10, 0.92, 0.65, 0.99, 'NDC')
  #        mcSampleTxt.SetTextSize(0.035)
  #        mcSampleTxt.SetFillColor(0)
  #        mcSampleTxt.SetFillStyle(3000)
  #        mcSampleTxt.SetTextColor(ROOT.kBlack)
  #        mcSampleTxt.SetTextFont(42)
  #        mcSampleTxt.AddText('MinBias PU200 [11_1_X]')
  #        mcSampleTxt.Draw('same')
  #
  #        canv.SaveAs('tmp.pdf')
  #        canv.Close()
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #        h0 = file0.Get('hltPFMET_pt')
  #        h1 = file0.Get('hltPFPuppiMET_pt')
  #        h2 = file0.Get('offlinePFMET_Raw_pt')
  #        h3 = file0.Get('offlinePFPuppiMET_Raw_pt')
  #        h4 = file0.Get('offlinePFPuppiMET_Type1_pt')
  #
  #        h00 = getRateHistogram(h0)
  #        h01 = getRateHistogram(h1)
  #        h02 = getRateHistogram(h2)
  #        h03 = getRateHistogram(h3)
  #        h04 = getRateHistogram(h4)
  #
  #        h00.SetLineColor(1)
  #        h01.SetLineColor(4)
  #        h02.SetLineColor(2)
  #        h03.SetLineColor(ROOT.kViolet)
  #        h04.SetLineColor(ROOT.kOrange)
  #
  #        h00.SetLineStyle(1)
  #        h01.SetLineStyle(1)
  #        h02.SetLineStyle(1)
  #        h03.SetLineStyle(1)
  #        h04.SetLineStyle(1)
  #
  #        h00.SetLineWidth(2)
  #        h01.SetLineWidth(2)
  #        h02.SetLineWidth(2)
  #        h03.SetLineWidth(2)
  #        h04.SetLineWidth(2)
  #
  #        h00.SetMarkerSize(0)
  #        h01.SetMarkerSize(0)
  #        h02.SetMarkerSize(0)
  #        h03.SetMarkerSize(0)
  #        h04.SetMarkerSize(0)
  #
  #        canv = ROOT.TCanvas()
  #
  ##       canv.SetRightMargin(0.05)
  ##       canv.SetLeftMargin(0.12)
  #
  #        canv.cd()
  #        canv.SetLogy()
  #
  #        h00.Draw('hist,e0')
  #        h01.Draw('hist,e0,same')
  #        h02.Draw('hist,e0,same')
  #        h03.Draw('hist,e0,same')
  #        h04.Draw('hist,e0,same')
  #
  #        h00.SetTitle(';HLT/Offline MET Threshold [GeV];Rate [kHz]')
  #        h00.GetYaxis().SetRangeUser(0.01, 1e5)
  #
  #        leg = ROOT.TLegend(0.65, 0.55, 0.95, 0.90)
  #        leg.SetNColumns(1)
  #        leg.AddEntry(h00, 'HLT MET PF', 'le')
  #        leg.AddEntry(h01, 'HLT MET PF+Puppi', 'le')
  #        leg.AddEntry(h02, 'Offl MET PF', 'le')
  #        leg.AddEntry(h03, 'Offl MET PF+Puppi', 'le')
  #        leg.AddEntry(h04, 'Offl MET PF+Puppi (Type-1)', 'le')
  #        leg.Draw('same')
  #
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
  #        mcSampleTxt = ROOT.TPaveText(0.10, 0.92, 0.65, 0.99, 'NDC')
  #        mcSampleTxt.SetTextSize(0.035)
  #        mcSampleTxt.SetFillColor(0)
  #        mcSampleTxt.SetFillStyle(3000)
  #        mcSampleTxt.SetTextColor(ROOT.kBlack)
  #        mcSampleTxt.SetTextFont(42)
  #        mcSampleTxt.AddText('MinBias PU200 [11_1_X]')
  #        mcSampleTxt.Draw('same')
  #
  #        canv.SaveAs('tmp2.pdf')
  #        canv.Close()
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  ##        h0 = file0.Get('l1tPFPuppiMET_pt__hltPFPuppiMET_pt')
  ##
  ##        eff_den = h0.ProjectionY('den', 0, -1)
  ##        eff_num = h0.ProjectionY('num', h0.GetXaxis().FindBin(136.1), -1)
  ##
  ##        met_binning = [0, 30, 60, 90, 100, 110, 120, 130, 140,150,160,170,180,200,220,240,260,280,300,340,380,440,500]
  ##
  ##        eff_den2 = get_rebinned_histo(eff_den, met_binning)
  ##        eff_num2 = get_rebinned_histo(eff_num, met_binning)
  ##
  ##        geff = get_efficiency_graph(eff_num2, eff_den2)
  ##
  ##        geff.SetLineColor(4)
  ##        geff.SetLineStyle(1)
  ##        geff.SetLineWidth(2)
  ##        geff.SetMarkerSize(0.5)
  ##
  ##        canv = ROOT.TCanvas()
  ##
  ###       canv.SetRightMargin(0.05)
  ###       canv.SetLeftMargin(0.12)
  ##
  ##        canv.cd()
  ##
  ##        geff.Draw('alp')
  ##
  ##        geff.SetTitle(';Offline PF+Puppi MET (Raw) [GeV];Efficiency')
  ###        geff.GetYaxis().SetRangeUser(0.01, 1e5)
  ##
  ###        leg = ROOT.TLegend(0.65, 0.70, 0.95, 0.90)
  ###        leg.SetNColumns(1)
  ###        leg.AddEntry(h00, 'L1T MET PF', 'le')
  ####       leg.AddEntry(h01, 'L1T MET PF', 'le')
  ###        leg.AddEntry(h02, 'L1T MET PF+Puppi', 'le')
  ###        leg.Draw('same')
  ###
  ###        l1tPFPuppiMET_tdrRate = ROOT.TLine(0, 18, 500, 18)
  ###        l1tPFPuppiMET_tdrRate.SetLineWidth(2)
  ###        l1tPFPuppiMET_tdrRate.SetLineStyle(2)
  ###        l1tPFPuppiMET_tdrRate.SetLineColor(ROOT.kBlue-1)
  ###        l1tPFPuppiMET_tdrRate.Draw('same')
  ###
  ###        l1tPFPuppiMET_tdrRateTxt = ROOT.TPaveText(0.175, 0.42, 0.325, 0.52, 'NDC')
  ###        l1tPFPuppiMET_tdrRateTxt.SetTextSize(0.035)
  ###        l1tPFPuppiMET_tdrRateTxt.SetFillColor(0)
  ###        l1tPFPuppiMET_tdrRateTxt.SetFillStyle(3000)
  ###        l1tPFPuppiMET_tdrRateTxt.SetTextColor(ROOT.kBlue-1)
  ###        l1tPFPuppiMET_tdrRateTxt.SetTextFont(42)
  ###        l1tPFPuppiMET_tdrRateTxt.AddText('[18 kHz]')
  ###        l1tPFPuppiMET_tdrRateTxt.Draw('same')
  ###
  ###        l1tPFPuppiMET_thresh = ROOT.TLine(136, 0.01, 136, 18)
  ###        l1tPFPuppiMET_thresh.SetLineWidth(2)
  ###        l1tPFPuppiMET_thresh.SetLineStyle(2)
  ###        l1tPFPuppiMET_thresh.SetLineColor(ROOT.kBlue-1)
  ###        l1tPFPuppiMET_thresh.Draw('same')
  ##
  ##        canv.SaveAs('tmp2.pdf')
  ##        canv.Close()
  #
  #        h0 = file1.Get('NoSelection/l1tAK4PFJetsCorrected_Eta2p4_HT')
  #        h2 = file1.Get('NoSelection/l1tAK4PFPuppiJetsCorrected_Eta2p4_HT')
  #
  #        h00 = getRateHistogram(h0)
  #        h02 = getRateHistogram(h2)
  #
  #        h00.SetLineColor(1)
  #        h02.SetLineColor(4)
  #
  #        h00.SetLineStyle(1)
  #        h02.SetLineStyle(1)
  #    
  #        h00.SetLineWidth(2)
  #        h02.SetLineWidth(2)
  #
  #        h00.SetMarkerSize(0)
  #        h02.SetMarkerSize(0)
  #
  #        canv = ROOT.TCanvas()
  #
  ##       canv.SetRightMargin(0.05)
  ##       canv.SetLeftMargin(0.12)
  #
  #        canv.cd()
  #        canv.SetLogy()
  #
  #        h00.Draw('hist,e0')
  #        h02.Draw('hist,e0,same')
  #
  #        h00.SetTitle(';L1T H_{T} Threshold [GeV];Rate [kHz]')
  #        h00.GetYaxis().SetRangeUser(0.01, 1e5)
  #
  #        leg = ROOT.TLegend(0.65, 0.70, 0.95, 0.90)
  #        leg.SetNColumns(1)
  #        leg.AddEntry(h00, 'L1T H_{T}(Jets) PF', 'le')
  #        leg.AddEntry(h02, 'L1T H_{T}(Jets) PF+Puppi', 'le')
  #        leg.Draw('same')
  #
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
  #        mcSampleTxt = ROOT.TPaveText(0.10, 0.92, 0.65, 0.99, 'NDC')
  #        mcSampleTxt.SetTextSize(0.035)
  #        mcSampleTxt.SetFillColor(0)
  #        mcSampleTxt.SetFillStyle(3000)
  #        mcSampleTxt.SetTextColor(ROOT.kBlack)
  #        mcSampleTxt.SetTextFont(42)
  #        mcSampleTxt.AddText('MinBias PU200 [11_1_X]')
  #        mcSampleTxt.Draw('same')
  #
  #        canv.SaveAs('tmp3.pdf')
  #        canv.Close()
  #
  #
  #
  #
  #file0.Close()

  if not opts.no_efficiencies:

    outputDir = opts.output
    MKDIRP(opts.output, verbose = (opts.verbosity > 0), dry_run = opts.dry_run)

    print '='*50
    print '='*50
    print '\033[1m'+'Efficiency Plots'+'\033[0m'
    print '='*50
    print '='*50

    canvasCount = 0
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
            'l1tPathKey': 'L1T_SinglePFPuppiJet200off',
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
            'l1tPathKey': 'L1T_PFPuppiHT450off',
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

          g0 = _tmp['graphs'][0]['graph']
          g0.SetMarkerSize(0.5)
          g0.SetLineWidth(2)
          g0.SetMarkerColor(_tmp['graphs'][0]['color'])
          g0.SetLineColor(_tmp['graphs'][0]['color'])

          g1 = _tmp['graphs'][1]['graph']
          g1.SetMarkerSize(0.5)
          g1.SetLineWidth(2)
          g1.SetMarkerColor(_tmp['graphs'][1]['color'])
          g1.SetLineColor(_tmp['graphs'][1]['color'])

          g2 = _tmp['graphs'][2]['graph']
          g2.SetMarkerSize(0.5)
          g2.SetLineWidth(2)
          g2.SetMarkerColor(_tmp['graphs'][2]['color'])
          g2.SetLineColor(_tmp['graphs'][2]['color'])

          canvas = ROOT.TCanvas('c'+canvasNamePostfix, 'c'+canvasNamePostfix)
          canvas.cd()

          h0 = canvas.DrawFrame(_tmp['xmin'], 0.0001, _tmp['xmax'], 1.19)

          for _tmp2 in [g0, g1, g2]:
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

          l1tRateLabel = ROOT.TPaveText(0.17, 0.85, 0.65, 0.90, 'NDC')
          l1tRateLabel.SetFillColor(0)
          l1tRateLabel.SetFillStyle(1001)
          l1tRateLabel.SetTextColor(ROOT.kBlack)
          l1tRateLabel.SetTextAlign(12)
          l1tRateLabel.SetTextFont(42)
          l1tRateLabel.SetTextSize(0.0325)
          l1tRateLabel.SetBorderSize(0)
          l1tRateLabel.AddText('L1T Rate = {:4.1f} +/- {:4.1f} kHz (MB)'.format(l1tRateVal/1000., l1tRateErr/1000.))
          l1tRateLabel.Draw('same')

          hltRateLabel = ROOT.TPaveText(0.17, 0.80, 0.65, 0.85, 'NDC')
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
          if g0: leg.AddEntry(g0, _tmp['graphs'][0]['legName'], 'lepx')
          if g1: leg.AddEntry(g1, _tmp['graphs'][1]['legName'], 'lepx')
          if g2: leg.AddEntry(g2, _tmp['graphs'][2]['legName'], 'lepx')
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
