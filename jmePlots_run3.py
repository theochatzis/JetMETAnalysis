#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import ROOT

from common.utils import *
from common.th1 import *
from common.efficiency import *
from common.plot import *
from common.plot_style import *

def clone_histogram(histograms, tag1, tag2, setters={}):

    if tag1 not in histograms:
       return None

    if tag2 not in histograms[tag1]:
       return None

    h0 = histograms[tag1][tag2].Clone()
    h0.UseCurrentStyle()
    h0.SetDirectory(0)

    h0 = th1_mergeUnderflowBinIntoFirstBin(h0)
    h0 = th1_mergeOverflowBinIntoLastBin(h0)

    # defaults
    h0.SetMarkerSize(0)
    h0.SetLineWidth(2)

    for i_set in setters:
        if hasattr(h0, 'Set'+i_set):
           getattr(h0, 'Set'+i_set)(setters[i_set])

    return h0

def clone_graph(graphs, tag1, tag2, setters={}, verbose=False):

    if tag1 not in graphs:
       if verbose: WARNING('clone_graph -- will skip graphs["'+tag1+'"]["'+tag2+'"] (key "'+tag1+'" not found')
       return None

    if tag2 not in graphs[tag1]:
       if verbose: WARNING('clone_graph -- will skip graphs["'+tag1+'"]["'+tag2+'"] (key "'+tag2+'" not found')
       return None

    g0 = graphs[tag1][tag2].Clone()
    g0.UseCurrentStyle()
#    g0.SetDirectory(0)

    g0.SetMarkerSize(0)

    for i_set in setters:
        if hasattr(g0, 'Set'+i_set):
           getattr(g0, 'Set'+i_set)(setters[i_set])

    return g0

def updateDictionary(dictionary, TDirectory, prefix='', verbose=False):

    key_prefix = ''
    if len(prefix) > 0: key_prefix = prefix+'/'

    for j_key in TDirectory.GetListOfKeys():

        j_key_name = j_key.GetName()

        j_obj = TDirectory.Get(j_key_name)

        if j_obj.InheritsFrom('TDirectory'):

           updateDictionary(dictionary, j_obj, prefix=key_prefix+j_key_name, verbose=verbose)

        elif j_obj.InheritsFrom('TH1'):

           out_key = key_prefix+j_key_name

           if out_key in dictionary:
              KILL(log_prx+'input error -> found duplicate of template ["'+out_key+'"] in input file: '+TDirectory.GetName())

           dictionary[out_key] = j_obj.Clone()
           dictionary[out_key].SetDirectory(0)

           if verbose:
              print(colored_text('[input]', ['1','92']), out_key)

    return dictionary

def getTH1sFromTFile(path, verbose=False):

    input_histos_dict = {}

    i_inptfile = ROOT.TFile.Open(path)
    if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered):
       return input_histos_dict

    updateDictionary(input_histos_dict, i_inptfile, prefix='', verbose=verbose)

    i_inptfile.Close()

    return input_histos_dict

class Histogram:
    def __init__(self):
        self.th1 = None
        self.draw = ''
        self.legendName = ''
        self.legendDraw = ''

def plot(canvas, histograms, outputs, title, labels, legXY=[], ratio=False, ratioPadFrac=0.3, xMin=None, xMax=None, yMin=None, yMax=None, logX=False, logY=False):

    h00 = histograms[0].th1
    nvalid_histograms = len(histograms)

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
              leg.AddEntry(_tmp.th1, _tmp.legendName, _tmp.legendDraw)

    canvas.cd()

    XMIN, XMAX = xMin, xMax
    if XMIN is None: XMIN = h00.GetBinLowEdge(1)
    if XMAX is None: XMAX = h00.GetBinLowEdge(1+h00.GetNbinsX())

    HMAX = 0.0
    for _tmp in histograms:
        if (_tmp.th1 is not None) and hasattr(_tmp.th1, 'GetNbinsX'):
           for i_bin in range(1, _tmp.th1.GetNbinsX()+1):
               HMAX = max(HMAX, (_tmp.th1.GetBinContent(i_bin) + _tmp.th1.GetBinError(i_bin)))

    YMIN, YMAX = yMin, yMax
    if YMIN is None: YMIN = .0003 if logY else .0001
    if YMAX is None: YMAX = .0003*((HMAX/.0003)**(1./.85)) if logY else .0001+((HMAX-.0001) *(1./.85))

    h0 = canvas.DrawFrame(XMIN, YMIN, XMAX, YMAX)

    if not ratio:

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

       h11 = None
       for _tmp in histograms:
           if _tmp.th1 is not None:
              if h11 is None: h11 = _tmp.th1
              _tmp.th1.Draw(_tmp.draw)

       if not h11: return 1

       h11.Draw('axis,same')
       h11.GetXaxis().SetTitle('')
       h11.GetYaxis().SetTitle(title.split(';')[2])
       h11.GetXaxis().SetRangeUser(XMIN, XMAX)

       h11.GetYaxis().SetTitleSize(h11.GetYaxis().GetTitleSize()/pad1H)
       h11.GetYaxis().SetTitleOffset(h11.GetYaxis().GetTitleOffset()*pad1H)
       h11.GetXaxis().SetLabelSize(0)
       h11.GetYaxis().SetLabelSize (h11.GetYaxis().GetLabelSize() /pad1H)
       h11.GetXaxis().SetTickLength(h11.GetXaxis().GetTickLength()/pad1H)

       if YMIN is None: YMIN = .0003 if logY else .0001
       if YMAX is None: YMAX = .0003*((HMAX/.0003)**(1./.85)) if logY else .0001+((HMAX-.0001) *(1./.85))

       h11.GetYaxis().SetRangeUser(YMIN, YMAX)

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
       for _tmp in range(0, denom.GetNbinsX()+2): denom.SetBinError(_tmp, 0.)

       h21 = None

       plot_ratios = []

       for _tmp in histograms:

           histo = Histogram()
           if _tmp.th1 is not None:
              histo.th1 = _tmp.th1.Clone()
              histo.th1.Divide(denom)

           histo.draw = _tmp.draw
           if 'same' not in histo.draw: histo.draw += ',same'

           histo.legendName = _tmp.legendName
           histo.legendDraw = _tmp.legendDraw

           if hasattr(histo.th1, 'SetStats'):
              histo.th1.SetStats(0)

           if h21 is None:
              h21 = histo.th1

           plot_ratios += [histo]

       ROOT.SetOwnership(pad2, False)

       pad2.cd()

       h21.SetFillStyle(3017)
       h21.SetFillColor(16)

       h21.GetXaxis().SetTitle(title.split(';')[1])
       h21.GetYaxis().SetTitle('Ratio')
       h21.GetYaxis().CenterTitle()
       h21.GetXaxis().SetTitleSize(h21.GetXaxis().GetTitleSize()/(1-pad1H))
       h21.GetYaxis().SetTitleSize(h21.GetYaxis().GetTitleSize()/(1-pad1H)*pad1H)
       h21.GetXaxis().SetTitleOffset(h21.GetXaxis().GetTitleOffset())
       h21.GetYaxis().SetTitleOffset(h21.GetYaxis().GetTitleOffset()*(1-pad1H)/pad1H)
       h21.GetXaxis().SetLabelSize(h21.GetYaxis().GetLabelSize()/(1-pad1H)*pad1H)
       h21.GetYaxis().SetLabelSize(h21.GetYaxis().GetLabelSize()/(1-pad1H)*pad1H)
       h21.GetXaxis().SetTickLength(h21.GetXaxis().GetTickLength()/(1-pad1H)*pad1H)
       h21.GetXaxis().SetLabelOffset(h21.GetXaxis().GetLabelOffset()/(1-pad1H))
       h21.GetYaxis().SetLabelOffset(h21.GetYaxis().GetLabelOffset())
       h21.GetYaxis().SetNdivisions(404)

       h21.GetXaxis().SetRangeUser(XMIN, XMAX)

       h2max, h2min = None, None
       for _tmp in plot_ratios:
           if _tmp.th1 is None: continue
           for _tmpb in range(1, _tmp.th1.GetNbinsX()+1):
               if (abs(_tmp.th1.GetBinContent(_tmpb)) > 1e-7) and (abs(_tmp.th1.GetBinError(_tmpb)) > 1e-7):
                  h2max = max(h2max, _tmp.th1.GetBinContent(_tmpb)+_tmp.th1.GetBinError(_tmpb)) if h2max is not None else _tmp.th1.GetBinContent(_tmpb)+_tmp.th1.GetBinError(_tmpb)
                  h2min = min(h2min, _tmp.th1.GetBinContent(_tmpb)-_tmp.th1.GetBinError(_tmpb)) if h2min is not None else _tmp.th1.GetBinContent(_tmpb)-_tmp.th1.GetBinError(_tmpb)
       if (h2max is not None) and (h2min is not None):
          h2min = min(int(h2min*105.)/100., int(h2min*95.)/100.)
          h2max = max(int(h2max*105.)/100., int(h2max*95.)/100.)
          h21.GetYaxis().SetRangeUser(h2min, h2max)

       h21.Draw('e2')
       for _tmp in plot_ratios:
           if _tmp.th1 == h21: continue
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

    return 0

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser()

   parser.add_argument('-i', '--inputs', dest='inputs', nargs='+', default=[], required=True,
                       help='list of input files [format: "PATH:LEGEND:LINECOLOR:LINESTYLE:MARKERSTYLE:MARKERCOLOR:MARKERSIZE"]')

   parser.add_argument('-o', '--output', dest='output', action='store', default=None, required=True,
                       help='path to output directory')

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
   INPUTS = []

   if os.path.exists(opts.output):
      KILL(log_prx+'target path to output directory already exists [-o]: '+opts.output)

   OUTDIR = os.path.abspath(os.path.realpath(opts.output))

   if len(opts_unknown) > 0:
      KILL(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))

   EXTS = list(set(opts.exts))
   ### -------------------

   inputList = []
   th1Keys = []
   for _input in opts.inputs:
       _input_pieces = _input.split(':')
       _input_pieces = [_tmp for _tmp in _input_pieces if _tmp]
       if len(_input_pieces) >= 3:
          _tmp = {}
          _tmp['TH1s'] = getTH1sFromTFile(_input_pieces[0], verbose=(opts.verbosity > 20))
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

   th1Keys = sorted(list(set(th1Keys)))

   apply_style(0)

   ROOT.TGaxis.SetMaxDigits(4)

   canvas = ROOT.TCanvas()
   canvas.SetGrid(1,1)
   canvas.SetTickx()
   canvas.SetTicky()

   Top = canvas.GetTopMargin()
   Rig = canvas.GetRightMargin()
   Bot = canvas.GetBottomMargin()
   Lef = canvas.GetLeftMargin()

   ROOT.TGaxis.SetExponentOffset(-Lef+.50*Lef, 0.03, 'y')

   label_sample = get_text(Lef+(1-Lef-Rig)*0.00, (1-Top)+Top*0.25, 11, .050, opts.label)

   for _hkey in th1Keys:

       _hkey_basename = os.path.basename(_hkey)

       _hIsProfile = '_wrt_' in _hkey_basename

       ## histograms
       _divideByBinWidth = False
       _normalizedToUnity = False

       _hists = []
       for inp in inputList:
           if _hkey not in inp['TH1s']: continue

           h0 = inp['TH1s'][_hkey].Clone()

           if h0.InheritsFrom('TH2'): continue

           h0.UseCurrentStyle()
           h0.SetDirectory(0)
           h0.SetLineColor(inp['LineColor'])
           h0.SetLineStyle(inp['LineStyle'])
           h0.SetMarkerStyle(inp['MarkerStyle'])
           h0.SetMarkerColor(inp['MarkerColor'])
           h0.SetMarkerSize(inp['MarkerSize'] if _hIsProfile else 0.)

           h0.SetBit(ROOT.TH1.kNoTitle)

           if hasattr(h0, 'SetStats'):
              h0.SetStats(0)

           if (len(_hists) == 0) and (not _hIsProfile):
              _tmpBW = None
              for _tmp in range(1, h0.GetNbinsX()+1):
                  if _tmpBW is None:
                     _tmpBW = h0.GetBinWidth(_tmp)
                  elif (abs(_tmpBW-h0.GetBinWidth(_tmp))/max(abs(_tmpBW), abs(h0.GetBinWidth(_tmp)))) > 1e-4:
                     _divideByBinWidth = True
                     break

           if _divideByBinWidth:
              h0.Scale(1., 'width')

           if _normalizedToUnity:
              h0.Scale(1. / h0.Integral())

           hist0 = Histogram()
           hist0.th1 = h0
           hist0.draw = 'ep' if _hIsProfile else 'hist,e0'
           hist0.legendName = inp['Legend']
           hist0.legendDraw = 'ep' if _hIsProfile else 'l'
           if len(_hists) > 0: hist0.draw += ',same'
           _hists.append(hist0)

       if len(_hists) == 0:
          continue

       ## labels
       _labels = [label_sample]

       _objLabel = ''
       if   _hkey_basename.startswith('ak4GenJets_EtaIncl_'): _objLabel = 'AK4GenJets'
       elif _hkey_basename.startswith('ak4GenJets_HB_'): _objLabel = 'AK4GenJets, |#eta|<1.5'
       elif _hkey_basename.startswith('ak4GenJets_HE_'): _objLabel = 'AK4GenJets, 1.5<|#eta|<3.0'
       elif _hkey_basename.startswith('ak4GenJets_HF_'): _objLabel = 'AK4GenJets, 3.0<|#eta|<5.0'

       elif _hkey_basename.startswith('hltAK4CaloJets_EtaIncl_'): _objLabel = 'HLT AK4CaloJets Uncorrected'
       elif _hkey_basename.startswith('hltAK4CaloJets_HB_'): _objLabel = 'HLT AK4CaloJets Uncorrected, |#eta|<1.5'
       elif _hkey_basename.startswith('hltAK4CaloJets_HE_'): _objLabel = 'HLT AK4CaloJets Uncorrected, 1.5<|#eta|<3.0'
       elif _hkey_basename.startswith('hltAK4CaloJets_HF_'): _objLabel = 'HLT AK4CaloJets Uncorrected, 3.0<|#eta|<5.0'

       elif _hkey_basename.startswith('hltAK4CaloJetsCorrected_EtaIncl_'): _objLabel = 'HLT AK4CaloJets'
       elif _hkey_basename.startswith('hltAK4CaloJetsCorrected_HB_'): _objLabel = 'HLT AK4CaloJets, |#eta|<1.5'
       elif _hkey_basename.startswith('hltAK4CaloJetsCorrected_HE_'): _objLabel = 'HLT AK4CaloJets, 1.5<|#eta|<3.0'
       elif _hkey_basename.startswith('hltAK4CaloJetsCorrected_HF_'): _objLabel = 'HLT AK4CaloJets, 3.0<|#eta|<5.0'

       elif _hkey_basename.startswith('hltAK4PFJets_EtaIncl_'): _objLabel = 'HLT AK4PFJets Uncorrected'
       elif _hkey_basename.startswith('hltAK4PFJets_HB_'): _objLabel = 'HLT AK4PFJets Uncorrected, |#eta|<1.5'
       elif _hkey_basename.startswith('hltAK4PFJets_HE_'): _objLabel = 'HLT AK4PFJets Uncorrected, 1.5<|#eta|<3.0'
       elif _hkey_basename.startswith('hltAK4PFJets_HF_'): _objLabel = 'HLT AK4PFJets Uncorrected, 3.0<|#eta|<5.0'

       elif _hkey_basename.startswith('hltAK4PFJetsCorrected_EtaIncl_'): _objLabel = 'HLT AK4PFJets'
       elif _hkey_basename.startswith('hltAK4PFJetsCorrected_HB_'): _objLabel = 'HLT AK4PFJets, |#eta|<1.5'
       elif _hkey_basename.startswith('hltAK4PFJetsCorrected_HE_'): _objLabel = 'HLT AK4PFJets, 1.5<|#eta|<3.0'
       elif _hkey_basename.startswith('hltAK4PFJetsCorrected_HF_'): _objLabel = 'HLT AK4PFJets, 3.0<|#eta|<5.0'

       elif _hkey_basename.startswith('hltCaloMET_'): _objLabel = 'HLT CaloMET'
       elif _hkey_basename.startswith('hltPFMET_'): _objLabel = 'HLT PFMET'
       elif _hkey_basename.startswith('hltPFMETTypeOne_'): _objLabel = 'HLT PFMET Type-1'

       if '_NotMatchedToGEN_' in _hkey_basename: _objLabel += ' [Not Matched to GEN]'
       elif '_MatchedToGEN_' in _hkey_basename: _objLabel += ' [Matched to GEN]'
       elif '_MatchedToOffline_' in _hkey_basename: _objLabel += ' [Matched to Offline]'

       label_obj = get_text(Lef+(1-Rig-Lef)*0.95, Bot+(1-Top-Bot)*0.925, 31, .035, _objLabel)
       _labels += [label_obj]

       ## axes' titles
       _titleX, _titleY = _hkey_basename, ''
       if _hIsProfile:
          if 'GenJets' in _hkey_basename:
             if _hkey_basename.endswith('_pt'): _titleX = 'GEN Jet p_{T} [GeV]'
             elif _hkey_basename.endswith('_eta'): _titleX = 'GEN Jet #eta'
          elif 'Jets' in _hkey_basename and 'Offline' in _hkey_basename:
             if _hkey_basename.endswith('_pt'): _titleX = 'Offline Jet p_{T} [GeV]'
             elif _hkey_basename.endswith('_eta'): _titleX = 'Offline Jet #eta'
          elif _hkey_basename.endswith('genMETTrue_sumEt'): _titleX = 'GEN #sum E_{T} [GeV]'
          elif _hkey_basename.endswith('genMETTrue_pt'): _titleX = 'GEN MET [GeV]'
          elif _hkey_basename.endswith('hltVerticesPF_mult'): _titleX = 'Number of hltVerticesPF'
       else:
          if 'MET' in _hkey_basename: _titleY = 'Events'
          elif 'Jets' in _hkey_basename: _titleY = 'Entries'

       if '_pt_paraToOffline_Mean_' in _hkey_basename: _titleY = '#LTp_{T}^{#parallel Offl}#GT [GeV]'
       elif '_pt_paraToOffline_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(p_{T}^{#parallel Offl}) / #LTp_{T} / p_{T}^{Offl}#GT [GeV]'
       elif '_pt_paraToOffline_RMS_' in _hkey_basename: _titleY = '#sigma(p_{T}^{#parallel Offl}) [GeV]'
       elif '_pt_paraToOffline_' in _hkey_basename: _titleX = 'p_{T}^{#parallel Offl} [GeV]'

       elif '_pt_paraToOfflineMinusOffline_Mean_' in _hkey_basename: _titleY = '#LTp_{T}^{#parallel Offl} - p_{T}^{Offl}#GT [GeV]'
       elif '_pt_paraToOfflineMinusOffline_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(p_{T}^{#parallel Offl} - p_{T}^{Offl}) / #LTp_{T} / p_{T}^{Offl}#GT [GeV]'
       elif '_pt_paraToOfflineMinusOffline_RMS_' in _hkey_basename: _titleY = '#sigma(p_{T}^{#parallel Offl} - p_{T}^{Offl}) [GeV]'
       elif '_pt_paraToOfflineMinusOffline_' in _hkey_basename: _titleX = 'p_{T}^{#parallel Offl} - p_{T}^{Offl} [GeV]'

       elif '_pt_perpToOffline_Mean_' in _hkey_basename: _titleY = '#LTp_{T}^{#perp Offl}#GT [GeV]'
       elif '_pt_perpToOffline_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(p_{T}^{#perp Offl}) / #LTp_{T} / p_{T}^{Offl}#GT [GeV]'
       elif '_pt_perpToOffline_RMS_' in _hkey_basename: _titleY = '#sigma(p_{T}^{#perp Offl}) [GeV]'
       elif '_pt_perpToOffline_' in _hkey_basename: _titleX = 'p_{T}^{#perp Offl} [GeV]'

       elif '_pt_minusGEN_Mean_' in _hkey_basename: _titleY = '#LTp_{T} - p_{T}^{GEN}#GT [GeV]'
       elif '_pt_minusGEN_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(p_{T} - p_{T}^{GEN}) / #LTp_{T} / p_{T}^{GEN}#GT [GeV]'
       elif '_pt_minusGEN_RMS_' in _hkey_basename: _titleY = '#sigma(p_{T} - p_{T}^{GEN}) [GeV]'
       elif '_pt_minusGEN_' in _hkey_basename: _titleX = 'p_{T} - p_{T}^{GEN} [GeV]'

       elif '_pt_overGEN_Mean_' in _hkey_basename: _titleY = '#LTp_{T} / p_{T}^{GEN}#GT'
       elif '_pt_overGEN_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(p_{T} / p_{T}^{GEN}) / #LTp_{T} / p_{T}^{GEN}#GT'
       elif '_pt_overGEN_RMS_' in _hkey_basename: _titleY = '#sigma(p_{T} / p_{T}^{GEN})'
       elif '_pt_overGEN_' in _hkey_basename: _titleX = 'p_{T} / p_{T}^{GEN}'

       elif '_pt_minusOffline_Mean_' in _hkey_basename: _titleY = '#LTp_{T} - p_{T}^{Offl}#GT [GeV]'
       elif '_pt_minusOffline_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(p_{T} - p_{T}^{Offl}) / #LTp_{T} / p_{T}^{Offl}#GT [GeV]'
       elif '_pt_minusOffline_RMS_' in _hkey_basename: _titleY = '#sigma(p_{T} - p_{T}^{Offl}) [GeV]'
       elif '_pt_minusOffline_' in _hkey_basename: _titleX = 'p_{T} - p_{T}^{Offl} [GeV]'

       elif '_pt_overOffline_Mean_' in _hkey_basename: _titleY = '#LTp_{T} / p_{T}^{Offl}#GT'
       elif '_pt_overOffline_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(p_{T} / p_{T}^{Offl}) / #LTp_{T} / p_{T}^{Offl}#GT'
       elif '_pt_overOffline_RMS_' in _hkey_basename: _titleY = '#sigma(p_{T} / p_{T}^{Offl})'
       elif '_pt_overOffline_' in _hkey_basename: _titleX = 'p_{T} / p_{T}^{Offl}'

       elif '_sumEt_minusGEN_Mean_' in _hkey_basename: _titleY = '#LTSumEt - SumEt^{GEN}#GT [GeV]'
       elif '_sumEt_minusGEN_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(SumEt - SumEt^{GEN}) / #LTSumEt / SumEt^{GEN}#GT [GeV]'
       elif '_sumEt_minusGEN_RMS_' in _hkey_basename: _titleY = '#sigma(SumEt - SumEt^{GEN}) [GeV]'
       elif '_sumEt_minusGEN_' in _hkey_basename: _titleX = 'SumEt - SumEt^{GEN} [GeV]'

       elif '_sumEt_overGEN_Mean_' in _hkey_basename: _titleY = '#LTSumEt / SumEt^{GEN}#GT'
       elif '_sumEt_overGEN_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(SumEt / SumEt^{GEN}) / #LTSumEt / SumEt^{GEN}#GT'
       elif '_sumEt_overGEN_RMS_' in _hkey_basename: _titleY = '#sigma(SumEt / SumEt^{GEN})'
       elif '_sumEt_overGEN_' in _hkey_basename: _titleX = 'SumEt / SumEt^{GEN}'

       elif '_sumEt_minusOffline_Mean_' in _hkey_basename: _titleY = '#LTSumEt - SumEt^{Offl}#GT [GeV]'
       elif '_sumEt_minusOffline_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(SumEt - SumEt^{Offl}) / #LTSumEt / SumEt^{Offl}#GT [GeV]'
       elif '_sumEt_minusOffline_RMS_' in _hkey_basename: _titleY = '#sigma(SumEt - SumEt^{Offl}) [GeV]'
       elif '_sumEt_minusOffline_' in _hkey_basename: _titleX = 'SumEt - SumEt^{Offl} [GeV]'

       elif '_sumEt_overOffline_Mean_' in _hkey_basename: _titleY = '#LTSumEt / SumEt^{Offl}#GT'
       elif '_sumEt_overOffline_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(SumEt / SumEt^{Offl}) / #LTSumEt / SumEt^{Offl}#GT'
       elif '_sumEt_overOffline_RMS_' in _hkey_basename: _titleY = '#sigma(SumEt / SumEt^{Offl})'
       elif '_sumEt_overOffline_' in _hkey_basename: _titleX = 'SumEt / SumEt^{Offl}'

       elif '_phi_minusGEN_Mean_' in _hkey_basename: _titleY = '#LT#phi - #phi^{GEN}#GT [GeV]'
       elif '_phi_minusGEN_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(#phi - #phi^{GEN}) / #LT#phi / #phi^{GEN}#GT [GeV]'
       elif '_phi_minusGEN_RMS_' in _hkey_basename: _titleY = '#sigma(#phi - #phi^{GEN}) [GeV]'
       elif '_phi_minusGEN_' in _hkey_basename: _titleX = '#phi - #phi^{GEN} [GeV]'

       elif '_phi_overGEN_Mean_' in _hkey_basename: _titleY = '#LT#phi / #phi^{GEN}#GT'
       elif '_phi_overGEN_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(#phi / #phi^{GEN}) / #LT#phi / #phi^{GEN}#GT'
       elif '_phi_overGEN_RMS_' in _hkey_basename: _titleY = '#sigma(#phi / #phi^{GEN})'
       elif '_phi_overGEN_' in _hkey_basename: _titleX = '#phi / #phi^{GEN}'

       elif '_phi_minusOffline_Mean_' in _hkey_basename: _titleY = '#LT#phi - #phi^{Offl}#GT [GeV]'
       elif '_phi_minusOffline_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(#phi - #phi^{Offl}) / #LT#phi / #phi^{Offl}#GT [GeV]'
       elif '_phi_minusOffline_RMS_' in _hkey_basename: _titleY = '#sigma(#phi - #phi^{Offl}) [GeV]'
       elif '_phi_minusOffline_' in _hkey_basename: _titleX = '#phi - #phi^{Offl} [GeV]'

       elif '_phi_overOffline_Mean_' in _hkey_basename: _titleY = '#LT#phi / #phi^{Offl}#GT'
       elif '_phi_overOffline_RMSScaledByResponse_' in _hkey_basename: _titleY = '#sigma(#phi / #phi^{Offl}) / #LT#phi / #phi^{Offl}#GT'
       elif '_phi_overOffline_RMS_' in _hkey_basename: _titleY = '#sigma(#phi / #phi^{Offl})'
       elif '_phi_overOffline_' in _hkey_basename: _titleX = '#phi / #phi^{Offl}'

       elif '_pt0' in _hkey_basename: _titleX = 'p_{T}-Leading Jet p_{T} [GeV]'
       elif '_pt' in _hkey_basename: _titleX = 'MET [GeV]' if 'MET' in _hkey_basename else 'Jet p_{T} [GeV]'
       elif '_eta' in _hkey_basename: _titleX = 'Jet #eta'
       elif '_phi' in _hkey_basename: _titleX = 'MET #phi' if 'MET' in _hkey_basename else 'Jet #phi'
       elif '_sumEt' in _hkey_basename: _titleX = 'Sum-E_{T} [GeV]'
       elif '_mass' in _hkey_basename: _titleX = 'Jet mass [GeV]'
       elif '_dRmatch' in _hkey_basename: _titleX = '#DeltaR'
       elif '_njets' in _hkey_basename: _titleX = 'Number of jets'
       elif '_chargedHadronEnergyFraction' in _hkey_basename: _titleX = 'Charged-Hadron Energy Fraction'
       elif '_chargedHadronMultiplicity' in _hkey_basename: _titleX = 'Charged-Hadron Multiplicity'
       elif '_neutralHadronEnergyFraction' in _hkey_basename: _titleX = 'Neutral-Hadron Energy Fraction'
       elif '_neutralHadronMultiplicity' in _hkey_basename: _titleX = 'Neutral-Hadron Multiplicity'
       elif '_electronEnergyFraction' in _hkey_basename: _titleX = 'Electron Energy Fraction'
       elif '_electronMultiplicity' in _hkey_basename: _titleX = 'Electron Multiplicity'
       elif '_photonEnergyFraction' in _hkey_basename: _titleX = 'Photon Energy Fraction'
       elif '_photonMultiplicity' in _hkey_basename: _titleX = 'Photon Multiplicity'
       elif '_muonEnergyFraction' in _hkey_basename: _titleX = 'Muon Energy Fraction'
       elif '_muonMultiplicity' in _hkey_basename: _titleX = 'Muon Multiplicity'

       if _divideByBinWidth:
          _titleY += ' / Bin width'

       _htitle = ';'+_titleX+';'+_titleY

       ## plot
       plot(**{
         'canvas': canvas,
         'histograms': _hists,
         'title': _htitle, 
         'labels': _labels, 
         'legXY': [Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.60, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.90],
         'outputs': [OUTDIR+'/'+_hkey+'.'+_tmp for _tmp in EXTS],

         'ratio': True,
         'logY': False,
       })
