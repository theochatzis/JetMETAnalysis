#include <Analysis/JMETrigger/interface/Utils.h>
#include <math.h>

std::vector<std::string> utils::stringTokens(const std::string& str, const std::string& delimiter){

  std::vector<std::string> toks;

  std::size_t last(0), next(0);
  while((next = str.find(delimiter, last)) != std::string::npos){
    std::string substr = str.substr(last, next-last);
    if(substr != "") toks.emplace_back(substr);
    last = next + delimiter.size();
  }

  if(str.substr(last) != ""){
    toks.emplace_back(str.substr(last));
  }

  return toks;
}

float utils::deltaPhi2(const float phi1, const float phi2){
  auto dphi(std::abs(phi1 - phi2));
  if(dphi > M_PI) dphi -= 2*M_PI;
  return dphi * dphi;
}

float utils::deltaR2(const float eta1, const float phi1, const float eta2, const float phi2){
  return (eta1 - eta2) * (eta1 - eta2) + deltaPhi2(phi1, phi2);
}
