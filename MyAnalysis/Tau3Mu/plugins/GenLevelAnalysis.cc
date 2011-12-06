

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/Handle.h"

// #include "DataFormats/VertexReco/interface/Vertex.h"
// #include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "DataFormats/Candidate/interface/Particle.h"

#include "MyAnalysis/Tau3Mu/src/Histograms.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h" 
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
//#include "DataFormats/MuonReco/interface/MuonEnergy.h" 


#include "DataFormats/L1Trigger/interface/L1MuonParticleFwd.h"
#include "DataFormats/L1Trigger/interface/L1MuonParticle.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/Common/interface/TriggerResults.h"

#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/IPTools/interface/IPTools.h"

#include "FWCore/Common/interface/TriggerNames.h"

#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TLorentzVector.h"
#include <TMath.h>
#include <iostream>
#include <map>

using namespace std;


// USEFUL DOCUMENTS:
// https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookGenParticleCandidate#GenPCand
// http://pdg.lbl.gov/mc_particle_id_contents.html


//-----------------------------------------------------------------

class MyGenEvent {
public:
  TLorentzVector theDs;
  int theDsCharge;
  TLorentzVector theTau;
  int theTauCharge;
  TLorentzVector theMu[3];
  int theMuCharge[3];  
//   TLorentzVector theMu2;
//   int theMu2Charge;  
//   TLorentzVector theMu3;
//   int theMu3Charge;  
  
 
  pair<int, int> minDPhiPair;

  pair<int, int> minDRPair;

  void closestPair() {
    int minDPhi = 999999;
    int minDR = 999999;

    for(int index1 = 0; index1 != 3; ++index1) {
      for(int index2 = index1+1; index2 != 3; ++index2) {

	if(theMu[index1].DeltaPhi(theMu[index2]) < minDPhi) {
	  minDPhiPair = make_pair(index1, index2);
	  minDPhi = theMu[index1].DeltaPhi(theMu[index2]);
	}

	if(theMu[index1].DeltaR(theMu[index2]) < minDR) {
	  minDRPair = make_pair(index1, index2);
	  minDR = theMu[index1].DeltaR(theMu[index2]);
	}

      }
    }
  }


private:
};

//-----------------------------------------------------------------

bool sortByPt(const reco::Candidate *part1, const reco::Candidate *part2) {

  return part1->pt() > part2->pt();
}


//-----------------------------------------------------------------
class GenLevelAnalysis : public edm::EDAnalyzer {
public:
  explicit GenLevelAnalysis(const edm::ParameterSet&);
  ~GenLevelAnalysis();

private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;


  
  HistoKin *hKinDs;
  HistoKin *hKinRecoDs;
  HistoKin *hKinRecoTau;

  HistoKin *hKinDs3RecoMatched;
  HistoKin *hKinDs2RecoMatched;

  HistoKin *hKinDs3RecoGoodMatched;
  HistoKin *hKinDs2RecoGoodMatched;

  HistoImpactParam *hd0MuonGood;
  HistoImpactParam *hd0MuonGoodMatched;


  HistoKin *hKinTau;
  HistoKin *hKinMu;
  HistoKin *hKinMuLead;
  HistoKin *hKinMuTrail;
  HistoKinPair *hKinDsVsMuLead;
  HistoKinPair *hKinClosestMuPhi;

  TH1F *hNRecoMuAll;
  TH1F *hNRecoMuMatched;
  TH1F *hNRecoMuGoodAll;
  TH1F *hNRecoMuGoodMatched;

  TH1F *hNRecoTkMuMatched;

  HistoKin *hKinDs3RecoMatched3L1Matched;
  HistoKin *hKinDs3RecoMatched2L1Matched;
  HistoKin *hKinDs3RecoMatched2L13p5Matched;
  HistoKin *hKinDs3RecoMatched2L15Matched;
  HistoKin *hKinDs3RecoMatchedHLTTau3Mu;

  int counter;
  int countInAccept;
  int counterMoreThan3Muons;
  int counterMoreThanOneds;
  int counterTaus;

};



//
// constants, enums and typedefs
//


//////////////////////////////////////////////////////////////////
// generically maximum
template <class T> const T& max ( const T& a, const T& b ) {
  return (b<a)?a:b;     // or: return comp(b,a)?a:b; for the comp version
}


//


GenLevelAnalysis::GenLevelAnalysis(const edm::ParameterSet& iConfig) {
  counter = 0;
  countInAccept = 0;
  counterMoreThan3Muons = 0;
  counterMoreThanOneds = 0;
  counterTaus = 0;
}

GenLevelAnalysis::~GenLevelAnalysis() {}


//
// member functions
//

// ------------ method called to for each event  ------------
void GenLevelAnalysis::analyze(const edm::Event& ev, const edm::EventSetup& iSetup) {


  cout << "--- new event ---" << endl;

  bool debug = false;

  double weight = 1.;

  using namespace edm;
  using namespace reco;
  using namespace std;
  
//   // get the gen level particles
//   Handle<HepMCProduct> hepProd ;
//   ev.getByLabel("generator",hepProd) ;
//   const HepMC::GenEvent * myGenEvent = hepProd->GetEvent();


  string mcTruthCollection = "genParticles";
  edm::Handle< reco::GenParticleCollection > genParticleHandle;
  ev.getByLabel(mcTruthCollection,genParticleHandle) ;
  const reco::GenParticleCollection *genParticleCollection = genParticleHandle.product();

  MyGenEvent genEvt;
  vector<const reco::Candidate *> muonsFromTau;
  vector<const reco::Candidate *> particlesDs;
  vector<const reco::Candidate *> particlesTau;


  
  reco::GenParticleCollection::const_iterator genPart;
  for(genPart=genParticleCollection->begin(); genPart!=genParticleCollection->end(); genPart++) {
    const reco::Candidate & cand = *genPart;                                                   

    if(abs(cand.pdgId()) == 431) { //D_s
      if(particlesDs.size() != 0) cout << "More than one Ds in this event" << endl;
      particlesDs.push_back(&cand);
    } else if(abs(cand.pdgId()) == 15) {//tau
      particlesTau.push_back(&cand);
    } else if(abs(cand.pdgId()) == 13) {//muon
    } else continue;

    const reco::Candidate * mother1 = cand.mother();
    const reco::Candidate * mother2 = cand.mother();

    
    // put the tau and the ds in the event
    if(abs(cand.pdgId()) == 15 && (abs(mother1->pdgId()) == 431 || abs(mother2->pdgId()) == 431)) { // this is a tau from Ds
      genEvt.theTau = TLorentzVector(cand.px(), cand.py(), cand.pz(), cand.energy());
      genEvt.theTauCharge = cand.pdgId();
	  
      const reco::Candidate* ds = 0;
      if(abs(mother1->pdgId()) == 431) ds = mother1;
      else if(abs(mother2->pdgId()) == 431) ds = mother2;
      genEvt.theDs = TLorentzVector(ds->px(), ds->py(), ds->pz(), ds->energy());
      genEvt.theDsCharge = ds->pdgId();

    }
  
    // these are the muons from the tau
    if(abs(mother1->pdgId()) == 15 || abs(mother2->pdgId()) == 15) {
      if(abs(cand.pdgId()) == 13) {
	if(debug) cout << "   Muon from tau, pt: " << cand.pt() << " eta: " << cand.eta() << endl;
// 	if(fabs(cand.pseudoRapidity()) < 2.4 && cand.perp() > 1) {
	  muonsFromTau.push_back(&cand);
// 	}
      }
    }

  }
  // sort the mu by pt
  sort(muonsFromTau.begin(), muonsFromTau.end(), sortByPt);


  if(muonsFromTau.size() == 3) {
    for(unsigned int index = 0; index != muonsFromTau.size(); ++index) {

      genEvt.theMu[index] = TLorentzVector(muonsFromTau[index]->px(),
					   muonsFromTau[index]->py(),
					   muonsFromTau[index]->pz(),
					   muonsFromTau[index]->energy());
      genEvt.theMuCharge[index] = muonsFromTau[index]->pdgId();
    }
  } else {
    cout << "Warning: could not find at leat 3 muons from tau within acceptance: " << muonsFromTau.size() << endl;
    return;
  }

  if(abs(genEvt.theDsCharge) != 431 ||  abs(genEvt.theTauCharge) != 15 ) {
    cout << "Warning: something fishy in this event, skipping" << endl;
    return;
  }


  // now fill the plots
  hKinDs->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  hKinTau->Fill(genEvt.theTau.Pt(), genEvt.theTau.Eta(), genEvt.theTau.Phi(), genEvt.theTau.M(), weight);
  hKinMu->Fill(genEvt.theMu[0].Pt(), genEvt.theMu[0].Eta(), genEvt.theMu[0].Phi(), genEvt.theMu[0].M(), weight);
  hKinMu->Fill(genEvt.theMu[1].Pt(), genEvt.theMu[1].Eta(), genEvt.theMu[1].Phi(), genEvt.theMu[1].M(), weight);
  hKinMu->Fill(genEvt.theMu[2].Pt(), genEvt.theMu[2].Eta(), genEvt.theMu[2].Phi(), genEvt.theMu[2].M(), weight);
  hKinMuLead->Fill(genEvt.theMu[0].Pt(), genEvt.theMu[0].Eta(), genEvt.theMu[0].Phi(), genEvt.theMu[0].M(), weight);
  hKinMuTrail->Fill(genEvt.theMu[2].Pt(), genEvt.theMu[2].Eta(), genEvt.theMu[2].Phi(), genEvt.theMu[2].M(), weight);
  hKinDsVsMuLead->Fill(genEvt.theDs.Pt(), genEvt.theMu[0].Pt(), -1, -1, -1, -1, weight);


  genEvt.closestPair();
  double minDeltaPhi = fabs(genEvt.theMu[genEvt.minDPhiPair.first].DeltaPhi(genEvt.theMu[genEvt.minDPhiPair.second]));
  double deltaR1 = genEvt.theMu[genEvt.minDPhiPair.first].DeltaR(genEvt.theMu[genEvt.minDPhiPair.second]);
  double deltaEta1 = fabs(genEvt.theMu[genEvt.minDPhiPair.first].Eta() - genEvt.theMu[genEvt.minDPhiPair.second].Eta());
  hKinClosestMuPhi->Fill(genEvt.theMu[genEvt.minDPhiPair.first].Pt(), genEvt.theMu[genEvt.minDPhiPair.second].Pt(), minDeltaPhi, deltaEta1, deltaR1, -1., weight);

  counter++;
  if(muonsFromTau.size() > 2) {
    countInAccept++;
    if(muonsFromTau.size() > 3) {
      counterMoreThan3Muons++;
    }
  }  
    
  if(particlesTau.size() > 1) counterTaus++;
  if(particlesDs.size() > 1) counterMoreThanOneds++;
    

  // ------------------------------------------------------------------------------------------------
  // RECO level analysis

  string theMuonLabel = "muons";
  string theVertexLabel = "offlinePrimaryVerticesWithBS";

  // get the muon container
  edm::Handle<MuonCollection> muons;
  ev.getByLabel(theMuonLabel,muons);
  
  // get the vertex collection
  edm::Handle< std::vector<reco::Vertex> > pvHandle;
  ev.getByLabel(theMuonLabel, pvHandle );


  // get the PV
  reco::Vertex primaryVertex;
  if(pvHandle.isValid()) {
    primaryVertex = pvHandle->at(0); 
  }

  // this is needed by the IPTools methods from the tracking group
  edm::ESHandle<TransientTrackBuilder> trackBuilder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder); 

  int nTotal = 0;
  int nGood = 0;
  int nMatched = 0;
  int nMatchedGood = 0;

  TLorentzVector recoTau;
  
  // check the validity of the collection
  if(muons.isValid()){
    for (MuonCollection::const_iterator recoMu = muons->begin();
         recoMu!=muons->end(); ++recoMu){ // loop over all muons
      double eta = (*recoMu).eta();
      double phi = (*recoMu).phi();
      double pt = (*recoMu).pt();

      string muonType = "";
      if(recoMu->isGlobalMuon()) muonType = " Glb";
      if(recoMu->isStandAloneMuon()) muonType = muonType + " STA";
      if(recoMu->isTrackerMuon()) muonType = muonType + " Trk";

      cout << "[MuonAnalysis] New Muon found:" << muonType << endl;
      cout << "-- eta: " << eta << " phi: " << phi << " pt: " << pt << endl;       

      TLorentzVector recoMuonMom(recoMu->px(), recoMu->py(), recoMu->pz(), recoMu->energy());

      bool isGoodMu = muon::isGoodMuon(*recoMu, muon::TMOneStationTight);
      double d0_corr = 0;
      double d0_err = 0;
      if(isGoodMu) {
	nGood++;
	cout << "Good" << endl;
	// compute the impact parameter significance
	reco::TrackRef innerTrack = (*recoMu).innerTrack(); 
	if ( innerTrack.isNonnull() && innerTrack.isAvailable() ) {
	  reco::TransientTrack tt = trackBuilder->build(innerTrack);
// 	  std::pair<bool,Measurement1D> result = IPTools::absoluteTransverseImpactParameter(tt, primaryVertex);
	  std::pair<bool,Measurement1D> result = IPTools::absoluteImpactParameter3D(tt, primaryVertex);

	  d0_corr = result.second.value();
	  d0_err = result.second.error();
	  cout << "d0: " << d0_corr << " d0 err: " <<  d0_err << endl;
	  hd0MuonGood->Fill(d0_corr, d0_err, weight);
	}

      }


      nTotal++;
      for(int index = 0; index != 3; ++index) {
	double deltar = recoMuonMom.DeltaR(genEvt.theMu[index]);
	cout << "   MC: " << index << " eta: " << genEvt.theMu[index].Eta() << " phi: " << genEvt.theMu[index].Phi()
	     << " pt: " << genEvt.theMu[index].Pt() << " DR: " << recoMuonMom.DeltaR(genEvt.theMu[index]) << endl;
	if(deltar < 0.05) {
	  cout << " matched!" << endl;
	  nMatched++;
	  recoTau+= recoMuonMom;
	  if(isGoodMu) {
	    nMatchedGood++;
	    hd0MuonGoodMatched->Fill(d0_corr, d0_err, weight);
	  }

	}
      }
	
      
    }
  }

  hNRecoMuAll->Fill(nTotal, weight);
  hNRecoMuMatched->Fill(nMatched, weight);
  hNRecoMuGoodAll->Fill(nGood, weight);

  hNRecoMuGoodMatched->Fill(nMatchedGood, weight);
  if(nMatched >= 3) {
    hKinDs3RecoMatched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
    hKinRecoTau->Fill(recoTau.Pt(), recoTau.Eta(), recoTau.Phi(), recoTau.M(), weight);
  } 
  if(nMatched >= 2) {
    hKinDs2RecoMatched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }
  if(nMatchedGood >= 3) {
    hKinDs3RecoGoodMatched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }
  if(nMatchedGood >= 2) {
    hKinDs2RecoGoodMatched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }




  // ------------------------------------------------------------------------------------------------
  // trigger analysis

  // some counters/flags from trigger info
  int nL1Muons=0;
  int nL1MuonsPt3p5=0;
  int nL1MuonsPt5=0;
  bool tau3MuTrig = false;

  // count number of L1 Muons at correct BX
  // no matching to reco by now. it will require some attention for multiples match, and the phi at MS2
  edm::Handle<l1extra::L1MuonParticleCollection> l1Muon; 
  ev.getByLabel(edm::InputTag("l1extraParticles",""), l1Muon);
  for(l1extra::L1MuonParticleCollection::const_iterator it=l1Muon->begin(); it!=l1Muon->end(); it++){
    if (it->bx()==0){             
      double l1pt=it->et();
      double eta=it->eta();
      double phi=it->phi();
      double charge=it->charge();
      nL1Muons++;
      if (l1pt>=3.5) nL1MuonsPt3p5++;
      if (l1pt>=5.0) nL1MuonsPt5++;
    }
  }
  cout<<"Found "<<nL1Muons<<" L1 Muons"<<endl;

  // check fired HLT paths
  edm::Handle<edm::TriggerResults> hltresults;
  ev.getByLabel("TriggerResults", hltresults);
  if (hltresults.isValid()) {
    const edm::TriggerNames TrigNames_ = ev.triggerNames(*hltresults);
    const int ntrigs = hltresults->size();
    for (int itr=0; itr<ntrigs; itr++){
      if (!hltresults->accept(itr)) continue;
      TString trigName=TrigNames_.triggerName(itr);
      //cout<<"Found HLT path "<< trigName<<endl;
      if (trigName=="HLT_TripleMu0_TauTo3Mu_v1") tau3MuTrig=true;
    }
  }
  else
    { 
      cout<<"Trigger results not found"<<endl;
    }
  
  
  
  if (nL1Muons>=3 && nMatched>=3){
    hKinDs3RecoMatched3L1Matched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }
  if (nL1Muons>=2 && nMatched>=3){
    hKinDs3RecoMatched2L1Matched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }
  if (nL1MuonsPt3p5>=2 && nMatched>=3){
    hKinDs3RecoMatched2L13p5Matched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }
  if (nL1MuonsPt5>=2 && nMatched>=3){
    hKinDs3RecoMatched2L15Matched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }
  if (nMatched>=3 && tau3MuTrig){
    hKinDs3RecoMatchedHLTTau3Mu->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }



}

// ------------ method called once each job just before starting event loop  ------------
void GenLevelAnalysis::beginJob() {
  cout << "begin job" << endl;
  edm::Service<TFileService> fs;

  hKinDs  = new HistoKin("Ds",*fs);
  hKinRecoDs  = new HistoKin("RecoDs",*fs);
  hKinRecoTau  = new HistoKin("RecoTau",*fs);

  hKinDs3RecoMatched  = new HistoKin("Ds3RecoMatched",*fs);
  hKinDs2RecoMatched  = new HistoKin("Ds2RecoMatched",*fs);
  hKinDs3RecoGoodMatched  = new HistoKin("Ds3RecoGoodMatched",*fs);
  hKinDs2RecoGoodMatched  = new HistoKin("Ds2RecoGoodMatched",*fs);

  hd0MuonGood = new HistoImpactParam("d0MuonGood", *fs);
  hd0MuonGoodMatched = new HistoImpactParam("d0MuonGoodMatched", *fs);


  hKinDs3RecoMatched3L1Matched  = new HistoKin("Ds3RecoMatched3L1Matched",*fs);
  hKinDs3RecoMatched2L1Matched  = new HistoKin("Ds3RecoMatched2L1Matched",*fs);
  hKinDs3RecoMatched2L13p5Matched  = new HistoKin("Ds3RecoMatched2L13p5Matched",*fs);
  hKinDs3RecoMatched2L15Matched  = new HistoKin("Ds3RecoMatched2L15Matched",*fs);
  hKinDs3RecoMatchedHLTTau3Mu = new HistoKin("Ds3RecoMatchedHLTTau3Mu",*fs);
  

  hKinTau = new HistoKin("Tau",*fs);
  hKinMu  = new HistoKin("Mu",*fs);
  hKinMuLead  = new HistoKin("MuLead",*fs);
  hKinMuTrail  = new HistoKin("MuTrail",*fs);
  hKinDsVsMuLead = new HistoKinPair("DsVsMuLead", 0,10,*fs);
  hKinClosestMuPhi =  new HistoKinPair("ClosestMuPhi", 0,10,*fs);

  hNRecoMuAll       = fs->make<TH1F>("hNRecoMuAll","Total # reco muons; # of reco muons; #events",10,0,10);
  hNRecoMuMatched       = fs->make<TH1F>("hNRecoMuMatched","Total # reco muons; # of reco muons; #events",10,0,10);

  hNRecoMuGoodAll       = fs->make<TH1F>("hNRecoMuGoodAll","Total # reco muons; # of reco muons; #events",10,0,10);
  hNRecoMuGoodMatched   = fs->make<TH1F>("hNRecoMuGoodMatched","Total # reco muons; # of reco muons; #events",10,0,10);
  hNRecoTkMuMatched = fs->make<TH1F>("hNRecoTkMuMatched","Total # reco muons; # of reco muons; #events",10,0,10);

}


// ------------ method called nce each job just after ending the event loop  ------------
void 
GenLevelAnalysis::endJob() {
  cout << "Total # events: " << counter << endl;
  cout << "   # events with muons in acceptance: " << countInAccept << endl;
  cout << "   # events with more than 1 Ds: " << counterMoreThanOneds << endl;
  cout << "   # events with more than 3 muons: " << counterMoreThan3Muons << endl;
  cout << "   # events with more than 1 tau: " << counterTaus << endl;
}



#include "FWCore/Framework/interface/MakerMacros.h"  
DEFINE_FWK_MODULE( GenLevelAnalysis );
