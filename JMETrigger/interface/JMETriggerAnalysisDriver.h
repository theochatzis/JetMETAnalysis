#ifndef NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriver_h
#define NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriver_h

#include <vector>

#include <NTupleAnalysis/JMETrigger/interface/AnalysisDriverBase.h>

class JMETriggerAnalysisDriver : public AnalysisDriverBase {

 public:
  explicit JMETriggerAnalysisDriver(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath="", const std::string& outputFileMode="recreate")
    : AnalysisDriverBase(tfile, ttree, outputFilePath, outputFileMode) {}
  ~JMETriggerAnalysisDriver() {}

  void init() override;
  void analyze() override;

 protected:

  static const std::vector<std::string> jetRegionLabels_;
  virtual bool jetBelongsToRegion(const std::string& regionLabel, const float jetAbsEta) const;

  class fillHistoDataJets {
   public:
    std::string jetCollection = "";
    float jetPtMin = -1.;

    struct Match {
      Match(const std::string& theLabel, const std::string& theJetCollection, const float theJetPtMin, const float theJetDeltaRMin)
        : label(theLabel), jetCollection(theJetCollection), jetPtMin(theJetPtMin), jetDeltaRMin(theJetDeltaRMin) {}
      std::string label;
      std::string jetCollection;
      float jetPtMin;
      float jetDeltaRMin;
    };
    std::vector<Match> matches;
  };

  class fillHistoDataMET {
   public:
    std::string metCollection = "";

    struct Match {
      Match(const std::string& theLabel, const std::string& theMETCollection)
      : label(theLabel), metCollection(theMETCollection) {}
      std::string label;
      std::string metCollection;
    };
    std::vector<Match> matches;
  };

  void fillHistograms_Jets(const std::string& dir, const fillHistoDataJets& fhDataJets);
  void fillHistograms_MET(const std::string& dir, const fillHistoDataMET& fhDataMET);

  void bookHistograms_Jets(const std::string& dir, const std::string& jetType, const std::vector<std::string>& matchLabels={});
  void bookHistograms_MET(const std::string& dir, const std::string& jetType, const std::vector<std::string>& matchLabels={});
};

#endif
