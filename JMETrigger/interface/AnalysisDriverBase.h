#ifndef Analysis_JMETrigger_AnalysisDriverBase_h
#define Analysis_JMETrigger_AnalysisDriverBase_h

#include <map>
#include <memory>
#include <string>
#include <vector>
#include <sstream>
#include <stdexcept>
#include <typeinfo>
#include <TFile.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>

class AnalysisDriverBase {

 public:
  explicit AnalysisDriverBase(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath="", const std::string& outputFileMode="recreate");
  virtual ~AnalysisDriverBase();

  virtual void init() = 0;
  virtual void analyze() = 0;
  virtual void write(TFile&) = 0;

  virtual void process(const Long64_t firstEntry=0, const Long64_t maxEntries=-1);
  virtual void writeToFile(const std::string& output_file, const std::string& output_mode);

  void setOutputFilePath(const std::string& foo){ outputFilePath_ = foo; }
  void setOutputFileMode(const std::string& foo){ outputFileMode_ = foo; }

  virtual void addOption(const std::string& key, const std::string& opt);
  virtual bool hasOption(const std::string& key) const { return (map_options_.find(key) != map_options_.end()); }
  virtual std::string const& getOption(const std::string& key) const;

  bool find(const std::string& key) const;

  template<class T> T const* value_ptr(const std::string& key) const;
  template<class T> T const& value(const std::string& key) const;

  template<class T> std::vector<T> const* vector_ptr(const std::string& key) const;
  template<class T> std::vector<T> const& vector(const std::string& key) const;

 protected:
  std::unique_ptr<TFile> theFile_;
  std::unique_ptr<TTreeReader> theReader_;
  std::string outputFilePath_;
  std::string outputFileMode_;

  std::map<std::string, std::unique_ptr<ROOT::Internal::TTreeReaderValueBase>> map_TTreeReaderValues_;
  std::map<std::string, std::string> map_options_;
};

template<class T>
T const* AnalysisDriverBase::value_ptr(const std::string& key) const {

  if(not this->find(key)){
    return nullptr;
  }

  auto* ptr(dynamic_cast<TTreeReaderValue<T>*>(map_TTreeReaderValues_.at(key).get()));

  if(not ptr){
    return nullptr;
  }

  return ptr->Get();
}

template<class T>
T const& AnalysisDriverBase::value(const std::string& key) const {

  auto const* ptr(this->value_ptr<T>(key));

  if(not ptr){
    std::ostringstream ss_str;
    ss_str << "value -- dynamic_cast to \"TTreeReaderValue<" << typeid(T).name() << ">*\" failed for key \"" << key << "\".";
    throw std::runtime_error(ss_str.str());
  }

  return *(ptr->Get());
}

template<class T>
std::vector<T> const* AnalysisDriverBase::vector_ptr(const std::string& key) const {

  if(not this->find(key)){
    return nullptr;
  }

  auto* ptr(dynamic_cast<TTreeReaderValue<std::vector<T>>*>(map_TTreeReaderValues_.at(key).get()));

  if(not ptr){
    return nullptr;
  }

  return ptr->Get();
}

template<class T>
std::vector<T> const& AnalysisDriverBase::vector(const std::string& key) const {

  auto const* ptr(this->vector_ptr<T>(key));

  if(not ptr){
    std::ostringstream ss_str;
    ss_str << "vector -- dynamic_cast to \"TTreeReaderValue<std::vector<" << typeid(T).name() << ">>*\" failed for key \"" << key << "\".";
    throw std::runtime_error(ss_str.str());
  }

  return *ptr;
}

#endif
