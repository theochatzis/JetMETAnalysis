#!/bin/bash

## -------------------------
## Setup instructions:
## -------------------------
## > scram p CMSSW CMSSW_11_2_0_Patatrack
## > cd CMSSW_11_2_0_Patatrack/src
## > eval `scram runtime -sh`
## > git clone https://github.com/missirol/JetMETAnalysis.git -o missirol -b run3_jrantuples
## > scram b -j 8
## > cd JetMETAnalysis
## > ./run_testRun3.sh test_output
## -------------------------

## -------------------------
## Hard-coded inputs/options
## -------------------------
JRANTuple_NoPU=root://cms-xrd-global.cern.ch//store/group/phys_jetmet/saparede/runIII_hlt_jec/jra_ntuples/noPU/noPU_testingJRANtuple.root
JRANTuple_PU=root://cms-xrd-global.cern.ch//store/group/phys_jetmet/saparede/runIII_hlt_jec/jra_ntuples/flatPU/flatPU_testingJRANtuple.root

ERA=Run3Winter20_V1_MC

JET_TYPES=(
#  ak4caloHLT
#  ak4pfclusterHLT
#  ak4pfHLT
#  ak4puppiHLT
  ak8caloHLT
  ak8pfclusterHLT
  ak8pfHLT
  ak8puppiHLT
)
## -------------------------

## -------------------------
## Main
## -------------------------
set -e

showHelpMsg=false
dryRun=false

# help message
usage() {
  cat <<@EOF
Usage:
  This script..

> ./run_testRun3.sh [-h] [-o output_dir] [-n maxEvents] [-p]

Options:
  -h, --help          Show this help message
  -o, --output-dir    Path to output directory          [Default: .]
  -n, --maxEvents     Max number of events to process   [Default: -1]
  -p, --parallelise   Parallelise by jet algorithm      [Default: false]
  -d, --dry-run       Enable dry-run mode               [Default: false]
@EOF
}

maxEvents=-1
paralleliseByAlgo=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) showHelpMsg=true; shift;;
    -o|--output-dir) outputDir=$2; shift; shift;;
    -n|--maxEvents) maxEvents=$2; shift; shift;;
    -p|--parallelise) paralleliseByAlgo=true; shift;;
    -d|--dry-run) dryRun=true; shift;;
    *) shift;;
  esac
done

# print help message
if [ "X${showHelpMsg}" = "Xtrue" ]; then
  usage
  exit 0
fi

INIDIR=${PWD}

if [[ ${outputDir} == "" ]]; then
  printf "%s\n" ">> ERROR -- empty path to output directory [-o]"
  exit 1
fi

if [ -d ${outputDir} ]; then
  printf "%s\n" ">> WARNING -- output directory already exists (existing files might get overwritten): ${outputDir}"
fi

stepCmd(){
  echo -e "#!/bin/bash\n\nset -e\n\n${1} 2>&1 | tee ${2}.log" > ${2}.sh
  chmod u+x ${2}.sh
  [ "X${dryRun}" = "Xtrue" ] || ./${2}.sh
  touch ${2}.done
}

runJECWorflowForOneAlgo(){
  jetType=${1}
  cd ${INIDIR}
  OUTDIR=${outputDir}/${jetType}
  mkdir -p ${OUTDIR}
  cd ${OUTDIR}

  stepN=0

  dRgen=0.2
  if [[ ${jetType} == ak8* ]]; then dRgen=0.4; fi

  ###
  ### L1FastJet
  ###
  stepNameOld=${stepName} && ((++stepN)) && stepName="step"$(printf "%02d" ${stepN})
  if [ ! -f ${stepName}.done ]; then
    CMD_STEP="jet_synchtest_x -algo1 ${jetType} -algo2 ${jetType} -sampleNoPU ${JRANTuple_NoPU} -samplePU ${JRANTuple_PU}"
    CMD_STEP+=" -ApplyJEC false"
    CMD_STEP+=" -useweight false -doNotSave true -ignoreNPV true -overwriteNPVwithNPUInTime true"
    CMD_STEP+=" -iftest true -maxEvts ${maxEvents} -outputPath ."
    stepCmd "mkdir -p plots_${stepName}\n\n${CMD_STEP}" ${stepName}
  fi

  stepNameOld=${stepName} && ((++stepN)) && stepName="step"$(printf "%02d" ${stepN})
  if [ ! -f ${stepName}.done ]; then
    CMD_STEP="jet_synchplot_x -algo1 ${jetType} -algo2 ${jetType} -fixedRange false -tdr true"
    CMD_STEP+=" -inputDir ./ -outDir plots_${stepName} -outputFormat .png"
    stepCmd "mkdir -p plots_${stepName}\n\n${CMD_STEP}" ${stepName}
  fi

  stepNameOld=${stepName} && ((++stepN)) && stepName="step"$(printf "%02d" ${stepN})
  if [ ! -f ${stepName}.done ]; then
    CMD_STEP="jet_synchfit_x -algo1 ${jetType} -algo2 ${jetType} -functionType standard -era ${ERA} -inputDir ./ -outputDir ./"
    stepCmd "mkdir -p plots_${stepName}\n\n${CMD_STEP}" ${stepName}
  fi

#  stepNameOld=${stepName} && ((++stepN)) && stepName="step"$(printf "%02d" ${stepN})
#  if [ ! -f ${stepName}.done ]; then
#    CMD_STEP="jet_synchtest_x -algo1 ${jetType} -algo2 ${jetType} -sampleNoPU ${JRANTuple_NoPU} -samplePU ${JRANTuple_PU}"
#    CMD_STEP+=" -ApplyJEC true -JECpar ./${ERA}_L1FastJet_*.txt"
#    CMD_STEP+=" -useweight false -doNotSave true -ignoreNPV true -overwriteNPVwithNPUInTime true"
#    CMD_STEP+=" -iftest true -maxEvts ${maxEvents} -outputPath plots_${stepName}"
#    stepCmd "mkdir -p plots_${stepName}\n\n${CMD_STEP}" ${stepName}
#  fi
#
#  stepNameOld=${stepName} && ((++stepN)) && stepName="step"$(printf "%02d" ${stepN})
#  if [ ! -f ${stepName}.done ]; then
#    CMD_STEP="jet_synchplot_x -algo1 ${jetType} -algo2 ${jetType} -fixedRange false -tdr true"
#    CMD_STEP+=" -inputDir plots_${stepNameOld} -outDir plots_${stepName} -outputFormat .png"
#    stepCmd "mkdir -p plots_${stepName}\n\n${CMD_STEP}" ${stepName}
#  fi

  ###
  ### L2Relative
  ### - contains both L2 and L3 JECs
  ###   (L3Absolute file will be dummy, i.e. equal to unity)
  ###
  stepNameOld=${stepName} && ((++stepN)) && stepName="step"$(printf "%02d" ${stepN})
  if [ ! -f ${stepName}.done ]; then
    CMD_STEP="jet_response_analyzer_x ${CMSSW_BASE}/src/JetMETAnalysis/JetAnalyzers/config/jra_hltRun3.config -input ${JRANTuple_PU} -algs ${jetType}:${dRgen}"
    CMD_STEP+=" -levels 1 -path ./ -era ${ERA} -output plots_${stepName}/histogram_${jetType}l1_${stepName}.root -maxEvts ${maxEvents}"
    CMD_STEP+=" -useweight false -nrefmax 50 -relrspmin 0.0 -relrspmax 5.0 -nbinsabsrsp 0 -nbinsetarsp 0 -nbinsphirsp 0 -nbinsrelrsp 200 -doflavor false"
    stepCmd "mkdir -p plots_${stepName}\n\n${CMD_STEP}" ${stepName}
  fi

  stepNameOld=${stepName} && ((++stepN)) && stepName="step"$(printf "%02d" ${stepN})
  if [ ! -f ${stepName}.done ]; then
    CMD_STEP="jet_l2_correction_x -algs ${jetType} -era ${ERA} -l2l3 true"
    CMD_STEP+=" -input plots_${stepNameOld}/histogram_${jetType}l1_${stepNameOld}.root -outputDir ./ -output l2p3.root"
    CMD_STEP+=" -makeCanvasVariable AbsCorVsJetPt:JetEta -batch true -histMet median -l2pffit standard -maxFitIter 50 -ptclipfit true"
    stepCmd "mkdir -p plots_${stepName}\n\n${CMD_STEP}" ${stepName}
  fi

  stepNameOld=${stepName} && ((++stepN)) && stepName="step"$(printf "%02d" ${stepN})
  if [ ! -f ${stepName}.done ]; then
    CMD_STEP="jet_correction_analyzer_x -ptmin 0 -inputFilename ${JRANTuple_PU} -algs ${jetType} -drmax ${dRgen} -evtmax ${maxEvents}"
    CMD_STEP+=" -useweight false -path ./ -era ${ERA} -levels 1 2 -L1FastJet true -outputDir plots_${stepName} -nbinsrelrsp 200 -relrspmin 0.0 -relrspmax 5.0 -nrefmax 50"
    stepCmd "mkdir -p plots_${stepName}\n\n${CMD_STEP}" ${stepName}
  fi

  stepNameOld=${stepName} && ((++stepN)) && stepName="step"$(printf "%02d" ${stepN})
  if [ ! -f ${stepName}.done ]; then
    CMD_STEP="jet_draw_closure_x -path plots_${stepNameOld} -filename Closure_${jetType} -histMet median -outputDir plots_${stepName}"
    CMD_STEP+=" -draw_guidelines true -doPt true -doEta true -doRatioPt false -doRatioEta false"
    stepCmd "mkdir -p plots_${stepName}\n\n${CMD_STEP}" ${stepName}
  fi

  ###
  ### Final JEC .txt files
  ### - copied in jesc/
  ###
  if [ "X${dryRun}" != "Xtrue" ]; then
    if [ ! -f ${ERA}_L1FastJet_*.txt ]; then
      printf "%s\n" ">> ERROR -- text file with L1FastJet JEC not found: ${ERA}_L1FastJet_*.txt"
    elif [ ! -f ${ERA}_L2Relative_*.txt ]; then
      printf "%s\n" ">> ERROR -- text file with L2Relative JEC not found: ${ERA}_L2Relative_*.txt"
    else
      mkdir -p jesc
      jecFile_l1=$(ls ${ERA}_L1FastJet_*.txt)
      jecFile_l2=$(ls ${ERA}_L2Relative_*.txt)
      jetTag=${jecFile_l1/${ERA}_L1FastJet_/}
      jetTag=${jetTag/.txt/}
      cp ${jecFile_l1} ${jecFile_l2} jesc
      cp ${CMSSW_BASE}/src/JetMETAnalysis/JetUtilities/data/JEC_L3Absolute_Dummy.txt jesc/${ERA}_L3Absolute_${jetTag}.txt
      cp ${CMSSW_BASE}/src/JetMETAnalysis/JetUtilities/data/JEC_L2L3Residual_Dummy.txt jesc/${ERA}_L2L3Residual_${jetTag}.txt
    fi
  fi
}

NUM_PROC=$(nproc)
for jet_type in "${JET_TYPES[@]}"; do
  if [ "X${paralleliseByAlgo}" = "Xtrue" ]; then
    while [ $(jobs -p | wc -l) -ge ${NUM_PROC} ]; do sleep 5; done
    runJECWorflowForOneAlgo ${jet_type} || true &
  else
    runJECWorflowForOneAlgo ${jet_type}
  fi
done

jobs
wait || true
