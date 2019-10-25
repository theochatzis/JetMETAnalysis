#!/usr/bin/env python
import argparse
import os
import glob
import array
import ROOT

from common.utils import *
from common.th1 import *

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
    output_histos_dict[i_met+'_phi'] = [3.1416*(2./40*_tmp-1) for _tmp in range(40+1)]
    output_histos_dict[i_met+'_sumEt'] = [0, 30, 60, 90, 120, 180, 250, 400, 600, 800, 1000, 1500, 2000, 3000]

    if i_met == 'genMetTrue': continue

    output_histos_dict[i_met+'_pt_minusGEN'] = [-250+10*_tmp for _tmp in range(50+1)]
    output_histos_dict[i_met+'_phi_minusGEN'] = [-2.5+0.1*_tmp for _tmp in range(50+1)]
    output_histos_dict[i_met+'_sumEt_minusGEN'] = [-250+10*_tmp for _tmp in range(50+1)]

    output_histos_dict[i_met+'_pt_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]
    output_histos_dict[i_met+'_phi_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]
    output_histos_dict[i_met+'_sumEt_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]

for i_met in METCollections:

    if i_met.startswith('hlt'): continue

    output_histos_dict['hltPFMET200/'+i_met+'_pt'] = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 250, 300, 400, 500, 600, 700, 800, 1000]

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

   parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['png'],
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

   print '\033[1m'+'\033[92m'+'[output]'+'\033[0m', opts.output
   ### -------------------
