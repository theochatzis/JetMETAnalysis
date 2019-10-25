#!/bin/bash

NoPU=
PU140=
PU200=

ODIR=

### ----------

mkdir -p ${ODIR}

./metAnalisis.py -i ${NoPU} -o ${ODIR}/NoPU.root
./metAnalisis.py -i ${PU140} -o ${ODIR}/PU140.root
./metAnalisis.py -i ${PU200} -o ${ODIR}/PU200.root

./metPlots.py \
 --NoPU ${ODIR}/NoPU.root \
 --PU140 ${ODIR}/PU140.root \
 --PU200 ${ODIR}/PU200.root \
 -o ${ODIR}/plots

unset -v ODIR
