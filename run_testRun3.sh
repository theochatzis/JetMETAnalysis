#!/bin/bash

JRANTuple_NoPU=root://cms-xrd-global.cern.ch//store/group/phys_jetmet/saparede/runIII_hlt_jec/jra_ntuples/noPU/noPU_testingJRANtuple.root
JRANTuple_PU=root://cms-xrd-global.cern.ch//store/group/phys_jetmet/saparede/runIII_hlt_jec/jra_ntuples/flatPU/flatPU_testingJRANtuple.root

ERA=ERA #Run3Winter20_MC_V1

JET_TYPES=(
  ak4pfHLT
)

set -e

for jet_type in ${JET_TYPES[@]}; do
  OUTDIR=tmpout1/${jet_type}
  mkdir -p ${OUTDIR}/jraNTuples
  cd ${OUTDIR}
  unset OUTDIR

  ###
  ### L1
  ###
#  if [ ! -f step01.done ]; then
#    CMD_STEP01="jet_synchtest_x -outputPath ./ -algo1 ${jet_type} -algo2 ${jet_type} -sampleNoPU ${JRANTuple_NoPU} -samplePU ${JRANTuple_PU}"
#    CMD_STEP01+=" -ApplyJEC false -useweight false -iftest true -maxEvts 1000000 -doNotSave true -ignoreNPV true -overwriteNPVwithNPUInTime true"
#    echo "${CMD_STEP01} 2>&1 | tee step01.log" > step01.sh && source step01.sh && touch step01.done
#  fi
#
#  if [ ! -f step02.done ]; then
#    CMD_STEP02="mkdir -p plots_step02 &&"
#    CMD_STEP02+=" jet_synchplot_x -algo1 ${jet_type} -algo2 ${jet_type} -fixedRange false -tdr true"
#    CMD_STEP02+=" -inputDir ./ -outDir ./plots_step02 -outputFormat .png"
#    echo "${CMD_STEP02} 2>&1 | tee step02.log" > step02.sh && source step02.sh && touch step02.done
#  fi
#
#  if [ ! -f step03.done ]; then
#    CMD_STEP03="jet_synchfit_x -algo1 ${jet_type} -algo2 ${jet_type} -functionType standard -era ${ERA} -inputDir ./ -outputDir ./"
#    echo "${CMD_STEP03} 2>&1 | tee step03.log" > step03.sh && source step03.sh && touch step03.done
#  fi

  if [ ! -f step04.done ]; then
    CMD_STEP04="mkdir -p plots_step04 &&"
    CMD_STEP04+=" jet_synchtest_x -algo1 ${jet_type} -algo2 ${jet_type} -sampleNoPU ${JRANTuple_NoPU} -samplePU ${JRANTuple_PU}"
    CMD_STEP04+=" -ApplyJEC true -JECpar ${ERA}_L1FastJet_*.txt -outputPath plots_step04"
    CMD_STEP04+=" -useweight false -iftest true -maxEvts 1e6 -doNotSave true -ignoreNPV true -overwriteNPVwithNPUInTime true"
    echo "${CMD_STEP04} 2>&1 | tee step04.log" > step04.sh && source step04.sh && touch step04.done
  fi

#  if [ ! -f step05.done ]; then
#    CMD_STEP05="mkdir -p plots_step05 &&"
#    CMD_STEP05+=" jet_synchplot_x -algo1 ${jet_type} -algo2 ${jet_type} -inputDir ./ -outputFormat .png"
#    CMD_STEP05+=" -fixedRange false -tdr true -outDir ./plots_step05 2>&1 | tee step05.log"
#    echo "${CMD_STEP05} 2>&1 | tee step05.log" > step05.sh && source step05.sh && touch step05.done
#  fi
#
#  if [ ! -f step06.done ]; then
#    CMD_STEP06="jet_apply_jec_x -algs ${jet_type} -input ${JRANTUPLE_DIR}/${JRANTUPLE_PU}"
#    CMD_STEP06+=" -output jraNTuples/PU_jec.root -era ${ERA} -levels 1 -jecpath ./ -L1FastJet true"
#    echo "${CMD_STEP06} 2>&1 | tee step06.log" > step06.sh && source step06.sh && touch step06.done
#  fi

  ###
  ### L2+L3
  ###
  continue

  if [ ! -f step07.done ]; then
    echo "jet_response_analyzer_x ${CMSSW_BASE}/src/JetMETAnalysis/JetAnalyzers/config/jra_hltRun3.config -input jraNTuples/PU_jec.root -algs ${jet_type}l1:0.2 -nbinsabsrsp 0 -nbinsetarsp 0 -nbinsphirsp 0 -nbinsrelrsp 200 -doflavor false -output histogram_${jet_type}l1_step07.root -useweight false -nrefmax 50 -relrspmin 0.0 -relrspmax 5.0"
    echo "${CMD_STEP07} 2>&1 | tee step07.log" > step07.sh && source step07.sh && touch step07.done
  fi

  if [ ! -f step08.done ]; then
    echo "jet_l2_correction_x -input histogram_${jet_type}l1_step07.root -algs ${jet_type}l1 -era ${ERA} -output l2p3.root -outputDir ./ -makeCanvasVariable AbsCorVsJetPt:JetEta -l2l3 true -batch true -histMet median -l2pffit Standard+Gaussian -maxFitIter 30 -ptclipfit false"
    echo "${CMD_STEP08} 2>&1 | tee step08.log" > step08.sh && source step08.sh && touch step08.done
  fi

  if [ ! -f step09.done ]; then
    echo "mkdir -p plots_step09 && jet_correction_analyzer_x -evtmax 0  -ptmin 30 -inputFilename jraNTuples/PU_jec.root -algs ${jet_type}l1 -drmax 0.2 -L1FastJet false -useweight false -path ./ -era ${ERA} -levels 2 -outputDir ./plots_step09 -nbinsrelrsp 200 -relrspmin 0.0 -relrspmax 5.0 -nrefmax 50"
    echo "${CMD_STEP09} 2>&1 | tee step09.log" > step09.sh && source step09.sh && touch step09.done
  fi

  if [ ! -f step10.done ]; then
    echo "jet_draw_closure_x -path plots_step09 -filename Closure_${jet_type}l1 -histMet median -outputDir plots_step10 -draw_guidelines true -doPt true -doEta true -doRatioPt false -doRatioEta false 2>&1 | tee step10.log"
    echo "${CMD_STEP10} 2>&1 | tee step10.log" > step10.sh && source step10.sh && touch step10.done
  fi

done
