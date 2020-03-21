#!/usr/bin/env python
from __future__ import print_function

import time
start = time.time()

import ROOT
if ROOT.gSystem.Load('libAnalysisJMETrigger'):
   raise RuntimeError('failed to load library: libAnalysisJMETrigger.so')

nevts = 0
plugin = 'JMETriggerAnalysisDriver'

if hasattr(ROOT, plugin):
   a = getattr(ROOT, plugin)('ntuples/HLT_iter2GlobalPtSeed0p9/Run3Winter20_QCD_Pt_170to300_14TeV.root', 'JMETriggerNTuple/Events')
   a.setOutputFilePath("out.root")
   a.setOutputFileMode("recreate")
   a.addOption("a", "a")
   a.process(0, -1)
   nevts = a.eventsProcessed()

finish = time.time()
print('-'*35)
print('events processed: {:d}'.format(nevts))
print('execution time [sec]: {:.5f}'.format(finish - start))
print('-'*35)
