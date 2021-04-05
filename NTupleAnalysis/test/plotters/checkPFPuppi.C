{
  TFile* f0 = TFile::Open("out_HLT_Run3TRK.root");
  TFile* f1 = TFile::Open("out_HLT_Run3TRKWithPU.root");

  TTree* t0 = (TTree*) f0->Get("JMETriggerNTuple/Events");
  TTree* t1 = (TTree*) f1->Get("JMETriggerNTuple/Events");

  t0->SetLineColor(1);
  t0->SetLineWidth(2);

  t1->SetLineColor(2);
  t1->SetLineWidth(2);

  t0->AddFriend(t1, "t1");

//  t0->Scan("hltParticleFlow_pdgId:hltParticleFlow_pt:hltParticleFlow_eta:hltParticleFlow_phi:hltPFPuppi_pt/hltParticleFlow_pt:t1.hltPFPuppi_pt/t1.hltParticleFlow_pt");
}
