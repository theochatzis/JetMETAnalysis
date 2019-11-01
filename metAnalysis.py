#!/usr/bin/env python
import argparse
import os
import glob
import array
import math
import ROOT

from common.utils import *

#### Histograms --------------------------------------------------------------------------------------------------------------------

# bin-edges for TH1Ds and TH2Ds
binEdges_1d = {}
binEdges_2d = {}

EvtSelections = [

  'NoSelection/',
  'hltPFMET200/',
  'hltPuppiMET200/',
]

METCollections = [

  'genMetTrue',

  'hltPFMET',
  'hltPFMETTypeOne',
  'hltPuppiMET',
  'hltPuppiMETWithPuppiForJets',

  'offlineMETs_Raw',
  'offlineMETs_Type1',
  'offlineMETsPuppi_Raw',
  'offlineMETsPuppi_Type1',
]

for i_sel in EvtSelections:

    binEdges_1d[i_sel+'hltNPV'] = [10*_tmp for _tmp in range(40+1)]
    binEdges_1d[i_sel+'offlineNPV'] = [10*_tmp for _tmp in range(40+1)]

    for i_met in METCollections:

        binEdges_1d[i_sel+i_met+'_pt'] = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 400, 500, 600, 700, 800, 1000]
        binEdges_1d[i_sel+i_met+'_phi'] = [math.pi*(2./40*_tmp-1) for _tmp in range(40+1)]
        binEdges_1d[i_sel+i_met+'_sumEt'] = [0, 30, 60, 90, 120, 180, 250, 400, 600, 800, 1000, 1500, 2000, 3000]

        for i_var in ['pt', 'phi', 'sumEt']:
            binEdges_2d[i_sel+i_met+'_'+i_var+':hltNPV'] = [binEdges_1d[i_sel+i_met+'_'+i_var], binEdges_1d[i_sel+'hltNPV']]
            binEdges_2d[i_sel+i_met+'_'+i_var+':offlineNPV'] = [binEdges_1d[i_sel+i_met+'_'+i_var], binEdges_1d[i_sel+'offlineNPV']]

        if i_met == 'genMetTrue': continue

        binEdges_1d[i_sel+i_met+'_pt_minusGEN'] = [-250+10*_tmp for _tmp in range(50+1)]
        binEdges_1d[i_sel+i_met+'_phi_minusGEN'] = [math.pi/40*_tmp for _tmp in range(40+1)]
        binEdges_1d[i_sel+i_met+'_sumEt_minusGEN'] = [-250+10*_tmp for _tmp in range(50+1)]

        binEdges_1d[i_sel+i_met+'_pt_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]
        binEdges_1d[i_sel+i_met+'_phi_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]
        binEdges_1d[i_sel+i_met+'_sumEt_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]

        binEdges_2d[i_sel+i_met+'_pt:genMetTrue_pt'] = [binEdges_1d[i_sel+i_met+'_pt'], binEdges_1d[i_sel+'genMetTrue_pt']]
        binEdges_2d[i_sel+i_met+'_phi:genMetTrue_pt'] = [binEdges_1d[i_sel+i_met+'_phi'], binEdges_1d[i_sel+'genMetTrue_pt']]
        binEdges_2d[i_sel+i_met+'_sumEt:genMetTrue_pt'] = [binEdges_1d[i_sel+i_met+'_sumEt'], binEdges_1d[i_sel+'genMetTrue_pt']]

        binEdges_2d[i_sel+i_met+'_pt_minusGEN:genMetTrue_pt'] = [binEdges_1d[i_sel+i_met+'_pt_minusGEN'], binEdges_1d[i_sel+'genMetTrue_pt']]
        binEdges_2d[i_sel+i_met+'_phi_minusGEN:genMetTrue_pt'] = [binEdges_1d[i_sel+i_met+'_phi_minusGEN'], binEdges_1d[i_sel+'genMetTrue_pt']]
        binEdges_2d[i_sel+i_met+'_sumEt_minusGEN:genMetTrue_pt'] = [binEdges_1d[i_sel+i_met+'_sumEt_minusGEN'], binEdges_1d[i_sel+'genMetTrue_pt']]

        binEdges_2d[i_sel+i_met+'_pt_overGEN:genMetTrue_pt'] = [binEdges_1d[i_sel+i_met+'_pt_overGEN'], binEdges_1d[i_sel+'genMetTrue_pt']]
        binEdges_2d[i_sel+i_met+'_phi_overGEN:genMetTrue_pt'] = [binEdges_1d[i_sel+i_met+'_phi_overGEN'], binEdges_1d[i_sel+'genMetTrue_pt']]
        binEdges_2d[i_sel+i_met+'_sumEt_overGEN:genMetTrue_pt'] = [binEdges_1d[i_sel+i_met+'_sumEt_overGEN'], binEdges_1d[i_sel+'genMetTrue_pt']]

        if i_met.startswith('hlt'):

           binEdges_1d[i_sel+i_met+'_pt_minusOffline'] = [-250+10*_tmp for _tmp in range(50+1)]
           binEdges_1d[i_sel+i_met+'_phi_minusOffline'] = [math.pi/40*_tmp for _tmp in range(40+1)]
           binEdges_1d[i_sel+i_met+'_sumEt_minusOffline'] = [-250+10*_tmp for _tmp in range(50+1)]

           binEdges_1d[i_sel+i_met+'_pt_overOffline'] = [0.1*_tmp for _tmp in range(50+1)]
           binEdges_1d[i_sel+i_met+'_phi_overOffline'] = [0.1*_tmp for _tmp in range(50+1)]
           binEdges_1d[i_sel+i_met+'_sumEt_overOffline'] = [0.1*_tmp for _tmp in range(50+1)]

    for [i_met_onl, i_met_off] in [
      ['hltPFMET', 'offlineMETs_Raw'],
      ['hltPFMETTypeOne', 'offlineMETs_Type1'],
      ['hltPuppiMET', 'offlineMETsPuppi_Raw'],
      ['hltPuppiMETWithPuppiForJets', 'offlineMETsPuppi_Raw'],
    ]:
        binEdges_2d[i_sel+i_met_onl+'_pt:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt'], binEdges_1d[i_sel+i_met_off+'_pt']]
        binEdges_2d[i_sel+i_met_onl+'_phi:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_phi'], binEdges_1d[i_sel+i_met_off+'_pt']]
        binEdges_2d[i_sel+i_met_onl+'_sumEt:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_sumEt'], binEdges_1d[i_sel+i_met_off+'_pt']]

        binEdges_2d[i_sel+i_met_onl+'_pt_minusOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt_minusOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]
        binEdges_2d[i_sel+i_met_onl+'_phi_minusOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_phi_minusOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]
        binEdges_2d[i_sel+i_met_onl+'_sumEt_minusOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_sumEt_minusOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]

        binEdges_2d[i_sel+i_met_onl+'_pt_overOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt_overOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]
        binEdges_2d[i_sel+i_met_onl+'_phi_overOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_phi_overOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]
        binEdges_2d[i_sel+i_met_onl+'_sumEt_overOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_sumEt_overOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]

#### Event Analysis ----------------------------------------------------------------------------------------------------------------

def analyze_event(event, th1s={}, th2s={}):

    values = {}

    for i_sel in EvtSelections:

        if i_sel == 'hltPFMET200/':
           if not (values['NoSelection/hltPFMET_pt'] > 200.): continue

        if i_sel == 'hltPuppiMET200/':
           if not (values['NoSelection/hltPuppiMET_pt'] > 200.): continue

        values[i_sel+'hltNPV'] = len(event.hltGoodPrimaryVertices_z)
        values[i_sel+'offlineNPV'] = len(event.offlinePrimaryVertices_z)

        for i_met in METCollections:
            for i_var in ['pt', 'phi', 'sumEt']:
                values[i_sel+i_met+'_'+i_var] = float(getattr(event, i_met+'_'+i_var)[0])

        for i_met in METCollections:

            if i_met == 'genMetTrue': continue

            for i_var in ['pt', 'phi', 'sumEt']:

                values[i_sel+i_met+'_'+i_var+'_minusGEN'] = values[i_sel+i_met+'_'+i_var] - values[i_sel+'genMetTrue_'+i_var]
                if i_var == 'phi':
                   values[i_sel+i_met+'_'+i_var+'_minusGEN'] = abs(values[i_sel+i_met+'_'+i_var+'_minusGEN'])
                   if values[i_sel+i_met+'_'+i_var+'_minusGEN'] > math.pi:
                      values[i_sel+i_met+'_'+i_var+'_minusGEN'] = 2*math.pi - values[i_sel+i_met+'_'+i_var+'_minusGEN']

                if values[i_sel+'genMetTrue_'+i_var] != 0:
                   values[i_sel+i_met+'_'+i_var+'_overGEN'] = values[i_sel+i_met+'_'+i_var] / values[i_sel+'genMetTrue_'+i_var]

        for [i_met_onl, i_met_off] in [
          ['hltPFMET', 'offlineMETs_Raw'],
          ['hltPFMETTypeOne', 'offlineMETs_Type1'],
          ['hltPuppiMET', 'offlineMETsPuppi_Raw'],
          ['hltPuppiMETWithPuppiForJets', 'offlineMETsPuppi_Raw'],
        ]:
            for i_var in ['pt', 'phi', 'sumEt']:

                values[i_sel+i_met_onl+'_'+i_var+'_minusOffline'] = values[i_sel+i_met_onl+'_'+i_var] - values[i_sel+i_met_off+'_'+i_var]
                if i_var == 'phi':
                   values[i_sel+i_met_onl+'_'+i_var+'_minusOffline'] = abs(values[i_sel+i_met_onl+'_'+i_var+'_minusOffline'])
                   if values[i_sel+i_met_onl+'_'+i_var+'_minusOffline'] > math.pi:
                      values[i_sel+i_met_onl+'_'+i_var+'_minusOffline'] = 2*math.pi - values[i_sel+i_met_onl+'_'+i_var+'_minusOffline']

                if values[i_sel+i_met_off+'_'+i_var] != 0:
                   values[i_sel+i_met_onl+'_'+i_var+'_overOffline'] = values[i_sel+i_met_onl+'_'+i_var] / values[i_sel+i_met_off+'_'+i_var]

    for i_hist_key in sorted(list(set(th1s.keys() + th2s.keys()))):

        if i_hist_key in th1s:

           if i_hist_key in values:
              th1s[i_hist_key].Fill(values[i_hist_key])

        elif i_hist_key in th2s:

           i_hist_key_basename = os.path.basename(i_hist_key)

           i_hist_key_basename_split = i_hist_key_basename.split(':')

           if len(i_hist_key_basename_split) != 2:
              KILL('AAA')

           i_hist_key_dirname = os.path.dirname(i_hist_key)
           if i_hist_key_dirname: i_hist_key_dirname += '/'

           i_hist_key_varX = i_hist_key_dirname+i_hist_key_basename_split[0]
           i_hist_key_varY = i_hist_key_dirname+i_hist_key_basename_split[1]

           if i_hist_key_varX not in values: continue
           if i_hist_key_varY not in values: continue

           th2s[i_hist_key].Fill(values[i_hist_key_varX], values[i_hist_key_varY])

def create_TH1D(name, binEdges):

    _binEdges_array = array.array('d', sorted(list(set(binEdges))))

    _th1d = ROOT.TH1D(name, name, len(_binEdges_array)-1, _binEdges_array)
    _th1d.SetDirectory(0)
    _th1d.Sumw2()

    return _th1d

def create_TH2D(name, binEdges):

    _binEdgesX_array = array.array('d', sorted(list(set(binEdges[0]))))
    _binEdgesY_array = array.array('d', sorted(list(set(binEdges[1]))))

    _th2d = ROOT.TH2D(name, name, len(_binEdgesX_array)-1, _binEdgesX_array, len(_binEdgesY_array)-1, _binEdgesY_array)
    _th2d.SetDirectory(0)
    _th2d.Sumw2()

    return _th2d

#### main --------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser()

   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=None,
                       help='path to input .root file(s)')

   parser.add_argument('-o', '--output', dest='output', required=True, action='store', default=None,
                       help='path to output .root file')

   parser.add_argument('-t', '--tree', dest='tree', action='store', default='JMETriggerNTuple/Events',
                       help='key of TTree in input file(s)')

   parser.add_argument('-n', '--num-maxEvents', dest='num_maxEvents', action='store', type=int, default=-1,
                       help='maximum number of events to be processed')

   parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                       help='enable verbose mode')

   opts, opts_unknown = parser.parse_known_args()
   ### -------------------

   ROOT.gROOT.SetBatch()
   ROOT.gErrorIgnoreLevel = ROOT.kError #kWarning

   log_prx = os.path.basename(__file__)+' -- '

   ### args validation ---
   INPUT_FILES = []

   for i_inpf in opts.inputs:

       i_inpf_ls = glob.glob(i_inpf)

       for i_inpf_2 in i_inpf_ls:

           if os.path.isfile(i_inpf_2):
              INPUT_FILES += [os.path.abspath(os.path.realpath(i_inpf_2))]

   INPUT_FILES = sorted(list(set(INPUT_FILES)))

   if len(INPUT_FILES) == 0:
      KILL(log_prx+'empty list of input files containing MEM TTrees [-i]')

   if os.path.exists(opts.output):
      KILL(log_prx+'target path to output .root file already exists [-o]: '+opts.output)

   if len(opts_unknown) > 0:
      KILL(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))
   ### -------------------

   # convert bin-edges to TH1D
   th1s = {}
   for h_name in binEdges_1d:
       th1s[h_name] = create_TH1D(h_name, binEdges_1d[h_name])

   th2s = {}
   for h_name in binEdges_2d:
       th2s[h_name] = create_TH2D(h_name, binEdges_2d[h_name])

   NUM_EVENTS_PROCESSED = 0

   for i_inpf in INPUT_FILES:

       if opts.verbose: print '\033[1m'+'\033[92m'+'[input]'+'\033[0m', i_inpf

       i_inptfile = ROOT.TFile.Open(i_inpf)
       if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered):
          WARNING(log_prx+'path to input file is not valid, or TFile is corrupted (file will be ignored) [-i]: '+i_inpf)
          continue

       i_ttree = i_inptfile.Get(opts.tree)
       if not i_ttree:
          WARNING(log_prx+'target TFile does not contain a TTree named "'+opts.tree+'" (file will be ignored) [-t]: '+i_inpf)
          continue

       for i_evt in i_ttree:

           if (opts.num_maxEvents >= 0) and (NUM_EVENTS_PROCESSED >= opts.num_maxEvents): break

           analyze_event(event=i_evt, th1s=th1s, th2s=th2s)

           NUM_EVENTS_PROCESSED += 1

       i_inptfile.Close()

   ### Histograms for mean Response and Resolution
   for i_h2_key in th2s.keys():

       i_h2_key_basename = os.path.basename(i_h2_key)

       i_h2_key_dirname = os.path.dirname(i_h2_key)
       if i_h2_key_dirname: i_h2_key_dirname += '/'

       if '_minus' in i_h2_key_basename:

          i_h2_compTag = 'GEN' if 'GEN:' in i_h2_key_basename else 'Offline'

          key_vars_split = i_h2_key_basename.split('_minus'+i_h2_compTag+':')
          if len(key_vars_split) != 2:
             KILL('ZZZ '+i_h2_key_basename)

          key_varX = key_vars_split[0]
          key_varY = key_vars_split[1]

          tmp_h2 = th2s[i_h2_key]

          # Mean of Diff, in bins of Y
          h_name0 = i_h2_key_dirname+key_varX+'_minus'+i_h2_compTag+'_Mean_wrt_'+key_varY
          if h_name0 in th1s: KILL('aaa '+h_name0)

          tmp_h1_diffMean = tmp_h2.ProjectionY(h_name0)
          tmp_h1_diffMean.SetDirectory(0)
          tmp_h1_diffMean.Reset()

          for _idx in range(1, 1+tmp_h2.GetNbinsY()):
              _htmp = tmp_h2.ProjectionX('_htmp'+str(_idx), _idx, _idx, 'e')
              _htmp.SetDirectory(0)
              tmp_h1_diffMean.SetBinContent(_idx, _htmp.GetMean())
              tmp_h1_diffMean.SetBinError(_idx, _htmp.GetMeanError())
              del _htmp

          th1s[h_name0] = tmp_h1_diffMean

          # RMS of Diff, in bins of Y
          h_name1 = i_h2_key_dirname+key_varX+'_minus'+i_h2_compTag+'_RMS_wrt_'+key_varY
          if h_name1 in th1s: KILL('aaa '+h_name1)

          tmp_h1_diffRMS = tmp_h2.ProjectionY(h_name1)
          tmp_h1_diffRMS.SetDirectory(0)
          tmp_h1_diffRMS.Reset()

          for _idx in range(1, 1+tmp_h2.GetNbinsY()):
              _htmp = tmp_h2.ProjectionX('_htmp'+str(_idx), _idx, _idx, 'e')
              _htmp.SetDirectory(0)
              tmp_h1_diffRMS.SetBinContent(_idx, _htmp.GetRMS())
              tmp_h1_diffRMS.SetBinError(_idx, _htmp.GetRMSError())
              del _htmp

          th1s[h_name1] = tmp_h1_diffRMS

          if i_h2_key_dirname+(i_h2_key_basename.replace('_minus'+i_h2_compTag+':', '_over'+i_h2_compTag+':')) in th2s:

             tmp_h2 = th2s[i_h2_key_dirname+(i_h2_key_basename.replace('_minus'+i_h2_compTag+':', '_over'+i_h2_compTag+':'))]

             h_name2 = i_h2_key_dirname+key_varX+'_over'+i_h2_compTag+'_Mean_wrt_'+key_varY
             if h_name2 in th1s: KILL('aaa '+h_name2)

             # Mean of Ratio, in bins of Y
             tmp_h1_ratioMean = tmp_h2.ProjectionY(h_name2)
             tmp_h1_ratioMean.SetDirectory(0)
             tmp_h1_ratioMean.Reset()

             for _idx in range(1, 1+tmp_h2.GetNbinsY()):
                 _htmp = tmp_h2.ProjectionX('_htmp'+str(_idx), _idx, _idx, 'e')
                 _htmp.SetDirectory(0)
                 tmp_h1_ratioMean.SetBinContent(_idx, _htmp.GetMean())
                 tmp_h1_ratioMean.SetBinError(_idx, _htmp.GetMeanError())
                 del _htmp

             th1s[h_name2] = tmp_h1_ratioMean

             # RMS of Diff scaled by Response, in bins of Y
             h_name3 = i_h2_key_dirname+key_varX+'_minus'+i_h2_compTag+'_RMSScaledByResponse_wrt_'+key_varY
             if h_name3 in th1s: KILL('aaa '+h_name3)

             tmp_h1_ratioMeanNoErr = tmp_h1_ratioMean.Clone()
             for _idx in range(tmp_h1_ratioMeanNoErr.GetNbinsX()+2):
                 tmp_h1_ratioMeanNoErr.SetBinError(_idx, 0)

             tmp_h1_ratioMeanNorm = tmp_h1_diffRMS.Clone()
             tmp_h1_ratioMeanNorm.SetName(h_name3)
             tmp_h1_ratioMeanNorm.SetDirectory(0)
             tmp_h1_ratioMeanNorm.Divide(tmp_h1_ratioMeanNoErr)

             th1s[h_name3] = tmp_h1_ratioMeanNorm
   ### -------------------

   ### output file -------
   output_dirname = os.path.dirname(os.path.abspath(opts.output))
   if not os.path.isdir(output_dirname): EXE('mkdir -p '+output_dirname)
   del output_dirname

   output_tfile = ROOT.TFile(opts.output, 'recreate')
   if (not output_tfile) or output_tfile.IsZombie() or output_tfile.TestBit(ROOT.TFile.kRecovered):
      raise SystemExit(1)

   for i_idx in sorted(th1s.keys() + th2s.keys()):

       output_tfile.cd()

       out_key = i_idx

       while '/' in out_key:
          slash_index = out_key.find('/')
          out_dir = out_key[:slash_index]
          out_key = out_key[slash_index+1:]
          out_dir = getattr(output_tfile, 'Get' if output_tfile.Get(out_dir) else 'mkdir')(out_dir)
          out_dir.cd()

       the_dict = th1s if i_idx in th1s else th2s

       the_dict[i_idx].SetName(out_key)
       the_dict[i_idx].SetTitle(out_key)
       the_dict[i_idx].Write()

#   ROOT.gROOT.GetListOfFiles().Remove(output_tfile)
   output_tfile.Close()

   print '\033[1m'+'\033[92m'+'[output]'+'\033[0m', opts.output
   ### -------------------
