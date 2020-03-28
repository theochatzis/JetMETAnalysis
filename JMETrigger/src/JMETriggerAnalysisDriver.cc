#include "Analysis/JMETrigger/interface/JMETriggerAnalysisDriver.h"

#include <TH1D.h>
#include <TH2D.h>

void JMETriggerAnalysisDriver::init(){
  // histogram: events counter
  addTH1D("eventsProcessed", {0, 1});

  for(auto const& selLabel : {"NoSelection"}){

    // histograms: Jets
    bookHistograms_Jets(selLabel, "ak4GenJets");
    bookHistograms_Jets(selLabel, "ak8GenJets");

    bookHistograms_Jets(selLabel, "hltAK4PFJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFJetsCorrected", {"GEN"});

    bookHistograms_Jets(selLabel, "hltAK8PFJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFJetsCorrected", {"GEN"});

    // histograms: MET
    bookHistograms_MET(selLabel, "genMETCalo");
    bookHistograms_MET(selLabel, "genMETTrue");

    bookHistograms_MET(selLabel, "hltPFMET", {"GEN", "Offline"});
    bookHistograms_MET(selLabel, "hltPFMETNoMu", {"GEN"});

    bookHistograms_MET(selLabel, "hltPuppiMET", {"GEN", "Offline"});
    bookHistograms_MET(selLabel, "hltPuppiMETNoMu", {"GEN"});
  }
}

void JMETriggerAnalysisDriver::addTH1D(const std::string& name, const std::vector<float>& binEdges){

  if(hasTH1D(name)){
    std::ostringstream oss;
    oss << "JMETriggerAnalysisDriver::addTH1D(\"" << name << "\", const std::vector<float>&) -- "
        << "TH1D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  }
  else if(hasTH2D(name)){
    std::ostringstream oss;
    oss << "JMETriggerAnalysisDriver::addTH1D(\"" << name << "\", const std::vector<float>&) -- "
        << "TH2D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  }

  if(binEdges.size() < 2){
    std::ostringstream oss;
    oss << "JMETriggerAnalysisDriver::addTH1D(\"" << name << "\", const std::vector<float>&) -- "
        << "std::vector of bin-edges has invalid size (" << binEdges.size() << " < 2)";
    throw std::runtime_error(oss.str());
  }

  mapTH1D_.insert(std::make_pair(name, std::unique_ptr<TH1D>(new TH1D(name.c_str(), name.c_str(), binEdges.size()-1, &binEdges[0]))));
  mapTH1D_.at(name)->SetDirectory(0);
  mapTH1D_.at(name)->Sumw2();

  outputKeys_.emplace_back(name);
}

void JMETriggerAnalysisDriver::addTH2D(const std::string& name, const std::vector<float>& binEdgesX, const std::vector<float>& binEdgesY){

  if(hasTH1D(name)){
    std::ostringstream oss;
    oss << "JMETriggerAnalysisDriver::addTH2D(\"" << name << "\", const std::vector<float>&, const std::vector<float>&) -- "
        << "TH1D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  }
  else if(hasTH2D(name)){
    std::ostringstream oss;
    oss << "JMETriggerAnalysisDriver::addTH2D(\"" << name << "\", const std::vector<float>&, const std::vector<float>&) -- "
        << "TH2D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  }

  if(binEdgesX.size() < 2){
    std::ostringstream oss;
    oss << "JMETriggerAnalysisDriver::addTH2D(\"" << name << "\", const std::vector<float>&) -- "
        << "std::vector of X-axis bin-edges has invalid size (" << binEdgesX.size() << " < 2)";
    throw std::runtime_error(oss.str());
  }

  if(binEdgesY.size() < 2){
    std::ostringstream oss;
    oss << "JMETriggerAnalysisDriver::addTH2D(\"" << name << "\", const std::vector<float>&) -- "
        << "std::vector of Y-axis bin-edges has invalid size (" << binEdgesY.size() << " < 2)";
    throw std::runtime_error(oss.str());
  }

  mapTH2D_.insert(std::make_pair(name, std::unique_ptr<TH2D>(new TH2D(name.c_str(), name.c_str(), binEdgesX.size()-1, &binEdgesX[0], binEdgesY.size()-1, &binEdgesY[0]))));
  mapTH2D_.at(name)->SetDirectory(0);
  mapTH2D_.at(name)->Sumw2();

  outputKeys_.emplace_back(name);
}

void JMETriggerAnalysisDriver::bookHistograms_Jets(const std::string& dir, const std::string& jetType, const std::vector<std::string>& matchLabels){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  const std::vector<std::string> regLabels({"_EtaIncl", "_HB", "_HE", "_HF"});

  std::vector<float> binEdges_njets(121);
  for(uint idx=0; idx<121; ++idx){ binEdges_njets.at(idx) = idx; }

  const std::vector<float> binEdges_pt(
    {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 400, 500, 600, 700, 800, 1000}
  );

  std::vector<float> binEdges_eta(101);
  for(uint idx=0; idx<101; ++idx){ binEdges_eta.at(idx) = -5.0+0.1*idx; }

  std::vector<float> binEdges_phi(41);
  for(uint idx=0; idx<41; ++idx){ binEdges_phi.at(idx) = M_PI*(0.05*idx - 1.); }

  const std::vector<float> binEdges_mass(
    {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 400, 500, 600}
  );

  std::vector<float> binEdges_energyFrac(21);
  for(uint idx=0; idx<21; ++idx){ binEdges_energyFrac.at(idx) = 0.05*idx; }

  std::vector<float> binEdges_dauMult1(61);
  for(uint idx=0; idx<61; ++idx){ binEdges_dauMult1.at(idx) = idx; }

  std::vector<float> binEdges_dauMult2(13);
  for(uint idx=0; idx<13; ++idx){ binEdges_dauMult2.at(idx) = idx; }

  for(auto const& regLabel : regLabels){

    addTH1D(dirPrefix+jetType+regLabel+"_njets", binEdges_njets);
    addTH1D(dirPrefix+jetType+regLabel+"_pt", binEdges_pt);
    addTH1D(dirPrefix+jetType+regLabel+"_pt0", binEdges_pt);
    addTH1D(dirPrefix+jetType+regLabel+"_eta", binEdges_eta);
    addTH1D(dirPrefix+jetType+regLabel+"_phi", binEdges_phi);
    addTH1D(dirPrefix+jetType+regLabel+"_mass", binEdges_mass);
    addTH1D(dirPrefix+jetType+regLabel+"_chargedHadronEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix+jetType+regLabel+"_neutralHadronEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix+jetType+regLabel+"_electronEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix+jetType+regLabel+"_photonEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix+jetType+regLabel+"_muonEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix+jetType+regLabel+"_chargedHadronMultiplicity", binEdges_dauMult1);
    addTH1D(dirPrefix+jetType+regLabel+"_neutralHadronMultiplicity", binEdges_dauMult1);
    addTH1D(dirPrefix+jetType+regLabel+"_electronMultiplicity", binEdges_dauMult2);
    addTH1D(dirPrefix+jetType+regLabel+"_photonMultiplicity", binEdges_dauMult1);
    addTH1D(dirPrefix+jetType+regLabel+"_muonMultiplicity", binEdges_dauMult2);

    addTH2D(dirPrefix+jetType+regLabel+"_eta__vs__pt", binEdges_eta, binEdges_pt);
  }

  if(matchLabels.empty()){
    return;
  }

  std::vector<float> binEdges_dRmatch(26);
  for(uint idx=0; idx<26; ++idx){ binEdges_dRmatch.at(idx) = 0.2*idx; }

  std::vector<float> binEdges_response(51);
  for(uint idx=0; idx<51; ++idx){ binEdges_response.at(idx) = 0.1*idx; }

  for(auto const& matchLabel : matchLabels){

    for(auto const& regLabel : regLabels){

      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_njets", binEdges_njets);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_pt", binEdges_pt);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_pt0", binEdges_pt);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_eta", binEdges_eta);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_phi", binEdges_phi);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_mass", binEdges_mass);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_chargedHadronEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_neutralHadronEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_electronEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_photonEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_muonEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_chargedHadronMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_neutralHadronMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_electronMultiplicity", binEdges_dauMult2);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_photonMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_muonMultiplicity", binEdges_dauMult2);

      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_dRmatch", binEdges_dRmatch);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_mass_over"+matchLabel, binEdges_response);
      addTH1D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_pt_over"+matchLabel, binEdges_response);

      addTH2D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_pt__vs__"+matchLabel+"_pt", binEdges_pt, binEdges_pt);
      addTH2D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_pt0__vs__"+matchLabel+"_pt", binEdges_pt, binEdges_pt);
      addTH2D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_eta__vs__"+matchLabel+"_eta", binEdges_eta, binEdges_eta);
      addTH2D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_mass_over"+matchLabel+"__vs__"+matchLabel+"_pt", binEdges_response, binEdges_pt);
      addTH2D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_mass_over"+matchLabel+"__vs__"+matchLabel+"_eta", binEdges_response, binEdges_eta);
      addTH2D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_mass_over"+matchLabel+"__vs__"+matchLabel+"_mass", binEdges_response, binEdges_mass);
      addTH2D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_pt", binEdges_response, binEdges_pt);
      addTH2D(dirPrefix+jetType+regLabel+"_MatchedTo"+matchLabel+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_eta", binEdges_response, binEdges_eta);

      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_njets", binEdges_njets);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_pt", binEdges_pt);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_pt0", binEdges_pt);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_eta", binEdges_eta);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_phi", binEdges_phi);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_mass", binEdges_mass);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_chargedHadronEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_neutralHadronEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_electronEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_photonEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_muonEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_chargedHadronMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_neutralHadronMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_electronMultiplicity", binEdges_dauMult2);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_photonMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix+jetType+regLabel+"_NotMatchedTo"+matchLabel+"_muonMultiplicity", binEdges_dauMult2);
    }
  }
}

void JMETriggerAnalysisDriver::bookHistograms_MET(const std::string& dir, const std::string& metType, const std::vector<std::string>& matchLabels){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  const std::vector<float> binEdges_pt(
    {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 400, 500, 600, 700, 800, 1000}
  );

  std::vector<float> binEdges_phi(41);
  for(uint idx=0; idx<41; ++idx){ binEdges_phi.at(idx) = M_PI*(0.05*idx - 1.); }

  const std::vector<float> binEdges_sumEt(
    {0, 30, 60, 90, 120, 180, 250, 400, 600, 800, 1000, 1500, 2000, 3000}
  );

  addTH1D(dirPrefix+metType+"_pt", binEdges_pt);
  addTH1D(dirPrefix+metType+"_phi", binEdges_phi);
  addTH1D(dirPrefix+metType+"_sumEt", binEdges_sumEt);

  if(matchLabels.empty()){
    return;
  }

  std::vector<float> binEdges_response(51);
  for(uint idx=0; idx<51; ++idx){ binEdges_response.at(idx) = 0.1*idx; }

  std::vector<float> binEdges_deltaPhi(21);
  for(uint idx=0; idx<21; ++idx){ binEdges_deltaPhi.at(idx) = M_PI*0.05*idx; }

  std::vector<float> binEdges_deltaPt(61);
  for(uint idx=0; idx<61; ++idx){ binEdges_deltaPt.at(idx) = -240+8.*idx; }

  for(auto const& matchLabel : matchLabels){

    addTH1D(dirPrefix+metType+"_pt_over"+matchLabel, binEdges_response);
    addTH1D(dirPrefix+metType+"_deltaPhi"+matchLabel, binEdges_deltaPhi);
    addTH1D(dirPrefix+metType+"_sumEt_over"+matchLabel, binEdges_response);
    addTH1D(dirPrefix+metType+"_pt_paraTo"+matchLabel, binEdges_deltaPt);
    addTH1D(dirPrefix+metType+"_pt_paraTo"+matchLabel+"Minus"+matchLabel, binEdges_deltaPt);
    addTH1D(dirPrefix+metType+"_pt_perpTo"+matchLabel, binEdges_deltaPt);

    addTH2D(dirPrefix+metType+"_pt__vs__"+matchLabel+"_pt", binEdges_pt, binEdges_pt);
    addTH2D(dirPrefix+metType+"_phi__vs__"+matchLabel+"_phi", binEdges_phi, binEdges_phi);
    addTH2D(dirPrefix+metType+"_sumEt__vs__"+matchLabel+"_sumEt", binEdges_sumEt, binEdges_sumEt);

    addTH2D(dirPrefix+metType+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_pt", binEdges_response, binEdges_pt);
    addTH2D(dirPrefix+metType+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_phi", binEdges_response, binEdges_phi);
    addTH2D(dirPrefix+metType+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_sumEt", binEdges_response, binEdges_sumEt);

    addTH2D(dirPrefix+metType+"_deltaPhi"+matchLabel+"__vs__"+matchLabel+"_pt", binEdges_deltaPhi, binEdges_pt);
    addTH2D(dirPrefix+metType+"_deltaPhi"+matchLabel+"__vs__"+matchLabel+"_phi", binEdges_deltaPhi, binEdges_phi);
    addTH2D(dirPrefix+metType+"_deltaPhi"+matchLabel+"__vs__"+matchLabel+"_sumEt", binEdges_deltaPhi, binEdges_sumEt);

    addTH2D(dirPrefix+metType+"_sumEt_over"+matchLabel+"__vs__"+matchLabel+"_pt", binEdges_response, binEdges_pt);
    addTH2D(dirPrefix+metType+"_sumEt_over"+matchLabel+"__vs__"+matchLabel+"_phi", binEdges_response, binEdges_phi);
    addTH2D(dirPrefix+metType+"_sumEt_over"+matchLabel+"__vs__"+matchLabel+"_sumEt", binEdges_response, binEdges_sumEt);

    addTH2D(dirPrefix+metType+"_pt_paraTo"+matchLabel+"__vs__"+matchLabel+"_pt", binEdges_deltaPt, binEdges_pt);
    addTH2D(dirPrefix+metType+"_pt_paraTo"+matchLabel+"__vs__"+matchLabel+"_phi", binEdges_deltaPt, binEdges_phi);
    addTH2D(dirPrefix+metType+"_pt_paraTo"+matchLabel+"__vs__"+matchLabel+"_sumEt", binEdges_deltaPt, binEdges_sumEt);

    addTH2D(dirPrefix+metType+"_pt_paraTo"+matchLabel+"Minus"+matchLabel+"__vs__"+matchLabel+"_pt", binEdges_deltaPt, binEdges_pt);
    addTH2D(dirPrefix+metType+"_pt_paraTo"+matchLabel+"Minus"+matchLabel+"__vs__"+matchLabel+"_phi", binEdges_deltaPt, binEdges_phi);
    addTH2D(dirPrefix+metType+"_pt_paraTo"+matchLabel+"Minus"+matchLabel+"__vs__"+matchLabel+"_sumEt", binEdges_deltaPt, binEdges_sumEt);

    addTH2D(dirPrefix+metType+"_pt_perpTo"+matchLabel+"__vs__"+matchLabel+"_pt", binEdges_deltaPt, binEdges_pt);
    addTH2D(dirPrefix+metType+"_pt_perpTo"+matchLabel+"__vs__"+matchLabel+"_phi", binEdges_deltaPt, binEdges_phi);
    addTH2D(dirPrefix+metType+"_pt_perpTo"+matchLabel+"__vs__"+matchLabel+"_sumEt", binEdges_deltaPt, binEdges_sumEt);
  }
}

void JMETriggerAnalysisDriver::analyze(){
 ++eventsProcessed_;
// h_eventsProcessed_->Fill(0.5, 1.);

// auto const& eta1 = this->vector<float>("hltAK4PFJetsCorrected_eta");
// for(const auto& tmp : eta1){ h_hltAK4PFJetsCorrected_eta_->Fill(tmp, 1.); }

// auto& eta2 = this->vector<float>("hltAK4PFCHSJetsCorrected_eta");
// for(const auto& tmp : eta2){ h_hltAK4PFCHSJetsCorrected_eta_->Fill(tmp, 1.); }

// auto const& eta3 = this->vector<float>("hltAK4PuppiJetsCorrected_eta");
// for(const auto& tmp : eta3){ h_hltAK4PuppiJetsCorrected_eta_->Fill(tmp, 1.); }
}

void JMETriggerAnalysisDriver::write(TFile& outFile){

  for(auto const& key : outputKeys_){

    auto keyTokens(stringTokens(key, "/"));
    if(keyTokens.empty()){ continue; }

    TDirectory* targetDir(&outFile);
    while(keyTokens.size() != 1){
      TDirectory* key = dynamic_cast<TDirectory*>(targetDir->Get(keyTokens.begin()->c_str()));
      targetDir = key ? key : targetDir->mkdir(keyTokens.begin()->c_str());
      keyTokens.erase(keyTokens.begin());
    }

    targetDir->cd();

    if(hasTH1D(key)){
      mapTH1D_.at(key)->SetName(keyTokens.begin()->c_str());
      mapTH1D_.at(key)->SetTitle(keyTokens.begin()->c_str());
      mapTH1D_.at(key)->Write();
    }
    else if(hasTH2D(key)){
      mapTH2D_.at(key)->SetName(keyTokens.begin()->c_str());
      mapTH2D_.at(key)->SetTitle(keyTokens.begin()->c_str());
      mapTH2D_.at(key)->Write();
    }
  }
}

std::vector<std::string> JMETriggerAnalysisDriver::stringTokens(const std::string& str, const std::string& delimiter) const {

  std::vector<std::string> toks; {

    std::size_t last(0), next(0);
    while((next = str.find(delimiter, last)) != std::string::npos){
      std::string substr = str.substr(last, next-last);
      if(substr != "") toks.push_back(substr);
      last = next + delimiter.size();
    }

    if(str.substr(last) != ""){
      toks.push_back(str.substr(last));
    }
  }

  return toks;
}
