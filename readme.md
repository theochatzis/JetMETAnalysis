# Tools for Jet/MET Analysis

Workflow to produce Jet/MET performance plots from "flat" ROOT NTuples

## Setup

* Update global environment variables:
```
source env.sh
```

## Batch Jobs

* Create scripts for submission of batch jobs:
```
batch_driver.py -s jmeAnalysis.py -i ${NTUDIR}/*root -o ${OUTDIR}/prod -n 5000
```

* Monitoring and (re)submission of batch jobs:
```
batch_monitor.py -i ${OUTDIR}
```

## Harvesting of Outputs

* Merge outputs of batch jobs:
```
merge_batchOutputs.py -i ${OUTDIR}/prod/*.root -o ${OUTDIR}/outputs
```

* Harvest outputs of `jmeAnalysis.py` script (produces profiles, efficiencies, etc):
```
jmeAnalysisHarvester.py -i ${OUTDIR}/outputs/*.root -o ${OUTDIR}/outputs_postHarvesting
```
