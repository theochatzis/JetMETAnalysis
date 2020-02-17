#ifndef Analysis_JMETrigger_JMETriggerAnalysisDriver_h
#define Analysis_JMETrigger_JMETriggerAnalysisDriver_h

#include "Analysis/JMETrigger/interface/AnalysisDriverBase.h"

#include <memory>

#include <TH1D.h>
#include <TH2D.h>

class JMETriggerAnalysisDriver : public AnalysisDriverBase {

 public:
  explicit JMETriggerAnalysisDriver(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath="", const std::string& outputFileMode="recreate")
    : AnalysisDriverBase(tfile, ttree, outputFilePath, outputFileMode) {}
  ~JMETriggerAnalysisDriver() {}

  void init() override;
  void analyze() override;
  void write() override;

  Long64_t eventsProcessed() const { return eventsProcessed_; }

 protected:
  Long64_t eventsProcessed_ = 0;
  std::unique_ptr<TH1D> h_eventsProcessed_;
  std::unique_ptr<TH1D> h_hltAK4PFJetsCorrected_eta_;
  std::unique_ptr<TH1D> h_hltAK4PFCHSJetsCorrected_eta_;
  std::unique_ptr<TH1D> h_hltAK4PuppiJetsCorrected_eta_;
};

#endif
