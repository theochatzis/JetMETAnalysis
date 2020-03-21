#!/usr/bin/env python
"""merge outputs of batch jobs"""
import os
import argparse
import glob
import array
import re
import ROOT

from common.utils import *

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

           if opts.verbose: print colored_text('[input]', ['1', '92']), out_key

    return dictionary

def getTH1sFromTFile(path):

    input_histos_dict = {}

    i_inptfile = ROOT.TFile.Open(path)
    if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered):
       return input_histos_dict

    updateDictionary(input_histos_dict, i_inptfile, prefix='')

    i_inptfile.Close()

    return input_histos_dict

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser(description=__doc__)

   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=[],
                       help='path to input file(s)')

   parser.add_argument('-o', '--output', dest='output', required=True, action='store', default='',
                       help='path to output file (1 input) or directory (multiple inputs')

   parser.add_argument('-l', '--level', dest='level', action='store', type=int, default=0,
                       help='level of directory depth in output directory')

   parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                       help='enable verbose mode')

   parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                       help='enable dry-run mode')

   opts, opts_unknown = parser.parse_known_args()
   ### -------------------

   log_prx = os.path.basename(__file__)+' -- '

   ROOT.gROOT.SetBatch()

   ROOT.gErrorIgnoreLevel = ROOT.kWarning

   ### args validation ---
   if opts.level < 0:
      KILL(log_prx+'negative level of directory depth in output directory (must be >=0) [-l]: '+str(opts.level))

   INPUT_FILES = []
   for i_inpf in opts.inputs:
       i_inpf_ls = glob.glob(i_inpf)
       for i_inpf_2 in i_inpf_ls:
           if os.path.isfile(i_inpf_2):
              INPUT_FILES += [os.path.abspath(os.path.realpath(i_inpf_2))]
   INPUT_FILES = sorted(list(set(INPUT_FILES)))

   if len(INPUT_FILES) == 0:
      KILL(log_prx+'empty list of input files')

   if os.path.exists(opts.output):
      KILL(log_prx+'target path to output file/directory already exists [-o]: '+opts.output)
   ### -------------------

   ROOT.TH1.AddDirectory(False)

   for inpf in INPUT_FILES:

       ### Input Histograms
       histograms = getTH1sFromTFile(inpf)

       ### Histograms for profile of Mean
       for i_h2_key in sorted(histograms.keys()):

           if not histograms[i_h2_key].InheritsFrom('TH2'):
              continue

           i_h2_key_basename = os.path.basename(i_h2_key)

           i_h2_key_dirname = os.path.dirname(i_h2_key)
           if i_h2_key_dirname: i_h2_key_dirname += '/'

           key_vars_split = i_h2_key_basename.split(':')
           if len(key_vars_split) != 2:
              KILL('ZZZ '+i_h2_key_basename)

           key_varX = key_vars_split[0]
           key_varY = key_vars_split[1]

           if not (key_varX.endswith('GEN') or key_varX.endswith('Offline')):
              continue

           tmp_h2 = histograms[i_h2_key]

           # Mean of X, in bins of Y
           h_name0 = i_h2_key_dirname+key_varX+'_Mean_wrt_'+key_varY
           if h_name0 in histograms: KILL('aaa1 '+h_name0)

           tmp_h1_xMean = tmp_h2.ProjectionY(h_name0)
           tmp_h1_xMean.SetDirectory(0)
           tmp_h1_xMean.Reset()

           for _idx in range(1, 1+tmp_h2.GetNbinsY()):
               _htmp = tmp_h2.ProjectionX('_htmp'+str(_idx), _idx, _idx, 'e')
               _htmp.SetDirectory(0)
               tmp_h1_xMean.SetBinContent(_idx, _htmp.GetMean())
               tmp_h1_xMean.SetBinError(_idx, _htmp.GetMeanError())
               del _htmp

           histograms[h_name0] = tmp_h1_xMean
       ### -------------------

       ### Histograms for profile of RMS
       ### (requires mean-Response histograms created in previous block)
       for i_h2_key in sorted(histograms.keys()):

           if not histograms[i_h2_key].InheritsFrom('TH2'):
              continue

           i_h2_key_basename = os.path.basename(i_h2_key)

           i_h2_key_dirname = os.path.dirname(i_h2_key)
           if i_h2_key_dirname: i_h2_key_dirname += '/'

           key_vars_split = i_h2_key_basename.split(':')
           if len(key_vars_split) != 2:
              KILL('ZZZ '+i_h2_key_basename)

           key_varX = key_vars_split[0]
           key_varY = key_vars_split[1]

           if key_varX.endswith('GEN'): compTag = 'GEN'
           elif key_varX.endswith('Offline'): compTag = 'Offline'
           else: continue

           tmp_h2 = histograms[i_h2_key]

           # RMS of X, in bins of Y
           h_name1 = i_h2_key_dirname+key_varX+'_RMS_wrt_'+key_varY
           if h_name1 in histograms: KILL('aaa3 '+h_name1)

           tmp_h1_xRMS = tmp_h2.ProjectionY(h_name1)
           tmp_h1_xRMS.SetDirectory(0)
           tmp_h1_xRMS.Reset()

           for _idx in range(1, 1+tmp_h2.GetNbinsY()):
               _htmp = tmp_h2.ProjectionX('_htmp'+str(_idx), _idx, _idx, 'e')
               _htmp.SetDirectory(0)
               tmp_h1_xRMS.SetBinContent(_idx, _htmp.GetRMS())
               tmp_h1_xRMS.SetBinError(_idx, _htmp.GetRMSError())
               del _htmp

           histograms[h_name1] = tmp_h1_xRMS

           # RMS of X scaled by Response, in bins of Y
           h_name2 = i_h2_key_dirname+key_varX+'_RMSScaledByResponse_wrt_'+key_varY
           if h_name2 in histograms: KILL('aaa4 '+h_name2)

           h_name4 = i_h2_key_dirname+key_varX[:key_varX.rfind('_')]+'_over'+compTag+'_Mean_wrt_'+key_varY
           if h_name4 not in histograms: KILL('aaa5 '+h_name4)

           tmp_h1_ratioMeanNoErr = histograms[h_name4].Clone()
           for _idx in range(tmp_h1_ratioMeanNoErr.GetNbinsX()+2):
               tmp_h1_ratioMeanNoErr.SetBinError(_idx, 0)

           tmp_h1_xRMSScaled = tmp_h1_xRMS.Clone()
           tmp_h1_xRMSScaled.SetName(h_name2)
           tmp_h1_xRMSScaled.SetDirectory(0)
           tmp_h1_xRMSScaled.Divide(tmp_h1_ratioMeanNoErr)

           histograms[h_name2] = tmp_h1_xRMSScaled
       ### -------------------

       ### output file -------
       output_file = None
       if len(INPUT_FILES) == 1:
          output_file = opts.output
       else:
          input_name_pieces = [os.path.basename(inpf)]
          input_dirname = os.path.dirname(inpf)
          while opts.level >= len(input_name_pieces):
             input_name_pieces.insert(0, os.path.basename(input_dirname))
             input_dirname = os.path.dirname(input_dirname)
          del input_dirname
          output_file = opts.output+'/'+('/'.join(input_name_pieces))

       if os.path.exists(output_file):
          KILL(log_prx+'logic error - target output file already exists: '+output_file)

       output_dirname = os.path.dirname(os.path.abspath(output_file))
       if not os.path.isdir(output_dirname):
          EXE('mkdir -p '+output_dirname, verbose=opts.verbose, dry_run=opts.dry_run)
       del output_dirname

       if not opts.dry_run:
          output_tfile = ROOT.TFile(output_file, 'create')
          if (not output_tfile) or output_tfile.IsZombie() or output_tfile.TestBit(ROOT.TFile.kRecovered):
             raise SystemExit(1)

          for i_idx in sorted(histograms.keys()):

              output_tfile.cd()

              out_key = i_idx

              while '/' in out_key:
                 slash_index = out_key.find('/')
                 out_dir = out_key[:slash_index]
                 out_key = out_key[slash_index+1:]
                 out_dir = getattr(output_tfile, 'Get' if output_tfile.Get(out_dir) else 'mkdir')(out_dir)
                 out_dir.cd()

              histograms[i_idx].SetName(out_key)
              histograms[i_idx].SetTitle(out_key)
              histograms[i_idx].Write()

          output_tfile.Close()

       print colored_text('[output]', ['1','92']), output_file
       ### -------------------
