#ifndef NTupleAnalysis_JMETrigger_Utils_h
#define NTupleAnalysis_JMETrigger_Utils_h

#include <string>
#include <vector>

namespace utils {

  std::vector<std::string> stringTokens(const std::string&, const std::string&);
  float deltaPhi2(const float phi1, const float phi2);
  float deltaR2(const float eta1, const float phi1, const float eta2, const float phi2);
}

#endif
