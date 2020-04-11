#include <NTupleAnalysis/JMETrigger/interface/JMETriggerAnalysisDriver.h>
#include <NTupleAnalysis/JMETrigger/interface/Utils.h>
#include <math.h>

JMETriggerAnalysisDriver::JMETriggerAnalysisDriver(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath, const std::string& outputFileMode)
  : AnalysisDriverBase(tfile, ttree, outputFilePath, outputFileMode) {

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

    "_HE1",
//  "_HE1Pt0",
//  "_HE1Pt1",
//  "_HE1Pt2",
//  "_HE1Pt3",
//  "_HE1Pt4",

    "_HE2",
//  "_HE2Pt0",
//  "_HE2Pt1",
//  "_HE2Pt2",
//  "_HE2Pt3",
//  "_HE2Pt4",

    "_HF",
//  "_HFPt0",
//  "_HFPt1",
//  "_HFPt2",
//  "_HFPt3",
//  "_HFPt4",
  };
}

bool JMETriggerAnalysisDriver::jetBelongsToCategory(const std::string& categLabel, const float jetPt, const float jetAbsEta) const {

  bool ret(false);
  if(categLabel == "_EtaIncl"){ ret = (jetAbsEta < 5.0); }
  else if(categLabel == "_EtaInclPt0"){ ret = (jetAbsEta < 5.0) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_EtaInclPt1"){ ret = (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_EtaInclPt2"){ ret = (jetAbsEta < 5.0) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_EtaInclPt3"){ ret = (jetAbsEta < 5.0) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_EtaInclPt4"){ ret = (jetAbsEta < 5.0) and (2000. <= jetPt); }

  else if(categLabel == "_HB"){ ret = (jetAbsEta < 1.3); }
  else if(categLabel == "_HBPt0"){ ret = (jetAbsEta < 1.3) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HBPt1"){ ret = (jetAbsEta < 1.3) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HBPt2"){ ret = (jetAbsEta < 1.3) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HBPt3"){ ret = (jetAbsEta < 1.3) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HBPt4"){ ret = (jetAbsEta < 1.3) and (2000. <= jetPt); }

  else if(categLabel == "_HE1"){ ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5); }
  else if(categLabel == "_HE1Pt0"){ ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HE1Pt1"){ ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HE1Pt2"){ ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HE1Pt3"){ ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HE1Pt4"){ ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (2000. <= jetPt); }

  else if(categLabel == "_HE2"){ ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0); }
  else if(categLabel == "_HE2Pt0"){ ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HE2Pt1"){ ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HE2Pt2"){ ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HE2Pt3"){ ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HE2Pt4"){ ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (2000. <= jetPt); }

  else if(categLabel == "_HF"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0); }
  else if(categLabel == "_HFPt0"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HFPt1"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HFPt2"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HFPt3"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HFPt4"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (2000. <= jetPt); }

  return ret;
}

void JMETriggerAnalysisDriver::init(){
  // histogram: events counter
  addTH1D("eventsProcessed", {0, 1});

  for(auto const& selLabel : {"NoSelection"}){

    // histograms: AK4 Jets
    bookHistograms_Jets(selLabel, "ak4GenJetsNoNu", {"Calo", "PF", "PFCHS", "Puppi"});
    bookHistograms_Jets(selLabel, "hltAK4CaloJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4CaloJetsCorrected", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFJetsCorrected", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFCHSJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFCHSJetsCorrected", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PuppiJets", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK4PuppiJetsCorrected", {"GEN", "Offline"});

    // histograms: AK8 Jets
    bookHistograms_Jets(selLabel, "ak8GenJetsNoNu", {"Calo", "PF", "PFCHS", "Puppi"});
    bookHistograms_Jets(selLabel, "hltAK8CaloJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8CaloJetsCorrected", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFJetsCorrected", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFCHSJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFCHSJetsCorrected", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PuppiJets", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK8PuppiJetsCorrected", {"GEN", "Offline"});

    // histograms: MET
    bookHistograms_MET(selLabel, "genMETCalo");
    bookHistograms_MET(selLabel, "genMETTrue");

    bookHistograms_MET(selLabel, "hltCaloMET", {"GEN"});

    bookHistograms_MET(selLabel, "hltPFMET", {"GEN", "Offline"});
    bookHistograms_MET(selLabel, "hltPFMETNoMu", {"GEN"});

    bookHistograms_MET(selLabel, "hltPuppiMET", {"GEN", "Offline"});
    bookHistograms_MET(selLabel, "hltPuppiMETNoMu", {"GEN"});

    bookHistograms_MET(selLabel, "hltPFMETCHS", {"GEN"});
    bookHistograms_MET(selLabel, "hltPFMETSoftKiller", {"GEN"});
  }
}

void JMETriggerAnalysisDriver::analyze(){

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
  fhDataAK4GEN.matches.emplace_back(fillHistoDataJets::Match("Calo", "hltAK4CaloJetsCorrected", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
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

  // AK4 CaloJetsCorrected
  fillHistoDataJets fhDataAK4CaloJetsCorrected;
  fhDataAK4CaloJetsCorrected.jetCollection = "hltAK4CaloJetsCorrected";
  fhDataAK4CaloJetsCorrected.jetPtMin = minAK4JetPt;
  fhDataAK4CaloJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK4CaloJetsCorrected);

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
  fhDataAK4PFCHSJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("Offline", "offlineAK4PFCHSJets", minAK4JetPt_Offline, maxAK4JetDeltaRmatch_Offline));
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
  fhDataAK4PuppiJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("Offline", "offlineAK4PuppiJets", minAK4JetPt_Offline, maxAK4JetDeltaRmatch_Offline));
  fillHistograms_Jets("NoSelection", fhDataAK4PuppiJetsCorrected);

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
  fhDataAK8GEN.matches.emplace_back(fillHistoDataJets::Match("Calo", "hltAK8CaloJetsCorrected", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
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

  // AK8 CaloJetsCorrected
  fillHistoDataJets fhDataAK8CaloJetsCorrected;
  fhDataAK8CaloJetsCorrected.jetCollection = "hltAK8CaloJetsCorrected";
  fhDataAK8CaloJetsCorrected.jetPtMin = minAK8JetPt;
  fhDataAK8CaloJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("GEN", "ak8GenJetsNoNu", minAK8JetPt_GEN, maxAK8JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK8CaloJetsCorrected);

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
  fhDataAK8PFCHSJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("Offline", "offlineAK8PFCHSJets", minAK8JetPt_Offline, maxAK8JetDeltaRmatch_Offline));
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
  fhDataAK8PuppiJetsCorrected.matches.emplace_back(fillHistoDataJets::Match("Offline", "offlineAK8PuppiJets", minAK8JetPt_Offline, maxAK8JetDeltaRmatch_Offline));
  fillHistograms_Jets("NoSelection", fhDataAK8PuppiJetsCorrected);

  //// MET

  // GEN Calo
  fillHistoDataMET fhDataGENMETCalo;
  fhDataGENMETCalo.metCollection = "genMETCalo";
  fillHistograms_MET("NoSelection", fhDataGENMETCalo);

  // GEN True
  fillHistoDataMET fhDataGENMETTrue;
  fhDataGENMETTrue.metCollection = "genMETTrue";
  fillHistograms_MET("NoSelection", fhDataGENMETTrue);

  // Calo
  fillHistoDataMET fhDataMETCalo;
  fhDataMETCalo.metCollection = "hltCaloMET";
  fhDataMETCalo.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETCalo"));
  fillHistograms_MET("NoSelection", fhDataMETCalo);

  // PF
  fillHistoDataMET fhDataMETPF;
  fhDataMETPF.metCollection = "hltPFMET";
  fhDataMETPF.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETTrue"));
  fillHistograms_MET("NoSelection", fhDataMETPF);

  // PFNoMu
  fillHistoDataMET fhDataMETPFNoMu;
  fhDataMETPFNoMu.metCollection = "hltPFMETNoMu";
  fhDataMETPFNoMu.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETCalo"));
  fillHistograms_MET("NoSelection", fhDataMETPFNoMu);

  // Puppi
  fillHistoDataMET fhDataMETPuppi;
  fhDataMETPuppi.metCollection = "hltPuppiMET";
  fhDataMETPuppi.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETTrue"));
  fillHistograms_MET("NoSelection", fhDataMETPuppi);

  // PuppiNoMu
  fillHistoDataMET fhDataMETPuppiNoMu;
  fhDataMETPuppiNoMu.metCollection = "hltPuppiMETNoMu";
  fhDataMETPuppiNoMu.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETCalo"));
  fillHistograms_MET("NoSelection", fhDataMETPuppiNoMu);

  // PF+CHS
  fillHistoDataMET fhDataMETPFCHS;
  fhDataMETPFCHS.metCollection = "hltPFMETCHS";
  fhDataMETPFCHS.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETTrue"));
  fillHistograms_MET("NoSelection", fhDataMETPFCHS);

  // PF+SoftKiller
  fillHistoDataMET fhDataMETPFSoftKiller;
  fhDataMETPFSoftKiller.metCollection = "hltPFMETSoftKiller";
  fhDataMETPFSoftKiller.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETTrue"));
  fillHistograms_MET("NoSelection", fhDataMETPFSoftKiller);
}

void JMETriggerAnalysisDriver::bookHistograms_Jets(const std::string& dir, const std::string& jetType, const std::vector<std::string>& matchLabels){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

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

  std::vector<float> binEdges_numberOfDaughters(121);
  for(uint idx=0; idx<121; ++idx){ binEdges_numberOfDaughters.at(idx) = 2.*idx; }

  std::vector<float> binEdges_energyFrac(21);
  for(uint idx=0; idx<21; ++idx){ binEdges_energyFrac.at(idx) = 0.05*idx; }

  std::vector<float> binEdges_dauMult1(61);
  for(uint idx=0; idx<61; ++idx){ binEdges_dauMult1.at(idx) = idx; }

  std::vector<float> binEdges_dauMult2(13);
  for(uint idx=0; idx<13; ++idx){ binEdges_dauMult2.at(idx) = idx; }

  std::vector<float> binEdges_dRmatch(26);
  for(uint idx=0; idx<26; ++idx){ binEdges_dRmatch.at(idx) = 0.2*idx; }

  std::vector<float> binEdges_response(51);
  for(uint idx=0; idx<51; ++idx){ binEdges_response.at(idx) = 0.1*idx; }

  for(auto const& catLabel : jetCategoryLabels_){

    addTH1D(dirPrefix+jetType+catLabel+"_njets", binEdges_njets);
    addTH1D(dirPrefix+jetType+catLabel+"_pt", binEdges_pt);
    addTH1D(dirPrefix+jetType+catLabel+"_pt0", binEdges_pt);
    addTH1D(dirPrefix+jetType+catLabel+"_eta", binEdges_eta);
    addTH2D(dirPrefix+jetType+catLabel+"_eta__vs__pt", binEdges_eta, binEdges_pt);
    addTH1D(dirPrefix+jetType+catLabel+"_phi", binEdges_phi);
    addTH1D(dirPrefix+jetType+catLabel+"_mass", binEdges_mass);
    addTH1D(dirPrefix+jetType+catLabel+"_numberOfDaughters", binEdges_numberOfDaughters);
    addTH1D(dirPrefix+jetType+catLabel+"_chargedHadronEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix+jetType+catLabel+"_neutralHadronEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix+jetType+catLabel+"_electronEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix+jetType+catLabel+"_photonEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix+jetType+catLabel+"_muonEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix+jetType+catLabel+"_chargedHadronMultiplicity", binEdges_dauMult1);
    addTH1D(dirPrefix+jetType+catLabel+"_neutralHadronMultiplicity", binEdges_dauMult1);
    addTH1D(dirPrefix+jetType+catLabel+"_electronMultiplicity", binEdges_dauMult2);
    addTH1D(dirPrefix+jetType+catLabel+"_photonMultiplicity", binEdges_dauMult1);
    addTH1D(dirPrefix+jetType+catLabel+"_muonMultiplicity", binEdges_dauMult2);

    for(auto const& matchLabel : matchLabels){

      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_njets", binEdges_njets);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_pt", binEdges_pt);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_pt0", binEdges_pt);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_eta", binEdges_eta);
      addTH2D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_eta__vs__pt", binEdges_eta, binEdges_pt);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_phi", binEdges_phi);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_mass", binEdges_mass);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_numberOfDaughters", binEdges_numberOfDaughters);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_chargedHadronEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_neutralHadronEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_electronEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_photonEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_muonEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_chargedHadronMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_neutralHadronMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_electronMultiplicity", binEdges_dauMult2);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_photonMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_muonMultiplicity", binEdges_dauMult2);

      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_dRmatch", binEdges_dRmatch);

      addTH2D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_pt__vs__"+matchLabel+"_pt", binEdges_pt, binEdges_pt);
      addTH2D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_pt0__vs__"+matchLabel+"_pt", binEdges_pt, binEdges_pt);
      addTH2D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_pt0__vs__"+matchLabel+"_eta", binEdges_pt, binEdges_eta);
      addTH2D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_eta__vs__"+matchLabel+"_eta", binEdges_eta, binEdges_eta);

      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_pt_over"+matchLabel, binEdges_response);
      addTH2D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_pt", binEdges_response, binEdges_pt);
      addTH2D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_eta", binEdges_response, binEdges_eta);

      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_pt0_over"+matchLabel, binEdges_response);
      addTH2D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_pt0_over"+matchLabel+"__vs__"+matchLabel+"_pt", binEdges_response, binEdges_pt);
      addTH2D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_pt0_over"+matchLabel+"__vs__"+matchLabel+"_eta", binEdges_response, binEdges_eta);

      addTH1D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_mass_over"+matchLabel, binEdges_response);
      addTH2D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_mass_over"+matchLabel+"__vs__"+matchLabel+"_pt", binEdges_response, binEdges_pt);
      addTH2D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_mass_over"+matchLabel+"__vs__"+matchLabel+"_eta", binEdges_response, binEdges_eta);
      addTH2D(dirPrefix+jetType+catLabel+"_MatchedTo"+matchLabel+"_mass_over"+matchLabel+"__vs__"+matchLabel+"_mass", binEdges_response, binEdges_mass);

      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_njets", binEdges_njets);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_pt", binEdges_pt);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_pt0", binEdges_pt);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_eta", binEdges_eta);
      addTH2D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_eta__vs__pt", binEdges_eta, binEdges_pt);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_phi", binEdges_phi);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_mass", binEdges_mass);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_numberOfDaughters", binEdges_numberOfDaughters);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_chargedHadronEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_neutralHadronEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_electronEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_photonEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_muonEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_chargedHadronMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_neutralHadronMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_electronMultiplicity", binEdges_dauMult2);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_photonMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix+jetType+catLabel+"_NotMatchedTo"+matchLabel+"_muonMultiplicity", binEdges_dauMult2);
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

  std::vector<float> binEdges_sumEt(121);
  for(uint idx=0; idx<121; ++idx){ binEdges_sumEt.at(idx) = 50.*idx; }

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

void JMETriggerAnalysisDriver::fillHistograms_Jets(const std::string& dir, const fillHistoDataJets& fhData){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  auto const* v_pt(this->vector_ptr<float>(fhData.jetCollection+"_pt"));
  auto const* v_eta(this->vector_ptr<float>(fhData.jetCollection+"_eta"));
  auto const* v_phi(this->vector_ptr<float>(fhData.jetCollection+"_phi"));
  auto const* v_mass(this->vector_ptr<float>(fhData.jetCollection+"_mass"));

  auto const* v_numberOfDaughters(this->vector_ptr<uint>(fhData.jetCollection+"_numberOfDaughters"));

  if(not (v_pt and v_eta and v_phi and v_mass)){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriver::fillHistograms_Jets(\"" << dir << "\", const fillHistoDataJets&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData.jetCollection+"_pt/eta/phi/mass" << std::endl;
    }
    return;
  }

  for(auto const& catLabel : jetCategoryLabels_){

    std::vector<size_t> jetIndices;
    jetIndices.reserve(v_pt->size());
    int indexMaxPtJet(-1);
    float jetPtMax(-1.);
    for(size_t idx=0; idx<v_pt->size(); ++idx){
      if(v_pt->at(idx) <= fhData.jetPtMin){ continue; }

      if(jetBelongsToCategory(catLabel, v_pt->at(idx), std::abs(v_eta->at(idx)))){
        jetIndices.emplace_back(idx);
        if((jetIndices.size() == 1) or (v_pt->at(idx) > jetPtMax)){
          jetPtMax = v_pt->at(idx);
          indexMaxPtJet = idx;
        }
      }
    }

    for(auto const jetIdx : jetIndices){
      H1(dirPrefix+fhData.jetCollection+catLabel+"_pt")->Fill(v_pt->at(jetIdx));
      H1(dirPrefix+fhData.jetCollection+catLabel+"_eta")->Fill(v_eta->at(jetIdx));
      H2(dirPrefix+fhData.jetCollection+catLabel+"_eta__vs__pt")->Fill(v_eta->at(jetIdx), v_pt->at(jetIdx));
      H1(dirPrefix+fhData.jetCollection+catLabel+"_phi")->Fill(v_phi->at(jetIdx));
      H1(dirPrefix+fhData.jetCollection+catLabel+"_mass")->Fill(v_mass->at(jetIdx));

      if(v_numberOfDaughters){
        H1(dirPrefix+fhData.jetCollection+catLabel+"_numberOfDaughters")->Fill(v_numberOfDaughters->at(jetIdx));
      }
    }

    H1(dirPrefix+fhData.jetCollection+catLabel+"_njets")->Fill(0.01 + jetIndices.size());

    if(indexMaxPtJet >= 0){
      H1(dirPrefix+fhData.jetCollection+catLabel+"_pt0")->Fill(v_pt->at(indexMaxPtJet));
    }
  }

  for(auto const& fhDataMatch : fhData.matches){

    auto const matchLabel(fhDataMatch.label);
    auto const matchJetColl(fhDataMatch.jetCollection);
    auto const matchJetPtMin(fhDataMatch.jetPtMin);
    auto const matchJetDeltaRMin(fhDataMatch.jetDeltaRMin);

    auto const* v_match_pt(this->vector_ptr<float>(matchJetColl+"_pt"));
    auto const* v_match_eta(this->vector_ptr<float>(matchJetColl+"_eta"));
    auto const* v_match_phi(this->vector_ptr<float>(matchJetColl+"_phi"));
    auto const* v_match_mass(this->vector_ptr<float>(matchJetColl+"_mass"));

    if(not (v_match_pt and v_match_eta and v_match_phi and v_match_mass)){
      if(verbosity_ >= 0){
        std::cout << "JMETriggerAnalysisDriver::fillHistograms_Jets(\"" << dir << "\", const fillHistoDataJets&) -- "
                  << "branches not available (histograms will not be filled): "
                  << matchJetColl+"_pt/eta/phi/mass" << std::endl;
      }
      continue;
    }

    std::map<size_t, size_t> mapMatchIndeces;
    for(size_t idx=0; idx<v_pt->size(); ++idx){
      if(v_pt->at(idx) <= fhData.jetPtMin){ continue; }

      int indexBestMatch(-1);
      float dR2min(matchJetDeltaRMin * matchJetDeltaRMin);
      for(size_t idxMatch=0; idxMatch<v_match_pt->size(); ++idxMatch){
        if(v_match_pt->at(idxMatch) <= matchJetPtMin){ continue; }

        auto const dR2(utils::deltaR2(v_eta->at(idx), v_phi->at(idx), v_match_eta->at(idxMatch), v_match_phi->at(idxMatch)));
        if(dR2 < dR2min){
          dR2min = dR2;
          indexBestMatch = idxMatch;
        }
      }

      if(indexBestMatch >= 0){
        mapMatchIndeces.insert(std::make_pair(idx, indexBestMatch));
      }
    }

    for(auto const& catLabel : jetCategoryLabels_){

      std::vector<size_t> jetIndices;
      jetIndices.reserve(v_pt->size());
      for(size_t idx=0; idx<v_pt->size(); ++idx){
        if(v_pt->at(idx) <= fhData.jetPtMin){ continue; }

        if(jetBelongsToCategory(catLabel, v_pt->at(idx), std::abs(v_eta->at(idx)))){
          jetIndices.emplace_back(idx);
        }
      }

      size_t nJetsMatched(0), nJetsNotMatched(0);
      int indexMaxPtJetWithMatch(-1), indexMaxPtJetWithNoMatch(-1);
      float maxPtJetPtWithMatch(-1.), maxPtJetPtWithNoMatch(-1.);

      for(auto const jetIdx : jetIndices){

        auto const jetPt(v_pt->at(jetIdx));
        auto const jetEta(v_eta->at(jetIdx));
        auto const jetPhi(v_phi->at(jetIdx));
        auto const jetMass(v_mass->at(jetIdx));

        auto const hasMatch(mapMatchIndeces.find(jetIdx) != mapMatchIndeces.end());

        if(hasMatch){

          ++nJetsMatched;

          if((nJetsMatched == 1) or (jetPt > maxPtJetPtWithMatch)){
	    maxPtJetPtWithMatch = jetPt;
            indexMaxPtJetWithMatch = jetIdx;
          }

          H1(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_pt")->Fill(jetPt);
          H1(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_eta")->Fill(jetEta);
          H2(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_eta__vs__pt")->Fill(jetEta, jetPt);
          H1(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_phi")->Fill(jetPhi);
          H1(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_mass")->Fill(jetMass);

          if(v_numberOfDaughters){
            H1(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_numberOfDaughters")->Fill(v_numberOfDaughters->at(jetIdx));
          }

          auto const jetMatchIdx(mapMatchIndeces.at(jetIdx));
          auto const jetMatchPt(v_match_pt->at(jetMatchIdx));
          auto const jetMatchEta(v_match_eta->at(jetMatchIdx));
          auto const jetMatchPhi(v_match_phi->at(jetMatchIdx));
          auto const jetMatchMass(v_match_mass->at(jetMatchIdx));

          H2(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_pt__vs__"+matchLabel+"_pt")->Fill(jetPt, jetMatchPt);
          H2(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_eta__vs__"+matchLabel+"_eta")->Fill(jetEta, jetMatchEta);

          auto const dR2match(utils::deltaR2(jetEta, jetPhi, jetMatchEta, jetMatchPhi));
          H1(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_dRmatch")->Fill(sqrt(dR2match));

          if(jetMatchPt != 0.){
            auto const jetPtRatio(jetPt / jetMatchPt);
            H1(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_pt_over"+matchLabel)->Fill(jetPtRatio);
            H2(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_pt")->Fill(jetPtRatio, jetMatchPt);
            H2(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_eta")->Fill(jetPtRatio, jetMatchEta);
          }

          if(jetMatchMass != 0.){
            auto const jetMassRatio(jetMass / jetMatchMass);
            H1(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_mass_over"+matchLabel)->Fill(jetMassRatio);
            H2(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_mass_over"+matchLabel+"__vs__"+matchLabel+"_pt")->Fill(jetMassRatio, jetMatchMass);
            H2(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_mass_over"+matchLabel+"__vs__"+matchLabel+"_eta")->Fill(jetMassRatio, jetMatchEta);
            H2(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_mass_over"+matchLabel+"__vs__"+matchLabel+"_mass")->Fill(jetMassRatio, jetMatchMass);
          }
        }
        else {

          ++nJetsNotMatched;

          if((nJetsNotMatched == 1) or (jetPt > maxPtJetPtWithNoMatch)){
	    maxPtJetPtWithNoMatch = jetPt;
            indexMaxPtJetWithNoMatch = jetIdx;
          }

          H1(dirPrefix+fhData.jetCollection+catLabel+"_NotMatchedTo"+matchLabel+"_pt")->Fill(jetPt);
          H1(dirPrefix+fhData.jetCollection+catLabel+"_NotMatchedTo"+matchLabel+"_eta")->Fill(jetEta);
          H2(dirPrefix+fhData.jetCollection+catLabel+"_NotMatchedTo"+matchLabel+"_eta__vs__pt")->Fill(jetEta, jetPt);
          H1(dirPrefix+fhData.jetCollection+catLabel+"_NotMatchedTo"+matchLabel+"_phi")->Fill(jetPhi);
          H1(dirPrefix+fhData.jetCollection+catLabel+"_NotMatchedTo"+matchLabel+"_mass")->Fill(jetMass);

          if(v_numberOfDaughters){
            H1(dirPrefix+fhData.jetCollection+catLabel+"_NotMatchedTo"+matchLabel+"_numberOfDaughters")->Fill(v_numberOfDaughters->at(jetIdx));
          }
        }
      }

      H1(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_njets")->Fill(0.01 + nJetsMatched);
      H1(dirPrefix+fhData.jetCollection+catLabel+"_NotMatchedTo"+matchLabel+"_njets")->Fill(0.01 + nJetsNotMatched);

      if(indexMaxPtJetWithMatch >= 0){
        auto const maxPtJetPt(v_pt->at(indexMaxPtJetWithMatch));
        auto const maxPtJetMatchPt(v_match_pt->at(mapMatchIndeces.at(indexMaxPtJetWithMatch)));
        auto const maxPtJetMatchEta(v_match_eta->at(mapMatchIndeces.at(indexMaxPtJetWithMatch)));
        H1(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_pt0")->Fill(maxPtJetPt);
        H2(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_pt0__vs__"+matchLabel+"_pt")->Fill(maxPtJetPt, maxPtJetMatchPt);
        H2(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_pt0__vs__"+matchLabel+"_eta")->Fill(maxPtJetPt, maxPtJetMatchEta);
        if(maxPtJetMatchPt != 0.){
          auto const maxPtJetPtRatio(maxPtJetPt / maxPtJetMatchPt);
          H1(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_pt0_over"+matchLabel)->Fill(maxPtJetPtRatio);
          H2(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_pt0_over"+matchLabel+"__vs__"+matchLabel+"_pt")->Fill(maxPtJetPtRatio, maxPtJetMatchPt);
          H2(dirPrefix+fhData.jetCollection+catLabel+"_MatchedTo"+matchLabel+"_pt0_over"+matchLabel+"__vs__"+matchLabel+"_eta")->Fill(maxPtJetPtRatio, maxPtJetMatchEta);
        }
      }

      if(indexMaxPtJetWithNoMatch >= 0){
        auto const maxPtJetPt(v_pt->at(indexMaxPtJetWithNoMatch));
        H1(dirPrefix+fhData.jetCollection+catLabel+"_NotMatchedTo"+matchLabel+"_pt0")->Fill(maxPtJetPt);
      }
    }
  }
}

void JMETriggerAnalysisDriver::fillHistograms_MET(const std::string& dir, const fillHistoDataMET& fhData){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  auto const* v_pt(this->vector_ptr<float>(fhData.metCollection+"_pt"));
  auto const* v_phi(this->vector_ptr<float>(fhData.metCollection+"_phi"));
  auto const* v_sumEt(this->vector_ptr<float>(fhData.metCollection+"_sumEt"));

  if(not (v_pt and v_phi and v_sumEt)){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriver::fillHistograms_MET(\"" << dir << "\", const fillHistoDataMET&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData.metCollection+"_pt/phi/sumEt" << std::endl;
    }
    return;
  }

  if(not ((v_pt->size() == 1) and (v_phi->size() == 1) and (v_sumEt->size() == 1))){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriver::fillHistograms_MET(\"" << dir << "\", const fillHistoDataMET&) -- "
                << "MET branches have invalid size (histograms will not be filled): "
                << fhData.metCollection+"_pt/phi/sumEt" << std::endl;
    }
    return;
  }

  auto const metPt(v_pt->at(0));
  auto const metPhi(v_phi->at(0));
  auto const metSumEt(v_sumEt->at(0));

  H1(dirPrefix+fhData.metCollection+"_pt")->Fill(metPt);
  H1(dirPrefix+fhData.metCollection+"_phi")->Fill(metPhi);
  H1(dirPrefix+fhData.metCollection+"_sumEt")->Fill(metSumEt);

  for(auto const& fhDataMatch : fhData.matches){

    auto const matchLabel(fhDataMatch.label);
    auto const matchMetColl(fhDataMatch.metCollection);

    auto const* v_match_pt(this->vector_ptr<float>(matchMetColl+"_pt"));
    auto const* v_match_phi(this->vector_ptr<float>(matchMetColl+"_phi"));
    auto const* v_match_sumEt(this->vector_ptr<float>(matchMetColl+"_sumEt"));

    if(not (v_match_pt and v_match_phi and v_match_sumEt)){
      if(verbosity_ >= 0){
        std::cout << "JMETriggerAnalysisDriver::fillHistograms_MET(\"" << dir << "\", const fillHistoDataMET&) -- "
                  << "branches not available (histograms will not be filled): "
                  << matchMetColl+"_pt/phi/sumEt" << std::endl;
      }
      continue;
    }

    if(not ((v_match_pt->size() == 1) and (v_match_phi->size() == 1) and (v_match_sumEt->size() == 1))){
      if(verbosity_ >= 0){
        std::cout << "JMETriggerAnalysisDriver::fillHistograms_MET(\"" << dir << "\", const fillHistoDataMET&) -- "
                  << "MET branches have invalid size (histograms will not be filled): "
                  << matchMetColl+"_pt/phi/sumEt" << std::endl;
      }
      continue;
    }

    auto const metMatchPt(v_match_pt->at(0));
    auto const metMatchPhi(v_match_phi->at(0));
    auto const metMatchSumEt(v_match_sumEt->at(0));

    if(metMatchPt != 0.){
      auto const metPtRatio(metPt / metMatchPt);
      H2(dirPrefix+fhData.metCollection+"_pt__vs__"+matchLabel+"_pt")->Fill(metPt, metMatchPt);
      H1(dirPrefix+fhData.metCollection+"_pt_over"+matchLabel)->Fill(metPtRatio);
      H2(dirPrefix+fhData.metCollection+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_pt")->Fill(metPtRatio, metMatchPt);
      H2(dirPrefix+fhData.metCollection+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_phi")->Fill(metPtRatio, metMatchPhi);
      H2(dirPrefix+fhData.metCollection+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_sumEt")->Fill(metPtRatio, metMatchSumEt);
    }

    if(metMatchSumEt != 0.){
      auto const metSumEtRatio(metSumEt / metMatchSumEt);
      H2(dirPrefix+fhData.metCollection+"_sumEt__vs__"+matchLabel+"_sumEt")->Fill(metSumEt, metMatchSumEt);
      H1(dirPrefix+fhData.metCollection+"_sumEt_over"+matchLabel)->Fill(metSumEtRatio);
      H2(dirPrefix+fhData.metCollection+"_sumEt_over"+matchLabel+"__vs__"+matchLabel+"_pt")->Fill(metSumEtRatio, metMatchPt);
      H2(dirPrefix+fhData.metCollection+"_sumEt_over"+matchLabel+"__vs__"+matchLabel+"_phi")->Fill(metSumEtRatio, metMatchPhi);
      H2(dirPrefix+fhData.metCollection+"_sumEt_over"+matchLabel+"__vs__"+matchLabel+"_sumEt")->Fill(metSumEtRatio, metMatchSumEt);
    }

    auto const metDeltaPhiMatch(utils::deltaPhi(metPhi, metMatchPhi));
    H2(dirPrefix+fhData.metCollection+"_phi__vs__"+matchLabel+"_phi")->Fill(metPhi, metMatchPhi);
    H1(dirPrefix+fhData.metCollection+"_deltaPhi"+matchLabel)->Fill(metDeltaPhiMatch);
    H2(dirPrefix+fhData.metCollection+"_deltaPhi"+matchLabel+"__vs__"+matchLabel+"_pt")->Fill(metDeltaPhiMatch, metMatchPt);
    H2(dirPrefix+fhData.metCollection+"_deltaPhi"+matchLabel+"__vs__"+matchLabel+"_phi")->Fill(metDeltaPhiMatch, metMatchPhi);
    H2(dirPrefix+fhData.metCollection+"_deltaPhi"+matchLabel+"__vs__"+matchLabel+"_sumEt")->Fill(metDeltaPhiMatch, metMatchSumEt);

    auto const metParaToMatch(metPt*(std::cos(metPhi)*std::cos(metMatchPhi) + std::sin(metPhi)*std::sin(metMatchPhi)));
    H1(dirPrefix+fhData.metCollection+"_pt_paraTo"+matchLabel)->Fill(metParaToMatch);
    H2(dirPrefix+fhData.metCollection+"_pt_paraTo"+matchLabel+"__vs__"+matchLabel+"_pt")->Fill(metParaToMatch, metMatchPt);
    H2(dirPrefix+fhData.metCollection+"_pt_paraTo"+matchLabel+"__vs__"+matchLabel+"_phi")->Fill(metParaToMatch, metMatchPhi);
    H2(dirPrefix+fhData.metCollection+"_pt_paraTo"+matchLabel+"__vs__"+matchLabel+"_sumEt")->Fill(metParaToMatch, metMatchSumEt);

    auto const metParaToMatchMinusMatch(metParaToMatch - metMatchPt);
    H1(dirPrefix+fhData.metCollection+"_pt_paraTo"+matchLabel+"Minus"+matchLabel)->Fill(metParaToMatchMinusMatch);
    H2(dirPrefix+fhData.metCollection+"_pt_paraTo"+matchLabel+"Minus"+matchLabel+"__vs__"+matchLabel+"_pt")->Fill(metParaToMatchMinusMatch, metMatchPt);
    H2(dirPrefix+fhData.metCollection+"_pt_paraTo"+matchLabel+"Minus"+matchLabel+"__vs__"+matchLabel+"_phi")->Fill(metParaToMatchMinusMatch, metMatchPhi);
    H2(dirPrefix+fhData.metCollection+"_pt_paraTo"+matchLabel+"Minus"+matchLabel+"__vs__"+matchLabel+"_sumEt")->Fill(metParaToMatchMinusMatch, metMatchSumEt);

    auto const metPerpToMatch(metPt*(std::cos(metPhi)*std::sin(metMatchPhi) - std::sin(metPhi)*std::cos(metMatchPhi)));
    H1(dirPrefix+fhData.metCollection+"_pt_perpTo"+matchLabel)->Fill(metPerpToMatch);
    H2(dirPrefix+fhData.metCollection+"_pt_perpTo"+matchLabel+"__vs__"+matchLabel+"_pt")->Fill(metPerpToMatch, metMatchPt);
    H2(dirPrefix+fhData.metCollection+"_pt_perpTo"+matchLabel+"__vs__"+matchLabel+"_phi")->Fill(metPerpToMatch, metMatchPhi);
    H2(dirPrefix+fhData.metCollection+"_pt_perpTo"+matchLabel+"__vs__"+matchLabel+"_sumEt")->Fill(metPerpToMatch, metMatchSumEt);
  }
}
