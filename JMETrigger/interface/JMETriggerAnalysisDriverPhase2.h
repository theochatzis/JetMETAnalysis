#ifndef NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverPhase2_h
#define NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverPhase2_h

#include <NTupleAnalysis/JMETrigger/interface/JMETriggerAnalysisDriver.h>

class JMETriggerAnalysisDriverPhase2 : public JMETriggerAnalysisDriver {

 public:
  explicit JMETriggerAnalysisDriverPhase2(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath="", const std::string& outputFileMode="recreate");
  ~JMETriggerAnalysisDriverPhase2() {}

  void init() override;
  void analyze() override;

 protected:

  bool jetBelongsToCategory(const std::string& categLabel, const float jetPt, const float jetAbsEta) const override;
};

#endif
