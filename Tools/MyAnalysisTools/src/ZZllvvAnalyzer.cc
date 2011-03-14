
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2011/03/08 15:13:10 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - CERN
 */

#include "Tools/MyAnalysisTools/src/ZZllvvAnalyzer.h"
#include "Tools/MyAnalysisTools/interface/Histograms.h"


#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/Framework/interface/EventSetup.h"
#include "AnalysisDataFormats/CMGTools/interface/Muon.h"
#include "AnalysisDataFormats/CMGTools/interface/PFJet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <iostream>
#include "TFile.h"

using namespace std;
using namespace edm;

ZZllvvAnalyzer::ZZllvvAnalyzer(const ParameterSet& pSet) : totNEvents(0),
							   weight(1) {

  theFile = new TFile(pSet.getUntrackedParameter<string>("fileName", "ZZllvvAnalyzer.root").c_str(),"RECREATE");


}

ZZllvvAnalyzer::~ZZllvvAnalyzer(){
  cout << "destructor" << endl;
}



void ZZllvvAnalyzer::beginJob() {
  
  
  theFile->cd();


  // book the histograms
  muonS1 = new HistoLept("MuonS1");


}


// Operations
void ZZllvvAnalyzer::beginRun(const Run& run, const EventSetup& eSetup) {
}
  
void ZZllvvAnalyzer::analyze(const Event& event, const EventSetup& eSetup) {
  totNEvents++;
  
  // -----------------------------------------------------------
  // get the event products
  

  Handle<vector<cmg::Muon> > muonsH;
  event.getByLabel("cmgMuon", muonsH);
  vector<cmg::Muon> muons = *(muonsH.product());

  Handle<vector<cmg::PFJet> > jetsH;
  event.getByLabel(string("cmgPFJet"), jetsH);
  vector<cmg::PFJet> jets = *(jetsH.product());

  theFile->cd();
  cout << "# of muons: " << muons.size() << endl;
  cout << "# of jets: " << jets.size() << endl;
  
  // ---------------------------------------------------------------
  // Step1
  
  // plot muons
  for(vector<cmg::Muon>::const_iterator muon = muons.begin();
      muon != muons.end();
      ++muon) {
    //    cout << "pt: " << muon->pt() << endl;
    int type  = -1; // FIXME move this to a function
    if(muon->isTracker() && !muon->isGlobal()) {
      type = 0;
    } else if(!muon->isTracker() && muon->isGlobal()) {
      type = 1;
    } else if(muon->isTracker() && muon->isGlobal()) {
      type = 2;
    }
//     muon->normalizedChi2();
    muonS1->Fill(muon->pt(), muon->eta(), muon->phi(),
		 muon->relIso(),
		 muon->dxy(), muon->dz(),
		 type,
		 muon->numberOfValidPixelHits(), muon->numberOfValidTrackerHits(), muon->numberOfValidMuonHits(), muon->numberOfMatches(),
		 weight);
  }
  muonS1->FillNLept(muons.size(), weight);
  
  



  // ---------------------------------------------------------------
  // Step2: ask for exactly 2 muons and set the mass window
  


//   Handle<vector<cmg::DiJet> > Zjjs;
//   event.getByLabel(string("selectedZjjCand"), Zjjs);  

//   Handle<vector<cmg::DiMuon> > Zmms;
//   event.getByLabel(string("selectedZCand"), Zmms);  

//   Handle<vector<cmg::DiJet> > Zjjs_nocuts;
//   event.getByLabel(string("cmgDiJet"), Zjjs_nocuts);  

//   Handle<vector<cmg::DiMuon> > Zmms_nocuts;
//   event.getByLabel(string("cmgDiMuon"), Zmms_nocuts);  

//  Handle<vector<cmg::DiMuonDiJet> > higgses;
//   event.getByLabel(string("cmgDiMuonDiJet"), higgses)

}

void ZZllvvAnalyzer::endJob() {
  cout << "Tot. # of events: " << totNEvents << endl;

// //   // Write the histograms
  theFile->cd();
  muonS1->Write();
  theFile->Close();
}



