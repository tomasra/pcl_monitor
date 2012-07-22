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
#include <TrackingTools/TrajectoryState/interface/TrajectoryStateClosestToPoint.h>

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
#include "TTree.h"
#include "TClonesArray.h"
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


//-----------------------------------------------------------------

inline bool sortGenIndex(std::pair<TLorentzVector,int> i1, std::pair<TLorentzVector,int> i2) {

  return i1.second < i2.second;
}

inline bool sortByPt(const reco::Candidate *part1, const reco::Candidate *part2) {

  return part1->pt() > part2->pt();
}

inline bool sortMuByPt(const reco::Muon mu1, const reco::Muon mu2) {

  return mu1.pt() > mu2.pt();
}

inline bool sortTLorentzByPt(const TLorentzVector mu1, const TLorentzVector mu2) {

  return mu1.Pt() > mu2.Pt();
}

//-----------------------------------------------------------------
class Tau3MuAnalysis_V2 : public edm::EDAnalyzer {
public:
  explicit Tau3MuAnalysis_V2(const edm::ParameterSet&);
  ~Tau3MuAnalysis_V2();

private:
  virtual void beginJob();
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob();
  virtual void beginRun(edm::Run const&, edm::EventSetup const&);
  virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
  virtual void Initialize_TreeVars();
  virtual void vtx(std::vector<TransientTrack>&, GlobalPoint &, GlobalError &);
  virtual pair<double,double> Compute_Lxy_and_Significance(Vertex &, TransientVertex &, TLorentzVector&);
  virtual void findBestDimuon(const edm::Event&, const edm::EventSetup&, MuonCollection&, MuonCollection&, TransientVertex&, Vertex&);
  virtual void findBestPiCand(const edm::Event&, const edm::EventSetup&, MuonCollection&, TransientVertex&, Vertex&, TransientVertex&,pair<double,double>& ,pair<double,double>&,TLorentzVector&, bool&,bool& ,int&,Track&);
  virtual bool isTight(const reco::Muon*);
  virtual bool TriggerDecision(const edm::Event&);
  virtual pair<bool,bool> isMu(const edm::Event&, const Track*, bool&, bool&, bool&);
  virtual int countTracksAround(const edm::Event&, const edm::EventSetup&, TLorentzVector*, double&, TransientVertex&);
  virtual pair<double,double> ComputeImpactParameterWrtPoint(TransientTrack& tt, Vertex&);
  virtual bool isMcMatched(const edm::Event&,TLorentzVector*,std::vector<TLorentzVector>&);
  virtual bool isInPV(Vertex&, TLorentzVector&);
  virtual double Compute_CosPointingAngle(Vertex& , TransientVertex& ,TLorentzVector&);
  virtual bool isClose(TransientTrack&, TransientVertex&);
  virtual bool isVtxErrorOk(TransientVertex&);
  virtual bool matchAllGen(const edm::Event&,std::vector<TLorentzVector>&,std::vector<std::pair<TLorentzVector,int> >&);
  virtual bool findGenMoms(const edm::Event&, std::vector<TLorentzVector>&);
  virtual bool alreadyMatched(uint&,std::vector<int>);
  //virtual bool countDs();

  string theVertexLabel;

  TH1F* hDiMuInvMass,* hGoodDiMuInvMass, *hSkim;
  TH1F* hDiMuTrackInvMass,* hGoodDiMuTrackInvMass,*hTriMuInvMass;

  TH1F* hpt, *hptMu,*hDiMuPt;
  TH1F* htotEff,* hDiMuEff, *hTrackEff;

  TH1F* hgenDr, *hcosPointing2,*hcosPointing3;
  //
  double diMuMassMin, diMuMassMax, diMuLxyMin, diMuLxyMax,diMuLxySigMin,diMuVtxChi2Max, diMuVprobMin, diMuCosPointMin,diMuTrackCosPointMin;
  double diMuTrackMassMin, diMuTrackMassMax, diMuTrackLxyMin,diMuTrackLxyMax,diMuTrackLxySigMin,diMuTrackVtxChi2Max,diMuTrackVprobMin;
  double MinTrackPt, MinMuPt;
  double Trackd0Max,Trackd0SigMin;
  double DRTracks;
  bool IsMC,isSignal, TightMuonsOnly;

  TH1F* hnmu,*hnt,*hvtx;

  double TrackMass;
  int nmuons;

  TFile* thefile;
  std::string FileName;
  TTree *ExTree, *GenTree;

  TLorentzVector* _Mu1_4Mom,*_Mu2_4Mom,*_MuTrack_4Mom, *_DiMu4Mom, *_DiMuPlusTrack4Mom;

  TLorentzVector* _Mu1_4MomG,*_Mu2_4MomG,*_MuTrack_4MomG, *_DiMu4MomG, *_DiMuPlusTrack4MomG;
  TLorentzVector* _Mu1_4MomR,*_Mu2_4MomR,*_MuTrack_4MomR, *_DiMu4MomR, *_DiMuPlusTrack4MomR;
  bool _IsGenRecoMatched,_IsOffline;

  int _Mu1Q,_Mu2Q,_Mu3Q;
  int _Run,_Evt,_Lum;

  TVector3 *_PV,*_SV,*_SVT,*_PVe,*_SVe,*_SVTe;

  double _SVchi,_SVprob;
  double _SVTchi,_SVTprob;
  double _Lxy,_LxySig,_LxyT,_LxyTSig;
  double _d0T,_d0T3,_d0TSig,_d0T3Sig, _dzT2;
  double _M3,_M2 ,_PtT,_dRdiMuT;
  double _cosp2,_cosp3;

  bool _TrigBit[10];

  int _NTracksInDr,_Nmu;

  bool _TrackIsMu;
  bool _Mu1IsGood,_Mu2IsGood,_TrackIsGoodMu,_isTight_Tk;
  bool _IsMu1InPV, _IsMu2InPV,_IsMu3InPV;
  bool _IsMcMatched;
  bool _IsTrig;
  bool _isSA_1, _isSA_2, _isSA_Tk;
  bool _isGlb_1,_isGlb_2,_isGlb_Tk;

  std::vector<string> HLT_paths;
  std::string HLT_process;

  bool OnlyOppositeCharge;
  bool debug;

  double ndm, ndmv, ndmm, ndmlxy, ndmlxys, ndmchi, ndmvprob,ndmclos;
  double nt, ntq, ntm, ntd0, ntd0s,ntv, ntlxy, ntlxys, ntchi, ntvprob,ntclos;

  double Total, Triggered, FoundDiMu , Offline, GenMatches;  

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

Tau3MuAnalysis_V2::Tau3MuAnalysis_V2(const edm::ParameterSet& cfg) {

  Total=0;
  Triggered=0;
  FoundDiMu=0;
  Offline=0;
  GenMatches=0;

  ndm=0; ndmv=0; ndmm=0; ndmlxy=0; ndmlxys=0; ndmchi=0; ndmvprob=0;ndmclos=0;
  nt=0; ntq=0; ntm=0; ntd0=0; ntd0s=0;ntv=0; ntlxy=0; ntlxys=0; ntchi=0; ntvprob=0;ntclos=0;

  diMuMassMin= cfg.getParameter<double> ("DiMuMassMin"); 
  diMuMassMax= cfg.getParameter<double> ("DiMuMassMax");  
  diMuLxyMin = cfg.getParameter<double> ("DiMuLxyMin"); 
  diMuLxyMax = cfg.getParameter<double> ("DiMuLxyMax"); 
  diMuLxySigMin = cfg.getParameter<double> ("DiMuLxySigMin");
  diMuVtxChi2Max= cfg.getParameter<double> ("DiMuVtxChi2Max");
  diMuVprobMin= cfg.getParameter<double> ("DiMuVprobMin");
  
  diMuTrackMassMin= cfg.getParameter<double> ("DiMuTrackMassMin"); 
  diMuTrackMassMax= cfg.getParameter<double> ("DiMuTrackMassMax"); 
  diMuTrackLxyMin = cfg.getParameter<double> ("DiMuTrackLxyMin");
  diMuTrackLxyMax = cfg.getParameter<double> ("DiMuTrackLxyMax");
  diMuTrackLxySigMin = cfg.getParameter<double> ("DiMuTrackLxySigMin");
  diMuTrackVtxChi2Max= cfg.getParameter<double> ("DiMuTrackVtxChi2Max");
  diMuTrackVprobMin= cfg.getParameter<double> ("DiMuTrackVprobMin");

  MinMuPt=cfg.getParameter<double> ("MuPTCut");
  MinTrackPt=cfg.getParameter<double> ("TrackPTCut");

  HLT_paths = cfg.getParameter<std::vector<string> > ("HLT_paths");
  HLT_process = cfg.getParameter<std::string> ("HLT_process");

  //TightMuonsOnly= cfg.getParameter<bool> ("OnlyTightMuons");
  IsMC= cfg.getParameter<bool> ("IsMC");
  
  OnlyOppositeCharge= cfg.getParameter<bool> ("OnlyOppositeChargeMuons");
  TrackMass= cfg.getParameter<double> ("GuessForTrackMass");

  diMuCosPointMin= cfg.getParameter<double> ("DiMuCosPointMin");
  diMuTrackCosPointMin= cfg.getParameter<double> ("DiMuTrackCosPointMin");

  DRTracks=cfg.getParameter<double> ("MaxDrForTrackCount");

  Trackd0Max= cfg.getParameter<double> ("Trackd0Max");
  Trackd0SigMin= cfg.getParameter<double> ("Trackd0SigMin");

  isSignal=cfg.getParameter<bool> ("isSignal");
  debug=cfg.getParameter<bool> ("Debug");
  FileName = cfg.getParameter<std::string> ("OutFileName");

  if ((IsMC && !isSignal) || OnlyOppositeCharge){
    if (debug) cout << "Running on Normalization Sample, mass min and max changed and opposite charge request activated" << endl;
    OnlyOppositeCharge=true;
    diMuMassMin=0.95;
    diMuMassMax=1.1;
    diMuTrackMassMin=1.85;
    diMuTrackMassMax=2.1;
    TrackMass=0.1396;
  }
}

Tau3MuAnalysis_V2::~Tau3MuAnalysis_V2() {}

//
// member functions
//

bool Tau3MuAnalysis_V2::alreadyMatched(uint& ind,std::vector<int> vind){

  bool alreadyMatched=false;
  
  for (uint i=0; i< vind.size(); i++){
    if (int(ind)==vind[i]) alreadyMatched=true; 
  }

  return alreadyMatched;
}

bool Tau3MuAnalysis_V2::isTight(const Muon* recoMu){

  bool isTight=false;

  if (!recoMu->isGlobalMuon()) return false;
  if (!recoMu->isPFMuon()) return false;
  if (!recoMu->isTrackerMuon()) return false;
  if (recoMu->globalTrack()->normalizedChi2() < 10 && 
      recoMu->globalTrack()->hitPattern().numberOfValidMuonHits() > 2 &&
      recoMu->numberOfMatchedStations() > 1 &&
      recoMu->innerTrack()->hitPattern().numberOfValidPixelHits() > 0 &&
      recoMu->innerTrack()->hitPattern().trackerLayersWithMeasurement() > 5) isTight=true;
  return isTight;
}

bool Tau3MuAnalysis_V2::isVtxErrorOk(TransientVertex& vtx){

  bool ok=true;

  double vxerr= vtx.positionError().cxx();
  double vyerr= vtx.positionError().cyy();
  double vzerr= vtx.positionError().czz();

  if (vxerr > 0.02 || vyerr > 0.02 || vzerr > 0.03) ok=false;

  return ok;

}


bool Tau3MuAnalysis_V2::isClose(TransientTrack& t, TransientVertex& tvtx){

  bool ok=false;

  Vertex vtx=Vertex(tvtx);

  /*double tz=t.trajectoryStateClosestToPoint(vtx.position()).position().z();
  double tx=t.trajectoryStateClosestToPoint(vtx.position()).position().x();
  double ty=t.trajectoryStateClosestToPoint(vtx.position()).position().y();

  double tez=t.trajectoryStateClosestToPoint(vtx.position()).perigeeError().longitudinalImpactParameterError();
  double tet=t.trajectoryStateClosestToPoint(vtx.position()).perigeeError().transverseImpactParameterError();
 
 
  //cout << "diffx " << diffx << " tet " << tet << endl;

  double diffz=fabs(tz-vtx.position().z());
  double diffy=fabs(ty-vtx.position().y());
  double diffx=fabs(tx-vtx.position().x());

  double vxerr= vtx.positionError().cxx();
  double vyerr= vtx.positionError().cyy();
  double vzerr= vtx.positionError().czz();

  vxerr=2*sqrt(vxerr*vxerr+tet*tet);
  vyerr=2*sqrt(vyerr*vyerr+tet*tet);
  vzerr=2*sqrt(vzerr*vzerr+tez*tez);
  
  

  if (debug){
  cout << "SV distance to track:" << endl; 
  cout << "diffz " << diffz <<  " verrz " << vzerr << endl;
  cout << "diffy " << diffy <<  " verry " << vyerr << endl;
  cout << "diffx " << diffx <<  " verrx " << vxerr << endl;
  }

  if (diffz < vzerr && diffx < vxerr && diffy < vyerr) ok=true;
  */
  double dz=t.track().dz(vtx.position());
  double verrz=vtx.zError();

  if (dz<0.03 && dz < verrz) ok=true;

  return ok;


}

void Tau3MuAnalysis_V2::findBestPiCand(const edm::Event& ev, const edm::EventSetup& iSetup, MuonCollection& dimu ,TransientVertex& tv, Vertex& primaryVertex,TransientVertex& dimuvtx ,pair<double,double>& d0track, pair<double,double>& d0track3, TLorentzVector& pi, bool & isMuon, bool& isGood ,int& q, Track& track){

  if (debug) cout << "Looking for the pi track" << endl;

  edm::ESHandle<TransientTrackBuilder> Builder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", Builder);

  Handle<TrackCollection> tracks;
  ev.getByLabel("generalTracks", tracks);

  if (!tracks.isValid()) return;
  if (tracks->size()>2) hnt->Fill(tracks->size()-2);

  KalmanVertexFitter avf;

  double tmpProb=diMuTrackVprobMin;
  double Vp0=diMuTrackVprobMin;

  for(TrackCollection::const_iterator it = tracks->begin();it != tracks->end(); ++it){

    if ((it->pt()==dimu[0].innerTrack()->pt() && it->eta()==dimu[0].innerTrack()->eta()) || (it->pt()==dimu[1].innerTrack()->pt() && it->eta()==dimu[1].innerTrack()->eta())) continue;
    if (dimu[0].charge()==dimu[1].charge() && it->charge()==dimu[0].charge()) continue; //impossible to have a particle with charge +/- 3

    nt++;

    bool goodTrack=false;

    if (it->quality(TrackBase::highPurity) && it->pt()> MinTrackPt) goodTrack=true;

    if (!goodTrack) continue;

    ntq++;

    TLorentzVector m1=TLorentzVector(dimu[0].px(),dimu[0].py(),dimu[0].pz(),dimu[0].energy());
    TLorentzVector m2=TLorentzVector(dimu[1].px(),dimu[1].py(),dimu[1].pz(),dimu[1].energy());
    TLorentzVector p=TLorentzVector(it->px(),it->py(),it->pz(),sqrt(TrackMass*TrackMass+it->p()*it->p()));
    TLorentzVector tot=m1+m2+p;

    if (tot.M() < diMuTrackMassMin || tot.M()> diMuTrackMassMax) continue;
    ntm++;

    TransientTrack ttpi=Builder->build(*it);

    vector<TransientTrack> tt;
    TransientVertex tmpvtx;

    TransientTrack tt1=Builder->build(dimu[0].innerTrack());
    TransientTrack tt2=Builder->build(dimu[1].innerTrack());

    tt.push_back(tt1);
    tt.push_back(tt2);
    tt.push_back(ttpi);

    Vertex diMuVtx=Vertex(dimuvtx);
    pair<double,double> d0tracktmp=ComputeImpactParameterWrtPoint(ttpi,diMuVtx);
    
    if (d0tracktmp.first > Trackd0Max) continue;
    ntd0++;

    if (fabs(d0tracktmp.first/d0tracktmp.second) < Trackd0SigMin) continue; 
    ntd0s++;

    tmpvtx=avf.vertex(tt);
    
    if (!tmpvtx.isValid()) continue;
    ntv++;

    double vChi2 = tmpvtx.totalChiSquared();
    double vNDF  = tmpvtx.degreesOfFreedom();

    double vProb(TMath::Prob(vChi2,(int)vNDF));

    if (vProb < Vp0) continue;

    ntvprob++;

    if (vChi2/vNDF > diMuTrackVtxChi2Max) continue;
    ntchi++;

    if(Compute_CosPointingAngle(primaryVertex,tmpvtx,tot)< diMuTrackCosPointMin) continue;

    pair<double,double> lxytmp=Compute_Lxy_and_Significance(primaryVertex,tmpvtx,tot);

    if (lxytmp.first < diMuTrackLxyMin || lxytmp.first > diMuTrackLxyMax ) continue;
    ntlxy++;

    if (lxytmp.first/lxytmp.second < diMuTrackLxySigMin) continue;
    ntlxys++;

    if (vProb < tmpProb) continue;

    tmpProb=vProb;
    pi=p;
    std::pair<bool,bool> isTkMu=isMu(ev,&(*it),_isSA_Tk,_isGlb_Tk,_isTight_Tk);

    isMuon=isTkMu.first;
    isGood=isTkMu.second;

    track=Track(*it);
    q=it->charge();
    tv=tmpvtx;
    d0track=d0tracktmp;   
    Vertex tmpvtx3=Vertex(tmpvtx);
    d0track3=ComputeImpactParameterWrtPoint(ttpi,tmpvtx3);

  }
}

bool Tau3MuAnalysis_V2::isInPV(Vertex& pv,TLorentzVector& track){

  bool inPV=false;
  for(std::vector<reco::TrackBaseRef>::const_iterator it = pv.tracks_begin() ; it != pv.tracks_end(); ++it ){
    if (!(it->isNonnull() && it->isAvailable())) continue;
    Track tr=*(it->get());
    TLorentzVector vect=TLorentzVector(tr.px(),tr.py(),tr.pz(),0);
    if (vect.DeltaR(track)==0) inPV=true;
  }
  return inPV;
}

void Tau3MuAnalysis_V2::findGenMoms(const edm::Event& ev, std::vector<TLorentzVector>& TheGenMus){
 if (debug) cout << "Find the GEN objects ...." << endl;

 //std::vector<TLorentzVector> TheGenMus;
  //find the right gen muons

  string mcTruthCollection = "genParticles";
  edm::Handle< reco::GenParticleCollection > genParticleHandle;
  ev.getByLabel(mcTruthCollection,genParticleHandle) ;

  if (!(genParticleHandle.isValid())) return;

  std::vector<int> genId;

  const reco::GenParticleCollection *genParticleCollection = genParticleHandle.product();

  reco::GenParticleCollection::const_iterator genPart;

  if (debug) cout << "Loop on genPart" << endl;

  if (isSignal){
    for(genPart=genParticleCollection->begin(); genPart!=genParticleCollection->end(); genPart++) {
      const reco::Candidate & cand = *genPart;

      if (abs(cand.pdgId())!=15) continue;
      if (debug) cout << "Mom Id " << cand.pdgId() << endl;

      int ndau=cand.numberOfDaughters();

      if (ndau<3) continue;
      if (debug) cout << "n tau daugthers:" << ndau << endl;
      for(int k = 0; k < ndau; ++ k) {
	TLorentzVector gen4mom;
	const Candidate * d = cand.daughter( k );
	int dauId = d->pdgId();
	if (debug) cout << "id " << dauId << endl;
	if (abs(dauId)==13) {
	  if (debug) cout << "gen mu status " << d->status() << endl;
	  gen4mom.SetPtEtaPhiM(d->pt(),d->eta(),d->phi(),d->mass());
	  TheGenMus.push_back(gen4mom);
	  genId.push_back(dauId);
	}
      }
    }
  }

  if (!isSignal){
    for(genPart=genParticleCollection->begin(); genPart!=genParticleCollection->end(); genPart++) {
      const reco::Candidate & cand = *genPart;
      
      if (abs(cand.pdgId())!= 431) continue;
      if (debug) cout << "Mom Id " << cand.pdgId() << endl;      

      int ndau=cand.numberOfDaughters();
      
      if (ndau<2) continue;
      
      for(int k = 0; k < ndau; ++ k) {
	TLorentzVector gen4mom;
	const Candidate * d = cand.daughter( k );
	int dauId = d->pdgId();

	if (abs(dauId)!=333 && abs(dauId)!=211 ) continue;

	if (dauId==333){
	  if (debug) cout << "Phi found!" << endl;
	  int ndauphi=d->numberOfDaughters();

	  for(int k1 = 0; k1 < ndauphi; ++ k1) {
	    const Candidate * d1 = d->daughter( k1 );
	    int dauphiId = d1->pdgId();

	    if (abs(dauphiId)==13) {
	      gen4mom.SetPtEtaPhiM(d1->pt(),d1->eta(),d1->phi(),d1->mass());
	      TheGenMus.push_back(gen4mom);
	      genId.push_back(dauphiId);
	    }
	  }
	}

	if (abs(dauId)==211) {
	  gen4mom.SetPtEtaPhiM(d->pt(),d->eta(),d->phi(),d->mass());
	  TheGenMus.push_back(gen4mom);
	  genId.push_back(dauId);
	}
      }
    }    
  }

  if (debug){
    cout << "Gen particles:" << endl;
    for(uint s=0; s<genId.size(); s++) {
      cout << " " << genId[s] << " Pt " << TheGenMus[s].Pt() << endl;
    }
  }
  if (TheGenMus.size()!=3){
    cout << "This is not Signal nor Normalization sample!!" << endl;
    return;
  }
  else{
    if (isSignal)sort(TheGenMus.begin(), TheGenMus.end(), sortTLorentzByPt);
      _Mu1_4MomG->SetPtEtaPhiM(TheGenMus[0].Pt(),TheGenMus[0].Eta(),TheGenMus[0].Phi(),0.1057);
      _Mu2_4MomG->SetPtEtaPhiM(TheGenMus[1].Pt(),TheGenMus[1].Eta(),TheGenMus[1].Phi(),0.1057);
      if (isSignal) _MuTrack_4MomG->SetPtEtaPhiM(TheGenMus[2].Pt(),TheGenMus[2].Eta(),TheGenMus[2].Phi(),0.1057);
      else  _MuTrack_4MomG->SetPtEtaPhiM(TheGenMus[2].Pt(),TheGenMus[2].Eta(),TheGenMus[2].Phi(),0.1396);
  }

  TLorentzVector dimu=TheGenMus[0]+TheGenMus[1];
  TLorentzVector trimu=dimu+TheGenMus[2];
  _DiMu4MomG->SetPtEtaPhiM(dimu.Pt(),dimu.Eta(),dimu.Phi(),dimu.M());
  _DiMuPlusTrack4MomG->SetPtEtaPhiM(trimu.Pt(),trimu.Eta(),trimu.Phi(),trimu.M());
  if (debug) cout << "Gen object mass " << trimu.M() << endl;
}

bool Tau3MuAnalysis_V2::isMcMatched(const edm::Event& ev,TLorentzVector* recov,std::vector<TLorentzVector>& TheGenMus){

  if (debug) cout << "GEN-RECO Matching ...." << endl;

  bool ThreeMatches=false;

  //see if they match reco muons
  bool RunMatch=true;

  std::vector<int> recoIndexes;
  std::vector<int> genIndexes;

  if (debug) cout << "Matching to reco objects" << endl;

  while (RunMatch){

    double dRtmp=0.05;

    int indR,indG;

    for (int r=0; r<3; r++){

      bool MatchedR=false;
      for (uint i=0; i<recoIndexes.size(); i++){
	if (recoIndexes[i]==r) MatchedR=true;  
      }

      if (MatchedR) continue;

      for (int g=0; g<3; g++){

	bool MatchedG=false;
	for (uint i=0; i<genIndexes.size(); i++){
	  if (genIndexes[i]==g) MatchedG=true;  
	}
	
	if (MatchedG) continue;

	double dR=recov[r].DeltaR(TheGenMus[g]);
	if (dR < dRtmp){
	  if (debug) cout << "Mc match found" << endl;
	  hgenDr->Fill(dR);
	  dRtmp=dR;
	  indR=r;
	  indG=g;
	}
      }
    }

    if (dRtmp==0.05) RunMatch=false;

    else{
      recoIndexes.push_back(indR);
      genIndexes.push_back(indG);
    }

    if (genIndexes.size()==3) RunMatch=false;
  }

  if (debug){
    for (uint i=0; i<genIndexes.size(); i++){
      cout << "Gen Mu " << genIndexes[i] << " Matched with offline mu " << recoIndexes[i] << endl;
      cout << "---- GenMom: pT= " << TheGenMus[genIndexes[i]].Pt() << " eta= " << TheGenMus[genIndexes[i]].Eta() << " phi= " << TheGenMus[genIndexes[i]].Phi() << endl;
      cout << "---- RecoMom: pT= " << recov[recoIndexes[i]].Pt() << " eta= " << recov[recoIndexes[i]].Eta() << " phi= " << recov[recoIndexes[i]].Phi() << endl;
    }
  }

  if (genIndexes.size()==3)  ThreeMatches=true;


  return ThreeMatches;
}


std::pair<bool,bool> Tau3MuAnalysis_V2::isMu(const edm::Event& ev,const Track* p, bool& isSA, bool& isGlb, bool& tight){
  bool ItIs=false;
  bool isGood=false;
  edm::Handle<MuonCollection> muons;
  ev.getByLabel("muons",muons);
  for (MuonCollection::const_iterator recoMu = muons->begin();
       recoMu!=muons->end(); ++recoMu){
    if(recoMu->isGlobalMuon() || recoMu->isTrackerMuon()){
      reco::TrackRef inp = recoMu->innerTrack();
      if (inp.isNonnull() && inp.isAvailable()){
	if (inp->pt()==p->pt() && inp->eta()==p->eta()) {
	  ItIs=true;
	  if (isTight(&*recoMu)) tight=true;
	  isGood=muon::isGoodMuon(*recoMu, muon::TMOneStationTight);
	  isSA=recoMu->isStandAloneMuon();
	  isGlb=recoMu->isGlobalMuon();
	  if (debug && ItIs) cout << "3 muons" << endl;
	  if (debug && isGood) cout << "3rd muon is Good" << endl;
	}	
      }
    }
  }
  return make_pair(ItIs,isGood);
}

int Tau3MuAnalysis_V2::countTracksAround(const edm::Event& ev, const edm::EventSetup& iSetup,TLorentzVector* vec, double& dR, TransientVertex& sv ){


  edm::ESHandle<TransientTrackBuilder> Builder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", Builder);

  int N=0;
  Handle<TrackCollection> tracks;
  ev.getByLabel("generalTracks", tracks);
  TLorentzVector TotMom= vec[0]+vec[1]+vec[2];

  for(TrackCollection::const_iterator it = tracks->begin();it != tracks->end(); ++it){
    bool isIn=false;

    TransientTrack ttpi=Builder->build(*it);
    Vertex diMuVtx=Vertex(sv);
    pair<double,double> d0tracktmp=ComputeImpactParameterWrtPoint(ttpi,diMuVtx);
    if (d0tracktmp.first > 0.2) continue; //The track is not close to SV

    TLorentzVector tvec=TLorentzVector(it->px(),it->py(),it->pz(),sqrt(TrackMass*TrackMass+it->p()*it->p()));
    for (int k=0; k<3; k++){
      if (tvec.Px()==vec[k].Px() && tvec.Py()==vec[k].Py() && tvec.Pz()==vec[k].Pz()) isIn=true;
    }
    if (isIn) continue;
    if (TotMom.DeltaR(tvec) < dR) N++;
  }
  return N;
}

void Tau3MuAnalysis_V2::findBestDimuon(const edm::Event& event, const edm::EventSetup& iSetup,MuonCollection& muIn, MuonCollection& dimu, TransientVertex& dimuvtx, Vertex& primaryVertex){
  
  if (debug) cout << "Finding the dimuon candidate" << endl;

  edm::ESHandle<TransientTrackBuilder> Builder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", Builder); 

  int one=1000, two=1000;

  double tmpProb=diMuVprobMin;  
  double Vp0=diMuVprobMin;

  KalmanVertexFitter avf;

  for(uint i=0; i < (muIn.size()-1); ++i){

    TransientVertex tmpvtx;

    reco::TrackRef inone = muIn[i].innerTrack();

    if (!(inone.isNonnull() && inone.isAvailable())) continue;

    if (!muIn[i].isTrackerMuon()) continue;

    for (uint j=i+1; j<muIn.size(); ++j){

      reco::TrackRef intwo = muIn[j].innerTrack();

      if (!(intwo.isNonnull() && intwo.isAvailable())) continue;
     
      if (!muIn[j].isTrackerMuon()) continue;

      ndm++;

      if (OnlyOppositeCharge && muIn[i].charge()==muIn[j].charge()) continue;

      TLorentzVector DiMu=TLorentzVector(muIn[i].innerTrack()->px()+ muIn[j].innerTrack()->px() , muIn[i].innerTrack()->py()+ muIn[j].innerTrack()->py(), muIn[i].innerTrack()->pz()+ muIn[j].innerTrack()->pz(), muIn[i].energy()+ muIn[j].energy());


      //if (!OnlyOppositeCharge && ((DiMu.M()>0.75 && DiMu.M() < 0.85) || (DiMu.M()>0.97 && DiMu.M()<1.07)) ) continue; //veto on w and phi

      if (DiMu.M() > diMuMassMax || DiMu.M() < diMuMassMin) continue;
      
      ndmm++;

      std::vector<TransientTrack> tt;

      TransientTrack tt1=Builder->build(inone);
      TransientTrack tt2=Builder->build(intwo);

      tt.push_back(tt1);
      tt.push_back(tt2);

      tmpvtx=avf.vertex(tt);

      if (!(tmpvtx.isValid())) continue;
      //if (!isVtxErrorOk(tmpvtx)) continue;
      ndmv++;


      double vChi2 = tmpvtx.totalChiSquared();
      double vNDF = tmpvtx.degreesOfFreedom();

      double vProb(TMath::Prob(vChi2,(int)vNDF));

      if (vProb < Vp0) continue;
      ndmvprob++;

      if( vChi2/vNDF > diMuVtxChi2Max) continue;
      ndmchi++; 

      double dzVTX=0.5;

      edm::Handle<VertexCollection> pvHandle;
      event.getByLabel(theVertexLabel, pvHandle );

      for (VertexCollection::const_iterator pvtmp=pvHandle->begin(); pvtmp!=pvHandle->end(); pvtmp++){
	if (fabs(pvtmp->z()-tmpvtx.position().z()) < dzVTX){
	  dzVTX=fabs(pvtmp->z()-tmpvtx.position().z());
	  primaryVertex=(*pvtmp);
	}
      }

      if(Compute_CosPointingAngle(primaryVertex,tmpvtx,DiMu)< diMuCosPointMin) continue;

      pair<double,double> lxytmp=Compute_Lxy_and_Significance(primaryVertex,tmpvtx,DiMu);

      if (debug) cout <<"vertex prob " << vProb << endl;

      if (lxytmp.first < diMuLxyMin || lxytmp.first > diMuLxyMax) continue;
      ndmlxy++;

      if (lxytmp.first/lxytmp.second < diMuLxySigMin) continue;
      ndmlxys++;

      if (vProb < tmpProb) continue;

      if (debug) cout << "Potential DiMu candidate found" << endl;

      tmpProb=vProb;
      one=i;
      two=j;
      dimuvtx=tmpvtx;            
    }
  }

  if (one!=1000){
    dimu.push_back(muIn[one]);
    dimu.push_back(muIn[two]);
  }
}


double  Tau3MuAnalysis_V2::Compute_CosPointingAngle(Vertex& PV, TransientVertex& sv,TLorentzVector& DiMuMom){

  TVector3 pperp;
  pperp.SetXYZ(DiMuMom.Px(),DiMuMom.Py(),0.);

  TVector3 Displacement=TVector3(sv.position().x()-PV.x(),sv.position().y()-PV.y(),0.);

  double cosAlpha=(Displacement.X()*pperp.X()+Displacement.Y()*pperp.Y())/(pperp.Mag()*Displacement.Mag());
  return cosAlpha;
}

pair<double,double> Tau3MuAnalysis_V2::Compute_Lxy_and_Significance(Vertex & primaryVertex, TransientVertex &SV, TLorentzVector& DiMuMom){
  
  if (debug) cout << "computing lxy and error" << endl;

  GlobalPoint v = SV.position();

  double lxy=((v.x()-primaryVertex.x())*DiMuMom.Px()+(v.y()-primaryVertex.y())*DiMuMom.Py())*DiMuMom.M()/pow(DiMuMom.Pt(),2);

  TVector3 pperp(DiMuMom.Px(), DiMuMom.Py(), 0);
  
  ROOT::Math::SVector<double,3> vpperp;

  vpperp[0] = pperp.x();
  vpperp[1] = pperp.y();
  vpperp[2] = 0.;

  GlobalError sVe= (Vertex(SV)).error();
  GlobalError PVe = primaryVertex.error();

  ROOT::Math::SMatrix<double,3,3> vXYe = sVe.matrix() + PVe.matrix();
  double lxyErr = sqrt(ROOT::Math::Similarity(vXYe,vpperp))*DiMuMom.M()/(pperp.Perp2());

  return make_pair(lxy,lxyErr);

}

void Tau3MuAnalysis_V2::vtx(std::vector<TransientTrack>& tt, GlobalPoint & p, GlobalError & ep){

  if (debug) cout << "finding the 2mu vertex" << endl;

  KalmanVertexFitter avf;
  TransientVertex tv=avf.vertex(tt);

  if (tv.isValid()){
    p=tv.position();
    ep=tv.positionError();
  }

}

std::pair<double,double> Tau3MuAnalysis_V2::ComputeImpactParameterWrtPoint(TransientTrack& tt, Vertex& v){

  std::pair<double,double> d0valerr;

  std::pair<bool,Measurement1D> result =IPTools::absoluteTransverseImpactParameter(tt, v); //IPTools::absoluteImpactParameter3D(tt, v);
  double d0_val = result.second.value();
  double d0_err = result.second.error();
  d0valerr=make_pair(d0_val,d0_err);
  return d0valerr;
}


bool Tau3MuAnalysis_V2::TriggerDecision(const edm::Event& ev){

  if (debug) cout << "Reading Trigger decision" << endl;

  bool passed=false;

  // check fired HLT paths
  edm::Handle<edm::TriggerResults> hltresults;
  edm::InputTag trigResultsTag("TriggerResults","",HLT_process);
  ev.getByLabel(trigResultsTag,hltresults);

  if (HLT_paths.size()==0){
    if (debug) cout << "WARNING:No HLT Path Selected, the event will pass!!!" << endl;
    passed=true;
    return passed;
  }

  if (HLT_paths.size()>10){
    cout << "WARNING:Only the first 10 paths will be considered!!!" << endl;
  }


  if (hltresults.isValid()) {
    const edm::TriggerNames TrigNames_ = ev.triggerNames(*hltresults);
    const int ntrigs = hltresults->size();
    for (int itr=0; itr<ntrigs; itr++){
      if (!hltresults->accept(itr)) continue;
      string trigName=TrigNames_.triggerName(itr);
      if (debug) cout<<"Found HLT path "<< trigName<<endl;
      int Tsize=HLT_paths.size();
      for (int i=0; i<min(Tsize,10); ++i){
	if (debug) cout << "accepted " << trigName << endl; 
	if (trigName.find(HLT_paths[i])!=string::npos) {
	  passed=true;
	  _TrigBit[i]=true;
	}
      }
      //      if (trigName=="HLT_Dimuon0_Omega_Phi_v3" || trigName=="HLT_Dimuon0_Omega_Phi_v4" || trigName=="HLT_Tau2Mu_RegPixTrack_v1") passed=true;
    }
  }
  else
    { 
      cout<<"Trigger results not found"<<endl;
    }

  if (passed && (debug)) cout << "Passed!!!!!!" << endl;

  return passed;

}


// ------------ method called to for each event  ------------
void Tau3MuAnalysis_V2::analyze(const edm::Event& ev, const edm::EventSetup& iSetup) {

  if (debug) cout << "//////////// NEW EVENT ///////////" << endl;

  _Run=ev.id().run();
  _Evt=ev.id().event();
  _Lum=ev.id().luminosityBlock();

  Initialize_TreeVars();
  bool triggered=TriggerDecision(ev);
  std::vector<TLorentzVector> TheGenMus;

  if (IsMC){   
    std::vector<pair<TLorentzVector,int> > matches;

    findGenMoms(ev,TheGenMus);
    
    bool matched=false;
    matched=matchAllGen(ev,TheGenMus,matches);

    if (matched){
      _IsGenRecoMatched=true;
      sort(matches.begin(),matches.end(),sortGenIndex);
      _Mu1_4MomR->SetPtEtaPhiM(matches[0].first.Pt(),matches[0].first.Eta(),matches[0].first.Phi(),matches[0].first.M());
      _Mu2_4MomR->SetPtEtaPhiM(matches[1].first.Pt(),matches[1].first.Eta(),matches[1].first.Phi(),matches[1].first.M());
      if (isSignal) (matches[2].first).SetPtEtaPhiM(matches[2].first.Pt(),matches[2].first.Eta(),matches[2].first.Phi(),0.1057);
      else (matches[2].first).SetPtEtaPhiM(matches[2].first.Pt(),matches[2].first.Eta(),matches[2].first.Phi(),0.1396);
      _MuTrack_4MomR->SetPtEtaPhiM(matches[2].first.Pt(),matches[2].first.Eta(),matches[2].first.Phi(),matches[2].first.M());
      TLorentzVector dmu=matches[0].first+matches[1].first;
      _DiMu4MomR->SetPtEtaPhiM(dmu.Pt(),dmu.Eta(),dmu.Phi(),dmu.M());
      TLorentzVector tmu=matches[0].first + matches[1].first + matches[2].first;
      _DiMuPlusTrack4MomR->SetPtEtaPhiM(tmu.Pt(),tmu.Eta(),tmu.Phi(),tmu.M());;
    }
    
    GenTree->Fill();
  }

  Total++;

  if (triggered)  Triggered++;


  string theMuonLabel = "muons";
  theVertexLabel = "offlinePrimaryVerticesWithBS";
    
  // get the muon container
  edm::Handle<MuonCollection> muons;
  ev.getByLabel(theMuonLabel,muons);
    
  // get the vertex collection
  edm::Handle<VertexCollection> pvHandle;
  ev.getByLabel(theVertexLabel, pvHandle );

  if(pvHandle.isValid()) hvtx->Fill(pvHandle->size());
  else return;

  // get the PV
  reco::Vertex primaryVertex;
    
  edm::ESHandle<TransientTrackBuilder> trackBuilder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder); 
    
  MuonCollection muSkim; // to be used to find the best dimuon
  nmuons=0;
   
  // check the validity of the collection
  if(muons.isValid()){
    hnmu->Fill(muons->size());
    _Nmu=muons->size();

    for (MuonCollection::const_iterator recoMu = muons->begin(); recoMu!=muons->end(); ++recoMu){ // loop over all muons
	
      double eta = (*recoMu).eta();
      double phi = (*recoMu).phi();
      double pt = (*recoMu).pt();
      double q=(*recoMu).charge();
      double d0=0;

      TLorentzVector mom=TLorentzVector((*recoMu).px(),(*recoMu).py(),(*recoMu).pz(),(*recoMu).energy());

      if(recoMu->isTrackerMuon()) d0=(*recoMu).innerTrack()->d0();
      double dz=0;
      if(recoMu->isTrackerMuon())dz=(*recoMu).innerTrack()->dz();
      
      string muonType = "";
      if(recoMu->isGlobalMuon()) muonType = " Glb";
      if(recoMu->isStandAloneMuon()) muonType = muonType + " STA";
      if(recoMu->isTrackerMuon()) muonType = muonType + " Trk";
	
      if (debug) cout << "[MuonAnalysis] New Muon found:" << muonType << endl;
      if (debug) cout << "-- eta: " << eta << " phi: " << phi << " pt: " << pt << " q: " << q << " d0: " << d0 << " dz: " << dz << endl;       
	

      if (recoMu->pt() < MinMuPt) continue;
      if (fabs(recoMu->eta()) > 2.1) continue;
      if (!isTight(&*recoMu)) continue;
      nmuons++;
      muSkim.push_back(*recoMu);
    }
  }

  MuonCollection BestDiMu;
    
  TLorentzVector DiMuMom=TLorentzVector(0.,0.,0.,0.);
  TLorentzVector Mu1Mom=TLorentzVector(0.,0.,0.,0.);
  TLorentzVector Mu2Mom=TLorentzVector(0.,0.,0.,0.);
  TLorentzVector pitrack=TLorentzVector(0.,0.,0.,0.);

  TLorentzVector DiMuTrackMom;
  
  TransientVertex tv;
  TransientVertex tv3;
    
  pair<double,double> d0track,d0track3;
  pair<double,double> lxy2, lxy3;

  if (muSkim.size() < 2) return;
  
  hSkim->Fill(muSkim.size());
  
  findBestDimuon(ev,iSetup, muSkim, BestDiMu, tv, primaryVertex);
  
  if (debug) cout << "dimuons size " << BestDiMu.size() << endl;

  if (BestDiMu.size()!=2) return; //only for control

  if (debug) cout << "DiMuons candidate found:" << endl;
  if (debug) cout << "Mu1 -- eta: " << BestDiMu[0].innerTrack()->eta() << " phi: " << BestDiMu[0].innerTrack()->phi() << " pt: " << BestDiMu[0].innerTrack()->pt() << " q: " << BestDiMu[0].innerTrack()->charge() << endl; 
  if (debug) cout << "Mu2 -- eta: "  << BestDiMu[1].innerTrack()->eta() << " phi: " << BestDiMu[1].innerTrack()->phi() << " pt: " << BestDiMu[1].innerTrack()->pt() << " q: " << BestDiMu[1].innerTrack()->charge() << endl;

  FoundDiMu++;

  bool TwoGood=false;
  bool Good1=false,Good2=false;
  int q1=0,q2=0,qtr=0;

  if ((muon::isGoodMuon(BestDiMu[0], muon::TMOneStationTight)) && (muon::isGoodMuon(BestDiMu[1], muon::TMOneStationTight))) TwoGood=true; 

  if (muon::isGoodMuon(BestDiMu[0], muon::TMOneStationTight)) Good1=true;    
  if (muon::isGoodMuon(BestDiMu[1], muon::TMOneStationTight)) Good2=true;

  q1=BestDiMu[0].charge();
  q2=BestDiMu[1].charge();

  _isSA_1=BestDiMu[0].isStandAloneMuon();
  _isSA_2=BestDiMu[1].isStandAloneMuon();

  _isGlb_1=BestDiMu[0].isGlobalMuon();
  _isGlb_2=BestDiMu[1].isGlobalMuon();
    
  Mu1Mom.SetPtEtaPhiM(BestDiMu[0].innerTrack()->pt() , BestDiMu[0].innerTrack()->eta(), BestDiMu[0].innerTrack()->phi(), 0.1057);
  Mu2Mom.SetPtEtaPhiM(BestDiMu[1].innerTrack()->pt() , BestDiMu[1].innerTrack()->eta(), BestDiMu[1].innerTrack()->phi(), 0.1057);
  //Mu2Mom=TLorentzVector(BestDiMu[1].innerTrack()->px() , BestDiMu[1].innerTrack()->py(), BestDiMu[1].innerTrack()->pz(), BestDiMu[1].energy());
    
  DiMuMom=Mu1Mom+Mu2Mom;
     
  if (debug) cout << "dimuon mass " << DiMuMom.M() << endl;

  lxy2=Compute_Lxy_and_Significance(primaryVertex,tv,DiMuMom);

  double v2Chi2 = tv.totalChiSquared();
  double v2NDF  = tv.degreesOfFreedom();
  double v2Prob(TMath::Prob(v2Chi2,(int)v2NDF));
  
  bool isAlsoMu=false;
  bool isAlsoGoodMu=false;
  Track thetrack;

  findBestPiCand(ev, iSetup, BestDiMu, tv3, primaryVertex, tv, d0track, d0track3 ,pitrack, isAlsoMu, isAlsoGoodMu, qtr, thetrack);

  if (pitrack.Px() !=0 && pitrack.Py()!=0 ){  //just a way to say that pitrack has been found

    Offline++;

    if (debug) cout << "track found" << endl;
    if (debug) cout << "eta " << pitrack.Eta() << " phi " << pitrack.Phi() << " pT " << pitrack.Pt() << endl;

    DiMuTrackMom = DiMuMom+pitrack;

    if (debug) cout << " 3Mu Inv. Mass= " <<  DiMuTrackMom.M() << endl;

    TLorentzVector TotMomArray[3]={Mu1Mom, Mu2Mom, pitrack};
    bool isEventMatched=false;
    TVector3 GenSV;

    if (IsMC){
      isEventMatched=isMcMatched(ev,TotMomArray,TheGenMus);
      if (isEventMatched) GenMatches++;
    }

    Vertex tvv=Vertex(tv);

    
    double cos2=Compute_CosPointingAngle(primaryVertex,tv,DiMuMom);
    double cos3=Compute_CosPointingAngle(primaryVertex,tv3,DiMuTrackMom);

    if (debug) cout << " Cos Pointing Angle diMu= " << cos2 << endl;
    if (debug) cout << " Cos Pointing Angle diMu + Track= " << cos3 << endl;

    hcosPointing2->Fill(cos2);
    hcosPointing3->Fill(cos3);

    int NDr = countTracksAround(ev,iSetup,TotMomArray,DRTracks,tv);	

    lxy3=Compute_Lxy_and_Significance(primaryVertex,tv3,DiMuTrackMom);
    
    double v3Chi2 = tv3.totalChiSquared();
    double v3NDF  = tv3.degreesOfFreedom();
    double v3Prob(TMath::Prob(v3Chi2,(int)v3NDF));

    hDiMuTrackInvMass->Fill(DiMuTrackMom.M());
    
    bool InPV1=isInPV(primaryVertex,Mu1Mom);
    bool InPV2=isInPV(primaryVertex,Mu2Mom);
    bool InPV3=isInPV(primaryVertex,pitrack);

    hpt->Fill(pitrack.Pt());
    
    hDiMuPt->Fill(DiMuMom.Pt());

    hDiMuInvMass->Fill(DiMuMom.M());

    if (TwoGood)  hGoodDiMuInvMass->Fill(DiMuMom.M());

    if (isAlsoMu){
      hptMu->Fill(DiMuTrackMom.Pt());
      hTriMuInvMass->Fill(DiMuTrackMom.M());
    }

    if (TwoGood) hGoodDiMuTrackInvMass->Fill(DiMuTrackMom.M());
     
    if (debug) cout << "total mass " << DiMuTrackMom.M() << endl;
    if (debug) cout << "Filling tree now ... " << endl;

    _DiMu4Mom->SetPtEtaPhiM(DiMuMom.Pt(),DiMuMom.Eta(),DiMuMom.Phi(),DiMuMom.M());

    _DiMuPlusTrack4Mom->SetPtEtaPhiM(DiMuTrackMom.Pt(),DiMuTrackMom.Eta(),DiMuTrackMom.Phi(),DiMuTrackMom.M());

    _Mu2_4Mom->SetPtEtaPhiM(Mu2Mom.Pt(),Mu2Mom.Eta(),Mu2Mom.Phi(),Mu2Mom.M());
    _Mu1_4Mom->SetPtEtaPhiM(Mu1Mom.Pt(),Mu1Mom.Eta(),Mu1Mom.Phi(),Mu1Mom.M());

    _MuTrack_4Mom->SetPtEtaPhiM(pitrack.Pt(),pitrack.Eta(),pitrack.Phi(),pitrack.M());
      
    _M3=DiMuTrackMom.M();
    _M2=DiMuMom.M(); 
    _PtT=pitrack.Pt();
    _dRdiMuT=pitrack.DeltaR(DiMuMom);

    _Mu1Q=q1;
    _Mu2Q=q2;
    _Mu3Q=qtr;

    _dzT2=thetrack.dz(tvv.position());
      
    _PV->SetXYZ(primaryVertex.x(),primaryVertex.y(),primaryVertex.z());
    _PVe->SetXYZ(primaryVertex.xError(),primaryVertex.yError(),primaryVertex.zError());

    
    _SV->SetXYZ(tv.position().x(),tv.position().y(),tv.position().z());
    _SVe->SetXYZ(tv.positionError().cxx(),tv.positionError().cyy(),tv.positionError().czz());

    _SVT->SetXYZ(tv3.position().x(),tv3.position().y(),tv3.position().z());
    _SVTe->SetXYZ(tv3.positionError().cxx(),tv3.positionError().cyy(),tv3.positionError().czz());
      
    _SVchi=v2Chi2/v2NDF;
    _SVprob=v2Prob;

    _SVTchi=v3Chi2/v3NDF;
    _SVTprob=v3Prob;

    _Lxy=lxy2.first;
    _LxySig=lxy2.first/lxy2.second;

    _LxyT=lxy3.first;
    _LxyTSig=lxy3.first/lxy3.second;

    _d0T=d0track.first;
    _d0T3=d0track3.first;
    _d0TSig=d0track.first/d0track.second;
    _d0T3Sig=d0track3.first/d0track3.second;
      
    _IsTrig=triggered;
    _cosp2=cos2;
    _cosp3=cos3;

    _TrackIsMu=isAlsoMu;
    _TrackIsGoodMu=isAlsoGoodMu;

    _NTracksInDr=NDr;
    _Mu1IsGood=Good1;
    _Mu2IsGood=Good2;

    _IsMu1InPV =InPV1;
    _IsMu2InPV=InPV2;
    _IsMu3InPV=InPV3;
    _IsMcMatched=isEventMatched;

    ExTree->Fill();

    if (debug) cout << "Tree filled" << endl;
  }    
}

void Tau3MuAnalysis_V2::Initialize_TreeVars(){

  for (int k=0; k<10; k++){
    _TrigBit[k]=false;
  }

  _Run=-1;
  _Lum=-1;
  _Evt=-1;

  _isTight_Tk=false;
  _isGlb_1=false; 
  _isGlb_2=false;
  _isGlb_Tk=false;

  _isSA_1=false; 
  _isSA_2=false;
  _isSA_Tk=false;


  _DiMu4Mom->SetPtEtaPhiM(0.,0.,0.,0.);
  _DiMuPlusTrack4Mom->SetPtEtaPhiM(0.,0.,0.,0.);

  _Mu1_4Mom->SetPtEtaPhiM(0.,0.,0.,0.);
  _Mu2_4Mom->SetPtEtaPhiM(0.,0.,0.,0.);

  _MuTrack_4Mom->SetPtEtaPhiM(0.,0.,0.,0.);


  if (IsMC){
    _IsGenRecoMatched=false;
    _IsOffline=false;

    _DiMu4MomR->SetPtEtaPhiM(0.,0.,0.,0.);
    _DiMuPlusTrack4MomR->SetPtEtaPhiM(0.,0.,0.,0.);
  
    _Mu1_4MomR->SetPtEtaPhiM(0.,0.,0.,0.);
    _Mu2_4MomR->SetPtEtaPhiM(0.,0.,0.,0.);

    _MuTrack_4MomR->SetPtEtaPhiM(0.,0.,0.,0.);

    _DiMu4MomG->SetPtEtaPhiM(0.,0.,0.,0.);
    _DiMuPlusTrack4MomG->SetPtEtaPhiM(0.,0.,0.,0.);

    _Mu1_4MomG->SetPtEtaPhiM(0.,0.,0.,0.);
    _Mu2_4MomG->SetPtEtaPhiM(0.,0.,0.,0.);

    _MuTrack_4MomG->SetPtEtaPhiM(0.,0.,0.,0.);
  }

  _Mu1Q=0;_Mu2Q=0;_Mu3Q=0;

 
  _PV->SetXYZ(0.,0.,0.);
  _SV->SetXYZ(0.,0.,0.);
  _SVT->SetXYZ(0.,0.,0.);

  _dzT2=-99;
  _M3=0;
  _M2=0; 
  _PtT=0;
  _dRdiMuT=0;
  _SVchi=-99;
  _SVprob=-99;
  _SVTchi=-99;
  _SVTprob=-99;
  _Lxy=-99;
  _LxySig=-99;
  _LxyT=-99;
  _LxyTSig=-99;
  _d0T=-99;
  _d0T3=-99;
  _cosp2=-99;
  _cosp3=-99;
  _d0TSig=-99;
  _Nmu=0;
  _NTracksInDr=-1;

  _TrackIsMu=false;
  _Mu1IsGood=false;
  _Mu2IsGood=false;

  _TrackIsGoodMu=false;
  _IsTrig=false;
  _IsMu1InPV=false;
  _IsMu2InPV=false;
  _IsMu3InPV=false;
  _IsMcMatched=false;
}


bool Tau3MuAnalysis_V2::matchAllGen(const edm::Event& ev,std::vector<TLorentzVector>& genv, std::vector<std::pair<TLorentzVector,int> >& matches){
 
  bool isMatched=false;
  bool runMatch=true;

  std::vector<int> genIndexes;
  std::vector<int> recoIndexes;

  Handle<TrackCollection> tracks;
  ev.getByLabel("generalTracks", tracks);
  if (!tracks.isValid()) return isMatched;

  while(runMatch){

    double dRtmp=0.05;
    uint tcount=0;
    int gindex=-999,tindex=-999;
    TLorentzVector tmpmatch;

    for(uint g=0;g < genv.size();g++){

      if (alreadyMatched(g,genIndexes)) continue;

      for(TrackCollection::const_iterator it = tracks->begin();it != tracks->end(); ++it){
	tcount++;

	if (alreadyMatched(tcount,recoIndexes)) continue;

	TLorentzVector t=TLorentzVector(it->px(),it->py(),it->pz(),sqrt(TrackMass*TrackMass+it->p()*it->p()));

	if (t.DeltaR(genv[g])<dRtmp){
	  dRtmp=t.DeltaR(genv[g]);
	  gindex=g;
	  tindex=tcount;
	  tmpmatch=t;
	}
      }
    }

    if (dRtmp==0.05) runMatch=false;
    else{
      genIndexes.push_back(gindex);
      recoIndexes.push_back(tindex);
      matches.push_back(make_pair(tmpmatch,gindex));
    }
   
    if (matches.size()==3){
      runMatch=false;
      isMatched=true;
    }
  }
  cout << "matched objects indexes:" << endl;
  for(uint i=0; i<matches.size();i++) cout << matches[i].second << " Pt " << (matches[i].first).Pt()<< endl;

  return isMatched;
}

// ------------ method called once each job just before starting event loop  ------------
void Tau3MuAnalysis_V2::beginJob() {

  thefile = new TFile (FileName.c_str(), "RECREATE" );
  thefile->cd();

  if (IsMC){

    GenTree = new TTree("treeGen","treeGen");

    _DiMu4MomG= new TLorentzVector(0.,0.,0.,0.);
    _DiMuPlusTrack4MomG= new TLorentzVector(0.,0.,0.,0.);
    
    _Mu1_4MomG= new TLorentzVector(0.,0.,0.,0.);
    _Mu2_4MomG= new TLorentzVector(0.,0.,0.,0.);
    _MuTrack_4MomG= new TLorentzVector(0.,0.,0.,0.);

    _DiMu4MomR= new TLorentzVector(0.,0.,0.,0.);
    _DiMuPlusTrack4MomR= new TLorentzVector(0.,0.,0.,0.);

    _Mu1_4MomR= new TLorentzVector(0.,0.,0.,0.);
    _Mu2_4MomR= new TLorentzVector(0.,0.,0.,0.);
    _MuTrack_4MomR= new TLorentzVector(0.,0.,0.,0.);

    int Tsize=HLT_paths.size();

    for (int i=0; i< min(Tsize,10); ++i){
      GenTree->Branch(HLT_paths[i].c_str(), &_TrigBit[i],"_TrigBit/B");
    }

    GenTree->Branch("IsRecoMatched",&_IsGenRecoMatched   ,"_IsGenRecoMatched/B");
    GenTree->Branch("DiMu4MomGen","TLorentzVector",&_DiMu4MomG); 
    GenTree->Branch("DiMuPlusTrack4MomGen","TLorentzVector",&_DiMuPlusTrack4MomG); 

    GenTree->Branch("Mu1_4MomGen","TLorentzVector",&_Mu1_4MomG); 
    GenTree->Branch("Mu2_4MomGen","TLorentzVector",&_Mu2_4MomG); 
    GenTree->Branch("MuTrack_4MomGen","TLorentzVector",&_MuTrack_4MomG);  


    GenTree->Branch("DiMu4MomRec","TLorentzVector",&_DiMu4MomR); 
    GenTree->Branch("DiMuPlusTrack4MomRec","TLorentzVector",&_DiMuPlusTrack4MomR); 

    GenTree->Branch("Mu1_4MomRec","TLorentzVector",&_Mu1_4MomR); 
    GenTree->Branch("Mu2_4MomRec","TLorentzVector",&_Mu2_4MomR); 
    GenTree->Branch("MuTrack_4MomRec","TLorentzVector",&_MuTrack_4MomR);   
  }

  ExTree = new TTree("tree","tree");

  _DiMu4Mom= new TLorentzVector(0.,0.,0.,0.);
  _DiMuPlusTrack4Mom= new TLorentzVector(0.,0.,0.,0.);

  _Mu1_4Mom= new TLorentzVector(0.,0.,0.,0.);
  _Mu2_4Mom= new TLorentzVector(0.,0.,0.,0.);
  _MuTrack_4Mom= new TLorentzVector(0.,0.,0.,0.);
  
  _PV= new TVector3(0.,0.,0.);
  _SV=new TVector3(0.,0.,0.);
  _SVT=new TVector3(0.,0.,0.);

  _PVe= new TVector3(0.,0.,0.);
  _SVe=new TVector3(0.,0.,0.);
  _SVTe=new TVector3(0.,0.,0.);

  int Tsize=HLT_paths.size();

  for (int i=0; i< min(Tsize,10); ++i){
    ExTree->Branch(HLT_paths[i].c_str(), &_TrigBit[i],"_TrigBit/B");
  }

  ExTree->Branch("DiMu4Mom","TLorentzVector",&_DiMu4Mom); 
  ExTree->Branch("DiMuPlusTrack4Mom","TLorentzVector",&_DiMuPlusTrack4Mom); 

  ExTree->Branch("Mu1_4Mom","TLorentzVector",&_Mu1_4Mom); 
  ExTree->Branch("Mu2_4Mom","TLorentzVector",&_Mu2_4Mom); 
  ExTree->Branch("MuTrack_4Mom","TLorentzVector",&_MuTrack_4Mom); 

  ExTree->Branch("PV","TVector3",&_PV); 
  ExTree->Branch("SV","TVector3",&_SV);
  ExTree->Branch("SVT","TVector3",&_SVT);

  ExTree->Branch("PVerr","TVector3",&_PVe); 
  ExTree->Branch("SVerr","TVector3",&_SVe);
  ExTree->Branch("SVTerr","TVector3",&_SVTe);

  ExTree->Branch("Run",&_Run   , "_Run/I");
  ExTree->Branch("Lumi",&_Lum   , "_Lum/I");
  ExTree->Branch("Event",&_Evt   , "_Evt/I");

  ExTree->Branch("Mu1Q",&_Mu1Q   , "_Mu1Q/I");
  ExTree->Branch("Mu2Q",&_Mu2Q   , "_Mu2Q/I");
  ExTree->Branch("Mu3Q",&_Mu3Q   , "_Mu3Q/I");

  ExTree->Branch("NTracksInDr", &_NTracksInDr , "_NTracksInDr/I");
  ExTree->Branch("Nmu", &_Nmu , "_Nmu/I");
  
  ExTree->Branch("SVchi",&_SVchi   ,"_SVchi/D"); 
  ExTree->Branch("SVprob",&_SVprob   ,"_SVprob/D"); 
  ExTree->Branch("SVTchi",&_SVTchi   ,"_SVTchi/D"); 
  ExTree->Branch("SVTprob",&_SVTprob   ,"_SVTprob/D"); 

  ExTree->Branch("MinvDiMuT",&_M3   ,"_M3/D");
  ExTree->Branch("MinvDiMu",&_M2   ,"_M2/D");
  ExTree->Branch("PtTrack",&_PtT   ,"_PtT/D");
  ExTree->Branch("dRTrackDiMu",&_dRdiMuT   ,"_dRdiMuT/D");

  ExTree->Branch("Lxy",&_Lxy   ,"_Lxy/D");
  ExTree->Branch("LxySig",&_LxySig   ,"_LxySig/D");
  ExTree->Branch("LxyT",&_LxyT   ,"_LxyT/D");
  ExTree->Branch("LxyTSig",&_LxyTSig   ,"_LxyTSig/D");
  ExTree->Branch("dzT2vtx",&_dzT2   ,"_dzT2/D");
  ExTree->Branch("d0T2vtx",&_d0T   ,"_d0T/D");
  ExTree->Branch("d0T3vtx",&_d0T3   ,"_d0T3/D");
  ExTree->Branch("d0TSig",&_d0TSig   ,"_d0TSig/D");
  ExTree->Branch("d0T3Sig",&_d0T3Sig   ,"_d0T3Sig/D");

  ExTree->Branch("CosPoint2",&_cosp2   ,"_cosp2/D");
  ExTree->Branch("CosPoint3",&_cosp3   ,"_cosp3/D");

  ExTree->Branch("Mu1IsSA",&_isSA_1   ,"_isSA_1/B");
  ExTree->Branch("Mu2IsSA",&_isSA_2   ,"_isSA_2/B");
  ExTree->Branch("TkIsSAmuon",&_isSA_Tk  ,"_isSA_Tk/B");

  ExTree->Branch("TkIsTightMuon",&_isTight_Tk   ,"_isTight_Tk/B");

  ExTree->Branch("Mu1IsGlb",&_isGlb_1   ,"_isGlb_1/B");
  ExTree->Branch("Mu2IsGlb",&_isGlb_2   ,"_isGlb_2/B");
  ExTree->Branch("TkIsGlbMuon",&_isGlb_Tk  ,"_isGlb_Tk/B");

  ExTree->Branch("Mu1IsGood",&_Mu1IsGood   ,"_Mu1IsGood/B");
  ExTree->Branch("Mu2IsGood",&_Mu2IsGood   ,"_Mu2IsGood/B");
  ExTree->Branch("TrackIsGoodMu",&_TrackIsGoodMu   ,"_TrackIsGoodMu/B");
  ExTree->Branch("TrackIsMu",&_TrackIsMu ,"_TrackIsMu/B");

  ExTree->Branch("IsMu1InPV",&_IsMu1InPV ,"_IsMu1InPV/B");
  ExTree->Branch("IsMu2InPV",&_IsMu2InPV ,"_IsMu2InPV/B");
  ExTree->Branch("IsMu3InPV",&_IsMu3InPV ,"_IsMu3InPV/B");

  ExTree->Branch("TriggerDecision",&_IsTrig ,"_IsTrig/B");

  ExTree->Branch("IsMcMatched",&_IsMcMatched ,"_IsMcMatched/B");

  hcosPointing2=new TH1F("CosPointing2","CosPointing2",200,-1,1);
  hcosPointing3=new TH1F("CosPointing3","CosPointing3",200,-1,1);

  hSkim= new TH1F("Nskim","Nskim",16,-0.5,15.5);

  hpt= new TH1F("TrackPT","Track pT",250,0,50);
  hptMu= new TH1F("TrackMuPT","Track with MuId pT",250,0,50);

  hnmu= new TH1F("Nmu","Nmu",16,-0.5,15.5);
  hnt= new TH1F("Ntracks","Ntracks",56,-0.5,55.5);
  hvtx= new TH1F("NPV","NPV",46,-0.5,45.5);

  hDiMuPt=new TH1F("hDiMuPt","DiMuonPt",250,0.,50);

  hDiMuInvMass= new TH1F("hDiMuInvMass","DiMuon Inv. Mass",100,diMuMassMin,diMuMassMax);
  hGoodDiMuInvMass= new TH1F("hGoodDiMuInvMass","Good DiMuon Inv. Mass",100,diMuMassMin,diMuMassMax);

  hTriMuInvMass= new TH1F("hTriMuInvMass","TriMuon Inv. Mass",100,diMuTrackMassMin,diMuTrackMassMax);

  hGoodDiMuTrackInvMass= new TH1F("hGoodDiMuTrackInvMass","Good DiMuon+Track Inv. Mass",100,diMuTrackMassMin,diMuTrackMassMax);
  hDiMuTrackInvMass= new TH1F("hDiMuTrackInvMass","DiMuon+Track Inv. Mass",100,diMuTrackMassMin,diMuTrackMassMax);

  hgenDr= new TH1F("MatchDR","MatchDr",50,0,0.05);
  
  htotEff=new TH1F("TotEff","Tot Eff",4,-0.5,3.5);
  hDiMuEff=new TH1F("DiMuEff","DiMuEff",9,-0.5,8.5);
  hTrackEff=new TH1F("TrackEff","TrackEff",12,-0.5,11.5);
  
  hpt->Sumw2();
  hptMu->Sumw2();
  hDiMuPt->Sumw2();

  hTriMuInvMass->Sumw2();
  hDiMuInvMass->Sumw2();
  hGoodDiMuInvMass->Sumw2();

  hDiMuTrackInvMass->Sumw2();
  hGoodDiMuTrackInvMass->Sumw2();

}




void 
Tau3MuAnalysis_V2::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup)
{
}

void 
Tau3MuAnalysis_V2::beginLuminosityBlock(edm::LuminosityBlock const& iLumi, edm::EventSetup const& iSetup)
{
}





// ------------ method called nce each job just after ending the event loop  ------------
void 
Tau3MuAnalysis_V2::endJob() {

  char title[100];
  sprintf(title,"Tot= %5.2f  Passed= %5.2f",Total,Offline);
  htotEff->SetTitle(title);

  htotEff->SetBinContent(1,1);
  htotEff->GetXaxis()->SetBinLabel(1,"tot");

  if (Total!=0) htotEff->SetBinContent(2, Triggered/Total);
  htotEff->GetXaxis()->SetBinLabel(2,"Trigger");

  if (Triggered!=0) htotEff->SetBinContent(3, FoundDiMu/Total);
  htotEff->GetXaxis()->SetBinLabel(3,"DiMu Found");

  if (FoundDiMu!=0) htotEff->SetBinContent(4, Offline/Total);
  htotEff->GetXaxis()->SetBinLabel(4,"Track Found");

 
  //Mu Eff
  sprintf(title,"TotDiMu= %5.2f  PassedDiMu= %5.2f",ndm,FoundDiMu);
  hDiMuEff->SetTitle(title);
  
  hDiMuEff->SetBinContent(1,1);
  hDiMuEff->GetXaxis()->SetBinLabel(1,"tot");
  
  if(ndm!=0){
    hDiMuEff->SetBinContent(2,ndmm/ndm);
    sprintf(title,"InvMassIn(%5.2f,%5.2f)",diMuMassMin, diMuMassMax);
    hDiMuEff->GetXaxis()->SetBinLabel(2,title);
  
    if(ndm !=0) hDiMuEff->SetBinContent(3,ndmv/ndm);
    hDiMuEff->GetXaxis()->SetBinLabel(3,"Vertex Ok");

    hDiMuEff->SetBinContent(4,ndmclos/ndm);
    hDiMuEff->GetXaxis()->SetBinLabel(4,"Close to SV");
  
    if(ndmv!=0) hDiMuEff->SetBinContent(5,ndmvprob/ndm);
    sprintf(title,"Vprob > %5.2f ", diMuVprobMin);
    hDiMuEff->GetXaxis()->SetBinLabel(5,title);
  
    if(ndmvprob!=0) hDiMuEff->SetBinContent(6,ndmchi/ndm);
    sprintf(title,"ch2Vtx < %5.2f",diMuVtxChi2Max);
    hDiMuEff->GetXaxis()->SetBinLabel(6,title);
  
    if(ndmchi!=0) hDiMuEff->SetBinContent(7,ndmlxy/ndm);
    sprintf(title,"Lxy > %5.2f",diMuLxyMin);
    hDiMuEff->GetXaxis()->SetBinLabel(7,title);
  
    if(ndmlxy!=0) hDiMuEff->SetBinContent(8,ndmlxys/ndm);
    sprintf(title,"LxySig > %5.2f",diMuLxySigMin);
    hDiMuEff->GetXaxis()->SetBinLabel(8,title);
  
    if(ndmlxys!=0) hDiMuEff->SetBinContent(9,FoundDiMu/ndm);
    hDiMuEff->GetXaxis()->SetBinLabel(9,"Selected");
  }
  //Tracks eff
  sprintf(title,"TotTracks= %5.2f  PassedTracks= %5.2f",nt,Offline);
  
  hTrackEff->SetTitle(title); 
  hTrackEff->SetBinContent(1,1);
  hTrackEff->GetXaxis()->SetBinLabel(1,"tot");
  
  if(nt!=0){
    hTrackEff->SetBinContent(2,ntq/nt);
    hTrackEff->GetXaxis()->SetBinLabel(2,"Quality Ok");
  
    if(ntq!=0) hTrackEff->SetBinContent(3,ntm/nt);
    sprintf(title,"InvMassIn(%5.2f,%5.2f)",diMuTrackMassMin,diMuTrackMassMax);
    hTrackEff->GetXaxis()->SetBinLabel(3,title);
  
    if(ntm!=0) hTrackEff->SetBinContent(4,ntclos/nt);
    hTrackEff->GetXaxis()->SetBinLabel(4,"Close to SV");

    if(ntm!=0) hTrackEff->SetBinContent(5,ntd0/nt);
    sprintf(title,"d0 wrt SV < %5.2f",Trackd0Max);
    hTrackEff->GetXaxis()->SetBinLabel(5,title);
  
    if(ntd0!=0) hTrackEff->SetBinContent(6,ntd0s/nt);
    sprintf(title,"d0sig  > %5.2f",Trackd0SigMin);
    hTrackEff->GetXaxis()->SetBinLabel(6,title);
  
    if(ntd0s!=0) hTrackEff->SetBinContent(7,ntv/nt);
    hTrackEff->GetXaxis()->SetBinLabel(7,"Vertex Ok");
  
    if(ntv!=0) hTrackEff->SetBinContent(8,ntvprob/nt);
    sprintf(title,"Vprob > %5.2f ", diMuTrackVprobMin);
    hTrackEff->GetXaxis()->SetBinLabel(8,title);
  
    if(ntvprob!=0) hTrackEff->SetBinContent(9,ntchi/nt);
    sprintf(title,"ch2Vtx < %5.2f",diMuTrackVtxChi2Max);
    hTrackEff->GetXaxis()->SetBinLabel(9,title);
    
    if(ntchi!=0) hTrackEff->SetBinContent(10,ntlxy/nt);
    sprintf(title,"Lxy > %5.2f",diMuTrackLxyMin);
    hTrackEff->GetXaxis()->SetBinLabel(10,title);
    
    if(ntlxy!=0) hTrackEff->SetBinContent(11,ntlxys/nt);
    sprintf(title,"LxySig > %5.2f",diMuTrackLxySigMin);
    hTrackEff->GetXaxis()->SetBinLabel(11,title);
    
    if(ntlxys!=0) hTrackEff->SetBinContent(12,Offline/nt);
    hTrackEff->GetXaxis()->SetBinLabel(12,"Selected");
  }
 
  thefile->cd();

  //some control histos
  hpt->Write();
  hptMu->Write();
  hDiMuPt->Write();
  htotEff->Write();
  hgenDr->Write();
  hSkim->Write(); 

  hDiMuEff->Write();
  hTrackEff->Write();
  
  hDiMuInvMass->Write();
  hGoodDiMuInvMass->Write();
  hDiMuTrackInvMass->Write();
  hGoodDiMuTrackInvMass->Write();
  hTriMuInvMass->Write();
  hcosPointing2->Write();
  hcosPointing3->Write();

  hnt->Write();
  hnmu->Write();
  hvtx->Write();
 
  thefile->Write();

  delete hnmu;
  delete hnt;
  delete hvtx;
  delete hcosPointing2;
  delete hcosPointing3;
  delete hpt;
  delete hptMu;
  delete hDiMuPt;
  delete htotEff;
  delete hgenDr;
  delete hSkim;
  delete hDiMuEff;
  delete hTrackEff;
  
  delete hDiMuInvMass;
  delete hGoodDiMuInvMass;
  delete hDiMuTrackInvMass;
  delete hGoodDiMuTrackInvMass;
  delete hTriMuInvMass;

  delete _SVT;
  delete _SV;
  delete _PV;

  delete _SVTe;
  delete _SVe;
  delete _PVe;

  delete _MuTrack_4Mom;
  delete _Mu2_4Mom;
  delete _Mu1_4Mom;
 
  delete _DiMuPlusTrack4Mom;
  delete _DiMu4Mom;

  delete ExTree;
  delete GenTree;

  thefile->Close();
  delete thefile;
  
  std::cout << "Total " << Total << std::endl;
  std::cout << "Triggered " << Triggered << std::endl;
  std::cout << "DiMu Found " << FoundDiMu << std::endl;
  std::cout << "DiMu+Track Found " << Offline << std::endl;
  if (IsMC) std::cout << "Events MC Matched " << GenMatches  << std::endl;
}

#include "FWCore/Framework/interface/MakerMacros.h"  
DEFINE_FWK_MODULE( Tau3MuAnalysis_V2 );
