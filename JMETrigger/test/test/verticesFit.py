#!/usr/bin/env python
import sys
import ROOT

tfile = ROOT.TFile(sys.argv[1])

ttree = tfile.Get('JMETriggerNTuple/Events')

h2 = ROOT.TH2D('h2', 'h2', 250, 0, 250, 250, 0, 250)
#ttree.Draw("offlineFixedGridRhoFastjetAll:offlinePrimaryVertices_z@.size()>>h2","","goff")
#ttree.Draw("fixedGridRhoFastjetAllTmp:offlinePrimaryVertices_z@.size()>>h2","","goff")
#ttree.Draw("hltPixelVertices_z@.size():offlinePrimaryVertices_z@.size()>>h2","","goff")
ttree.Draw("hltPrimaryVertices_z@.size():offlinePrimaryVertices_z@.size()>>h2","","goff")
#ttree.Draw("pileupInfo_BX0_numPUInteractions:hltPixelVertices_z@.size()>>h2","","goff")
#ttree.Draw("pileupInfo_BX0_numPUInteractions:hltPrimaryVertices_z@.size()>>h2","","goff")
#ttree.Draw("pileupInfo_BX0_numPUInteractions:offlinePrimaryVertices_z@.size()>>h2","","goff")
#ttree.Draw("pileupInfo_BX0_numPUInteractions:fixedGridRhoFastjetAllTmp>>h2","","goff")
#ttree.Draw("pileupInfo_BX0_numPUInteractions:offlineFixedGridRhoFastjetAll>>h2","","goff")
#ttree.Draw("pileupInfo_BX0_numPUInteractions:n_hltPixelTracks>>h2","","goff")

#h2 = ROOT.TH2D('h2', 'h2', 250, 0, 250, 250, 0, 250)
#ttree.Draw("pileupInfo_BX0_numPUInteractions:hltPixelVertices_z@.size()>>h2","","goff")
#ttree.Draw("pileupInfo_BX0_numPUInteractions:hltPixelVerticesForPuppi1_z@.size()>>h2","","goff")
#ttree.Draw("pileupInfo_BX0_numPUInteractions:hltPixelVerticesForPuppi2_z@.size()>>h2","","goff")
#ttree.Draw("pileupInfo_BX0_numPUInteractions:hltPixelVerticesForPuppi3_z@.size()>>h2","","goff")
#ttree.Draw("pileupInfo_BX0_numPUInteractions:hltPixelVerticesForPuppi4_z@.size()>>h2","","goff")
#ttree.Draw("pileupInfo_BX0_numPUInteractions:hltPixelVerticesForPuppi5_z@.size()>>h2","","goff")
#ttree.Draw("pileupInfo_BX0_numPUInteractions:hltPixelVerticesForPuppi6_z@.size()>>h2","","goff")
#ttree.Draw("pileupInfo_BX0_numPUInteractions:hltPixelVerticesForPuppi7_z@.size()>>h2","","goff")

#h2 = ROOT.TH2D('h2', 'h2', 250, 0, 250, 300, 0, 3000)
#ttree.Draw("n_hltPixelTracks:offlinePrimaryVertices_z@.size()>>h2","","goff")
#ttree.Draw("n_hltPixelTracks:pileupInfo_BX0_numPUInteractions>>h2","","goff")

h2_py = h2.ProfileY('h2_py')
h2_py.Draw()

h2_py_pol1 = ROOT.TF1('h2_py_pol1', 'pol1')
h2_py.Fit(h2_py_pol1)
