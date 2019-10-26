#!/usr/bin/env python
import argparse
import os
import glob
import array
import math
import ROOT

from common.utils import *
from common.th1 import *

#### Histograms --------------------------------------------------------------------------------------------------------------------

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

output_histos_dict = {}

output_histos_dict['hltNPV'] = [10*_tmp for _tmp in range(40+1)]
output_histos_dict['offlineNPV'] = [10*_tmp for _tmp in range(40+1)]

for i_met in METCollections:
    output_histos_dict[i_met+'_pt'] = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 250, 300, 400, 500, 600, 700, 800, 1000]
    output_histos_dict[i_met+'_phi'] = [math.pi*(2./40*_tmp-1) for _tmp in range(40+1)]
    output_histos_dict[i_met+'_sumEt'] = [0, 30, 60, 90, 120, 180, 250, 400, 600, 800, 1000, 1500, 2000, 3000]

    if i_met == 'genMetTrue': continue

    output_histos_dict[i_met+'_pt_minusGEN'] = [-250+10*_tmp for _tmp in range(50+1)]
    output_histos_dict[i_met+'_phi_minusGEN'] = [math.pi/40*_tmp for _tmp in range(40+1)]
    output_histos_dict[i_met+'_sumEt_minusGEN'] = [-250+10*_tmp for _tmp in range(50+1)]

    output_histos_dict[i_met+'_pt_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]
    output_histos_dict[i_met+'_phi_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]
    output_histos_dict[i_met+'_sumEt_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]

for i_met in METCollections:

    if i_met.startswith('hlt'): continue

    output_histos_dict['hltPFMET200/'+i_met+'_pt'] = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 250, 300, 400, 500, 600, 700, 800, 1000]

#### Event Analysis ----------------------------------------------------------------------------------------------------------------

def analyze_event(event, histograms):

    values = {}

    values['hltNPV'] = len(event.hltGoodPrimaryVertices_z)
    values['offlineNPV'] = len(event.offlinePrimaryVertices_z)

    for i_met in METCollections:
        for i_var in ['pt', 'phi', 'sumEt']:
            values[i_met+'_'+i_var] = getattr(event, i_met+'_'+i_var)[0]

    for i_met in METCollections:

        if i_met == 'genMetTrue': continue

        for i_var in ['pt', 'phi', 'sumEt']:

            values[i_met+'_'+i_var+'_minusGEN'] = values[i_met+'_'+i_var] - values['genMetTrue_'+i_var]
            if i_var == 'phi':
               values[i_met+'_'+i_var+'_minusGEN'] = abs(values[i_met+'_'+i_var+'_minusGEN'])
               if values[i_met+'_'+i_var+'_minusGEN'] > math.pi:
                  values[i_met+'_'+i_var+'_minusGEN'] = 2*math.pi - values[i_met+'_'+i_var+'_minusGEN']

            if values['genMetTrue_'+i_var] != 0:
               values[i_met+'_'+i_var+'_overGEN'] = values[i_met+'_'+i_var] / values['genMetTrue_'+i_var]

    if values['hltPFMET_pt'] > 200.:
       for i_met in METCollections:
           if i_met.startswith('hlt'): continue
           values['hltPFMET200/'+i_met+'_pt'] = values[i_met+'_pt']

    for i_val_key in values:
        histograms[i_val_key].Fill(values[i_val_key])

#### -------------------------------------------------------------------------------------------------------------------------------
#### -------------------------------------------------------------------------------------------------------------------------------
#### -------------------------------------------------------------------------------------------------------------------------------

def create_TH1D(name, binEdges):

    _binEdges_array = array.array('d', sorted(list(set(binEdges))))

    _th1d = ROOT.TH1D(name, name, len(_binEdges_array)-1, _binEdges_array)
    _th1d.SetDirectory(0)
    _th1d.Sumw2()

    return _th1d

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser()

   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=None,
                       help='path to input .root file(s)')

   parser.add_argument('-o', '--output', dest='output', required=True, action='store', default=None,
                       help='path to output .root file')

   parser.add_argument('-t', '--tree', dest='tree', action='store', default='JMETriggerNTuple/Events',
                       help='key of TTree in input file(s)')

#   parser.add_argument('--only-keys', dest='only_keys', nargs='+', default=['/HLT/', '/TOP/'],
#                       help='list of strings required to be in histogram key')
#
#   parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['png'],
#                       help='list of extension(s) for output file(s)')
#
#   parser.add_argument('-n', '--name-only', dest='name_only', action='store_true', default=False,
#                       help='only print name of input histograms')

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
   for h_name in output_histos_dict:
       output_histos_dict[h_name] = create_TH1D(h_name, output_histos_dict[h_name])

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
           analyze_event(event=i_evt, histograms=output_histos_dict)

       i_inptfile.Close()

   ### output file -------
   output_dirname = os.path.dirname(os.path.abspath(opts.output))
   if not os.path.isdir(output_dirname): EXE('mkdir -p '+output_dirname)
   del output_dirname

   output_tfile = ROOT.TFile(opts.output, 'recreate')
   if (not output_tfile) or output_tfile.IsZombie() or output_tfile.TestBit(ROOT.TFile.kRecovered):
      raise SystemExit(1)

   for i_idx in sorted(output_histos_dict.keys()):

       output_tfile.cd()

       out_key = i_idx

       while '/' in out_key:
          slash_index = out_key.find('/')
          out_dir = out_key[:slash_index]
          out_key = out_key[slash_index+1:]
          out_dir = getattr(output_tfile, 'Get' if output_tfile.Get(out_dir) else 'mkdir')(out_dir)
          out_dir.cd()

       output_histos_dict[out_key] = th1_mergeUnderflowBinIntoFirstBin(output_histos_dict[out_key])
       output_histos_dict[out_key] = th1_mergeOverflowBinIntoLastBin(output_histos_dict[out_key])

       output_histos_dict[out_key].SetName(out_key)
       output_histos_dict[out_key].SetTitle(out_key)
       output_histos_dict[out_key].Write()

#   ROOT.gROOT.GetListOfFiles().Remove(output_tfile)
   output_tfile.Close()

   print '\033[1m'+'\033[92m'+'[output]'+'\033[0m', opts.output
   ### -------------------
