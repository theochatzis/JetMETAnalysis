#!/bin/bash

OUTCFG_NAME=hlt_GRun_111X_patatrackPlusSingleIterTRK_jmeMCPaths

hltGetConfiguration /dev/CMSSW_11_1_0/GRun/V11 \
 --full \
 --mc \
 --era Run3 \
 --unprescale \
 --timing \
 --process HLT2 \
 --max-events 10 \
 --customise \
HLTrigger/Configuration/customizeHLTforPatatrack.customise_for_Patatrack_on_gpu,\
JMETriggerAnalysis/Common/customise_hltTRK_singleIteration.customise_hltTRK_singleIteration\
 --input /store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/1E007C6B-0236-774C-AE76-16FF40129ED8.root \
 --globaltag 111X_mcRun3_2021_realistic_v7 \
 --path HLTriggerFirstPath,MC_PFMET_v17,MC_CaloMET_v8,MC_AK4PFJets_v17,MC_AK4CaloJets_v9,HLTriggerFinalPath,HLTAnalyzerEndpath \
 > ${OUTCFG_NAME}_cfg.py

edmConfigDump ${OUTCFG_NAME}_cfg.py > tmp.py #${CMSSW_BASE}/src/JMETriggerAnalysis/Common/python/configs/${OUTCFG_NAME}_configDump.py

#rm ${OUTCFG_NAME}_cfg.py

unset OUTCFG_NAME
