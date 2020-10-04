#ifndef NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverPhase2_h
#define NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverPhase2_h

#include <map>

#include <NTupleAnalysis/JMETrigger/interface/JMETriggerAnalysisDriver.h>

class JMETriggerAnalysisDriverPhase2 : public JMETriggerAnalysisDriver {

 public:
  explicit JMETriggerAnalysisDriverPhase2(const std::string& outputFilePath="", const std::string& outputFileMode="recreate");
  explicit JMETriggerAnalysisDriverPhase2(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath, const std::string& outputFileMode="recreate");
  ~JMETriggerAnalysisDriverPhase2() {}

  void init() override;
  void analyze() override;

 protected:
  bool jetBelongsToCategory(const std::string& categLabel, const float jetPt, const float jetAbsEta) const override;

  std::map<std::string, std::map<std::string, std::string>> labelMap_jetAK4_;
  std::map<std::string, std::map<std::string, std::string>> labelMap_jetAK8_;
  std::map<std::string, std::map<std::string, std::string>> labelMap_MET_;

  std::vector<std::string> l1tSeeds_1Jet_;
  std::vector<std::string> l1tSeeds_MET_;
};

#endif
