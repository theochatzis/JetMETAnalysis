#include <NTupleAnalysis/JMETrigger/interface/JMETriggerAnalysisDriverPhase2.h>

const std::vector<std::string> JMETriggerAnalysisDriverPhase2::jetRegionLabels_ = {"_EtaIncl", "_HB", "_HGCal", "_HF1", "_HF2"};

bool JMETriggerAnalysisDriverPhase2::jetBelongsToRegion(const std::string& regionLabel, const float jetAbsEta) const {

  bool ret(false);
  if(regionLabel == "_EtaIncl"){ ret = (jetAbsEta < 5.0); }
  else if(regionLabel == "_HB"){ ret = (jetAbsEta < 1.5); }
  else if(regionLabel == "_HGCal"){ ret = (1.5 <= jetAbsEta) and (jetAbsEta < 3.0); }
  else if(regionLabel == "_HF1"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0); }
  else if(regionLabel == "_HF2"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0); }

  return ret;
}
