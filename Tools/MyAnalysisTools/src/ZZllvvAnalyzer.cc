/*
 *  See header file for a description of this class.
 *
 *  $Date: 2011/04/18 17:39:18 $
 *  $Revision: 1.5 $
 *  \author G. Cerminara - CERN
 */
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"
#include "Tools/MyAnalysisTools/src/ZZllvvAnalyzer.h"
#include "Tools/MyAnalysisTools/interface/Histograms.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"


#include "FWCore/Framework/interface/EventSetup.h"
// #include "AnalysisDataFormats/CMGTools/interface/Muon.h"
// #include "AnalysisDataFormats/CMGTools/interface/PFJet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/EventHypothesis.h"
#include "DataFormats/PatCandidates/interface/EventHypothesisLooper.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include <iostream>
#include "TFile.h"

#include "CMGTools/HtoZZ2l2nu/interface/Utils.h"
#include "CMGTools/HtoZZ2l2nu/interface/ReducedMETComputer.h"
#include "CMGTools/HtoZZ2l2nu/interface/ObjectFilters.h"

using namespace std;
using namespace edm;

int nEventPreSkim;
int nEventBaseFilter;
int nEventSkim;
TH1F *hEventCounter;

HistoLept *hMuonLead_cut0;    
HistoLept *hMuonSubLead_cut0;
HistoKin *hDiLeptKin_cut0;
HistoRedMET *hRedMetStd_cut0;
HistoKin *hJetKin_cut0;
HistoKin *hMETKin_cut0;

HistoLept *hMuonLead_cut1;    
HistoLept *hMuonSubLead_cut1;
HistoKin *hDiLeptKin_cut1;
HistoKin *hJetKin_cut1;
HistoKin *hMETKin_cut1;
HistoKin *hMETKin_J0_cut1;
HistoKin *hMETKin_J1_cut1;


HistoRedMET *hRedMetStd_cut1;
HistoRedMET *hRedMetStd_J0_cut1;
HistoRedMET *hRedMetStd_J1_cut1;
                        
HistoRedMET *hRedMetTuneA_cut1;
HistoRedMET *hRedMetTuneA_J0_cut1;
HistoRedMET *hRedMetTuneA_J1_cut1;
                        
HistoRedMET *hRedMetTuneB_cut1;
HistoRedMET *hRedMetTuneB_J0_cut1;
HistoRedMET *hRedMetTuneB_J1_cut1;














TH1F *hNVertexAll;

ReducedMETComputer *redMETComputer_std;
ReducedMETComputer *redMETComputer_tuneA;
ReducedMETComputer *redMETComputer_tuneB;

ZZllvvAnalyzer::ZZllvvAnalyzer(const ParameterSet& pSet) : totNEvents(0),
							   weight(1) {

  theFile = new TFile(pSet.getUntrackedParameter<string>("fileName", "ZZllvvAnalyzer.root").c_str(),"RECREATE");
  source = pSet.getUntrackedParameter<InputTag>("source");
  zmmInput = pSet.getUntrackedParameter<InputTag>("zmmInput");
  debug = pSet.getUntrackedParameter<bool>("debug","False");
  nEventPreSkim = 0;
  nEventBaseFilter = 0;
  nEventSkim = 0;
  redMETComputer_std   = new ReducedMETComputer();
  redMETComputer_tuneA = new ReducedMETComputer(1., 1. );
  redMETComputer_tuneB = new ReducedMETComputer(1., 1., 0., 0.);

  vertexSelection =  pSet.getParameter<ParameterSet>("Vertices");
}

ZZllvvAnalyzer::~ZZllvvAnalyzer(){
  cout << "destructor" << endl;
}



void ZZllvvAnalyzer::beginJob() {
  
  
  theFile->cd();

  hEventCounter = new TH1F("hEventCounter", "Event counters", 10,0,10);
  hEventCounter->GetXaxis()->SetBinLabel(1,"before skim");
  hEventCounter->GetXaxis()->SetBinLabel(2,"after pre-filters");
  hEventCounter->GetXaxis()->SetBinLabel(3,"after skim");
  hEventCounter->GetXaxis()->SetBinLabel(4,"analyzed");
  hEventCounter->GetXaxis()->SetBinLabel(5,"pre sel.");
  hEventCounter->GetXaxis()->SetBinLabel(6,"sel dilepton");
  hEventCounter->GetXaxis()->SetBinLabel(7,"mass window");

  hEventCounter->Sumw2();

  // book the histograms
  hNVertexAll = new TH1F("hNVertexAll", "# of vertices", 100,0,100);
  hNVertexAll->Sumw2();

  hMuonLead_cut0    = new HistoLept("MuonLead_cut0");
  hMuonSubLead_cut0 = new HistoLept("MuonSubLead_cut0");
  hDiLeptKin_cut0   = new HistoKin("DiLeptKin_cut0");

  hMuonLead_cut1    = new HistoLept("MuonLead_cut1");
  hMuonSubLead_cut1 = new HistoLept("MuonSubLead_cut1");
  hDiLeptKin_cut1   = new HistoKin("DiLeptKin_cut1");

  hRedMetStd_cut0 = new HistoRedMET("RedMetStd_cut0");

  // original NEU kFactors
  hRedMetStd_cut1 = new HistoRedMET("RedMetStd_cut1");
  hRedMetStd_J0_cut1 = new HistoRedMET("RedMetStd_J0__cut1");
  hRedMetStd_J1_cut1 = new HistoRedMET("RedMetStd_J1_cut1");

  hRedMetTuneA_cut1 = new HistoRedMET("RedMetTuneA_cut1");
  hRedMetTuneA_J0_cut1 = new HistoRedMET("RedMetTuneA_J0_cut1");
  hRedMetTuneA_J1_cut1 = new HistoRedMET("RedMetTuneA_J1_cut1");

  hRedMetTuneB_cut1 = new HistoRedMET("RedMetTuneB_cut1");
  hRedMetTuneB_J0_cut1 = new HistoRedMET("RedMetTuneB_J0_cut1");
  hRedMetTuneB_J1_cut1 = new HistoRedMET("RedMetTuneB_J1_cut1");



  hJetKin_cut0 = new HistoKin("JetKin_cut0");
  hMETKin_cut0 = new HistoKin("METKin_cut0");
  hJetKin_cut1 = new HistoKin("JetKin_cut1");
  hMETKin_cut1 = new HistoKin("METKin_cut1");
  hMETKin_J0_cut1 = new HistoKin("METKin_J0_cut1");
  hMETKin_J1_cut1 = new HistoKin("METKin_J1_cut1");


}


// Operations
void ZZllvvAnalyzer::beginRun(const Run& run, const EventSetup& eSetup) {
}
  
void ZZllvvAnalyzer::analyze(const Event& event, const EventSetup& eSetup) {

  totNEvents++;
  // count all the events

  using reco::Candidate; 
  using reco::CandidatePtr;
  
  //pre-select vertices
  Handle<reco::VertexCollection> offlinePrimVertices;
  event.getByLabel("offlinePrimaryVertices", offlinePrimVertices);  
  std::vector<reco::VertexRef> selVertices = vertex::filter(offlinePrimVertices,vertexSelection);
  if(debug) cout << "# of vertices: " << selVertices.size() << endl;;



  //retrieve the event hypothesis
  Handle<vector<pat::EventHypothesis> > hyps;
  edm::InputTag selEvtTag(source.label()+":selectedEvent");
  event.getByLabel(selEvtTag, hyps);

  //retrieve the selection path
  Handle<std::vector<int> > selectionInfo;
  edm::InputTag selInfoTag(source.label()+":selectionInfo");
  event.getByLabel(selInfoTag, selectionInfo);

  //retrieve the selected vertex
  Handle<reco::VertexCollection> selectedVertex;
  edm::InputTag selVtxTag(source.label()+":selectedVertices");
  event.getByLabel(selVtxTag, selectedVertex);

  // Get the candidate collection
  Handle<View<reco::CompositeCandidate> > diMuonCands;
  event.getByLabel(string("zMMCand"), diMuonCands);  
  if(diMuonCands.isValid()) {
    if(debug) cout << "# of dimuons: " << diMuonCands->size() << endl;
  }

  // Get the candidate collection
  Handle<View<reco::CompositeCandidate> > diElectrCands;
  event.getByLabel("zEECand", diElectrCands);  
  
  if(debug) cout << "# of dielectrons: " << diElectrCands->size() << endl;
  

  if(hyps->size()==0) return;
  hEventCounter->Fill(4);
  
  const pat::EventHypothesis &h = (*hyps)[0];

  //dump selected event 
  // SlectionInfo [0] -> path: {UNKNOWN=0,MUMU=1,EE=2,EMU=3};
  // SlectionInfo [1] -> step: 
  if(debug) {
    cout << "Retrieve an event hypothesis selected at step=" << (*selectionInfo)[1]
	 << " for path " << (*selectionInfo)[0] 
	 << " with " << selectedVertex->size() << " vertices" << std::endl;
  }

  if((*selectionInfo)[0] == 0) {
    if(debug)  cout << "\t no dilepton has been selected" << std::endl;
    return;
  }

  const pat::MET *met = h.getAs<pat::MET>("met");
  if(debug) cout << "\t met:" << met->pt() << ";" << met->phi() << endl;
  hMETKin_cut0->Fill(met->pt(), met->eta(), met->phi(), met->mass(), weight);

  vector<LorentzVector> jetMomenta;

  for (pat::eventhypothesis::Looper<pat::Jet> jet = h.loopAs<pat::Jet>("jet"); jet; ++jet) {
    if(debug) cout << "\t jet: " << jet->pt() << ";" << jet->eta() << ";" << jet->phi() << std::endl;
    jetMomenta.push_back(jet->p4());
    hJetKin_cut0->Fill(jet->pt(), jet->eta(), jet->phi(), jet->mass(), weight);
  }
  hJetKin_cut0->FillNObj(jetMomenta.size(), weight);
  if(debug) cout << "# of jets: " << jetMomenta.size() << endl;

  // =====================================================================
  // cut0: ask for the dilepton to exist
  
  hEventCounter->Fill(5);

  CandidatePtr lep1 = h["leg1"];
  CandidatePtr lep2 = h["leg2"];
  if(debug) {
    cout << "\t dilepton leg1: " << lep1->pt() << ";" << lep1->eta() << ";" << lep1->phi() << endl
	 << "\t          leg2: " << lep2->pt() << ";" << lep2->eta() << ";" << lep2->phi() << endl;
  }
  const pat::Muon *muonLead    = dynamic_cast<const pat::Muon *>(lep1.get());
  const pat::Muon *muonSubLead = dynamic_cast<const pat::Muon *>(lep2.get());
  const reco::Vertex *vtx = &(*selectedVertex)[0];

  

  typedef reco::Candidate::LorentzVector LorentzVector;
  LorentzVector leadLeptMom = lep1->p4();
  LorentzVector subLeadLeptMom = lep2->p4();
  LorentzVector diLeptonMom = leadLeptMom + subLeadLeptMom;


  hMuonLead_cut0->Fill(muonLead, vtx, weight);
  hMuonSubLead_cut0->Fill(muonSubLead, vtx, weight);
  hDiLeptKin_cut0->Fill(diLeptonMom.pt(), diLeptonMom.eta(), diLeptonMom.phi(), diLeptonMom.mass(), weight);

  

  // compute the red met
  redMETComputer_std->compute(muonLead->p4(), muonLead->track()->ptError(),
			      muonSubLead->p4(), muonSubLead->track()->ptError(),
			      jetMomenta,
			      met->p4());
  redMETComputer_tuneA->compute(muonLead->p4(), muonLead->track()->ptError(),
				muonSubLead->p4(), muonSubLead->track()->ptError(),
				jetMomenta,
				met->p4());
  redMETComputer_tuneB->compute(muonLead->p4(), muonLead->track()->ptError(),
				muonSubLead->p4(), muonSubLead->track()->ptError(),
				jetMomenta,
				met->p4());

  hRedMetStd_cut0->Fill(redMETComputer_std, met->pt(), weight);
			
  if(fabs(diLeptonMom.mass()-91.)>15.) return;
  
  // =====================================================================
  // cut1: apply mass window on the Z mass
  hEventCounter->Fill(6);
  
  hMuonLead_cut1->Fill(muonLead, vtx, weight);
  hMuonSubLead_cut1->Fill(muonSubLead, vtx, weight);
  hDiLeptKin_cut1->Fill(diLeptonMom.pt(), diLeptonMom.eta(), diLeptonMom.phi(), diLeptonMom.mass(), weight);
  hRedMetStd_cut1->Fill(redMETComputer_std, met->pt(), weight);
  hRedMetTuneA_cut1->Fill(redMETComputer_tuneA, met->pt(), weight);
  hRedMetTuneB_cut1->Fill(redMETComputer_tuneB, met->pt(), weight);

  hMETKin_cut1->Fill(met->pt(), met->eta(), met->phi(), met->mass(), weight);  

//   HistoRedMET * hRedMetStd = 0;
//   HistoRedMET * hRedMetTuneA = 0;
//   HistoRedMET * hRedMetTuneB = 0;
  
  if(jetMomenta.size() == 0) { // 0 jet bin
    hEventCounter->Fill(7);
    hRedMetStd_J0_cut1->Fill(redMETComputer_std, met->pt(), weight);
    hRedMetTuneA_J0_cut1->Fill(redMETComputer_tuneA, met->pt(), weight);
    hRedMetTuneB_J0_cut1->Fill(redMETComputer_tuneB, met->pt(), weight);
    hMETKin_J0_cut1->Fill(met->pt(), met->eta(), met->phi(), met->mass(), weight);  

  } else if(jetMomenta.size() == 1) { // 1 jet bin
    hEventCounter->Fill(8);
    hRedMetStd_J1_cut1->Fill(redMETComputer_std, met->pt(), weight);
    hRedMetTuneA_J1_cut1->Fill(redMETComputer_tuneA, met->pt(), weight);
    hRedMetTuneB_J1_cut1->Fill(redMETComputer_tuneB, met->pt(), weight);
    hMETKin_J1_cut1->Fill(met->pt(), met->eta(), met->phi(), met->mass(), weight);  
  }




  for (pat::eventhypothesis::Looper<pat::Jet> jet = h.loopAs<pat::Jet>("jet"); jet; ++jet) {
    if(debug) cout << "\t jet: " << jet->pt() << ";" << jet->eta() << ";" << jet->phi() << std::endl;
    hJetKin_cut1->Fill(jet->pt(), jet->eta(), jet->phi(), jet->mass(), weight);
  }
  hJetKin_cut1->FillNObj(jetMomenta.size(), weight);


  for (pat::eventhypothesis::Looper<pat::Electron> elec = h.loopAs<pat::Electron>("electron"); elec; ++elec) {
    if(debug) cout << "\t e: " << elec->pt() << ";" << elec->eta() << ";" << elec->phi() << std::endl;
  }

  for (pat::eventhypothesis::Looper<pat::Muon> muon = h.loopAs<pat::Muon>("muon"); muon; ++muon) {
    if(debug) cout << "\t mu: " << muon->pt() << ";" << muon->eta() << ";" << muon->phi() << std::endl;
  }


  //if event is MC debug gen level event
  if(!event.isRealData())
    {
      if(debug) cout << "\t Generator level event " << flush;
      int igenpart(0);
      for (pat::eventhypothesis::Looper<reco::GenParticle> genpart = h.loopAs<reco::GenParticle>("genparticle"); genpart; ++genpart) 
	{
	  if(debug) cout << "\t" << genpart->pdgId() << " -> " << flush;  

	  int igenpartdau(0);
	  char buf[20];
	  sprintf(buf,"gendaughter_%d",igenpart);
	  for(pat::eventhypothesis::Looper<reco::GenParticle> genpartdau = h.loopAs<reco::GenParticle>(buf); genpartdau; ++genpartdau)
	    {
	      if(debug) cout << genpartdau->pdgId() << " (" << flush;

	      char buf[20];
	      sprintf(buf,"gendaughter_%d_%d",igenpart,igenpartdau);
	      for(pat::eventhypothesis::Looper<reco::GenParticle> genpartgdau = h.loopAs<reco::GenParticle>(buf); genpartgdau; ++genpartgdau)
		if(debug) cout << genpartgdau->pdgId() << " " << flush;
	      
	      cout << ") " << flush;
	      igenpartdau++;
	    }
	  igenpart++;
	}
      if(debug) cout << endl;
    }
  
  



}


void ZZllvvAnalyzer::endJob() {
  cout << "Tot. # of events pre skim: " << nEventPreSkim << endl;
  cout << "Tot. # of events after base filters: " << nEventBaseFilter << endl;
  cout << "Tot. # of events after skim: " << nEventSkim << endl;
  cout << "Tot. # of events: " << totNEvents << endl;
  hEventCounter->SetBinContent(1,nEventPreSkim);
  hEventCounter->SetBinContent(2,nEventBaseFilter);
  hEventCounter->SetBinContent(3,nEventSkim);
  hEventCounter->SetBinContent(4,totNEvents);

// //   // Write the histograms
  theFile->cd();
  hEventCounter->Write();
  hNVertexAll->Write();
  hMuonLead_cut0->Write();    
  hMuonSubLead_cut0->Write();
  hDiLeptKin_cut0->Write();

  hMuonLead_cut1->Write();    
  hMuonSubLead_cut1->Write();
  hDiLeptKin_cut1->Write();
  hRedMetStd_cut0->Write();

  hRedMetStd_cut1->Write();
  hRedMetStd_J0_cut1->Write();
  hRedMetStd_J1_cut1->Write();

  hRedMetTuneA_cut1->Write();
  hRedMetTuneA_J0_cut1->Write();
  hRedMetTuneA_J1_cut1->Write();

  hRedMetTuneB_cut1->Write();
  hRedMetTuneB_J0_cut1->Write();
  hRedMetTuneB_J1_cut1->Write();


  hJetKin_cut0->Write();
  hMETKin_cut0->Write();
  hJetKin_cut1->Write();
  hMETKin_cut1->Write();
  hMETKin_J0_cut1->Write();
  hMETKin_J1_cut1->Write();


  theFile->Close();
}



void ZZllvvAnalyzer::beginLuminosityBlock(const edm::LuminosityBlock & iLumi, const edm::EventSetup & iSetup) {

}

void ZZllvvAnalyzer::endLuminosityBlock(const edm::LuminosityBlock & iLumi, const edm::EventSetup & iSetup) {
  edm::Handle<edm::MergeableCounter> nEventPreSkim_lumi;
  iLumi.getByLabel("startCounter", nEventPreSkim_lumi);
  nEventPreSkim += nEventPreSkim_lumi->value;

  edm::Handle<edm::MergeableCounter> nEventBaseFilter_lumi;
  iLumi.getByLabel("preFilterCounter", nEventBaseFilter_lumi);
  nEventBaseFilter += nEventBaseFilter_lumi->value;

  edm::Handle<edm::MergeableCounter> nEventSkim_lumi;
  iLumi.getByLabel("mumuCounter", nEventSkim_lumi);
  nEventSkim += nEventSkim_lumi->value;


}
