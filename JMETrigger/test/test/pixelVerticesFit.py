#!/usr/bin/env python
import sys
import ROOT

tfile = ROOT.TFile(sys.argv[1])

ttree = tfile.Get('JMETriggerNTuple/Events')

h2 = ROOT.TH2D('h2', 'h2', 120, 0, 120, 120, 0, 120)

ttree.Draw("hltPixelVertices_z@.size():offlinePrimaryVertices_z@.size()>>h2","","goff")

h2_py = h2.ProfileY('h2_py')
h2_py.Draw()

h2_py_pol1 = ROOT.TF1('h2_py_pol1', 'pol1')
h2_py.Fit(h2_py_pol1)
