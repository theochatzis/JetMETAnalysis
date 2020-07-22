#include <NTupleAnalysis/JMETrigger/interface/JMETriggerAnalysisDriverPhase2.h>
#include <NTupleAnalysis/JMETrigger/interface/Utils.h>
#include <utility>

JMETriggerAnalysisDriverPhase2::JMETriggerAnalysisDriverPhase2(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath, const std::string& outputFileMode)
  : JMETriggerAnalysisDriverPhase2(outputFilePath, outputFileMode) {
  setInputTTree(tfile, ttree);
}

JMETriggerAnalysisDriverPhase2::JMETriggerAnalysisDriverPhase2(const std::string& outputFilePath, const std::string& outputFileMode)
  : JMETriggerAnalysisDriver(outputFilePath, outputFileMode) {}

bool JMETriggerAnalysisDriverPhase2::jetBelongsToCategory(const std::string& categLabel, const float jetPt, const float jetAbsEta) const {

  bool ret(false);
  if(categLabel == "_EtaIncl"){ ret = (jetAbsEta < 5.0); }
  else if(categLabel == "_EtaInclPt0"){ ret = (jetAbsEta < 5.0) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_EtaInclPt1"){ ret = (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_EtaInclPt2"){ ret = (jetAbsEta < 5.0) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_EtaInclPt3"){ ret = (jetAbsEta < 5.0) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_EtaInclPt4"){ ret = (jetAbsEta < 5.0) and (2000. <= jetPt); }

  else if(categLabel == "_HB"){ ret = (jetAbsEta < 1.5); }
  else if(categLabel == "_HBPt0"){ ret = (jetAbsEta < 1.5) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HBPt1"){ ret = (jetAbsEta < 1.5) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HBPt2"){ ret = (jetAbsEta < 1.5) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HBPt3"){ ret = (jetAbsEta < 1.5) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HBPt4"){ ret = (jetAbsEta < 1.5) and (2000. <= jetPt); }

  else if(categLabel == "_HGCal"){ ret = (1.5 <= jetAbsEta) and (jetAbsEta < 3.0); }
  else if(categLabel == "_HGCalPt0"){ ret = (1.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HGCalPt1"){ ret = (1.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HGCalPt2"){ ret = (1.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HGCalPt3"){ ret = (1.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HGCalPt4"){ ret = (1.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (2000. <= jetPt); }

  else if(categLabel == "_HF1"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0); }
  else if(categLabel == "_HF1Pt0"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HF1Pt1"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HF1Pt2"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HF1Pt3"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HF1Pt4"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (2000. <= jetPt); }

  else if(categLabel == "_HF2"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0); }
  else if(categLabel == "_HF2Pt0"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HF2Pt1"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HF2Pt2"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HF2Pt3"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HF2Pt4"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (2000. <= jetPt); }

  return ret;
}

void JMETriggerAnalysisDriverPhase2::init(){

  jetCategoryLabels_ = {
    "_EtaIncl",
//  "_EtaInclPt0",
//  "_EtaInclPt1",
//  "_EtaInclPt2",
//  "_EtaInclPt3",
//  "_EtaInclPt4",

    "_HB",
//  "_HBPt0",
//  "_HBPt1",
//  "_HBPt2",
//  "_HBPt3",
//  "_HBPt4",

    "_HGCal",
//  "_HGCalPt0",
//  "_HGCalPt1",
//  "_HGCalPt2",
//  "_HGCalPt3",
//  "_HGCalPt4",

    "_HF1",
//  "_HF1Pt0",
//  "_HF1Pt1",
//  "_HF1Pt2",
//  "_HF1Pt3",
//  "_HF1Pt4",

    "_HF2",
//  "_HF2Pt0",
//  "_HF2Pt1",
//  "_HF2Pt2",
//  "_HF2Pt3",
//  "_HF2Pt4",
  };

  // histogram: events counter
  addTH1D("eventsProcessed", {0, 1});

  labelMap_jetAK4_.clear();
  labelMap_jetAK4_ = {
    {"ak4GenJetsNoNu", {
      {"L1TCaloCorr"     , "l1tAK4CaloJetsCorrected"},
      {"L1TPFCorr"       , "l1tAK4PFJetsCorrected"},
      {"L1TPuppiCorr"    , "l1tAK4PuppiJetsCorrected"},
      {"Calo"            , "hltAK4CaloJets"},
      {"PFCluster"       , "hltAK4PFClusterJets"},
      {"PF"              , "hltAK4PFJets"},
      {"PFCorr"          , "hltAK4PFJetsCorrected"},
      {"PFCHS"           , "hltAK4PFCHSJets"},
      {"PFCHSCorr"       , "hltAK4PFCHSJetsCorrected"},
      {"Puppi"           , "hltAK4PuppiJets"},
      {"PuppiCorr"       , "hltAK4PuppiJetsCorrected"},
      {"OfflinePuppiCorr", "offlineAK4PuppiJetsCorrected"},
    }},

    {"l1tAK4CaloJetsCorrected" , {{"GEN", "ak4GenJetsNoNu"}}},
    {"l1tAK4PFJetsCorrected"   , {{"GEN", "ak4GenJetsNoNu"}}},
    {"l1tAK4PuppiJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}, {"Offline", "offlineAK4PuppiJetsCorrected"}}},

    {"hltAK4CaloJets"          , {{"GEN", "ak4GenJetsNoNu"}}},
    {"hltAK4PFClusterJets"     , {{"GEN", "ak4GenJetsNoNu"}}},
    {"hltAK4PFJets"            , {{"GEN", "ak4GenJetsNoNu"}}},
    {"hltAK4PFJetsCorrected"   , {{"GEN", "ak4GenJetsNoNu"}}},
    {"hltAK4PFCHSJets"         , {{"GEN", "ak4GenJetsNoNu"}}},
    {"hltAK4PFCHSJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}, {"Offline", "offlineAK4PFCHSJetsCorrected"}}},
    {"hltAK4PuppiJets"         , {{"GEN", "ak4GenJetsNoNu"}}},
    {"hltAK4PuppiJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}, {"Offline", "offlineAK4PuppiJetsCorrected"}}},

    {"offlineAK4PFCHSJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}}},
    {"offlineAK4PuppiJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}}},
  };

  labelMap_jetAK8_.clear();
  labelMap_jetAK8_ = {
    {"ak8GenJetsNoNu", {
      {"Calo"            , "hltAK8CaloJets"},
      {"PFCluster"       , "hltAK8PFClusterJets"},
      {"PF"              , "hltAK8PFJets"},
      {"PFCorr"          , "hltAK8PFJetsCorrected"},
      {"PFCHS"           , "hltAK8PFCHSJets"},
      {"PFCHSCorr"       , "hltAK8PFCHSJetsCorrected"},
      {"Puppi"           , "hltAK8PuppiJets"},
      {"PuppiCorr"       , "hltAK8PuppiJetsCorrected"},
      {"OfflinePuppiCorr", "offlineAK8PuppiJetsCorrected"},
    }},

    {"hltAK8CaloJets"          , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8PFClusterJets"     , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8PFJets"            , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8PFJetsCorrected"   , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8PFCHSJets"         , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8PFCHSJetsCorrected", {{"GEN", "ak8GenJetsNoNu"}, {"Offline", "offlineAK8PFCHSJetsCorrected"}}},
    {"hltAK8PuppiJets"         , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8PuppiJetsCorrected", {{"GEN", "ak8GenJetsNoNu"}, {"Offline", "offlineAK8PuppiJetsCorrected"}}},

    {"offlineAK8PFCHSJetsCorrected", {{"GEN", "ak8GenJetsNoNu"}}},
    {"offlineAK8PuppiJetsCorrected", {{"GEN", "ak8GenJetsNoNu"}}},
  };

  labelMap_MET_.clear();
  labelMap_MET_ = {
    {"genMETCalo", {}},
    {"genMETTrue", {}},

    {"l1tCaloMET" , {{"GEN", "genMETCalo"}}},
    {"l1tPFMET"   , {{"GEN", "genMETTrue"}, {"Offline", "offlinePFMET_Raw"}}},
    {"l1tPuppiMET", {{"GEN", "genMETTrue"}, {"Offline", "offlinePuppiMET_Raw"}}},

    {"hltPFClusterMET"   , {{"GEN", "genMETCalo"}}},
    {"hltPFMETNoMu"      , {{"GEN", "genMETCalo"}}},
    {"hltPFMET"          , {{"GEN", "genMETTrue"}, {"Offline", "offlinePFMET_Raw"}}},
    {"hltPFCHSMET"       , {{"GEN", "genMETTrue"}}},
    {"hltPFSoftKillerMET", {{"GEN", "genMETTrue"}}},
    {"hltPuppiMETNoMu"   , {{"GEN", "genMETCalo"}}},
    {"hltPuppiMET"       , {{"GEN", "genMETTrue"}, {"Offline", "offlinePuppiMET_Raw"}}},

    {"offlinePFMET_Raw"     , {{"GEN", "genMETTrue"}}},
    {"offlinePFMET_Type1"   , {{"GEN", "genMETTrue"}}},
    {"offlinePuppiMET_Raw"  , {{"GEN", "genMETTrue"}}},
    {"offlinePuppiMET_Type1", {{"GEN", "genMETTrue"}}},
  };

  for(auto const& selLabel : {
    "NoSelection",
  }){
    // histograms: AK4 Jets
    for(auto const& jetLabel : labelMap_jetAK4_){
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    }

    // histograms: AK8 Jets
    for(auto const& jetLabel : labelMap_jetAK8_){
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    }

    // histograms: MET
    for(auto const& metLabel : labelMap_MET_){
      bookHistograms_MET(selLabel, metLabel.first, utils::mapKeys(metLabel.second));
    }
  }

  for(std::string const& algo : {"PF", "PFCHS", "Puppi"}){
    for(std::string const& categ : jetCategoryLabels_){
      if(algo == "PF"){
        bookHistograms_Jets("HLT_AK4"+algo+"JetCorrected"+categ+"_100", "hltAK4"+algo+"JetsCorrected", {"GEN"});
      }
      else {
        bookHistograms_Jets("HLT_AK4"+algo+"JetCorrected"+categ+"_100", "hltAK4"+algo+"JetsCorrected", {"GEN", "Offline"});
      }
    }
  }
}

void JMETriggerAnalysisDriverPhase2::analyze(){
  H1("eventsProcessed")->Fill(0.5, 1.);

  //// AK4 Jets
  const float minAK4JetPt(30.);
  const float minAK4JetPtRef(20.);
  const float maxAK4JetDeltaRmatchRef(0.1);

  for(auto const& jetLabel : labelMap_jetAK4_){
    auto jetPt1(minAK4JetPt), jetPt2(minAK4JetPtRef);
    if(jetLabel.first.find("GenJets") != std::string::npos){
      std::swap(jetPt1, jetPt2);
    }

    fillHistoDataJets fhDataAK4Jets;
    fhDataAK4Jets.jetCollection = jetLabel.first;
    fhDataAK4Jets.jetPtMin = jetPt1;
    for(auto const& jetLabelRefs : jetLabel.second){
      fhDataAK4Jets.matches.emplace_back(fillHistoDataJets::Match(jetLabelRefs.first, jetLabelRefs.second, jetPt2, maxAK4JetDeltaRmatchRef));
    }
    fillHistograms_Jets("NoSelection", fhDataAK4Jets);
  }

  //// HLT_AK4*JetCorrected*_100
  for(std::string const& algo : {"PF", "PFCHS", "Puppi"}){

    for(std::string const& categ : jetCategoryLabels_){

      auto const selLabel("HLT_AK4"+algo+"JetCorrected"+categ+"_100");

      auto const jetCollection("hltAK4"+algo+"JetsCorrected");
      auto const& vec_pt(vector<float>(jetCollection+"_pt"));
      auto const& vec_eta(vector<float>(jetCollection+"_eta"));
      bool pass(false);
      for(size_t jetIdx=0; jetIdx<vec_eta.size(); ++jetIdx){
        if((vec_pt.at(jetIdx) > 100.) and jetBelongsToCategory(categ, vec_pt.at(jetIdx), std::abs(vec_eta.at(jetIdx)))){
          pass = true;
          break;
        }
      }
      if(pass){
        fillHistoDataJets fhData;
        fhData.jetCollection = jetCollection;
        fhData.jetPtMin = minAK4JetPt;
        fhData.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPtRef, maxAK4JetDeltaRmatchRef));
        if(algo == "Puppi"){
          fhData.matches.emplace_back(fillHistoDataJets::Match("Offline", "offlineAK4PuppiJetsCorrected", minAK4JetPtRef, maxAK4JetDeltaRmatchRef));
        }
        else if(algo == "PFCHS"){
          fhData.matches.emplace_back(fillHistoDataJets::Match("Offline", "offlineAK4PFCHSJetsCorrected", minAK4JetPtRef, maxAK4JetDeltaRmatchRef));
        }
        fillHistograms_Jets(selLabel, fhData);
      }
    }
  }

  //// AK8 Jets
  const float minAK8JetPt(90.);
  const float minAK8JetPtRef(60.);
  const float maxAK8JetDeltaRmatchRef(0.1);

  for(auto const& jetLabel : labelMap_jetAK8_){
    auto jetPt1(minAK8JetPt), jetPt2(minAK8JetPtRef);
    if(jetLabel.first.find("GenJets") != std::string::npos){
      std::swap(jetPt1, jetPt2);
    }

    fillHistoDataJets fhDataAK8Jets;
    fhDataAK8Jets.jetCollection = jetLabel.first;
    fhDataAK8Jets.jetPtMin = jetPt1;
    for(auto const& jetLabelRefs : jetLabel.second){
      fhDataAK8Jets.matches.emplace_back(fillHistoDataJets::Match(jetLabelRefs.first, jetLabelRefs.second, jetPt2, maxAK8JetDeltaRmatchRef));
    }
    fillHistograms_Jets("NoSelection", fhDataAK8Jets);
  }

  //// MET
  for(auto const& metLabel : labelMap_MET_){
    fillHistoDataMET fhDataMET;
    fhDataMET.metCollection = metLabel.first;
    for(auto const& metRefs : metLabel.second){
      fhDataMET.matches.emplace_back(fillHistoDataMET::Match(metRefs.first, metRefs.second));
    }
    fillHistograms_MET("NoSelection", fhDataMET);
  }
}
