#!/bin/bash

NoPU=/home/missirol/Desktop/JMETriggerNTuples/191030_inclAging1000Fix/jmeTriggerNtuple_VBF_HToInvisible_M125_14TeV_NoPU_temp.root
PU140=/home/missirol/Desktop/JMETriggerNTuples/191030_inclAging1000Fix/jmeTriggerNtuple_VBF_HToInvisible_M125_14TeV_PU140_temp.root
PU200=/home/missirol/Desktop/JMETriggerNTuples/191030_inclAging1000Fix/jmeTriggerNtuple_VBF_HToInvisible_M125_14TeV_PU200_temp.root

ODIR=output_191030

### ----------

if [ -d ${ODIR} ]; then

  printf "\n%s\n\n" " >> execution stopped --> target output directory already exists: ${ODIR}"
  exit 1
fi

mkdir -p ${ODIR}

./metAnalysis.py -n -1 -i ${NoPU}  -o ${ODIR}/NoPU.root
./metAnalysis.py -n -1 -i ${PU140} -o ${ODIR}/PU140.root
./metAnalysis.py -n -1 -i ${PU200} -o ${ODIR}/PU200.root

./metPlots.py \
 --NoPU ${ODIR}/NoPU.root \
 --PU140 ${ODIR}/PU140.root \
 --PU200 ${ODIR}/PU200.root \
 -o ${ODIR}/plots \
 -e png pdf root

unset -v NoPU PU140 PU200 ODIR
