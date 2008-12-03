//
// Original Author:  Marco Zanetti
//         Created:  Tue Sep  9 15:56:24 CEST 2008


// system include files
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "AnalysisDataFormats/SimpleEvent/interface/SimpleEvent.h"

#include <vector>
#include <map>

class TFile;
class TH1F;

class BXDistanceFilter : public edm::EDFilter {
public:
  explicit BXDistanceFilter(const edm::ParameterSet&);
  ~BXDistanceFilter();
  
private:
  virtual void beginJob(const edm::EventSetup&) ;
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  virtual bool beginRun(edm::Run& run,  const edm::EventSetup& es );

  edm::InputTag inputLabel;
  unsigned int maxDistance; 
  bool debug;
  int previousOrbit;
  int previousBX;

   
  TFile *theRootFile;
  TH1F *bxDistr;
  TH1F *hAllBxDistance;

  std::map<int, SimpleEvent> eventMap;

};
