#!/usr/bin/env python
import argparse
import os
import glob
import array
import copy
import ROOT

from common.utils import *
from common.plot import *
from common.plot_style import *

RATIOPLOT = False

def get_histogram(histograms, tag1, tag2, setters):

    if tag1 not in histograms:
       return None

    if tag2 not in histograms[tag1]:
       return None

    h0 = histograms[tag1][tag2].Clone()
    h0.UseCurrentStyle()
    h0.SetDirectory(0)

    h0.SetMarkerSize(0)

    for i_set in setters:
        if hasattr(h0, 'Set'+i_set):
           getattr(h0, 'Set'+i_set)(setters[i_set])

    return h0

def updateDictionary(dictionary, TDirectory, prefix=''):

    key_prefix = ''
    if len(prefix) > 0: key_prefix = prefix+'/'

    for j_key in TDirectory.GetListOfKeys():

        j_key_name = j_key.GetName()

        j_obj = TDirectory.Get(j_key_name)

        if j_obj.InheritsFrom('TDirectory'):

           updateDictionary(dictionary, j_obj, prefix=key_prefix+j_key_name)

        elif j_obj.InheritsFrom('TH1'):

           out_key = key_prefix+j_key_name

           if out_key in dictionary:
              KILL(log_prx+'input error -> found duplicate of template ["'+out_key+'"] in input file: '+TDirectory.GetName())

           dictionary[out_key] = j_obj.Clone()
           dictionary[out_key].SetDirectory(0)

           if opts.verbose: print '\033[1m'+'\033[92m'+'[input]'+'\033[0m', out_key

    return dictionary

def getTH1sFromTFile(path):

    input_histos_dict = {}

    i_inptfile = ROOT.TFile.Open(path)
    if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered):
       return input_histos_dict

    updateDictionary(input_histos_dict, i_inptfile, prefix='')

    i_inptfile.Close()

    return input_histos_dict

class Histogram:
    def __init__(self):
        self.th1 = None
        self.draw = ''
        self.legendName = ''
        self.legendDraw = ''

def plot(canvas, output_extensions, stickers, output, templates, title, legXY, divideByBinWidth=False, normalizedToUnity=False, xMin=None, xMax=None, logX=False, logY=False):

    h0 = None

    plot_histograms = []

    for _tmp in templates:

        histo = Histogram()
        histo.th1 = _tmp['TH1']
        histo.draw = _tmp['draw'] + bool(h0 is not None)*',same'
        histo.legendName = _tmp['legendName']
        histo.legendDraw = _tmp['legendDraw']

        if histo.th1 is not None:

           if h0 is None: h0 = histo.th1

           histo.th1.SetBit(ROOT.TH1.kNoTitle)
           histo.th1.SetStats(0)

           if divideByBinWidth:
              histo.th1.Scale(1., 'width')

           if normalizedToUnity:
              histo.th1.Scale(1. / histo.th1.Integral())

        plot_histograms += [histo]

    if h0 is None:
       return 1

    Top = canvas.GetTopMargin()
    Rig = canvas.GetRightMargin()
    Bot = canvas.GetBottomMargin()
    Lef = canvas.GetLeftMargin()

    leg = ROOT.TLegend(legXY[0], legXY[1], legXY[2], legXY[3])
    leg.SetBorderSize(2)
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    for _tmp in plot_histograms:
        if _tmp.th1 is not None:
           leg.AddEntry(_tmp.th1, _tmp.legendName, _tmp.legendDraw)

    canvas.cd()

    HMAX = 0.0
    for _tmp in plot_histograms:
        if _tmp.th1 is not None:
           for i_bin in range(1, _tmp.th1.GetNbinsX()+1):
               HMAX = max(HMAX, (_tmp.th1.GetBinContent(i_bin) + _tmp.th1.GetBinError(i_bin)))

    XMIN, XMAX = xMin, xMax
    if XMIN is None: XMIN = h0.GetBinLowEdge(1)
    if XMAX is None: XMAX = h0.GetBinLowEdge(1+h0.GetNbinsX())

    if not RATIOPLOT:

       canvas.SetTickx()
       canvas.SetTicky()

       canvas.SetLogx(logX)
       canvas.SetLogy(logY)

       for _tmp in plot_histograms:
           if _tmp.th1 is not None:
              _tmp.th1.Draw(_tmp.draw)

       if h0:
          h0.Draw('axis,same')
          h0.GetXaxis().SetTitle(title.split(';')[0])
          h0.GetYaxis().SetTitle(title.split(';')[1])
          h0.GetXaxis().SetRangeUser(XMIN, XMAX)
          if logY: h0.GetYaxis().SetRangeUser(.0003, .0003*((HMAX/.0003)**(1./.85)))
          else:    h0.GetYaxis().SetRangeUser(.0001, .0001+((HMAX-.0001) *(1./.85)))

       if leg: leg.Draw('same')

       for _tmp in stickers:
           _tmp.Draw('same')

    else:

        canvas.cd()

        pad1H = 0.7

        pad1 = ROOT.TPad('pad1', 'pad1', 0, 1-pad1H, 1, 1)

        pad1.SetTopMargin(pad1.GetTopMargin()/pad1H)
        pad1.SetBottomMargin(0.02)
        pad1.SetGrid(1,1)
        pad1.SetTickx()
        pad1.SetTicky()
        pad1.Draw()

        ROOT.SetOwnership(pad1, False)

        pad1.cd()
        h11 = h_refe.DrawCopy(opt_draw)
        h11.SetXTitle('')

        h11.GetYaxis().SetTitleSize(h11.GetYaxis().GetTitleSize()/pad1H)
        h11.GetYaxis().SetTitleOffset(h11.GetYaxis().GetTitleOffset()*pad1H)
        h11.GetXaxis().SetLabelSize(0)
        h11.GetYaxis().SetLabelSize (h11.GetYaxis().GetLabelSize() /pad1H)
        h11.GetXaxis().SetTickLength(h11.GetXaxis().GetTickLength()/pad1H)

#        h11.GetXaxis().SetRangeUser(xmin_, xmax_)

        pad1.SetLogy(logY)

        if logY: h11.GetYaxis().SetRangeUser(.0003, .0003*((HMAX/.0003)**(1./.85)))
        else   : h11.GetYaxis().SetRangeUser(.0001, .0001+((HMAX-.0001) *(1./.85)))

        if leg:
           leg.SetY1NDC(1.-(1.-leg.GetY1NDC())/pad1H)
           leg.SetY2NDC(1.-(1.-leg.GetY2NDC())/pad1H)
           leg.Draw('same')

        for _tmp in stickers:
            _tmp.SetTextSize(_tmp.GetTextSize()/pad1H)
            _tmp.SetY(1.-(1.-_tmp.GetY())/pad1H)
            _tmp.Draw('same')

        pad1.Update()

#        if leg:
#           leg.SetY1NDC((leg.GetY1NDC()-canvas.GetBottomMargin()+pad1.GetBottomMargin())/pad1H)
#           leg.SetY2NDC((leg.GetY2NDC()-canvas.GetBottomMargin()+pad1.GetBottomMargin())/pad1H)

        canvas.cd()

        pad2 = ROOT.TPad('pad2', 'pad2', 0, 0, 1, 1-pad1H)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(pad2.GetBottomMargin()/(1-pad1H))
        pad2.SetGrid(1,1)
        pad2.SetTickx()
        pad2.SetTicky()
        pad2.Draw()

        denom = h_refe.Clone()
        for _tmp in range(0, denom.GetNbinsX()+2): denom.SetBinError(_tmp, 0.)

        h21 = h_refe.Clone()
        h22 = h_targ.Clone()

        h21.Divide(denom)
        h22.Divide(denom)

#        for h0 in [h21, h22]:
#            for _tmp in range(0, h0.GetNbinsX()+2):
#                h0.SetBinContent(_tmp, h0.GetBinContent(b)-1.)

        ROOT.SetOwnership(pad2, False)

        pad2.cd()
        h21.SetStats(0)
#        h21.SetTitle(title_)
        h21.SetMarkerSize(0)

        h21.SetFillStyle(3017)
        h21.SetFillColor(16)

        h21.GetYaxis().SetTitle('X / GEN')
        h21.GetYaxis().CenterTitle()
        h21.GetXaxis().SetTitleSize  (h21.GetXaxis().GetTitleSize()   /(1-pad1H))
        h21.GetYaxis().SetTitleSize  (h21.GetYaxis().GetTitleSize()   /(1-pad1H))
        h21.GetXaxis().SetTitleOffset(h21.GetXaxis().GetTitleOffset()           )
        h21.GetYaxis().SetTitleOffset(h21.GetYaxis().GetTitleOffset() *(1-pad1H))
        h21.GetXaxis().SetLabelSize  (h21.GetXaxis().GetLabelSize()   /(1-pad1H))
        h21.GetYaxis().SetLabelSize  (h21.GetYaxis().GetLabelSize()   /(1-pad1H))
        h21.GetXaxis().SetLabelOffset(h21.GetXaxis().GetLabelOffset() /(1-pad1H))
        h21.GetYaxis().SetLabelOffset(h21.GetYaxis().GetLabelOffset()           )
        h21.GetXaxis().SetTickLength (h21.GetXaxis().GetTickLength()  /(1-pad1H))
        h21.GetYaxis().SetNdivisions(304)

        h21.GetXaxis().SetRangeUser(XMIN, XMAX)

        h2max, h2min = None, None
        for h_tmp in [h21, h22]:
            for _tmp in range(1, h_tmp.GetNbinsX()+1):

                if (h21.GetBinContent(_tmp) == 0.) and (h21.GetBinLowEdge(_tmp) == h22.GetBinLowEdge(_tmp)) and (h22.GetBinContent(_tmp) == 0.): continue

                h2max = max(h2max, h_tmp.GetBinContent(_tmp)+h_tmp.GetBinError(_tmp)) if h2max is not None else h_tmp.GetBinContent(_tmp)+h_tmp.GetBinError(_tmp)
                h2min = min(h2min, h_tmp.GetBinContent(_tmp)-h_tmp.GetBinError(_tmp)) if h2min is not None else h_tmp.GetBinContent(_tmp)-h_tmp.GetBinError(_tmp)

        if (h2max is not None) and (h2min is not None):

           h2min = min(int(h2min*101.)/100., int(h2min*99.)/100.)
           h2max = max(int(h2max*101.)/100., int(h2max*99.)/100.)

           h21.GetYaxis().SetRangeUser(h2min, h2max)

        h21.GetYaxis().SetNdivisions(404)

        h21.Draw('e2')
        h22.Draw(opt_draw+',same')
        h21.Draw('axis,same')

    canvas.cd()
    canvas.Update()

    output_basename_woExt = str(output)

    output_dirname = os.path.dirname(output_basename_woExt)
    if not os.path.isdir(output_dirname):
       EXE('mkdir -p '+output_dirname)

    for i_ext in output_extensions:

        out_file = output_basename_woExt+'.'+i_ext

        canvas.SaveAs(out_file)

        print '\033[1m'+'\033[92m'+'[output]'+'\033[0m', os.path.relpath(out_file)

    return 0


############
############
############METCollections = [
############
############  'genMetTrue',
############
############  'hltPFMET',
############  'hltPFMETTypeOne',
############  'hltPuppiMET',
############  'hltPuppiMETWithPuppiForJets',
############
############  'offlineMETs_Raw',
############  'offlineMETs_Type1',
############  'offlineMETsPuppi_Raw',
############  'offlineMETsPuppi_Type1',
############]
############
############output_histos_dict = {}
############
############output_histos_dict['hltNPV'] = [10*_tmp for _tmp in range(40+1)]
############output_histos_dict['offlineNPV'] = [10*_tmp for _tmp in range(40+1)]
############
############for i_met in METCollections:
############    output_histos_dict[i_met+'_pt'] = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 250, 300, 400, 500, 600, 700, 800, 1000]
############    output_histos_dict[i_met+'_phi'] = [3.1416*(2./40*_tmp-1) for _tmp in range(40+1)]
############    output_histos_dict[i_met+'_sumEt'] = [0, 30, 60, 90, 120, 180, 250, 400, 600, 800, 1000, 1500, 2000, 3000]
############
############    if i_met == 'genMetTrue': continue
############
############    output_histos_dict[i_met+'_pt_minusGEN'] = [-250+10*_tmp for _tmp in range(50+1)]
############    output_histos_dict[i_met+'_phi_minusGEN'] = [-2.5+0.1*_tmp for _tmp in range(50+1)]
############    output_histos_dict[i_met+'_sumEt_minusGEN'] = [-250+10*_tmp for _tmp in range(50+1)]
############
############    output_histos_dict[i_met+'_pt_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]
############    output_histos_dict[i_met+'_phi_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]
############    output_histos_dict[i_met+'_sumEt_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]
############
############for i_met in METCollections:
############
############    if i_met.startswith('hlt'): continue
############
############    output_histos_dict['hltPFMET200/'+i_met+'_pt'] = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 250, 300, 400, 500, 600, 700, 800, 1000]

#### -------------------------------------------------------------------------------------------------------------------------------
#### -------------------------------------------------------------------------------------------------------------------------------
#### -------------------------------------------------------------------------------------------------------------------------------

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser()

   parser.add_argument('--NoPU', dest='NoPU', action='store', default=None,
                       help='path to input .root file for NoPU')

   parser.add_argument('--PU140', dest='PU140', action='store', default=None,
                       help='path to input .root file for PU140')

   parser.add_argument('--PU200', dest='PU200', action='store', default=None,
                       help='path to input .root file for PU200')

   parser.add_argument('-o', '--output', dest='output', action='store', default=None, required=True,
                       help='path to output directory')

   parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['pdf'],
                       help='list of extension(s) for output file(s)')

   parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                       help='enable verbose mode')

   opts, opts_unknown = parser.parse_known_args()
   ### -------------------

   ROOT.gROOT.SetBatch()
   ROOT.gErrorIgnoreLevel = ROOT.kWarning

   log_prx = os.path.basename(__file__)+' -- '

   ### args validation ---
   if os.path.exists(opts.output):
      KILL(log_prx+'target path to output directory already exists [-o]: '+opts.output)

   if len(opts_unknown) > 0:
      KILL(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))

   EXTS = list(set(opts.exts))
   ### -------------------

   histograms = {}

   if opts.NoPU is not None:
      if not os.path.isfile(opts.NoPU):
         WARNING('AAA')
      else:
         histograms['NoPU'] = getTH1sFromTFile(opts.NoPU)

   if opts.PU140 is not None:
      if not os.path.isfile(opts.PU140):
         WARNING('AAA')
      else:
         histograms['PU140'] = getTH1sFromTFile(opts.PU140)

   if opts.PU200 is not None:
      if not os.path.isfile(opts.PU200):
         WARNING('AAA')
      else:
         histograms['PU200'] = getTH1sFromTFile(opts.PU200)

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

#   leg = ROOT.TLegend(L+(1-Rig-Lef)*0.00, (1-Top)+Top*0.05, Lef+(1-Rig-Lef)*1.00, (1-Top)+T*0.95)
#   leg.SetBorderSize(2)
#   leg.SetTextFont(42)
#   leg.SetFillColor(0)
#   leg.AddEntry(h_targ, '#bf{Target}: '   +target_legend   , opt_legd)
#   leg.AddEntry(h_refe, '#bf{Reference}: '+reference_legend, opt_legd)
#
#   txt1 = None
#   if   histo_type == 'NUM': txt1 = get_text((1-R)+R*0.25, (1-T), 11, .025, '[Numerator]');   txt1.SetTextAngle(-90);
#   elif histo_type == 'DEN': txt1 = get_text((1-R)+R*0.25, (1-T), 11, .025, '[Denominator]'); txt1.SetTextAngle(-90);

   label_sample = get_text(Lef+(1-Lef-Rig)*0.00, (1-Top)+Top*0.25, 11, .050, 'VBF_H125ToInv_14TeV')

   for pu_tag in ['NoPU', 'PU140', 'PU200']:

       label_PU = get_text((1-Lef-Rig)+Lef*1.00, (1-Top)+Top*0.25, 31, .050, pu_tag)

       # pT
       plot(canvas=canvas, output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.45, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

         stickers=[label_sample, label_PU], output=opts.output+'/MET_pt_'+pu_tag,

         templates=[

           {'TH1': get_histogram(histograms, pu_tag, 'genMetTrue'            +'_pt', {'LineColor': ROOT.kBlack, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'GEN', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'hltPFMET'              +'_pt', {'LineColor': ROOT.kOrange, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'HLT-like PF-MET', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'hltPFMETTypeOne'       +'_pt', {'LineColor': ROOT.kRed, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'HLT-like PF-MET Type-1', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'offlineMETs_Type1'     +'_pt', {'LineColor': ROOT.kCyan, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'offline PF-MET Type-1', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'offlineMETsPuppi_Type1'+'_pt', {'LineColor': ROOT.kBlue, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'offline Puppi-MET Type-1', 'legendDraw': 'l'},
         ],

         logX = True,

         xMin = 10,

         divideByBinWidth = True,

         normalizedToUnity = True,

         title = 'p_{T} [GeV];Fraction Of Events;',
       )

       # pT response (Ratio wrt GEN)
       plot(canvas=canvas, output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.45, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

         stickers=[label_sample, label_PU], output=opts.output+'/MET_pt_overGEN_'+pu_tag,

         templates=[

           {'TH1': get_histogram(histograms, pu_tag, 'hltPFMET'              +'_pt_overGEN', {'LineColor': ROOT.kOrange, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'HLT-like PF-MET', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'hltPFMETTypeOne'       +'_pt_overGEN', {'LineColor': ROOT.kRed, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'HLT-like PF-MET Type-1', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'offlineMETs_Type1'     +'_pt_overGEN', {'LineColor': ROOT.kCyan, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'offline PF-MET Type-1', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'offlineMETsPuppi_Type1'+'_pt_overGEN', {'LineColor': ROOT.kBlue, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'offline Puppi-MET Type-1', 'legendDraw': 'l'},
         ],

         normalizedToUnity = True,

         title = 'p_{T} response (Ratio wrt GEN);Fraction Of Events;',
       )

       # Phi response (Ratio wrt GEN)
       plot(canvas=canvas, output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.45, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

         stickers=[label_sample, label_PU], output=opts.output+'/MET_phi_overGEN_'+pu_tag,

         templates=[

           {'TH1': get_histogram(histograms, pu_tag, 'hltPFMET'              +'_phi_overGEN', {'LineColor': ROOT.kOrange, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'HLT-like PF-MET', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'hltPFMETTypeOne'       +'_phi_overGEN', {'LineColor': ROOT.kRed, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'HLT-like PF-MET Type-1', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'offlineMETs_Type1'     +'_phi_overGEN', {'LineColor': ROOT.kCyan, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'offline PF-MET Type-1', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'offlineMETsPuppi_Type1'+'_phi_overGEN', {'LineColor': ROOT.kBlue, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'offline Puppi-MET Type-1', 'legendDraw': 'l'},
         ],

         normalizedToUnity = True,

         title = '#phi response (Ratio wrt GEN);Fraction Of Events;',
       )

       # pT Delta GEN
       plot(canvas=canvas, output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

         stickers=[label_sample, label_PU], output=opts.output+'/MET_pt_minusGEN_'+pu_tag,

         templates=[

           {'TH1': get_histogram(histograms, pu_tag, 'hltPFMET'              +'_pt_minusGEN', {'LineColor': ROOT.kOrange, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'HLT-like PF-MET', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'hltPFMETTypeOne'       +'_pt_minusGEN', {'LineColor': ROOT.kRed, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'HLT-like PF-MET Type-1', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'offlineMETs_Type1'     +'_pt_minusGEN', {'LineColor': ROOT.kCyan, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'offline PF-MET Type-1', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'offlineMETsPuppi_Type1'+'_pt_minusGEN', {'LineColor': ROOT.kBlue, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'offline Puppi-MET Type-1', 'legendDraw': 'l'},
         ],

         normalizedToUnity = True,

         title = '#Deltap_{T} (X - GEN);Fraction Of Events;',
       )

       # Phi Delta GEN
       plot(canvas=canvas, output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.45, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

         stickers=[label_sample, label_PU], output=opts.output+'/MET_phi_minusGEN_'+pu_tag,

         templates=[

           {'TH1': get_histogram(histograms, pu_tag, 'hltPFMET'              +'_phi_minusGEN', {'LineColor': ROOT.kOrange, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'HLT-like PF-MET', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'hltPFMETTypeOne'       +'_phi_minusGEN', {'LineColor': ROOT.kRed, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'HLT-like PF-MET Type-1', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'offlineMETs_Type1'     +'_phi_minusGEN', {'LineColor': ROOT.kCyan, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'offline PF-MET Type-1', 'legendDraw': 'l'},
           {'TH1': get_histogram(histograms, pu_tag, 'offlineMETsPuppi_Type1'+'_phi_minusGEN', {'LineColor': ROOT.kBlue, 'LineWidth': 2}), 'draw': 'hist,e0', 'legendName': 'offline Puppi-MET Type-1', 'legendDraw': 'l'},
         ],

         normalizedToUnity = True,

         title = '#Delta#phi (X - GEN);Fraction Of Events;',
       )

   print '\033[1m'+'\033[92m'+'[output]'+'\033[0m', opts.output
