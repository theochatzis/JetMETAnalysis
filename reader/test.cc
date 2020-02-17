#include <iostream>
#include <map>
#include <memory>
#include <chrono>
#include <string>
#include <vector>
#include <sstream>
#include <stdexcept>
#include <typeinfo>
#include <TFile.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TH1D.h>
#include <TH2D.h>

class AnalysisDriver {

 public:
  AnalysisDriver(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath="", const std::string& outputFileMode="recreate")
    : theFile(tfile.c_str()), theReader(ttree.c_str(), &theFile), outputFilePath_(outputFilePath), outputFileMode_(outputFileMode) {
    map_TTreeReaderValues_.clear();
    auto iter = theReader.GetTree()->GetIteratorOnAllLeaves();
    TLeaf* leaf(nullptr);
    while(leaf = (TLeaf*) iter->Next()){
      const std::string type(leaf->GetTypeName());
      if(type == "UInt_t"){
        map_TTreeReaderValues_.insert(std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<unsigned int>>(theReader, leaf->GetName())));
      }
      else if(type == "Int_t"){
        map_TTreeReaderValues_.insert(std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<int>>(theReader, leaf->GetName())));
      }
      else if(type == "Long64_t"){
        map_TTreeReaderValues_.insert(std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<long long>>(theReader, leaf->GetName())));
      }
      else if(type == "ULong64_t"){
        map_TTreeReaderValues_.insert(std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<unsigned long long>>(theReader, leaf->GetName())));
      }
      else if(type == "vector<bool>"){
        map_TTreeReaderValues_.insert(std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<std::vector<bool>>>(theReader, leaf->GetName())));
      }
      else if(type == "vector<unsigned int>"){
        map_TTreeReaderValues_.insert(std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<std::vector<unsigned int>>>(theReader, leaf->GetName())));
      }
      else if(type == "vector<int>"){
        map_TTreeReaderValues_.insert(std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<std::vector<int>>>(theReader, leaf->GetName())));
      }
      else if(type == "vector<float>"){
        map_TTreeReaderValues_.insert(std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<std::vector<float>>>(theReader, leaf->GetName())));
      }
      else if(type == "vector<double>"){
        map_TTreeReaderValues_.insert(std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<std::vector<double>>>(theReader, leaf->GetName())));
      }
      else {
	std::ostringstream ss_str;
        ss_str << "invalid type for input TLeaf \"" << leaf->GetName() << "\": " << type;
        throw std::runtime_error(ss_str.str());
      }
    }
  }

  bool find(const std::string& key) const {

    return (map_TTreeReaderValues_.find(key) != map_TTreeReaderValues_.end());
  }

  template<class T>
  T const& value(const std::string& key) const {

    if(not this->find(key)){
      std::ostringstream ss_str;
      ss_str << "value -- invalid key (check if TLeaf/TBranch exists): " << key;
      throw std::runtime_error(ss_str.str());
    }

    if(dynamic_cast<TTreeReaderValue<T>*>(map_TTreeReaderValues_.at(key).get()) == nullptr){
      std::ostringstream ss_str;
      ss_str << "value -- dynamic_cast to \"TTreeReaderValue<" << typeid(T).name() << ">*\" failed for key \"" << key << "\".";
      throw std::runtime_error(ss_str.str());
    }

    return *(((TTreeReaderValue<T>*) map_TTreeReaderValues_.at(key).get())->Get());
  }

  template<class T>
  std::vector<T> const& vector(const std::string& key) const {

    if(not this->find(key)){
      std::ostringstream ss_str;
      ss_str << "vector -- invalid key (check if TLeaf/TBranch exists): " << key;
      throw std::runtime_error(ss_str.str());
    }

    if(dynamic_cast<TTreeReaderValue<std::vector<T>>*>(map_TTreeReaderValues_.at(key).get()) == nullptr){
      std::ostringstream ss_str;
      ss_str << "vector -- dynamic_cast to \"TTreeReaderValue<std::vector<" << typeid(T).name() << ">>*\" failed for key \"" << key << "\".";
      throw std::runtime_error(ss_str.str());
    }

    return *(((TTreeReaderValue<std::vector<T>>*) map_TTreeReaderValues_.at(key).get())->Get());
  }

  void process(const Long64_t firstEntry=0, const Long64_t maxEntries=-1){

    this->init();

    while(theReader.Next()){

      if(theReader.GetCurrentEntry() < firstEntry){ continue; }

      if(maxEntries == 0){
        break;
      }
      else if(maxEntries > 0){
        if(theReader.GetCurrentEntry() >= (firstEntry+maxEntries)){ continue; }
      }

      this->analyze();
    }

    if(outputFilePath_ != ""){
      this->writeToFile(outputFilePath_, outputFileMode_);
    }
  }

  void writeToFile(const std::string& output_file, const std::string& output_mode){

    TFile outFile(output_file.c_str(), output_mode.c_str());
    if(not outFile.IsZombie()){
      outFile.cd();
      this->write();
    }
    outFile.Close();
  }

  void init(){

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

  void analyze(){
    ++eventsProcessed_;
    h_eventsProcessed_->Fill(0.5, 1.);

    auto const& eta1 = this->vector<float>("hltAK4PFJetsCorrected_eta");
    for(const auto& tmp : eta1){ h_hltAK4PFJetsCorrected_eta_->Fill(tmp, 1.); }

    auto const& eta2 = this->vector<float>("hltAK4PFCHSJetsCorrected_eta");
    for(const auto& tmp : eta2){ h_hltAK4PFCHSJetsCorrected_eta_->Fill(tmp, 1.); }

    auto const& eta3 = this->vector<float>("hltAK4PuppiJetsCorrected_eta");
    for(const auto& tmp : eta3){ h_hltAK4PuppiJetsCorrected_eta_->Fill(tmp, 1.); }
  }

  void write(){

    h_eventsProcessed_->Write();
    h_hltAK4PFJetsCorrected_eta_->Write();
    h_hltAK4PFCHSJetsCorrected_eta_->Write();
    h_hltAK4PuppiJetsCorrected_eta_->Write();
  }

  void setOutputFilePath(const std::string& foo){ outputFilePath_ = foo; }
  void setOutputFileMode(const std::string& foo){ outputFileMode_ = foo; }

  void addOption(const std::string& key, const std::string& opt){

    if(map_options_.find(key) != map_options_.end()){
      std::cout << key << " " << opt << std::endl;
    }
    else {
      map_options_.insert(std::make_pair(key, opt));
    }
  }

  Long64_t eventsProcessed() const { return eventsProcessed_; }

  TFile theFile;
  TTreeReader theReader;
  std::string outputFilePath_;
  std::string outputFileMode_;

  Long64_t eventsProcessed_ = 0;
  std::unique_ptr<TH1D> h_eventsProcessed_;
  std::unique_ptr<TH1D> h_hltAK4PFJetsCorrected_eta_;
  std::unique_ptr<TH1D> h_hltAK4PFCHSJetsCorrected_eta_;
  std::unique_ptr<TH1D> h_hltAK4PuppiJetsCorrected_eta_;

  std::map<std::string, std::unique_ptr<ROOT::Internal::TTreeReaderValueBase>> map_TTreeReaderValues_;
  std::map<std::string, std::string> map_options_;
};

int main(){

  const auto start = std::chrono::high_resolution_clock::now();

  AnalysisDriver a("../ntuples_prod_v06/QCD_Pt_15to3000_Flat_14TeV_PU200.root", "JMETriggerNTuple/Events");
  a.setOutputFilePath("out.root");
  a.setOutputFileMode("recreate");
  a.addOption("a", "a");
  a.process(0, -1);

  const auto finish = std::chrono::high_resolution_clock::now();
  const auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(finish - start);
  std::cout << std::string(35, '-') << std::endl;
  std::cout << "events processed: " << a.eventsProcessed() << std::endl;
  std::cout << "execution time [msec]: " << duration.count() << std::endl;
  std::cout << std::string(35, '-') << std::endl;

  return 0;
}
