#ifndef EventListProducer_H
#define EventListProducer_H

/** \class EventListProducer
 *  No description available.
 *
 *  $Date: 2008/12/03 10:41:13 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "AnalysisDataFormats/SimpleEvent/interface/SimpleEvent.h"


class EventListProducer : public edm::EDProducer {
   public:
      explicit EventListProducer(const edm::ParameterSet&);
      ~EventListProducer();

private:
  virtual void beginJob(const edm::EventSetup&) ;
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endRun(edm::Run&, const edm::EventSetup&);
  virtual void endJob() ;
      
      // ----------member data ---------------------------


  std::auto_ptr<SimpleEventCollection> _sec;
//   std::auto_ptr<SimpleEventCollection> _secFirst;

  SimpleEvent previousEvent;
  int maxDistance; 
};



#endif


