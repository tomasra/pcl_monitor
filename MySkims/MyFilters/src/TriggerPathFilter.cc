//
// Original Author:  Marco Zanetti
//         Created:  Tue Sep  9 15:56:24 CEST 2008



// user include files
#include "MySkims/MyFilters/src/TriggerPathFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

// L1
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"

// HLT
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/Common/interface/HLTenums.h"
#include "FWCore/Framework/interface/TriggerNames.h"


using namespace edm;
using namespace std;
  



TriggerPathFilter::TriggerPathFilter(const edm::ParameterSet& iConfig) {
  triggerResultsLabel = iConfig.getParameter<edm::InputTag>("triggerResults");
  l1DataLabel = iConfig.getParameter<edm::InputTag>("l1GtData");
  l1Bits = iConfig.getParameter<std::vector<int> >("l1Bits");
  hltBits = iConfig.getParameter<std::vector<std::string> >("hltBits");
  resultDefinition = iConfig.getParameter<int>("resultDefinition");
  debug = iConfig.getUntrackedParameter<bool>("debug",false);
}



TriggerPathFilter::~TriggerPathFilter() { }



bool TriggerPathFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  
  if(debug) cout << "[TriggerPathFilter] filtering" << endl;
  bool l1Result = false;
  bool hltResult = false;
  bool result = false;

//   // FIXME: commented for running on the RECO data
//   // L1 results
//   Handle<L1GlobalTriggerReadoutRecord> myGTReadoutRecord;
//   iEvent.getByLabel(l1DataLabel,myGTReadoutRecord);

//   DecisionWord gtDecisionWord = myGTReadoutRecord->decisionWord();
//   if ( ! gtDecisionWord.empty() ) { // if board not there this is zero
//     for ( vector<int>::const_iterator i = l1Bits.begin(); i != l1Bits.end(); i++) {
//       if ( gtDecisionWord[(*i)] ) l1Result = true;
//     }
//   }
  
  // HLT results
  Handle<TriggerResults> hltResults;
  iEvent.getByLabel(triggerResultsLabel, hltResults);
  
  TriggerNames pathNames(*hltResults);
  if(debug) cout << "   size of HLT resutls: " << hltResults->size() << endl;
  for (unsigned int i = 0; i < hltResults->size(); i++) {
    for (vector<string>::const_iterator s = hltBits.begin(); s != hltBits.end(); s++) {
      //matching the path names
      if(debug) cout << "    HLT trigger name: " << pathNames.triggerName(i) << endl;
      if (pathNames.triggerName(i) == (*s) ) {
	if ( hltResults->state(i) == hlt::Pass) {
	  hltResult = true;
	}
      }
    }
  }
  
  if(debug) {
    if(hltResult == true) {
      cout << " hlt bit found" << endl;
    } else {
      cout << " hlt bit not found" << endl;
    }
  }

  if (resultDefinition == 1) result = hltResult || l1Result;
  if (resultDefinition == 2) result = hltResult && l1Result;
  if (resultDefinition == 3) result = l1Result;
  if (resultDefinition == 4) result = hltResult;

  return result;
}



// ------------ method called once each job just before starting event loop  ------------
void  TriggerPathFilter::beginJob(const edm::EventSetup&) {
}



// ------------ method called once each job just after ending the event loop  ------------
void  TriggerPathFilter::endJob() {
}

