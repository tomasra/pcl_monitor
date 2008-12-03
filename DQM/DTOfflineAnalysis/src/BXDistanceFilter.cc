//
// Original Author:  Marco Zanetti
//         Created:  Tue Sep  9 15:56:24 CEST 2008


#include "DQM/DTOfflineAnalysis/src/BXDistanceFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "EventFilter/Utilities/interface/GlobalEventNumber.h"
#include <DataFormats/FEDRawData/interface/FEDRawDataCollection.h>

#include "TH1F.h"
#include "TFile.h"


// user include files
using namespace edm;
using namespace std;


BXDistanceFilter::BXDistanceFilter(const edm::ParameterSet& iConfig) : previousOrbit(0),
								       previousBX(0) {
  cout << "[BXDistanceFilter] contructor called" << endl;
  inputLabel = iConfig.getUntrackedParameter<edm::InputTag>("inputLabel",edm::InputTag("source"));
  maxDistance = iConfig.getUntrackedParameter<unsigned int>("maxDistance", 10);
  debug = iConfig.getUntrackedParameter<unsigned int>("debug", false);
}


BXDistanceFilter::~BXDistanceFilter() { }


bool BXDistanceFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {

//   if(eventMap.size() == 0) {
//     Run& run = iEvent.getRun();
//     edm::Handle<SimpleEventCollection> seListHandle;
//     run.getByLabel("eventListProducer", seListHandle);
  
//     SimpleEventCollection seList = *seListHandle;

//     cout << "-------------------------------------------------------------------" << endl;
//     cout << "---- Close trigger event list:" << endl;
//     for(vector<SimpleEvent>::const_iterator evt = seList.begin();
// 	evt != seList.end(); ++evt) {
//       eventMap[(*evt).eventId()] = *evt; 
//       cout << "  Event: " << (*evt).eventId() << endl;
//     }
//     cout << "-------------------------------------------------------------------" << endl;

//   }


   bool result = false;

   if(eventMap.find(iEvent.id().event()) != eventMap.end()) {
     result = true;
     cout << "[BXDistanceFilter] event: " << iEvent.id().event() << " has been kept!" << endl;
   }

   return result;
}




// ------------ method called once each job just before starting event loop  ------------
void  BXDistanceFilter::beginJob(const edm::EventSetup&) {
  cout << "[BXDistanceFilter] beginJob" << endl;

  theRootFile = new TFile("BXDistr.root","RECREATE");
  theRootFile->cd();
  bxDistr = new TH1F("bxDistr", "bxDistr",4000,0,4000);
  hAllBxDistance = new TH1F("hAllBxDistance", "Dist BX all triggers", 5000, 0, 5000);

}


// ------------ method called once each job just after ending the event loop  ------------
void  BXDistanceFilter::endJob() {
  theRootFile->cd();
  bxDistr->Write();
  hAllBxDistance->Write();
  theRootFile->Close();

}


bool BXDistanceFilter::beginRun(edm::Run& run,  const edm::EventSetup& es ) {
  cout << "[BXDistanceFilter] beginRun" << endl;
  
  edm::Handle<SimpleEventCollection> seListHandle;
  run.getByLabel("eventListProducer", seListHandle);
  
  SimpleEventCollection seList = *seListHandle;

  cout << "-------------------------------------------------------------------" << endl;
  cout << "---- Close trigger event list:" << endl;
  for(vector<SimpleEvent>::const_iterator evt = seList.begin();
      evt != seList.end(); ++evt) {
    eventMap[(*evt).eventId()] = *evt; 
    cout << "  Event: " << (*evt).eventId() << endl;
  }
  cout << "-------------------------------------------------------------------" << endl;
  
  return true;
}
