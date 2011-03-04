
/*
 *  See header file for a description of this class.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - CERN
 */

#include "Tools/MyAnalysisTools/src/ZZllvvAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "AnalysisDataFormats/CMGTools/interface/Muon.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"

#include <iostream>

using namespace std;
using namespace edm;

ZZllvvAnalyzer::ZZllvvAnalyzer(const ParameterSet& pSet){
  totNEvents = 0;
}

ZZllvvAnalyzer::~ZZllvvAnalyzer(){}




// Operations
void ZZllvvAnalyzer::beginRun(const Run& run, const EventSetup& eSetup) {}
  
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


  cout << "# of muons: " << muons.size() << endl;
  cout << "# of jets: " << jets.size() << endl;
  

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
}



