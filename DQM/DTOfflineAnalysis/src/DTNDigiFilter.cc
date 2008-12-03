/*
 *  See header file for a description of this class.
 *
 *  $Date: 2008/10/27 16:25:25 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - INFN Torino
 */

#include "DQM/DTOfflineAnalysis/src/DTNDigiFilter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <DataFormats/DTDigi/interface/DTDigiCollection.h>

#include <iostream>

using namespace std;
using namespace edm;

DTNDigiFilter::DTNDigiFilter(const edm::ParameterSet& pset) :  allEvents(0),
							       keptEvents(0) {
  // the name of the 4D rec hits collection
  theDigiLabel =  pset.getParameter<InputTag>("dtDigiLabel");
  debug = pset.getUntrackedParameter<bool>("debug",false);

  threshold = pset.getUntrackedParameter<int>("threshold",10);
  // perChamber -> cut on # digis per chamber
  // global -> cut on total # of digis
  granularity = pset.getUntrackedParameter<string>("granularity","global");
  // moreThan -> require # digis > threshold
  // lessThan -> require # digis < threshold
  cutType =  pset.getUntrackedParameter<string>("cutType","lessThan");
}

DTNDigiFilter::~DTNDigiFilter(){}


bool DTNDigiFilter::filter(edm::Event& event, const edm::EventSetup& setup) {
  allEvents++;

  map<DTChamberId, int> nDigisPerChamber;

  // Digi collection
  edm::Handle<DTDigiCollection> dtdigis;
  event.getByLabel(theDigiLabel, dtdigis);

  int totalNDigis = 0;


  DTDigiCollection::DigiRangeIterator dtLayerId_It;
  for (dtLayerId_It=dtdigis->begin(); dtLayerId_It!=dtdigis->end(); ++dtLayerId_It) { // Loop over layers
    DTChamberId chId = ((*dtLayerId_It).first).chamberId();
    int nDigisPerLayer = 0;
    
    nDigisPerLayer += distance(((*dtLayerId_It).second).first, ((*dtLayerId_It).second).second);
    nDigisPerChamber[chId] += nDigisPerLayer;
    totalNDigis += nDigisPerLayer;
  }


  if(granularity == "global") { 
    if(cutType == "lessThan" && totalNDigis < threshold) {
      keptEvents++;
      return true;
    } else if(cutType == "moreThan" && totalNDigis > threshold) {
      keptEvents++;
      return true;
    } else return false;
  } else if(granularity == "perChamber") {
    for(map<DTChamberId, int>::const_iterator nDigisCh = nDigisPerChamber.begin();
	nDigisCh != nDigisPerChamber.end(); ++nDigisCh) {
      DTChamberId chId = (*nDigisCh).first;
      int num = (*nDigisCh).second;
      
      if(cutType == "lessThan" && num < threshold) {
	keptEvents++;
	return true;
      } else if(cutType == "moreThan" && num >  threshold) {            keptEvents++;
	keptEvents++;
	return true;
      } else return false;
    }
  }

  return false;
}

void  DTNDigiFilter::endJob() {
  cout << "[DTNDigiFilter] # processed events: " << allEvents << endl;
  cout << "                # kept events: " << keptEvents << endl;
  cout << "                eff: " << 100*(float)keptEvents/(float)allEvents << "%" << endl;
}
