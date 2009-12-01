//
// Original Author:  Marco Zanetti
//         Created:  Tue Sep  9 15:56:24 CEST 2008


// system include files
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include <vector>

class TFile;
class TH1F;

class BxNumberFilter : public edm::EDFilter {
public:
  explicit BxNumberFilter(const edm::ParameterSet&);
  ~BxNumberFilter();
  
private:
  virtual void beginJob(const edm::EventSetup&) ;
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  
  edm::InputTag inputLabel;
  std::vector<int> goldenBXIds;
  unsigned int range; 
  bool debug;
   
  TFile *theRootFile;
  TH1F *bxDistr;


};
