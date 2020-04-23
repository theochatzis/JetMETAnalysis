#!/bin/bash

set -e

if [ ! -d ${JMEANA_BASE} ]; then
  exit 1
fi

inpdir=${JMEANA_BASE}/output_200423_v01/harvesting
outdir=plots_hltPhase2_200423_v01

samples=(
  Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_NoPU
  Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200
  Phase2HLTTDR_VBF_HToInvisible_14TeV_NoPU
  Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200
)

outdirbase=${outdir%%/*}

if [ ! -f ${outdirbase}.tar.gz ] && [ ! -d ${outdirbase} ]; then

  for sample in "${samples[@]}"; do

    outd_i=${outdir}/run2_vs_iter0withPatatrack/${sample}

    opts_i=""
    if   [[ ${sample} == *"QCD_"* ]]; then opts_i="-k '*Jets*' '*MET_pt'"
    elif [[ ${sample} == *"HToInv"* ]]; then opts_i="-k '*MET_*'"
    elif [[ ${sample} == *"DYToLL"* ]]; then opts_i="-k '*MET_*'"
    elif [[ ${sample} == *"ZprimeToMuMu"* ]]; then opts_i="-k '*METNoMu_*'"
    fi

    dqmPlots_compareFiles.py -o ${outd_i}/dqm -l ${sample} -e pdf root -i \
      ${inpdir}/ntuples/HLT_TRKv06/${sample}.root:'TRKv06':1:1:20 \
      ${inpdir}/ntuples/HLT_TRKv06_TICL/${sample}.root:'TRKv06 + TICL':2:1:24

    if [ ${sample} == "Run3Winter20_QCD_Pt_15to3000_Flat_14TeV" ]; then
      dqmPlots_compareObjs.py -o ${outdir}/run2/${sample}/dqm_compareObjs -l ${sample} -e pdf root -i \
        ${inpdir}/ntuples/HLT_TRKv06/${sample}.root:'':1:1:20

      dqmPlots_compareFilesAndObjs.py -o ${outd_i}/dqm_compareObjs -l ${sample} -e pdf root -i \
        ${inpdir}/ntuples/HLT_TRKv06/${sample}.root:'TRKv06':1:1:20 \
        ${inpdir}/ntuples/HLT_TRKv06_TICL/${sample}.root:'TRKv06 + TICL':2:2:24
    fi

    jmePlots_compareFiles.py -u ${opts_i} -o ${outd_i}/jme -l ${sample} -e pdf root -i \
      ${inpdir}/harvesting/HLT_TRKv06/${sample}.root:'TRKv06':1:1:20 \
      ${inpdir}/harvesting/HLT_TRKv06_TICL/${sample}.root:'TRKv06 + TICL':2:1:24

    jmePlots_compareObjs.py -u ${opts_i} -o ${outdir}/run2/${sample}/jme_compareObjs -l ${sample} -e pdf root -i \
      ${inpdir}/harvesting/HLT_TRKv06/${sample}.root:'':1:1:20

    jmePlots_compareFilesAndObjs.py -u ${opts_i} -o ${outd_i}/jme_compareObjs -l ${sample} -e pdf root -i \
      ${inpdir}/harvesting/HLT_TRKv06/${sample}.root:'TRKv06':1:1:20 \
      ${inpdir}/harvesting/HLT_TRKv06_TICL/${sample}.root:'TRKv06 + TICL':2:2:24

    unset -v outd_i opts_i
  done
  unset -v sample

  if [ -d ${outdirbase} ]; then
    tar cfz ${outdirbase}.tar.gz ${outdirbase}
    rm -rf ${outdirbase}
  fi
fi

unset -v inpdir outdir samples outdirbase
