#!/usr/bin/env python
"""merge outputs of batch jobs"""
import os
import argparse
import glob
import array
import re
import ROOT

from common.utils import *

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser(description=__doc__)

   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=[],
                       help='path to input file(s)')

   parser.add_argument('-o', '--output', dest='output', required=True, action='store', default='',
                       help='path to output directory')

#   parser.add_argument('-t', '--tree-name', dest='tree_name', action='store', default='tree',
#                       help='TTree key in input file(s)')

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
   if os.path.exists(opts.output):
      KILL(log_prx+'target path to output directory already exists [-o]: '+opts.output)

   # inputs
   INPUT_FILES = []

   for i_inpf in opts.inputs:

       i_inpf_ls = glob.glob(i_inpf)

       for i_inpf_2 in i_inpf_ls:

           if os.path.isfile(i_inpf_2):
              INPUT_FILES += [os.path.abspath(os.path.realpath(i_inpf_2))]

   INPUT_FILES = sorted(list(set(INPUT_FILES)))

   if len(INPUT_FILES) == 0:
      KILL(log_prx+'empty list of input files')

   # outputs
   outputs_dict = {}

   for i_input in INPUT_FILES:

       input_basename_woExt = os.path.splitext(os.path.basename(i_input))[0]

       input_basename_woExt_splits = input_basename_woExt.split('__')

       if len(input_basename_woExt_splits) != 2:
          KILL(log_prx+'input file name with invalid format: '+i_input)

       if not is_int(input_basename_woExt_splits[1]):
          KILL(log_prx+'input file name with invalid format: '+i_input)

       output_name = input_basename_woExt_splits[0]

       if output_name not in outputs_dict: outputs_dict[output_name] = []

       outputs_dict[output_name] += [i_input]

   EXE('mkdir -p '+opts.output, verbose=opts.verbose, dry_run=opts.dry_run)

   for i_output in sorted(outputs_dict.keys()):

       i_output_path = opts.output+'/'+i_output+'.root'

       if len(outputs_dict[i_output]) == 1:

          if opts.verbose:
             print colored_text('['+i_output+']', ['1', '93']), 'copying the only input file'

          EXE('cp '+outputs_dict[i_output][0]+' '+i_output_path, verbose=opts.verbose, dry_run=opts.dry_run)

       else:

          if opts.verbose:
             print colored_text('['+i_output+']', ['1', '93']), 'attempting to merge', len(outputs_dict[i_output]), 'input files'

          i_input_files = outputs_dict[i_output].sort()

          i_merger = ROOT.TFileMerger(False, True)
          i_merger.OutputFile(i_output_path)
          for _tmp in outputs_dict[i_output]: i_merger.AddFile(_tmp)

          if i_merger.HasCompressionChange():
             print colored_text('[output='+i_output_path+']', ['1']), 'compression-level of output file differs from that of input files, merging will be slower'

          ret = i_merger.Merge()
          if not ret:
             WARNING(log_prx+'TFileMerger::Merge() did not succeed for sample "'+i_output+'"')

       print colored_text('['+i_output+']', ['1', '92'])
