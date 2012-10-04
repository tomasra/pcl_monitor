#include "TrackingTools/PatternTools/interface/TSCBLBuilderNoMaterial.h"
#include "TrackingTools/TrajectoryState/interface/FreeTrajectoryState.h" 
#include "TrackingTools/TrajectoryParametrization/interface/GlobalTrajectoryParameters.h"
#include "DataFormats/MuonSeed/interface/L3MuonTrajectorySeed.h"
#include "DataFormats/MuonSeed/interface/L3MuonTrajectorySeedCollection.h"
#include "DataFormats/TrackCandidate/interface/TrackCandidate.h"
#include "DataFormats/TrackCandidate/interface/TrackCandidateCollection.h"

#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "DataFormats/TrajectorySeed/interface/TrajectorySeed.h"
#include "DataFormats/TrajectorySeed/interface/TrajectorySeedCollection.h"
#include "DataFormats/MuonReco/interface/MuonTrackLinks.h"
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

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"

#include "DataFormats/Math/interface/Error.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "DataFormats/GeometryCommonDetAlgo/interface/GlobalError.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidateFwd.h"

#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"
#include "DataFormats/HLTReco/interface/TriggerRefsCollections.h"
#include "DataFormats/HLTReco/interface/TriggerEventWithRefs.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "TrackingTools/PatternTools/interface/ClosestApproachInRPhi.h"

#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TLorentzVector.h"
#include <TMath.h>
#include <iostream>
#include <map>

using namespace std;
using namespace reco;


// USEFUL DOCUMENTS:
// https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookGenParticleCandidate#GenPCand
// http://pdg.lbl.gov/mc_particle_id_contents.html


//-----------------------------------------------------------------


// bool sortByPt(const reco::Candidate *part1, const reco::Candidate *part2) {

//   return part1->pt() > part2->pt();
// }

//////////////////////////////////////////////////////////////////
// generically maximum
template <class T> const T& max ( const T& a, const T& b ) {
  return (b<a)?a:b;     // or: return comp(b,a)?a:b; for the comp version
}


//-----------------------------------------------------------------
class L3RecoInSteps : public edm::EDAnalyzer {
public:
  explicit L3RecoInSteps(const edm::ParameterSet&);
  ~L3RecoInSteps();

private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  virtual bool MatchObjects(std::vector<TLorentzVector> &, std::vector<TLorentzVector> &, int);
  virtual FreeTrajectoryState initialFreeState( const reco::Track&,const MagneticField*);

  edm::InputTag l1ExtraParticlesIntag;
  edm::InputTag inputTr;
  edm::InputTag DisplacedVertexTag_;
  edm::InputTag beamSpotTag_;
  edm::InputTag RegTrackCands_;
  edm::InputTag L3muCandLabel_;
  edm::InputTag L3muDisplVtxCandLabel_;
  edm::InputTag L2muCandLabel_;
  edm::InputTag L2muPreFilterCandLabel_ ;
  edm::InputTag mmkVtxLabel;

  HistoVertex *hHLTDiMuonVertex;
  HistoVertex *hHLTTriTrackVertex;
  HistoVertex *hHLTTriTrackVertexNotFiltered;
  HistoKinPair *hDiMuL2P,*hDiMuL2FilteredP,*hDiMuL3P,*hDiMuL3FilteredDispVtxP,*hDiMuL3Filtered3VtxP,*hDiMuL3TrkP;

  HistoKin *hL2k;
  HistoKin *hL2Filtered;
  HistoKin *hL3k;
  HistoKin *hL3FilteredDispVtx;
  HistoKin *hL3Filtered3Vtx;
  HistoKin *hAllTracks;
  HistoKin *hTracksTriVtx;
  HistoKin *hDiMuL2;
  HistoKin *hDiMuL2Filtered;
  HistoKin *hDiMuL3;
  HistoKin *hDiMuL3Filtered;
  HistoKin *hDiMuL3FilteredDispVtx;
  HistoKin *hDiMuL3Filtered3Vtx;
  HistoKin *hDiMuL3Trk;

  TH1F * hL2ptN,*hL2phiN,*hL2etaN,* hL2ptS,*hL2phiS,*hL2etaS,  *hL2hN, *hL2hS,*hL2chiN,*hL2chiS;
  TH1F * hL3ptN,* hL3etaN,* hL3ptS,* hL3etaS;

  TH2F* ptDsVsptTau, *PtL2Dr;

  TH1F *hNVtxMuMuTrk;
  TH1F *hNVtxMuMu;
  TH1F *hNRegTracks;
  TH1F *hNL3Muons;
  TH1F *hNL2Muons;
  TH1F* h0All,* h0Pass,*h0Fail;

  TH1F *hL2DxyB,*hL2DzB, *hL2DxySigB;
  TH1F *hL2DxyA,*hL2DzA, *hL2DxySigA;

  TH1F* hL1,*hL1s,*hL1f, *hL2, *hL2f, *hL3, *hL3f, *hL3vtx, *hL3vtxf, *hTracks, *hL3Tracksf, *hDCA,*hVProb, *hL3Mass,*hL3TrackMass, *hDoSigTk;


  int counter;
  int counterDs;
  int countInAccept;
  int counterMoreThan3Muons;
  int counterMoreThanOneds;
  int counterTaus;

  bool debug;

};

//
// constants, enums and typedefs
//
//

L3RecoInSteps::L3RecoInSteps(const edm::ParameterSet& iConfig) {

  counter = 0;
  counterDs = 0;
  countInAccept = 0;
  counterMoreThan3Muons = 0;
  counterMoreThanOneds = 0;
  counterTaus = 0;

  l1ExtraParticlesIntag = iConfig.getUntrackedParameter<edm::InputTag>("l1ExtraParticles",
								       edm::InputTag("l1extraParticles",""));

  inputTr               = iConfig.getUntrackedParameter<edm::InputTag>("TriggerResults",
								       edm::InputTag("TriggerResults", "", "HLTX"));

  DisplacedVertexTag_   = iConfig.getUntrackedParameter<edm::InputTag>("diMuDisplacedVertex",
								       edm::InputTag("hltDisplacedmumuVtxProducerDoubleMuTau2Mu::HLTX"));
  //hltDisplacedmumuVtxProducerDoubleMuTau2Mu
								       //edm::InputTag("hltDisplacedmumuFilterDoubleMuTau2Mu"));

  L3muDisplVtxCandLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("diMuDisplacedVertexFiltLabel",
									edm::InputTag("hltDisplacedmumuFilterDoubleMuTau2Mu::HLTX"));

  beamSpotTag_          = iConfig.getUntrackedParameter<edm::InputTag>("beamSpot",
								       edm::InputTag("hltOnlineBeamSpot::HLTX"));

  L3muCandLabel_        = iConfig.getUntrackedParameter<edm::InputTag>("l3MuonCands",
								       edm::InputTag("hltL3MuonCandidates::HLTX"));

  RegTrackCands_        = iConfig.getUntrackedParameter<edm::InputTag>("tracks",
								       edm::InputTag("hltTau3MuAllTracks::HLTX"));

  L2muCandLabel_        = iConfig.getUntrackedParameter<edm::InputTag>("l2MuonCands",
								       edm::InputTag("hltL2MuonCandidates::HLTX"));

  mmkVtxLabel           = iConfig.getUntrackedParameter<edm::InputTag>("mmkVtxLabel",
								       edm::InputTag("hltTau3MuMuMuTkFilter::HLTX"));

  debug                 = iConfig.getUntrackedParameter<bool>("debug", false);

  L2muPreFilterCandLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("diMuL2FilterLabel",
								       edm::InputTag("hltDimuon0or33L2PreFiltered0::HLTX"));
}

L3RecoInSteps::~L3RecoInSteps() {}


//
// member functions
//

// ------------ method called to for each event  ------------
void L3RecoInSteps::analyze(const edm::Event& ev, const edm::EventSetup& iSetup) {
  float weight = 1.;

  // ------------------------------------------------------------------------------------------------
  // trigger analysis
  cout << endl;
  cout << "-------------New Event----------------" << endl;
  // some counters/flags from trigger info
  int nL1Muons=0;
  int nL1MuonsPt3p5=0;
  int nL1MuonsPt5=0;
  bool tau3MuTrig = false;
  bool tau2MuPixTrack = false;
  bool tau2MuRegionalPixTrack = false;
  bool tau2MuRegionalPixTrackTight = false;

  counter++;

  //get the Gen Ds
  double thePT=99999, PtTau=0;
  int nds=0, nlow=0;
  std::vector<TLorentzVector> muvec;
  string mcTruthCollection = "genParticles";
  edm::Handle< reco::GenParticleCollection > genParticleHandle;
  ev.getByLabel(mcTruthCollection,genParticleHandle) ;
  const reco::GenParticleCollection *genParticleCollection = genParticleHandle.product();

  int nmu=0;

  reco::GenParticleCollection::const_iterator genPart;
  
  for(genPart=genParticleCollection->begin(); genPart!=genParticleCollection->end(); genPart++) {
    const reco::Candidate & cand = *genPart;
    if (abs(cand.pdgId()) == 431){
      int ndau=cand.numberOfDaughters();
      for(int k = 0; k < ndau; ++ k) {
	const Candidate * d = cand.daughter( k );
	int dauId = d->pdgId();
	if (abs(dauId)==15) {
	  nds++; thePT=cand.pt();
	  PtTau=d->pt();
	  int ndau1=d->numberOfDaughters();
	  for(int s = 0; s < ndau1; ++ s) {
	    const Candidate * m = d->daughter( s );
	    if (abs(m->pdgId())==13){
	      nmu++;
	      TLorentzVector tmp;
	      tmp.SetPtEtaPhiM( m->pt(),m->eta(),m->phi(),0.1057);
	      muvec.push_back(tmp);
	      if (m->pt()<3) nlow++;  
	      cout << "GenMuon: " << nmu << " pt " << m->pt() << " eta " << m->eta() << " phi " << m->phi() << " charge " << m->charge() << endl;
	    }
	  }
	}
      }    
    }
  }
  //if (nlow>0) return;
  if (thePT==99999 || nds>1 || muvec.size()!=3) return;
  //cout << "Ds found " << endl;
  counterDs++;

  ptDsVsptTau->Fill(PtTau,thePT);
  edm::ESHandle<MagneticField> bFieldHandle;
  iSetup.get<IdealMagneticFieldRecord>().get(bFieldHandle);

  const MagneticField* magField=bFieldHandle.product();

  //get the Beam Spot
  reco::BeamSpot vertexBeamSpot;
  edm::Handle<reco::BeamSpot> recoBeamSpotHandle;
  ev.getByLabel(beamSpotTag_,recoBeamSpotHandle);
  vertexBeamSpot = *recoBeamSpotHandle;

  TSCBLBuilderNoMaterial blsBuilder;

  TLorentzVector L21,L22;
  double nh1,nh2, chi1, chi2;

  // get the l2 candidates passing the prefilter
  edm::Handle<trigger::TriggerFilterObjectWithRefs> l2mufilt;
  ev.getByLabel(L2muPreFilterCandLabel_ ,l2mufilt);
  if (l2mufilt.isValid()){
    std::vector<RecoChargedCandidateRef> tr;
    l2mufilt->getObjects(trigger::TriggerMuon, tr);
    cout << "L2 size " << tr.size() << endl;
    if (tr.size() < 2) return;
    hL2f->Fill(thePT);
  }

  edm::Handle<L3MuonTrajectorySeedCollection> L3TrajSeedOIState;
  ev.getByLabel(edm::InputTag("hltL3TrajSeedOIState"),L3TrajSeedOIState);
  if (L3TrajSeedOIState.isValid()) cout << "L3TrajSeedOIState  " << L3TrajSeedOIState->size() << endl;

  edm::Handle<TrackCandidateCollection> L3TrackCandidateFromL2OIState;
  ev.getByLabel(edm::InputTag("hltL3TrackCandidateFromL2OIState"),L3TrackCandidateFromL2OIState);
  if (L3TrackCandidateFromL2OIState.isValid()) cout << "L3TrackCandidateFromL2OIState  " << L3TrackCandidateFromL2OIState->size() << endl;

  edm::Handle<TrackCollection> L3TkTracksFromL2OIState;
  ev.getByLabel(edm::InputTag("hltL3TkTracksFromL2OIState"),L3TkTracksFromL2OIState);
  if (L3TkTracksFromL2OIState.isValid()) cout << "L3TkTracksFromL2OIState  " << L3TkTracksFromL2OIState->size() << endl;

  edm::Handle<TrackCollection> L3MuonsOIState;
  ev.getByLabel(edm::InputTag("hltL3MuonsOIState"),L3MuonsOIState);
  if (L3MuonsOIState.isValid()) cout << "L3MuOI  " << L3MuonsOIState->size() << endl;

  edm::Handle<L3MuonTrajectorySeedCollection> L3TrajSeedOIHit;
  ev.getByLabel(edm::InputTag("hltL3TrajSeedOIHit"),L3TrajSeedOIHit);
  if (L3TrajSeedOIHit.isValid()) cout << "L3TrajSeedOIHit  " << L3TrajSeedOIHit->size() << endl;

  edm::Handle<TrackCandidateCollection> L3TrackCandidateFromL2OIHit;
  ev.getByLabel(edm::InputTag("hltL3TrackCandidateFromL2OIHit"),L3TrackCandidateFromL2OIHit);
  if (L3TrackCandidateFromL2OIHit.isValid()) cout << "L3TrackCandidateFromL2OIHit  " << L3TrackCandidateFromL2OIHit->size() << endl;

  edm::Handle<TrackCollection> L3TkTracksFromL2OIHit;
  ev.getByLabel(edm::InputTag("hltL3TkTracksFromL2OIHit"),L3TkTracksFromL2OIHit);
  if (L3TkTracksFromL2OIHit.isValid()) cout << "L3TkTracksFromL2OIHit  " << L3TkTracksFromL2OIHit->size() << endl;

  edm::Handle<TrackCollection> L3MuonsOIHit;
  ev.getByLabel(edm::InputTag("hltL3MuonsOIHit"),L3MuonsOIHit);
  if (L3MuonsOIHit.isValid()) cout << "L3MuonsOIHit  " << L3MuonsOIHit->size() << endl;

  edm::Handle<TrackCollection> L3TkFromL2OICombination;
  ev.getByLabel(edm::InputTag("hltL3TkFromL2OICombination"),L3TkFromL2OICombination);
  if (L3TkFromL2OICombination.isValid()) cout << "L3TkFromL2OICombination  " << L3TkFromL2OICombination->size() << endl;

  edm::Handle<L3MuonTrajectorySeedCollection> L3TrajSeedIOHit;
  ev.getByLabel(edm::InputTag("hltL3TrajSeedIOHit"),L3TrajSeedIOHit);
  if (L3TrajSeedIOHit.isValid()) cout << "L3TrajSeedIOHit  " << L3TrajSeedIOHit->size() << endl;

  edm::Handle<TrackCandidateCollection> L3TrackCandidateFromL2IOHit;
  ev.getByLabel(edm::InputTag("hltL3TrackCandidateFromL2IOHit"),L3TrackCandidateFromL2IOHit);
  if (L3TrackCandidateFromL2IOHit.isValid()) cout << "L3TrackCandidateFromL2IOHit  " << L3TrackCandidateFromL2IOHit->size() << endl;

  edm::Handle<TrackCollection> L3TkTracksFromL2IOHit;
  ev.getByLabel(edm::InputTag("hltL3TkTracksFromL2IOHit"),L3TkTracksFromL2IOHit);
  if (L3TkTracksFromL2IOHit.isValid()) cout << "L3TkTracksFromL2IOHit  " << L3TkTracksFromL2IOHit->size() << endl;

  edm::Handle<TrackCollection> L3MuonsIOHit;
  ev.getByLabel(edm::InputTag("hltL3MuonsIOHit"),L3MuonsIOHit);
  if (L3MuonsIOHit.isValid()) cout << "L3MuonsIOHit  " << L3MuonsIOHit->size() << endl;

  edm::Handle<L3MuonTrajectorySeedCollection> L3TrajectorySeed;
  ev.getByLabel(edm::InputTag("hltL3TrajectorySeed"),L3TrajectorySeed);
  if (L3TrajectorySeed.isValid()) cout << "L3TrajectorySeed  " << L3TrajectorySeed->size() << endl;

  edm::Handle<TrackCandidateCollection> L3TrackCandidateFromL2;
  ev.getByLabel(edm::InputTag("hltL3TrackCandidateFromL2"),L3TrackCandidateFromL2);
  if (L3TrackCandidateFromL2.isValid()) cout << "L3TrackCandidateFromL2  " << L3TrackCandidateFromL2->size() << endl;

  edm::Handle<TrackCollection> L3TkTracksFromL2;
  ev.getByLabel(edm::InputTag("hltL3TkTracksFromL2"),L3TkTracksFromL2);
  if (L3TkTracksFromL2.isValid()) cout << "L3TkTracksFromL2  " << L3TkTracksFromL2->size() << endl;

  edm::Handle<vector<MuonTrackLinks> > L3MuonsLinksCombination;
  ev.getByLabel(edm::InputTag("hltL3MuonsLinksCombination"),L3MuonsLinksCombination);
  if (L3MuonsLinksCombination.isValid()) cout << "L3MuonsLinksCombination  " << L3MuonsLinksCombination->size() << endl;

  edm::Handle<TrackCollection> L3Muon;
  ev.getByLabel(edm::InputTag("hltL3Muons"),L3Muon);
  if (L3Muon.isValid()) cout << "L3Muon  " << L3Muon->size() << endl;
 
  // get all l3 mu candidates
  edm::Handle<RecoChargedCandidateCollection> l3mucands;
  ev.getByLabel (L3muCandLabel_,l3mucands);
  if (l3mucands.isValid()){
    hNL3Muons->Fill(l3mucands->size());
    cout << "L3MuonCandidates  " << l3mucands->size() << endl;

    if (l3mucands->size() < 2) return;    
  }
}

// ------------ method called once each job just before starting event loop  ------------
void L3RecoInSteps::beginJob() {
  cout << "begin job" << endl;
  edm::Service<TFileService> fs;

  hHLTDiMuonVertex = new HistoVertex("HLTDiMuonVertex",*fs);
  hHLTTriTrackVertex = new HistoVertex("HLTTriTrackVertex",*fs);
  hHLTTriTrackVertexNotFiltered = new HistoVertex("HLTTriTrackVertexNotFiltered",*fs);
  hL2k=new HistoKin("L2Muons",*fs);
  hL2Filtered=new HistoKin("L2MuonsFiltered",*fs);
  hL3k=new HistoKin("L3Muons",*fs);

  hL3FilteredDispVtx=new HistoKin("L3MuonsFilteredDispVtx",*fs);
  hL3Filtered3Vtx=new HistoKin("L3MuonsFiltered3Vtx",*fs);
  hAllTracks=new HistoKin("AllRegTracks",*fs);
  hTracksTriVtx=new HistoKin("TracksInVtx",*fs);
  hDiMuL2=new HistoKin("L2DiMuons",*fs);
  hDiMuL2Filtered=new HistoKin("L2DiMuonsFiltered",*fs);
  hDiMuL3=new HistoKin("L3DiMuons",*fs);
  hDiMuL3Filtered=new HistoKin("L3DiMuonsFiltered",*fs);
  hDiMuL3FilteredDispVtx=new HistoKin("L3DiMuonsFilteredDispVtx",*fs);
  hDiMuL3Filtered3Vtx=new HistoKin("L3DiMuonsFiltered3Vtx",*fs);
  hDiMuL3Trk=new HistoKin("L3DiMuonsTrack",*fs);

  hDiMuL2P=new HistoKinPair("L2DiMuonsPair",0,5,*fs);
  hDiMuL2FilteredP=new HistoKinPair("L2DiMuonsFilteredPair",0,5,*fs);
  hDiMuL3P=new HistoKinPair("L3DiMuonsPair",0,5,*fs);
  hDiMuL3FilteredDispVtxP=new HistoKinPair("L3DiMuonsFilteredDispVtxPair",0,5,*fs);
  hDiMuL3Filtered3VtxP=new HistoKinPair("L3DiMuonsFiltered3VtxPair",0,5,*fs);
  hDiMuL3TrkP=new HistoKinPair("L3DiMuonsTrackPair",0,5,*fs);

  hL2DxyB= fs->make<TH1F>("hL2DxyBeforeFilter", "# Dxy;# Dxy; # events", 250,0,0.5);
  hL2DzB = fs->make<TH1F>("hL2DzBeforeFilter", "# Dz;# Dz; # events", 250,0,0.5);
  hL2DxySigB = fs->make<TH1F>("hL2DxySigBeforeFilter", "# DxySig;# DxySig; # events", 100,0,50);

  hL2DxyA= fs->make<TH1F>("hL2DxyAfterFilter", "# Dxy;# Dxy; # events", 250,0,0.5);
  hL2DzA = fs->make<TH1F>("hL2DzAfterFilter", "# Dz;# Dz; # events", 250,0,0.5);
  hL2DxySigA = fs->make<TH1F>("hL2DxySigAfterFilter", "# DxySig;# DxySig; # events", 100,0,50);

  hNVtxMuMuTrk = fs->make<TH1F>("hNVtxMuMuTrk", "# vertices;# vertices; # events", 50,0,50);
  hNVtxMuMu = fs->make<TH1F>("hNVtxMuMu", "# vertices;# vertices; # events", 50,0,50);
  hNRegTracks = fs->make<TH1F>("hNRegTracks", "# RegTracks;# tracks; # events", 50,0,50);
  hNL3Muons= fs->make<TH1F>("hNL3", "# L3Muons;# muons; # events", 50,0,50);
  hNL2Muons= fs->make<TH1F>("hNL2", "# L2Muons;# muons; # events", 50,0,50);

  h0All= fs->make<TH1F>("h0All", "# L2Muons;ValidHits==0; # events", 1,0.,1.);
  h0Pass= fs->make<TH1F>("h0Pass", "# L2Muons;ValidHits==0; # events", 1,0.,1.);
  h0Fail= fs->make<TH1F>("h0Fail", "# L2Muons;ValidHits==0; # events", 1,0.,1.);

  ptDsVsptTau= fs->make<TH2F>("PtVsPt", "# GenPt; Pt Tau; Pt Ds", 25, 0., 50., 25, 0, 50);
  PtL2Dr= fs->make<TH2F>("L2DrVsPt", "# L2; Pt L2 DiMu; DR", 50, 0., 50., 100, 0, 2);

  hL2chiN= fs->make<TH1F>("hL2chiN", "# L2Muons;chi2/ndof; # events", 51,-0.5,50);
  hL2chiS= fs->make<TH1F>("hL2chiS", "# L2Muons;chi2/ndof; # events", 51,-0.5,50);

  hL2hN= fs->make<TH1F>("hL2hN", "# L2Muons; N valid hits; # events", 91,-0.5,90);
  hL2hS= fs->make<TH1F>("hL2hS", "# L2Muons; N valid hits; # events", 91,-0.5,90);

  hL2ptN= fs->make<TH1F>("hL2ptN", "# L2Muons; pT (GeV/c); # events", 25,0,50);
  hL2phiN=fs->make<TH1F>("hL2phiN", "# L2Muons; phi; # events", 50,-3.2,3.2);
  hL2etaN=fs->make<TH1F>("hL2etaN", "# L2Muons; eta; # events", 50,-2.5,2.5);

  hL3ptN= fs->make<TH1F>("hL3ptN", "# L3Muons Not Passing; pT (GeV/c); # events", 25,0,50);
  hL3etaN=fs->make<TH1F>("hL3etaN", "# L3Muons Not Passing; eta; # events", 50,-2.5,2.5);

  hL3ptS= fs->make<TH1F>("hL3ptS", "# L3Muons Passing; pT (GeV/c); # events", 25,0,50);
  hL3etaS=fs->make<TH1F>("hL3etaS", "# L3Muons Passing; eta; # events", 50,-2.5,2.5);

  hL2ptS= fs->make<TH1F>("hL2ptS", "# L2Muons; pT (GeV/c); # events", 25,0,50);
  hL2phiS=fs->make<TH1F>("hL2phiS", "# L2Muons; phi; # events", 50,-3.2,3.2);
  hL2etaS=fs->make<TH1F>("hL2etaS", "# L2Muons; eta; # events", 50,-2.5,2.5);

  hL1= fs->make<TH1F>("hL1", "# L1Muons;Ds pT (GeV/c); # events", 25,0,50);
  hL1s= fs->make<TH1F>("hL1s", "# L1SeedFilteredMuons;Ds pT (GeV/c); # events", 25,0,50);
  hL1f = fs->make<TH1F>("hL1f", "# L1FilteredMuons;Ds pT (GeV/c); # events", 25,0,50);
  hL2 = fs->make<TH1F>("hL2", "# L2Muons;Ds pT (GeV/c); # events", 25,0,50);
  hL2f = fs->make<TH1F>("hL2f", "# L2FilteredMuons;Ds pT (GeV/c); # events", 25,0,50);
  hL3 = fs->make<TH1F>("hL3", "# L3Muons;Ds pT (GeV/c); # events", 25,0,50);
  hL3f = fs->make<TH1F>("hL3f", "# L3FilteredMuons;Ds pT (GeV/c); # events", 25,0,50);
  hL3vtx = fs->make<TH1F>("hL3vtx", "# L3Vertices;Ds pT (GeV/c); # events", 25,0,50);
  hL3vtxf = fs->make<TH1F>("hL3vtxf", "# L3VtxFilteredMuons;Ds pT (GeV/c); # events", 25,0,50);
  hTracks = fs->make<TH1F>("hTracks", "# Regional Tracks; Ds pT (Gev/c); # events", 25,0,50);
  hL3Tracksf= fs->make<TH1F>("hL3Tracksf", "# L3PlusTrackFilter;Ds pT (GeV/c); # events", 25,0,50);
  
  hL1->Sumw2();
  hL1s->Sumw2();
  hL1f->Sumw2();
  hL2->Sumw2();
  hL2f->Sumw2();
  hL3->Sumw2();
  hL3f->Sumw2();
  hL3vtx->Sumw2();
  hL3vtxf->Sumw2();
  hTracks->Sumw2();
  hL3Tracksf->Sumw2();
  
  hL3TrackMass=fs->make<TH1F>("L3PlusTrackInvMass", "L3DiMu+Tk Mass;L3+Tk Inv. Mass (GeV/c^{2}); # events", 100,1.5,2);
  hL3Mass=fs->make<TH1F>("L3InvMass", "L3DiMu Mass;L3 Inv. Mass (GeV/c^{2}); # events", 200,0,2);
  hDCA = fs->make<TH1F>("DCA", "DCA MuMu;DCA (cm); # events", 100,0,2);
  hDoSigTk = fs->make<TH1F>("D0SigTk", "D0 Sig Tk;D0 (cm); # events", 300,0,30);
  hVProb = fs->make<TH1F>("hVProb", "Vtx Prob;prob.; # events", 100,0,1);

}

bool 
L3RecoInSteps::MatchObjects(std::vector<TLorentzVector> & gen, std::vector<TLorentzVector> &other, int mode) {
  bool match=false;
  std::vector<pair<uint, uint> > matched;
  bool runmatch=true;
  int nmatches=0;

  while (runmatch){
    double dRtmp=0.5;
    int indexgen=9999, indexother=9999;
    for (uint g=0; g< gen.size(); ++g){
      bool donegen=false;
      for (uint i=0; i<matched.size(); ++i){
	if (g==matched[i].first) donegen=true; 
      }
      if (donegen) continue;
      for (uint o=0; o<other.size(); ++o){
	bool doneother=false;
	for (uint i=0; i<matched.size(); ++i){
	  if (o==matched[i].second) doneother=true; 
	}
	if (doneother) continue;
	if (gen[g].DeltaR(other[o])<dRtmp && mode==0){
	  dRtmp=gen[g].DeltaR(other[o]);
	  indexgen=g;
	  indexother=o;
	}
	if (fabs(gen[g].Eta()-other[o].Eta())<dRtmp && mode==1){
	  dRtmp=fabs(gen[g].Eta()-other[o].Eta());
	  indexgen=g;
	  indexother=o;
	}
      }
    }
    if (dRtmp==0.5) {
      runmatch=false;
    }else{
      matched.push_back(make_pair(indexgen,indexother));
      nmatches++;
    }
  }

  if (nmatches>=2) match=true;
  return match;
}



// ------------ method called nce each job just after ending the event loop  ------------
void 
L3RecoInSteps::endJob() {
  cout << "Total # events: " << counter << endl;
  cout << "Total # events with a single Ds->tau->3mu: " << counterDs << endl;
}

FreeTrajectoryState L3RecoInSteps::initialFreeState( const reco::Track& tk,
                                                     const MagneticField* field)
{
  Basic3DVector<float> pos( tk.vertex());
  GlobalPoint gpos( pos);
  Basic3DVector<float> mom( tk.momentum());
  GlobalVector gmom( mom);
  GlobalTrajectoryParameters par( gpos, gmom, tk.charge(), field);
  CurvilinearTrajectoryError err( tk.covariance());
  return FreeTrajectoryState( par, err);
}
 


#include "FWCore/Framework/interface/MakerMacros.h"  
DEFINE_FWK_MODULE( L3RecoInSteps );
