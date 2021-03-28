#!/bin/bash

OUTDIR=tmpout1

JETTYPE=ak4pfHLT

set -e

if [ ! -d ${OUTDIR} ]; then
  mkdir -p ${OUTDIR}/jraNTuples
  ln -sf ${CMSSW_BASE}/src/JetMETAnalysis/jraNTuples_run3_1120_GRun/NoPU.root ${OUTDIR}/jraNTuples/NoPU.root
  ln -sf ${CMSSW_BASE}/src/JetMETAnalysis/jraNTuples_run3_1120_GRun/PU.root ${OUTDIR}/jraNTuples/PU.root
fi

cd ${OUTDIR}
unset OUTDIR

## pre-processing
#if [ ! -f step0.sh ]; then
#  JRA_NoPU=${CMSSW_BASE}/src/JetMETAnalysis/jraNTuples_run3_1120_GRun/NoPU.root
#  JRA_PU=${CMSSW_BASE}/src/JetMETAnalysis/jraNTuples_run3_1120_GRun/PU.root
#  echo "mkdir -p jraNTuples && \\
#${CMSSW_BASE}/src/JetMETAnalysis/JetAnalyzers/scripts/renameJRADirs.py -v 2 -i ${JRA_NoPU} -o jraNTuples/NoPU.root && \\
#${CMSSW_BASE}/src/JetMETAnalysis/JetAnalyzers/scripts/renameJRADirs.py -v 2 -i ${JRA_PU} -o jraNTuples/PU.root  2>&1 | tee step0.log" > step0.sh
#  unset JRA_NoPU JRA_PU
#  source step0.sh
#fi

## L1
if [ ! -f step1.done ]; then
  echo "jet_synchtest_x -algo1 ${JETTYPE} -algo2 ${JETTYPE} -basepath jraNTuples -sampleNoPU NoPU.root -samplePU PU.root -ApplyJEC false -useweight false -iftest false -maxEvts 1000 -doNotSave true -ignoreNPV true -overwriteNPVwithNPU true 2>&1 | tee step1.log" > step1.sh
  source step1.sh
  touch step1.done
fi

#if [ ! -f step2.done ]; then
#  echo "mkdir -p plots_step2 && jet_synchplot_x -algo1 ${JETTYPE} -algo2 ${JETTYPE} -inputDir ./ -outputFormat .png -fixedRange false -tdr true -outDir ./plots_step2 2>&1 | tee step2.log" > step2.sh
#  source step2.sh
#  touch step2.done
#fi

#if [ ! -f step3.done ]; then
#  echo "jet_synchfit_x  -algo1 ${JETTYPE} -algo2 ${JETTYPE} -era ERA 2>&1 | tee step3.log" > step3.sh
#  source step3.sh && touch step3.done
#fi
#
#if [ ! -f step4.done ]; then
#  echo "mkdir -p plots_step4 && jet_synchplot_x -algo1 ${JETTYPE} -algo2 ${JETTYPE} -inputDir ./ -outputFormat .png -fixedRange false -tdr true -outDir ./plots_step4 2>&1 | tee step4.log" > step4.sh
#  source step4.sh && touch step4.done
#fi
#
#if [ ! -f step5.done ]; then
#  echo "jet_apply_jec_x -algs ${JETTYPE} -input jraNTuples/PU.root -era ERA -levels 1 -jecpath ./ -L1FastJet true 2>&1 | tee step5.log" > step5.sh
#  source step5.sh && touch step5.done
#fi

### L2+L3
#if [ ! -f step6.done ]; then
#  echo "jet_response_analyzer_x ${CMSSW_BASE}/src/JetMETAnalysis/JetAnalyzers/config/jra_hltRun3.config -input jraNTuples/PU_jec.root -algs ${JETTYPE}l1:0.2 -nbinsabsrsp 0 -nbinsetarsp 0 -nbinsphirsp 0 -nbinsrelrsp 200 -doflavor false -output histogram_${JETTYPE}l1_step6.root -useweight false -nrefmax 20 -relrspmin 0.0 -relrspmax 5.0 2>&1 | tee step6.log" > step6.sh
#  source step6.sh && touch step6.done
#fi
#
#if [ ! -f step7.done ]; then
#  echo "jet_l2_correction_x -input histogram_${JETTYPE}l1_step6.root -algs ${JETTYPE}l1 -era ERA -output l2p3.root -outputDir ./ -makeCanvasVariable AbsCorVsJetPt:JetEta -l2l3 true -batch true -histMet median -l2pffit Standard+Gaussian -maxFitIter 30 -ptclipfit false 2>&1 | tee step7.log" > step7.sh
#  source step7.sh && touch step7.done
#fi
#
#if [ ! -f step8.done ]; then
#  echo "mkdir -p plots_step8 && jet_correction_analyzer_x -evtmax 0  -ptmin 30 -inputFilename jraNTuples/PU_jec.root -algs ${JETTYPE}l1 -drmax 0.2 -L1FastJet false -useweight false -path ./ -era ERA -levels 2 -outputDir ./plots_step8 -nbinsrelrsp 200 -relrspmin 0.0 -relrspmax 5.0 -nrefmax 20 2>&1 | tee step8.log" > step8.sh
#  source step8.sh && touch step8.done
#fi
#
#if [ ! -f step9.done ]; then
#  echo "jet_draw_closure_x -path plots_step8 -filename Closure_${JETTYPE}l1 -histMet median -outputDir plots_step9 -draw_guidelines true -doPt true -doEta true -doRatioPt false -doRatioEta false 2>&1 | tee step9.log" > step9.sh
#  source step9.sh && touch step9.done
#fi
