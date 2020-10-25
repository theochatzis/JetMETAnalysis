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

  else if(categLabel == "_Eta2p4"){ ret = (jetAbsEta < 2.4); }
  else if(categLabel == "_Eta2p4Pt0"){ ret = (jetAbsEta < 2.4) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_Eta2p4Pt1"){ ret = (jetAbsEta < 2.4) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_Eta2p4Pt2"){ ret = (jetAbsEta < 2.4) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_Eta2p4Pt3"){ ret = (jetAbsEta < 2.4) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_Eta2p4Pt4"){ ret = (jetAbsEta < 2.4) and (2000. <= jetPt); }

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

  else if(categLabel == "_HF"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0); }
  else if(categLabel == "_HFPt0"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HFPt1"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HFPt2"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HFPt3"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HFPt4"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (2000. <= jetPt); }

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

    "_Eta2p4",
//  "_Eta2p4Pt0",
//  "_Eta2p4Pt1",
//  "_Eta2p4Pt2",
//  "_Eta2p4Pt3",
//  "_Eta2p4Pt4",

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

    "_HF",
//  "_HFPt0",
//  "_HFPt1",
//  "_HFPt2",
//  "_HFPt3",
//  "_HFPt4",

//  "_HF1",
//  "_HF1Pt0",
//  "_HF1Pt1",
//  "_HF1Pt2",
//  "_HF1Pt3",
//  "_HF1Pt4",

//  "_HF2",
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
      {"l1tCaloCorr"    , "l1tAK4CaloJetsCorrected"},
      {"l1tPFCorr"      , "l1tAK4PFJetsCorrected"},
      {"l1tPFPuppiCorr2", "l1tAK4PFPuppiJetsCorrected"},
      {"l1tPFPuppiCorr" , "l1tSlwPFPuppiJetsCorrected"},
//    {"hltCalo"        , "hltAK4CaloJets"},
//    {"hltPFCluster"   , "hltAK4PFClusterJets"},
//    {"hltPF"          , "hltAK4PFJets"},
      {"hltPFCorr"      , "hltAK4PFJetsCorrected"},
//    {"hltPFCHS"       , "hltAK4PFCHSJets"},
      {"hltPFCHSCorr"   , "hltAK4PFCHSJetsCorrected"},
      {"hltPFPuppi"     , "hltAK4PFPuppiJets"},
      {"hltPFPuppiCorr" , "hltAK4PFPuppiJetsCorrected"},
      {"offlPFPuppiCorr", "offlineAK4PFPuppiJetsCorrected"},
    }},

    {"l1tAK4CaloJetsCorrected"   , {{"GEN", "ak4GenJetsNoNu"}}},
    {"l1tAK4PFJetsCorrected"     , {{"GEN", "ak4GenJetsNoNu"}}},
    {"l1tAK4PFPuppiJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}, {"Offline", "offlineAK4PFPuppiJetsCorrected"}}},
    {"l1tSlwPFPuppiJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}, {"Offline", "offlineAK4PFPuppiJetsCorrected"}}},

//  {"hltAK4CaloJets"            , {{"GEN", "ak4GenJetsNoNu"}}},
//  {"hltAK4PFClusterJets"       , {{"GEN", "ak4GenJetsNoNu"}}},
//  {"hltAK4PFJets"              , {{"GEN", "ak4GenJetsNoNu"}}},
    {"hltAK4PFJetsCorrected"     , {{"GEN", "ak4GenJetsNoNu"}}},
//  {"hltAK4PFCHSJets"           , {{"GEN", "ak4GenJetsNoNu"}}},
    {"hltAK4PFCHSJetsCorrected"  , {{"GEN", "ak4GenJetsNoNu"}, {"Offline", "offlineAK4PFCHSJetsCorrected"}}},
//  {"hltAK4PFPuppiJets"         , {{"GEN", "ak4GenJetsNoNu"}}},
    {"hltAK4PFPuppiJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}, {"Offline", "offlineAK4PFPuppiJetsCorrected"}}},

    {"offlineAK4PFCHSJetsCorrected"  , {{"GEN", "ak4GenJetsNoNu"}}},
    {"offlineAK4PFPuppiJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}}},
  };

  labelMap_jetAK8_.clear();
  labelMap_jetAK8_ = {
    {"ak8GenJetsNoNu", {
//    {"hltCalo"        , "hltAK8CaloJets"},
//    {"hltPFCluster"   , "hltAK8PFClusterJets"},
//    {"hltPF"          , "hltAK8PFJets"},
      {"hltPFCorr"      , "hltAK8PFJetsCorrected"},
//    {"hltPFCHS"       , "hltAK8PFCHSJets"},
      {"hltPFCHSCorr"   , "hltAK8PFCHSJetsCorrected"},
//    {"hltPFPuppi"     , "hltAK8PFPuppiJets"},
      {"hltPFPuppiCorr" , "hltAK8PFPuppiJetsCorrected"},
      {"offlPFPuppiCorr", "offlineAK8PFPuppiJetsCorrected"},
    }},

//  {"hltAK8CaloJets"            , {{"GEN", "ak8GenJetsNoNu"}}},
//  {"hltAK8PFClusterJets"       , {{"GEN", "ak8GenJetsNoNu"}}},
//  {"hltAK8PFJets"              , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8PFJetsCorrected"     , {{"GEN", "ak8GenJetsNoNu"}}},
//  {"hltAK8PFCHSJets"           , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8PFCHSJetsCorrected"  , {{"GEN", "ak8GenJetsNoNu"}, {"Offline", "offlineAK8PFCHSJetsCorrected"}}},
//  {"hltAK8PFPuppiJets"         , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8PFPuppiJetsCorrected", {{"GEN", "ak8GenJetsNoNu"}, {"Offline", "offlineAK8PFPuppiJetsCorrected"}}},

    {"offlineAK8PFCHSJetsCorrected"  , {{"GEN", "ak8GenJetsNoNu"}}},
    {"offlineAK8PFPuppiJetsCorrected", {{"GEN", "ak8GenJetsNoNu"}}},
  };

  labelMap_MET_.clear();
  labelMap_MET_ = {
    {"genMETCalo", {}},
    {"genMETTrue", {}},

    {"l1tCaloMET"   , {{"GEN", "genMETCalo"}}},
    {"l1tPFMET"     , {{"GEN", "genMETTrue"}, {"Offline", "offlinePFMET_Raw"}}},
    {"l1tPFPuppiMET", {{"GEN", "genMETTrue"}, {"Offline", "offlinePFPuppiMET_Raw"}}},

//  {"hltPFClusterMET"   , {{"GEN", "genMETCalo"}}},
//  {"hltPFMETNoMu"      , {{"GEN", "genMETCalo"}}},
    {"hltPFMET"          , {{"GEN", "genMETTrue"}, {"Offline", "offlinePFMET_Raw"}}},
    {"hltPFCHSMET"       , {{"GEN", "genMETTrue"}}},
    {"hltPFSoftKillerMET", {{"GEN", "genMETTrue"}}},
//  {"hltPFPuppiMETNoMu" , {{"GEN", "genMETCalo"}}},
    {"hltPFPuppiMET"     , {{"GEN", "genMETTrue"}, {"Offline", "offlinePFPuppiMET_Raw"}}},
    {"hltPFPuppiMETv0"   , {{"GEN", "genMETTrue"}, {"Offline", "offlinePuppiMET_Raw"}}},

    {"offlinePFMET_Raw"       , {{"GEN", "genMETTrue"}}},
    {"offlinePFMET_Type1"     , {{"GEN", "genMETTrue"}}},
    {"offlinePFPuppiMET_Raw"  , {{"GEN", "genMETTrue"}}},
    {"offlinePFPuppiMET_Type1", {{"GEN", "genMETTrue"}}},
  };

  for(auto const& selLabel : {
    "NoSelection",
  }){
    // histograms: AK4 Jets
    for(auto const& jetLabel : labelMap_jetAK4_){
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    }

    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFJetsCorrected", "l1tSlwPFJetsCorrected");
    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFJetsCorrected", "offlineAK4PFJetsCorrected");

    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFPuppiJetsCorrected", "l1tSlwPFPuppiJetsCorrected");
    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFPuppiJetsCorrected", "offlineAK4PFPuppiJetsCorrected");

    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiHT", "l1tPFPuppiHT", true);

    // histograms: AK8 Jets
    for(auto const& jetLabel : labelMap_jetAK8_){
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    }

    // histograms: MET
    for(auto const& metLabel : labelMap_MET_){
      bookHistograms_MET(selLabel, metLabel.first, utils::mapKeys(metLabel.second));
    }

    bookHistograms_MET_2DMaps(selLabel, "hltPFMET", "l1tPFMET");
    bookHistograms_MET_2DMaps(selLabel, "hltPFMET", "offlinePFMET_Raw");

    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiMET", "l1tPFPuppiMET");
    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiMET", "offlinePFPuppiMET_Raw");
  }

  l1tSeeds_1Jet_ = {
    "L1T_SinglePFPuppiJet200off",
  };

  for(auto const& selLabel : l1tSeeds_1Jet_){
    // histograms: AK4 Jets
    for(auto const& jetLabel : labelMap_jetAK4_){
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    }
  }

  l1tSeeds_HT_ = {
    "L1T_PFPuppiHT450off",
  };

  for(auto const& selLabel : l1tSeeds_HT_){

    for(auto const& jetLabel : labelMap_jetAK4_){
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    }

    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFJetsCorrected", "l1tSlwPFJetsCorrected");
    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFJetsCorrected", "offlineAK4PFJetsCorrected");

    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFPuppiJetsCorrected", "l1tSlwPFPuppiJetsCorrected");
    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFPuppiJetsCorrected", "offlineAK4PFPuppiJetsCorrected");

    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiHT", "l1tPFPuppiHT", true);
  }

  l1tSeeds_MET_ = {
    "L1T_PFPuppiMET200off",
    "L1T_PFPuppiMET245off",
  };

  for(auto const& selLabel : l1tSeeds_MET_){
    // histograms: MET
    for(auto const& metLabel : labelMap_MET_){
      bookHistograms_MET(selLabel, metLabel.first, utils::mapKeys(metLabel.second));
    }

    bookHistograms_MET_2DMaps(selLabel, "hltPFMET", "l1tPFMET");
    bookHistograms_MET_2DMaps(selLabel, "hltPFMET", "offlinePFMET_Raw");

    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiMET", "l1tPFPuppiMET");
    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiMET", "offlinePFPuppiMET_Raw");
  }
}

void JMETriggerAnalysisDriverPhase2::analyze(){
  H1("eventsProcessed")->Fill(0.5, 1.);

  //// AK4 Jets
  const float minAK4JetPt(30.);
  const float minAK4JetPtRef(20.);
  const float maxAK4JetDeltaRmatchRef(0.1);

  // Single-Jet
  for(auto const& jetLabel : labelMap_jetAK4_){
    auto jetPt1(minAK4JetPt), jetPt2(minAK4JetPtRef);
    if(jetLabel.first.find("GenJets") != std::string::npos){
      std::swap(jetPt1, jetPt2);
    }

    fillHistoDataJets fhDataAK4Jets;
    fhDataAK4Jets.jetCollection = jetLabel.first;
    fhDataAK4Jets.jetPtMin = jetPt1;
    fhDataAK4Jets.jetAbsEtaMax = 5.0;
    for(auto const& jetLabelRefs : jetLabel.second){
      fhDataAK4Jets.matches.emplace_back(fillHistoDataJets::Match(jetLabelRefs.first, jetLabelRefs.second, jetPt2, maxAK4JetDeltaRmatchRef));
    }

    fillHistograms_Jets("NoSelection", fhDataAK4Jets);

    for(auto const& selLabel : l1tSeeds_1Jet_){
      if(not value<bool>(selLabel)){
        continue;
      }

      fillHistograms_Jets(selLabel, fhDataAK4Jets);
    }

    for(auto const& selLabel : l1tSeeds_HT_){
      if(not value<bool>(selLabel)){
        continue;
      }

      fillHistograms_Jets(selLabel, fhDataAK4Jets);
    }
  }

  // HT
  for(std::string const& jetType : {"PF", "PFPuppi"}){

    fillHistoDataJets fhDataL1TSLWJets;
    fhDataL1TSLWJets.jetCollection = "l1tSlw"+jetType+"JetsCorrected";
    fhDataL1TSLWJets.jetPtMin = 30.0;
    fhDataL1TSLWJets.jetAbsEtaMax = 2.4;

    fillHistoDataJets fhDataHLTAK4Jets;
    fhDataHLTAK4Jets.jetCollection = "hltAK4"+jetType+"JetsCorrected";
    fhDataHLTAK4Jets.jetPtMin = 30.0;
    fhDataHLTAK4Jets.jetAbsEtaMax = 5.0;

    fillHistoDataJets fhDataOffAK4Jets;
    fhDataOffAK4Jets.jetCollection = "offlineAK4"+jetType+"JetsCorrected";
    fhDataOffAK4Jets.jetPtMin = 30.0;
    fhDataOffAK4Jets.jetAbsEtaMax = 5.0;

    fillHistograms_Jets_2DMaps("NoSelection", fhDataHLTAK4Jets, fhDataL1TSLWJets);
    fillHistograms_Jets_2DMaps("NoSelection", fhDataHLTAK4Jets, fhDataOffAK4Jets);

    fillHistoDataMET fhDataHLTHT;
    fhDataHLTHT.metCollection = "hlt"+jetType+"HT";

    fillHistoDataMET fhDataL1THT;
    fhDataL1THT.metCollection = "l1t"+jetType+"HT";

    fillHistograms_MET_2DMaps("NoSelection", fhDataHLTHT, fhDataL1THT, true);

    for(auto const& selLabel : l1tSeeds_HT_){
      if(not value<bool>(selLabel)){
        continue;
      }

      fillHistograms_Jets_2DMaps(selLabel, fhDataHLTAK4Jets, fhDataL1TSLWJets);
      fillHistograms_Jets_2DMaps(selLabel, fhDataHLTAK4Jets, fhDataOffAK4Jets);

      if(jetType == "PFPuppi"){
        fillHistograms_MET_2DMaps(selLabel, fhDataHLTHT, fhDataL1THT, true);
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
    fhDataAK8Jets.jetAbsEtaMax = 5.0;

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

    for(auto const& selLabel : l1tSeeds_MET_){
      if(not value<bool>(selLabel)){
        continue;
      }

      fillHistograms_MET(selLabel, fhDataMET);
    }
  }

  for(std::string const& metType : {"PF", "PFPuppi"}){

    fillHistoDataMET fhDataL1TMET;
    fhDataL1TMET.metCollection = "l1t"+metType+"MET";

    fillHistoDataMET fhDataHLTMET;
    fhDataHLTMET.metCollection = "hlt"+metType+"MET";

    fillHistoDataMET fhDataOffMET;
    fhDataOffMET.metCollection = "offline"+metType+"MET_Raw";

    fillHistograms_MET_2DMaps("NoSelection", fhDataHLTMET, fhDataL1TMET);
    fillHistograms_MET_2DMaps("NoSelection", fhDataHLTMET, fhDataOffMET);

    for(auto const& selLabel : l1tSeeds_MET_){
      fillHistograms_MET_2DMaps(selLabel, fhDataHLTMET, fhDataL1TMET);
      fillHistograms_MET_2DMaps(selLabel, fhDataHLTMET, fhDataOffMET);
    }
  }
}

void JMETriggerAnalysisDriverPhase2::bookHistograms_Jets_2DMaps(const std::string& dir, const std::string& jetType1, const std::string& jetType2){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  std::vector<float> binEdges_HT(151);
  for(uint idx=0; idx<binEdges_HT.size(); ++idx){ binEdges_HT.at(idx) = idx * 10.; }

  addTH2D(dirPrefix+jetType1+"_HT__vs__"+jetType2+"_HT", binEdges_HT, binEdges_HT);
}

void JMETriggerAnalysisDriverPhase2::bookHistograms_MET_2DMaps(const std::string& dir, const std::string& metType1, const std::string& metType2, bool const book1D){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  std::vector<float> binEdges_pt(61);
  for(uint idx=0; idx<binEdges_pt.size(); ++idx){ binEdges_pt.at(idx) = idx * 10.; }

  std::vector<float> binEdges_phi(41);
  for(uint idx=0; idx<binEdges_phi.size(); ++idx){ binEdges_phi.at(idx) = M_PI*(0.05*idx - 1.); }

  std::vector<float> binEdges_sumEt(151);
  for(uint idx=0; idx<binEdges_sumEt.size(); ++idx){ binEdges_sumEt.at(idx) = 10.*idx; }

  if(book1D){
    addTH1D(dirPrefix+metType1+"_pt", binEdges_pt);
    addTH1D(dirPrefix+metType1+"_phi", binEdges_phi);
    addTH1D(dirPrefix+metType1+"_sumEt", binEdges_sumEt);

    addTH1D(dirPrefix+metType2+"_pt", binEdges_pt);
    addTH1D(dirPrefix+metType2+"_phi", binEdges_phi);
    addTH1D(dirPrefix+metType2+"_sumEt", binEdges_sumEt);
  }

  addTH2D(dirPrefix+metType1+"_pt__vs__"+metType2+"_pt", binEdges_pt, binEdges_pt);
  addTH2D(dirPrefix+metType1+"_phi__vs__"+metType2+"_phi", binEdges_phi, binEdges_phi);
  addTH2D(dirPrefix+metType1+"_sumEt__vs__"+metType2+"_sumEt", binEdges_sumEt, binEdges_sumEt);
}

void JMETriggerAnalysisDriverPhase2::fillHistograms_Jets_2DMaps(const std::string& dir, const fillHistoDataJets& fhData1, const fillHistoDataJets& fhData2){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  auto const* v_pt1(this->vector_ptr<float>(fhData1.jetCollection+"_pt"));
  auto const* v_eta1(this->vector_ptr<float>(fhData1.jetCollection+"_eta"));

  if(not (v_pt1 and v_eta1)){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverPhase2::fillHistograms_Jets_2DMaps(\"" << dir << "\", const fillHistoDataJets&, const fillHistoDataJets&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData1.jetCollection+"_pt/eta" << std::endl;
    }
    return;
  }

  auto const* v_pt2(this->vector_ptr<float>(fhData2.jetCollection+"_pt"));
  auto const* v_eta2(this->vector_ptr<float>(fhData2.jetCollection+"_eta"));

  if(not (v_pt2 and v_eta2)){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverPhase2::fillHistograms_Jets_2DMaps(\"" << dir << "\", const fillHistoDataJets&, const fillHistoDataJets&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData2.jetCollection+"_pt/eta" << std::endl;
    }
    return;
  }

  float sumPt1(0.);
  for(size_t idx=0; idx<v_pt1->size(); ++idx){
    if(v_pt1->at(idx) > fhData1.jetPtMin and std::abs(v_eta1->at(idx)) < fhData1.jetAbsEtaMax){
      sumPt1 += v_pt1->at(idx);
    }
  }

  float sumPt2(0.);
  for(size_t idx=0; idx<v_pt2->size(); ++idx){
    if(v_pt2->at(idx) > fhData2.jetPtMin and std::abs(v_eta2->at(idx)) < fhData2.jetAbsEtaMax){
      sumPt2 += v_pt2->at(idx);
    }
  }

  H2(dirPrefix+fhData1.jetCollection+"_HT__vs__"+fhData2.jetCollection+"_HT")->Fill(sumPt1, sumPt2);
}

void JMETriggerAnalysisDriverPhase2::fillHistograms_MET_2DMaps(const std::string& dir, const fillHistoDataMET& fhData1, const fillHistoDataMET& fhData2, bool const fill1D){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  auto const* v_pt1(this->vector_ptr<float>(fhData1.metCollection+"_pt"));
  if(not v_pt1){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverPhase2::fillHistograms_MET_2DMaps(\"" << dir << "\", const fillHistoDataMET&, const fillHistoDataMET&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData1.metCollection+"_pt" << std::endl;
    }
    return;
  }
  else if(v_pt1->size() != 1){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverPhase2::fillHistograms_MET_2DMaps(\"" << dir << "\", const fillHistoDataMET&, const fillHistoDataMET&) -- "
                << "MET branches have invalid size (histograms will not be filled): "
                << fhData1.metCollection+"_pt" << std::endl;
    }
    return;
  }

  auto const* v_pt2(this->vector_ptr<float>(fhData2.metCollection+"_pt"));
  if(not v_pt2){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverPhase2::fillHistograms_MET_2DMaps(\"" << dir << "\", const fillHistoDataMET&, const fillHistoDataMET&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData2.metCollection+"_pt" << std::endl;
    }
    return;
  }
  else if(v_pt2->size() != 1){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverPhase2::fillHistograms_MET_2DMaps(\"" << dir << "\", const fillHistoDataMET&, const fillHistoDataMET&) -- "
                << "MET branches have invalid size (histograms will not be filled): "
                << fhData2.metCollection+"_pt" << std::endl;
    }
    return;
  }

  auto const* v_phi1(this->vector_ptr<float>(fhData1.metCollection+"_phi"));
  auto const* v_phi2(this->vector_ptr<float>(fhData2.metCollection+"_phi"));

  auto const* v_sumEt1(this->vector_ptr<float>(fhData1.metCollection+"_sumEt"));
  auto const* v_sumEt2(this->vector_ptr<float>(fhData2.metCollection+"_sumEt"));

  auto const met1_pt(v_pt1->at(0)), met1_phi(v_phi1->at(0)), met1_sumEt(v_sumEt1->at(0));
  auto const met2_pt(v_pt2->at(0)), met2_phi(v_phi2->at(0)), met2_sumEt(v_sumEt2->at(0));

  if(fill1D){
    H1(dirPrefix+fhData1.metCollection+"_pt")->Fill(met1_pt);
    H1(dirPrefix+fhData1.metCollection+"_phi")->Fill(met1_phi);
    H1(dirPrefix+fhData1.metCollection+"_sumEt")->Fill(met1_sumEt);

    H1(dirPrefix+fhData2.metCollection+"_pt")->Fill(met2_pt);
    H1(dirPrefix+fhData2.metCollection+"_phi")->Fill(met2_phi);
    H1(dirPrefix+fhData2.metCollection+"_sumEt")->Fill(met2_sumEt);
  }

  H2(dirPrefix+fhData1.metCollection+"_pt__vs__"+fhData2.metCollection+"_pt")->Fill(met1_pt, met2_pt);
  H2(dirPrefix+fhData1.metCollection+"_phi__vs__"+fhData2.metCollection+"_phi")->Fill(met1_phi, met2_phi);
  H2(dirPrefix+fhData1.metCollection+"_sumEt__vs__"+fhData2.metCollection+"_sumEt")->Fill(met1_sumEt, met2_sumEt);
}
