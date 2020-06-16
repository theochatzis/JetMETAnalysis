#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import fnmatch
import ROOT

from common.utils import *
from common.th1 import *
from common.efficiency import *
from common.plot import *
from common.plot_style import *

def updateDictionary(dictionary, TDirectory, prefix='', matches=[], skip=[], verbose=False):

    key_prefix = prefix+'/' if (len(prefix) > 0) else ''

    for j_key in TDirectory.GetListOfKeys():

        j_key_name = j_key.GetName()

        j_obj = TDirectory.Get(j_key_name)

        if j_obj.InheritsFrom('TDirectory'):

           updateDictionary(dictionary, j_obj, prefix=key_prefix+j_key_name, matches=matches, skip=skip, verbose=verbose)

        elif j_obj.InheritsFrom('TH1') or j_obj.InheritsFrom('TGraph'):

           out_key = key_prefix+j_key_name

           if skip:
              skip_key = False
              for _keyw in skip:
                  if fnmatch.fnmatch(out_key, _keyw):
                     skip_key = True
                     break
              if skip_key:
                 continue

           if matches:
              skip_key = True
              for _keyw in matches:
                  if fnmatch.fnmatch(out_key, _keyw):
                     skip_key = False
                     break
              if skip_key:
                 continue

           if out_key in dictionary:
              KILL(log_prx+'input error -> found duplicate of template ["'+out_key+'"] in input file: '+TDirectory.GetName())

           dictionary[out_key] = j_obj.Clone()
           if hasattr(dictionary[out_key], 'SetDirectory'):
              dictionary[out_key].SetDirectory(0)

           if verbose:
              print(colored_text('[input]', ['1','92']), out_key)

    return dictionary

def getTH1sFromTFile(path, matches, skip, verbose=False):

    input_histos_dict = {}

    i_inptfile = ROOT.TFile.Open(path)
    if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered):
       return input_histos_dict

    updateDictionary(input_histos_dict, i_inptfile, prefix='', matches=matches, skip=skip, verbose=verbose)

    i_inptfile.Close()

    return input_histos_dict

class Histogram:
    def __init__(self):
        self.th1 = None
        self.draw = ''
        self.Legend = ''
        self.LegendDraw = ''

def plot(histograms, outputs, title, labels, legXY=[], ratio=False, ratioPadFrac=0.3, xMin=None, xMax=None, yMin=None, yMax=None, logX=False, logY=False, autoRangeX=False):

    xyMinMax = []
    if histograms[0].th1.InheritsFrom('TGraph'):
       xyMinMax = get_xyminmax_from_graph(histograms[0].th1)

    nvalid_histograms = len(histograms)

    canvas = ROOT.TCanvas()
    canvas.SetGrid(1,1)
    canvas.SetTickx()
    canvas.SetTicky()

    Top = canvas.GetTopMargin()
    Rig = canvas.GetRightMargin()
    Bot = canvas.GetBottomMargin()
    Lef = canvas.GetLeftMargin()

    leg = None
    if len(legXY) == 4:
       leg = ROOT.TLegend(legXY[0], legXY[1], legXY[2], legXY[3])
       leg.SetBorderSize(2)
       leg.SetTextFont(42)
       leg.SetFillColor(0)
       for _tmp in histograms:
           if _tmp.th1 is not None:
              if (_tmp.th1.InheritsFrom('TH1') and _tmp.th1.GetEntries()) or (_tmp.th1.InheritsFrom('TGraph') and _tmp.th1.GetN()):
                 leg.AddEntry(_tmp.th1, _tmp.Legend, _tmp.LegendDraw)

    if autoRangeX:
       xMinCalc, xMaxCalc = None, None
       for _tmp in histograms:
           if (_tmp.th1 is not None):
              if hasattr(_tmp.th1, 'GetNbinsX'):
                 tmpXMin, tmpXMax = _tmp.th1.GetBinLowEdge(1), _tmp.th1.GetBinLowEdge(1+_tmp.th1.GetNbinsX())
                 if _tmp.th1.Integral() > 0.:
                    for i_bin in range(1, _tmp.th1.GetNbinsX()+1):
                        if (_tmp.th1.GetBinContent(i_bin) != 0.) or (_tmp.th1.GetBinError(i_bin) != 0.): break
                        tmpXMin = _tmp.th1.GetBinLowEdge(i_bin)
                    for i_bin in reversed(range(1, _tmp.th1.GetNbinsX()+1)):
                        if (_tmp.th1.GetBinContent(i_bin) != 0.) or (_tmp.th1.GetBinError(i_bin) != 0.): break
                        tmpXMax = _tmp.th1.GetBinLowEdge(i_bin)
                 xMinCalc = min(xMinCalc, tmpXMin) if xMinCalc is not None else tmpXMin
                 xMaxCalc = max(xMaxCalc, tmpXMax) if xMaxCalc is not None else tmpXMax
              else:
                 _tmp_xyMinMax = get_xyminmax_from_graph(_tmp.th1)
                 xMinCalc = min(xMinCalc, _tmp_xyMinMax[0]) if xMinCalc is not None else _tmp_xyMinMax[0]
                 xMaxCalc = max(xMaxCalc, _tmp_xyMinMax[2]) if xMaxCalc is not None else _tmp_xyMinMax[2]
    else:
       xMinCalc = xyMinMax[0] if xyMinMax else histograms[0].th1.GetBinLowEdge(1)
       xMaxCalc = xyMinMax[2] if xyMinMax else histograms[0].th1.GetBinLowEdge(1+histograms[0].th1.GetNbinsX())

    XMIN = xMinCalc if xMin is None else (max(xMin, xMinCalc) if autoRangeX else xMin)
    XMAX = xMaxCalc if xMax is None else (min(xMax, xMaxCalc) if autoRangeX else xMax)

    HMIN, HMAX = 1e8, -1e8
    for _tmp in histograms:
        if (_tmp.th1 is not None):
           if hasattr(_tmp.th1, 'GetNbinsX'):
              for i_bin in range(1, _tmp.th1.GetNbinsX()+1):
                  HMAX = max(HMAX, (_tmp.th1.GetBinContent(i_bin) + _tmp.th1.GetBinError(i_bin)))
           else:
              _tmp_xyMinMax = get_xyminmax_from_graph(_tmp.th1)
              HMIN = min(HMIN, _tmp_xyMinMax[1])
              HMAX = max(HMAX, _tmp_xyMinMax[3])

    YMIN, YMAX = yMin, yMax
    if YMIN is None: YMIN = .0003 if logY else .0001
    if YMAX is None: YMAX = .0003*((HMAX/.0003)**(1./.85)) if logY else .0001+((HMAX-.0001) *(1./.85))

    canvas.cd()

    if not ratio:

       h0 = canvas.DrawFrame(XMIN, YMIN, XMAX, YMAX)

       canvas.SetTickx()
       canvas.SetTicky()

       canvas.SetLogx(logX)
       canvas.SetLogy(logY)

       for _tmp in histograms:
           if _tmp.th1 is not None:
              _tmp.th1.Draw(_tmp.draw)

       h0.Draw('axis,same')
       h0.SetTitle(title)
#       h0.GetXaxis().SetRangeUser(XMIN, XMAX)
#       h0.GetYaxis().SetRangeUser(YMIN, YMAX)

       if leg: leg.Draw('same')

       for _tmp in labels:
           if hasattr(_tmp, 'Draw'):
              _tmp.Draw('same')

    else:

       pad1H = max(0.01, 1.-ratioPadFrac)

       pad1 = ROOT.TPad('pad1', 'pad1', 0, 1-pad1H, 1, 1)

       pad1.SetTopMargin(pad1.GetTopMargin()/pad1H)
       pad1.SetBottomMargin(0.02)
       pad1.SetGrid(1,1)
       pad1.SetTickx()
       pad1.SetTicky()
       pad1.SetLogx(logX)
       pad1.SetLogy(logY)
       pad1.Draw()

       ROOT.SetOwnership(pad1, False)

       pad1.cd()

       h0 = pad1.DrawFrame(XMIN, YMIN, XMAX, YMAX)

       h11 = None
       for _tmp in histograms:
           if _tmp.th1 is not None:
              if h11 is None: h11 = _tmp.th1
              _tmp.th1.Draw(_tmp.draw)

       if not h11: return 1

       h0.Draw('axis,same')
       h0.GetXaxis().SetTitle('')
       h0.GetYaxis().SetTitle(title.split(';')[2])
       h0.GetXaxis().SetRangeUser(XMIN, XMAX)

       h0.GetYaxis().SetTitleSize(h0.GetYaxis().GetTitleSize()/pad1H)
       h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset()*pad1H)
       h0.GetXaxis().SetLabelSize(0)
       h0.GetYaxis().SetLabelSize(h0.GetYaxis().GetLabelSize()/pad1H)
       h0.GetXaxis().SetTickLength(h0.GetXaxis().GetTickLength()/pad1H)

       if YMIN is None: YMIN = .0003 if logY else .0001
       if YMAX is None: YMAX = .0003*((HMAX/.0003)**(1./.85)) if logY else .0001+((HMAX-.0001)*(1./.85))

       h0.GetYaxis().SetRangeUser(YMIN, YMAX)

       if leg:
          leg.Draw('same')
          pad1.Update()
          leg.SetY1NDC(1.-(1.-leg.GetY1NDC())/pad1H)
          leg.SetY2NDC(1.-(1.-leg.GetY2NDC())/pad1H)

       labels2 = []
       for _tmp in labels:
           if hasattr(_tmp, 'Clone'):
              _tmp2 = _tmp.Clone()
              labels2 += [_tmp2]

       for _tmp in labels2:
           _tmp.Draw('same')
           pad1.Update()
           _tmp.SetTextSize(_tmp.GetTextSize()/pad1H)
           _tmp.SetY(1.-(1.-_tmp.GetY())/pad1H)

       pad1.Update()

       canvas.cd()

       pad2 = ROOT.TPad('pad2', 'pad2', 0, 0, 1, 1-pad1H)
       pad2.SetTopMargin(0)
       pad2.SetBottomMargin(pad2.GetBottomMargin()/(1-pad1H))
       pad2.SetGrid(1,1)
       pad2.SetLogx(logX)
       pad2.SetTickx()
       pad2.SetTicky()
       pad2.Draw()

       denom = h11.Clone()
       if hasattr(denom, 'GetNbinsX'):
          for _tmp in range(0, denom.GetNbinsX()+2): denom.SetBinError(_tmp, 0.)
       else:
          for _tmp in range(denom.GetN()):
              denom.SetPointEYhigh(_tmp, 0.)
              denom.SetPointEYlow(_tmp, 0.)

       plot_ratios = []

       for _tmp in histograms:
           histo = Histogram()
           if _tmp.th1 is not None:
              histo.th1 = _tmp.th1.Clone()
              if histo.th1.InheritsFrom('TH1'):
                 histo.th1.Divide(denom)
              else:
                 histo.th1 = get_ratio_graph(histo.th1, denom)

           histo.draw = _tmp.draw
           if _tmp.th1.InheritsFrom('TH1') and ('same' not in histo.draw):
              histo.draw += ',same'

           histo.Legend = _tmp.Legend
           histo.LegendDraw = _tmp.LegendDraw

           if hasattr(histo.th1, 'SetStats'):
              histo.th1.SetStats(0)

           plot_ratios += [histo]

       ROOT.SetOwnership(pad2, False)

       pad2.cd()

       h21 = pad2.DrawFrame(XMIN, 0., XMAX, 2.)

       h21.SetFillStyle(3017)
       h21.SetFillColor(16)

       h21.GetXaxis().SetTitle(title.split(';')[1])
       h21.GetYaxis().SetTitle('Ratio')
       h21.GetYaxis().CenterTitle()
       h21.GetXaxis().SetTitleSize(h21.GetXaxis().GetTitleSize()/(1-pad1H))
       h21.GetYaxis().SetTitleSize(h21.GetYaxis().GetTitleSize()/(1-pad1H))
       h21.GetXaxis().SetTitleOffset(h21.GetXaxis().GetTitleOffset())
       h21.GetYaxis().SetTitleOffset(h21.GetYaxis().GetTitleOffset()*(1-pad1H))
       h21.GetXaxis().SetLabelSize(h21.GetYaxis().GetLabelSize()/(1-pad1H))
       h21.GetYaxis().SetLabelSize(h21.GetYaxis().GetLabelSize()/(1-pad1H))
       h21.GetXaxis().SetTickLength(h21.GetXaxis().GetTickLength()/(1-pad1H))
       h21.GetXaxis().SetLabelOffset(h21.GetXaxis().GetLabelOffset()/(1-pad1H))
       h21.GetYaxis().SetNdivisions(404)

       h21.GetXaxis().SetRangeUser(XMIN, XMAX)

       h2max, h2min = None, None
       for _tmp in plot_ratios:
           if _tmp.th1 is None: continue
           if hasattr(_tmp.th1, 'GetNbinsX'):
              for _tmpb in range(1, _tmp.th1.GetNbinsX()+1):
                  if (abs(_tmp.th1.GetBinContent(_tmpb)) > 1e-7) and (abs(_tmp.th1.GetBinError(_tmpb)) > 1e-7):
                     h2max = max(h2max, _tmp.th1.GetBinContent(_tmpb)+_tmp.th1.GetBinError(_tmpb)) if (h2max is not None) else _tmp.th1.GetBinContent(_tmpb)+_tmp.th1.GetBinError(_tmpb)
                     h2min = min(h2min, _tmp.th1.GetBinContent(_tmpb)-_tmp.th1.GetBinError(_tmpb)) if (h2min is not None) else _tmp.th1.GetBinContent(_tmpb)-_tmp.th1.GetBinError(_tmpb)
           else:
              _tmp_xyMinMax = get_xyminmax_from_graph(_tmp.th1)
              h2min = min(h2min, _tmp_xyMinMax[1]) if (h2min is not None) else _tmp_xyMinMax[1]
              h2max = max(h2max, _tmp_xyMinMax[3]) if (h2max is not None) else _tmp_xyMinMax[3]

       if (h2max is not None) and (h2min is not None):
          h2min = min(int(h2min*105.)/100., int(h2min*95.)/100.)
          h2max = max(int(h2max*105.)/100., int(h2max*95.)/100.)

          h2min = max(h2min, -5)
          h2max = min(h2max, 5)

          h21.GetYaxis().SetRangeUser(h2min, h2max)

#       h21.Draw('e2')
       for _tmp in plot_ratios:
           if _tmp.th1 is not None:
              _tmp.th1.Draw(_tmp.draw)
       h21.Draw('axis,same')

    canvas.cd()
    canvas.Update()

    for output_file in outputs:
        output_dirname = os.path.dirname(output_file)
        if not os.path.isdir(output_dirname):
           EXE('mkdir -p '+output_dirname)

        canvas.SetName(os.path.splitext(output_file)[0])
        canvas.SaveAs(output_file)

        print(colored_text('[output]', ['1', '92']), os.path.relpath(output_file))

    canvas.Close()

    if ratio:
       del plot_ratios
       del denom

    return 0

def getPlotLabels(key, isProfile, isEfficiency, keyword):

    _objLabel = ''
    if   key.startswith('ak4GenJets_'):                _objLabel = 'AK4GenJets'
    elif key.startswith('hltAK4CaloJets_'):            _objLabel = 'HLT AK4CaloJets'
    elif key.startswith('hltAK4CaloJetsCorrected_'):   _objLabel = 'HLT AK4CaloJetsCorrected'
    elif key.startswith('hltAK4PFJets_'):              _objLabel = 'HLT AK4PFJets'
    elif key.startswith('hltAK4PFJetsCorrected_'):     _objLabel = 'HLT AK4PFJetsCorrected'
    elif key.startswith('hltAK4PFCHSJets_'):           _objLabel = 'HLT AK4PFCHSJets'
    elif key.startswith('hltAK4PFCHSJetsCorrected_'):  _objLabel = 'HLT AK4PFCHSJetsCorrected'
    elif key.startswith('hltAK4PFCHSv1Jets_'):         _objLabel = 'HLT AK4PFCHSv1Jets'
    elif key.startswith('hltAK4PFCHSv1JetsCorrected_'):_objLabel = 'HLT AK4PFCHSv1JetsCorrected'
    elif key.startswith('hltAK4PFCHSv2Jets_'):         _objLabel = 'HLT AK4PFCHSv2Jets'
    elif key.startswith('hltAK4PFCHSv2JetsCorrected_'):_objLabel = 'HLT AK4PFCHSv2JetsCorrected'
    elif key.startswith('hltAK4PuppiJets_'):           _objLabel = 'HLT AK4PuppiJets'
    elif key.startswith('hltAK4PuppiJetsCorrected_'):  _objLabel = 'HLT AK4PuppiJetsCorrected'
    elif key.startswith('hltAK4PuppiV1Jets_'):         _objLabel = 'HLT AK4PuppiV1Jets'
    elif key.startswith('hltAK4PuppiV3Jets_'):         _objLabel = 'HLT AK4PuppiV3Jets'
    elif key.startswith('ak8GenJets_'):                _objLabel = 'AK8GenJets'
    elif key.startswith('hltAK8CaloJets_'):            _objLabel = 'HLT AK8CaloJets'
    elif key.startswith('hltAK8CaloJetsCorrected_'):   _objLabel = 'HLT AK8CaloJetsCorrected'
    elif key.startswith('hltAK8PFJets_'):              _objLabel = 'HLT AK8PFJets'
    elif key.startswith('hltAK8PFJetsCorrected_'):     _objLabel = 'HLT AK8PFJetsCorrected'
    elif key.startswith('hltAK8PFCHSJets_'):           _objLabel = 'HLT AK8PFCHSJets'
    elif key.startswith('hltAK8PFCHSJetsCorrected_'):  _objLabel = 'HLT AK8PFCHSJetsCorrected'
    elif key.startswith('hltAK8PuppiJets_'):           _objLabel = 'HLT AK8PuppiJets'
    elif key.startswith('hltAK8PuppiJetsCorrected_'):  _objLabel = 'HLT AK8PuppiJetsCorrected'
    elif key.startswith('hltCaloMET_'):                _objLabel = 'HLT CaloMET'
    elif key.startswith('hltPFMET_'):                  _objLabel = 'HLT PFMET'
    elif key.startswith('hltPFMETNoMu_'):              _objLabel = 'HLT PFMETNoMu'
    elif key.startswith('hltPFMETTypeOne_'):           _objLabel = 'HLT PFMET Type-1'
    elif key.startswith('hltPuppiMET_'):               _objLabel = 'HLT PuppiMET'
    elif key.startswith('hltPuppiMETNoMu_'):           _objLabel = 'HLT PuppiMETNoMu'
    elif key.startswith('hltPuppiV1MET_'):             _objLabel = 'HLT PuppiV1MET'
    elif key.startswith('hltPuppiV1METNoMu_'):         _objLabel = 'HLT PuppiV1METNoMu'
    elif key.startswith('hltPuppiV2MET_'):             _objLabel = 'HLT PuppiV2MET'
    elif key.startswith('hltPuppiV2METNoMu_'):         _objLabel = 'HLT PuppiV2METNoMu'
    elif key.startswith('hltPuppiV3MET_'):             _objLabel = 'HLT PuppiV3MET'
    elif key.startswith('hltPuppiV3METNoMu_'):         _objLabel = 'HLT PuppiV3METNoMu'
    elif key.startswith('hltPuppiV4MET_'):             _objLabel = 'HLT PuppiV4MET'
    elif key.startswith('hltPuppiV4METNoMu_'):         _objLabel = 'HLT PuppiV4METNoMu'
    elif key.startswith('hltPFCHSMET_'):               _objLabel = 'HLT PF+CHS MET'
    elif key.startswith('hltPFCHSv1MET_'):             _objLabel = 'HLT PF+CHSv1 MET'
    elif key.startswith('hltPFCHSv2MET_'):             _objLabel = 'HLT PF+CHSv2 MET'
    elif key.startswith('hltPFSoftKillerMET_'):        _objLabel = 'HLT PF+SoftKiller MET'

    if   '_EtaIncl_' in key: pass
    elif '_HB_'      in key: _objLabel += ', |#eta|<'+('1.5' if keyword.startswith('phase2') else '1.3')
    elif '_HGCal_'   in key: _objLabel += ', 1.5<|#eta|<3.0'
    elif '_HE_'      in key: _objLabel += ', 1.3<|#eta|<3.0'
    elif '_HE1_'     in key: _objLabel += ', 1.3<|#eta|<2.5'
    elif '_HE2_'     in key: _objLabel += ', 2.5<|#eta|<3.0'
    elif '_HF_'      in key: _objLabel += ', 3.0<|#eta|<5.0'
    elif '_HF1_'     in key: _objLabel += ', 3.0<|#eta|<4.0'
    elif '_HF2_'     in key: _objLabel += ', 4.0<|#eta|<5.0'

    if   '_NotMatchedToGEN'     in key: _objLabel += ' [Not Matched to GEN]'
    elif '_NotMatchedToOffline' in key: _objLabel += ' [Not Matched to Offline]'
    elif '_NotMatchedToCalo'    in key: _objLabel += ' [Not Matched to Calo]'
    elif '_NotMatchedToPF'      in key: _objLabel += ' [Not Matched to PF]'
    elif '_NotMatchedToPFCHS'   in key: _objLabel += ' [Not Matched to PFCHS]'
    elif '_NotMatchedToPuppi'   in key: _objLabel += ' [Not Matched to Puppi]'
    elif '_MatchedToGEN'        in key: _objLabel += ' [Matched to GEN]'
    elif '_MatchedToOffline'    in key: _objLabel += ' [Matched to Offline]'
    elif '_MatchedToCalo'       in key: _objLabel += ' [Matched to Calo]'
    elif '_MatchedToPF'         in key: _objLabel += ' [Matched to PF]'
    elif '_MatchedToPFCHS'      in key: _objLabel += ' [Matched to PFCHS]'
    elif '_MatchedToPuppi'      in key: _objLabel += ' [Matched to Puppi]'

    ## axes' titles
    _titleX, _titleY = key, 'Entries'
    if isProfile:
       if 'Jets' in key:
          if key.endswith('_pt'): _titleX = 'Jet p_{T} [GeV]'
          elif key.endswith('_eta'): _titleX = 'Jet #eta'
          elif key.endswith('_phi'): _titleX = 'Jet #phi'
          elif key.endswith('_mass'): _titleX = 'Jet mass [GeV]'
       elif 'MET' in key:
          if key.endswith('_pt'): _titleX = 'MET [GeV]'
          elif key.endswith('_phi'): _titleX = 'MET #phi'
          elif key.endswith('_sumEt'): _titleX = 'MET Sum-E_{T} [GeV]'
          elif key.endswith('_offlineNPV'): _titleX = 'Offline N_{PV}'
       if ('_GEN_' in key) or ('GenJets' in key):
          _titleX = 'GEN '+_titleX
       elif '_Offline_' in key:
          _titleX = 'Offline '+_titleX
    elif isEfficiency:
       if 'Jets' in key:
          if key.endswith('_pt_eff'): _titleX = 'Jet p_{T} [GeV]'
          elif key.endswith('_eta_eff'): _titleX = 'Jet #eta'
          elif key.endswith('_phi_eff'): _titleX = 'Jet #phi'
          elif key.endswith('_mass_eff'): _titleX = 'Jet mass [GeV]'
       elif 'MET' in key:
          if key.endswith('_pt_eff'): _titleX = 'MET [GeV]'
          elif key.endswith('_phi_eff'): _titleX = 'MET #phi'
          elif key.endswith('_sumEt_eff'): _titleX = 'MET Sum-E_{T} [GeV]'
       if ('_GEN_' in key) or ('GenJets' in key):
          _titleX = 'GEN '+_titleX
       elif '_Offline_' in key:
          _titleX = 'Offline '+_titleX
    else:
       if 'MET' in key:
          _titleY = 'Events'
       elif 'Jets' in key:
          if '_njets' in key:
             _titleY = 'Events'
          else:
             _titleY = 'Entries'

    if isEfficiency:
       _titleY = 'Efficiency'

    if   '_pt_overGEN_Mean_' in key: _titleY = '#LTp_{T} / p_{T}^{GEN}#GT'
    elif '_pt_overGEN_RMSOverMean_' in key: _titleY = '#sigma(p_{T} / p_{T}^{GEN}) / #LTp_{T} / p_{T}^{GEN}#GT'
    elif '_pt_overGEN_RMS_' in key: _titleY = '#sigma(p_{T} / p_{T}^{GEN})'

    elif '_pt_overOffline_Mean_' in key: _titleY = '#LTp_{T} / p_{T}^{Offl}#GT'
    elif '_pt_overOffline_RMSOverMean_' in key: _titleY = '#sigma(p_{T} / p_{T}^{Offl}) / #LTp_{T} / p_{T}^{Offl}#GT'
    elif '_pt_overOffline_RMS_' in key: _titleY = '#sigma(p_{T} / p_{T}^{Offl})'

    elif '_mass_overGEN_Mean_' in key: _titleY = '#LTmass / mass^{GEN}#GT'
    elif '_mass_overGEN_RMSOverMean_' in key: _titleY = '#sigma(m / m^{GEN}) / #LTm / m^{GEN}#GT'
    elif '_mass_overGEN_RMS_' in key: _titleY = '#sigma(mass / mass^{GEN})'

    elif '_mass_overOffline_Mean_' in key: _titleY = '#LTmass / mass^{Offl}#GT'
    elif '_mass_overOffline_RMSOverMean_' in key: _titleY = '#sigma(m / m^{Offl}) / #LTm / m^{Offl}#GT'
    elif '_mass_overOffline_RMS_' in key: _titleY = '#sigma(mass / mass^{Offl})'

    elif '_sumEt_overGEN_Mean_' in key: _titleY = '#LTSum-E_{T} / Sum-E_{T}^{GEN}#GT'
    elif '_sumEt_overGEN_RMSOverMean_' in key: _titleY = '#sigma(Sum-E_{T} / Sum-E_{T}^{GEN}) / #LTSum-E_{T} / Sum-E_{T}^{GEN}#GT'
    elif '_sumEt_overGEN_RMS_' in key: _titleY = '#sigma(Sum-E_{T} / Sum-E_{T}^{GEN})'

    elif '_sumEt_overOffline_Mean_' in key: _titleY = '#LTSum-E_{T} / Sum-E_{T}^{Offl}#GT'
    elif '_sumEt_overOffline_RMSOverMean_' in key: _titleY = '#sigma(Sum-E_{T} / Sum-E_{T}^{Offl}) / #LTSum-E_{T} / Sum-E_{T}^{Offl}#GT'
    elif '_sumEt_overOffline_RMS_' in key: _titleY = '#sigma(Sum-E_{T} / Sum-E_{T}^{Offl})'

    elif '_deltaPhiGEN_Mean_' in key: _titleY = '#LT#Delta#phi^{GEN}#GT'
#   elif '_deltaPhiGEN_RMSOverMean_' in key: _titleY = '#sigma(#Delta#phi^{GEN}) / #LT#Delta#phi^{GEN}#GT'
    elif '_deltaPhiGEN_RMS_' in key: _titleY = '#sigma(#Delta#phi^{GEN})'

    elif '_deltaPhiOffline_Mean_' in key: _titleY = '#LT#Delta#phi^{Offl}#GT'
#   elif '_deltaPhiOffline_RMSOverMean_' in key: _titleY = '#sigma(#Delta#phi^{Offl}) / #LT#Delta#phi^{Offl}#GT'
    elif '_deltaPhiOffline_RMS_' in key: _titleY = '#sigma(#Delta#phi^{Offl})'

    elif '_pt_paraToGEN_Mean_' in key: _titleY = '#LTp_{T}^{#parallel GEN}#GT [GeV]'
    elif '_pt_paraToGEN_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#parallel GEN}) / #LTp_{T} / p_{T}^{GEN}#GT [GeV]'
    elif '_pt_paraToGEN_RMS_' in key: _titleY = '#sigma(p_{T}^{#parallel GEN}) [GeV]'

    elif '_pt_paraToOffline_Mean_' in key: _titleY = '#LTp_{T}^{#parallel Offl}#GT [GeV]'
    elif '_pt_paraToOffline_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#parallel Offl}) / #LTp_{T} / p_{T}^{Offl}#GT [GeV]'
    elif '_pt_paraToOffline_RMS_' in key: _titleY = '#sigma(p_{T}^{#parallel Offl}) [GeV]'

    elif '_pt_paraToGENMinusGEN_Mean_' in key: _titleY = '#LTp_{T}^{#parallel GEN} - p_{T}^{GEN}#GT [GeV]'
    elif '_pt_paraToGENMinusGEN_RMSOverMean_' in key: _titleY = '#sigma(#Deltap_{T}^{#parallel GEN}) / #LTp_{T} / p_{T}^{GEN}#GT [GeV]'
    elif '_pt_paraToGENMinusGEN_RMS_' in key: _titleY = '#sigma(p_{T}^{#parallel GEN} - p_{T}^{GEN}) [GeV]'

    elif '_pt_paraToOfflineMinusOffline_Mean_' in key: _titleY = '#LTp_{T}^{#parallel Offl} - p_{T}^{Offl}#GT [GeV]'
    elif '_pt_paraToOfflineMinusOffline_RMSOverMean_' in key: _titleY = '#sigma(#Deltap_{T}^{#parallel Offl}) / #LTp_{T} / p_{T}^{Offl}#GT [GeV]'
    elif '_pt_paraToOfflineMinusOffline_RMS_' in key: _titleY = '#sigma(p_{T}^{#parallel Offl} - p_{T}^{Offl}) [GeV]'

    elif '_pt_perpToGEN_Mean_' in key: _titleY = '#LTp_{T}^{#perp GEN}#GT [GeV]'
    elif '_pt_perpToGEN_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#perp GEN}) / #LTp_{T} / p_{T}^{GEN}#GT [GeV]'
    elif '_pt_perpToGEN_RMS_' in key: _titleY = '#sigma(p_{T}^{#perp GEN}) [GeV]'

    elif '_pt_perpToOffline_Mean_' in key: _titleY = '#LTp_{T}^{#perp Offl}#GT [GeV]'
    elif '_pt_perpToOffline_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#perp Offl}) / #LTp_{T} / p_{T}^{Offl}#GT [GeV]'
    elif '_pt_perpToOffline_RMS_' in key: _titleY = '#sigma(p_{T}^{#perp Offl}) [GeV]'

    elif ('Jets' in key) and not (isProfile or isEfficiency):
      if   key.endswith('_pt0'): _titleX = 'p_{T}-Leading Jet p_{T} [GeV]'
      elif key.endswith('_pt'): _titleX = 'Jet p_{T} [GeV]'
      elif key.endswith('_eta'): _titleX = 'Jet #eta'
      elif key.endswith('_mass'): _titleX = 'Jet mass [GeV]'
      elif key.endswith('_dRmatch'): _titleX = '#DeltaR'
      elif key.endswith('_numberOfDaughters'): _titleX = 'Number of jet constituents'
      elif key.endswith('_njets'): _titleX = 'Number of jets'
      elif key.endswith('_chargedHadronEnergyFraction'): _titleX = 'Charged-Hadron Energy Fraction'
      elif key.endswith('_chargedHadronMultiplicity'): _titleX = 'Charged-Hadron Multiplicity'
      elif key.endswith('_neutralHadronEnergyFraction'): _titleX = 'Neutral-Hadron Energy Fraction'
      elif key.endswith('_neutralHadronMultiplicity'): _titleX = 'Neutral-Hadron Multiplicity'
      elif key.endswith('_electronEnergyFraction'): _titleX = 'Electron Energy Fraction'
      elif key.endswith('_electronMultiplicity'): _titleX = 'Electron Multiplicity'
      elif key.endswith('_photonEnergyFraction'): _titleX = 'Photon Energy Fraction'
      elif key.endswith('_photonMultiplicity'): _titleX = 'Photon Multiplicity'
      elif key.endswith('_muonEnergyFraction'): _titleX = 'Muon Energy Fraction'
      elif key.endswith('_muonMultiplicity'): _titleX = 'Muon Multiplicity'
      elif key.endswith('_pt_overGEN'): _titleX = 'p_{T} / p_{T}^{GEN}'
      elif key.endswith('_pt_overOffline'): _titleX = 'p_{T} / p_{T}^{Offl}'
      elif key.endswith('_mass_overGEN'): _titleX = 'mass / mass^{GEN}'
      elif key.endswith('_mass_overOffline'): _titleX = 'mass / mass^{Offl}'

    elif ('MET' in key) and not (isProfile or isEfficiency):
      if key.endswith('_pt'): _titleX = 'MET [GeV]'
      elif key.endswith('_phi'): _titleX = 'MET #phi'
      elif key.endswith('_sumEt'): _titleX = 'Sum-E_{T} [GeV]'
      elif key.endswith('_sumEt_overGEN'): _titleX = 'Sum-E_{T} / Sum-E_{T}^{GEN}'
      elif key.endswith('_sumEt_overOffline'): _titleX = 'Sum-E_{T} / Sum-E_{T}^{Offl}'
      elif key.endswith('_deltaPhiGEN'): _titleX = '#Delta#phi^{GEN}'
      elif key.endswith('_deltaPhiOffline'): _titleX = '#Delta#phi^{Offl}'
      elif key.endswith('_pt_overGEN'): _titleX = 'MET / MET^{GEN}'
      elif key.endswith('_pt_overOffline'): _titleX = 'MET / MET^{Offl}'
      elif key.endswith('_pt_paraToGEN'): _titleX = 'p_{T}^{#parallel GEN} [GeV]'
      elif key.endswith('_pt_paraToOffline'): _titleX = 'p_{T}^{#parallel Offl} [GeV]'
      elif key.endswith('_pt_paraToGENMinusGEN'): _titleX = 'p_{T}^{#parallel GEN} - p_{T}^{GEN} [GeV]'
      elif key.endswith('_pt_paraToOfflineMinusOffline'): _titleX = 'p_{T}^{#parallel Offl} - p_{T}^{Offl} [GeV]'
      elif key.endswith('_pt_perpToGEN'): _titleX = 'p_{T}^{#perp GEN} [GeV]'
      elif key.endswith('_pt_perpToOffline'): _titleX = 'p_{T}^{#perp Offl} [GeV]'

    return _titleX, _titleY, _objLabel

class PlotConfig:
    def __init__(self):
        self.hists = []
        self.IsProfile = False
        self.IsEfficiency = False
        self.logY = False
        self.titleX = ''
        self.titleY = ''
        self.objLabel = ''
#        self.divideByBinWidth = False
#        self.normalizedToUnity = False
        self.legXY = [0.75, 0.60, 0.95, 0.90]
        self.ratio = True
        self.autoRangeX = True
        self.outputName = 'tmp'

def getHistogram(key, inputDict, plotCfg, **kwargs):

    Legend      = kwargs.get('Legend'     , inputDict['Legend'])
    Color       = kwargs.get('Color'      , inputDict['LineColor'])
    LineWidth   = kwargs.get('LineStyle'  , 2)
    LineStyle   = kwargs.get('LineStyle'  , inputDict['LineStyle'])
    MarkerStyle = kwargs.get('MarkerStyle', inputDict['MarkerStyle'])
    MarkerSize  = kwargs.get('MarkerSize' , inputDict['MarkerSize'])

    if key not in inputDict['TH1s']:
       return None

    h0 = inputDict['TH1s'][key].Clone()

    if h0.InheritsFrom('TH2'):
       return None

    h0.UseCurrentStyle()
    if hasattr(h0, 'SetDirectory'):
       h0.SetDirectory(0)

    h0.SetLineColor(Color)
    h0.SetLineWidth(2)
    h0.SetLineStyle(1 if (plotCfg.IsProfile or plotCfg.IsEfficiency) else LineStyle)
    h0.SetMarkerStyle(MarkerStyle)
    h0.SetMarkerColor(Color)
    h0.SetMarkerSize(MarkerSize if (plotCfg.IsProfile or plotCfg.IsEfficiency) else 0.)

    h0.SetBit(ROOT.TH1.kNoTitle)

    if hasattr(h0, 'SetStats'):
       h0.SetStats(0)

    hist0 = Histogram()
    hist0.th1 = h0
    hist0.draw = 'ep' if (plotCfg.IsProfile or plotCfg.IsEfficiency) else 'hist,e0'
    hist0.draw += ',same'
    hist0.Legend = Legend
    hist0.LegendDraw = 'ep' if (plotCfg.IsProfile or plotCfg.IsEfficiency) else 'l'

    return hist0

def getPlotConfig(key, keyword, inputList):

    cfg = PlotConfig()

    key_basename = os.path.basename(key)
    key_dirname = os.path.dirname(key)

    cfg.outputName = key

    cfg.IsProfile = '_wrt_' in key_basename

    cfg.IsEfficiency = key_basename.endswith('_eff')

    cfg.logY = ('_NotMatchedTo' in key_basename) and key_basename.endswith('pt_eff')

    cfg.titleX, cfg.titleY, cfg.objLabel = getPlotLabels(key=key_basename, isProfile=cfg.IsProfile, isEfficiency=cfg.IsEfficiency, keyword=keyword)

    objLabel_repl = ''

    cfg.hists = []

    if keyword == 'phase2_jme_compareTRK1':
       pass
###       if 'hltPFMET_' in key:
###          objLabel_repl = 'hltPFMET'
###          histCfgList = [
####           ('offlinePFMET_Raw'   , ROOT.kPink+3  , [inputList[0]]),
###            ('offlinePuppiMET_Raw', ROOT.kPink+1  , [inputList[0]]),
###            ('hltPFClusterMET'    , ROOT.kOrange+1, [inputList[0]]),
###            ('hltPFMET'           , ROOT.kBlack   ,  inputList    ),
###            ('PFSoftKillerMET'    , ROOT.kBlue    ,  inputList    ),
###            ('hltPFCHSMET'        , ROOT.kViolet  ,  inputList    ),
###            ('hltPuppiMET'        , ROOT.kRed     ,  inputList    ),
###          ]
###       elif 'hltAK4PFJets_' in key:
###          objLabel_repl = 'hltAK4PFJets'
###          histCfgList = [
###            ('hltAK4CaloJets'     , ROOT.kGray+1  , [inputList[0]]),
###            ('hltAK4PFClusterJets', ROOT.kOrange+1, [inputList[0]]),
###            ('hltAK4PFJets'       , ROOT.kBlack   ,  inputList    ),
####           ('hltAK4PFCHSJets'    , ROOT.kViolet  ,  inputList    ),
###            ('hltAK4PuppiJets'    , ROOT.kRed     ,  inputList    ),
###          ]
###       elif 'hltAK4PFJetsCorrected_' in key:
###          objLabel_repl = 'hltAK4PFJetsCorrected'
###          histCfgList = [
####           ('offlineAK4PuppiJetsCorrected', ROOT.kPink+1  , [inputList[0]]),
####           ('hltAK4CaloJets'              , ROOT.kGray+1  , [inputList[0]]),
####           ('hltAK4PFClusterJets'         , ROOT.kOrange+1, [inputList[0]]),
###            ('hltAK4PFJetsCorrected'       , ROOT.kBlack   ,  inputList    ),
###            ('hltAK4PFCHSJetsCorrected'    , ROOT.kViolet  ,  inputList    ),
###            ('hltAK4PuppiJetsCorrected'    , ROOT.kRed     ,  inputList    ),
###          ]
###       elif 'hltAK8PFJets_' in key:
###          objLabel_repl = 'hltAK8PFJets'
###          histCfgList = [
###            ('hltAK8CaloJets'     , ROOT.kGray+1  , [inputList[0]]),
###            ('hltAK8PFClusterJets', ROOT.kOrange+1, [inputList[0]]),
###            ('hltAK8PFJets'       , ROOT.kBlack   ,  inputList    ),
####           ('hltAK8PFCHSJets'    , ROOT.kViolet  ,  inputList    ),
###            ('hltAK8PuppiJets'    , ROOT.kRed     ,  inputList    ),
###          ]
###       elif 'hltAK8PFJetsCorrected_' in key:
###          objLabel_repl = 'hltAK8PFJetsCorrected'
###          histCfgList = [
####           ('offlineAK8PuppiJetsCorrected', ROOT.kPink+1  , [inputList[0]]),
####           ('hltAK8CaloJets'              , ROOT.kGray+1  , [inputList[0]]),
####           ('hltAK8PFClusterJets'         , ROOT.kOrange+1, [inputList[0]]),
###            ('hltAK8PFJetsCorrected'       , ROOT.kBlack   ,  inputList    ),
###            ('hltAK8PFCHSJetsCorrected'    , ROOT.kViolet  ,  inputList    ),
###            ('hltAK8PuppiJetsCorrected'    , ROOT.kRed     ,  inputList    ),
###          ]
###       elif 'MatchedToPF_' in key:
###          objLabel_repl = 'PF'
###          histCfgList = [
###            ('Calo'     , ROOT.kGray+1  , [inputList[0]]),
###            ('PFCluster', ROOT.kOrange+1, [inputList[0]]),
###            ('PF'       , ROOT.kBlack   ,  inputList    ),
####           ('PFCHS'    , ROOT.kViolet  ,  inputList    ),
###            ('Puppi'    , ROOT.kRed     ,  inputList    ),
###          ]
###       elif 'MatchedToPFCorr_' in key:
###          objLabel_repl = 'PFCorr'
###          histCfgList = [
####           ('OfflinePuppiCorr', ROOT.kPink+1  , [inputList[0]]),
####           ('Calo'            , ROOT.kGray+1  , [inputList[0]]),
####           ('PFCluster'       , ROOT.kOrange+1, [inputList[0]]),
###            ('PFCorr'          , ROOT.kBlack   ,  inputList    ),
###            ('PFCHSCorr'       , ROOT.kViolet  ,  inputList    ),
###            ('PuppiCorr'       , ROOT.kRed     ,  inputList    ),
###          ]

    ##
    ## keyword: phase2_dqm_compareTRK2
    ##
    elif keyword == 'phase2_dqm_compareTRK2':

       if key.endswith('pfcand_pt_2'):
          cfg.logY, cfg.xMin, cfg.xMax = True, 0., 100.

       skip_key = False
       for _pfTypeTag in ['_h', '_e', '_mu', '_gamma', '_h0']:
          if key_dirname.endswith(_pfTypeTag) and key_basename.startswith('pfcand_mult_') and (not key_basename.endswith(_pfTypeTag)):
             skip_key = True
             break
       if skip_key:
          return

       if ('_particleFlowTmp/' in key) or ('_particleFlowTmp_' in key):
        cfg.legXY = [0.55, 0.70, 0.99, 0.99]
        cfg.outputName = key.replace('_particleFlowTmp', '')
        for idx, inp in enumerate(inputList):
          legTag = '[ '+inp['Legend']+' ] '
          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_particleFlowTmp', '_offlineParticleFlow'), Legend=       'Offline PF'     , Color=ROOT.kPink+1) if idx==0 else None]
          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_particleFlowTmp', '_simPFProducer')      , Legend=legTag+'simPFProducer'  , Color=ROOT.kOrange+1)]
          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_particleFlowTmp', '_pfTICL')             , Legend=legTag+'pfTICL'         , Color=ROOT.kBlue)]
          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_particleFlowTmp', '_particleFlowTmp')    , Legend=legTag+'particleFlowTmp', Color=ROOT.kBlack)]
#         cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_particleFlowTmp', '_hltPuppi')           , Legend=legTag+'hltPuppi'       , Color=ROOT.kRed)]

    ##
    ## keyword: run3_dqm_compareTRK2
    ##
    elif keyword == 'run3_dqm_compareTRK2':

       if key.endswith('pfcand_pt_2'):
          cfg.logY, cfg.xMin, cfg.xMax = True, 0., 100.

       skip_key = False
       for _pfTypeTag in ['_h', '_e', '_mu', '_gamma', '_h0']:
          if key_dirname.endswith(_pfTypeTag) and key_basename.startswith('pfcand_mult_') and (not key_basename.endswith(_pfTypeTag)):
             skip_key = True
             break
       if skip_key:
          return

       if ('_hltParticleFlow/' in key) or ('_hltParticleFlow_' in key):
         cfg.legXY = [0.55, 0.50, 0.99, 0.99]
         cfg.outputName = key.replace('_hltParticleFlow', '')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_offlineParticleFlow') , Legend='Offline PF'            , Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_hltParticleFlow')     , Legend='hltParticleFlow'+legTag, Color=ROOT.kBlack)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_hltParticleFlowCHSv1'), Legend='hltPFCHSv1'     +legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_hltParticleFlowCHSv2'), Legend='hltPFCHSv2'     +legTag, Color=ROOT.kViolet)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_hltPuppiV1')          , Legend='hltPuppiV1'     +legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_hltPuppiV3')          , Legend='hltPuppiV3'     +legTag, Color=ROOT.kRed)]

       elif '_hltPixelTracks' in key:
         cfg.legXY = [0.55, 0.75, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPixelTracks'+legTag)]

       elif '_hltMergedTracks' in key:
         cfg.legXY = [0.45, 0.70, 0.99, 0.99]
         cfg.outputName = key.replace('_hltMergedTracks', '')
         iter0Tracks = 'hltIter0PFlowTrackSelectionHighPurity'
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltMergedTracks', '_hltMergedTracks'), Legend='hltMergedTracks'+legTag) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltMergedTracks', '_'+iter0Tracks), Legend=iter0Tracks+legTag) if (idx != 0) else None]

       elif '_hltPixelVertices' in key:
         cfg.legXY = [0.55, 0.70, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltPixelVertices', '_offlineSlimmedPrimaryVertices'), Legend='offlinePrimaryVertices', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltPixelVertices', '_hltPixelVertices'), Legend='hltPixelVertices'+legTag)]

       elif '_hltVerticesPF' in key:
         cfg.legXY = [0.55, 0.70, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltVerticesPF', '_offlineSlimmedPrimaryVertices'), Legend='offlinePrimaryVertices', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltVerticesPF', '_hltVerticesPF'), Legend='hltVerticesPF'+legTag)]

    ##
    ## keyword: run3_dqm_compareTRK5
    ##
    elif keyword == 'run3_dqm_compareTRK5':

       if key.endswith('pfcand_pt_2'):
          cfg.logY, cfg.xMin, cfg.xMax = True, 0., 100.

       skip_key = False
       for _pfTypeTag in ['_h', '_e', '_mu', '_gamma', '_h0']:
          if key_dirname.endswith(_pfTypeTag) and key_basename.startswith('pfcand_mult_') and (not key_basename.endswith(_pfTypeTag)):
             skip_key = True
             break
       if skip_key:
          return

       if ('_hltParticleFlow/' in key) or ('_hltParticleFlow_' in key):
         cfg.legXY = [0.55, 0.60, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_offlineParticleFlow'), Legend='Offline PF', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltParticleFlow'+legTag)]

       elif '_hltPuppiV1' in key:
         cfg.legXY = [0.55, 0.60, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltPuppiV1', '_offlineParticleFlow'), Legend='Offline PF', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPuppiV1'+legTag)]

       elif '_hltPuppiV3' in key:
         cfg.legXY = [0.55, 0.60, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltPuppiV3', '_offlineParticleFlow'), Legend='Offline PF', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPuppiV3'+legTag)]

       elif '_hltVerticesPF' in key:
         cfg.legXY = [0.45, 0.70, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltVerticesPF', '_offlineSlimmedPrimaryVertices'), Legend='offlinePrimaryVertices', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltVerticesPF', '_hltPixelVertices'), Legend='hltPixelVertices'+legTag, Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltVerticesPF'+legTag)]

       elif '_hltMergedTracks' in key:
         cfg.legXY = [0.45, 0.70, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltMergedTracks'+legTag, Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltMergedTracks', '_hltIter0PFlowTrackSelectionHighPurity'), Legend='hltIter0PFlowTrackSelectionHighPurity'+legTag)]

    ##
    ## keyword: run3_jme_compareTRK1
    ##
    elif keyword == 'run3_jme_compareTRK1':

#       if ('_wrt_' not in key_basename) and (not key_basename.endswith('_eff')) and \
#          (not ('MET' in key_basename and key_basename.endswith('_pt'))) and \
#          ('pt_over' not in key_basename):
#          return

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       cfg.legXY = [0.55, 0.40, 0.95, 0.90]

       if 'hltPFMET_' in key:
         cfg.objLabel = cfg.objLabel.replace('hltPFMET', 'MET')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFMET_Raw_')   , Legend='Offline PFMET'       , Color=ROOT.kGreen+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePuppiMET_Raw_'), Legend='Offline PuppiMET'    , Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltCaloMET_')         , Legend='hltCaloMET'          , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFClusterMET_')    , Legend='hltPFClusterMET'     , Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFMET_')           , Legend='hltPFMET'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFCHSv1MET_')      , Legend='hltPFCHSv1MET'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFCHSv2MET_')      , Legend='hltPFCHSv2MET'+legTag, Color=ROOT.kViolet)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPuppiV2MET_')      , Legend='hltPuppiV1MET'+legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPuppiV4MET_')      , Legend='hltPuppiV3MET'+legTag, Color=ROOT.kRed)]

       elif 'hltAK4PFJets_' in key:
         baseColl = 'hltAK4PFJets'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK4')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4CaloJets_')     , Legend='hltAK4CaloJets'          , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFClusterJets_'), Legend='hltAK4PFClusterJets'     , Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFJets_')       , Legend='hltAK4PFJets'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFCHSv1Jets_')  , Legend='hltAK4PFCHSv1Jets'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFCHSv2Jets_')  , Legend='hltAK4PFCHSv2Jets'+legTag, Color=ROOT.kViolet)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PuppiV1Jets_')  , Legend='hltAK4PuppiV1Jets'+legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PuppiV3Jets_')  , Legend='hltAK4PuppiV3Jets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'hltAK4PFJetsCorrected_' in key:
         baseColl = 'hltAK4PFJetsCorrected'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK4+JECs')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK4PuppiJetsCorrected_'), Legend='offlineAK4PuppiJetsCorrected', Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4CaloJetsCorrected_')     , Legend='hltAK4CaloJetsCorrected'     , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFJetsCorrected_')       , Legend='hltAK4PFJetsCorrected'+legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFCHSv1Jets_')  , Legend='hltAK4PFCHSv1Jets'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFCHSv2Jets_')  , Legend='hltAK4PFCHSv2Jets'+legTag, Color=ROOT.kViolet)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PuppiV1Jets_')  , Legend='hltAK4PuppiV1Jets'+legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PuppiV3Jets_')  , Legend='hltAK4PuppiV3Jets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'hltAK8PFJets_' in key:
         baseColl = 'hltAK8PFJets'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK8')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8CaloJets_')     , Legend='hltAK8CaloJets'          , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFClusterJets_'), Legend='hltAK8PFClusterJets'     , Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFJets_')       , Legend='hltAK8PFJets'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFCHSv1Jets_')  , Legend='hltAK8PFCHSv1Jets'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFCHSv2Jets_')  , Legend='hltAK8PFCHSv2Jets'+legTag, Color=ROOT.kViolet)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PuppiV1Jets_')  , Legend='hltAK8PuppiV1Jets'+legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PuppiV3Jets_')  , Legend='hltAK8PuppiV3Jets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'hltAK8PFJetsCorrected_' in key:
         baseColl = 'hltAK8PFJetsCorrected'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK8+JECs')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK8PuppiJetsCorrected_'), Legend='offlineAK8PuppiJetsCorrected', Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8CaloJetsCorrected_')     , Legend='hltAK8CaloJetsCorrected'     , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFJetsCorrected_')       , Legend='hltAK8PFJetsCorrected'+legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFCHSv1Jets_')  , Legend='hltAK8PFCHSv1Jets'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFCHSv2Jets_')  , Legend='hltAK8PFCHSv2Jets'+legTag, Color=ROOT.kViolet)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PuppiV1Jets_')  , Legend='hltAK8PuppiV1Jets'+legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PuppiV3Jets_')  , Legend='hltAK8PuppiV3Jets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'MatchedToPF_' in key:
         baseColl = 'PF'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'Reco(w/o JECs)')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'Offline_')  , Legend='Offline'       , Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'Calo_')     , Legend='Calo'          , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCluster_'), Legend='PFCluster'     , Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PF_')       , Legend='PF'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCHSv1_')  , Legend='PFCHSv1'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCHSv2_')  , Legend='PFCHSv2'+legTag, Color=ROOT.kViolet)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PuppiV1_')  , Legend='PuppiV1'+legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PuppiV3_')  , Legend='PuppiV3'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'MatchedToPFCorr_' in key:
         baseColl = 'PFCorr'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'Reco(+JECs)')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'OfflineCorr_')  , Legend='OfflineCorr'       , Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'CaloCorr_')     , Legend='CaloCorr'          , Color=ROOT.kGray+1)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFClusterCorr_'), Legend='PFClusterCorr'     , Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCorr_')       , Legend='PFCorr'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCHSv1_')      , Legend='PFCHSv1'    +legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCHSv2_')      , Legend='PFCHSv2'    +legTag, Color=ROOT.kViolet)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PuppiV1_')      , Legend='PuppiV1'    +legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PuppiV3_')      , Legend='PuppiV3'    +legTag, Color=ROOT.kRed)]
         del baseColl, legTag

    ##
    ## keyword: run3_jme_compareTRK2
    ##
    elif keyword == 'run3_jme_compareTRK2':

#       if ('_wrt_' not in key_basename) and (not key_basename.endswith('_eff')) and \
#          (not ('MET' in key_basename and key_basename.endswith('_pt'))) and \
#          ('pt_over' not in key_basename):
#          return

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       cfg.legXY = [0.55, 0.40, 0.95, 0.90]

       if 'hltPFMET_' in key:
         cfg.objLabel = cfg.objLabel.replace('hltPFMET', 'MET')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFMET_Raw_')   , Legend='Offline PFMET'       , Color=ROOT.kGreen+2)  if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePuppiMET_Raw_'), Legend='Offline PuppiMET'    , Color=ROOT.kPink+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltCaloMET_')         , Legend='hltCaloMET'          , Color=ROOT.kGray+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFClusterMET_')    , Legend='hltPFClusterMET'     , Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFMET_')           , Legend='hltPFMET'     +legTag, Color=ROOT.kBlack)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFCHSv1MET_')      , Legend='hltPFCHSv1MET'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFCHSv2MET_')      , Legend='hltPFCHSv2MET'+legTag, Color=ROOT.kViolet)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPuppiV2MET_')      , Legend='hltPuppiV1MET'+legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPuppiV4MET_')      , Legend='hltPuppiV3MET'+legTag, Color=ROOT.kRed)]

       elif 'hltAK4PFJets_' in key:
         baseColl = 'hltAK4PFJets'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK4')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4CaloJets_')     , Legend='hltAK4CaloJets'          , Color=ROOT.kGray+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFClusterJets_'), Legend='hltAK4PFClusterJets'     , Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFJets_')       , Legend='hltAK4PFJets'     +legTag, Color=ROOT.kBlack)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFCHSv1Jets_')  , Legend='hltAK4PFCHSv1Jets'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFCHSv2Jets_')  , Legend='hltAK4PFCHSv2Jets'+legTag, Color=ROOT.kViolet)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PuppiV1Jets_')  , Legend='hltAK4PuppiV1Jets'+legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PuppiV3Jets_')  , Legend='hltAK4PuppiV3Jets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'hltAK4PFJetsCorrected_' in key:
         baseColl = 'hltAK4PFJetsCorrected'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK4+JECs')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK4PuppiJetsCorrected_'), Legend='offlineAK4PuppiJetsCorrected', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4CaloJetsCorrected_')     , Legend='hltAK4CaloJetsCorrected'     , Color=ROOT.kGray+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFJetsCorrected_')       , Legend='hltAK4PFJetsCorrected'     +legTag, Color=ROOT.kBlack)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFCHSv1Jets_')  , Legend='hltAK4PFCHSv1Jets'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFCHSv2Jets_')  , Legend='hltAK4PFCHSv2Jets'+legTag, Color=ROOT.kViolet)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PuppiV1Jets_')  , Legend='hltAK4PuppiV1Jets'+legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PuppiV3Jets_')  , Legend='hltAK4PuppiV3Jets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'hltAK8PFJets_' in key:
         baseColl = 'hltAK8PFJets'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK8')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8CaloJets_')     , Legend='hltAK8CaloJets'          , Color=ROOT.kGray+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFClusterJets_'), Legend='hltAK8PFClusterJets'     , Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFJets_')       , Legend='hltAK8PFJets'     +legTag, Color=ROOT.kBlack)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFCHSv1Jets_')  , Legend='hltAK8PFCHSv1Jets'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFCHSv2Jets_')  , Legend='hltAK8PFCHSv2Jets'+legTag, Color=ROOT.kViolet)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PuppiV1Jets_')  , Legend='hltAK8PuppiV1Jets'+legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PuppiV3Jets_')  , Legend='hltAK8PuppiV3Jets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'hltAK8PFJetsCorrected_' in key:
         baseColl = 'hltAK8PFJetsCorrected'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK8+JECs')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK8PuppiJetsCorrected_'), Legend='offlineAK8PuppiJetsCorrected', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8CaloJetsCorrected_')     , Legend='hltAK8CaloJetsCorrected'     , Color=ROOT.kGray+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFJetsCorrected_')       , Legend='hltAK8PFJetsCorrected'     +legTag, Color=ROOT.kBlack)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFCHSv1Jets_')  , Legend='hltAK8PFCHSv1Jets'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFCHSv2Jets_')  , Legend='hltAK8PFCHSv2Jets'+legTag, Color=ROOT.kViolet)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PuppiV1Jets_')  , Legend='hltAK8PuppiV1Jets'+legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PuppiV3Jets_')  , Legend='hltAK8PuppiV3Jets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'MatchedToPF_' in key:
         baseColl = 'PF'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'Reco(w/o JECs)')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'Offline_')  , Legend='Offline'       , Color=ROOT.kPink+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'Calo_')     , Legend='Calo'          , Color=ROOT.kGray+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCluster_'), Legend='PFCluster'     , Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PF_')       , Legend='PF'     +legTag, Color=ROOT.kBlack)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCHSv1_')  , Legend='PFCHSv1'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCHSv2_')  , Legend='PFCHSv2'+legTag, Color=ROOT.kViolet)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PuppiV1_')  , Legend='PuppiV1'+legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PuppiV3_')  , Legend='PuppiV3'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'MatchedToPFCorr_' in key:
         baseColl = 'PFCorr'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'Reco(+JECs)')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'OfflineCorr_')  , Legend='OfflineCorr'       , Color=ROOT.kPink+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'CaloCorr_')     , Legend='CaloCorr'          , Color=ROOT.kGray+1)   if idx==0 else None]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFClusterCorr_'), Legend='PFClusterCorr'     , Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCorr_')       , Legend='PFCorr'     +legTag, Color=ROOT.kBlack)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCHSv1Corr_')  , Legend='PFCHSv1Corr'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCHSv2Corr_')  , Legend='PFCHSv2Corr'+legTag, Color=ROOT.kViolet)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PuppiV1Corr_')  , Legend='PuppiV1Corr'+legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PuppiV3Corr_')  , Legend='PuppiV3Corr'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

    ##
    ## keyword: run3_jme_compareTRK5
    ##
    elif keyword == 'run3_jme_compareTRK5':

#       if ('_wrt_' not in key_basename) and (not key_basename.endswith('_eff')) and \
#          (not ('MET' in key_basename and key_basename.endswith('_pt'))) and \
#          ('pt_over' not in key_basename):
#          return

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       cfg.legXY = [0.55, 0.60, 0.95, 0.90]

       ## MET
       if 'hltCaloMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCaloMET_', 'offlinePFMET_Raw_'), Legend='Offline PFMET', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltCaloMET [ '+inp['Legend']+' ]')]

       elif 'hltPFMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFMET_Raw_'), Legend='Offline PFMET', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPFMET [ '+inp['Legend']+' ]')]

       elif 'hltPFSoftKillerMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFSoftKillerMET_', 'offlinePuppiMET_Raw_'), Legend='Offline PuppiMET', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPFSoftKillerMET [ '+inp['Legend']+' ]')]

       elif 'hltPFCHSv1MET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFCHSv1MET_', 'offlinePuppiMET_Raw_'), Legend='Offline PuppiMET', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPFCHSv1MET [ '+inp['Legend']+' ]')]

       elif 'hltPFCHSv2MET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFCHSv2MET_', 'offlinePuppiMET_Raw_'), Legend='Offline PuppiMET', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPFCHSv2MET [ '+inp['Legend']+' ]')]

       elif 'hltPuppiV1MET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPuppiV1MET_', 'offlinePuppiMET_Raw_'), Legend='Offline PuppiMET', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPuppiV1MET [ '+inp['Legend']+' ]')]

       elif 'hltPuppiV2MET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPuppiV2MET_', 'offlinePuppiMET_Raw_'), Legend='Offline PuppiMET', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPuppiV1MET [ '+inp['Legend']+' ]')]

       elif 'hltPuppiV3MET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPuppiV3MET_', 'offlinePuppiMET_Raw_'), Legend='Offline PuppiMET', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPuppiV3MET [ '+inp['Legend']+' ]')]

       elif 'hltPuppiV4MET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPuppiV4MET_', 'offlinePuppiMET_Raw_'), Legend='Offline PuppiMET', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPuppiV3MET [ '+inp['Legend']+' ]')]

       ## Jets
       elif 'hltAK4PFJets_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJets_', 'offlineAK4PuppiJetsCorrected_'), Legend='Offline AK4Puppi', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltAK4PFJets [ '+inp['Legend']+' ]')]

       elif 'hltAK4PFJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PuppiJetsCorrected_'), Legend='Offline AK4Puppi', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltAK4PFJetsCorrected [ '+inp['Legend']+' ]')]

       elif 'hltAK4PFCHSv1Jets_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFCHSv1Jets_', 'offlineAK4PuppiJetsCorrected_'), Legend='Offline AK4Puppi', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltAK4PFCHSv1Jets [ '+inp['Legend']+' ]')]

       elif 'hltAK4PFCHSv2Jets_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFCHSv2Jets_', 'offlineAK4PuppiJetsCorrected_'), Legend='Offline AK4Puppi', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltAK4PFCHSv2Jets [ '+inp['Legend']+' ]')]

       elif 'hltAK4PuppiV1Jets_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PuppiV1Jets_', 'offlineAK4PuppiJetsCorrected_'), Legend='Offline AK4Puppi', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltAK4PuppiV1Jets [ '+inp['Legend']+' ]')]

       elif 'hltAK4PuppiV3Jets_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PuppiV3Jets_', 'offlineAK4PuppiJetsCorrected_'), Legend='Offline AK4Puppi', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltAK4PuppiV3Jets [ '+inp['Legend']+' ]')]

       elif 'MatchedToPF_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PF_', 'OfflineCorr_'), Legend='OfflineCorr', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF'+' [ '+inp['Legend']+' ]')]

       elif 'MatchedToPFCorr_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFCorr_', 'OfflineCorr_'), Legend='OfflineCorr', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PFCorr'+' [ '+inp['Legend']+' ]')]

       elif 'MatchedToPFCHSv1_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFCHSv1_', 'OfflineCorr_'), Legend='OfflineCorr', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PFCHSv1'+' [ '+inp['Legend']+' ]')]

       elif 'MatchedToPFCHSv2_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFCHSv2_', 'OfflineCorr_'), Legend='OfflineCorr', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PFCHSv2'+' [ '+inp['Legend']+' ]')]

       elif 'MatchedToPuppiV1_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PuppiV1_', 'OfflineCorr_'), Legend='OfflineCorr', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PuppiV1'+' [ '+inp['Legend']+' ]')]

       elif 'MatchedToPuppiV3_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PuppiV3_', 'OfflineCorr_'), Legend='OfflineCorr', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PuppiV3'+' [ '+inp['Legend']+' ]')]

    else:
#       KILL('getPlotConfig(key="'+key+'", keyword="'+keyword+'") -- invalid keyword: "'+keyword+'"')

       if key.endswith('jet_pt'):
          cfg.logY = True

       cfg.legXY = [0.50, 0.70, 0.99, 0.99]
       for idx, inp in enumerate(inputList):
         cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key)]

    # remove None entries
    cfg.hists = list(filter(None, cfg.hists))

    if len(cfg.hists) < 2:
       return None

    usedDivideByBinWidth = False

    if not (cfg.IsProfile or cfg.IsEfficiency):
       for cfg_h in cfg.hists:

          divideByBinWidth = False
          _tmpBW = None
          for _tmp in range(1, cfg_h.th1.GetNbinsX()+1):
              if _tmpBW is None:
                 _tmpBW = cfg_h.th1.GetBinWidth(_tmp)
              elif (abs(_tmpBW-cfg_h.th1.GetBinWidth(_tmp))/max(abs(_tmpBW), abs(cfg_h.th1.GetBinWidth(_tmp)))) > 1e-4:
                 divideByBinWidth = True
                 break
          if divideByBinWidth:
             cfg_h.th1.Scale(1., 'width')
             usedDivideByBinWidth = True

          normalizedToUnity = False
          if normalizedToUnity:
             cfg_h.th1.Scale(1. / cfg_h.th1.Integral())

    if usedDivideByBinWidth:
       cfg.titleY += ' / Bin width'

    return cfg

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser()

   parser.add_argument('-i', '--inputs', dest='inputs', nargs='+', default=[], required=True,
                       help='list of input files [format: "PATH:LEGEND:LINECOLOR:LINESTYLE:MARKERSTYLE:MARKERCOLOR:MARKERSIZE"]')

   parser.add_argument('-o', '--output', dest='output', action='store', default=None, required=True,
                       help='path to output directory')

   parser.add_argument('-k', '--keywords', dest='keywords', nargs='+', default=[], required=True,
                       help='keywords for plot configuration')

   parser.add_argument('-m', '--matches', dest='matches', nargs='+', default=[],
                       help='list of matching-patterns to skim input histograms (input is a match if its name matches any of the specified patterns)')

   parser.add_argument('-s', '--skip', dest='skip', nargs='+', default=[],
                       help='list of matching-patterns to skip input histograms (input is skipped if its name matches any of the specified patterns)')

   parser.add_argument('-l', '--label', dest='label', action='store', default='',
                       help='text label (displayed in top-left corner)')

   parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['pdf'],
                       help='list of extension(s) for output file(s)')

   parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', const=1, type=int, default=0,
                       help='verbosity level')

   opts, opts_unknown = parser.parse_known_args()
   ### -------------------

   ROOT.gROOT.SetBatch()
   ROOT.gErrorIgnoreLevel = ROOT.kWarning

   log_prx = os.path.basename(__file__)+' -- '

   ### args validation ---
   if len(opts_unknown) > 0:
      KILL(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))

   if os.path.exists(opts.output):
      KILL(log_prx+'target path to output directory already exists [-o]: '+opts.output)

   OUTDIR = os.path.abspath(os.path.realpath(opts.output))

   KEYWORDS = sorted(list(set(opts.keywords)))

   MATCHES = sorted(list(set(opts.matches)))
   MATCHES = [_tmp.replace('\'','').replace('"','') for _tmp in MATCHES]

   SKIP = sorted(list(set(opts.skip)))
   SKIP = [_tmp.replace('\'','').replace('"','') for _tmp in SKIP]

   EXTS = list(set(opts.exts))
   ### -------------------

   inputList = []
   th1Keys = []
   for _input in opts.inputs:
       _input_pieces = _input.split(':')
       if len(_input_pieces) >= 3:
          print('reading..', os.path.relpath(_input_pieces[0]))
          _tmp = {}
          _tmp['TH1s'] = getTH1sFromTFile(_input_pieces[0], matches=MATCHES, skip=SKIP, verbose=(opts.verbosity > 20))
          th1Keys += _tmp['TH1s'].keys()
          _tmp['Legend'] = _input_pieces[1]
          _tmp['LineColor'] = int(_input_pieces[2])
          _tmp['LineStyle'] = int(_input_pieces[3]) if len(_input_pieces) >= 4 else 1
          _tmp['MarkerStyle'] = int(_input_pieces[4]) if len(_input_pieces) >= 5 else 20
          _tmp['MarkerColor'] = int(_input_pieces[5]) if len(_input_pieces) >= 6 else int(_input_pieces[2])
          _tmp['MarkerSize'] = float(_input_pieces[6]) if len(_input_pieces) >= 7 else 1.0
          inputList.append(_tmp)
       else:
          KILL(log_prx+'argument of --inputs has invalid format: '+_input)

   if not inputList:
      raise SystemExit(0)

   th1Keys = sorted(list(set(th1Keys)))

   apply_style(0)

   ROOT.TGaxis.SetMaxDigits(4)

   Top = ROOT.gStyle.GetPadTopMargin()
   Rig = ROOT.gStyle.GetPadRightMargin()
   Bot = ROOT.gStyle.GetPadBottomMargin()
   Lef = ROOT.gStyle.GetPadLeftMargin()

   ROOT.TGaxis.SetExponentOffset(-Lef+.50*Lef, 0.03, 'y')

   label_sample = get_text(Lef+(1-Lef-Rig)*0.00, (1-Top)+Top*0.25, 11, .035, opts.label)

   for _hkey in th1Keys:

       for _keyw in KEYWORDS:

           _plotConfig = getPlotConfig(key=_hkey, keyword=_keyw, inputList=inputList)

           if _plotConfig is None:
              continue

           ## labels and axes titles
           label_obj = get_text(Lef+(1-Rig-Lef)*0.95, Bot+(1-Top-Bot)*0.925, 31, .035, _plotConfig.objLabel)
           _labels = [label_sample, label_obj]

           _htitle = ';'+_plotConfig.titleX+';'+_plotConfig.titleY

           ## plot
           plot(**{
             'histograms': _plotConfig.hists,
             'title': _htitle,
             'labels': _labels,
             'legXY': [Lef+(1-Rig-Lef)*_plotConfig.legXY[0], Bot+(1-Bot-Top)*_plotConfig.legXY[1], Lef+(1-Rig-Lef)*_plotConfig.legXY[2], Bot+(1-Bot-Top)*_plotConfig.legXY[3]],
             'outputs': [OUTDIR+'/'+_plotConfig.outputName+'.'+_tmp for _tmp in EXTS],
             'ratio': _plotConfig.ratio,
             'logY': _plotConfig.logY,
             'autoRangeX': _plotConfig.autoRangeX,
           })

           del _plotConfig
