### Tools for Jet/MET Analysis

Workflow to produce Jet/MET performance plots from "flat" ROOT NTuples

#### Setup

* Update global environment variables:
```
source env.sh
```

#### Prepare Analysis NTuples from batch/crab3 outputs

* Create output directory with one .root for each crab3 task:
```
hadd_ntuples.py -i [DIRS] -o [OUTDIR] # -l 0 -p _temp
```

#### Submit Analysis Jobs to Batch System (HT-Condor)

* Create scripts for submission of batch jobs:
```
batch_driver.py -i ${NTUDIR}/*root -o ${OUTDIR}/outputs -n 5000 # -l 0 -s jmeAnalysis.py
```

* Monitoring and (re)submission of batch jobs:
```
batch_monitor.py -i ${OUTDIR}
```

#### Harvesting of Outputs

* Merge outputs of batch jobs:
```
merge_batchOutputs.py -i ${OUTDIR}/analysis/*.root -o ${OUTDIR}/mergedOutputs # -l 0
```

* Harvest outputs (manipulates histograms, produces profiles, efficiencies, etc):
```
jmeAnalysisHarvester.py -i ${OUTDIR}/outputs/*.root -o ${OUTDIR}/harvesting # -l 0
```
