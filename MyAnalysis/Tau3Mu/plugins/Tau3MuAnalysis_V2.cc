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

//inline bool sortGenIndexTrack(std::pair<TrackCollection::const_iterator,int> i1, std::pair<TrackCollection::const_iterator,int> i2) {
inline bool sortGenIndexTrack(std::pair<const Track*,int> i1, std::pair<const Track*,int> i2) {
  return i1.second < i2.second;
}

inline bool sortGenIndexCand(std::pair<const Candidate*,int> i1, std::pair<const Candidate*,int> i2) {

  return i1.second < i2.second;
}


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
  virtual void offlineReco(const edm::Event&, const edm::EventSetup&,bool&,std::vector<TLorentzVector>&, bool&);
  virtual Vertex findClosestPV(const edm::Event&, TransientVertex&, bool&);
  virtual void vtx(std::vector<TransientTrack>&, GlobalPoint &, GlobalError &);
  virtual pair<double,double> Compute_Lxy_and_Significance(Vertex &, TransientVertex &, TLorentzVector&);
  virtual void findBestDimuon(const edm::Event&, const edm::EventSetup&, MuonCollection&, MuonCollection&, TransientVertex&, Vertex&);
  virtual void findBestPiCand(const edm::Event&, const edm::EventSetup&, MuonCollection&, TransientVertex&, Vertex&, TransientVertex&,TLorentzVector&,Track&);
  virtual bool isTight(const reco::Muon*);
  virtual bool TriggerDecision(const edm::Event&);
  virtual pair<bool,bool> isMu(const edm::Event&, const Track*, bool&, bool&, bool&);
  virtual int countTracksAround(const edm::Event&, const edm::EventSetup&, TLorentzVector*, double&, TransientVertex&);
  virtual pair<double,double> ComputeImpactParameterWrtPoint(TransientTrack& tt, Vertex&);
  virtual bool isMcMatched(const edm::Event&,TLorentzVector*,std::vector<TLorentzVector>&);
  virtual bool isBkgMatched(const edm::Event&,TLorentzVector*);
  virtual bool isInPV(Vertex&, TLorentzVector&);
  virtual double Compute_CosPointingAngle(Vertex& , TransientVertex& ,TLorentzVector&);
  virtual bool isClose(TransientTrack&, TransientVertex&);
  virtual bool isVtxErrorOk(TransientVertex&);
  virtual bool matchGenReco(const edm::Event&,std::vector<TLorentzVector>&,std::vector<std::pair<TLorentzVector,int> >&,std::vector<pair<const Track*,int> >&);
  virtual void findGenMoms(const edm::Event&, std::vector<TLorentzVector>&);
  virtual bool alreadyMatched(uint&,std::vector<int>);
  virtual bool isVolunteer(const edm::Event&);
  virtual void fillRecoMatchedInfo(const edm::Event&, const edm::EventSetup&, std::vector<pair<const Track*,int> >&);
  virtual void setMuIdToTrack(const edm::Event&, const Track*,bool&,bool&,bool&,bool&,bool&,bool&,int&,int&,int&,int&,double&,double&);
  virtual void setMuIdToMu(Muon &,bool&,bool&,bool&,bool&,bool&,bool&,int&,int&,int&,int&,double&,double&);

  string theVertexLabel;

  TH1F* htotEff,* hDiMuEff, *hTrackEff;

  //PSet parameters
  double diMuMassMin, diMuMassMax, diMuLxyMin, diMuLxyMax,diMuLxySigMin,diMuVtxChi2Max, diMuVprobMin, diMuCosPointMin,diMuTrackCosPointMin;
  double diMuTrackMassMin, diMuTrackMassMax, diMuTrackLxyMin,diMuTrackLxyMax,diMuTrackLxySigMin,diMuTrackVtxChi2Max,diMuTrackVprobMin;
  double MinTrackPt, MinMuPt;
  
  bool IsMC,isSignal,isBkg;

  double TrackMass;
  int nmuons;

  //output files
  TFile* thefile;
  std::string FileName;

  TTree *ExTree;
 
  bool _IsGenRecoMatched,_IsOffline,_TrigBit[10];

  std::vector<string> HLT_paths;
  std::string HLT_process;

  int _Run,_Evt,_Lum,_Nvtx, _Nmu, _Ntk;

  //Gen Level variables
  TLorentzVector* _Mu1_4MomG,*_Mu2_4MomG,*_MuTrack_4MomG, *_DiMu4MomG, *_DiMuPlusTrack4MomG;
  TVector3 *_GenSV;

  int _pdg1,_pdg2,_pdg3;
  int _Mpdg1,_Mpdg2,_Mpdg3;

  //4Mom and Vertices for gen matched Reco objects
  TLorentzVector* _Mu1_4MomR,*_Mu2_4MomR,*_MuTrack_4MomR, *_DiMu4MomR, *_DiMuPlusTrack4MomR;

  TVector3 *_PVR,*_SVR,*_SVTR,*_PVeR,*_SVeR,*_SVTeR;

  bool _svValidR,_svtValidR, _isPVLeadingR;

  double _SVchiR,_SVprobR, _SVTchiR,_SVTprobR;
  double _LxyR,_LxySigR,_LxyTR,_LxyTSigR;

  double _cosp2R,_cosp3R;

  //mu id variables for the gen matched Reco objects
  bool _isTkR1, _isGlbR1, _isSAR1, _isTMOR1, _isTightR1, _isPFR1;
  int _npixR1, _nTkR1, _nMuR1, _qR1;
  double _chiTkR1, _chiMuR1;

  bool _isTkR2, _isGlbR2, _isSAR2, _isTMOR2, _isTightR2, _isPFR2;
  int _npixR2, _nTkR2, _nMuR2, _qR2;
  double _chiTkR2, _chiMuR2;

  bool _isTkR3, _isGlbR3, _isSAR3, _isTMOR3, _isTightR3, _isPFR3;
  int _npixR3, _nTkR3, _nMuR3, _qR3;
  double _chiTkR3, _chiMuR3;
  //

  //Offline Reco variables
  TLorentzVector* _Mu1_4Mom,*_Mu2_4Mom,*_MuTrack_4Mom_Mu,*_MuTrack_4Mom_Pi, *_DiMu4Mom, *_DiMuPlusTrack4Mom_Mu,*_DiMuPlusTrack4Mom_Pi; //4mom both for the pi and mu track guess
  TVector3 *_PV,*_SV,*_SVT,*_PVe,*_SVe,*_SVTe;

  double _SVchi,_SVprob, _SVTchi,_SVTprob;
  double _Lxy,_LxySig,_LxyT,_LxyTSig;

  bool _svValid,_svtValid, _isPVLeading;

  double _cosp2,_cosp3;

  //mu id variables for the Offline objects

  bool _isTk1, _isGlb1, _isSA1, _isTMO1, _isTight1, _isPF1;
  int _npix1, _nTk1, _nMu1, _q1;
  double _chiTk1, _chiMu1;

  bool _isTk2, _isGlb2, _isSA2, _isTMO2, _isTight2, _isPF2;
  int _npix2, _nTk2, _nMu2, _q2;
  double _chiTk2, _chiMu2;

  bool _isTk3, _isGlb3, _isSA3, _isTMO3, _isTight3, _isPF3;
  int _npix3, _nTk3, _nMu3, _q3;
  double _chiTk3, _chiMu3;
  //
 
  bool _IsMcMatched;
 

  bool OnlyOppositeCharge;
  bool debug;

  //counters for efficiency histos

  int ndm, ndmq,ndmv, ndmm, ndmlxy, ndmlxys, ndmchi, ndmvprob, ndmcos;
  int nt, ntq, ntm, ntv, ntlxy, ntlxys, ntchi, ntvprob, ntcos;

  int Total, Triggered, FoundDiMu, Offline, GenMatches, Nvolunteers;
  int  FoundDiMuTrig,OfflineTrig;
  bool triggered; 

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
  FoundDiMuTrig=0;
  OfflineTrig=0;
  GenMatches=0;
  Nvolunteers=0;

  ndm=0; ndmv=0; ndmm=0; ndmlxy=0; ndmlxys=0; ndmchi=0; ndmvprob=0; ndmq=0; ndmcos=0;
  nt=0; ntq=0; ntm=0; ntv=0; ntlxy=0; ntlxys=0; ntchi=0; ntvprob=0; ntcos=0;

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

  IsMC= cfg.getParameter<bool> ("IsMC");
  
  TrackMass= cfg.getParameter<double> ("GuessForTrackMass");

  diMuCosPointMin= cfg.getParameter<double> ("DiMuCosPointMin");
  diMuTrackCosPointMin= cfg.getParameter<double> ("DiMuTrackCosPointMin");

  isSignal=cfg.getParameter<bool> ("isSignal");
  isBkg=cfg.getParameter<bool> ("isBackground");

  debug=cfg.getParameter<bool> ("Debug");

  FileName = cfg.getParameter<std::string> ("OutFileName");

  if (isSignal && isBkg) cout << "WARNING: choose if the MC is Signal or Background!!!" << endl;

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

Vertex Tau3MuAnalysis_V2::findClosestPV(const edm::Event& ev,TransientVertex& sv, bool& isPrimary){
  if (debug) cout << "Searching for the PV closest in z to given SV" << endl;

  double dzVTX=10;
  isPrimary=false;

  Vertex pVertex;
  edm::Handle<VertexCollection> pvHandle;
  ev.getByLabel(theVertexLabel, pvHandle );

  int countVtx=0;
  int vtxIndex=-999;

  for (VertexCollection::const_iterator pvtmp=pvHandle->begin(); pvtmp!=pvHandle->end(); pvtmp++){
    countVtx++;
    if (fabs(pvtmp->z()-sv.position().z()) < dzVTX){
      dzVTX=fabs(pvtmp->z()-sv.position().z());
      if (debug) cout << "closest pv for now has dz wrt sv = " << dzVTX << endl;
      pVertex=(*pvtmp);
      vtxIndex=countVtx;
    }
  }
  if (vtxIndex==1) isPrimary=true;
  return pVertex;
}

bool Tau3MuAnalysis_V2::isTight(const Muon* recoMu){
  if (debug) cout << "Checking if this mu is tight:" << endl;

  bool isTight=false;

  if (!recoMu->isGlobalMuon()) {if (debug) cout << "Is global? " << recoMu->isGlobalMuon() << endl; return isTight;}
  if (!recoMu->isPFMuon()) {if (debug) cout << "Is PF? " << recoMu->isPFMuon() << endl; return isTight;}
  if (!recoMu->isTrackerMuon()) {if (debug) cout << "Is TkMu? " << recoMu->isTrackerMuon() << endl; return isTight;}

  if (recoMu->globalTrack()->normalizedChi2() < 10 && 
      recoMu->globalTrack()->hitPattern().numberOfValidMuonHits() > 2 &&
      recoMu->numberOfMatchedStations() > 1 &&
      recoMu->innerTrack()->hitPattern().numberOfValidPixelHits() > 0 &&
      recoMu->innerTrack()->hitPattern().trackerLayersWithMeasurement() > 5) {isTight=true; if (debug) cout << "is Tight muon!" << endl;}

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

void Tau3MuAnalysis_V2::findBestPiCand(const edm::Event& ev, const edm::EventSetup& iSetup, MuonCollection& dimu ,TransientVertex& tv, Vertex& primaryVertex,TransientVertex& dimuvtx , TLorentzVector& pi, Track& track){

  if (debug) cout << "Looking for the pi track" << endl;

  bool passq=true, passm=true,passvtx=true, passvprob=true, passlxy=true, passlxys=true, passchi=true, passcos=true;
  bool trackFound=false;

  edm::ESHandle<TransientTrackBuilder> Builder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", Builder);

  Handle<TrackCollection> tracks;
  ev.getByLabel("generalTracks", tracks);

  if (!tracks.isValid()) return;

  KalmanVertexFitter avf;

  double tmpProb=diMuTrackVprobMin;
  double Vp0=diMuTrackVprobMin;

  if (triggered) nt++;

  for(TrackCollection::const_iterator it = tracks->begin();it != tracks->end(); ++it){

    if ((it->pt()==dimu[0].innerTrack()->pt() && it->eta()==dimu[0].innerTrack()->eta()) || (it->pt()==dimu[1].innerTrack()->pt() && it->eta()==dimu[1].innerTrack()->eta())) continue;
    if (dimu[0].charge()==dimu[1].charge() && it->charge()==dimu[0].charge()) continue; //impossible to have a particle with charge +/- 3

    bool goodTrack=false;

    if (it->quality(TrackBase::highPurity) && it->pt()> MinTrackPt) goodTrack=true;

    if (!goodTrack) continue;

    if(passq && triggered) {ntq++;passq=false;}

    TLorentzVector m1=TLorentzVector(dimu[0].px(),dimu[0].py(),dimu[0].pz(),dimu[0].energy());
    TLorentzVector m2=TLorentzVector(dimu[1].px(),dimu[1].py(),dimu[1].pz(),dimu[1].energy());
    TLorentzVector p=TLorentzVector(it->px(),it->py(),it->pz(),sqrt(TrackMass*TrackMass+it->p()*it->p()));
    TLorentzVector tot=m1+m2+p;

    if (tot.M() < diMuTrackMassMin || tot.M()> diMuTrackMassMax) continue;
    if (passm && triggered){ ntm++;passm=false;}

    TransientTrack ttpi=Builder->build(*it);

    vector<TransientTrack> tt;
    TransientVertex tmpvtx;

    TransientTrack tt1=Builder->build(dimu[0].innerTrack());
    TransientTrack tt2=Builder->build(dimu[1].innerTrack());

    tt.push_back(tt1);
    tt.push_back(tt2);
    tt.push_back(ttpi);

    tmpvtx=avf.vertex(tt);
    
    if (!tmpvtx.isValid()) continue;
    if (passvtx && triggered) {ntv++;passvtx=false;}

    double vChi2 = tmpvtx.totalChiSquared();
    double vNDF  = tmpvtx.degreesOfFreedom();

    double vProb(TMath::Prob(vChi2,(int)vNDF));

    if (vProb < Vp0) continue;

    if (passvprob && triggered){ntvprob++;passvprob=false;}

    if (vChi2/vNDF > diMuTrackVtxChi2Max) continue;
    if (passchi && triggered){ntchi++;passchi=false;}

    if(Compute_CosPointingAngle(primaryVertex,tmpvtx,tot)< diMuTrackCosPointMin) continue;
    if (passcos && triggered){ntcos++; passcos=false;}

    pair<double,double> lxytmp=Compute_Lxy_and_Significance(primaryVertex,tmpvtx,tot);

    if (lxytmp.first < diMuTrackLxyMin || lxytmp.first > diMuTrackLxyMax ) continue;
    if (passlxy && triggered){ntlxy++;passlxy=false;}

    if (fabs(lxytmp.first)/lxytmp.second < diMuTrackLxySigMin) continue;
    if (passlxys && triggered){ntlxys++;passlxys=false;}

    if (vProb < tmpProb) continue;

    tmpProb=vProb;
    pi=p;
    track=Track(*it);
    tv=tmpvtx;   
    Vertex tmpvtx3=Vertex(tmpvtx);
    trackFound=true;
  }

  if (trackFound) setMuIdToTrack(ev,&track, _isTk3,_isSA3,_isGlb3 ,_isTMO3, _isPF3, _isTight3, _npix3,_nTk3,_nMu3,_q3, _chiTk3,_chiMu3);

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

bool Tau3MuAnalysis_V2::isVolunteer(const edm::Event& ev){
 
  bool itIs=false;
  int nds=0;
  string mcTruthCollection = "genParticles";
  edm::Handle< reco::GenParticleCollection > genParticleHandle;
  ev.getByLabel(mcTruthCollection,genParticleHandle) ;

  if (!(genParticleHandle.isValid())) return true;

  const reco::GenParticleCollection *genParticleCollection = genParticleHandle.product();

  reco::GenParticleCollection::const_iterator genPart;

  for(genPart=genParticleCollection->begin(); genPart!=genParticleCollection->end(); genPart++) {
    const reco::Candidate & cand = *genPart;      
    if (abs(cand.pdgId())!= 431) continue;
    nds++;
  }

  if (debug) cout << "N Ds in event " << nds << endl;
  if (nds>1) itIs=true;
  return itIs;
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

  int nmu=0;

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
	  nmu++; if (nmu==3) _GenSV->SetXYZ(d->vx(),d->vy(),d->vz());
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
	  int nmu=0;
	  for(int k1 = 0; k1 < ndauphi; ++ k1) {
	    const Candidate * d1 = d->daughter( k1 );
	    int dauphiId = d1->pdgId();

	    if (abs(dauphiId)==13) {
	      nmu++; if (nmu==2) _GenSV->SetXYZ(d->vx(),d->vy(),d->vz());
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
    else sort(TheGenMus.begin(), TheGenMus.begin()+2,sortTLorentzByPt);
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

  if (debug) cout << "Offline-Gen Matching ...." << endl;

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

  bool passq=true, passm=true,passvtx=true, passvprob=true, passlxy=true, passlxys=true, passchi=true, passcos=true;

  edm::ESHandle<TransientTrackBuilder> Builder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", Builder); 

  int one=1000, two=1000;

  double tmpProb=diMuVprobMin;  
  double Vp0=diMuVprobMin;

  KalmanVertexFitter avf;

  if (triggered) ndm++;

  for(uint i=0; i < (muIn.size()-1); ++i){

    TransientVertex tmpvtx;

    reco::TrackRef inone = muIn[i].innerTrack();

    if (!(inone.isNonnull() && inone.isAvailable())) continue;

    if (!muIn[i].isTrackerMuon()) continue;

    for (uint j=i+1; j<muIn.size(); ++j){

      reco::TrackRef intwo = muIn[j].innerTrack();

      if (!(intwo.isNonnull() && intwo.isAvailable())) continue;
     
      if (!muIn[j].isTrackerMuon()) continue;

      if (passq && triggered) {ndmq++;passq=false;}

      TLorentzVector DiMu=TLorentzVector(muIn[i].innerTrack()->px()+ muIn[j].innerTrack()->px() , muIn[i].innerTrack()->py()+ muIn[j].innerTrack()->py(), muIn[i].innerTrack()->pz()+ muIn[j].innerTrack()->pz(), muIn[i].energy()+ muIn[j].energy());

      if (DiMu.M() > diMuMassMax || DiMu.M() < diMuMassMin) continue;
      
      if (passm && triggered) {ndmm++; passm=false;}

      std::vector<TransientTrack> tt;

      TransientTrack tt1=Builder->build(inone);
      TransientTrack tt2=Builder->build(intwo);

      tt.push_back(tt1);
      tt.push_back(tt2);

      tmpvtx=avf.vertex(tt);

      if (!(tmpvtx.isValid())) continue;
      if (passvtx && triggered) {ndmv++;passvtx=false;}

      double vChi2 = tmpvtx.totalChiSquared();
      double vNDF = tmpvtx.degreesOfFreedom();
      double vProb(TMath::Prob(vChi2,(int)vNDF));

      if (vProb < Vp0) continue;

      if (passvprob && triggered){ndmvprob++;passvprob=false;}

      if( vChi2/vNDF > diMuVtxChi2Max) continue;

      if(passchi && triggered){ndmchi++;passchi=false;}

      bool isPVLeading=false;

      primaryVertex=findClosestPV(event,tmpvtx,isPVLeading);

      if(Compute_CosPointingAngle(primaryVertex,tmpvtx,DiMu)< diMuCosPointMin) continue;

      if (passcos && triggered) {ndmcos++;passcos=false;}

      pair<double,double> lxytmp=Compute_Lxy_and_Significance(primaryVertex,tmpvtx,DiMu);

      if (debug) cout <<"vertex prob " << vProb << endl;

      if (lxytmp.first < diMuLxyMin || lxytmp.first > diMuLxyMax) continue;
      if (passlxy && triggered) {ndmlxy++;passlxy=false;}

      if (fabs(lxytmp.first)/lxytmp.second < diMuLxySigMin) continue;
      if (passlxys && triggered) {ndmlxys++;passlxys=false;}

      if (vProb < tmpProb) continue;

      if (debug) cout << "Potential DiMu candidate found" << endl;

      tmpProb=vProb;
      _isPVLeading=isPVLeading;
      one=i;
      two=j;
      dimuvtx=tmpvtx;            
    }
  }

  if (one!=1000){
    if (muIn[one].pt()>muIn[two].pt()){ //pt ordered
      dimu.push_back(muIn[one]);
      dimu.push_back(muIn[two]);
    }
    else {
      dimu.push_back(muIn[two]);
      dimu.push_back(muIn[one]);
    }
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

  if (debug) cout << "run " << _Run << " lumi " << _Lum << " event " << _Evt << endl;

  if (IsMC) {

    bool volunteer=false;

    volunteer=isVolunteer(ev);

    if (volunteer) {
      Nvolunteers++;
      if (debug) cout << "Skipping a multiple Ds event" << endl;
      return;
    }
  }

  Initialize_TreeVars();

  //checking the validity of relevant collections

  theVertexLabel = "offlinePrimaryVerticesWithBS";

  //vertices
  edm::Handle<VertexCollection> pvHandle;
  ev.getByLabel(theVertexLabel, pvHandle );
  
  if(pvHandle.isValid()) _Nvtx=int(pvHandle->size());
  else {cout << "PV COLLECTION NOT VALID ... return" << endl; return;}
  
  //tracks
  Handle<TrackCollection> tracks;
  ev.getByLabel("generalTracks", tracks);
  if (tracks.isValid()) _Ntk=int(tracks->size());
  else {cout << "Track COLLECTION NOT VALID ... return" << endl;return;}

  //muons
  edm::Handle<MuonCollection> muons;
  ev.getByLabel("muons",muons);
  if (muons.isValid()) _Nmu=int(muons->size());
  else {cout << "Mu COLLECTION NOT VALID ... return" << endl;return;}

  triggered=TriggerDecision(ev);
  std::vector<TLorentzVector> TheGenMus;

  if (IsMC && !isBkg){   

    if (debug) cout << "Filling Gen and Reco-Gen matched infos ..." << endl;

    std::vector<pair<TLorentzVector,int> > matches;
    std::vector<pair<const Track*,int> > tmatches;

    findGenMoms(ev,TheGenMus);
    
    bool matched=false;
    matched=matchGenReco(ev,TheGenMus,matches,tmatches);

    if (matched){
      _IsGenRecoMatched=true;     
      _Mu1_4MomR->SetPtEtaPhiM(matches[0].first.Pt(),matches[0].first.Eta(),matches[0].first.Phi(),matches[0].first.M());
      _Mu2_4MomR->SetPtEtaPhiM(matches[1].first.Pt(),matches[1].first.Eta(),matches[1].first.Phi(),matches[1].first.M());
      _MuTrack_4MomR->SetPtEtaPhiM(matches[2].first.Pt(),matches[2].first.Eta(),matches[2].first.Phi(),matches[2].first.M());

      TLorentzVector dmu=matches[0].first+matches[1].first;
      _DiMu4MomR->SetPtEtaPhiM(dmu.Pt(),dmu.Eta(),dmu.Phi(),dmu.M());
      TLorentzVector tmu=matches[0].first + matches[1].first + matches[2].first;
      _DiMuPlusTrack4MomR->SetPtEtaPhiM(tmu.Pt(),tmu.Eta(),tmu.Phi(),tmu.M());

      fillRecoMatchedInfo(ev,iSetup,tmatches);
    }
  }

  Total++;

  if (triggered)  Triggered++;

  offlineReco(ev,iSetup,_IsOffline,TheGenMus, triggered);

  if (IsMC && !isBkg) ExTree->Fill();

  if (!IsMC  || (IsMC && isBkg)){
    if (_IsOffline) ExTree->Fill();    
  }
}

void Tau3MuAnalysis_V2::offlineReco(const edm::Event& ev, const edm::EventSetup& iSetup, bool& isOffline,std::vector<TLorentzVector>& TheGenMus, bool& triggered){

  if (debug) cout << "Starting offline selection" << endl;

  //Reconstruction on data
  string theMuonLabel = "muons";
    
  // get the muon container
  edm::Handle<MuonCollection> muons;
  ev.getByLabel(theMuonLabel,muons);
   
  reco::Vertex primaryVertex;
    
  edm::ESHandle<TransientTrackBuilder> trackBuilder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder); 
    
  MuonCollection muSkim; // to be used to find the best dimuon
  nmuons=0;
   
  // check the validity of the collection
  if(muons.isValid()){

    for (MuonCollection::const_iterator recoMu = muons->begin(); recoMu!=muons->end(); ++recoMu){ // loop over all muons
	
      double eta = (*recoMu).eta();
      double phi = (*recoMu).phi();
      double pt = (*recoMu).pt();
      double q=(*recoMu).charge();

      TLorentzVector mom=TLorentzVector((*recoMu).px(),(*recoMu).py(),(*recoMu).pz(),(*recoMu).energy());
      
      string muonType = "";
      if(recoMu->isGlobalMuon()) muonType = " Glb";
      if(recoMu->isStandAloneMuon()) muonType = muonType + " STA";
      if(recoMu->isTrackerMuon()) muonType = muonType + " Trk";
	
      if (debug) cout << "[MuonAnalysis] New Muon found:" << muonType << endl;
      if (debug) cout << "-- eta: " << eta << " phi: " << phi << " pt: " << pt << " q: " << q  << endl;       
      
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

  TLorentzVector pitrack_Mu=TLorentzVector(0.,0.,0.,0.);// the track can be a muon or a pion
  TLorentzVector pitrack_Pi=TLorentzVector(0.,0.,0.,0.);

  TLorentzVector DiMuTrackMom_Mu,DiMuTrackMom_Pi;
  
  TransientVertex tv;
  TransientVertex tv3;
    
  pair<double,double> lxy2, lxy3;

  if (muSkim.size() < 2) return;
  
  findBestDimuon(ev,iSetup, muSkim, BestDiMu, tv, primaryVertex);
  
  if (debug) cout << "dimuons size " << BestDiMu.size() << endl;

  if (BestDiMu.size()!=2) return; //only for control

   FoundDiMu++;
   if (triggered) FoundDiMuTrig++;

  _svValid=true;

  if (debug) cout << "DiMuon candidate found:" << endl;
  if (debug) cout << "Mu1 -- eta: " << BestDiMu[0].innerTrack()->eta() << " phi: " << BestDiMu[0].innerTrack()->phi() << " pt: " << BestDiMu[0].innerTrack()->pt() << " q: " << BestDiMu[0].innerTrack()->charge() << endl; 
  if (debug) cout << "Mu2 -- eta: "  << BestDiMu[1].innerTrack()->eta() << " phi: " << BestDiMu[1].innerTrack()->phi() << " pt: " << BestDiMu[1].innerTrack()->pt() << " q: " << BestDiMu[1].innerTrack()->charge() << endl;

  setMuIdToMu(BestDiMu[0], _isTk1,_isSA1,_isGlb1 ,_isTMO1, _isPF1, _isTight1, _npix1,_nTk1,_nMu1,_q1, _chiTk1,_chiMu1);
  setMuIdToMu(BestDiMu[1], _isTk2,_isSA2,_isGlb2 ,_isTMO2, _isPF2, _isTight2, _npix2,_nTk2,_nMu2,_q2, _chiTk2,_chiMu2);

  Mu1Mom.SetPtEtaPhiM(BestDiMu[0].innerTrack()->pt() , BestDiMu[0].innerTrack()->eta(), BestDiMu[0].innerTrack()->phi(), 0.1057);
  Mu2Mom.SetPtEtaPhiM(BestDiMu[1].innerTrack()->pt() , BestDiMu[1].innerTrack()->eta(), BestDiMu[1].innerTrack()->phi(), 0.1057);
  //Mu2Mom=TLorentzVector(BestDiMu[1].innerTrack()->px() , BestDiMu[1].innerTrack()->py(), BestDiMu[1].innerTrack()->pz(), BestDiMu[1].energy());
    
  DiMuMom=Mu1Mom+Mu2Mom;
     
  if (debug) cout << "dimuon mass " << DiMuMom.M() << endl;

  lxy2=Compute_Lxy_and_Significance(primaryVertex,tv,DiMuMom);

  double v2Chi2 = tv.totalChiSquared();
  double v2NDF  = tv.degreesOfFreedom();
  double v2Prob(TMath::Prob(v2Chi2,(int)v2NDF));
  
  Track thetrack;

  findBestPiCand(ev, iSetup, BestDiMu, tv3, primaryVertex, tv ,pitrack, thetrack);

  if (pitrack.Px() !=0 && pitrack.Py()!=0 ){  //just a way to say that pitrack has been found

    _svtValid=true;

    Offline++;
    if(triggered) OfflineTrig++;

    if (debug) cout << "track found" << endl;
    if (debug) cout << "eta " << pitrack.Eta() << " phi " << pitrack.Phi() << " pT " << pitrack.Pt() << endl;

    pitrack_Mu.SetPtEtaPhiM(pitrack.Pt(),pitrack.Eta(),pitrack.Phi(),0.1057);
    pitrack_Pi.SetPtEtaPhiM(pitrack.Pt(),pitrack.Eta(),pitrack.Phi(),0.1369);

    DiMuTrackMom_Mu = DiMuMom+pitrack_Mu;
    DiMuTrackMom_Pi = DiMuMom+pitrack_Pi;

    if (debug) cout << " 3Mu Inv. Mass= " <<  DiMuTrackMom_Pi.M() << endl;

    TLorentzVector TotMomArray[3]={Mu1Mom, Mu2Mom, pitrack};

    bool isEventMatched=false;

    if (IsMC){
      if (!isBkg) isEventMatched=isMcMatched(ev,TotMomArray,TheGenMus);
      else isEventMatched=isBkgMatched(ev,TotMomArray);
      if (isEventMatched) GenMatches++;
    }

    Vertex tvv=Vertex(tv);
    
    double cos2=Compute_CosPointingAngle(primaryVertex,tv,DiMuMom);
    double cos3=Compute_CosPointingAngle(primaryVertex,tv3,DiMuTrackMom_Mu);

    if (debug) cout << " Cos Pointing Angle diMu= " << cos2 << endl;
    if (debug) cout << " Cos Pointing Angle diMu + Track= " << cos3 << endl;

    lxy3=Compute_Lxy_and_Significance(primaryVertex,tv3,DiMuTrackMom_Mu);
    
    double v3Chi2 = tv3.totalChiSquared();
    double v3NDF  = tv3.degreesOfFreedom();
    double v3Prob(TMath::Prob(v3Chi2,(int)v3NDF));
     
    if (debug) cout << "total mass " << DiMuTrackMom_Pi.M() << endl;
    if (debug) cout << "Filling tree now ... " << endl;

    _DiMu4Mom->SetPtEtaPhiM(DiMuMom.Pt(),DiMuMom.Eta(),DiMuMom.Phi(),DiMuMom.M());

    _DiMuPlusTrack4Mom_Mu->SetPtEtaPhiM(DiMuTrackMom_Mu.Pt(),DiMuTrackMom_Mu.Eta(),DiMuTrackMom_Mu.Phi(),DiMuTrackMom_Mu.M());
    _DiMuPlusTrack4Mom_Pi->SetPtEtaPhiM(DiMuTrackMom_Pi.Pt(),DiMuTrackMom_Pi.Eta(),DiMuTrackMom_Pi.Phi(),DiMuTrackMom_Pi.M());

    _Mu2_4Mom->SetPtEtaPhiM(Mu2Mom.Pt(),Mu2Mom.Eta(),Mu2Mom.Phi(),Mu2Mom.M());
    _Mu1_4Mom->SetPtEtaPhiM(Mu1Mom.Pt(),Mu1Mom.Eta(),Mu1Mom.Phi(),Mu1Mom.M());

    _MuTrack_4Mom_Mu->SetPtEtaPhiM(pitrack_Mu.Pt(),pitrack_Mu.Eta(),pitrack_Mu.Phi(),pitrack_Mu.M());
    _MuTrack_4Mom_Pi->SetPtEtaPhiM(pitrack_Pi.Pt(),pitrack_Pi.Eta(),pitrack_Pi.Phi(),pitrack_Pi.M());
      
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
    _LxySig=fabs(lxy2.first)/lxy2.second;

    _LxyT=lxy3.first;
    _LxyTSig=fabs(lxy3.first)/lxy3.second;

    _cosp2=cos2;
    _cosp3=cos3;
   
    _IsMcMatched=isEventMatched;

    isOffline=true;

    if (debug) cout << "Offline end, filling tree now ..." << endl;
  }
}

void Tau3MuAnalysis_V2::Initialize_TreeVars(){

  if (debug) cout << "Initializing vars for the TTree" << endl;

  triggered=false;

  for (int k=0; k<10; k++){
    _TrigBit[k]=false;
  }

  _Run=-1;
  _Lum=-1;
  _Evt=-1;

  _Nvtx=-1;
  _Nmu=-1;
  _Ntk=-1;

  if (IsMC){

    if (isBkg){
      _pdg1=-999;_pdg2=-999;_pdg3=-999;
      _Mpdg1=-999;_Mpdg2=-999;_Mpdg3=-999;
    }
    else{
      _DiMu4MomG->SetPtEtaPhiM(0.,0.,0.,0.);
      _DiMuPlusTrack4MomG->SetPtEtaPhiM(0.,0.,0.,0.);

      _Mu1_4MomG->SetPtEtaPhiM(0.,0.,0.,0.);
      _Mu2_4MomG->SetPtEtaPhiM(0.,0.,0.,0.);

      _GenSV->SetXYZ(0.,0.,0.);

      _IsGenRecoMatched=false;

      //reco gen-matched
      _DiMu4MomR->SetPtEtaPhiM(0.,0.,0.,0.);
      _DiMuPlusTrack4MomR->SetPtEtaPhiM(0.,0.,0.,0.);
  
      _Mu1_4MomR->SetPtEtaPhiM(0.,0.,0.,0.);
      _Mu2_4MomR->SetPtEtaPhiM(0.,0.,0.,0.);
      
      _MuTrack_4MomR->SetPtEtaPhiM(0.,0.,0.,0.);

      _MuTrack_4MomG->SetPtEtaPhiM(0.,0.,0.,0.);


      _isTkR1=false; _isGlbR1=false; _isSAR1=false; _isTMOR1=false; _isTightR1=false; _isPFR1=false;
      
      _npixR1=-10; _nTkR1=-10; _nMuR1=-10; _qR1=-10;
   
      _chiTkR1=-10; _chiMuR1=-10;


      _isTkR2=false; _isGlbR2=false; _isSAR2=false; _isTMOR2=false; _isTightR2=false; _isPFR2=false;

      _npixR2=-10; _nTkR2=-10; _nMuR2=-10; _qR2=-10;
   
      _chiTkR2=-10; _chiMuR2=-10;


      _isTkR3=false; _isGlbR3=false; _isSAR3=false; _isTMOR3=false; _isTightR3=false; _isPFR3=false;

      _npixR3=-10; _nTkR3=-10; _nMuR3=-10; _qR3=-10;
   
      _chiTkR3=-10; _chiMuR3=-10;

      //reco gen-matched vertices
      _PVR->SetXYZ(0.,0.,0.);
      _SVR->SetXYZ(0.,0.,0.);
      _SVTR->SetXYZ(0.,0.,0.);
    
      _PVeR->SetXYZ(0.,0.,0.);
      _SVeR->SetXYZ(0.,0.,0.);
      _SVTeR->SetXYZ(0.,0.,0.);

      _svValidR=false;
      _svtValidR=false;
      _isPVLeadingR=false;

      _SVchiR=-1;
      _SVprobR=-1;
      _SVTchiR=-1;
      _SVTprobR=-1;
      
      _LxyR=-1;
      _LxySigR=-1;
      _LxyTR=-1;
      _LxyTSigR=-1;

      _cosp2R=-2;
      _cosp3R=-2;

      //
    }

    _IsMcMatched=false;
  }

  _IsOffline=false;

  _DiMu4Mom->SetPtEtaPhiM(0.,0.,0.,0.);
  _DiMuPlusTrack4Mom_Mu->SetPtEtaPhiM(0.,0.,0.,0.);
  _DiMuPlusTrack4Mom_Pi->SetPtEtaPhiM(0.,0.,0.,0.);

  _Mu1_4Mom->SetPtEtaPhiM(0.,0.,0.,0.);
  _Mu2_4Mom->SetPtEtaPhiM(0.,0.,0.,0.);
  
  _MuTrack_4Mom_Mu->SetPtEtaPhiM(0.,0.,0.,0.);
  _MuTrack_4Mom_Pi->SetPtEtaPhiM(0.,0.,0.,0.);


  _isTk1=false; _isGlb1=false; _isSA1=false; _isTMO1=false; _isTight1=false; _isPF1=false;

  _npix1=-10; _nTk1=-10; _nMu1=-10; _q1=-10;
  
  _chiTk1=-10; _chiMu1=-10;


  _isTk2=false; _isGlb2=false; _isSA2=false; _isTMO2=false; _isTight2=false; _isPF2=false;

  _npix2=-10; _nTk2=-10; _nMu2=-10; _q2=-10;
  
  _chiTk2=-10; _chiMu2=-10;


  _isTk3=false; _isGlb3=false; _isSA3=false; _isTMO3=false; _isTight3=false; _isPF3=false;

  _npix3=-10; _nTk3=-10; _nMu3=-10; _q3=-10;
   
  _chiTk3=-10; _chiMu3=-10;

  //Offline vertices
  _PV->SetXYZ(0.,0.,0.);
  _SV->SetXYZ(0.,0.,0.);
  _SVT->SetXYZ(0.,0.,0.);
    
  _PVe->SetXYZ(0.,0.,0.);
  _SVe->SetXYZ(0.,0.,0.);
  _SVTe->SetXYZ(0.,0.,0.);

  _svValid=false;
  _svtValid=false;
  _isPVLeading=false;

  _SVchi=-1;
  _SVprob=-1;
  _SVTchi=-1;
  _SVTprob=-1;

  _Lxy=-1;
  _LxySig=-1;
  _LxyT=-1;
  _LxyTSig=-1;

  _cosp2=-2;
  _cosp3=-2;


 if (debug) cout << "END Initializing vars for the TTree" << endl;
}

bool Tau3MuAnalysis_V2::isBkgMatched(const edm::Event& ev,TLorentzVector* recov){

  if (debug) cout << "Looking for gen particles matching with offline muons" << endl;

  bool isMatched=false;

  //see if they match reco muons
  bool runMatch=true;

  std::vector<pair<const Candidate*,int> > matches;
  std::vector<int> recoIndexes;
  std::vector<int> genIndexes;

  string mcTruthCollection = "genParticles";
  edm::Handle< reco::GenParticleCollection > genParticleHandle;
  ev.getByLabel(mcTruthCollection,genParticleHandle) ;

  if (!(genParticleHandle.isValid())) return isMatched;
 
  while(runMatch){

    double dRtmp=0.05;
    uint tcount=0;
    int gindex=-999,rindex=-999;
    const Candidate* cand;
    //TrackCollection::const_iterator tmpref;
    
    for(uint r=0;r < 3;r++){

      if (alreadyMatched(r,recoIndexes)) continue;

      for(GenParticleCollection::const_iterator it = genParticleHandle->begin(); it != genParticleHandle->end(); ++it){
	tcount++;

	if (alreadyMatched(tcount,genIndexes)) continue;

	TLorentzVector t=TLorentzVector(it->px(),it->py(),it->pz(),it->energy());

	if (it->status()!=1) continue;
	if (t.DeltaR(recov[r]) < dRtmp){
	  dRtmp=t.DeltaR(recov[r]);
	  gindex=tcount;
	  rindex=r;
	  cand=&*it;
	}
      }
    }

    if (dRtmp==0.05) runMatch=false;

    else{
      genIndexes.push_back(gindex);
      recoIndexes.push_back(rindex);
      matches.push_back(make_pair(cand,rindex));
    }

    if (matches.size()==3){
      runMatch=false;
      isMatched=true;
      sort(matches.begin(),matches.end(),sortGenIndexCand);
    }
  }

  if (isMatched){
    _pdg1=matches[0].first->pdgId();
    _Mpdg1=matches[0].first->mother()->pdgId();

    _pdg2=matches[1].first->pdgId();
    _Mpdg2=matches[1].first->mother()->pdgId();

    _pdg3=matches[2].first->pdgId();
    _Mpdg3=matches[2].first->mother()->pdgId();
  }

  return isMatched;
}


bool Tau3MuAnalysis_V2::matchGenReco(const edm::Event& ev,std::vector<TLorentzVector>& genv, std::vector<std::pair<TLorentzVector,int> >& matches,std::vector<pair<const Track*,int> >& tmatches){
 
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
    //TrackCollection::const_iterator tmpref;
    const Track* tmpref;

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
	  tmpref=&*it;
	}
      }
    }

    if (dRtmp==0.05) runMatch=false;
    else{
      genIndexes.push_back(gindex);
      recoIndexes.push_back(tindex);
      matches.push_back(make_pair(tmpmatch,gindex));
      tmatches.push_back(make_pair(tmpref,gindex));
    }
   
    if (matches.size()==3){
      runMatch=false;
      isMatched=true;
      sort(matches.begin(),matches.end(),sortGenIndex);
      sort(tmatches.begin(),tmatches.end(),sortGenIndexTrack);
    }
  }

  if (debug){
    cout << "matched objects indexes:" << endl;
    for(uint i=0; i<matches.size();i++) cout << tmatches[i].second << " Pt " << (tmatches[i].first)->pt()<< endl;
  }
  
  return isMatched;
}

void Tau3MuAnalysis_V2::setMuIdToMu(Muon & mu,bool& isTkMu,bool& isSAMu,bool& isGlbMu,bool& isTMOMu,bool& isPFMu,bool& isTightMu,int& pix,int& tk,int& muh, int& q,double & chiTk,double& chiMu){

  q=mu.charge();

  if (mu.isTrackerMuon()){

    isTkMu=true;

    pix=mu.innerTrack()->hitPattern().numberOfValidPixelHits();
    tk=mu.innerTrack()->hitPattern().numberOfValidTrackerHits();
    chiTk=mu.innerTrack()->normalizedChi2();
  }

  if (mu.isStandAloneMuon()) isSAMu=true;
  if (mu.isGlobalMuon()){
    isGlbMu=true;
    chiMu=mu.globalTrack()->normalizedChi2();
    muh=(mu.globalTrack())->hitPattern().numberOfValidMuonHits();
  }
  if (muon::isGoodMuon(mu, muon::TMOneStationTight)) isTMOMu=true;
  if (mu.isPFMuon()) isPFMu=true;
  if (isTight(&mu)) isTightMu=true;
}

void Tau3MuAnalysis_V2::setMuIdToTrack(const edm::Event& ev, const Track* t,bool& isTkMu,bool& isSAMu,bool& isGlbMu,bool& isTMOMu,bool& isPFMu,bool& isTightMu,int& pix,int& tk,int& muh, int& q,double & chiTk,double& chiMu){

  if (debug) cout << "Setting the mu id" << endl;

  pix=t->hitPattern().numberOfValidPixelHits();
  tk=t->hitPattern().numberOfValidTrackerHits();
  chiTk=t->normalizedChi2();
  q=t->charge();

  edm::Handle<MuonCollection> muons;
  ev.getByLabel("muons",muons);

  for (MuonCollection::const_iterator recoMu = muons->begin();
       recoMu!=muons->end(); ++recoMu){

    if (!recoMu->isTrackerMuon()) continue;

    reco::TrackRef mu = recoMu->innerTrack();

    if (mu.isNonnull() && mu.isAvailable()){
      
      if (mu->pt() != t->pt() && mu->phi() != t->phi()) continue;
      if (debug) cout << "the track is a muon" << endl;
      
      isTkMu=true;
      
      if (recoMu->isStandAloneMuon()) isSAMu=true;
      if (recoMu->isGlobalMuon()){
	isGlbMu=true;
	chiMu=recoMu->globalTrack()->normalizedChi2();
	muh=(recoMu->globalTrack())->hitPattern().numberOfValidMuonHits();
      }
      if (muon::isGoodMuon(*recoMu, muon::TMOneStationTight)) isTMOMu=true;
      if (recoMu->isPFMuon()) isPFMu=true;
      if (isTight(&*recoMu)) isTightMu=true;
    }
  }  
}

void Tau3MuAnalysis_V2::fillRecoMatchedInfo(const edm::Event& event, const edm::EventSetup& iSetup, std::vector<pair<const Track*,int> >&  matches){
  
  if (matches.size()!=3){
    cout << "Only " << matches.size() << " matched objects, this function should not have been called!! " << endl;
    return;
  }

  setMuIdToTrack(event,matches[0].first, _isTkR1,_isSAR1,_isGlbR1 ,_isTMOR1, _isPFR1, _isTightR1, _npixR1,_nTkR1,_nMuR1,_qR1, _chiTkR1,_chiMuR1);
  setMuIdToTrack(event,matches[1].first, _isTkR2,_isSAR2,_isGlbR2 ,_isTMOR2, _isPFR2, _isTightR2, _npixR2,_nTkR2,_nMuR2,_qR2, _chiTkR2,_chiMuR2);
  setMuIdToTrack(event,matches[2].first, _isTkR3,_isSAR3,_isGlbR3 ,_isTMOR3, _isPFR3, _isTightR3, _npixR3,_nTkR3,_nMuR3,_qR3, _chiTkR3,_chiMuR3);

  edm::ESHandle<TransientTrackBuilder> Builder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", Builder);

  vector<TransientTrack> ttv;

  TransientTrack tt1=Builder->build(matches[0].first);
  TransientTrack tt2=Builder->build(matches[1].first);
  TransientTrack tt3=Builder->build(matches[2].first);

  TLorentzVector m1, m2, tr;

  m1.SetPtEtaPhiM(matches[0].first->pt(),matches[0].first->eta(),matches[0].first->phi(),0.1057);
  m2.SetPtEtaPhiM(matches[1].first->pt(),matches[1].first->eta(),matches[1].first->phi(),0.1057);

  TLorentzVector dimu=m1+m2;
  TLorentzVector trimu=dimu+tr;

  if (isSignal) tr.SetPtEtaPhiM(matches[2].first->pt(),matches[2].first->eta(),matches[2].first->phi(),0.1057);
  else tr.SetPtEtaPhiM(matches[2].first->pt(),matches[2].first->eta(),matches[2].first->phi(),0.1369);

  ttv.push_back(tt1);
  ttv.push_back(tt2);

  KalmanVertexFitter avf;

  TransientVertex dimuvtx=avf.vertex(ttv);

  Vertex pvR;

  if (dimuvtx.isValid()){

    _svValidR=true;

    if (debug) cout << " found valid Reco matched dimu vtx " << endl;

    _SVR->SetXYZ(dimuvtx.position().x(),dimuvtx.position().y(),dimuvtx.position().z());
    _SVeR->SetXYZ(dimuvtx.positionError().cxx(),dimuvtx.positionError().cyy(),dimuvtx.positionError().czz());

    _SVchiR=dimuvtx.normalisedChiSquared();
    _SVprobR=TMath::Prob(dimuvtx.totalChiSquared(),dimuvtx.degreesOfFreedom());

    pvR=findClosestPV(event,dimuvtx,_isPVLeadingR);

    pair<double,double> lxy=Compute_Lxy_and_Significance(pvR,dimuvtx,dimu);

    _LxyR=lxy.first;
    _LxySigR=lxy.first/lxy.second;

    _cosp2R=Compute_CosPointingAngle(pvR,dimuvtx,dimu);

  }

  ttv.push_back(tt3);

  TransientVertex trimuvtx=avf.vertex(ttv);

  if (trimuvtx.isValid()){

    _svtValidR=true;

    if (debug) cout << " found valid Reco matched dimu+track vtx " << endl;

    _SVTR->SetXYZ(trimuvtx.position().x(),trimuvtx.position().y(),trimuvtx.position().z());
    _SVTeR->SetXYZ(trimuvtx.positionError().cxx(),trimuvtx.positionError().cyy(),trimuvtx.positionError().czz());

    _SVTchiR=trimuvtx.normalisedChiSquared();
    _SVTprobR=TMath::Prob(trimuvtx.totalChiSquared(),trimuvtx.degreesOfFreedom());

    if (!_svValidR)  pvR=findClosestPV(event,trimuvtx,_isPVLeadingR);

    pair<double,double> lxy=Compute_Lxy_and_Significance(pvR,trimuvtx,trimu);

    _LxyTR=lxy.first;
    _LxyTSigR=lxy.first/lxy.second;

    _cosp3R=Compute_CosPointingAngle(pvR,trimuvtx,trimu);

  }

  return;

}



// ------------ method called once each job just before starting event loop  ------------
void Tau3MuAnalysis_V2::beginJob() {

  if (debug) cout << "begin job" << endl;

  thefile = new TFile (FileName.c_str(), "RECREATE" );
  thefile->cd();

  if (debug) cout << "Creating new tree" << endl;
  ExTree = new TTree("tree","tree");

  int Tsize=HLT_paths.size();

  for (int i=0; i< min(Tsize,10); ++i){
    ExTree->Branch(HLT_paths[i].c_str(), &_TrigBit[i],"_TrigBit/b");
  }

  if (debug) cout << "adding event branches" << endl;

  ExTree->Branch("Run",&_Run   , "_Run/I");
  ExTree->Branch("Lumi",&_Lum   , "_Lum/I");
  ExTree->Branch("Event",&_Evt   , "_Evt/I");

  ExTree->Branch("NumberOfVertices",&_Nvtx   , "_Nvtx/I");
  ExTree->Branch("NumberOfMuons",&_Nmu   , "_Nmu/I");
  ExTree->Branch("NumberOfTracks",&_Ntk   , "_Ntk/I");

  
  if (IsMC){

    if (debug) cout << "adding MC gen branches" << endl;

    if (isBkg){
      ExTree->Branch("pdgId_1",&_pdg1   , "_pdg1/I");
      ExTree->Branch("pdgId_2",&_pdg2   , "_pdg2/I");
      ExTree->Branch("pdgId_3",&_pdg3   , "_pdg3/I");

      ExTree->Branch("Mom_pdgId_1",&_Mpdg1   , "_Mpdg1/I");
      ExTree->Branch("Mom_pdgId_2",&_Mpdg2   , "_Mpdg2/I");
      ExTree->Branch("Mom_pdgId_3",&_Mpdg3   , "_Mpdg3/I");
    }

    else {
      // gen variables
      _DiMu4MomG= new TLorentzVector(0.,0.,0.,0.);
      _DiMuPlusTrack4MomG= new TLorentzVector(0.,0.,0.,0.);
    
      _Mu1_4MomG= new TLorentzVector(0.,0.,0.,0.);
      _Mu2_4MomG= new TLorentzVector(0.,0.,0.,0.);
      _MuTrack_4MomG= new TLorentzVector(0.,0.,0.,0.);
    
      _GenSV=new TVector3(0.,0.,0.);
      
      //reco gen-matched 4momenta
      _DiMu4MomR= new TLorentzVector(0.,0.,0.,0.);
      _DiMuPlusTrack4MomR= new TLorentzVector(0.,0.,0.,0.);

      _Mu1_4MomR= new TLorentzVector(0.,0.,0.,0.);
      _Mu2_4MomR= new TLorentzVector(0.,0.,0.,0.);
      _MuTrack_4MomR= new TLorentzVector(0.,0.,0.,0.);

      //reco gen-matched vertices
      _PVR= new TVector3(0.,0.,0.);
      _SVR=new TVector3(0.,0.,0.);
      _SVTR=new TVector3(0.,0.,0.);

      _PVeR= new TVector3(0.,0.,0.);
      _SVeR=new TVector3(0.,0.,0.);
      _SVTeR=new TVector3(0.,0.,0.);

      //
   
      //Gen variables
      ExTree->Branch("DiMu4Mom_Gen","TLorentzVector",&_DiMu4MomG); 
      ExTree->Branch("DiMuPlusTrack4Mom_Gen","TLorentzVector",&_DiMuPlusTrack4MomG); 
      
      ExTree->Branch("Mu1_4Mom_Gen","TLorentzVector",&_Mu1_4MomG); 
      ExTree->Branch("Mu2_4Mom_Gen","TLorentzVector",&_Mu2_4MomG); 
      ExTree->Branch("MuTrack_4Mom_Gen","TLorentzVector",&_MuTrack_4MomG);  

      ExTree->Branch("SV_Gen","TVector3",&_GenSV); 

      if (debug) cout << "adding Reco MC matched branches" << endl;

      //Reco mc-matched branches
      ExTree->Branch("IsGenRecoMatched",&_IsGenRecoMatched   ,"_IsGenRecoMatched/b");

      ExTree->Branch("DiMu4Mom_Reco","TLorentzVector",&_DiMu4MomR); 
      ExTree->Branch("DiMuPlusTrack4Mom_Reco","TLorentzVector",&_DiMuPlusTrack4MomR); 
      
      ExTree->Branch("Mu1_4Mom_Reco","TLorentzVector",&_Mu1_4MomR); 
      ExTree->Branch("Mu2_4Mom_Reco","TLorentzVector",&_Mu2_4MomR); 
      ExTree->Branch("MuTrack_4Mom_Reco","TLorentzVector",&_MuTrack_4MomR);   
      
      //first muon
      ExTree->Branch("IsTkMu_Reco_1",&_isTkR1   ,"_isTkR1/b");
      ExTree->Branch("IsGlbMu_Reco_1",&_isGlbR1   ,"_isGlbR1/b");
      ExTree->Branch("IsSAMu_Reco_1",&_isSAR1   ,"_isSAR1/b");
      ExTree->Branch("IsTMOMu_Reco_1",&_isTMOR1   ,"_isTMOR1/b");
      ExTree->Branch("IsTightMu_Reco_1",&_isTightR1   ,"_isTightR1/b");
      ExTree->Branch("IsPFMu_Reco_1",&_isPFR1   ,"_isPFR1/b");
      
      ExTree->Branch("nPixHits_Reco_1",&_npixR1   ,"_npixR1/I");
      ExTree->Branch("nTkHits_Reco_1",&_nTkR1   ,"_nTkR1/I");
      ExTree->Branch("nMuHits_Reco_1",&_nMuR1   ,"_nMuR1/I");
      ExTree->Branch("Q_Reco_1",&_qR1   ,"_qR1/I");

      ExTree->Branch("chiTk_Reco_1",&_chiTkR1   ,"_chiTkR1/D");
      ExTree->Branch("chiMu_Reco_1",&_chiMuR1   ,"_chiMuR1/D");

      //second muon
      ExTree->Branch("IsTkMu_Reco_2",&_isTkR2   ,"_isTkR2/b");
      ExTree->Branch("IsGlbMu_Reco_2",&_isGlbR2   ,"_isGlbR2/b");
      ExTree->Branch("IsSAMu_Reco_2",&_isSAR2   ,"_isSAR2/b");
      ExTree->Branch("IsTMOMu_Reco_2",&_isTMOR2   ,"_isTMOR2/b");
      ExTree->Branch("IsTightMu_Reco_2",&_isTightR2   ,"_isTightR2/b");
      ExTree->Branch("IsPFMu_Reco_2",&_isPFR2   ,"_isPFR2/b");

      ExTree->Branch("nPixHits_Reco_2",&_npixR2   ,"_npixR2/I");
      ExTree->Branch("nTkHits_Reco_2",&_nTkR2   ,"_nTkR2/I");
      ExTree->Branch("nMuHits_Reco_2",&_nMuR2   ,"_nMuR2/I");
      ExTree->Branch("Q_Reco_2",&_qR2   ,"_qR2/I");

      ExTree->Branch("chiTk_Reco_2",&_chiTkR2   ,"_chiTkR2/D");
      ExTree->Branch("chiMu_Reco_2",&_chiMuR2   ,"_chiMuR2/D");

      //third mu-track
      ExTree->Branch("IsTkMu_Reco_3",&_isTkR3   ,"_isTkR3/b");
      ExTree->Branch("IsGlbMu_Reco_3",&_isGlbR3   ,"_isGlbR3/b");
      ExTree->Branch("IsSAMu_Reco_3",&_isSAR3   ,"_isSAR3/b");
      ExTree->Branch("IsTMOMu_Reco_3",&_isTMOR3   ,"_isTMOR3/b");
      ExTree->Branch("IsTightMu_Reco_3",&_isTightR3   ,"_isTightR3/b");
      ExTree->Branch("IsPFMu_Reco_3",&_isPFR3   ,"_isPFR3/b");

      ExTree->Branch("nPixHits_Reco_3",&_npixR3   ,"_npixR3/I");
      ExTree->Branch("nTkHits_Reco_3",&_nTkR3   ,"_nTkR3/I");
      ExTree->Branch("nMuHits_Reco_3",&_nMuR3   ,"_nMuR3/I");
      ExTree->Branch("Q_Reco_3",&_qR3   ,"_qR3/I");

      ExTree->Branch("chiTk_Reco_3",&_chiTkR3   ,"_chiTkR3/D");
      ExTree->Branch("chiMu_Reco_3",&_chiMuR3   ,"_chiMuR3/D");
      //

      //Reco GEN matched vertices
 
      ExTree->Branch("isValidSV_Reco",&_svValidR,"_svValidR/b"); 
      ExTree->Branch("isValidSVT_Reco",&_svtValidR,"_svtValidR/b"); 
      ExTree->Branch("isPVLeading_Reco",&_isPVLeadingR,"_isPVLeadingR/b");

      ExTree->Branch("PV_Reco","TVector3",&_PVR); 
      ExTree->Branch("SV_Reco","TVector3",&_SVR);
      ExTree->Branch("SVT_Reco","TVector3",&_SVTR);

      ExTree->Branch("PVerr_Reco","TVector3",&_PVeR); 
      ExTree->Branch("SVerr_Reco","TVector3",&_SVeR);
      ExTree->Branch("SVTerr_Reco","TVector3",&_SVTeR);

      ExTree->Branch("SVchi_Reco",&_SVchiR   ,"_SVchiR/D"); 
      ExTree->Branch("SVprob_Reco",&_SVprobR   ,"_SVprobR/D"); 
      ExTree->Branch("SVTchi_Reco",&_SVTchiR   ,"_SVTchiR/D"); 
      ExTree->Branch("SVTprob_Reco",&_SVTprobR   ,"_SVTprobR/D"); 
      
      ExTree->Branch("CosPoint2_Reco",&_cosp2R   ,"_cosp2R/D");
      ExTree->Branch("CosPoint3_Reco",&_cosp3R   ,"_cosp3R/D");
      //
    }

    ExTree->Branch("IsOfflineMcMatched",&_IsMcMatched ,"_IsMcMatched/b");
  }

  if (debug) cout << "adding Offline branches" << endl;
  //Offline variables

  ExTree->Branch("IsOfflineReco",&_IsOffline,"_IsOffline/b");	

  _DiMu4Mom= new TLorentzVector(0.,0.,0.,0.);
  _DiMuPlusTrack4Mom_Mu= new TLorentzVector(0.,0.,0.,0.);
  _DiMuPlusTrack4Mom_Pi= new TLorentzVector(0.,0.,0.,0.);

  _Mu1_4Mom= new TLorentzVector(0.,0.,0.,0.);
  _Mu2_4Mom= new TLorentzVector(0.,0.,0.,0.);

  _MuTrack_4Mom_Mu= new TLorentzVector(0.,0.,0.,0.);
  _MuTrack_4Mom_Pi= new TLorentzVector(0.,0.,0.,0.);
  
  _PV= new TVector3(0.,0.,0.);
  _SV=new TVector3(0.,0.,0.);
  _SVT=new TVector3(0.,0.,0.);

  _PVe= new TVector3(0.,0.,0.);
  _SVe=new TVector3(0.,0.,0.);
  _SVTe=new TVector3(0.,0.,0.);

  ExTree->Branch("DiMu4Mom_Offline","TLorentzVector",&_DiMu4Mom); 
  ExTree->Branch("DiMuPlusTrack4Mom_Mu_Offline","TLorentzVector",&_DiMuPlusTrack4Mom_Mu); 
  ExTree->Branch("DiMuPlusTrack4Mom_Pi_Offline","TLorentzVector",&_DiMuPlusTrack4Mom_Pi); 

  ExTree->Branch("Mu1_4Mom_Offline","TLorentzVector",&_Mu1_4Mom); 
  ExTree->Branch("Mu2_4Mom_Offline","TLorentzVector",&_Mu2_4Mom); 
  ExTree->Branch("MuTrack_4Mom_Pi_Offline","TLorentzVector",&_MuTrack_4Mom_Pi); 

 //first offline mu   
  ExTree->Branch("IsTkMu_Offline_1",&_isTk1   ,"_isTk1/b");
  ExTree->Branch("IsGlbMu_Offline_1",&_isGlb1   ,"_isGlb1/b");
  ExTree->Branch("IsSAMu_Offline_1",&_isSA1   ,"_isSA1/b");
  ExTree->Branch("IsTMOMu_Offline_1",&_isTMO1   ,"_isTMO1/b");
  ExTree->Branch("IsTightMu_Offline_1",&_isTight1   ,"_isTight1/b");
  ExTree->Branch("IsPFMu_Offline_1",&_isPF1   ,"_isPF1/b");

  ExTree->Branch("nPixHits_Offline_1",&_npix1   ,"_npix1/I");
  ExTree->Branch("nTkHits_Offline_1",&_nTk1   ,"_nTk1/I");
  ExTree->Branch("nMuHits_Offline_1",&_nMu1   ,"_nMu1/I");
  ExTree->Branch("Q_Offline_1",&_q1   ,"_q1/I");

  ExTree->Branch("chiTk_Offline_1",&_chiTk1   ,"_chiTk1/D");
  ExTree->Branch("chiMu_Offline_1",&_chiMu1   ,"_chiMu1/D");
  //
 
  //second offline mu
  ExTree->Branch("IsTkMu_Offline_2",&_isTk2   ,"_isTk2/b");
  ExTree->Branch("IsGlbMu_Offline_2",&_isGlb2   ,"_isGlb2/b");
  ExTree->Branch("IsSAMu_Offline_2",&_isSA2   ,"_isSA2/b");
  ExTree->Branch("IsTMOMu_Offline_2",&_isTMO2   ,"_isTMO2/b");
  ExTree->Branch("IsTightMu_Offline_2",&_isTight2   ,"_isTight2/b");
  ExTree->Branch("IsPFMu_Offline_2",&_isPF2   ,"_isPF2/b");

  ExTree->Branch("nPixHits_Offline_2",&_npix2   ,"_npix2/I");
  ExTree->Branch("nTkHits_Offline_2",&_nTk2   ,"_nTk2/I");
  ExTree->Branch("nMuHits_Offline_2",&_nMu2   ,"_nMu2/I");
  ExTree->Branch("Q_Offline_2",&_q2   ,"_q2/I");

  ExTree->Branch("chiTk_Offline_2",&_chiTk2   ,"_chiTk2/D");
  ExTree->Branch("chiMu_Offline_2",&_chiMu2   ,"_chiMu2/D");
 //
 //third offline mu-track   
  ExTree->Branch("IsTkMu_Offline_3",&_isTk3   ,"_isTk3/b");
  ExTree->Branch("IsGlbMu_Offline_3",&_isGlb3   ,"_isGlb3/b");
  ExTree->Branch("IsSAMu_Offline_3",&_isSA3   ,"_isSA3/b");
  ExTree->Branch("IsTMOMu_Offline_3",&_isTMO3   ,"_isTMO3/b");
  ExTree->Branch("IsTightMu_Offline_3",&_isTight3   ,"_isTight3/b");
  ExTree->Branch("IsPFMu_Offline_3",&_isPF3   ,"_isPF3/b");

  ExTree->Branch("nPixHits_Offline_3",&_npix3   ,"_npix3/I");
  ExTree->Branch("nTkHits_Offline_3",&_nTk3   ,"_nTk3/I");
  ExTree->Branch("nMuHits_Offline_3",&_nMu3   ,"_nMu3/I");
  ExTree->Branch("Q_Offline_3",&_q3   ,"_q3/I");

  ExTree->Branch("chiTk_Offline_3",&_chiTk3   ,"_chiTk3/D");
  ExTree->Branch("chiMu_Offline_3",&_chiMu3   ,"_chiMu3/D");
 //
 //Offline vertices

  ExTree->Branch("isValidSV_Offline",&_svValid,"_svValid/b"); 
  ExTree->Branch("isValidSVT_Offline",&_svtValid,"_svtValid/b"); 
  ExTree->Branch("isPVLeading_Offline",&_isPVLeading,"_isPVLeading/b");

  ExTree->Branch("PV_Offline","TVector3",&_PV); 
  ExTree->Branch("SV_Offline","TVector3",&_SV);
  ExTree->Branch("SVT_Offline","TVector3",&_SVT);

  ExTree->Branch("PVerr_Offline","TVector3",&_PVe); 
  ExTree->Branch("SVerr_Offline","TVector3",&_SVe);
  ExTree->Branch("SVTerr_Offline","TVector3",&_SVTe);
  
  ExTree->Branch("SVchi_Offline",&_SVchi   ,"_SVchi/D"); 
  ExTree->Branch("SVprob_Offline",&_SVprob   ,"_SVprob/D"); 
  ExTree->Branch("SVTchi_Offline",&_SVTchi   ,"_SVTchi/D"); 
  ExTree->Branch("SVTprob_Offline",&_SVTprob   ,"_SVTprob/D"); 

  ExTree->Branch("Lxy_Offline",&_Lxy   ,"_Lxy/D");
  ExTree->Branch("LxySig_Offline",&_LxySig   ,"_LxySig/D");
  ExTree->Branch("LxyT_Offline",&_LxyT   ,"_LxyT/D");
  ExTree->Branch("LxyTSig_Offline",&_LxyTSig   ,"_LxyTSig/D");

  ExTree->Branch("CosPoint2_Offline",&_cosp2   ,"_cosp2/D");
  ExTree->Branch("CosPoint3_Offline",&_cosp3   ,"_cosp3/D");
  //
  htotEff=new TH1F("TotEff","Tot Eff",4,-0.5,3.5);
  hDiMuEff=new TH1F("DiMuEff","DiMuEff",10,-0.5,9.5);
  hTrackEff=new TH1F("TrackEff","TrackEff",10,-0.5,9.5);
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
  sprintf(title,"Tot= %i  Passed= %i",Total,OfflineTrig);
  htotEff->SetTitle(title);

  htotEff->SetBinContent(1,Total);
  htotEff->GetXaxis()->SetBinLabel(1,"tot");

  htotEff->SetBinContent(2, Triggered);
  htotEff->GetXaxis()->SetBinLabel(2,"Trigger");

  htotEff->SetBinContent(3, FoundDiMuTrig);
  htotEff->GetXaxis()->SetBinLabel(3,"DiMu Found");

  htotEff->SetBinContent(4, OfflineTrig);
  htotEff->GetXaxis()->SetBinLabel(4,"Track Found");

  //Mu Eff
  sprintf(title,"Tot diMu Searches= %i  events with diMu= %i",ndm, FoundDiMuTrig);
  hDiMuEff->SetTitle(title);
  
  hDiMuEff->SetBinContent(1,ndm);
  hDiMuEff->GetXaxis()->SetBinLabel(1,"tot");
  
  hDiMuEff->SetBinContent(2,ndmq);
  hDiMuEff->GetXaxis()->SetBinLabel(2,"IsTkMu");

  hDiMuEff->SetBinContent(3,ndmm);
  sprintf(title,"InvMassIn(%5.2f,%5.2f)",diMuMassMin, diMuMassMax);
  hDiMuEff->GetXaxis()->SetBinLabel(3,title);
  
  hDiMuEff->SetBinContent(4,ndmv);
  hDiMuEff->GetXaxis()->SetBinLabel(4,"Vertex Ok");
  
  hDiMuEff->SetBinContent(5,ndmvprob);
  sprintf(title,"Vprob > %5.2f ", diMuVprobMin);
  hDiMuEff->GetXaxis()->SetBinLabel(5,title);
  
  hDiMuEff->SetBinContent(6,ndmchi);
  sprintf(title,"chi2Vtx < %5.2f",diMuVtxChi2Max);
  hDiMuEff->GetXaxis()->SetBinLabel(6,title);
  
  hDiMuEff->SetBinContent(7,ndmcos);
  sprintf(title,"CosPointing < %5.2f",diMuCosPointMin);
  hDiMuEff->GetXaxis()->SetBinLabel(7,title);

  hDiMuEff->SetBinContent(8,ndmlxy);
  sprintf(title,"Lxy > %5.2f",diMuLxyMin);
  hDiMuEff->GetXaxis()->SetBinLabel(8,title);

  hDiMuEff->SetBinContent(9,ndmlxys);
  sprintf(title,"LxySig > %5.2f",diMuLxySigMin);
  hDiMuEff->GetXaxis()->SetBinLabel(9,title);
  
  hDiMuEff->SetBinContent(10,FoundDiMuTrig);
  hDiMuEff->GetXaxis()->SetBinLabel(10,"Selected");
  
  //Tracks eff
  sprintf(title,"Tot Track Searches= %i  events passed= %i",FoundDiMuTrig,OfflineTrig);
  
  hTrackEff->SetTitle(title); 
  hTrackEff->SetBinContent(1,nt);
  hTrackEff->GetXaxis()->SetBinLabel(1,"tot");
  
  hTrackEff->SetBinContent(2,ntq);
  hTrackEff->GetXaxis()->SetBinLabel(2,"Quality Ok");
  
  hTrackEff->SetBinContent(3,ntm);
  sprintf(title,"InvMassIn(%5.2f,%5.2f)",diMuTrackMassMin,diMuTrackMassMax);
  hTrackEff->GetXaxis()->SetBinLabel(3,title);
  
  hTrackEff->SetBinContent(4,ntv);
  hTrackEff->GetXaxis()->SetBinLabel(4,"Vertex Ok");
    
  hTrackEff->SetBinContent(5,ntvprob);
  sprintf(title,"Vprob > %5.2f ", diMuTrackVprobMin);
  hTrackEff->GetXaxis()->SetBinLabel(5,title);
  
  hTrackEff->SetBinContent(6,ntchi);
  sprintf(title,"ch2Vtx < %5.2f",diMuTrackVtxChi2Max);
  hTrackEff->GetXaxis()->SetBinLabel(6,title);

  hTrackEff->SetBinContent(7,ntcos);
  sprintf(title,"CosPointing > %5.2f",diMuTrackCosPointMin);
  hTrackEff->GetXaxis()->SetBinLabel(7,title);    

  hTrackEff->SetBinContent(8,ntlxy);
  sprintf(title,"Lxy > %5.2f",diMuTrackLxyMin);
  hTrackEff->GetXaxis()->SetBinLabel(8,title);
    
  hTrackEff->SetBinContent(9,ntlxys);
  sprintf(title,"LxySig > %5.2f",diMuTrackLxySigMin);
  hTrackEff->GetXaxis()->SetBinLabel(9,title);
    
  hTrackEff->SetBinContent(10,OfflineTrig);
  hTrackEff->GetXaxis()->SetBinLabel(10,"Selected");
  
  thefile->cd();

  //some control histos
 
  htotEff->Write();
  hDiMuEff->Write();
  hTrackEff->Write();
 
  thefile->Write();

  delete htotEff;
  delete hDiMuEff;
  delete hTrackEff;

  if (IsMC && !isBkg){

    delete _SVTR;
    delete _SVR;
    delete _PVR;

    delete _SVTeR;
    delete _SVeR;
    delete _PVeR;
  
    delete _MuTrack_4MomR;
    delete _Mu2_4MomR;
    delete _Mu1_4MomR;
     
    delete _DiMuPlusTrack4MomR;
    delete _DiMu4MomR;

    delete _MuTrack_4MomG;
    delete _Mu2_4MomG;
    delete _Mu1_4MomG;
 
    delete _DiMuPlusTrack4MomG;
    delete _DiMu4MomG;

    delete _GenSV;
  }

  delete _SVT;
  delete _SV;
  delete _PV;

  delete _SVTe;
  delete _SVe;
  delete _PVe;

  delete _MuTrack_4Mom_Mu;
  delete _MuTrack_4Mom_Pi;
  delete _Mu2_4Mom;
  delete _Mu1_4Mom;
 
  delete _DiMuPlusTrack4Mom_Pi;
  delete _DiMuPlusTrack4Mom_Mu;
  delete _DiMu4Mom;

  delete ExTree;

  thefile->Close();
  delete thefile;
  
  std::cout << "Total " << Total << std::endl;
  std::cout << "Triggered " << Triggered << std::endl;
  std::cout << "DiMu Found " << FoundDiMu << std::endl;
  std::cout << "DiMu+Track Found " << Offline << std::endl;
  if (IsMC) std::cout << "Dropped Volunteers " << Nvolunteers << std::endl;
  if (IsMC) std::cout << "Events MC Matched " << GenMatches  << std::endl;
}

#include "FWCore/Framework/interface/MakerMacros.h"  
DEFINE_FWK_MODULE( Tau3MuAnalysis_V2 );
