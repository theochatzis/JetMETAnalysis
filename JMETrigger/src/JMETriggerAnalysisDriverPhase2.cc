#include <NTupleAnalysis/JMETrigger/interface/JMETriggerAnalysisDriverPhase2.h>

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

  for(auto const& selLabel : {"NoSelection"}){

    // histograms: AK4 Jets
    bookHistograms_Jets(selLabel, "ak4GenJetsNoNu", {"Calo", "PFCluster", "PF", "PFCHS", "Puppi"});
    bookHistograms_Jets(selLabel, "hltAK4CaloJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFClusterJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFJetsCorrected", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFCHSJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFCHSJetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK4PuppiJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PuppiJetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "offlineAK4PFCHSJetsCorrected", {"GEN"});
    bookHistograms_Jets(selLabel, "offlineAK4PuppiJetsCorrected", {"GEN"});

    // histograms: AK8 Jets
    bookHistograms_Jets(selLabel, "ak8GenJetsNoNu", {"Calo", "PFCluster", "PF", "PFCHS", "Puppi"});
    bookHistograms_Jets(selLabel, "hltAK8CaloJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFClusterJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFJetsCorrected", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFCHSJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFCHSJetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK8PuppiJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PuppiJetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "offlineAK8PFCHSJetsCorrected", {"GEN"});
    bookHistograms_Jets(selLabel, "offlineAK8PuppiJetsCorrected", {"GEN"});

    // histograms: MET
    bookHistograms_MET(selLabel, "genMETCalo");
    bookHistograms_MET(selLabel, "genMETTrue");

    bookHistograms_MET(selLabel, "hltPFClusterMET", {"GEN"});

    bookHistograms_MET(selLabel, "hltPFMET", {"GEN", "Offline"});
    bookHistograms_MET(selLabel, "hltPFMETNoMu", {"GEN"});

    bookHistograms_MET(selLabel, "hltPFCHSMET", {"GEN"});
    bookHistograms_MET(selLabel, "hltPFSoftKillerMET", {"GEN"});

    bookHistograms_MET(selLabel, "hltPuppiMET", {"GEN", "Offline"});
    bookHistograms_MET(selLabel, "hltPuppiMETNoMu", {"GEN"});

    bookHistograms_MET(selLabel, "offlinePFMET_Raw", {"GEN"});
    bookHistograms_MET(selLabel, "offlinePFMET_Type1", {"GEN"});
    bookHistograms_MET(selLabel, "offlinePuppiMET_Raw", {"GEN"});
    bookHistograms_MET(selLabel, "offlinePuppiMET_Type1", {"GEN"});
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
  const float minAK4JetPt_GEN(25.);
  const float minAK4JetPt_Offline(25.);
  const float maxAK4JetDeltaRmatch_GEN(0.1);
  const float maxAK4JetDeltaRmatch_Offline(0.1);

  // AK4 GEN
  fillHistoDataJets fhDataAK4GEN;
  fhDataAK4GEN.jetCollection = "ak4GenJetsNoNu";
  fhDataAK4GEN.jetPtMin = minAK4JetPt_GEN;
  fhDataAK4GEN.matches.emplace_back(fillHistoDataJets::Match("Calo", "hltAK4CaloJets", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(fillHistoDataJets::Match("PFCluster", "hltAK4PFClusterJets", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(fillHistoDataJets::Match("PF", "hltAK4PFJetsCorrected", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(fillHistoDataJets::Match("PFCHS", "hltAK4PFCHSJetsCorrected", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(fillHistoDataJets::Match("Puppi", "hltAK4PuppiJetsCorrected", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK4GEN);

  // AK4 CaloJets
  fillHistoDataJets fhDataAK4CaloJets;
  fhDataAK4CaloJets.jetCollection = "hltAK4CaloJets";
  fhDataAK4CaloJets.jetPtMin = minAK4JetPt;
  fhDataAK4CaloJets.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK4CaloJets);

  // AK4 PFClusterJets
  fillHistoDataJets fhDataAK4PFClusterJets;
  fhDataAK4PFClusterJets.jetCollection = "hltAK4PFClusterJets";
  fhDataAK4PFClusterJets.jetPtMin = minAK4JetPt;
  fhDataAK4PFClusterJets.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK4PFClusterJets);

  // AK4 PFJets
  fillHistoDataJets fhDataAK4PFJets;
  fhDataAK4PFJets.jetCollection = "hltAK4PFJets";
  fhDataAK4PFJets.jetPtMin = minAK4JetPt;
  fhDataAK4PFJets.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK4PFJets);

  // AK4 PFJetsCorrected
  fillHistoDataJets fhDataAK4PFJetsCorrected;
  fhDataAK4PFJetsCorrected.jetCollection = "hltAK4PFJetsCorrected";
  fhDataAK4PFJetsCorrected.jetPtMin = minAK4JetPt;
  fhDataAK4PFJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK4PFJetsCorrected);

  // AK4 PFCHSJets
  fillHistoDataJets fhDataAK4PFCHSJets;
  fhDataAK4PFCHSJets.jetCollection = "hltAK4PFCHSJets";
  fhDataAK4PFCHSJets.jetPtMin = minAK4JetPt;
  fhDataAK4PFCHSJets.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK4PFCHSJets);

  // AK4 PFCHSJetsCorrected
  fillHistoDataJets fhDataAK4PFCHSJetsCorrected;
  fhDataAK4PFCHSJetsCorrected.jetCollection = "hltAK4PFCHSJetsCorrected";
  fhDataAK4PFCHSJetsCorrected.jetPtMin = minAK4JetPt;
  fhDataAK4PFCHSJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4PFCHSJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("Offline", "offlineAK4PFCHSJetsCorrected", minAK4JetPt_Offline, maxAK4JetDeltaRmatch_Offline));
  fillHistograms_Jets("NoSelection", fhDataAK4PFCHSJetsCorrected);

  // AK4 PuppiJets
  fillHistoDataJets fhDataAK4PuppiJets;
  fhDataAK4PuppiJets.jetCollection = "hltAK4PuppiJets";
  fhDataAK4PuppiJets.jetPtMin = minAK4JetPt;
  fhDataAK4PuppiJets.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK4PuppiJets);

  // AK4 PuppiJetsCorrected
  fillHistoDataJets fhDataAK4PuppiJetsCorrected;
  fhDataAK4PuppiJetsCorrected.jetCollection = "hltAK4PuppiJetsCorrected";
  fhDataAK4PuppiJetsCorrected.jetPtMin = minAK4JetPt;
  fhDataAK4PuppiJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4PuppiJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("Offline", "offlineAK4PuppiJetsCorrected", minAK4JetPt_Offline, maxAK4JetDeltaRmatch_Offline));
  fillHistograms_Jets("NoSelection", fhDataAK4PuppiJetsCorrected);

  // Offline: AK4 PFCHSJetsCorrected
  fillHistoDataJets fhDataOfflineAK4PFCHSJetsCorrected;
  fhDataOfflineAK4PFCHSJetsCorrected.jetCollection = "offlineAK4PFCHSJetsCorrected";
  fhDataOfflineAK4PFCHSJetsCorrected.jetPtMin = minAK4JetPt;
  fhDataOfflineAK4PFCHSJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataOfflineAK4PFCHSJetsCorrected);

  // Offline: AK4 PuppiJetsCorrected
  fillHistoDataJets fhDataOfflineAK4PuppiJetsCorrected;
  fhDataOfflineAK4PuppiJetsCorrected.jetCollection = "offlineAK4PuppiJetsCorrected";
  fhDataOfflineAK4PuppiJetsCorrected.jetPtMin = minAK4JetPt;
  fhDataOfflineAK4PuppiJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataOfflineAK4PuppiJetsCorrected);

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
        fhData.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));
        if(algo == "Puppi"){
          fhData.matches.emplace_back(fillHistoDataJets::Match("Offline", "offlineAK4PuppiJetsCorrected", minAK4JetPt_Offline, maxAK4JetDeltaRmatch_Offline));
        }
        else if(algo == "PFCHS"){
          fhData.matches.emplace_back(fillHistoDataJets::Match("Offline", "offlineAK4PFCHSJetsCorrected", minAK4JetPt_Offline, maxAK4JetDeltaRmatch_Offline));
        }
        fillHistograms_Jets(selLabel, fhData);
      }
    }
  }

  //// AK8 Jets
  const float minAK8JetPt(90.);
  const float minAK8JetPt_GEN(75.);
  const float minAK8JetPt_Offline(75.);
  const float maxAK8JetDeltaRmatch_GEN(0.1);
  const float maxAK8JetDeltaRmatch_Offline(0.1);

  // AK8 GEN
  fillHistoDataJets fhDataAK8GEN;
  fhDataAK8GEN.jetCollection = "ak8GenJetsNoNu";
  fhDataAK8GEN.jetPtMin = minAK8JetPt_GEN;
  fhDataAK8GEN.matches.emplace_back(fillHistoDataJets::Match("Calo", "hltAK8CaloJets", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(fillHistoDataJets::Match("PFCluster", "hltAK8PFClusterJets", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(fillHistoDataJets::Match("PF", "hltAK8PFJetsCorrected", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(fillHistoDataJets::Match("PFCHS", "hltAK8PFCHSJetsCorrected", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(fillHistoDataJets::Match("Puppi", "hltAK8PuppiJetsCorrected", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK8GEN);

  // AK8 CaloJets
  fillHistoDataJets fhDataAK8CaloJets;
  fhDataAK8CaloJets.jetCollection = "hltAK8CaloJets";
  fhDataAK8CaloJets.jetPtMin = minAK8JetPt;
  fhDataAK8CaloJets.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak8GenJetsNoNu", minAK8JetPt_GEN, maxAK8JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK8CaloJets);

  // AK8 PFClusterJets
  fillHistoDataJets fhDataAK8PFClusterJets;
  fhDataAK8PFClusterJets.jetCollection = "hltAK8PFClusterJets";
  fhDataAK8PFClusterJets.jetPtMin = minAK8JetPt;
  fhDataAK8PFClusterJets.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak8GenJetsNoNu", minAK8JetPt_GEN, maxAK8JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK8PFClusterJets);

  // AK8 PFJets
  fillHistoDataJets fhDataAK8PFJets;
  fhDataAK8PFJets.jetCollection = "hltAK8PFJets";
  fhDataAK8PFJets.jetPtMin = minAK8JetPt;
  fhDataAK8PFJets.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak8GenJetsNoNu", minAK8JetPt_GEN, maxAK8JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK8PFJets);

  // AK8 PFJetsCorrected
  fillHistoDataJets fhDataAK8PFJetsCorrected;
  fhDataAK8PFJetsCorrected.jetCollection = "hltAK8PFJetsCorrected";
  fhDataAK8PFJetsCorrected.jetPtMin = minAK8JetPt;
  fhDataAK8PFJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak8GenJetsNoNu", minAK8JetPt_GEN, maxAK8JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK8PFJetsCorrected);

  // AK8 PFCHSJets
  fillHistoDataJets fhDataAK8PFCHSJets;
  fhDataAK8PFCHSJets.jetCollection = "hltAK8PFCHSJets";
  fhDataAK8PFCHSJets.jetPtMin = minAK8JetPt;
  fhDataAK8PFCHSJets.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak8GenJetsNoNu", minAK8JetPt_GEN, maxAK8JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK8PFCHSJets);

  // AK8 PFCHSJetsCorrected
  fillHistoDataJets fhDataAK8PFCHSJetsCorrected;
  fhDataAK8PFCHSJetsCorrected.jetCollection = "hltAK8PFCHSJetsCorrected";
  fhDataAK8PFCHSJetsCorrected.jetPtMin = minAK8JetPt;
  fhDataAK8PFCHSJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak8GenJetsNoNu", minAK8JetPt_GEN, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8PFCHSJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("Offline", "offlineAK8PFCHSJetsCorrected", minAK8JetPt_Offline, maxAK8JetDeltaRmatch_Offline));
  fillHistograms_Jets("NoSelection", fhDataAK8PFCHSJetsCorrected);

  // AK8 PuppiJets
  fillHistoDataJets fhDataAK8PuppiJets;
  fhDataAK8PuppiJets.jetCollection = "hltAK8PuppiJets";
  fhDataAK8PuppiJets.jetPtMin = minAK8JetPt;
  fhDataAK8PuppiJets.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak8GenJetsNoNu", minAK8JetPt_GEN, maxAK8JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK8PuppiJets);

  // AK8 PuppiJetsCorrected
  fillHistoDataJets fhDataAK8PuppiJetsCorrected;
  fhDataAK8PuppiJetsCorrected.jetCollection = "hltAK8PuppiJetsCorrected";
  fhDataAK8PuppiJetsCorrected.jetPtMin = minAK8JetPt;
  fhDataAK8PuppiJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak8GenJetsNoNu", minAK8JetPt_GEN, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8PuppiJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("Offline", "offlineAK8PuppiJetsCorrected", minAK8JetPt_Offline, maxAK8JetDeltaRmatch_Offline));
  fillHistograms_Jets("NoSelection", fhDataAK8PuppiJetsCorrected);

  // Offline: AK8 PFCHSJetsCorrected
  fillHistoDataJets fhDataOfflineAK8PFCHSJetsCorrected;
  fhDataOfflineAK8PFCHSJetsCorrected.jetCollection = "offlineAK8PFCHSJetsCorrected";
  fhDataOfflineAK8PFCHSJetsCorrected.jetPtMin = minAK8JetPt;
  fhDataOfflineAK8PFCHSJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak8GenJetsNoNu", minAK8JetPt_GEN, maxAK8JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataOfflineAK8PFCHSJetsCorrected);

  // Offline: AK8 PuppiJetsCorrected
  fillHistoDataJets fhDataOfflineAK8PuppiJetsCorrected;
  fhDataOfflineAK8PuppiJetsCorrected.jetCollection = "offlineAK8PuppiJetsCorrected";
  fhDataOfflineAK8PuppiJetsCorrected.jetPtMin = minAK8JetPt;
  fhDataOfflineAK8PuppiJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak8GenJetsNoNu", minAK8JetPt_GEN, maxAK8JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataOfflineAK8PuppiJetsCorrected);

  //// MET

  // GEN Calo
  fillHistoDataMET fhDataGENMETCalo;
  fhDataGENMETCalo.metCollection = "genMETCalo";
  fillHistograms_MET("NoSelection", fhDataGENMETCalo);

  // GEN True
  fillHistoDataMET fhDataGENMETTrue;
  fhDataGENMETTrue.metCollection = "genMETTrue";
  fillHistograms_MET("NoSelection", fhDataGENMETTrue);

  // PF
  fillHistoDataMET fhDataMETPF;
  fhDataMETPF.metCollection = "hltPFMET";
  fhDataMETPF.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETTrue"));
  fhDataMETPF.matches.emplace_back(fillHistoDataMET::Match("Offline", "offlinePFMET_Raw"));
  fillHistograms_MET("NoSelection", fhDataMETPF);

  // Puppi
  fillHistoDataMET fhDataMETPuppi;
  fhDataMETPuppi.metCollection = "hltPuppiMET";
  fhDataMETPuppi.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETTrue"));
  fhDataMETPuppi.matches.emplace_back(fillHistoDataMET::Match("Offline", "offlinePuppiMET_Raw"));
  fillHistograms_MET("NoSelection", fhDataMETPuppi);

  // METNoMu
  for(std::string const& metLabel : {
    "hltPFClusterMET",
    "hltPFMETNoMu",
    "hltPuppiMETNoMu",
  }){
    fillHistoDataMET fhDataMET;
    fhDataMET.metCollection = metLabel;
    fhDataMET.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETCalo"));
    fillHistograms_MET("NoSelection", fhDataMET);
  }

  // MET
  for(std::string const& metLabel : {
    "hltPFCHSMET",
    "hltPFSoftKillerMET",
    "offlinePFMET_Raw",
    "offlinePFMET_Type1",
    "offlinePuppiMET_Raw",
    "offlinePuppiMET_Type1",
  }){
    fillHistoDataMET fhDataMET;
    fhDataMET.metCollection = metLabel;
    fhDataMET.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETTrue"));
    fillHistograms_MET("NoSelection", fhDataMET);
  }
}
