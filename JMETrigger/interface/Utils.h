#ifndef NTupleAnalysis_JMETrigger_Utils_h
#define NTupleAnalysis_JMETrigger_Utils_h

#include <string>
#include <vector>

namespace utils {

  float deltaPhi(const float phi1, const float phi2);
  float deltaR2(const float eta1, const float phi1, const float eta2, const float phi2);

  std::vector<std::string> stringTokens(const std::string&, const std::string&);
  bool stringStartsWith(const std::string& str, const std::string& substr);
  bool stringEndsWith(const std::string& str, const std::string& substr);
}

#endif
