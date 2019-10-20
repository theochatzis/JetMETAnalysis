#ifndef JMETriggerAnalysis_PATMuonCollectionContainer_h
#define JMETriggerAnalysis_PATMuonCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VCollectionContainer.h>
#include <DataFormats/PatCandidates/interface/Muon.h>

#include <vector>

class PATMuonCollectionContainer : public VCollectionContainer<pat::MuonCollection> {

 public:
  explicit PATMuonCollectionContainer(const std::string&, const std::string&, const edm::EDGetToken&);
  virtual ~PATMuonCollectionContainer() {}

  void clear();
  void fill(const pat::MuonCollection&, const bool clear_before_filling=true);

  void orderByHighestPt(const bool foo){ orderByHighestPt_ = foo; }

  std::vector<int>& vec_pdgId(){ return pdgId_; }
  std::vector<float>& vec_pt(){ return pt_; }
  std::vector<float>& vec_eta(){ return eta_; }
  std::vector<float>& vec_phi(){ return phi_; }
  std::vector<float>& vec_mass(){ return mass_; }
  std::vector<float>& vec_vx(){ return vx_; }
  std::vector<float>& vec_vy(){ return vy_; }
  std::vector<float>& vec_vz(){ return vz_; }
  std::vector<float>& vec_dxyPV(){ return dxyPV_; }
  std::vector<float>& vec_dzPV(){ return dzPV_; }
  std::vector<uint>& vec_id(){ return id_; }
  std::vector<float>& vec_pfIso(){ return pfIso_; }

 protected:
  bool orderByHighestPt_;

  // vector of indeces (used for ordering)
  std::vector<size_t> idxs_;

  std::vector<int> pdgId_;
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;
  std::vector<float> vx_;
  std::vector<float> vy_;
  std::vector<float> vz_;
  std::vector<float> dxyPV_;
  std::vector<float> dzPV_;
  std::vector<uint> id_;
  std::vector<float> pfIso_;
};

#endif
