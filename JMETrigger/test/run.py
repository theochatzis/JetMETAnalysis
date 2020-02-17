#!/usr/bin/env python
from __future__ import print_function
import time
start = time.time()

import ROOT
if ROOT.gSystem.Load('libAnalysisJMETrigger'):
   raise RuntimeError('failed to load library: libAnalysisJMETrigger.so')

a = ROOT.JMETriggerAnalysisDriver('../../Old/test/ntuples_prod_v06/QCD_Pt_15to3000_Flat_14TeV_PU200.root', 'JMETriggerNTuple/Events')
a.setOutputFilePath("out.root");
a.setOutputFileMode("recreate");
a.addOption("a", "a");
a.process(0, -1);

finish = time.time()
print('-'*35)
print('events processed:', a.eventsProcessed())
print('execution time [sec]:', finish - start)
print('-'*35)
