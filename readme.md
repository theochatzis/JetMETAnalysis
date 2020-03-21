# Tools for Jet/MET Analysis

Workflow to produce Jet/MET performance plots from "flat" ROOT NTuples

## Setup

* Update global environment variables:
```
source env.sh
```

## Prepare Analysis NTuples from crab3 outputs

* Create output directory with one .root for each crab3 task:
```
hadd_ntuples.py -i /pnfs/desy.de/cms/tier2/store/user/missirol/jme_trigger/jmeTriggerNtuples/Phase2/trackingV2/191119/* -o ${NTUDIR} # -l 0 -p _temp
```

## Batch Jobs

* Create scripts for submission of batch jobs:
```
batch_driver.py -i ${NTUDIR}/*root -o ${OUTDIR}/prod -n 5000 # -l 0 -s jmeAnalysis.py
```

* Monitoring and (re)submission of batch jobs:
```
batch_monitor.py -i ${OUTDIR}
```

## Harvesting of Outputs

* Merge outputs of batch jobs:
```
merge_batchOutputs.py -i ${OUTDIR}/prod/*.root -o ${OUTDIR}/outputs # -l 0
```

* Harvest outputs of `jmeAnalysis.py` script (produces profiles, efficiencies, etc):
```
jmeAnalysisHarvester.py -i ${OUTDIR}/outputs/*.root -o ${OUTDIR}/outputs_postHarvesting # -l 0
```

## Plots

* Produce plots from harvesting outputs:
```
jmePlots.py -h
```
