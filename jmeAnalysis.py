#!/usr/bin/env python
import argparse
import os
import glob
import array
import math
import ROOT
import uproot

from common.utils import *

EvtSelections = [

  'NoSelection/',
  'hltPFMET200/',
  'hltPuppiMET200/',
]

METCollections = [

  'genMetTrue',

  'hltPFMET',
  'hltPFMETTypeOne',
  'hltPFMETNoPileUpJME',
  'hltPuppiMET',
  'hltPuppiMETTypeOne',
  'hltPuppiMETWithPuppiForJets',
  'hltSoftKillerMET',

  'offlineMETs_Raw',
  'offlineMETs_Type1',
  'offlineMETsPuppi_Raw',
  'offlineMETsPuppi_Type1',
]

METOnlineOfflinePairs = [
  ['hltPFMET', 'offlineMETs_Raw'],
  ['hltPFMETTypeOne', 'offlineMETs_Type1'],
  ['hltPuppiMET', 'offlineMETsPuppi_Raw'],
  ['hltPuppiMETTypeOne', 'offlineMETsPuppi_Type1'],
  ['hltPuppiMETWithPuppiForJets', 'offlineMETsPuppi_Raw'],
]

JetCollections = [

  'ak4GenJets',
  'hltAK4PFCHSJetsCorrected',
  'offlineAK4PFCHSJetsCorrected',
]

JetOnlineOfflinePairs = [

  ['hltAK4PFCHSJetsCorrected', 'offlineAK4PFCHSJetsCorrected'],
]

def delta_phi(phi1, phi2):
    ret = phi1 - phi2
    if ret >  math.pi: ret -= math.pi*2
    if ret < -math.pi: ret += math.pi*2
    return ret

#### Histograms --------------------------------------------------------------------------------------------------------------------

def create_histograms():

    # bin-edges for TH1Ds and TH2Ds
    binEdges_1d = {}
    binEdges_2d = {}

    for i_sel in EvtSelections:

        binEdges_1d[i_sel+'hltNPV'] = [10*_tmp for _tmp in range(40+1)]
        binEdges_1d[i_sel+'offlineNPV'] = [10*_tmp for _tmp in range(40+1)]

        ### Jets
        for i_jet in JetCollections:

            for i_reg in ['', '_HB', '_HE', '_HF']:

                binEdges_1d[i_sel+i_jet+i_reg+'_Njets'] = [_tmp for _tmp in range(12)]

                binEdges_1d[i_sel+i_jet+i_reg+'_pt'] = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 400, 500, 600, 700, 800, 1000]
                binEdges_1d[i_sel+i_jet+i_reg+'_eta'] = [-5.0, -4.7, -4.2, -3.5, -3.0, -2.7, -2.4, -2.0, -1.6, -1.2, -0.8, -0.4, 0.0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.7, 3.0, 3.5, 4.2, 4.7, 5.0]
                binEdges_1d[i_sel+i_jet+i_reg+'_phi'] = [math.pi*(2./40*_tmp-1) for _tmp in range(40+1)]

                if i_jet == 'ak4GenJets': continue

                binEdges_1d[i_sel+i_jet+i_reg+'_matchedToGEN_Njets'] = [_tmp for _tmp in range(12)]

                binEdges_1d[i_sel+i_jet+i_reg+'_matchedToGEN_pt']  = binEdges_1d[i_sel+i_jet+i_reg+'_pt']
                binEdges_1d[i_sel+i_jet+i_reg+'_matchedToGEN_eta'] = binEdges_1d[i_sel+i_jet+i_reg+'_eta']
                binEdges_1d[i_sel+i_jet+i_reg+'_matchedToGEN_phi'] = binEdges_1d[i_sel+i_jet+i_reg+'_phi']
                binEdges_1d[i_sel+i_jet+i_reg+'_matchedToGEN_dRgen'] = [0.2*_tmp for _tmp in range(25+1)]

                binEdges_1d[i_sel+i_jet+i_reg+'_matchedToGEN_pt_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]
                binEdges_1d[i_sel+i_jet+i_reg+'_matchedToGEN_pt_minusGEN']  = [-250+10*_tmp for _tmp in range(50+1)]

                for v_ref in ['ak4GenJets_pt', 'ak4GenJets_eta']:

                    if v_ref == 'ak4GenJets_pt':
                       binEdges_2d[i_sel+i_jet+i_reg+'_matchedToGEN_pt:'+v_ref] = [binEdges_1d[i_sel+i_jet+i_reg+'_matchedToGEN_pt'], binEdges_1d[i_sel+v_ref]]

                    if v_ref == 'ak4GenJets_eta':
                       binEdges_2d[i_sel+i_jet+i_reg+'_matchedToGEN_eta:'+v_ref] = [binEdges_1d[i_sel+i_jet+i_reg+'_matchedToGEN_eta'], binEdges_1d[i_sel+v_ref]]

                    binEdges_2d[i_sel+i_jet+i_reg+'_matchedToGEN_pt_overGEN:'+v_ref] = [binEdges_1d[i_sel+i_jet+i_reg+'_matchedToGEN_pt_overGEN'], binEdges_1d[i_sel+v_ref]]
                    binEdges_2d[i_sel+i_jet+i_reg+'_matchedToGEN_pt_minusGEN:'+v_ref] = [binEdges_1d[i_sel+i_jet+i_reg+'_matchedToGEN_pt_minusGEN'], binEdges_1d[i_sel+v_ref]]

        for [i_jet_onl, i_jet_off] in JetOnlineOfflinePairs:

            for i_reg in ['', '_HB', '_HE', '_HF']:

                binEdges_1d[i_sel+i_jet_onl+i_reg+'_matchedToOffline_pt'] = binEdges_1d[i_sel+i_jet_onl+i_reg+'_pt']
                binEdges_1d[i_sel+i_jet_onl+i_reg+'_matchedToOffline_pt_overOffline'] = [0.1*_tmp for _tmp in range(50+1)]
                binEdges_1d[i_sel+i_jet_onl+i_reg+'_matchedToOffline_pt_minusOffline'] = [-250+10*_tmp for _tmp in range(50+1)]
                binEdges_1d[i_sel+i_jet_onl+i_reg+'_matchedToOffline_dRoff'] = [0.2*_tmp for _tmp in range(25+1)]

                for i_var in ['_pt', '_eta']:

                    binEdges_2d[i_sel+i_jet_onl+i_reg+'_matchedToOffline_pt:'+i_jet_off+i_var] = [binEdges_1d[i_sel+i_jet_onl+i_reg+'_matchedToOffline_pt'], binEdges_1d[i_sel+i_jet_off+i_var]]
                    binEdges_2d[i_sel+i_jet_onl+i_reg+'_matchedToOffline_pt_overOffline:'+i_jet_off+i_var] = [binEdges_1d[i_sel+i_jet_onl+i_reg+'_matchedToOffline_pt_overOffline'], binEdges_1d[i_sel+i_jet_off+i_var]]
                    binEdges_2d[i_sel+i_jet_onl+i_reg+'_matchedToOffline_pt_minusOffline:'+i_jet_off+i_var] = [binEdges_1d[i_sel+i_jet_onl+i_reg+'_matchedToOffline_pt_minusOffline'], binEdges_1d[i_sel+i_jet_off+i_var]]

        ### MET
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

            binEdges_1d[i_sel+i_met+'_pt_paraToGEN'] = [-200+10*_tmp for _tmp in range(60+1)]
            binEdges_1d[i_sel+i_met+'_pt_paraToGENMinusGEN'] = [-250+10*_tmp for _tmp in range(50+1)]
            binEdges_1d[i_sel+i_met+'_pt_perpToGEN'] = [-200+10*_tmp for _tmp in range(60+1)]

            for v_ref in ['genMetTrue_pt', 'genMetTrue_sumEt', 'offlineNPV']:

                binEdges_2d[i_sel+i_met+'_pt:'+v_ref] = [binEdges_1d[i_sel+i_met+'_pt'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_phi:'+v_ref] = [binEdges_1d[i_sel+i_met+'_phi'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_sumEt:'+v_ref] = [binEdges_1d[i_sel+i_met+'_sumEt'], binEdges_1d[i_sel+v_ref]]

                binEdges_2d[i_sel+i_met+'_pt_minusGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_pt_minusGEN'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_phi_minusGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_phi_minusGEN'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_sumEt_minusGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_sumEt_minusGEN'], binEdges_1d[i_sel+v_ref]]

                binEdges_2d[i_sel+i_met+'_pt_overGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_pt_overGEN'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_phi_overGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_phi_overGEN'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_sumEt_overGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_sumEt_overGEN'], binEdges_1d[i_sel+v_ref]]

                binEdges_2d[i_sel+i_met+'_pt_paraToGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_pt_paraToGEN'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_pt_paraToGENMinusGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_pt_paraToGENMinusGEN'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_pt_perpToGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_pt_perpToGEN'], binEdges_1d[i_sel+v_ref]]

        for [i_met_onl, i_met_off] in METOnlineOfflinePairs:

            binEdges_1d[i_sel+i_met_onl+'_pt_minusOffline'] = [-250+10*_tmp for _tmp in range(50+1)]
            binEdges_1d[i_sel+i_met_onl+'_phi_minusOffline'] = [math.pi/40*_tmp for _tmp in range(40+1)]
            binEdges_1d[i_sel+i_met_onl+'_sumEt_minusOffline'] = [-250+10*_tmp for _tmp in range(50+1)]

            binEdges_1d[i_sel+i_met_onl+'_pt_overOffline'] = [0.1*_tmp for _tmp in range(50+1)]
            binEdges_1d[i_sel+i_met_onl+'_phi_overOffline'] = [0.1*_tmp for _tmp in range(50+1)]
            binEdges_1d[i_sel+i_met_onl+'_sumEt_overOffline'] = [0.1*_tmp for _tmp in range(50+1)]

            binEdges_1d[i_sel+i_met_onl+'_pt_paraToOffline'] = [-200+10*_tmp for _tmp in range(60+1)]
            binEdges_1d[i_sel+i_met_onl+'_pt_paraToOfflineMinusOffline'] = [-250+10*_tmp for _tmp in range(50+1)]
            binEdges_1d[i_sel+i_met_onl+'_pt_perpToOffline'] = [-200+10*_tmp for _tmp in range(60+1)]

            binEdges_2d[i_sel+i_met_onl+'_pt:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt'], binEdges_1d[i_sel+i_met_off+'_pt']]
            binEdges_2d[i_sel+i_met_onl+'_pt_minusOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt_minusOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]
            binEdges_2d[i_sel+i_met_onl+'_pt_overOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt_overOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]

            binEdges_2d[i_sel+i_met_onl+'_sumEt:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_sumEt'], binEdges_1d[i_sel+i_met_off+'_pt']]
            binEdges_2d[i_sel+i_met_onl+'_sumEt_minusOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_sumEt_minusOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]
            binEdges_2d[i_sel+i_met_onl+'_sumEt_overOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_sumEt_overOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]

            binEdges_2d[i_sel+i_met_onl+'_pt_paraToOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt_paraToOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]
            binEdges_2d[i_sel+i_met_onl+'_pt_paraToOfflineMinusOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt_paraToOfflineMinusOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]
            binEdges_2d[i_sel+i_met_onl+'_pt_perpToOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt_perpToOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]

    th1s = {}
    for h_name in binEdges_1d:
        th1s[h_name] = create_TH1D(h_name, binEdges_1d[h_name])

    th2s = {}
    for h_name in binEdges_2d:
        th2s[h_name] = create_TH2D(h_name, binEdges_2d[h_name])

    return th1s, th2s

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

#### Event Analysis ----------------------------------------------------------------------------------------------------------------

def analyze_event(arrays, index, th1s={}, th2s={}, verbose=False):

    values = {}

    RecoJet_minPt = 20.

    for i_sel in EvtSelections:

        if i_sel == 'hltPFMET200/':
           if not (values['NoSelection/hltPFMET_pt'] > 200.): continue

        if i_sel == 'hltPuppiMET200/':
           if not (values['NoSelection/hltPuppiMET_pt'] > 200.): continue

        values[i_sel+'hltNPV'] = len(arrays['hltGoodPrimaryVertices_z'][index])
        values[i_sel+'offlineNPV'] = len(arrays['offlinePrimaryVertices_z'][index])

        ## Jets
        for i_jet in JetCollections:

            n_jets = len(arrays[i_jet+'_pt'][index])

            for jet_idx in range(n_jets):

                jet_pt = arrays[i_jet+'_pt'][index][jet_idx]
                jet_eta = arrays[i_jet+'_eta'][index][jet_idx]
                jet_phi = arrays[i_jet+'_phi'][index][jet_idx]
                jet_mass = arrays[i_jet+'_mass'][index][jet_idx]

                if (i_jet != 'ak4GenJets') and (jet_pt < RecoJet_minPt): continue

                jet_labels = ['']
                if abs(jet_eta) < 1.3: jet_labels += ['_HB']
                elif abs(jet_eta) < 3.0: jet_labels += ['_HE']
                else: jet_labels += ['_HF']

                for i_reg in jet_labels:

                    for _tmp in [
                      i_sel+i_jet+i_reg+'_pt',
                      i_sel+i_jet+i_reg+'_eta',
                      i_sel+i_jet+i_reg+'_phi',
                    ]:
                      if _tmp not in values: values[_tmp] = []

                    values[i_sel+i_jet+i_reg+'_pt']  += [jet_pt]
                    values[i_sel+i_jet+i_reg+'_eta'] += [jet_eta]
                    values[i_sel+i_jet+i_reg+'_phi'] += [jet_phi]

                    if i_jet == 'ak4GenJets': continue

                    n_genJets = len(arrays['ak4GenJets_pt'][index])

                    genJet_match = None
                    for genJet_idx in range(n_genJets):
                        genJet_pt = arrays['ak4GenJets_pt'][index][genJet_idx]
                        genJet_eta = arrays['ak4GenJets_eta'][index][genJet_idx]
                        genJet_phi = arrays['ak4GenJets_phi'][index][genJet_idx]
                        genJet_mass = arrays['ak4GenJets_mass'][index][genJet_idx]

                        recogen_dEta = jet_eta - genJet_eta
                        recogen_dPhi = delta_phi(jet_phi, genJet_phi)
                        recogen_dR2 = (recogen_dEta*recogen_dEta + recogen_dPhi*recogen_dPhi)

                        if recogen_dR2 < 0.16:
                           if (genJet_match is None) or (recogen_dR2 < recogen_dR2min):
                              recogen_dR2min = recogen_dR2
                              genJet_match = genJet_idx

                    if genJet_match is not None:

                       for _tmp in [
                         i_sel+i_jet+i_reg+'_matchedToGEN_pt',
                         i_sel+i_jet+i_reg+'_matchedToGEN_eta',
                         i_sel+i_jet+i_reg+'_matchedToGEN_phi',
                         i_sel+i_jet+i_reg+'_matchedToGEN_dRgen',
                       ]:
                         if _tmp not in values: values[_tmp] = []

                       values[i_sel+i_jet+i_reg+'_matchedToGEN_pt'] += [jet_pt]
                       values[i_sel+i_jet+i_reg+'_matchedToGEN_eta'] += [jet_eta]
                       values[i_sel+i_jet+i_reg+'_matchedToGEN_phi'] += [jet_phi]
                       values[i_sel+i_jet+i_reg+'_matchedToGEN_dRgen'] += [math.sqrt(recogen_dR2min)]

                       genJet_match_pt = arrays['ak4GenJets_pt'][index][genJet_match]
                       genJet_match_eta = arrays['ak4GenJets_eta'][index][genJet_match]

                       if genJet_match_pt != 0:

                          for _tmp in [
                            i_sel+i_jet+i_reg+'_matchedToGEN_pt_overGEN',
                            i_sel+i_jet+i_reg+'_matchedToGEN_pt_minusGEN',
                            i_sel+i_jet+i_reg+'_matchedToGEN_pt:'         +'ak4GenJets_pt',
                            i_sel+i_jet+i_reg+'_matchedToGEN_pt_overGEN:' +'ak4GenJets_pt',
                            i_sel+i_jet+i_reg+'_matchedToGEN_pt_minusGEN:'+'ak4GenJets_pt',
                            i_sel+i_jet+i_reg+'_matchedToGEN_eta:'        +'ak4GenJets_eta',
                            i_sel+i_jet+i_reg+'_matchedToGEN_pt_overGEN:' +'ak4GenJets_eta',
                            i_sel+i_jet+i_reg+'_matchedToGEN_pt_minusGEN:'+'ak4GenJets_eta',
                          ]:
                            if _tmp not in values: values[_tmp] = []

                          values[i_sel+i_jet+i_reg+'_matchedToGEN_pt_overGEN']  += [jet_pt / genJet_match_pt]
                          values[i_sel+i_jet+i_reg+'_matchedToGEN_pt_minusGEN'] += [jet_pt - genJet_match_pt]

                          values[i_sel+i_jet+i_reg+'_matchedToGEN_pt:'         +'ak4GenJets_pt'] += [(jet_pt,  genJet_match_pt)]
                          values[i_sel+i_jet+i_reg+'_matchedToGEN_pt_overGEN:' +'ak4GenJets_pt'] += [(jet_pt / genJet_match_pt, genJet_match_pt)]
                          values[i_sel+i_jet+i_reg+'_matchedToGEN_pt_minusGEN:'+'ak4GenJets_pt'] += [(jet_pt - genJet_match_pt, genJet_match_pt)]

                          values[i_sel+i_jet+i_reg+'_matchedToGEN_eta:'        +'ak4GenJets_eta'] += [(jet_eta, genJet_match_eta)]
                          values[i_sel+i_jet+i_reg+'_matchedToGEN_pt_overGEN:' +'ak4GenJets_eta'] += [(jet_pt / genJet_match_pt, genJet_match_eta)]
                          values[i_sel+i_jet+i_reg+'_matchedToGEN_pt_minusGEN:'+'ak4GenJets_eta'] += [(jet_pt - genJet_match_pt, genJet_match_eta)]

            njets_tags = ['', '_HB', '_HE', '_HF']
            if (i_jet != 'ak4GenJets'):
               njets_tags += ['_matchedToGEN', '_HB_matchedToGEN', '_HE_matchedToGEN', '_HF_matchedToGEN']

            for i_jettag in njets_tags:
                values[i_sel+i_jet+i_jettag+'_Njets'] = len(values[i_sel+i_jet+i_jettag+'_pt']) if (i_sel+i_jet+i_jettag+'_pt' in values) else 0

        ## MET
        for i_met in METCollections:
            for i_var in ['pt', 'phi', 'sumEt']:
                values[i_sel+i_met+'_'+i_var] = arrays[i_met+'_'+i_var][index][0]

        genMetTrue_vec2d = ROOT.TVector2()
        genMetTrue_vec2d.SetMagPhi(values[i_sel+'genMetTrue_pt'], values[i_sel+'genMetTrue_phi'])

        for i_met in METCollections:

            if i_met == 'genMetTrue': continue

            values[i_sel+i_met+'_pt'], values[i_sel+i_met+'_phi']

            iMET_vec2d = ROOT.TVector2()
            iMET_vec2d.SetMagPhi(values[i_sel+i_met+'_pt'], values[i_sel+i_met+'_phi'])

            values[i_sel+i_met+'_pt_paraToGEN'] = iMET_vec2d.Mod() * math.cos(iMET_vec2d.DeltaPhi(genMetTrue_vec2d))
            values[i_sel+i_met+'_pt_perpToGEN'] = iMET_vec2d.Mod() * math.sin(iMET_vec2d.DeltaPhi(genMetTrue_vec2d))

            values[i_sel+i_met+'_pt_paraToGENMinusGEN'] = values[i_sel+i_met+'_pt_paraToGEN'] - values[i_sel+'genMetTrue_pt']

            for i_var in ['pt', 'phi', 'sumEt']:

                values[i_sel+i_met+'_'+i_var+'_minusGEN'] = values[i_sel+i_met+'_'+i_var] - values[i_sel+'genMetTrue_'+i_var]
                if i_var == 'phi':
                   values[i_sel+i_met+'_'+i_var+'_minusGEN'] = abs(values[i_sel+i_met+'_'+i_var+'_minusGEN'])
                   if values[i_sel+i_met+'_'+i_var+'_minusGEN'] > math.pi:
                      values[i_sel+i_met+'_'+i_var+'_minusGEN'] = 2*math.pi - values[i_sel+i_met+'_'+i_var+'_minusGEN']

                if values[i_sel+'genMetTrue_'+i_var] != 0:
                   values[i_sel+i_met+'_'+i_var+'_overGEN'] = values[i_sel+i_met+'_'+i_var] / values[i_sel+'genMetTrue_'+i_var]

        for [i_met_onl, i_met_off] in METOnlineOfflinePairs:

            iMETonl_vec2d = ROOT.TVector2()
            iMETonl_vec2d.SetMagPhi(values[i_sel+i_met_onl+'_pt'], values[i_sel+i_met_onl+'_phi'])

            iMEToff_vec2d = ROOT.TVector2()
            iMEToff_vec2d.SetMagPhi(values[i_sel+i_met_off+'_pt'], values[i_sel+i_met_off+'_phi'])

            values[i_sel+i_met_onl+'_pt_paraToOffline'] = iMETonl_vec2d.Mod() * math.cos(iMETonl_vec2d.DeltaPhi(iMEToff_vec2d))
            values[i_sel+i_met_onl+'_pt_perpToOffline'] = iMETonl_vec2d.Mod() * math.sin(iMETonl_vec2d.DeltaPhi(iMEToff_vec2d))

            values[i_sel+i_met_onl+'_pt_paraToOfflineMinusOffline'] = values[i_sel+i_met_onl+'_pt_paraToOffline'] - values[i_sel+i_met_off+'_pt']

            for i_var in ['pt', 'phi', 'sumEt']:

                values[i_sel+i_met_onl+'_'+i_var+'_minusOffline'] = values[i_sel+i_met_onl+'_'+i_var] - values[i_sel+i_met_off+'_'+i_var]
                if i_var == 'phi':
                   values[i_sel+i_met_onl+'_'+i_var+'_minusOffline'] = abs(values[i_sel+i_met_onl+'_'+i_var+'_minusOffline'])
                   if values[i_sel+i_met_onl+'_'+i_var+'_minusOffline'] > math.pi:
                      values[i_sel+i_met_onl+'_'+i_var+'_minusOffline'] = 2*math.pi - values[i_sel+i_met_onl+'_'+i_var+'_minusOffline']

                if values[i_sel+i_met_off+'_'+i_var] != 0:
                   values[i_sel+i_met_onl+'_'+i_var+'_overOffline'] = values[i_sel+i_met_onl+'_'+i_var] / values[i_sel+i_met_off+'_'+i_var]

    ## histogram filling
    for i_hist_key in sorted(list(set(th1s.keys() + th2s.keys()))):

        if i_hist_key in th1s:

           if i_hist_key in values:

              if isinstance(values[i_hist_key], list):
                 for _tmp in values[i_hist_key]:
                     th1s[i_hist_key].Fill(_tmp)
              else:
                 th1s[i_hist_key].Fill(values[i_hist_key])

        elif i_hist_key in th2s:

           if i_hist_key in values:

              if isinstance(values[i_hist_key], list):
                 for _tmp in values[i_hist_key]:
                     if len(_tmp) != 2: KILL('xxx1 '+i_hist_key)
                     th2s[i_hist_key].Fill(_tmp[0], _tmp[1])
              else:
                 if len(values[i_hist_key]) != 2: KILL('xxx2 '+i_hist_key)
                 th2s[i_hist_key].Fill(values[i_hist_key][0], values[i_hist_key][1])

           else:
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

              if isinstance(values[i_hist_key_varX], list):
                 if not isinstance(values[i_hist_key_varY], list): KILL('YYY')
                 if len(values[i_hist_key_varX]) != len(values[i_hist_key_varY]): KILL(i_hist_key_varX+' '+i_hist_key_varY)
                 for _tmp in range(len(values[i_hist_key_varX])):
                     th2s[i_hist_key].Fill(values[i_hist_key_varX][_tmp], values[i_hist_key_varY][_tmp])
              else:
                 th2s[i_hist_key].Fill(values[i_hist_key_varX], values[i_hist_key_varY])

    if verbose:
       for _tmp in sorted(values.keys()):
           if 'met' in _tmp.lower(): continue
           if 'jets' not in _tmp.lower(): continue
           print colored_text(_tmp, ['1','95']), values[_tmp]

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

   parser.add_argument('-e', '--every', dest='every', action='store', type=int, default=1e2,
                       help='show progress of processing every N events')

   parser.add_argument('-f', '--firstEvent', dest='firstEvent', action='store', type=int, default=0,
                       help='index of first event to be processed (inclusive)')

   parser.add_argument('-l', '--lastEvent', dest='lastEvent', action='store', type=int, default=-1,
                       help='index of last event to be processed (inclusive)')

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
      KILL(log_prx+'empty list of input files [-i]')

   if os.path.exists(opts.output):
      KILL(log_prx+'target path to output .root file already exists [-o]: '+opts.output)

   SHOW_EVERY = opts.every
   if SHOW_EVERY <= 0:
      WARNING(log_prx+'invalid (non-positive) value for option "-e/--every" ('+str(SHOW_EVERY)+'), value will be changed to 100')
      SHOW_EVERY = 1e2

   if len(opts_unknown) > 0:
      KILL(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))
   ### -------------------

   # convert bin-edges to TH1D
   th1s, th2s = create_histograms()

   for i_inpf in INPUT_FILES:

       if opts.verbose: print colored_text('[input]', ['1','92']), os.path.relpath(i_inpf)

       try:
          i_ttree = uproot.open(i_inpf)[opts.tree]
       except:
          WARNING(log_prx+'target TFile does not contain a TTree named "'+opts.tree+'" (file will be ignored) [-t]: '+i_inpf)
          continue

       print 'loading content of TBranches into arrays..'
       arr_entrystart = 0 if opts.firstEvent < 0 else opts.firstEvent
       arr_entrystop = i_ttree.numentries if opts.lastEvent < 0 else min(i_ttree.numentries, opts.lastEvent + 1)

       if arr_entrystart > arr_entrystop:
          KILL(log_prx+'logic error: entry-start ('+str(arr_entrystart)+') is higher than entry-stop ('+str(arr_entrystop)+')')

       arr = i_ttree.arrays('*', entrystart=arr_entrystart, entrystop=arr_entrystop)
       print 'done'

       for evt_idx in range(arr_entrystop - arr_entrystart):

           analyze_event(arrays=arr, index=evt_idx, th1s=th1s, th2s=th2s, verbose=opts.verbose)

           if not (evt_idx % SHOW_EVERY) and (evt_idx > 0):
              print colored_text('['+str(os.path.relpath(opts.output))+']', ['1','93']), 'events processed:', evt_idx

       print 'events processed:', (arr_entrystop - arr_entrystart)

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

   print colored_text('[output]', ['1','92']), os.path.relpath(opts.output)
   ### -------------------
