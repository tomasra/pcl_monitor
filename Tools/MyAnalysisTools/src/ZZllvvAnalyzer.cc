
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2011/03/04 18:10:33 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - CERN
 */

#include "Tools/MyAnalysisTools/src/ZZllvvAnalyzer.h"
// #include "Tools/MyAnalysisTools/interface/Histograms.h"


#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/Framework/interface/EventSetup.h"
// #include "AnalysisDataFormats/CMGTools/interface/Muon.h"
// #include "AnalysisDataFormats/CMGTools/interface/PFJet.h"
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

  theFile = new TFile("ZZllvvAnalyzer.root","RECREATE");


}

ZZllvvAnalyzer::~ZZllvvAnalyzer(){
  delete theFile;
}



void ZZllvvAnalyzer::beginJob() {
  
  
//   edm::Service<TFileService> tFileService;
//   // create the root file
//   theFile = &tFileService->file();
//     //  theFile = new TFile("ZZllvvAnalyzer.root","RECREATE"); //FIXME: file name from pSet
//   theFile->cd();


//   // book the histograms
//   muonS1 = new HistoLept("MuonS1");
//   // apply the weighting
//   weight = 1;
}


// Operations
void ZZllvvAnalyzer::beginRun(const Run& run, const EventSetup& eSetup) {
}
  
void ZZllvvAnalyzer::analyze(const Event& event, const EventSetup& eSetup) {
  totNEvents++;
  
  // -----------------------------------------------------------
  // get the event products
  

//   Handle<vector<cmg::Muon> > muonsH;
//   event.getByLabel("cmgMuon", muonsH);
//   vector<cmg::Muon> muons = *(muonsH.product());

//   Handle<vector<cmg::PFJet> > jetsH;
//   event.getByLabel(string("cmgPFJet"), jetsH);
//   vector<cmg::PFJet> jets = *(jetsH.product());

// //   theFile->cd();
//   cout << "# of muons: " << muons.size() << endl;
//   cout << "# of jets: " << jets.size() << endl;
  
//   // Step1
//   for(vector<cmg::Muon>::const_iterator muon = muons.begin();
//       muon != muons.end();
//       ++muon) {
//     muonS1->Fill(muon->pt(), muon->eta(), muon->phi(), 1);
//   }

  

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
//   theFile->cd();
//   muonS1->Write();theFile->Close();
}



