

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
//#include "DataFormats/MuonReco/interface/MuonEnergy.h" 
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TLorentzVector.h"
#include <TMath.h>
#include <iostream>
#include <map>

using namespace std;


// #include "CLHEP/Units/GlobalPhysicalConstants.h"

// #include "Hgg/ClusteringWithPU/interface/SCwithPUhistos.h"
// #include "Hgg/ClusteringWithPU/interface/Utils.h"

// pdg particle numbering : higgs->25, Z0->23
// http://pdg.lbl.gov/mc_particle_id_contents.html


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


bool sortByPt(const HepMC::GenParticle *part1, const HepMC::GenParticle *part2) {

  return part1->momentum().perp() > part2->momentum().perp();
}



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

  HistoKin *hKinDs3RecoMatched;
  HistoKin *hKinDs2RecoMatched;
  HistoKin *hKinTau;
  HistoKin *hKinMu;
  HistoKin *hKinMuLead;
  HistoKin *hKinMuTrail;
  HistoKinPair *hKinDsVsMuLead;
  HistoKinPair *hKinClosestMuPhi;

  TH1F *hNRecoMuAll;
  TH1F *hNRecoMuMatched;
  TH1F *hNRecoTkMuMatched;

  
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
  bool debug = false;

  double weight = 1.;

  using namespace edm;
  using namespace reco;
  using namespace std;
  
  // get the gen level particles
  Handle<HepMCProduct> hepProd ;
  ev.getByLabel("generator",hepProd) ;
  const HepMC::GenEvent * myGenEvent = hepProd->GetEvent();


  string mcTruthCollection = "genParticles";

//   edm::Handle< reco::GenParticleCollection > genParticleHandle;
//   try { ev.getByLabel(mcTruthCollection, genParticleHandle); }
//   catch ( cms::Exception& ex ) { edm::LogWarning("HWWTreeDumper") << "Can't get MC Truth Collection: " << mcTruthCollection; }
//   const reco::GenParticleCollection *genParticleCollection = genParticleHandle.product();

  
//   reco::GenParticleCollection::const_iterator genPart;
//   for(genPart=genParticleCollection->begin(); genPart!=genParticleCollection->end(); genPart++) {
//     const reco::Candidate & cand = *genPart;                                                   
//     if(abs(cand.pdgId()) == 15) {
//       cout << "TAU, mother: " << cand.mother()->pdgId() << endl;
//       cout << "    # of mothers: " << cand.numberOfMothers() << endl;

//     }
//   }

  // TODO:
  // 1. plot the mother of all Ds
  // 2. plot the kinematics of all Ds
  // 3. plot the kinematics of all Taus
  
  // DOCUMENTS:
  // https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookGenParticleCandidate#GenPCand
  // http://pdg.lbl.gov/mc_particle_id_contents.html


  vector<HepMC::GenParticle *> muonsFromTau;
  vector<HepMC::GenParticle *> particlesDs;
  vector<HepMC::GenParticle *> particlesTau;

  MyGenEvent genEvt;

  cout << "--- new event ---" << endl;
  // loop over MC-truth particles
  for ( HepMC::GenEvent::particle_const_iterator part = myGenEvent->particles_begin();
	part != myGenEvent->particles_end(); ++part ) {

    HistoKin *histo = 0;

    if(abs((*part)->pdg_id()) == 431) { //D_s
      if(particlesDs.size() != 0) cout << "More than one Ds in this event" << endl;
      particlesDs.push_back(*part);
      histo = hKinDs;
    } else if(abs((*part)->pdg_id()) == 15) {//tau
      particlesTau.push_back(*part);
      histo = hKinTau;
    } else if(abs((*part)->pdg_id()) == 13) {//muon
      histo = hKinMu;
    } else continue;
    
    if(debug) std::cout << "- particle with pdg is: " << (*part)->pdg_id() << " with status: " << (*part)->status() << std::endl;

    HepMC::GenParticle* mother1  = 0;
    HepMC::GenParticle* mother2  = 0;

    // get the other mothers from the vertex
    if((*part)->production_vertex()) {
//       for(HepMC::GenVertex::particles_in_const_iterator mom = (*part)->production_vertex()->particles_begin(HepMC::parents);
// 	  mom != (*part)->production_vertex()->particles_end(HepMC::parents); ++mom) {
// 	cout << **mom << endl;
//       }
      
      if((*part)->production_vertex()->particles_begin(HepMC::parents) !=  (*part)->production_vertex()->particles_end(HepMC::parents))
	mother1 = *((*part)->production_vertex()->particles_begin(HepMC::parents));
    }

    if(mother1 !=0 && mother1->production_vertex()) {
      mother2 = *( mother1->production_vertex()->particles_begin(HepMC::parents));
    }

    if(debug) cout << "   mother1: " << mother1->pdg_id()
		   << " mother2: " << mother2->pdg_id() << endl;

    
    // put the tau and the ds in the event
    if(abs((*part)->pdg_id()) == 15 && (abs(mother1->pdg_id()) == 431 || abs(mother2->pdg_id()) == 431)) {
      genEvt.theTau = TLorentzVector((*part)->momentum().px(), (*part)->momentum().py(), (*part)->momentum().pz(), (*part)->momentum().e());
      genEvt.theTauCharge = (*part)->pdg_id();
	 
      HepMC::GenParticle* ds = 0;
      if(abs(mother1->pdg_id()) == 431) ds = mother1;
      else if(abs(mother2->pdg_id()) == 431) ds = mother2;
      genEvt.theDs = TLorentzVector(ds->momentum().px(), ds->momentum().py(), ds->momentum().pz(), ds->momentum().e());
      genEvt.theDsCharge = ds->pdg_id();
    }



       
    // these are the muons from the tau
    if(abs(mother1->pdg_id()) == 15 || abs(mother2->pdg_id()) == 15) {
      if(abs((*part)->pdg_id()) == 13) {
	if(debug) cout << "   Muon from tau, pt: " << (*part)->momentum().perp() << " eta: " << (*part)->momentum().pseudoRapidity() << endl;
// 	if(fabs((*part)->momentum().pseudoRapidity()) < 2.4 && (*part)->momentum().perp() > 1) {
	  muonsFromTau.push_back(*part);
// 	}
      }
    }

  }// loop over all MC-truth particles  - keep only electrons or photons 

  // sort them by pt
  sort(muonsFromTau.begin(), muonsFromTau.end(), sortByPt);


  if(muonsFromTau.size() == 3) {
    for(unsigned int index = 0; index != muonsFromTau.size(); ++index) {

      genEvt.theMu[index] = TLorentzVector(muonsFromTau[index]->momentum().px(),
					   muonsFromTau[index]->momentum().py(),
					   muonsFromTau[index]->momentum().pz(),
					   muonsFromTau[index]->momentum().e());
      genEvt.theMuCharge[index] = muonsFromTau[index]->pdg_id();
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
  // Take the muon container
  edm::Handle<MuonCollection> muons;
  ev.getByLabel(theMuonLabel,muons);
  
  int nTotal = 0;
  int nMatched = 0;

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

      nTotal++;
      for(int index = 0; index != 3; ++index) {
	double deltar = recoMuonMom.DeltaR(genEvt.theMu[index]);
	cout << "   MC: " << index << " eta: " << genEvt.theMu[index].Eta() << " phi: " << genEvt.theMu[index].Phi()
	     << " pt: " << genEvt.theMu[index].Pt() << " DR: " << recoMuonMom.DeltaR(genEvt.theMu[index]) << endl;
	if(deltar < 0.05) {
	  cout << " matched!" << endl;
	  nMatched++;
	  recoTau+= recoMuonMom;
	}
      }
	
      
    }

  }

  hNRecoMuAll->Fill(nTotal, weight);
  hNRecoMuMatched->Fill(nMatched, weight);
  
  if(nMatched >= 3) {
    hKinDs3RecoMatched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
    hKinRecoDs->Fill(recoTau.Pt(), recoTau.Eta(), recoTau.Phi(), recoTau.M(), weight);
  } 
  if(nMatched >= 2) {
    hKinDs2RecoMatched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }
}

// ------------ method called once each job just before starting event loop  ------------
void GenLevelAnalysis::beginJob() {
  cout << "begin job" << endl;
  edm::Service<TFileService> fs;

  hKinDs  = new HistoKin("Ds",*fs);
  hKinRecoDs  = new HistoKin("RecoDs",*fs);

  hKinDs3RecoMatched  = new HistoKin("Ds3RecoMatched",*fs);
  hKinDs2RecoMatched  = new HistoKin("Ds2RecoMatched",*fs);

  hKinTau = new HistoKin("Tau",*fs);
  hKinMu  = new HistoKin("Mu",*fs);
  hKinMuLead  = new HistoKin("MuLead",*fs);
  hKinMuTrail  = new HistoKin("MuTrail",*fs);
  hKinDsVsMuLead = new HistoKinPair("DsVsMuLead", 0,10,*fs);
  hKinClosestMuPhi =  new HistoKinPair("ClosestMuPhi", 0,10,*fs);

  hNRecoMuAll       = fs->make<TH1F>("hNRecoMuAll","Total # reco muons; # of reco muons; #events",10,0,10);
  hNRecoMuMatched   = fs->make<TH1F>("hNRecoMuMatched","Total # reco muons; # of reco muons; #events",10,0,10);
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
