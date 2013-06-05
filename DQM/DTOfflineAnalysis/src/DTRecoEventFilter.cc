/*
 *  See header file for a description of this class.
 *
 *  $Date: 2008/12/03 10:41:13 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "DQM/DTOfflineAnalysis/src/DTRecoEventFilter.h"
#include "DataFormats/DTRecHit/interface/DTRecSegment4DCollection.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include <DataFormats/DTDigi/interface/DTDigiCollection.h>

#include <iostream>

using namespace std;
using namespace edm;

DTRecoEventFilter::DTRecoEventFilter(const edm::ParameterSet& pset) : HLTFilter(pset){
  // the name of the 4D rec hits collection
  theDigiLabel =  pset.getParameter<InputTag>("dtDigiLabel");

  theRecHits4DLabel = pset.getParameter<string>("recHits4DLabel");
  LogVerbatim("DTRecoEventFilter") << "[DTRecoEventFilter] constructor called" << endl;

}

DTRecoEventFilter::~DTRecoEventFilter(){}


bool DTRecoEventFilter::filter(edm::Event& event, const edm::EventSetup& setup) {
  LogVerbatim("DTRecoEventFilter") << "[DTRecoEventFilter] filter" << endl;

  map<DTChamberId, int> nDigisPerChamber;

  // Digi collection
  edm::Handle<DTDigiCollection> dtdigis;
  event.getByLabel(theDigiLabel, dtdigis);

  DTDigiCollection::DigiRangeIterator dtLayerId_It;
  for (dtLayerId_It=dtdigis->begin(); dtLayerId_It!=dtdigis->end(); ++dtLayerId_It) { // Loop over layers
    DTChamberId chId = ((*dtLayerId_It).first).chamberId();
    int nDigisPerLayer = 0;
    
    nDigisPerLayer += distance(((*dtLayerId_It).second).first, ((*dtLayerId_It).second).second);
    nDigisPerChamber[chId] += nDigisPerLayer;

  }

  for(map<DTChamberId, int>::const_iterator nDigisCh = nDigisPerChamber.begin();
      nDigisCh != nDigisPerChamber.end(); ++nDigisCh) {
    DTChamberId chId = (*nDigisCh).first;
    int num = (*nDigisCh).second;
    if(num > 20) {
      cout << " event accepted, chamber: " << chId << " has: " << num << " digis" << endl;
      return true;
    }
  }

  return false;
//   edm::Handle<DTRecSegment4DCollection> all4DSegments;
//   event.getByLabel(theRecHits4DLabel, all4DSegments);
//   LogVerbatim("DTRecoEventFilter") << "[DTRecoEventFilter] 4D RecHit collection size: " << all4DSegments->size() << endl;
//   if(all4DSegments->size() == 0) return false;

//   return true;
}
