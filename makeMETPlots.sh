#!/bin/bash

NoPU="${METANA_BASE}"/ntuples/191030_inclAging1000Fix/jmeTriggerNtuple_VBF_HToInvisible_M125_14TeV_NoPU_temp.root
PU140="${METANA_BASE}"/ntuples/191030_inclAging1000Fix/jmeTriggerNtuple_VBF_HToInvisible_M125_14TeV_PU140_temp.root
PU200="${METANA_BASE}"/ntuples/191030_inclAging1000Fix/jmeTriggerNtuple_VBF_HToInvisible_M125_14TeV_PU200_temp.root

ODIR=output_191104

NEVT=-1

### ----------

if [ -d ${ODIR} ]; then

  printf "\n%s\n\n" " >> execution stopped --> target output directory already exists: ${ODIR}"
  exit 1
fi

mkdir -p ${ODIR}

"${METANA_BASE}"/metAnalysis.py -n ${NEVT} -i ${NoPU}  -o ${ODIR}/NoPU.root
"${METANA_BASE}"/metAnalysis.py -n ${NEVT} -i ${PU140} -o ${ODIR}/PU140.root
"${METANA_BASE}"/metAnalysis.py -n ${NEVT} -i ${PU200} -o ${ODIR}/PU200.root

"${METANA_BASE}"/metPlots.py \
 --NoPU ${ODIR}/NoPU.root \
 --PU140 ${ODIR}/PU140.root \
 --PU200 ${ODIR}/PU200.root \
 -o ${ODIR}/plots \
 -e png pdf root

unset -v NoPU PU140 PU200 ODIR NEVT
