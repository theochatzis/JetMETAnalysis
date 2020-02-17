#include <iostream>
#include <chrono>
#include <string>

#include <Analysis/JMETrigger/interface/JMETriggerAnalysisDriver.h>

int main(){

  const auto start = std::chrono::high_resolution_clock::now();

  JMETriggerAnalysisDriver a("../ntuples_prod_v06/QCD_Pt_15to3000_Flat_14TeV_PU200.root", "JMETriggerNTuple/Events");
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
