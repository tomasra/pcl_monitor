#ifndef TriggerSourceFilter_H
#define TriggerSourceFilter_H

/** \class TriggerSourceFilter
 *  No description available.
 *
 *  $Date: 2008/12/03 10:41:14 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

// system include files
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"


class TriggerSourceFilter : public edm::EDFilter {
public:
  explicit TriggerSourceFilter(const edm::ParameterSet&);
  ~TriggerSourceFilter();
  
private:
  virtual void beginJob(const edm::EventSetup&) ;
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
//   virtual bool beginRun(edm::Run& run,  const edm::EventSetup& es );

  edm::InputTag gmtInputTag;
  bool debug;
  int triggerSource;

  int allEvents;
  int keptEvents;
};

#endif
