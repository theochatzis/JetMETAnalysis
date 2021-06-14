#!/usr/bin/env python
import json
from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_Data_NoOutput_configDump import cms, process

triggersForPureRate = []
for streamName in process.streams.parameterNames_():
  if streamName.startswith('Physics'):
    for dsetName in getattr(process.streams, streamName):
      for trigName in getattr(process.datasets, dsetName):
        if trigName.startswith('HLT_'):
          triggersForPureRate.append(trigName)
triggersForPureRate = list(set(triggersForPureRate))
json.dump(sorted(triggersForPureRate), open('triggersForPureRate.json', 'w'), sort_keys=True, indent=2)
