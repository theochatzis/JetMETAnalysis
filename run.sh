#!/bin/bash

NoPU=/home/missirol/Desktop/VBF_HToInvisible_M125_14TeV_NoPU_temp.root
PU140=/home/missirol/Desktop/VBF_HToInvisible_M125_14TeV_PU140_temp.root
PU200=/home/missirol/Desktop/VBF_HToInvisible_M125_14TeV_PU200_temp.root

ODIR=tmptmp

### ----------

#if [ -d ${ODIR} ]; then exit 1; fi;

mkdir -p ${ODIR}

#./metAnalysis.py -i ${NoPU} -o ${ODIR}/NoPU.root
#./metAnalysis.py -i ${PU140} -o ${ODIR}/PU140.root
#./metAnalysis.py -i ${PU200} -o ${ODIR}/PU200.root

./metPlots.py \
 --NoPU ${ODIR}/NoPU.root \
 --PU140 ${ODIR}/PU140.root \
 --PU200 ${ODIR}/PU200.root \
 -o ${ODIR}/plots \
 -e png pdf root

unset -v ODIR
