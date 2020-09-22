#!/bin/bash

set -e

OUTPUT_DIR=output_hltPhase2_200909_MB

#batch_driver.py -l 1 -i ${OUTPUT_DIR}/ntuples/*/* -o ${OUTPUT_DIR}/jobs -n 5000 -p JMETriggerAnalysisDriverPhase2
#batch_monitor.py -i ${OUTPUT_DIR}/jobs

merge_batchOutputs.py   -l 1 -i ${OUTPUT_DIR}/jobs/*/*.root    -o ${OUTPUT_DIR}/outputs
jmeAnalysisHarvester.py -l 1 -i ${OUTPUT_DIR}/outputs/*/*.root -o ${OUTPUT_DIR}/harvesting
