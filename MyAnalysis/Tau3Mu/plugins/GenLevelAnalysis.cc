#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

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
#include <DataFormats/VertexReco/interface/VertexFwd.h>

#include "FWCore/Common/interface/TriggerNames.h"

#include "DataFormats/GeometryCommonDetAlgo/interface/GlobalError.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"

#include "Math/SMatrix.h"
#include "Math/VectorUtil.h"
#include "TVector3.h"
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TLorentzVector.h"
#include <TMath.h>
#include <TMatrixD.h>
#include <iostream>
#include <map>
#include <set>
#include <TROOT.h>
//#include "SMatrix.h"
using namespace std;
using namespace reco;
using namespace edm;

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

  pair<int, int> maxDPhiPair;
  pair<int, int> maxDRPair;

  void closestPair() {

    double minDPhi = 999999;
    double minDR = 999999;

    double maxDPhi = 0;
    double maxDR = 0;

    for(int index1 = 0; index1 != 3; ++index1) {
      for(int index2 = index1+1; index2 != 3; ++index2) {

	if(theMu[index1].DeltaPhi(theMu[index2]) < minDPhi) {
	  minDPhiPair = make_pair(index1, index2);
	  minDPhi = theMu[index1].DeltaPhi(theMu[index2]);
	}

	if(theMu[index1].DeltaPhi(theMu[index2]) > maxDPhi) {
	  maxDPhiPair = make_pair(index1, index2);
	  maxDPhi = theMu[index1].DeltaPhi(theMu[index2]);
	}

	if(theMu[index1].DeltaR(theMu[index2]) < minDR) {
	  minDRPair = make_pair(index1, index2);
	  minDR = theMu[index1].DeltaR(theMu[index2]);
	}

	if(theMu[index1].DeltaR(theMu[index2]) > maxDR) {
	  maxDRPair = make_pair(index1, index2);
	  maxDR = theMu[index1].DeltaR(theMu[index2]);
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

bool sortMuByPt(const reco::Muon mu1, const reco::Muon mu2) {

  return mu1.pt() > mu2.pt();
}

//-----------------------------------------------------------------
class GenLevelAnalysis : public edm::EDAnalyzer {
public:
  explicit GenLevelAnalysis(const edm::ParameterSet&);
  ~GenLevelAnalysis();

private:
  virtual void beginJob();
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob();
  virtual void L1Match(const edm::Event&, TLorentzVector* , std::vector<pair<TLorentzVector,int> >&);
  virtual void RecoMatch(edm::Handle<reco::MuonCollection>&, TLorentzVector*, reco::MuonCollection *);

  
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


  TH1F *hNVertex;

  HistoKin *hKinDs3L1Matched;
  HistoKin *hKinDs2L1Matched;
  HistoKin *hKinDs2L13p5Matched;
  HistoKin *hKinDs2L15Matched;
  HistoKin *hKinDsHLTTau3Mu;

  TH1F* hDiMuInvMass,* hGoodDiMuInvMass ;
  TH1F* h1MuL1pass,*h2MuL1pass, *h3MuL1pass,* hInputL1;
  TH1F* h1MuL1Matchedpass,*h2MuL1Matchedpass, *h3MuL1Matchedpass;
  TH1F * hNDs, *hNmuFromTau, *hMuMaxDistance;
  TH1F* hNL1Cand,*hNL1MatchedCand;
  TH2F* hL1EtaPt,*hL1MatchedEtaPt,*hMinMuDRVsPtDs;
  TH1F *hInputL1_2cands, *h2MuL1Matchedpass_2cands;

  TH1F *hDL,*hDLSig,*hsvchi2;
  TH1F* hvtxResx,*hvtxResz,*hvtxResy;
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

void GenLevelAnalysis::L1Match(const edm::Event& ev, TLorentzVector* genMus, std::vector<std::pair<TLorentzVector,int> >& matched){

  edm::Handle<l1extra::L1MuonParticleCollection> l1Muon; 
  ev.getByLabel(edm::InputTag("l1extraParticles",""), l1Muon);

  bool runMatch=true;

  std::vector<int> muMatches, l1Matches;

  while (runMatch){
    
    double dRtmp=0.1;

    //cout << "MATCHING TRY starting from dR= " << dRtmp << endl;

    TLorentzVector l1Match4Mom;

    int muIndex,l1Index;

    bool oneMatch=false;
    
    for (int k=0; k<3; ++k){
      
      bool alreadyMatchedMu=false;

      for (uint i=0;i<muMatches.size(); ++i){
	if (muMatches[i]==k) alreadyMatchedMu=true;
	//if (alreadyMatchedMu) cout << "alredy matched mu " << k << endl;
      }
      
      if (alreadyMatchedMu) continue;
    
      int l1counter=-1;
    
      for(l1extra::L1MuonParticleCollection::const_iterator it=l1Muon->begin(); it!=l1Muon->end(); it++){

	l1counter++;

	bool alreadyMatchedl1=false;

	for (uint i=0;i<l1Matches.size(); ++i){
	  if (l1Matches[i]==l1counter) alreadyMatchedl1=true;
	  //if (alreadyMatchedl1) cout << "alredy matched L1 " << l1counter << endl;
	}

	if (alreadyMatchedl1) continue;
	
       if (it->bx()==0){

	 TLorentzVector l1p4=TLorentzVector(it->px(),it->py(),it->pz(),it->energy());
	 //	 double distance=l1p4.DeltaR(genMus[k]);
	 double distance=fabs(l1p4.Eta()-genMus[k].Eta());
	 //cout << " distance between mu " << k << " and l1 " << l1counter << " = " << distance << endl;
	 if (distance<dRtmp){
	   oneMatch=true;
	   dRtmp=distance;
	   l1Match4Mom=l1p4;
	   l1Index=l1counter;
	   muIndex=k;

	 }
       }
      }
    }

    if (oneMatch){
      muMatches.push_back(muIndex);
      l1Matches.push_back(l1Index);
      matched.push_back(make_pair(l1Match4Mom,muIndex));
      //cout << "MATCHED mu " << muIndex << " with l1 " << l1Index << " dR " << dRtmp << endl;
      
    }

    else runMatch=false;

    if (matched.size()==3) runMatch=false;
  }
}

void GenLevelAnalysis::RecoMatch(edm::Handle<reco::MuonCollection>& recoMus, TLorentzVector* genMus, reco::MuonCollection * myMatches ){
  cout << "Doing Reco Match" << endl;

  bool runMatch=true;

  std::vector<int> muMatches, recoMatches;

  while (runMatch){
    
    double dRtmp=0.05;
    
    reco::MuonCollection::const_iterator RecoMatch;

    int muIndex,recoIndex;

    bool oneMatch=false;
    
    for (int k=0; k<3; ++k){
      
      bool alreadyMatchedMu=false;

      for (uint i=0;i<muMatches.size(); ++i){
	if (muMatches[i]==k) alreadyMatchedMu=true;
	//if (alreadyMatchedMu) cout << "alredy matched mu " << k << endl;
      }
      
      if (alreadyMatchedMu) continue;
    
      int recocounter=-1;
    
      for(reco::MuonCollection::const_iterator it=recoMus->begin(); it!=recoMus->end(); it++){

	recocounter++;

	bool alreadyMatchedReco=false;

	for (uint i=0;i<recoMatches.size(); ++i){
	  if (recoMatches[i]==recocounter) alreadyMatchedReco=true;
	  //if (alreadyMatchedl1) cout << "alredy matched L1 " << l1counter << endl;
	}

	if (alreadyMatchedReco) continue;

	 TLorentzVector recop4=TLorentzVector(it->px(),it->py(),it->pz(),it->energy());
	 double distance=recop4.DeltaR(genMus[k]);

	 if (distance<dRtmp){
	   oneMatch=true;
	   dRtmp=distance;
	   RecoMatch=it;
	   recoIndex=recocounter;
	   muIndex=k;

	 }
       
      }
    }

    if (oneMatch){
      muMatches.push_back(muIndex);
      recoMatches.push_back(recoIndex);
      myMatches->push_back(*RecoMatch);
    }

    else runMatch=false;

    if (myMatches->size()==3) runMatch=false;
  }

  cout << "Done Reco Matching" << endl;
}
  


 


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

  bool isDs=false, isTau=false, is3Mu=false;

  bool only1Ds=true;
  
  reco::GenParticleCollection::const_iterator genPart;
  for(genPart=genParticleCollection->begin(); genPart!=genParticleCollection->end(); genPart++) {
    const reco::Candidate & cand = *genPart;                                                   
    
   
     if (abs(cand.pdgId()) == 431){

       cout << "------------------Ds------------" << endl;      
       //nds++;
       int ndau=cand.numberOfDaughters();
       cout << "Ds Status" << cand.status() << endl;
       cout << "Ds Daughters: " ;
       for(int k = 0; k < ndau; ++ k) {
	 const Candidate * d = cand.daughter( k );
	int dauId = d->pdgId();
	cout << dauId << ", ";
	if (dauId==333 || abs(dauId)==15) {
	  cout << endl;
	  //  nphidau++;
	  int ndau1=d->numberOfDaughters();
	  if (dauId==333)cout << " : Phi doughters: " ;
	  else cout << " : Tau doughters: " ;

	  for (int l=0; l<ndau1; l++){
	    const Candidate * d1 = d->daughter( l );
	    cout << d1->pdgId() << ", ";
	  }
	}
       }
      cout << endl;
     }

    
     //cout << " Ds Number " << nds << endl;
//cout << "--------------------------------------------" << endl;
    if(abs(cand.pdgId()) == 431) { //D_s
      if(particlesDs.size() != 0) {cout << "More than one Ds in this event" << endl; only1Ds=false;}
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
      isTau=true;
	  
      const reco::Candidate* ds = 0;
      if(abs(mother1->pdgId()) == 431) ds = mother1;
      else if(abs(mother2->pdgId()) == 431) ds = mother2;
      genEvt.theDs = TLorentzVector(ds->px(), ds->py(), ds->pz(), ds->energy());
      genEvt.theDsCharge = ds->pdgId();
      isDs=true;
    }
  
    // these are the muons from the tau
    if(abs(mother1->pdgId()) == 15 || abs(mother2->pdgId()) == 15) {
      if(abs(cand.pdgId()) == 13) {
	if(debug) cout << "   Muon from tau, pt: " << cand.pt() << " eta: " << cand.eta() << endl;
	//	if(fabs(cand.pseudoRapidity()) < 2.4 && cand.perp() > 1) {
	  muonsFromTau.push_back(&cand);
	  if ( muonsFromTau.size()==3) is3Mu=true;
	  //	}
      }
    }

  }

  if (!isDs || !isTau || !is3Mu) {cout << "bad event " << endl; return;}

  hNDs->Fill(particlesDs.size());
  // sort the mu by pt
  sort(muonsFromTau.begin(), muonsFromTau.end(), sortByPt);

  hNmuFromTau->Fill(muonsFromTau.size());

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

  hMuMaxDistance->Fill(genEvt.theMu[genEvt.maxDPhiPair.first].DeltaR(genEvt.theMu[genEvt.maxDPhiPair.second]));

  bool AtLeast3Mu=false;

  counter++;
  if(muonsFromTau.size() > 2) {
    countInAccept++;
    AtLeast3Mu=true;
    if(muonsFromTau.size() > 3) {
      counterMoreThan3Muons++;
    }
  }  

  if (AtLeast3Mu) hMinMuDRVsPtDs->Fill(genEvt.theDs.Pt(),deltaR1);

  if (particlesDs.size() >0 && AtLeast3Mu && only1Ds) hInputL1->Fill(genEvt.theDs.Pt()); 

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
  ev.getByLabel(theVertexLabel, pvHandle );


  // get the PV
  bool isPvGood=false;
  reco::Vertex primaryVertex;

  if(pvHandle.isValid()) {
    isPvGood=true;
    primaryVertex = pvHandle->at(0); 
    hNVertex->Fill(pvHandle->size(),weight);
  }


  // this is needed by the IPTools methods from the tracking group
  edm::ESHandle<TransientTrackBuilder> trackBuilder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder); 

  int nTotal = 0;
  int nGood = 0;
  int nMatched = 0;
  int nMatchedGood = 0;

  TLorentzVector recoTau;

  MuonCollection *MyMatchedMuons= new MuonCollection;
  bool DiMuGood=false;

  std::vector<TransientTrack> tt4vertex, tt4Trivertex;

   // check the validity of the collection
  if(muons.isValid()){
    RecoMatch(muons,genEvt.theMu,MyMatchedMuons);
    sort(MyMatchedMuons->begin(), MyMatchedMuons->end(), sortMuByPt);

    for (MuonCollection::const_iterator recoMu = MyMatchedMuons->begin();
         recoMu!=MyMatchedMuons->end(); ++recoMu){ // loop over all muons

      nTotal++;

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

      reco::TrackRef innerTrack = (*recoMu).innerTrack(); 
      reco::TransientTrack tt;
      if ( innerTrack.isNonnull() && innerTrack.isAvailable() ) {
	tt = trackBuilder->build(innerTrack);
	tt4Trivertex.push_back(tt);
	if (nTotal<3) tt4vertex.push_back(tt); //only the two hardest
      }

      if(isGoodMu) {
	nGood++;
	if (nTotal==2 && nGood==2) DiMuGood=true;
	cout << "Good" << endl;
	// compute the impact parameter significance
	if ( innerTrack.isNonnull() && innerTrack.isAvailable() ) {

// 	  std::pair<bool,Measurement1D> result = IPTools::absoluteTransverseImpactParameter(tt, primaryVertex);
	  std::pair<bool,Measurement1D> result = IPTools::absoluteImpactParameter3D(tt, primaryVertex);

	  d0_corr = result.second.value();
	  d0_err = result.second.error();
	  cout << "d0: " << d0_corr << " d0 err: " <<  d0_err << endl;
	  hd0MuonGood->Fill(d0_corr, d0_err, weight);
	}

      }
      
    }
  }

  TLorentzVector DiMuMom;  
  if (MyMatchedMuons->size()>=2){
    TLorentzVector mu1p4=TLorentzVector((*MyMatchedMuons)[0].px(),(*MyMatchedMuons)[0].py(),(*MyMatchedMuons)[0].pz(),(*MyMatchedMuons)[0].energy());
    TLorentzVector mu2p4=TLorentzVector((*MyMatchedMuons)[1].px(),(*MyMatchedMuons)[1].py(),(*MyMatchedMuons)[1].pz(),(*MyMatchedMuons)[1].energy());
    DiMuMom=mu1p4+mu2p4;
    double DiMuMass=(mu1p4+mu2p4).M();
    hDiMuInvMass->Fill(DiMuMass);
    if (DiMuGood) hGoodDiMuInvMass->Fill(DiMuMass);
  }

  TransientVertex tv,tv3;
  
  GlobalPoint v(100.,100.,100);
  double vchi2=0.; 
  GlobalError errv(0.,0.,0.,0.,0.,0.);

  GlobalPoint v3(100.,100.,100);
  double v3chi2=0.; 
  GlobalError errv3(0.,0.,0.,0.,0.,0.);
  
  if (tt4vertex.size()>=2){

    AdaptiveVertexFitter avf;
    tv=avf.vertex(tt4vertex);       

    if (tv.isValid()) { 
      vchi2=tv.normalisedChiSquared();
      v = tv.position();
      errv = tv.positionError();

       if (tt4Trivertex.size()==3){ //try the vertex with 3 muons
	tv3=avf.vertex(tt4Trivertex);
	if (tv3.isValid()){
	  v3chi2=tv3.normalisedChiSquared();
	  v3 = tv3.position();
	  errv3 = tv3.positionError();
	  hvtxResx->Fill(v.x()-v3.x());
	  hvtxResy->Fill(v.y()-v3.y());
	  hvtxResz->Fill(v.z()-v3.z());
	}
       }

       if (isPvGood){
	double lxy=((v.x()-primaryVertex.x())*DiMuMom.Px()+(v.y()-primaryVertex.y())*DiMuMom.Py())*DiMuMom.M()/pow(DiMuMom.Pt(),2);

	TVector3 pperp(DiMuMom.Px(), DiMuMom.Py(), 0);
	//AlgebraicVector vpperp(3);
	ROOT::Math::SVector<double,3> vpperp;
	vpperp[0] = pperp.x();
	vpperp[1] = pperp.y();
	vpperp[2] = 0.;

	GlobalError sVe= (Vertex(tv)).error();
	GlobalError PVe = primaryVertex.error();

	//AlgebraicSymMatrix33 
	ROOT::Math::SMatrix<double,3,3> vXYe = sVe.matrix() + PVe.matrix();
	double lxyErr = sqrt(ROOT::Math::Similarity(vXYe,vpperp))*DiMuMom.M()/(pperp.Perp2());
	hDL->Fill(lxy);
	hDLSig->Fill(lxy/lxyErr);
	hsvchi2->Fill(vchi2);
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
      //double eta=it->eta();
      //double phi=it->phi();
      //double charge=it->charge();
      //cout << "Index " << l1count << " Pt " << it->pt() << endl;
      hL1EtaPt->Fill(fabs(it->eta()),it->pt());
      nL1Muons++;
      if (l1pt>=3.5) nL1MuonsPt3p5++;
      if (l1pt>=5.0) nL1MuonsPt5++;
    }
  }

  cout<<"Found "<<nL1Muons<<" L1 Muons"<<endl;
  cout << "three muons " << AtLeast3Mu << endl;
  std::vector<pair<TLorentzVector,int> > L1Matches;

  if (AtLeast3Mu) L1Match(ev,genEvt.theMu, L1Matches);

  int nL1MatchedMuons=L1Matches.size();

  for(int s=0; s<nL1MatchedMuons; s++){
    double pt=(L1Matches[s].first).Pt();
    double eta=(L1Matches[s].first).Eta();
    hL1MatchedEtaPt->Fill(fabs(eta),pt);
  }

  hNL1Cand->Fill(nL1Muons);
  hNL1MatchedCand->Fill(nL1MatchedMuons);

  if (particlesDs.size() >0 && AtLeast3Mu && nL1Muons > 0) h1MuL1pass->Fill(genEvt.theDs.Pt());
  if (particlesDs.size() >0 && AtLeast3Mu && nL1Muons > 1) h2MuL1pass->Fill(genEvt.theDs.Pt());
  if (particlesDs.size() >0 && AtLeast3Mu && nL1Muons > 2) h3MuL1pass->Fill(genEvt.theDs.Pt());

  if (particlesDs.size() >0 && AtLeast3Mu && nL1MatchedMuons > 0 && only1Ds){
    h1MuL1Matchedpass->Fill(genEvt.theDs.Pt());

    /*if (genEvt.theDs.Pt() > 0){

      cout << "Check L1 Match:------------------------------------------------------------" << endl;
      cout << "N L1 cands = " << nL1Muons << " N Matched cands = " << nL1MatchedMuons << endl;
      cout << "ALL L1 csnd variables: " << endl;
      for(l1extra::L1MuonParticleCollection::const_iterator it=l1Muon->begin(); it!=l1Muon->end(); it++){
	if (it->bx()==0){
	  cout << "pt " << it->pt() << "  eta " << it->eta() << "  phi " << it->phi() << endl; 
	}
      }
      cout << " Matched L1 cand variables: " << endl;
      for (int j=0; j<nL1MatchedMuons; j++){
	cout << "pt " << (L1Matches[j].first).Pt() << "  eta " << (L1Matches[j].first).Eta() << "  phi " << (L1Matches[j].first).Phi()<< " Mu Match " << L1Matches[j].second << " dR= " << (L1Matches[j].first).DeltaR(genEvt.theMu[L1Matches[j].second])  << endl; 
      }
      cout << " GenMu variables: " << endl;
      for (int j=0; j<3; j++){
	cout << "pt " << genEvt.theMu[j].Pt() << "  eta " << genEvt.theMu[j].Eta() << "  phi " << genEvt.theMu[j].Phi()<< " Mu Num " << j  << endl; 
      }

      }*/
  }

  if (particlesDs.size() >0 && AtLeast3Mu && nL1MatchedMuons > 1 && only1Ds) {
    h2MuL1Matchedpass->Fill(genEvt.theDs.Pt());
  }

  if (particlesDs.size() >0 && AtLeast3Mu && nL1MatchedMuons == 2 && nL1Muons == 2) {
    h2MuL1Matchedpass_2cands->Fill(genEvt.theDs.Pt());
  }

  if (particlesDs.size() >0 && AtLeast3Mu &&  nL1Muons == 2) {hInputL1_2cands->Fill(genEvt.theDs.Pt());}

  if (particlesDs.size() >0 && AtLeast3Mu && nL1MatchedMuons > 2 && only1Ds) h3MuL1Matchedpass->Fill(genEvt.theDs.Pt());


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
  
  
  
  if (nL1Muons>=3 && nMatchedGood>=3){
    hKinDs3RecoMatched3L1Matched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }
  if (nL1Muons>=2 && nMatchedGood>=3){
    hKinDs3RecoMatched2L1Matched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }
  if (nL1MuonsPt3p5>=2 && nMatchedGood>=3){
    hKinDs3RecoMatched2L13p5Matched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }
  if (nL1MuonsPt5>=2 && nMatchedGood>=3){
    hKinDs3RecoMatched2L15Matched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }
if (tau3MuTrig && nMatchedGood>=3){
    hKinDs3RecoMatchedHLTTau3Mu->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }

if (nL1Muons>=3){
  hKinDs3L1Matched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }
if (nL1Muons>=2){
  hKinDs2L1Matched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
 }
if (nL1MuonsPt3p5>=2){
  hKinDs2L13p5Matched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
 }
if (nL1MuonsPt5>=2){
    hKinDs2L15Matched->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }
if (tau3MuTrig){
  hKinDsHLTTau3Mu->Fill(genEvt.theDs.Pt(), genEvt.theDs.Eta(), genEvt.theDs.Phi(), genEvt.theDs.M(), weight);
  }


 delete MyMatchedMuons;
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


  hKinDs3RecoMatched3L1Matched  = new HistoKin("Ds3RecoGoodMatched3L1Matched",*fs);
  hKinDs3RecoMatched2L1Matched  = new HistoKin("Ds3RecoGoodMatched2L1Matched",*fs);
  hKinDs3RecoMatched2L13p5Matched  = new HistoKin("Ds3RecoGoodMatched2L13p5Matched",*fs);
  hKinDs3RecoMatched2L15Matched  = new HistoKin("Ds3RecoGoodMatched2L15Matched",*fs);
  hKinDs3RecoMatchedHLTTau3Mu = new HistoKin("Ds3RecoGoodMatchedHLTTau3Mu",*fs);

  hKinDs3L1Matched  =    new HistoKin("Ds3L1Matched",*fs);
  hKinDs2L1Matched  =    new HistoKin("Ds2L1Matched",*fs);
  hKinDs2L13p5Matched  = new HistoKin("Ds2L13p5Matched",*fs);
  hKinDs2L15Matched  =   new HistoKin("Ds2L15Matched",*fs);
  hKinDsHLTTau3Mu =      new HistoKin("DsHLTTau3Mu",*fs);
  

  hKinTau = new HistoKin("Tau",*fs);
  hKinMu  = new HistoKin("Mu",*fs);
  hKinMuLead  = new HistoKin("MuLead",*fs);
  hKinMuTrail  = new HistoKin("MuTrail",*fs);
  hKinDsVsMuLead = new HistoKinPair("DsVsMuLead", 0,10,*fs);
  hKinClosestMuPhi =  new HistoKinPair("ClosestMuPhi", 0,10,*fs);

  hMuMaxDistance = fs->make<TH1F>("hMuMaxDistance","Max dR in 3Mu",100,0,6.28);
  hMuMaxDistance->Sumw2();

  hNRecoMuAll       = fs->make<TH1F>("hNRecoMuAll","Total # reco muons; # of reco muons; #events",10,0,10);
  hNRecoMuMatched       = fs->make<TH1F>("hNRecoMuMatched","Total # reco muons; # of reco muons; #events",10,0,10);

  hNRecoMuGoodAll       = fs->make<TH1F>("hNRecoMuGoodAll","Total # reco muons; # of reco muons; #events",10,0,10);
  hNRecoMuGoodMatched   = fs->make<TH1F>("hNRecoMuGoodMatched","Total # reco muons; # of reco muons; #events",10,0,10);
  hNRecoTkMuMatched = fs->make<TH1F>("hNRecoTkMuMatched","Total # reco muons; # of reco muons; #events",10,0,10);
  hNVertex = fs->make<TH1F>("hNVertex","# vertexes; # vertices; #events",100,0,100);

  h1MuL1pass = fs->make<TH1F>("h1MuL1pass","At least 1 muon L1 pass",100,0,50);
  h2MuL1pass = fs->make<TH1F>("h2MuL1pass","At least 2 muon L1 pass",100,0,50);
  h3MuL1pass = fs->make<TH1F>("h3MuL1pass","At least 3 muon L1 pass",100,0,50);

  h1MuL1Matchedpass = fs->make<TH1F>("h1MuL1Matchedpass","At least 1 muon matched L1 pass",100,0,50);
  h2MuL1Matchedpass = fs->make<TH1F>("h2MuL1Matchedpass","At least 2 muon matched L1 pass",100,0,50);
  h3MuL1Matchedpass = fs->make<TH1F>("h3MuL1Matchedpass","At least 3 muon matched L1 pass",100,0,50);


  h2MuL1Matchedpass_2cands = fs->make<TH1F>("h2MuL1Matchedpass_2cands","Exactly 2 muons matched L1 pass",100,0,50);
  hInputL1 = fs->make<TH1F>("hInputL1","Tot L1 input",100,0,50);

  hInputL1_2cands = fs->make<TH1F>("hInputL1_2cands","Tot L1 input with 2 cands",100,0,50);

  hDiMuInvMass= fs->make<TH1F>("hDiMuInvMass","Hardest DiMuon Inv. Mass",100,0,10);
  hGoodDiMuInvMass= fs->make<TH1F>("hGoodDiMuInvMass","Hardest Good DiMuon Inv. Mass",100,0,10);

  hsvchi2= fs->make<TH1F>("hsvchi2","Secondary Vertex chi2",100,0,10);
  hDL = fs->make<TH1F>("hDL","DiMuon decay lenght",150,-.2,.5);
  hDLSig = fs->make<TH1F>("hDLSig","DiMuon decay lenght significance",600,-30,30);

  hvtxResx=fs->make<TH1F>("hvtxResx","DiMuon-TriMuon Vtx Residual X",200,-1,1);
  hvtxResy=fs->make<TH1F>("hvtxResy","DiMuon-TriMuon Vtx Residual Y",200,-1,1);
  hvtxResz=fs->make<TH1F>("hvtxResz","DiMuon-TriMuon Vtx Residual Z",200,-1,1);

  hNDs = fs->make<TH1F>("hNDs","Number of Ds in the event",11,-0.5,10.5);
  hNmuFromTau= fs->make<TH1F>("hNmuFromTau","Number of mu from tau",6,-0.5,5.5);
  hNL1Cand= fs->make<TH1F>("hNL1Cand","N L1 Muons",6,-0.5,5.5);
  hNL1MatchedCand= fs->make<TH1F>("hNL1MatchedCand","N L1 Matched Muons",6,-0.5,5.5);

  hL1EtaPt=fs->make<TH2F>("hL1EtaPt","L1 Cand. Pt Vs Eta",60,0,3,100,0,50);
  hL1MatchedEtaPt=fs->make<TH2F>("hL1MatchedEtaPt","L1 Matched Cand. Pt Vs Eta",60,0,3,100,0,50);
  hMinMuDRVsPtDs=fs->make<TH2F>(" hMinMuDRVsPtDs","Min Mu dR Vs Ds pT",100,0,50,50,0,5);

  h1MuL1pass->Sumw2();
  h2MuL1pass->Sumw2();
  h3MuL1pass->Sumw2();
  hInputL1->Sumw2();
  hInputL1_2cands->Sumw2();
  h2MuL1Matchedpass_2cands->Sumw2();

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
