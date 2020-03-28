#ifndef Analysis_JMETrigger_JMETriggerAnalysisDriver_h
#define Analysis_JMETrigger_JMETriggerAnalysisDriver_h

#include "Analysis/JMETrigger/interface/AnalysisDriverBase.h"

#include <vector>
#include <memory>
#include <map>

#include <TH1D.h>
#include <TH2D.h>

class JMETriggerAnalysisDriver : public AnalysisDriverBase {

 public:
  explicit JMETriggerAnalysisDriver(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath="", const std::string& outputFileMode="recreate")
    : AnalysisDriverBase(tfile, ttree, outputFilePath, outputFileMode) {}
  ~JMETriggerAnalysisDriver() {}

  void init() override;
  void analyze() override;
  void write(TFile&) override;

  Long64_t eventsProcessed() const { return eventsProcessed_; }

 protected:
  bool hasTH1D(const std::string& key) const { return (mapTH1D_.find(key) != mapTH1D_.end()); }
  bool hasTH2D(const std::string& key) const { return (mapTH2D_.find(key) != mapTH2D_.end()); }
  void addTH1D(const std::string&, const std::vector<float>&);
  void addTH2D(const std::string&, const std::vector<float>&, const std::vector<float>&);
  std::vector<std::string> stringTokens(const std::string&, const std::string&) const;

  void bookHistograms_Jets(const std::string& dir, const std::string& jetType, const std::vector<std::string>& matchLabels={});
  void bookHistograms_MET(const std::string& dir, const std::string& jetType, const std::vector<std::string>& matchLabels={});

  Long64_t eventsProcessed_ = 0;
  std::map<std::string, std::unique_ptr<TH1D>> mapTH1D_;
  std::map<std::string, std::unique_ptr<TH2D>> mapTH2D_;

  std::vector<std::string> outputKeys_;
};

#endif
