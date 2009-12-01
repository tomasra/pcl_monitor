
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2008/12/03 10:41:14 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */


#include "MySkims/MyFilters/src/TriggerSourceFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/L1GlobalMuonTrigger/interface/L1MuRegionalCand.h"
#include "DataFormats/L1GlobalMuonTrigger/interface/L1MuGMTReadoutCollection.h"

#include "TH1F.h"
#include "TFile.h"


// user include files
using namespace edm;
using namespace std;


TriggerSourceFilter::TriggerSourceFilter(const edm::ParameterSet& ps) : allEvents(0),
									keptEvents(0) {
  cout << "[TriggerSourceFilter] contructor called" << endl;
  gmtInputTag = ps.getParameter<edm::InputTag>("GMTInputTag");
  // Trigger source:
  // 1 -> DT
  // 2 -> CSC
  // 3 -> CSC Halo
  // 4 -> RPC barrel
  // 5 -> RPC endcap
  triggerSource = ps.getUntrackedParameter<int>("triggerSource",1);

  debug = ps.getUntrackedParameter<bool>("debug", false);


}


TriggerSourceFilter::~TriggerSourceFilter() { }


bool TriggerSourceFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  allEvents++;
  bool result = false;

   edm::Handle<L1MuGMTReadoutCollection> gmtrc_handle; 
   iEvent.getByLabel(gmtInputTag,gmtrc_handle);
   L1MuGMTReadoutCollection const* gmtrc = gmtrc_handle.product();
   
   bool dt_l1a = false;
   bool csc_l1a = false;
   bool halo_l1a = false;
   bool rpcb_l1a = false;
   bool rpcf_l1a = false;
   
   std::vector<L1MuGMTReadoutRecord> gmt_records = gmtrc->getRecords();
   std::vector<L1MuGMTReadoutRecord>::const_iterator igmtrr;
   
   for(igmtrr=gmt_records.begin(); igmtrr!=gmt_records.end(); igmtrr++) {

     std::vector<L1MuRegionalCand>::const_iterator iter1;
     std::vector<L1MuRegionalCand> rmc;

     // DT muon candidates
     int idt = 0;
     rmc = igmtrr->getDTBXCands();
     for(iter1=rmc.begin(); iter1!=rmc.end(); iter1++) {
       if ( !(*iter1).empty() ) {
            idt++;
       }
     }
     
     if(debug)
       if(idt>0) std::cout << "Found " << idt << " valid DT candidates in bx wrt. L1A = " 
			   << igmtrr->getBxInEvent() << std::endl;

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
     
     if(debug) {
       if(icsc>0) std::cout << "Found " << icsc << " valid CSC candidates in bx wrt. L1A = " 
			    << igmtrr->getBxInEvent() << std::endl;
       if(ihalo>0) std::cout << "Found " << ihalo << " valid CSC halo candidates in bx wrt. L1A = " 
			     << igmtrr->getBxInEvent() << std::endl;
     }

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
     
     if(debug)
       if(irpcb>0) std::cout << "Found " << irpcb << " valid barrel RPC candidates in bx wrt. L1A = " 
			     << igmtrr->getBxInEvent() << std::endl;

     if(igmtrr->getBxInEvent()==0 && irpcb>0) rpcb_l1a = true;
     
     // RPC endcap muon candidates
     int irpcf = 0;
     rmc = igmtrr->getFwdRPCCands();
     for(iter1=rmc.begin(); iter1!=rmc.end(); iter1++) {
       if ( !(*iter1).empty() ) {
            irpcf++;
       }
     }
     
     if(debug)
       if(irpcf>0) std::cout << "Found " << irpcf << " valid endcap RPC candidates in bx wrt. L1A = " 
			     << igmtrr->getBxInEvent() << std::endl;
     
     if(igmtrr->getBxInEvent()==0 && irpcf>0) rpcf_l1a = true;
     
   }

   if(debug) {
     std::cout << "**** L1 Muon Trigger Source ****" << std::endl;
     if(dt_l1a) std::cout << "DT" << std::endl;
     if(csc_l1a) std::cout << "CSC" << std::endl;
     if(halo_l1a) std::cout << "CSC halo" << std::endl;
     if(rpcb_l1a) std::cout << "barrel RPC" << std::endl;
     if(rpcf_l1a) std::cout << "endcap RPC" << std::endl;
     std::cout << "************************" << std::endl;
   }   

   if(triggerSource == 1) {
     result = dt_l1a;
   } else if(triggerSource == 2) {
     result = csc_l1a;
   } else if(triggerSource == 3) {
     result = halo_l1a;
   } else if(triggerSource == 4) {
     result = rpcb_l1a;
   } else if(triggerSource == 5) {
     result = rpcf_l1a;
   }

   

   if(debug && result) cout << "   keeping event!" << endl;
   if(result) keptEvents++;

   return result;
}




// ------------ method called once each job just before starting event loop  ------------
void  TriggerSourceFilter::beginJob(const edm::EventSetup&) {
  if(debug) cout << "[TriggerSourceFilter] beginJob" << endl;

}


// ------------ method called once each job just after ending the event loop  ------------
void  TriggerSourceFilter::endJob() {
  cout << "[TriggerSourceFilter] # processed events: " << allEvents << endl;
  cout << "                # kept events: " << keptEvents << endl;
  cout << "                eff: " << 100*(float)keptEvents/(float)allEvents << "%" << endl;
}


