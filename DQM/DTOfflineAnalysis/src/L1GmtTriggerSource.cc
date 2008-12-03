// -*- C++ -*-
//
// Package:    L1GmtTriggerSource
// Class:      L1GmtTriggerSource
// 
/**\class L1GmtTriggerSource L1GmtTriggerSource.cc 

 Description: Analyzer to determine the source of muon triggers

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  Ivan Mikulec
//         Created:  
//
//


// system include files
#include <memory>
#include <vector>
#include <iostream>

// user include files
#include "DQM/DTOfflineAnalysis/src/L1GmtTriggerSource.h"
#include "DQM/DTOfflineAnalysis/src/Histograms.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/L1GlobalMuonTrigger/interface/L1MuRegionalCand.h"
#include "DataFormats/L1GlobalMuonTrigger/interface/L1MuGMTReadoutCollection.h"

#include "EventFilter/Utilities/interface/GlobalEventNumber.h"
#include <DataFormats/FEDRawData/interface/FEDRawDataCollection.h>


#include "TH1F.h"
#include "TFile.h"

using namespace std;


L1GmtTriggerSource::L1GmtTriggerSource(const edm::ParameterSet& ps) {
   //now do what ever initialization is needed
  m_GMTInputTag = ps.getParameter<edm::InputTag>("GMTInputTag");
  inputLabel  = ps.getParameter<edm::InputTag>("inputLabel");
  debug = ps.getUntrackedParameter<bool>("debug", false);
}


L1GmtTriggerSource::~L1GmtTriggerSource()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
L1GmtTriggerSource::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  if(debug)
    cout << "=== Event: " << iEvent.id().event() << "===============================================================" << endl;
  
   using namespace edm;
   unsigned int GTEVMId= 812;

   Handle<FEDRawDataCollection> rawdata;
   iEvent.getByLabel(inputLabel, rawdata);  
   const FEDRawData& data = rawdata->FEDData(GTEVMId);



   edm::Handle<L1MuGMTReadoutCollection> gmtrc_handle; 
   iEvent.getByLabel(m_GMTInputTag,gmtrc_handle);
   L1MuGMTReadoutCollection const* gmtrc = gmtrc_handle.product();
   
   bool dt_l1a = false;
   bool csc_l1a = false;
   bool halo_l1a = false;
   bool rpcb_l1a = false;
   bool rpcf_l1a = false;
   
   vector<L1MuGMTReadoutRecord> gmt_records = gmtrc->getRecords();
   vector<L1MuGMTReadoutRecord>::const_iterator igmtrr;
   
   for(igmtrr=gmt_records.begin(); igmtrr!=gmt_records.end(); igmtrr++) {

     vector<L1MuRegionalCand>::const_iterator iter1;
     vector<L1MuRegionalCand> rmc;

     // DT muon candidates
     int idt = 0;
     rmc = igmtrr->getDTBXCands();
     for(iter1=rmc.begin(); iter1!=rmc.end(); iter1++) {
       if ( !(*iter1).empty() ) {
            idt++;
       }
     }
     
     if(idt>0 && debug) cout << "Found " << idt << " valid DT candidates in bx wrt. L1A = " 
                                     << igmtrr->getBxInEvent() << endl;
     if(igmtrr->getBxInEvent()==0 && idt>0) dt_l1a = true;
     
     // CSC muon candidates
     int icsc = 0;
     int ihalo = 0;
     rmc = igmtrr->getCSCCands();
     for(iter1=rmc.begin(); iter1!=rmc.end(); iter1++) {
       if ( !(*iter1).empty() ) {
            if((*iter1).isFineHalo()) {
              ihalo++;
            } else {
              icsc++;
            }
       }
     }
     
     if(icsc>0 & debug) cout << "Found " << icsc << " valid CSC candidates in bx wrt. L1A = " 
                                     << igmtrr->getBxInEvent() << endl;
     if(ihalo>0 & debug) cout << "Found " << ihalo << " valid CSC halo candidates in bx wrt. L1A = " 
                                     << igmtrr->getBxInEvent() << endl;
     if(igmtrr->getBxInEvent()==0 && icsc>0) csc_l1a = true;
     if(igmtrr->getBxInEvent()==0 && ihalo>0) halo_l1a = true;
     
     // RPC barrel muon candidates
     int irpcb = 0;
     rmc = igmtrr->getBrlRPCCands();
     for(iter1=rmc.begin(); iter1!=rmc.end(); iter1++) {
       if ( !(*iter1).empty() ) {
            irpcb++;
       }
     }
     
     if(irpcb>0 & debug) cout << "Found " << irpcb << " valid barrel RPC candidates in bx wrt. L1A = " 
                                     << igmtrr->getBxInEvent() << endl;
     if(igmtrr->getBxInEvent()==0 && irpcb>0) rpcb_l1a = true;
     
     // RPC endcap muon candidates
     int irpcf = 0;
     rmc = igmtrr->getFwdRPCCands();
     for(iter1=rmc.begin(); iter1!=rmc.end(); iter1++) {
       if ( !(*iter1).empty() ) {
            irpcf++;
       }
     }
     
     if(irpcf>0 && debug) cout << "Found " << irpcf << " valid endcap RPC candidates in bx wrt. L1A = " 
                                     << igmtrr->getBxInEvent() << endl;
     if(igmtrr->getBxInEvent()==0 && irpcf>0) rpcf_l1a = true;
     
   }

   int currentOrbit = evf::evtn::getorbit(data.data());
   int currentBX = evf::evtn::getfdlbx(data.data());

   pair<int, int> currentId = make_pair(currentOrbit, currentBX);


   if (debug) {
     cout << "[L1GmtTriggerSource] Event # " << evf::evtn::get(data.data(),true)
	  << " LS # " << evf::evtn::getlbn(data.data())
	  << " Orbit # " << evf::evtn::getorbit(data.data())
// 	  << " GPS low # " << evf::evtn::getgpslow(data.data())
// 	  << " GPS hi # " << evf::evtn::getgpshigh(data.data())
	  << " BX from FDL 0-xing # " << evf::evtn::getfdlbx(data.data()) << endl;
   }
   
   int bxDistanceAll = bxDist(prevOrbtAndBxAll, currentId);
   prevOrbtAndBxAll = currentId;
   hAll->Fill(bxDistanceAll);
   if(debug) cout << "   BX distance from previous event: " << bxDistanceAll << endl;
       
   if(dt_l1a) {
     int bxDistDT = bxDist(prevOrbtAndBxDT, currentId);
     prevOrbtAndBxDT = currentId;
     hDT->Fill(bxDistDT);
     if(debug) cout << "   BX distance from previous event (DT trigger): " << bxDistDT << endl;
   }
   
   if(dt_l1a && !rpcf_l1a && !rpcb_l1a && !csc_l1a && !halo_l1a) {
     int bxDistDTonly = bxDist(prevOrbtAndBxDTonly, currentId);
     prevOrbtAndBxDTonly = currentId;
     hDTonly->Fill(bxDistDTonly);
     if(debug) cout << "   BX distance from previous event (DT trigger only): " << bxDistDTonly << endl;
   }

   if(dt_l1a || rpcb_l1a || rpcf_l1a) {
     int bxDistDTorRPC = bxDist(prevOrbtAndBxDTorRPC, currentId);
     prevOrbtAndBxDTorRPC = currentId;
     hDTorRPC->Fill(bxDistDTorRPC);
     if(debug) cout << "   BX distance from previous event (DT or RPC trigger): " << bxDistDTorRPC << endl;
   }

   if(rpcb_l1a || rpcf_l1a) {
     int bxDistRPC = bxDist(prevOrbtAndBxRPC, currentId);
     prevOrbtAndBxRPC = currentId;
     hRPC->Fill(bxDistRPC);
     if(debug) cout << "   BX distance from previous event (RPC trigger): " << bxDistRPC << endl;
   }

   if((rpcb_l1a || rpcf_l1a) && !dt_l1a && !csc_l1a && !halo_l1a) {
     int bxDistRPConly = bxDist(prevOrbtAndBxRPConly, currentId);
     prevOrbtAndBxRPConly = currentId;
     hRPConly->Fill(bxDistRPConly);
     if(debug) cout << "   BX distance from previous event (RPC trigger only): " << bxDistRPConly << endl;
   }
   


   //-----------------------------------------------------------
      
   if(debug) {
     cout << "**** L1 Muon Trigger Source ****" << endl;
     if(dt_l1a) cout << "DT" << endl;
     if(csc_l1a) cout << "CSC" << endl;
     if(halo_l1a) cout << "CSC halo" << endl;
     if(rpcb_l1a) cout << "barrel RPC" << endl;
     if(rpcf_l1a) cout << "endcap RPC" << endl;
     cout << "************************" << endl;
   }
}


// ------------ method called once each job just before starting event loop  ------------
void 
L1GmtTriggerSource::beginJob(const edm::EventSetup&) {

  theFile = new TFile("L1GmtTriggerSource.root","RECREATE");
  theFile->cd();

  hDT = new HBxDistance("DT");
  hAll = new HBxDistance("All");
  hDTorRPC = new HBxDistance("DTorRPC");
  hRPC = new HBxDistance("RPC");
  hDTonly = new HBxDistance("DTonly");
  hRPConly = new HBxDistance("RPConly");

}

// ------------ method called once each job just after ending the event loop  ------------
void 
L1GmtTriggerSource::endJob() {

  theFile->cd();  
  hDT->Write();
  hAll->Write();
  hDTorRPC->Write();
  hRPC->Write();
  hDTonly->Write();
  hRPConly->Write();
  theFile->Close();
}



int L1GmtTriggerSource::bxDist(const pair<int, int>& previousId, const pair<int, int>& currentId) const {
     return  ((currentId.first*3564)+currentId.second)-((previousId.first*3564)+previousId.second);
}



//define this as a plug-in
DEFINE_FWK_MODULE(L1GmtTriggerSource);
