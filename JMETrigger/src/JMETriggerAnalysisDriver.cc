#include "Analysis/JMETrigger/interface/JMETriggerAnalysisDriver.h"

#include <TH1D.h>
#include <TH2D.h>

void JMETriggerAnalysisDriver::init(){

  h_eventsProcessed_.reset(new TH1D("eventsProcessed", "eventsProcessed", 1, 0, 1));
  h_eventsProcessed_->SetDirectory(0);
  h_eventsProcessed_->Sumw2();

  h_hltAK4PFJetsCorrected_eta_.reset(new TH1D("hltAK4PFJetsCorrected_eta", "hltAK4PFJetsCorrected_eta", 120, -5, 5));
  h_hltAK4PFJetsCorrected_eta_->SetDirectory(0);
  h_hltAK4PFJetsCorrected_eta_->Sumw2();

  h_hltAK4PFCHSJetsCorrected_eta_.reset(new TH1D("hltAK4PFCHSJetsCorrected_eta", "hltAK4PFCHSJetsCorrected_eta", 120, -5, 5));
  h_hltAK4PFCHSJetsCorrected_eta_->SetDirectory(0);
  h_hltAK4PFCHSJetsCorrected_eta_->Sumw2();

  h_hltAK4PuppiJetsCorrected_eta_.reset(new TH1D("hltAK4PuppiJetsCorrected_eta", "hltAK4PuppiJetsCorrected_eta", 120, -5, 5));
  h_hltAK4PuppiJetsCorrected_eta_->SetDirectory(0);
  h_hltAK4PuppiJetsCorrected_eta_->Sumw2();
}

void JMETriggerAnalysisDriver::analyze(){
  ++eventsProcessed_;
  h_eventsProcessed_->Fill(0.5, 1.);

  auto const& eta1 = this->vector<float>("hltAK4PFJetsCorrected_eta");
  for(const auto& tmp : eta1){ h_hltAK4PFJetsCorrected_eta_->Fill(tmp, 1.); }

//  auto& eta2 = this->vector<float>("hltAK4PFCHSJetsCorrected_eta");
//  for(const auto& tmp : eta2){ h_hltAK4PFCHSJetsCorrected_eta_->Fill(tmp, 1.); }

//  auto const& eta3 = this->vector<float>("hltAK4PuppiJetsCorrected_eta");
//  for(const auto& tmp : eta3){ h_hltAK4PuppiJetsCorrected_eta_->Fill(tmp, 1.); }
}

void JMETriggerAnalysisDriver::write(){

  h_eventsProcessed_->Write();
  h_hltAK4PFJetsCorrected_eta_->Write();
  h_hltAK4PFCHSJetsCorrected_eta_->Write();
  h_hltAK4PuppiJetsCorrected_eta_->Write();
}
