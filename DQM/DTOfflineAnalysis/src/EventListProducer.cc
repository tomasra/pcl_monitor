

// system include files
#include <memory>


#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "AnalysisDataFormats/SimpleEvent/interface/SimpleEvent.h"
#include "DQM/DTOfflineAnalysis/src/EventListProducer.h"

#include <iostream>

using namespace std;


EventListProducer::EventListProducer(const edm::ParameterSet& iConfig):
  _sec(new SimpleEventCollection())
{

  maxDistance = iConfig.getUntrackedParameter<unsigned int>("maxDistance", 10);

   //register your products

  produces<SimpleEventCollection,edm::InRun>("All");

   //now do what ever other initialization is needed
  
}


EventListProducer::~EventListProducer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
EventListProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   
   SimpleEvent se(iEvent.id().event(),iEvent.orbitNumber(),iEvent.bunchCrossing());

   if(se.evtDist(previousEvent) == 1 && se.bxDist(previousEvent) < maxDistance) {
     if(_sec->size() == 0) _sec->push_back(previousEvent); 
     else if(_sec->back().eventId() != previousEvent.eventId()) _sec->push_back(previousEvent); 
     _sec->push_back(se);
     cout << "Evt pair #: " << previousEvent.eventId() << " and " << se.eventId()
	  << " dist BX: " << se.bxDist(previousEvent) << endl; 
   }




   previousEvent = se;
}

// ------------ method called once each job just before starting event loop  ------------
void 
EventListProducer::beginJob(const edm::EventSetup&)
{
}

void 
EventListProducer::endRun(edm::Run& iRun, const edm::EventSetup&) {
  cerr << "Collection of " << _sec->size() << " SimpleEvents ready to be saved" << endl;
  

  edm::LogInfo("SavingSimpleEvents") << " Collection of " << _sec->size() << " SimpleEvents ready to be saved";
  cout << "D1" << endl;
  iRun.put(_sec, "All");
  cout << "D2" << endl;


}

// ------------ method called once each job just after ending the event loop  ------------
void 
EventListProducer::endJob() {
}

