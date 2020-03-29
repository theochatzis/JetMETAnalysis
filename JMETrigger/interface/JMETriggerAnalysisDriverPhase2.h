#ifndef NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverPhase2_h
#define NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverPhase2_h

#include <NTupleAnalysis/JMETrigger/interface/JMETriggerAnalysisDriver.h>

class JMETriggerAnalysisDriverPhase2 : public JMETriggerAnalysisDriver {

 public:
  explicit JMETriggerAnalysisDriverPhase2(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath="", const std::string& outputFileMode="recreate")
    : JMETriggerAnalysisDriver(tfile, ttree, outputFilePath, outputFileMode) {}
  ~JMETriggerAnalysisDriverPhase2() {}

 protected:

  static const std::vector<std::string> jetRegionLabels_;

  virtual bool jetBelongsToRegion(const std::string& regionLabel, const float jetAbsEta) const;
};

#endif
