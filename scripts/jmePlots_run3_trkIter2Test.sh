#!/bin/bash

set -e

inpdir=${JMEANA_BASE}/analysis_output_run3_v03/outputs_postHarvesting
outdir=run3_trkIter2Test

samples=(
 QCD_Pt_15to3000_Flat
 QCD_Pt_50to80
 QCD_Pt_170to300
)

if [ ! -f ${outdir%%/*}.tar.gz ]; then

  for sample in "${samples[@]}"; do

    outd_i=${outdir}/${sample}

    jmePlots_run3.py -o ${outd_i} -l ${sample} -e pdf png root -i \
     ${inpdir}/HLT/Run3Winter20_${sample}_14TeV.root:'Reg 0.4':1 \
     ${inpdir}/HLT_trkIter2RegionalPtSeed0p9/Run3Winter20_${sample}_14TeV.root:'Reg 0.9':920 \
     ${inpdir}/HLT_trkIter2RegionalPtSeed2p0/Run3Winter20_${sample}_14TeV.root:'Reg 2.0':800 \
     ${inpdir}/HLT_trkIter2RegionalPtSeed5p0/Run3Winter20_${sample}_14TeV.root:'Reg 5.0':880 \
     ${inpdir}/HLT_trkIter2RegionalPtSeed10p0/Run3Winter20_${sample}_14TeV.root:'Reg 10.0':2 \
     ${inpdir}/HLT_trkIter2GlobalPtSeed0p9/Run3Winter20_${sample}_14TeV.root:'Glo 0.9':4

    unset -v outd_i
  done
  unset -v sample

  tar cfz ${outdir%%/*}.tar.gz ${outdir%%/*}
  rm -rf ${outdir%%/*}
fi

unset -v inpdir outdir samples
