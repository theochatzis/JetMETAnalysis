#!/usr/bin/env python
import os
import ROOT

outputDir = 'plots_tmp'
os.makedirs(outputDir)

ROOT.gROOT.SetBatch()

from common.plot_style import apply_style
apply_style(0)

for pfAlgo in ['PF', 'PFPuppi']:

 for key in [0, 1, 2]:

  if key == 0:
   inputNtuplesDir = 'output_hltPhase2_201002_v2/ntuples'
   ntupleName = 'Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200'
   outputTag = pfAlgo+'_HLT_TRKv06vs07p2'
   reco0 = 'HLT_TRKv06'
   reco1 = 'HLT_TRKv07p2'
   reco2 = ''
   color0 = 1
   color1 = ROOT.kGray

  elif key == 1:
   inputNtuplesDir = 'output_hltPhase2_201002_v2/ntuples'
   ntupleName = 'Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200'
   outputTag = pfAlgo+'_HLT_TRKv06'
   reco0 = 'HLT_TRKv06'
   reco1 = 'HLT_TRKv06_TICL'
   reco2 = 'HLT_TRKv06_TICL2'
   color0 = 1
   color1 = 2
   color2 = 4

  elif key == 2:
   inputNtuplesDir = 'output_hltPhase2_201002_v2/ntuples'
   ntupleName = 'Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200'
   outputTag = pfAlgo+'_HLT_TRKv07p2'
   reco0 = 'HLT_TRKv07p2'
   reco1 = 'HLT_TRKv07p2_TICL'
   reco2 = 'HLT_TRKv07p2_TICL2'
   color0 = ROOT.kGray
   color1 = ROOT.kOrange+1
   color2 = ROOT.kViolet-1

  else:
   raise RuntimeError(key)

  f0 = ROOT.TFile.Open(inputNtuplesDir+'/'+reco0+'/'+ntupleName+'.root')
  f1 = ROOT.TFile.Open(inputNtuplesDir+'/'+reco1+'/'+ntupleName+'.root')
  f2 = ROOT.TFile.Open(inputNtuplesDir+'/'+reco2+'/'+ntupleName+'.root')

  t0 = f0.Get("JMETriggerNTuple/Events") if f0 else None
  t1 = f1.Get("JMETriggerNTuple/Events") if f1 else None
  t2 = f2.Get("JMETriggerNTuple/Events") if f2 else None

  canvases = []

  for _tmp in [
    {
      'outputName': outputDir+'/'+ntupleName+'_'+outputTag+'_jpt030.pdf',
      'cut': 'hltAK4'+pfAlgo+'JetsCorrected_pt > 30',
      'title': ';Jet p_{T} [GeV];Entries',
      'objLabel': 'hltAK4'+pfAlgo+'Jets, pT > 30 GeV',
      'topLabel': ntupleName,
      'var': 'hltAK4'+pfAlgo+'JetsCorrected_eta',
      'xnbins': 55,
      'xmin': -5.5,
      'xmax': 5.5,
      'logY': 0,
    },
    {
      'outputName': outputDir+'/'+ntupleName+'_'+outputTag+'_jpt050.pdf',
      'cut': 'hltAK4'+pfAlgo+'JetsCorrected_pt > 50',
      'title': ';Jet p_{T} [GeV];Entries',
      'objLabel': 'hltAK4'+pfAlgo+'Jets, pT > 50 GeV',
      'topLabel': ntupleName,
      'var': 'hltAK4'+pfAlgo+'JetsCorrected_eta',
      'xnbins': 55,
      'xmin': -5.5,
      'xmax': 5.5,
      'logY': 0,
    },
    {
      'outputName': outputDir+'/'+ntupleName+'_'+outputTag+'_jpt100.pdf',
      'cut': 'hltAK4'+pfAlgo+'JetsCorrected_pt > 100',
      'title': ';Jet p_{T} [GeV];Entries',
      'objLabel': 'hltAK4'+pfAlgo+'Jets, pT > 100 GeV',
      'topLabel': ntupleName,
      'var': 'hltAK4'+pfAlgo+'JetsCorrected_eta',
      'xnbins': 55,
      'xmin': -5.5,
      'xmax': 5.5,
      'logY': 0,
    },
    {
      'outputName': outputDir+'/'+ntupleName+'_'+outputTag+'_'+pfAlgo+'MET.pdf',
      'cut': '',
      'title': ';MET [GeV];Entries',
      'objLabel': 'hlt'+pfAlgo+'MET',
      'topLabel': ntupleName,
      'var': 'hlt'+pfAlgo+'MET_pt',
      'xnbins': 100,
      'xmin': 0,
      'xmax': 400,
      'logY': 1,
    },
  ]:
    h0 = None
    h1 = None
    h2 = None

    histoNamePostfix = '_'+str(len(canvases))

    if t0:
      h0 = ROOT.TH1D('h0'+histoNamePostfix, 'h0'+histoNamePostfix, _tmp['xnbins'], _tmp['xmin'], _tmp['xmax'])
      h0.Sumw2()
      h0.SetMarkerSize(0.)
      h0.SetLineWidth(2)
      h0.SetLineColor(color0)
      t0.Draw(_tmp['var']+'>>h0'+histoNamePostfix, _tmp['cut'], 'goff')
  
    if t1:
      h1 = ROOT.TH1D('h1'+histoNamePostfix, 'h1'+histoNamePostfix, _tmp['xnbins'], _tmp['xmin'], _tmp['xmax'])
      h1.Sumw2()
      h1.SetMarkerSize(0.)
      h1.SetLineWidth(2)
      h1.SetLineColor(color1)
      t1.Draw(_tmp['var']+'>>h1'+histoNamePostfix, _tmp['cut'], 'goff')
  
    if t2:
      h2 = ROOT.TH1D('h2'+histoNamePostfix, 'h2'+histoNamePostfix, _tmp['xnbins'], _tmp['xmin'], _tmp['xmax'])
      h2.Sumw2()
      h2.SetMarkerSize(0.)
      h2.SetLineWidth(2)
      h2.SetLineColor(color2)
      t2.Draw(_tmp['var']+'>>h2'+histoNamePostfix, _tmp['cut'], 'goff')
  
    canvas = ROOT.TCanvas('c'+histoNamePostfix, 'c'+histoNamePostfix)
    canvas.cd()

    h1st = None
    hmax = -1.
    for _tmp2 in [h0, h1, h2]:
      if _tmp2 is not None:
        _tmp2.Draw('hist,e'+(h1st is not None)*',same')
        if h1st is None: h1st = _tmp2
        hmax = max(hmax, _tmp2.GetMaximum())
  
    topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDCNB')
    topLabel.SetFillColor(0)
  # topLabel.SetFillStyle(3000)
    topLabel.SetTextColor(ROOT.kBlack)
    topLabel.SetTextAlign(12)
    topLabel.SetTextFont(42)
    topLabel.SetTextSize(0.035)
    topLabel.SetBorderSize(10)
    topLabel.AddText(_tmp['topLabel'])
    topLabel.Draw('same')

    objLabel = ROOT.TPaveText(0.18, 0.82, 0.64, 0.88, 'NDC')
    objLabel.SetFillColor(0)
  # objLabel.SetFillStyle(3000)
    objLabel.SetTextColor(ROOT.kBlack)
    topLabel.SetTextAlign(11)
    objLabel.SetTextFont(42)
    objLabel.SetTextSize(0.0325)
    objLabel.SetBorderSize(0)
    objLabel.AddText(_tmp['objLabel'])
    objLabel.Draw('same')
  
    leg = ROOT.TLegend(0.65, 0.70, 0.95, 0.90)
    leg.SetNColumns(1)
    if h0: leg.AddEntry(h0, reco0, 'le')
    if h1: leg.AddEntry(h1, reco1, 'le')
    if h2: leg.AddEntry(h2, reco2, 'le')
    leg.Draw('same')

    h1st.SetTitle(_tmp['title'])
    h1st.GetYaxis().SetTitleOffset(h1st.GetYaxis().GetTitleOffset() * 1.2)
    if _tmp['logY']:
      h1st.GetYaxis().SetRangeUser(1, hmax**(1./0.8))  
    else:
      h1st.GetYaxis().SetRangeUser(0, hmax* (1./0.8))  

    canvas.SetLogy(_tmp['logY'])
    canvas.SetGrid(1, 1)

    canvas.SaveAs(_tmp['outputName'])
    canvases.append(canvas)
    canvas.Close()

  if f0: f0.Close()
  if f1: f1.Close()
  if f2: f2.Close()
