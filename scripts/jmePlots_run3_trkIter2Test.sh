#!/bin/bash

jmePlots_run3.py -o tmptmp -l QCD_Pt_170to300 -e pdf png -i \
 ${JMEANA_BASE}/analysis_output_run3_v02/outputs_postHarvesting/HLT/Run3Winter20_QCD_Pt_170to300_14TeV.root:'Reg 0.4':1 \
 ${JMEANA_BASE}/analysis_output_run3_v02/outputs_postHarvesting/HLT_iter2RegionalPtSeed0p9/Run3Winter20_QCD_Pt_170to300_14TeV.root:'Reg 0.9':920 \
 ${JMEANA_BASE}/analysis_output_run3_v02/outputs_postHarvesting/HLT_iter2RegionalPtSeed2p0/Run3Winter20_QCD_Pt_170to300_14TeV.root:'Reg 2.0':800 \
 ${JMEANA_BASE}/analysis_output_run3_v02/outputs_postHarvesting/HLT_iter2RegionalPtSeed5p0/Run3Winter20_QCD_Pt_170to300_14TeV.root:'Reg 5.0':880 \
 ${JMEANA_BASE}/analysis_output_run3_v02/outputs_postHarvesting/HLT_iter2RegionalPtSeed10p0/Run3Winter20_QCD_Pt_170to300_14TeV.root:'Reg 10.0':2 \
 ${JMEANA_BASE}/analysis_output_run3_v02/outputs_postHarvesting/HLT_iter2GlobalPtSeed0p9/Run3Winter20_QCD_Pt_170to300_14TeV.root:'Glo 0.9':4
