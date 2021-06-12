Quick set of instructions for HLT-rate estimates on 2018 pp data.

Ref: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SteamHLTRatesCalculation

```
cd rates/

# test locally
cmsRun hltResults_cfg.py maxEvents=500 reco=HLT_Run3TRK output=tmp.root

# create area(s) with batch-job submission
./makeEDMFiles_hltTriggerResults_210611.sh tmpout

# submit jobs to the batch system
bmonitor -i tmpout -r
```
