

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"


// #include "DataFormats/VertexReco/interface/Vertex.h"
// #include "DataFormats/VertexReco/interface/VertexFwd.h"

// #include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
// #include "DataFormats/Candidate/interface/Particle.h"

// #include "MyAnalysis/Tau3Mu/src/Histograms.h"
// #include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
// #include "DataFormats/HepMCCandidate/interface/GenParticle.h" 
//#include "DataFormats/MuonReco/interface/MuonEnergy.h" 


// #include "DataFormats/L1Trigger/interface/L1MuonParticleFwd.h"
// #include "DataFormats/L1Trigger/interface/L1MuonParticle.h"
// #include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
// #include "DataFormats/Common/interface/TriggerResults.h"

// #include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
// #include "TrackingTools/Records/interface/TransientTrackRecord.h"
// #include "TrackingTools/TransientTrack/interface/TransientTrack.h"
// #include "TrackingTools/IPTools/interface/IPTools.h"


// #include "DataFormats/Math/interface/Error.h"
// #include "DataFormats/Math/interface/Point3D.h"
// #include "DataFormats/GeometryVector/interface/GlobalPoint.h"
// #include "DataFormats/GeometryCommonDetAlgo/interface/GlobalError.h"
// #include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"
// #include "DataFormats/RecoCandidate/interface/RecoChargedCandidateFwd.h"

// #include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"
// #include "DataFormats/HLTReco/interface/TriggerRefsCollections.h"
// #include "DataFormats/HLTReco/interface/TriggerEventWithRefs.h"
// #include "DataFormats/HLTReco/interface/TriggerEvent.h"
// #include "FWCore/Common/interface/TriggerNames.h"

#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TLorentzVector.h"
#include <TMath.h>
#include <TTree.h>
#include <iostream>
#include <map>

using namespace std;
using namespace reco;




//-----------------------------------------------------------------


// bool sortByPt(const reco::Candidate *part1, const reco::Candidate *part2) {

//   return part1->pt() > part2->pt();
// }

// //////////////////////////////////////////////////////////////////
// // generically maximum
// template <class T> const T& max ( const T& a, const T& b ) {
//   return (b<a)?a:b;     // or: return comp(b,a)?a:b; for the comp version
// }


//-----------------------------------------------------------------
class ZTreeBuilder : public edm::EDAnalyzer {
public:
  explicit ZTreeBuilder(const edm::ParameterSet&);
  ~ZTreeBuilder();

private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  void resetTree();


  int counter;

  edm::InputTag muonInput;
  edm::InputTag vertexInput;
  double muonPtMin;
  double minDiLeptonMass;
 
  bool debug;

  // variables for the tree
  int run;
  int lumi;
  int bx;
  int event;
  
  float l1_px;
  float l1_py;
  float l1_pz;
  float l1_en;
  int l1_pid;
  int l1_id;
  float l1_genid;
  float l1_ptErr;
  float l1_iso1;
  float l1_iso2;
  float l1_iso3;

  float l2_px;
  float l2_py;
  float l2_pz;
  float l2_en;
  float l2_pid;
  int l2_id;
  int l2_genid;
  float l2_ptErr;
  float l2_iso1;
  float l2_iso2;
  float l2_iso3;



  TTree *tree;



};



// get the tight muon defintion from recent versions of MuonSelector
bool isTightMuon(const reco::Muon& muon, const reco::Vertex& vtx){

  if(!muon.isTrackerMuon() || !muon.isGlobalMuon()) return false;

  bool muID = isGoodMuon(muon,muon::GlobalMuonPromptTight) && isGoodMuon(muon,muon::TrackerMuonArbitrated);

  bool hits = muon.innerTrack()->numberOfValidHits() > 10 &&
    muon.innerTrack()->hitPattern().numberOfValidPixelHits() > 0 &&
    muon.numberOfMatchedStations() > 1;

  bool ip = fabs(muon.innerTrack()->dxy(vtx.position())) < 0.2;

  return muID && hits && ip;
}
  
//
// constants, enums and typedefs
//



//


ZTreeBuilder::ZTreeBuilder(const edm::ParameterSet& iConfig) {
  counter = 0;

  muonInput             = iConfig.getUntrackedParameter<edm::InputTag>("muonInput",
								       edm::InputTag("muons",""));

  vertexInput           = iConfig.getUntrackedParameter<edm::InputTag>("vertexInput",
								       edm::InputTag("offlinePrimaryVerticesWithBS",""));
  
  muonPtMin             = iConfig.getUntrackedParameter<double>("muonPtMin", 1.);

  minDiLeptonMass       = iConfig.getUntrackedParameter<double>("minDiLeptonMass", 30.);
  debug                 = iConfig.getUntrackedParameter<bool>("debug", false);

}

ZTreeBuilder::~ZTreeBuilder() {}


//
// member functions
//

// ------------ method called to for each event  ------------
void ZTreeBuilder::analyze(const edm::Event& ev, const edm::EventSetup& iSetup) {
  resetTree();
  
  float weight = 1.;

  run = ev.id().run();
  lumi = ev.luminosityBlock();
  bx = ev.eventAuxiliary().bunchCrossing();
  event = ev.id().event();

  // get the muon container
  edm::Handle<MuonCollection> muons;
  ev.getByLabel(muonInput,muons);
  
  // get the vertex collection
  edm::Handle< std::vector<reco::Vertex> > pvHandle;
  ev.getByLabel(vertexInput, pvHandle );

  // get the PV
  reco::Vertex primaryVertex;
  if(pvHandle.isValid()) {
    primaryVertex = pvHandle->at(0); 
  }
 

  int nGoodMuons = 0;
  
  TLorentzVector recoMuonMom1;
  TLorentzVector recoMuonMom2;

  // check the validity of the collection
  if(muons.isValid()) {
    for (MuonCollection::const_iterator recoMu = muons->begin();
         recoMu!=muons->end(); ++recoMu){ // loop over all muons


      // check the quality of the muon
      if(!isTightMuon(*recoMu, primaryVertex)) continue;

      double eta = (*recoMu).eta();
      double phi = (*recoMu).phi();
      double pt = (*recoMu).pt();

      if(pt < muonPtMin) continue;
      

      if(debug) cout << "[ZTreeBuilder] New Tight Muon found:" << endl;
      if(debug) cout << "-- eta: " << eta << " phi: " << phi << " pt: " << pt << endl;       

      // check that we have exactly 2 good muons in this event
      if(nGoodMuons >= 2) return;
      
      nGoodMuons++;
      MuonIsolation isol03 = (*recoMu).isolationR03();
      double relIso = (isol03.emEt + isol03.hadEt + isol03.sumPt)/recoMu->pt();
      
      if(nGoodMuons == 1) {  
	recoMuonMom1 = TLorentzVector((*recoMu).px(), (*recoMu).py(), (*recoMu).pz(), (*recoMu).energy());
	l1_px = recoMu->px();
	l1_py = recoMu->py();
	l1_pz = recoMu->pz();
	l1_en = recoMu->energy();
	l1_pid = recoMu->charge()*13;
	l1_ptErr = 0;
	l1_iso1 = relIso;
	// l1_iso2;
	// l1_iso3;
      } else if(nGoodMuons == 2) {
	recoMuonMom2 = TLorentzVector((*recoMu).px(), (*recoMu).py(), (*recoMu).pz(), (*recoMu).energy());
	l2_px = recoMu->px();
	l2_py = recoMu->py();
	l2_pz = recoMu->pz();
	l2_en = recoMu->energy();
	l2_pid = recoMu->charge()*13;
	l2_ptErr = 0;
	l2_iso1 = relIso;
	// l2_iso2;
	// l2_iso3;
      }
      // FIXME add Pt cut and M min cut
    }
  }
  
  TLorentzVector diLepton = recoMuonMom1 + recoMuonMom2;
  if(diLepton.M() < minDiLeptonMass) return;

  tree->Fill();

}


void ZTreeBuilder::resetTree() {
  run = 0;
  lumi = 0;
  bx = 0;
  event = 0;
  
  l1_px = 0;
  l1_py = 0;
  l1_pz = 0;
  l1_en = 0;
  l1_pid = 0;
  l1_id = 0;
  l1_genid = 0;
  l1_ptErr = 0;
  l1_iso1 = 0;
  l1_iso2 = 0;
  l1_iso3 = 0;

  l2_px = 0;
  l2_py = 0;
  l2_pz = 0;
  l2_en = 0;
  l2_pid = 0;
  l2_id = 0;
  l2_genid = 0;
  l2_ptErr = 0;
  l2_iso1 = 0;
  l2_iso2 = 0;
  l2_iso3 = 0;
}


// ------------ method called once each job just before starting event loop  ------------
void ZTreeBuilder::beginJob() {
  cout << "begin job" << endl;
  edm::Service<TFileService> fs;
  
  tree = fs->make<TTree>("ZTree", "ZTree");

 //event info
  tree->Branch("run",        &run,        "run/I");
  tree->Branch("lumi",       &lumi,       "lumi/I");
  tree->Branch("event",      &event,      "event/I");
  tree->Branch("bx",         &bx,         "bx/I");


 //Selected di-leptons
  tree->Branch("l1_px",      &l1_px,      "l1_px/F");
  tree->Branch("l1_py",      &l1_py,      "l1_py/F");
  tree->Branch("l1_pz",      &l1_pz,      "l1_pz/F");
  tree->Branch("l1_en",      &l1_en,      "l1_en/F");
  tree->Branch("l1_pid",     &l1_pid,     "l1_pid/I");  
  tree->Branch("l1_id",      &l1_id,      "l1_id/I");
  tree->Branch("l1_genid",   &l1_genid,   "l1_genid/I");
  tree->Branch("l1_ptErr",   &l1_ptErr,   "l1_ptErr/F");
  tree->Branch("l1_iso1",    &l1_iso1,    "l1_iso1/F");
  tree->Branch("l1_iso2",    &l1_iso2,    "l1_iso2/F");
  tree->Branch("l1_iso3",    &l1_iso3,    "l1_iso3/F");

  tree->Branch("l2_px",      &l2_px,      "l2_px/F");
  tree->Branch("l2_py",      &l2_py,      "l2_py/F");
  tree->Branch("l2_pz",      &l2_pz,      "l2_pz/F");
  tree->Branch("l2_en",      &l2_en,      "l2_en/F");
  tree->Branch("l2_pid",     &l2_pid,      "l2_pid/I");
  tree->Branch("l2_id",      &l2_id,      "l2_id/I");
  tree->Branch("l2_genid",   &l2_genid,   "l2_genid/I");
  tree->Branch("l2_ptErr",   &l2_ptErr,   "l2_ptErr/F");
  tree->Branch("l2_iso1",    &l2_iso1,    "l2_iso1/F");
  tree->Branch("l2_iso2",    &l2_iso2,    "l2_iso2/F");
  tree->Branch("l2_iso3",    &l2_iso3,    "l2_iso3/F");




}


// ------------ method called nce each job just after ending the event loop  ------------
void 
ZTreeBuilder::endJob() {
  cout << "Total # events: " << counter << endl;
}



#include "FWCore/Framework/interface/MakerMacros.h"  
DEFINE_FWK_MODULE( ZTreeBuilder );
