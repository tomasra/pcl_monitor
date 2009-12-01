//
// Original Author:  Marco Zanetti
//         Created:  Tue Sep  9 15:56:24 CEST 2008


// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"


#include <vector>
#include <string>

class TriggerPathFilter : public edm::EDFilter {
public:

  explicit TriggerPathFilter(const edm::ParameterSet&);

  ~TriggerPathFilter();
  
private:
  virtual void beginJob(const edm::EventSetup&) ;

  virtual bool filter(edm::Event&, const edm::EventSetup&);

  virtual void endJob() ;
  
  edm::InputTag triggerResultsLabel;
  edm::InputTag l1DataLabel;
  std::vector<int> l1Bits;
  std::vector<std::string> hltBits;
  int resultDefinition;

  bool debug;

};

