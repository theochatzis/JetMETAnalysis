#!/bin/bash

set -e

#batch_driver.py -l 1 -i output_hltPhase2_200702_v01/ntuples/*/* -o output_hltPhase2_200702_v01/jobs -n 5000 -p JMETriggerAnalysisDriverPhase2
batch_monitor.py -i output_hltPhase2_200702_v01/jobs

merge_batchOutputs.py   -l 1 -i output_hltPhase2_200702_v01/jobs/*/*.root    -o output_hltPhase2_200702_v01/outputs
jmeAnalysisHarvester.py -l 1 -i output_hltPhase2_200702_v01/outputs/*/*.root -o output_hltPhase2_200702_v01/harvesting
