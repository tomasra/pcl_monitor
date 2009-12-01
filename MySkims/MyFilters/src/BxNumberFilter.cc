//
// Original Author:  Marco Zanetti
//         Created:  Tue Sep  9 15:56:24 CEST 2008


#include "MySkims/MyFilters/src/BxNumberFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "EventFilter/FEDInterface/interface/GlobalEventNumber.h"
#include <DataFormats/FEDRawData/interface/FEDRawDataCollection.h>

#include "TH1F.h"
#include "TFile.h"


// user include files
using namespace edm;
using namespace std;


BxNumberFilter::BxNumberFilter(const edm::ParameterSet& iConfig) {

  inputLabel = iConfig.getUntrackedParameter<edm::InputTag>("inputLabel",edm::InputTag("source"));
  goldenBXIds = iConfig.getParameter<std::vector<int> >("goldenBXIds");
  range = iConfig.getUntrackedParameter<unsigned int>("range", 1);
  debug = iConfig.getUntrackedParameter<unsigned int>("debug", false);
}


BxNumberFilter::~BxNumberFilter() { }


bool BxNumberFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
   bool result = false;

   unsigned int GTEVMId= 812;

   Handle<FEDRawDataCollection> rawdata;
   iEvent.getByLabel(inputLabel, rawdata);  
   const FEDRawData& data = rawdata->FEDData(GTEVMId);

   bxDistr->Fill(evf::evtn::getfdlbx(data.data()));

   // loop over the predefined BX's
   for (vector<int>::const_iterator i = goldenBXIds.begin(); i != goldenBXIds.end(); i++) {

     // Select the BX
     if ( evf::evtn::getfdlbx(data.data()) <= (*i) + range
	  &&
	  evf::evtn::getfdlbx(data.data()) >= (*i) - range ) {
       result = true;
       
       if (debug) {
	 cout << "Event # " << evf::evtn::get(data.data(),true) << endl;
	 cout << "LS # " << evf::evtn::getlbn(data.data()) << endl;
	 cout << "ORBIT # " << evf::evtn::getorbit(data.data()) << endl;
	 cout << "GPS LOW # " << evf::evtn::getgpslow(data.data()) << endl;
	 cout << "GPS HI # " << evf::evtn::getgpshigh(data.data()) << endl;
	 cout << "BX FROM FDL 0-xing # " << evf::evtn::getfdlbx(data.data()) << endl;
       }
       
     } 
   }
   return result;
}

// ------------ method called once each job just before starting event loop  ------------
void  BxNumberFilter::beginJob(const edm::EventSetup&) {
  theRootFile = new TFile("BXDistr.root","RECREATE");
  theRootFile->cd();
  bxDistr = new TH1F("bxDistr", "bxDistr",4000,0,4000);


}


// ------------ method called once each job just after ending the event loop  ------------
void  BxNumberFilter::endJob() {
  theRootFile->cd();
  bxDistr->Write();
  theRootFile->Close();

}
