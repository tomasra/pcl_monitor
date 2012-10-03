#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "RecoVertex/KalmanVertexFit/interface/SingleTrackVertexConstraint.h"

#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"
#include "DataFormats/HLTReco/interface/TriggerRefsCollections.h"
#include "DataFormats/HLTReco/interface/TriggerEventWithRefs.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidateFwd.h"

#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"

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
  virtual void vtx(const edm::Event&, const edm::EventSetup&, std::vector<TransientTrack>&, TVector3*, TVector3*, bool &, double &, double &, int);
  virtual pair<double,double> Compute_Lxy_and_Significance(Vertex &, TransientVertex &, TLorentzVector&);
  virtual void findBestDimuon(const edm::Event&, const edm::EventSetup&, MuonCollection&, MuonCollection&, TransientVertex&, Vertex&);
  virtual void findBestPiCand(const edm::Event&, const edm::EventSetup&, MuonCollection&, TransientVertex&, Vertex&, TransientVertex&,TLorentzVector&,Track&);
  virtual bool isTight(const reco::Muon*);
  virtual bool TriggerDecision(const edm::Event&);
  virtual bool getMu(const edm::Event&, Track&, Muon&);
  virtual int countTracksAround(const edm::Event&, const edm::EventSetup&, TLorentzVector*, double&, TransientVertex&, int);
  virtual pair<double,double> ComputeImpactParameterWrtPoint(TransientTrack& tt, Vertex&);
  virtual bool isMcMatched(const edm::Event&,TLorentzVector*,std::vector<TLorentzVector>&);
  virtual bool isBkgMatched(const edm::Event&,TLorentzVector*);
  virtual bool isInPV(Vertex&, TLorentzVector&);
  virtual void TrackCompatibility(const edm::EventSetup&,Vertex&, TransientVertex&, vector<TransientTrack>&, int&);
  virtual void ptAround(Vertex&, vector<TransientTrack>&, TLorentzVector&, double, double&);
  virtual double Compute_CosPointingAngle(Vertex& , TransientVertex& ,TLorentzVector&);
  virtual bool isClose(TransientTrack&, TransientVertex&);
  virtual bool isVtxErrorOk(TransientVertex&);
  virtual bool matchGenReco(const edm::Event&,std::vector<TLorentzVector>&,std::vector<std::pair<TLorentzVector,int> >&,std::vector<pair<const Track*,int> >&);
  virtual void findGenMoms(const edm::Event&, std::vector<TLorentzVector>&);
  virtual bool alreadyMatched(uint&,std::vector<int>);
  virtual bool isVolunteer(const edm::Event&);
  virtual void fillRecoMatchedInfo(const edm::Event&, const edm::EventSetup&, std::vector<pair<const Track*,int> >&);
  virtual void setMuIdToTrack(const edm::Event&, const Track*,bool&,bool&,bool&,bool&,bool&,bool&,int&,int&,int&,int&,double&,double&, bool&, double&);
  virtual void setMuIdToMu(Muon &,bool&,bool&,bool&,bool&,bool&,bool&,int&,int&,int&,int&,double&,double&);
  virtual void findTriggerObjects(const edm::Event&, const edm::EventSetup&, std::vector<TLorentzVector>&, int);
  virtual void vertexingTracks(const edm::Event&, const edm::EventSetup&, TransientVertex&, int&);
  virtual int  sharedSegmentsTkMu( const reco::Muon&, const reco::Muon&);

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
  bool _TriggerMatched, _DiMuFound, _TrackFound;

  std::vector<string> HLT_paths;
  std::string HLT_process;

  int _Run,_Evt,_Lum,_Nvtx, _Nmu, _Ntk, _NTrigMu,_NTrigTk;

  std::string _TrigName;

  //Gen Level variables
  TLorentzVector* _Mu1_4MomG,*_Mu2_4MomG,*_MuTrack_4MomG, *_DiMu4MomG, *_DiMuPlusTrack4MomG, *_Ds_4MomG;
  TVector3 *_GenSV;

  int _pdg1,_pdg2,_pdg3;
  int _Mpdg1,_Mpdg2,_Mpdg3;

  bool _isFSR; //is there final state radiation in the event?

  double _cosp2G,_cosp3G;

  //4Mom and Vertices for gen matched Reco objects
  TLorentzVector* _Mu1_4MomR,*_Mu2_4MomR,*_MuTrack_4MomR, *_DiMu4MomR, *_DiMuPlusTrack4MomR;

  TLorentzVector* _Mu1_4MomR_Refit,*_Mu2_4MomR_Refit,*_MuTrack_4MomR_Refit;

  TVector3 *_PVR,*_SVR,*_SVTR,*_PVeR,*_SVeR,*_SVTeR;

  TVector3 *_SV_Mu1TR, *_SVe_Mu1TR,*_SV_Mu2TR,*_SVe_Mu2TR;

  bool _svValidR,_svtValidR, _isPVLeadingR;

  bool _sv1tValidR, _sv2tValidR;

  double _SVchiR,_SVprobR, _SVTchiR,_SVTprobR,_SV1chiR,_SV1probR,_SV2chiR,_SV2probR;
  double _LxyR,_LxySigR,_LxyTR,_LxyTSigR;

  double _cosp2R,_cosp3R;

  int _Ntracks_Mu1_R,_Ntracks_Mu2_R;

  int _Ntracks_SVT_R, _Ntracks_SV1_R, _Ntracks_SV2_R;
  int _NtracksPV_SVT_R;

  double _Sum01R,_Sum03R,_Sum05R;

  double _DZ1R,_DZ2R,_DZ3R;

  //mu id variables for the gen matched Reco objects
  bool _isTkR1, _isGlbR1, _isSAR1, _isTMOR1, _isTightR1, _isPFR1;
  int _npixR1, _nTkR1, _nMuR1, _qR1;
  double _chiTkR1, _chiMuR1,_chiTkR1_Refit;

  bool _isTkR2, _isGlbR2, _isSAR2, _isTMOR2, _isTightR2, _isPFR2;
  int _npixR2, _nTkR2, _nMuR2, _qR2;
  double _chiTkR2, _chiMuR2,_chiTkR2_Refit;

  bool _isTkR3, _isGlbR3, _isSAR3, _isTMOR3, _isTightR3, _isPFR3;
  int _npixR3, _nTkR3, _nMuR3, _qR3;
  double _chiTkR3, _chiMuR3,_chiTkR3_Refit;

  double _DCA_SVR;

  double _3D_IP_SVR,_3D_IPSig_SVR ;
  double _3D_IP_PVR,_3D_IPSig_PVR ;

  //

  //Offline Reco variables
  TLorentzVector* _Mu1_4Mom,*_Mu2_4Mom,*_MuTrack_4Mom_Mu,*_MuTrack_4Mom_Pi, *_DiMu4Mom, *_DiMuPlusTrack4Mom_Mu,*_DiMuPlusTrack4Mom_Pi; //4mom both for the pi and mu track guess
  TLorentzVector* _Mu1_4Mom_Refit,*_Mu2_4Mom_Refit,*_MuTrack_4Mom_Mu_Refit,*_MuTrack_4Mom_Pi_Refit;

  TVector3 *_PV,*_SV,*_SVT,*_PVe,*_SVe,*_SVTe;

  TVector3 *_SV_Mu1T, *_SVe_Mu1T,*_SV_Mu2T,*_SVe_Mu2T;

  bool _sv1tValid, _sv2tValid;

  double _SVchi,_SVprob, _SVTchi,_SVTprob,_SV1chi,_SV1prob,_SV2chi,_SV2prob;
  double _Lxy,_LxySig,_LxyT,_LxyTSig;

  bool _svValid,_svtValid, _isPVLeading;

  double _cosp2,_cosp3;

  int _Ntracks_Mu1,_Ntracks_Mu2;
  int _Ntracks_SVT, _Ntracks_SV1, _Ntracks_SV2;
  int _NtracksPV_SVT;

  double _Sum01,_Sum03,_Sum05;
  double _DZ1,_DZ2,_DZ3;


  //mu id variables for the Offline objects
  bool _isTk1, _isGlb1, _isSA1, _isTMO1, _isTight1, _isPF1;
  int _npix1, _nTk1, _nMu1, _q1;
  double _chiTk1, _chiMu1,_chiTk1_Refit;
  double _kink1,_kink2, _kink3;

  bool _isTk2, _isGlb2, _isSA2, _isTMO2, _isTight2, _isPF2;
  int _npix2, _nTk2, _nMu2, _q2;
  double _chiTk2, _chiMu2,_chiTk2_Refit;

  bool _isTk3, _isGlb3, _isSA3, _isTMO3, _isTight3, _isPF3;
  int _npix3, _nTk3, _nMu3, _q3;
  double _chiTk3, _chiMu3,_chiTk3_Refit;
  double _DCA_SV;

  double _3D_IP_SV,_3D_IPSig_SV ;
  double _3D_IP_PV,_3D_IPSig_PV ;

  //
 
  bool _IsMcMatched;
 
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


void  Tau3MuAnalysis_V2::findTriggerObjects(const edm::Event& iEvent, const edm::EventSetup& iSetup, std::vector<TLorentzVector> &triggeredObjects, int pdgId ){
 
  using namespace std;
  using namespace edm;
  using namespace reco;
  using namespace trigger;

  if (HLT_process=="HLT"){
    edm::Handle<edm::TriggerResults>   triggerResultsHandle_;
    edm::Handle<trigger::TriggerEvent> triggerEventHandle_;

    iEvent.getByLabel(InputTag("TriggerResults","",HLT_process),triggerResultsHandle_);
    if (!triggerResultsHandle_.isValid()) {
      cout << "Error in getting TriggerResults product from Event!" << endl;
      return;
    }

    iEvent.getByLabel(InputTag("hltTriggerSummaryAOD","",HLT_process),triggerEventHandle_);
    if (!triggerEventHandle_.isValid()) {
      cout << "Error in getting TriggerEvent product from Event!" << endl;
      return;
    }

    const unsigned int filterIndex(triggerEventHandle_->filterIndex(InputTag("hltTau3MuMuMuTkFilter","",HLT_process)));
    if (debug) cout << "trigger index " << filterIndex << " size filters " << triggerEventHandle_->sizeFilters() << endl;
    if (filterIndex < triggerEventHandle_->sizeFilters()) {
      const Vids& VIDS (triggerEventHandle_->filterIds(filterIndex));
      const Keys& KEYS(triggerEventHandle_->filterKeys(filterIndex));
      const size_type nI(VIDS.size());
      const size_type nK(KEYS.size());
      size_type n;
      if (nI>nK) n=nI;
      else n=nK;
      const TriggerObjectCollection& TOC(triggerEventHandle_->getObjects());
      if (debug) cout << "Objects that fired the Trigger:" << endl;
      for (size_type i=0; i!=n; ++i) {
	const TriggerObject& TO(TOC[KEYS[i]]);
	if (abs(TO.id())==pdgId){
	  TLorentzVector tmu=TLorentzVector(0.,0.,0.,0.);
	  if (pdgId==13) tmu.SetPtEtaPhiM(TO.pt(),TO.eta(),TO.phi(),0.1057);
	  if (pdgId==211) tmu.SetPtEtaPhiM(TO.pt(),TO.eta(),TO.phi(),0.1396);
	  triggeredObjects.push_back(tmu);
	  if (debug) cout << "   " << i << " " << VIDS[i] << "/" << KEYS[i] << ": "
			  << TO.id() << " " << TO.pt() << " " << TO.eta() << " " << TO.phi() << " " << TO.mass() << " "  << " " << TO.energy() 
			  << endl;
	}
      }
    }
  
    else
      {
	if (debug) cout << "Module index out of HLT modules index range ... i.e this event doesn't pass the trigger" << endl;
	return;
      }
  }

  if (HLT_process=="HLTX"){

    edm::Handle<trigger::TriggerFilterObjectWithRefs> dimuAndTrackVtxCands;

    iEvent.getByLabel(edm::InputTag("hltTau3MuMuMuTkFilter::HLTX"),dimuAndTrackVtxCands);

    if (dimuAndTrackVtxCands.isValid()){

      if (pdgId==13){
	std::vector<RecoChargedCandidateRef> muons;
	dimuAndTrackVtxCands->getObjects(trigger::TriggerMuon, muons);
	int ms=muons.size();
	if (ms<2) cout << "WARNING: triggered event with less than 2 muons!!!" << endl;
	TLorentzVector mom;
	for(int n = 0; n != ms; ++n) {
	  mom.SetPtEtaPhiM(muons[n]->pt(), muons[n]->eta(), muons[n]->phi(),0.1057);
	  triggeredObjects.push_back(mom);
	}
      }

      if (pdgId==211){
	std::vector<RecoChargedCandidateRef> tracks;
	dimuAndTrackVtxCands->getObjects(trigger::TriggerTrack, tracks);
	int ts=tracks.size();
	if (ts<1) cout << "WARNING: triggered event with less than 1 track!!!" << endl;
	TLorentzVector mom;
	for(int n = 0; n != ts; ++n) {
	  mom.SetPtEtaPhiM(tracks[n]->pt(), tracks[n]->eta(), tracks[n]->phi(),0.1396);
	  triggeredObjects.push_back(mom);
	}
      }
    }
  }
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

  KalmanVertexFitter avf(true);

  double tmpProb=diMuTrackVprobMin;
  double Vp0=diMuTrackVprobMin;

  if (triggered) nt++;

  std::vector<TLorentzVector> triggerTracks;
  findTriggerObjects(ev,iSetup,triggerTracks,211);
  _NTrigTk=triggerTracks.size();

  TLorentzVector m1=TLorentzVector(dimu[0].px(),dimu[0].py(),dimu[0].pz(),dimu[0].energy());
  TLorentzVector m2=TLorentzVector(dimu[1].px(),dimu[1].py(),dimu[1].pz(),dimu[1].energy());  


  int tcounter=0;
  for(TrackCollection::const_iterator it = tracks->begin();it != tracks->end(); ++it){
    tcounter++;

    if ((it->pt()==dimu[0].innerTrack()->pt() && it->eta()==dimu[0].innerTrack()->eta()) || (it->pt()==dimu[1].innerTrack()->pt() && it->eta()==dimu[1].innerTrack()->eta())) continue;
    if (dimu[0].charge()==dimu[1].charge() && it->charge()==dimu[0].charge()) continue; //impossible to have a particle with charge +/- 3

    bool goodTrack=false;

    if (it->quality(TrackBase::highPurity) && it->pt()> MinTrackPt) goodTrack=true;

    if (!goodTrack) continue;

    TLorentzVector p=TLorentzVector(it->px(),it->py(),it->pz(),sqrt(TrackMass*TrackMass+it->p()*it->p()));
    if (p.DeltaR(m1)<0.005 || p.DeltaR(m2) < 0.005) continue; // to avoid split tracks

    if(passq && triggered) {ntq++;passq=false;}

    TLorentzVector tot=m1+m2+p;

    double dRtrack=0.05;
    bool isTriggerTrack=false;

    for (uint s=0; s<triggerTracks.size(); s++){
      if (triggerTracks[s].DeltaR(p) < dRtrack){
	isTriggerTrack=true;
	dRtrack=triggerTracks[s].DeltaR(p);
      }
    }

    if (!isTriggerTrack) continue;

    if (debug) cout << "distance reco-track trigger-track= " << dRtrack << endl;

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

  Muon muTk;
  bool isMu=getMu(ev,track,muTk);
  bool shares=false;

  if (isMu) {

    int shared1=sharedSegmentsTkMu(muTk,dimu[0]);
    int shared2=sharedSegmentsTkMu(muTk,dimu[1]);
    int seg=0;

    //count the segments associated to the track
    for(std::vector<reco::MuonChamberMatch>::const_iterator chamberMatch = muTk.matches().begin();
	chamberMatch != muTk.matches().end(); ++chamberMatch) {
      for(std::vector<reco::MuonSegmentMatch>::const_iterator segmentMatch = chamberMatch->segmentMatches.begin(); 
	  segmentMatch != chamberMatch->segmentMatches.end(); ++segmentMatch) {
	if (!segmentMatch->isMask(reco::MuonSegmentMatch::BestInChamberByDR)) continue;
	seg++;
      }
    }

    if (debug) cout << "Shared segments with mu1 " << shared1 << " mu2 " << shared2  << " tot seg matched to track " << seg << endl;

    if (double(shared1)/double(seg) >= 0.5 || double(shared2)/double(seg) >= 0.5) shares=true; 
  }

  if (debug && shares) cout << "No Mu id will be given to the track" << endl;

  if (trackFound) setMuIdToTrack(ev, &track, _isTk3,_isSA3,_isGlb3 ,_isTMO3, _isPF3, _isTight3, _npix3,_nTk3,_nMu3,_q3, _chiTk3,_chiMu3, shares, _kink3);
  if (_kink3==999) _kink3=-1;
  
}

int Tau3MuAnalysis_V2::sharedSegmentsTkMu( const reco::Muon& mu, const reco::Muon& mu2) {
    int ret = 0;
    if (debug) cout << "cecking shared segments between track and muon" << endl;

    // Will do with a stupid double loop, since creating and filling a map is probably _more_ inefficient for a single lookup.
    for(std::vector<reco::MuonChamberMatch>::const_iterator chamberMatch = mu.matches().begin();
        chamberMatch != mu.matches().end(); ++chamberMatch) {
        if (chamberMatch->segmentMatches.empty()) continue;
        for(std::vector<reco::MuonChamberMatch>::const_iterator chamberMatch2 = mu2.matches().begin();
            chamberMatch2 != mu2.matches().end(); ++chamberMatch2) {
            if (chamberMatch2->segmentMatches.empty()) continue;
            if (chamberMatch2->id() != chamberMatch->id()) continue;
            for(std::vector<reco::MuonSegmentMatch>::const_iterator segmentMatch = chamberMatch->segmentMatches.begin(); 
                segmentMatch != chamberMatch->segmentMatches.end(); ++segmentMatch) {
	      if (!segmentMatch->isMask(reco::MuonSegmentMatch::BestInChamberByDR)) continue;
                for(std::vector<reco::MuonSegmentMatch>::const_iterator segmentMatch2 = chamberMatch2->segmentMatches.begin(); 
                    segmentMatch2 != chamberMatch2->segmentMatches.end(); ++segmentMatch2) {
		  if (!segmentMatch2->isMask(reco::MuonSegmentMatch::BestInChamberByDR)) continue;
                    if ((segmentMatch->cscSegmentRef.isNonnull() && segmentMatch->cscSegmentRef == segmentMatch2->cscSegmentRef) ||
                        (segmentMatch-> dtSegmentRef.isNonnull() && segmentMatch-> dtSegmentRef == segmentMatch2-> dtSegmentRef) ) {
                        ++ret;
                    } // is the same
                } // segment of mu2 in chamber
            } // segment of mu1 in chamber
        } // chamber of mu2
    } // chamber of mu1
  
    return ret; 
}

void Tau3MuAnalysis_V2::ptAround(Vertex& pv, vector<TransientTrack>& vtt, TLorentzVector& trimu, double dR, double& sumPt){

  sumPt=0;

  for(std::vector<reco::TrackBaseRef>::const_iterator it = pv.tracks_begin() ; it != pv.tracks_end(); ++it ){

    Track tr=*(it->get());

    if (tr.pt()==vtt[0].track().pt() || tr.pt()==vtt[1].track().pt() || tr.pt()==vtt[2].track().pt()) continue;

    TLorentzVector trv=TLorentzVector(tr.px(),tr.py(),tr.pz(),sqrt(TrackMass*TrackMass+tr.p()*tr.p()));
    if (trv.DeltaR(trimu) < dR) sumPt += tr.pt();
  }
}

void Tau3MuAnalysis_V2::TrackCompatibility(const edm::EventSetup& iSetup, Vertex & pv, TransientVertex& sv, vector<TransientTrack>& vtt, int& ncomp){

  ncomp=0;

  edm::ESHandle<TransientTrackBuilder> Builder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", Builder);

  for(std::vector<reco::TrackBaseRef>::const_iterator it = pv.tracks_begin() ; it != pv.tracks_end(); ++it ){

    Track tr=*(it->get());

    if (tr.pt()==vtt[0].track().pt() || tr.pt()==vtt[1].track().pt() || tr.pt()==vtt[2].track().pt()) continue;

    TransientTrack tt=Builder->build(tr);
    std::pair<bool,Measurement1D> ipv = IPTools::absoluteImpactParameter3D(tt,pv);
    std::pair<bool,Measurement1D> isv = IPTools::absoluteImpactParameter3D(tt,sv);

    if (ipv.first && isv.first){
      if (isv.second.value() < ipv.second.value()) ncomp++;
    }
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

bool Tau3MuAnalysis_V2::isVolunteer(const edm::Event& ev){
 
  if (isBkg) return false;

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

  TVector3 Dsvtx;

  if (isSignal){
    for(genPart=genParticleCollection->begin(); genPart!=genParticleCollection->end(); genPart++) {
      const reco::Candidate & cand = *genPart;

      if (abs(cand.pdgId())!=15) continue;
      if (abs(cand.mother()->pdgId())!=431) continue;

      if (debug) cout << "Mom Id " << cand.pdgId() << endl;

      int ndau=cand.numberOfDaughters();

      if (ndau<3) continue;
      if (debug) cout << "n tau daugthers:" << ndau << endl;
      for(int k = 0; k < ndau; ++ k) {
	TLorentzVector gen4mom;
	const Candidate * d = cand.daughter( k );
	int dauId = d->pdgId();

	if (debug) cout << "id " << dauId << endl;

	if (abs(dauId)==22) _isFSR=true;

	if (abs(dauId)==13) {
	  nmu++; 
	  if (nmu==3){//fill vertices only when we know this is the right event
	    _GenSV->SetXYZ(d->vx(),d->vy(),d->vz());
	    Dsvtx.SetXYZ(cand.mother()->vx(),cand.mother()->vy(),cand.mother()->vz());
	    _Ds_4MomG->SetPxPyPzE(cand.mother()->px(),cand.mother()->py(),cand.mother()->pz(),cand.mother()->energy());
	  }
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
	
	if (abs(dauId)==22)_isFSR=true;
	if (abs(dauId)!=333 && abs(dauId)!=211 ) continue;

	if (dauId==333){
	  if (debug) cout << "Phi found!" << endl;
	  int ndauphi=d->numberOfDaughters();
	  int nmu=0;
	  for(int k1 = 0; k1 < ndauphi; ++ k1) {
	    const Candidate * d1 = d->daughter( k1 );
	    int dauphiId = d1->pdgId();

	    if (abs(dauphiId)==22)_isFSR=true;

	    if (abs(dauphiId)==13) {
	      nmu++; 
	      if (nmu==2){
		_GenSV->SetXYZ(d->vx(),d->vy(),d->vz());
		Dsvtx.SetXYZ(cand.vx(),cand.vy(),cand.vz());
		_Ds_4MomG->SetPxPyPzE(cand.px(),cand.py(),cand.pz(),cand.energy());
	      }
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
    cout << " event " << ev.id().event() << " run " << ev.id().run() << " lumi " << ev.id().luminosityBlock() << " has not the needed gen content " << endl;
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


  TVector3 Displacement=TVector3(_GenSV->X()-Dsvtx.X(),_GenSV->Y()-Dsvtx.Y(),0.);

  _cosp2G=(Displacement.X()*dimu.Px()+Displacement.Y()*dimu.Py())/(dimu.Mag()*Displacement.Mag());
  _cosp3G=(Displacement.X()*trimu.Px()+Displacement.Y()*trimu.Py())/(trimu.Mag()*Displacement.Mag());

  if (debug) cout << "Gen object mass " << trimu.M() << endl;

}

bool Tau3MuAnalysis_V2::isMcMatched(const edm::Event& ev,TLorentzVector* recov,std::vector<TLorentzVector>& TheGenMus){

  if (debug) cout << "Offline-Gen Matching ...." << endl;

  bool ThreeMatches=false;

  if (TheGenMus.size()!=3) return false;

  //see if they match reco muons
  bool RunMatch=true;

  std::vector<int> recoIndexes;
  std::vector<int> genIndexes;

  if (debug) cout << "Matching to reco objects" << endl;

  while (RunMatch){

    double dRtmp=0.005;

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

    if (dRtmp==0.005) RunMatch=false;

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


bool Tau3MuAnalysis_V2::getMu(const edm::Event& ev,Track& p, Muon& mutk){

  bool ItIs=false;
  edm::Handle<MuonCollection> muons;
  ev.getByLabel("muons",muons);

  for (MuonCollection::const_iterator recoMu = muons->begin(); recoMu!=muons->end(); ++recoMu){

    if(!recoMu->isTrackerMuon()) continue;

    reco::TrackRef inp = recoMu->innerTrack();
    if (inp.isNonnull() && inp.isAvailable()){
      if (inp->pt()==p.pt() && inp->eta()==p.eta()) {
	ItIs=true;
	mutk=Muon(*recoMu);	 
      }	
    }
  }

  return ItIs;  
}

void Tau3MuAnalysis_V2::vertexingTracks(const edm::Event& ev, const edm::EventSetup& iSetup, TransientVertex& vtx, int& ntracks){
 
  std::vector<TransientTrack> vtt=vtx.originalTracks();
  int originalSize= vtt.size();

  double ex=vtx.positionError().cxx();
  double ey=vtx.positionError().cyy();
  double ez=vtx.positionError().czz();
  double chi2=vtx.normalisedChiSquared();

  edm::ESHandle<TransientTrackBuilder> Builder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", Builder);

  Handle<TrackCollection> tracks;
  ev.getByLabel("generalTracks", tracks);

  KalmanVertexFitter avf;

  for(TrackCollection::const_iterator it = tracks->begin();it != tracks->end(); ++it){

    if (!(it->quality(TrackBase::highPurity) && it->pt()> MinTrackPt)) continue;
    if (it->dz(Vertex(vtx).position())>0.1) continue;

    bool isIn=false;

    for (uint k=0; k< vtt.size(); ++k){
      if (vtt[k].track().pt()==it->pt() && vtt[k].track().phi()==it->phi()) isIn=true;     
    }

    if (isIn) continue;
    
    std::vector<TransientTrack> vtmp;
    
    for (uint k=0; k< vtt.size(); ++k){
      vtmp.push_back(vtt[k]);
    }

    TransientTrack t=Builder->build(*it);
    vtmp.push_back(t);

    TransientVertex tmpVtx=avf.vertex(vtmp);

    if (!tmpVtx.isValid()) continue;

    double chi=tmpVtx.normalisedChiSquared();
    if (chi==0) continue;

    if (fabs(tmpVtx.position().x()-vtx.position().x()) > 1.5*ex || fabs(tmpVtx.position().y()-vtx.position().y()) > 1.5*ey || fabs(tmpVtx.position().z()-vtx.position().z()) > 1.5*ez) continue;
    if (chi > chi2) continue; //control if the new vertex is better than the old one

    vtt.push_back(t);
  }

  int finalSize=vtt.size();
  ntracks=finalSize-originalSize;

}

int Tau3MuAnalysis_V2::countTracksAround(const edm::Event& ev, const edm::EventSetup& iSetup,TLorentzVector* vec, double& dR, TransientVertex& sv, int oneORtwo ){

  if (debug) cout << "counting tracks around mu" << oneORtwo << endl;

  int N=0;
  Handle<TrackCollection> tracks;
  ev.getByLabel("generalTracks", tracks);
  TLorentzVector Mom= vec[oneORtwo];
  Vertex Vtx=Vertex(sv);

  for(TrackCollection::const_iterator it = tracks->begin();it != tracks->end(); ++it){
    bool isIn=false;
     
    double dz=it->dz(Vtx.position());

    if (dz > 0.1) continue; //The track is not close to SV

    TLorentzVector tvec=TLorentzVector(it->px(),it->py(),it->pz(),sqrt(TrackMass*TrackMass+it->p()*it->p()));
    for (int k=0; k<3; k++){
      if (tvec.DeltaR(vec[k]) < 1.e-4) isIn=true;
    }

    if (isIn) continue;
    if (Mom.DeltaR(tvec) < dR) N++;
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

    if (!muIn[i].isTrackerMuon()) continue;

    reco::TrackRef inone = muIn[i].innerTrack();

    if (!(inone.isNonnull() && inone.isAvailable())) continue;

    for (uint j=i+1; j<muIn.size(); ++j){

      if (!muIn[j].isTrackerMuon()) continue;

      reco::TrackRef intwo = muIn[j].innerTrack();

      if (!(intwo.isNonnull() && intwo.isAvailable())) continue;

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

void Tau3MuAnalysis_V2::vtx(const edm::Event& event, const edm::EventSetup& iSetup, std::vector<TransientTrack>& tt, TVector3* p, TVector3* ep, bool & valid, double & chi2, double & prob, int muNumber){

  if (debug) cout << "finding the single mu + track vertex" << endl;

  KalmanVertexFitter avf;
  TransientVertex tv=avf.vertex(tt);

  if (tv.isValid()){

    if (muNumber==1) vertexingTracks(event,iSetup, tv, _Ntracks_SV1);
    if (muNumber==2) vertexingTracks(event,iSetup, tv, _Ntracks_SV2);

    valid=true;

    p->SetXYZ(tv.position().x(),tv.position().y(),tv.position().z());
    ep->SetXYZ(tv.positionError().cxx(),tv.positionError().cyy(),tv.positionError().czz());
    double vChi2 = tv.totalChiSquared();
    double vNDF  = tv.degreesOfFreedom();
    chi2=vChi2/vNDF;
    prob= TMath::Prob(vChi2,(int)vNDF);

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
	  _TrigName=string(trigName);
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

  _Run=ev.id().run();
  _Evt=ev.id().event();
  _Lum=ev.id().luminosityBlock();

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

    if (TheGenMus.size()!=3) return;    

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

  if (!triggered) { if (debug) cout << "The event fail trigger selection and will be rejected" << endl; return;}

  if (debug) cout << "Starting offline selection" << endl;

  //Reconstruction on data
  string theMuonLabel = "muons";
    
  // get the muon container
  edm::Handle<MuonCollection> muons;
  ev.getByLabel(theMuonLabel,muons);
   
  reco::Vertex primaryVertex;

  /* edm::Handle<BeamSpot> beamSpot;
  ev.getByLabel(InputTag("OfflineBeamSpot"),beamSpot) ;

  cout << beamSpot->x0() << endl;
  */

  edm::ESHandle<TransientTrackBuilder> trackBuilder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder); 
    
  MuonCollection muSkim; // to be used to find the best dimuon
  nmuons=0;
   
  std::vector<TLorentzVector> triggerMuons;

  // check the validity of the collection
  if(muons.isValid()){

    findTriggerObjects(ev,iSetup,triggerMuons,13);
    _NTrigMu=triggerMuons.size();

     for (MuonCollection::const_iterator recoMu = muons->begin(); recoMu!=muons->end(); ++recoMu){ // loop over all muons to search those matched with the trigger objects
	
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
      
      if (pt < MinMuPt) {
	if (debug) cout << " pt of muon is " << pt << " < min pt = " << MinMuPt << " rejecting muon " <<  endl;  
	continue;
      }

      bool isTriggerMatched=false;
      std::vector<int> indexes;

      for (uint s=0; s<triggerMuons.size(); s++){

	if (alreadyMatched(s,indexes)) continue; // to avoid multiple matches with the same trigger muon

	if (triggerMuons[s].DeltaR(mom) < 0.02) {
	  isTriggerMatched=true;
	  indexes.push_back(s);
	  if (debug) cout << "Dr offlineMu-L3Mu " << mom.DeltaR(triggerMuons[s]) << endl;
	  if (debug) cout << "pt offline " << pt << " pt L3 " << triggerMuons[s].Pt() << endl;
	}
      }

      if (!isTriggerMatched) continue;     
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
  
  _TriggerMatched=true;  

  findBestDimuon(ev,iSetup, muSkim, BestDiMu, tv, primaryVertex);
  
  if (debug) cout << " number of selected muons " << BestDiMu.size() << endl;

  if (BestDiMu.size()!=2) return; //only for control

  _DiMuFound=true;

   FoundDiMu++;
   if (triggered) FoundDiMuTrig++;

  _svValid=true;

  if (debug) cout << "DiMuon candidate found:" << endl;
  if (debug) cout << "Mu1 -- eta: " << BestDiMu[0].innerTrack()->eta() << " phi: " << BestDiMu[0].innerTrack()->phi() << " pt: " << BestDiMu[0].innerTrack()->pt() << " q: " << BestDiMu[0].innerTrack()->charge() << endl; 
  if (debug) cout << "Mu2 -- eta: "  << BestDiMu[1].innerTrack()->eta() << " phi: " << BestDiMu[1].innerTrack()->phi() << " pt: " << BestDiMu[1].innerTrack()->pt() << " q: " << BestDiMu[1].innerTrack()->charge() << endl;

  setMuIdToMu(BestDiMu[0], _isTk1,_isSA1,_isGlb1 ,_isTMO1, _isPF1, _isTight1, _npix1,_nTk1,_nMu1,_q1, _chiTk1,_chiMu1);
  setMuIdToMu(BestDiMu[1], _isTk2,_isSA2,_isGlb2 ,_isTMO2, _isPF2, _isTight2, _npix2,_nTk2,_nMu2,_q2, _chiTk2,_chiMu2);

  _kink1=BestDiMu[0].combinedQuality().trkKink;
  _kink2=BestDiMu[1].combinedQuality().trkKink;

  if (_kink1==999) _kink1=-1;
  if (_kink2==999) _kink2=-1;

  if (debug) cout << "kink1 " << _kink1 << " kink2 " << _kink2 << endl;

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

    _TrackFound=true;

    vertexingTracks(ev,iSetup, tv3, _Ntracks_SVT);

    if (tv3.hasRefittedTracks()){
      std::vector<TransientTrack> vtt= tv3.refittedTracks();
     
      if (vtt.size()==3){

	_Mu1_4Mom_Refit->SetPtEtaPhiM(vtt[0].track().pt(),vtt[0].track().eta(),vtt[0].track().phi(),0.1057);
	_Mu2_4Mom_Refit->SetPtEtaPhiM(vtt[1].track().pt(),vtt[1].track().eta(),vtt[1].track().phi(),0.1057);
	_MuTrack_4Mom_Mu_Refit->SetPtEtaPhiM(vtt[2].track().pt(),vtt[2].track().eta(),vtt[2].track().phi(),0.1057);
	_MuTrack_4Mom_Pi_Refit->SetPtEtaPhiM(vtt[2].track().pt(),vtt[2].track().eta(),vtt[2].track().phi(),0.1396);

	_chiTk1_Refit=vtt[0].track().normalizedChi2();
	_chiTk2_Refit=vtt[1].track().normalizedChi2();
	_chiTk3_Refit=vtt[2].track().normalizedChi2();
      }
    }

    edm::ESHandle<TransientTrackBuilder> Builder;
    iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", Builder);

    TransientTrack mu1tt=Builder->build(BestDiMu[0].innerTrack());
    TransientTrack mu2tt=Builder->build(BestDiMu[1].innerTrack());
    TransientTrack pitt=Builder->build(thetrack);

    vector<TransientTrack> vtt13;
    vector<TransientTrack> vtt23;
    vector<TransientTrack> vtttot;

    vtttot.push_back(mu1tt);
    vtttot.push_back(mu2tt);
    vtttot.push_back(pitt);

    vtt13.push_back(mu1tt);
    vtt13.push_back(pitt);

    vtt23.push_back(mu2tt);
    vtt23.push_back(pitt);

    vtx(ev,iSetup,vtt13,_SV_Mu1T,_SVe_Mu1T,_sv1tValid,_SV1chi,_SV1prob,1); //fill the vertex of track with single muons
    vtx(ev,iSetup,vtt23,_SV_Mu2T,_SVe_Mu2T,_sv2tValid,_SV2chi,_SV2prob,2);

    Vertex muvtx=Vertex(tv);

    pair<double,double> d0sv=ComputeImpactParameterWrtPoint(pitt,muvtx);

    _DCA_SV=d0sv.first;

    std::pair<bool,Measurement1D> ipv = IPTools::absoluteImpactParameter3D(pitt,primaryVertex);
    std::pair<bool,Measurement1D> isv = IPTools::absoluteImpactParameter3D(pitt,muvtx);

    if (ipv.first){
      _3D_IP_PV=ipv.second.value();
      if (debug) cout << "3D IP wrt pv " << ipv.second.value() << endl;
      _3D_IPSig_PV=ipv.second.significance();
    }

    if (isv.first){
      _3D_IP_SV=isv.second.value();
      if (debug) cout << "3D IP wrt sv= " << isv.second.value() << endl;
      _3D_IPSig_SV=isv.second.significance();
    }

    TrackCompatibility(iSetup,primaryVertex,tv3,vtttot,_NtracksPV_SVT);

    _svtValid=true;

    _DZ1=BestDiMu[0].innerTrack()->dz(Vertex(tv3).position());
    _DZ2=BestDiMu[1].innerTrack()->dz(Vertex(tv3).position());
    _DZ3=thetrack.dz(Vertex(tv3).position());

    if(triggered) OfflineTrig++;

    if (debug) cout << "track found" << endl;
    if (debug) cout << "eta " << pitrack.Eta() << " phi " << pitrack.Phi() << " pT " << pitrack.Pt() << endl;

    pitrack_Mu.SetPtEtaPhiM(pitrack.Pt(),pitrack.Eta(),pitrack.Phi(),0.1057);
    pitrack_Pi.SetPtEtaPhiM(pitrack.Pt(),pitrack.Eta(),pitrack.Phi(),0.1396);

    DiMuTrackMom_Mu = DiMuMom+pitrack_Mu;
    DiMuTrackMom_Pi = DiMuMom+pitrack_Pi;

    ptAround(primaryVertex,vtttot,DiMuTrackMom_Mu, 0.1, _Sum01);
    ptAround(primaryVertex,vtttot,DiMuTrackMom_Mu, 0.3, _Sum03);
    ptAround(primaryVertex,vtttot,DiMuTrackMom_Mu, 0.5, _Sum05);

    if (debug) cout << " 3Mu Inv. Mass= " <<  DiMuTrackMom_Pi.M() << endl;

    TLorentzVector TotMomArray[3]={Mu1Mom, Mu2Mom, pitrack};

    double dRcount=0.2;

    _Ntracks_Mu1=countTracksAround(ev,iSetup,TotMomArray,dRcount,tv,1);
    _Ntracks_Mu2=countTracksAround(ev,iSetup,TotMomArray,dRcount,tv,2);

    bool isEventMatched=false;

    if (IsMC){
      if (!isBkg) isEventMatched=isMcMatched(ev,TotMomArray,TheGenMus);
      else isEventMatched=isBkgMatched(ev,TotMomArray);
      if (isEventMatched) GenMatches++;
    }
    
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
    Offline++;

    if (debug) cout << "Offline end, filling tree now ..." << endl;
  }
}

void Tau3MuAnalysis_V2::Initialize_TreeVars(){

  if (debug) cout << "Initializing vars for the TTree" << endl;

  triggered=false;

  _TriggerMatched=false;
  _DiMuFound=false;
  _TrackFound=false;

  for (int k=0; k<10; k++){
    _TrigBit[k]=false;
  }

  _Run=-1;
  _Lum=-1;
  _Evt=-1;

  _Nvtx=-1;
  _Nmu=-1;
  _Ntk=-1;

  _NTrigTk=-1;
  _NTrigMu=-1;

  if (IsMC){

    if (isBkg){
      _pdg1=-999;_pdg2=-999;_pdg3=-999;
      _Mpdg1=-999;_Mpdg2=-999;_Mpdg3=-999;
    }
    else{

      _Ds_4MomG->SetPtEtaPhiM(0.,0.,0.,0.);
      _DiMu4MomG->SetPtEtaPhiM(0.,0.,0.,0.);
      _DiMuPlusTrack4MomG->SetPtEtaPhiM(0.,0.,0.,0.);

      _Mu1_4MomG->SetPtEtaPhiM(0.,0.,0.,0.);
      _Mu2_4MomG->SetPtEtaPhiM(0.,0.,0.,0.);

      _MuTrack_4MomG->SetPtEtaPhiM(0.,0.,0.,0.);

      _GenSV->SetXYZ(0.,0.,0.);

      _IsGenRecoMatched=false;

      _isFSR=false;

      _cosp2G=-2;
      _cosp3G=-2;

      //reco gen-matched
      _DiMu4MomR->SetPtEtaPhiM(0.,0.,0.,0.);
      _DiMuPlusTrack4MomR->SetPtEtaPhiM(0.,0.,0.,0.);
  
      _Mu1_4MomR->SetPtEtaPhiM(0.,0.,0.,0.);
      _Mu2_4MomR->SetPtEtaPhiM(0.,0.,0.,0.);
      
      _MuTrack_4MomR->SetPtEtaPhiM(0.,0.,0.,0.);

      _Mu1_4MomR_Refit->SetPtEtaPhiM(0.,0.,0.,0.);
      _Mu2_4MomR_Refit->SetPtEtaPhiM(0.,0.,0.,0.);
      
      _MuTrack_4MomR_Refit->SetPtEtaPhiM(0.,0.,0.,0.);

      _isTkR1=false; _isGlbR1=false; _isSAR1=false; _isTMOR1=false; _isTightR1=false; _isPFR1=false;
      
      _npixR1=-10; _nTkR1=-10; _nMuR1=-10; _qR1=-10;
   
      _chiTkR1=-10; _chiMuR1=-10;_chiTkR1_Refit=-10;


      _isTkR2=false; _isGlbR2=false; _isSAR2=false; _isTMOR2=false; _isTightR2=false; _isPFR2=false;

      _npixR2=-10; _nTkR2=-10; _nMuR2=-10; _qR2=-10;
   
      _chiTkR2=-10; _chiMuR2=-10; _chiTkR2_Refit=-10;


      _isTkR3=false; _isGlbR3=false; _isSAR3=false; _isTMOR3=false; _isTightR3=false; _isPFR3=false;

      _npixR3=-10; _nTkR3=-10; _nMuR3=-10; _qR3=-10;
   
      _chiTkR3=-10; _chiMuR3=-10; _chiTkR3_Refit=-10;

      _DCA_SVR=-1;

      _3D_IP_SVR=-1;
      _3D_IPSig_SVR=-1 ;
      _3D_IP_PVR=-1;
      _3D_IPSig_PVR=-1 ;

      _Sum01R=-1;
      _Sum03R=-1;
      _Sum05R=-1;

      //reco gen-matched vertices
      _PVR->SetXYZ(0.,0.,0.);
      _SVR->SetXYZ(0.,0.,0.);
      _SVTR->SetXYZ(0.,0.,0.);
    
      _PVeR->SetXYZ(0.,0.,0.);
      _SVeR->SetXYZ(0.,0.,0.);
      _SVTeR->SetXYZ(0.,0.,0.);

      _SV_Mu1TR->SetXYZ(0.,0.,0.); 
      _SVe_Mu1TR->SetXYZ(0.,0.,0.);
      _SV_Mu2TR->SetXYZ(0.,0.,0.);
      _SVe_Mu2TR->SetXYZ(0.,0.,0.);

      _svValidR=false;
      _svtValidR=false;
      _isPVLeadingR=false;

      _sv1tValidR=false;
      _sv2tValidR=false;

      _SVchiR=-1;
      _SVprobR=-1;

      _SV1chiR=-1;
      _SV1probR=-1;

      _SV2chiR=-1;
      _SV2probR=-1;

      _SVTchiR=-1;
      _SVTprobR=-1;
      
      _LxyR=-1;
      _LxySigR=-1;
      _LxyTR=-1;
      _LxyTSigR=-1;

      _cosp2R=-2;
      _cosp3R=-2;

      _Ntracks_Mu1_R=-1;
      _Ntracks_Mu2_R=-1;

      _Ntracks_SVT_R=-1;
      _Ntracks_SV1_R=-1;
      _Ntracks_SV2_R=-1;

      _NtracksPV_SVT_R=-1;

      _DZ1R=-1;
      _DZ2R=-1;
      _DZ3R=-1;
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

  _Mu1_4Mom_Refit->SetPtEtaPhiM(0.,0.,0.,0.);
  _Mu2_4Mom_Refit->SetPtEtaPhiM(0.,0.,0.,0.);
  
  _MuTrack_4Mom_Mu_Refit->SetPtEtaPhiM(0.,0.,0.,0.);
  _MuTrack_4Mom_Pi_Refit->SetPtEtaPhiM(0.,0.,0.,0.);

  _Ntracks_Mu1=-1;
  _Ntracks_Mu2=-1;

  _Ntracks_SVT=-1;
  _Ntracks_SV1=-1;
  _Ntracks_SV2=-1;

  _NtracksPV_SVT=-1;

  _DZ1=-1;
  _DZ2=-1;
  _DZ3=-1;

  _Sum01=-1;
  _Sum03=-1;
  _Sum05=-1;

  _kink1=-1;
  _kink2=-1;
  _kink3=-1;

  _isTk1=false; _isGlb1=false; _isSA1=false; _isTMO1=false; _isTight1=false; _isPF1=false;

  _npix1=-10; _nTk1=-10; _nMu1=-10; _q1=-10;
  
  _chiTk1=-10; _chiMu1=-10;_chiTk1_Refit=-10;

  _isTk2=false; _isGlb2=false; _isSA2=false; _isTMO2=false; _isTight2=false; _isPF2=false;

  _npix2=-10; _nTk2=-10; _nMu2=-10; _q2=-10;
  
  _chiTk2=-10; _chiMu2=-10;_chiTk2_Refit=-10;

  _isTk3=false; _isGlb3=false; _isSA3=false; _isTMO3=false; _isTight3=false; _isPF3=false;

  _npix3=-10; _nTk3=-10; _nMu3=-10; _q3=-10;
   
  _chiTk3=-10; _chiMu3=-10;_chiTk3_Refit=-10;

  _DCA_SV=-1;
  
  _3D_IP_SV=-1;
  _3D_IPSig_SV=-1 ;
  _3D_IP_PV=-1;
  _3D_IPSig_PV=-1 ;
    
  //Offline vertices
  _PV->SetXYZ(0.,0.,0.);
  _SV->SetXYZ(0.,0.,0.);
  _SVT->SetXYZ(0.,0.,0.);
    
  _PVe->SetXYZ(0.,0.,0.);
  _SVe->SetXYZ(0.,0.,0.);
  _SVTe->SetXYZ(0.,0.,0.);

  _SV_Mu1T->SetXYZ(0.,0.,0.);
  _SVe_Mu1T->SetXYZ(0.,0.,0.);
  _SV_Mu2T->SetXYZ(0.,0.,0.);
  _SVe_Mu2T->SetXYZ(0.,0.,0.);

  _sv1tValid=false;
  _sv2tValid=false;
  _svValid=false;
  _svtValid=false;
  _isPVLeading=false;

  _SV1chi=-1;
  _SV1prob=-1;

  _SV2chi=-1;
  _SV2prob=-1;

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

    double dRtmp=0.005;
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

    if (dRtmp==0.005) runMatch=false;

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
    if (debug) cout << "new gen to match" << endl;
    double dRtmp=0.005;
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

    if (dRtmp==0.005) runMatch=false;
    else{
      if (debug) cout << "matched gindex " << gindex << " with tk " << tindex << " with dR " << dRtmp << endl; 
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
      if (debug){
	for (uint k=0; k< matches.size() ; ++k){
	  cout << "Gen particle " << matches[k].second << " matched with reco track:" <<endl;
	  cout << "Gen Pt " << genv[matches[k].second].Pt() << " reco Pt " << matches[k].first.Pt() << endl;
	}
      }
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

void Tau3MuAnalysis_V2::setMuIdToTrack(const edm::Event& ev, const Track* t,bool& isTkMu,bool& isSAMu,bool& isGlbMu,bool& isTMOMu,bool& isPFMu,bool& isTightMu,int& pix,int& tk,int& muh, int& q,double & chiTk,double& chiMu, bool& shares, double& kink){

  if (debug) cout << "Setting the mu id" << endl;

  pix=t->hitPattern().numberOfValidPixelHits();
  tk=t->hitPattern().numberOfValidTrackerHits();
  chiTk=t->normalizedChi2();
  q=t->charge();

  if (shares) return;

  edm::Handle<MuonCollection> muons;
  ev.getByLabel("muons",muons);

  for (MuonCollection::const_iterator recoMu = muons->begin();
       recoMu!=muons->end(); ++recoMu){

    if (!recoMu->isTrackerMuon()) continue;

    kink=recoMu->combinedQuality().trkKink;
    //cout << "track kink " << kink << endl;

    reco::TrackRef mu = recoMu->innerTrack();

    if (mu.isNonnull() && mu.isAvailable()){
      
      if (mu->pt() != t->pt()) continue;
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

  double kink=0;
  bool shares=false;
  setMuIdToTrack(event,matches[0].first, _isTkR1,_isSAR1,_isGlbR1 ,_isTMOR1, _isPFR1, _isTightR1, _npixR1,_nTkR1,_nMuR1,_qR1, _chiTkR1,_chiMuR1, shares, kink);
  setMuIdToTrack(event,matches[1].first, _isTkR2,_isSAR2,_isGlbR2 ,_isTMOR2, _isPFR2, _isTightR2, _npixR2,_nTkR2,_nMuR2,_qR2, _chiTkR2,_chiMuR2, shares, kink);
  setMuIdToTrack(event,matches[2].first, _isTkR3,_isSAR3,_isGlbR3 ,_isTMOR3, _isPFR3, _isTightR3, _npixR3,_nTkR3,_nMuR3,_qR3, _chiTkR3,_chiMuR3, shares, kink);

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
 
  if (isSignal) tr.SetPtEtaPhiM(matches[2].first->pt(),matches[2].first->eta(),matches[2].first->phi(),0.1057);
  else tr.SetPtEtaPhiM(matches[2].first->pt(),matches[2].first->eta(),matches[2].first->phi(),0.1396);

  TLorentzVector trimu=dimu+tr;

  TLorentzVector TotMomArray[3]={m1, m2, tr};
  double dRcount=0.2;

  ttv.push_back(tt1);
  ttv.push_back(tt2);

  KalmanVertexFitter avf(true);

  TransientVertex dimuvtx=avf.vertex(ttv);

  Vertex pvR;

  if (dimuvtx.isValid()){

    _Ntracks_Mu1_R=countTracksAround(event,iSetup,TotMomArray,dRcount,dimuvtx,1);
    _Ntracks_Mu2_R=countTracksAround(event,iSetup,TotMomArray,dRcount,dimuvtx,2);

    Vertex tv=Vertex(dimuvtx);
    pair<double,double> d0sv=ComputeImpactParameterWrtPoint(tt3,tv);

    _DCA_SVR=d0sv.first;

    _svValidR=true;

    if (debug) cout << " found valid Reco matched dimu vtx " << endl;

    _SVR->SetXYZ(dimuvtx.position().x(),dimuvtx.position().y(),dimuvtx.position().z());
    _SVeR->SetXYZ(dimuvtx.positionError().cxx(),dimuvtx.positionError().cyy(),dimuvtx.positionError().czz());

    _SVchiR=dimuvtx.normalisedChiSquared();
    _SVprobR=TMath::Prob(dimuvtx.totalChiSquared(),dimuvtx.degreesOfFreedom());

    pvR=findClosestPV(event,dimuvtx,_isPVLeadingR);

    _PVR->SetXYZ(pvR.position().x(),pvR.position().y(),pvR.position().z());

    pair<double,double> lxy=Compute_Lxy_and_Significance(pvR,dimuvtx,dimu);

    _LxyR=lxy.first;
    _LxySigR=lxy.first/lxy.second;

    _cosp2R=Compute_CosPointingAngle(pvR,dimuvtx,dimu);

    std::pair<bool,Measurement1D> ipv = IPTools::absoluteImpactParameter3D(tt3,pvR);
    std::pair<bool,Measurement1D> isv = IPTools::absoluteImpactParameter3D(tt3,tv);

    if (ipv.first){
      _3D_IP_PVR=ipv.second.value();
      if (debug) cout << "McMatched 3D IP wrt pv " << ipv.second.value() << endl;
      _3D_IPSig_PVR=ipv.second.significance();
    }

    if (isv.first){
      _3D_IP_SVR=isv.second.value();
      if (debug) cout << "McMatched 3D IP wrt sv= " << isv.second.value() << endl;
      _3D_IPSig_SVR=isv.second.significance();
    }

  }

  ttv.push_back(tt3);

  ptAround(pvR,ttv,trimu, 0.1, _Sum01R);
  ptAround(pvR,ttv,trimu, 0.3, _Sum03R);
  ptAround(pvR,ttv,trimu, 0.5, _Sum05R);

  TransientVertex trimuvtx=avf.vertex(ttv);

  if (trimuvtx.isValid()){

    TrackCompatibility(iSetup,pvR,trimuvtx,ttv,_NtracksPV_SVT_R);


    _svtValidR=true;

    if (debug) cout << " found valid Reco matched dimu+track vtx " << endl;

    if (trimuvtx.hasRefittedTracks()){

      if (debug) cout << "filling Reco Gen matched infos after vertex refit " << endl;
     
      TransientTrack t1=trimuvtx.refittedTrack(ttv[0]);
      TransientTrack t2=trimuvtx.refittedTrack(ttv[1]);
      TransientTrack t3=trimuvtx.refittedTrack(ttv[2]);

      _Mu1_4MomR_Refit->SetPtEtaPhiM(t1.track().pt(),t1.track().eta(),t1.track().phi(),0.1057);
      _Mu2_4MomR_Refit->SetPtEtaPhiM(t2.track().pt(),t2.track().eta(),t2.track().phi(),0.1057);
      if (isSignal) _MuTrack_4MomR_Refit->SetPtEtaPhiM(t3.track().pt(),t3.track().eta(),t3.track().phi(),0.1057);
      else _MuTrack_4MomR_Refit->SetPtEtaPhiM(t3.track().pt(),t3.track().eta(),t3.track().phi(),0.1396);

      _chiTkR1_Refit=t1.track().normalizedChi2();
      _chiTkR2_Refit=t2.track().normalizedChi2();
      _chiTkR3_Refit=t3.track().normalizedChi2();
      
    }

    _SVTR->SetXYZ(trimuvtx.position().x(),trimuvtx.position().y(),trimuvtx.position().z());
    _SVTeR->SetXYZ(trimuvtx.positionError().cxx(),trimuvtx.positionError().cyy(),trimuvtx.positionError().czz());

    vertexingTracks(event,iSetup, trimuvtx, _Ntracks_SVT_R);

    _SVTchiR=trimuvtx.normalisedChiSquared();
    _SVTprobR=TMath::Prob(trimuvtx.totalChiSquared(),trimuvtx.degreesOfFreedom());

    _DZ1R=matches[0].first->dz(Vertex(trimuvtx).position());
    _DZ2R=matches[1].first->dz(Vertex(trimuvtx).position());
    _DZ3R=matches[2].first->dz(Vertex(trimuvtx).position());

    if (!_svValidR)  pvR=findClosestPV(event,trimuvtx,_isPVLeadingR);

    pair<double,double> lxy=Compute_Lxy_and_Significance(pvR,trimuvtx,trimu);

    _LxyTR=lxy.first;
    _LxyTSigR=lxy.first/lxy.second;

    _cosp3R=Compute_CosPointingAngle(pvR,trimuvtx,trimu);

  }

  if (debug) cout << "Computing SV between the track and single muons" << endl;
  //vertices of track with single muons
  vector<TransientTrack> ttv1T;

  ttv1T.push_back(tt1);
  ttv1T.push_back(tt3);

  TransientVertex vtx1T=avf.vertex(ttv1T);

  if (vtx1T.isValid()){

    _sv1tValidR=true;

    _SV_Mu1TR->SetXYZ(vtx1T.position().x(),vtx1T.position().y(),vtx1T.position().z());
    _SVe_Mu1TR->SetXYZ(vtx1T.positionError().cxx(),vtx1T.positionError().cyy(),vtx1T.positionError().czz());

    _SV1chiR=vtx1T.normalisedChiSquared();
    _SV1probR=TMath::Prob(vtx1T.totalChiSquared(),vtx1T.degreesOfFreedom());

    vertexingTracks(event,iSetup, vtx1T, _Ntracks_SV1_R);
  }


  vector<TransientTrack> ttv2T;

  ttv2T.push_back(tt2);
  ttv2T.push_back(tt3);

  TransientVertex vtx2T=avf.vertex(ttv2T);

  if (vtx2T.isValid()){

    _sv2tValidR=true;

    _SV_Mu2TR->SetXYZ(vtx2T.position().x(),vtx2T.position().y(),vtx2T.position().z());
    _SVe_Mu2TR->SetXYZ(vtx2T.positionError().cxx(),vtx2T.positionError().cyy(),vtx2T.positionError().czz());

    _SV2chiR=vtx2T.normalisedChiSquared();
    _SV2probR=TMath::Prob(vtx2T.totalChiSquared(),vtx2T.degreesOfFreedom());

    vertexingTracks(event,iSetup, vtx2T, _Ntracks_SV2_R);
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
    ExTree->Branch(HLT_paths[i].c_str(), &_TrigBit[i],"_TrigBit/O");
  }

  if (debug) cout << "adding event branches" << endl;

  ExTree->Branch("Run",&_Run   , "_Run/I");
  ExTree->Branch("Lumi",&_Lum   , "_Lum/I");
  ExTree->Branch("Event",&_Evt   , "_Evt/I");

  ExTree->Branch("NumberOfVertices",&_Nvtx   , "_Nvtx/I");
  ExTree->Branch("NumberOfMuons",&_Nmu   , "_Nmu/I");
  ExTree->Branch("NumberOfTracks",&_Ntk   , "_Ntk/I");
  ExTree->Branch("NumberOfTriggerTracks",&_NTrigTk   , "_NTrigTk/I");
  ExTree->Branch("NumberOfTriggerMuons",&_NTrigMu   , "_NTrigMu/I");
  
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
      _Ds_4MomG= new TLorentzVector(0.,0.,0.,0.);
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

      _Mu1_4MomR_Refit= new TLorentzVector(0.,0.,0.,0.);
      _Mu2_4MomR_Refit= new TLorentzVector(0.,0.,0.,0.);
      _MuTrack_4MomR_Refit= new TLorentzVector(0.,0.,0.,0.);

      //reco gen-matched vertices
      _PVR= new TVector3(0.,0.,0.);
      _SVR=new TVector3(0.,0.,0.);
      _SVTR=new TVector3(0.,0.,0.);

      _PVeR= new TVector3(0.,0.,0.);
      _SVeR=new TVector3(0.,0.,0.);
      _SVTeR=new TVector3(0.,0.,0.);

      _SV_Mu1TR= new TVector3(0.,0.,0.);
      _SVe_Mu1TR= new TVector3(0.,0.,0.);
      _SV_Mu2TR= new TVector3(0.,0.,0.);
      _SVe_Mu2TR= new TVector3(0.,0.,0.);

      //
   
      //Gen variables
      ExTree->Branch("Ds_4Mom_Gen","TLorentzVector",&_Ds_4MomG); 
      ExTree->Branch("DiMu4Mom_Gen","TLorentzVector",&_DiMu4MomG); 
      ExTree->Branch("DiMuPlusTrack4Mom_Gen","TLorentzVector",&_DiMuPlusTrack4MomG); 
      
      ExTree->Branch("Mu1_4Mom_Gen","TLorentzVector",&_Mu1_4MomG); 
      ExTree->Branch("Mu2_4Mom_Gen","TLorentzVector",&_Mu2_4MomG); 
      ExTree->Branch("MuTrack_4Mom_Gen","TLorentzVector",&_MuTrack_4MomG);  

      ExTree->Branch("SV_Gen","TVector3",&_GenSV); 

      ExTree->Branch("CosPoint2_Gen",&_cosp2G   ,"_cosp2G/D");
      ExTree->Branch("CosPoint3_Gen",&_cosp3G   ,"_cosp3G/D");

      ExTree->Branch("IsFSR_Gen",&_isFSR   ,"_isFSR/O");

      if (debug) cout << "adding Reco MC matched branches" << endl;

      //Reco mc-matched branches
      ExTree->Branch("IsGenRecoMatched",&_IsGenRecoMatched   ,"_IsGenRecoMatched/O");

      ExTree->Branch("DiMu4Mom_Reco","TLorentzVector",&_DiMu4MomR); 
      ExTree->Branch("DiMuPlusTrack4Mom_Reco","TLorentzVector",&_DiMuPlusTrack4MomR); 
      
      ExTree->Branch("Mu1_4Mom_Reco","TLorentzVector",&_Mu1_4MomR); 
      ExTree->Branch("Mu2_4Mom_Reco","TLorentzVector",&_Mu2_4MomR); 
      ExTree->Branch("MuTrack_4Mom_Reco","TLorentzVector",&_MuTrack_4MomR);   

      ExTree->Branch("Mu1_4Mom_Refit_Reco","TLorentzVector",&_Mu1_4MomR_Refit); 
      ExTree->Branch("Mu2_4Mom_Refit_Reco","TLorentzVector",&_Mu2_4MomR_Refit); 
      ExTree->Branch("MuTrack_4Mom_Refit_Reco","TLorentzVector",&_MuTrack_4MomR_Refit);   
      
      //first muon
      ExTree->Branch("IsTkMu_Reco_1",&_isTkR1   ,"_isTkR1/O");
      ExTree->Branch("IsGlbMu_Reco_1",&_isGlbR1   ,"_isGlbR1/O");
      ExTree->Branch("IsSAMu_Reco_1",&_isSAR1   ,"_isSAR1/O");
      ExTree->Branch("IsTMOMu_Reco_1",&_isTMOR1   ,"_isTMOR1/O");
      ExTree->Branch("IsTightMu_Reco_1",&_isTightR1   ,"_isTightR1/O");
      ExTree->Branch("IsPFMu_Reco_1",&_isPFR1   ,"_isPFR1/O");
      
      ExTree->Branch("nPixHits_Reco_1",&_npixR1   ,"_npixR1/I");
      ExTree->Branch("nTkHits_Reco_1",&_nTkR1   ,"_nTkR1/I");
      ExTree->Branch("nMuHits_Reco_1",&_nMuR1   ,"_nMuR1/I");
      ExTree->Branch("Q_Reco_1",&_qR1   ,"_qR1/I");

      ExTree->Branch("chiTk_Reco_1",&_chiTkR1   ,"_chiTkR1/D");
      //ExTree->Branch("chiTk_Refit_Reco_1",&_chiTkR1_Refit   ,"_chiTkR1_Refit/D");
      ExTree->Branch("chiMu_Reco_1",&_chiMuR1   ,"_chiMuR1/D");

      //second muon
      ExTree->Branch("IsTkMu_Reco_2",&_isTkR2   ,"_isTkR2/O");
      ExTree->Branch("IsGlbMu_Reco_2",&_isGlbR2   ,"_isGlbR2/O");
      ExTree->Branch("IsSAMu_Reco_2",&_isSAR2   ,"_isSAR2/O");
      ExTree->Branch("IsTMOMu_Reco_2",&_isTMOR2   ,"_isTMOR2/O");
      ExTree->Branch("IsTightMu_Reco_2",&_isTightR2   ,"_isTightR2/O");
      ExTree->Branch("IsPFMu_Reco_2",&_isPFR2   ,"_isPFR2/O");

      ExTree->Branch("nPixHits_Reco_2",&_npixR2   ,"_npixR2/I");
      ExTree->Branch("nTkHits_Reco_2",&_nTkR2   ,"_nTkR2/I");
      ExTree->Branch("nMuHits_Reco_2",&_nMuR2   ,"_nMuR2/I");
      ExTree->Branch("Q_Reco_2",&_qR2   ,"_qR2/I");

      ExTree->Branch("chiTk_Reco_2",&_chiTkR2   ,"_chiTkR2/D");
      //ExTree->Branch("chiTk_Refit_Reco_2",&_chiTkR2_Refit   ,"_chiTkR2_Refit/D");
      ExTree->Branch("chiMu_Reco_2",&_chiMuR2   ,"_chiMuR2/D");

      //third mu-track
      ExTree->Branch("IsTkMu_Reco_3",&_isTkR3   ,"_isTkR3/O");
      ExTree->Branch("IsGlbMu_Reco_3",&_isGlbR3   ,"_isGlbR3/O");
      ExTree->Branch("IsSAMu_Reco_3",&_isSAR3   ,"_isSAR3/O");
      ExTree->Branch("IsTMOMu_Reco_3",&_isTMOR3   ,"_isTMOR3/O");
      ExTree->Branch("IsTightMu_Reco_3",&_isTightR3   ,"_isTightR3/O");
      ExTree->Branch("IsPFMu_Reco_3",&_isPFR3   ,"_isPFR3/O");

      ExTree->Branch("nPixHits_Reco_3",&_npixR3   ,"_npixR3/I");
      ExTree->Branch("nTkHits_Reco_3",&_nTkR3   ,"_nTkR3/I");
      ExTree->Branch("nMuHits_Reco_3",&_nMuR3   ,"_nMuR3/I");
      ExTree->Branch("Q_Reco_3",&_qR3   ,"_qR3/I");

      ExTree->Branch("chiTk_Reco_3",&_chiTkR3   ,"_chiTkR3/D");
      //ExTree->Branch("chiTk_Refit_Reco_3",&_chiTkR3_Refit   ,"_chiTkR3_Refit/D");
      ExTree->Branch("chiMu_Reco_3",&_chiMuR3   ,"_chiMuR3/D");

      ExTree->Branch("DCATrack_SV_Reco_3",&_DCA_SVR   ,"_DCA_SVR/D");

      ExTree->Branch("SumPt01_Reco",&_Sum01R,"_Sum01R/D");
      ExTree->Branch("SumPt03_Reco",&_Sum03R,"_Sum03R/D");
      ExTree->Branch("SumPt05_Reco",&_Sum05R,"_Sum05R/D");

      ExTree->Branch("IP3D_SV_Reco",&_3D_IP_SVR   ,"_3D_IP_SVR/D");
      ExTree->Branch("IP3DSig_SV_Reco",&_3D_IPSig_SVR   ,"_3D_IPSig_SVR/D");

      ExTree->Branch("IP3D_PV_Reco",&_3D_IP_PVR   ,"_3D_IP_PVR/D");
      ExTree->Branch("IP3DSig_PV_Reco",&_3D_IPSig_PVR   ,"_3D_IPSig_PVR/D");
  
      //

      //Reco GEN matched vertices
 
      ExTree->Branch("isValid_Mu1TrackSV_Reco",&_sv1tValidR,"_sv1tValidR/O");
      ExTree->Branch("isValid_Mu2TrackSV_Reco",&_sv2tValidR,"_sv2tValidR/O"); 

      ExTree->Branch("isValidSV_Reco",&_svValidR,"_svValidR/O"); 
      ExTree->Branch("isValidSVT_Reco",&_svtValidR,"_svtValidR/O"); 
      ExTree->Branch("isPVLeading_Reco",&_isPVLeadingR,"_isPVLeadingR/O");

      ExTree->Branch("PV_Reco","TVector3",&_PVR); 
      ExTree->Branch("SV_Reco","TVector3",&_SVR);
      ExTree->Branch("SVT_Reco","TVector3",&_SVTR);

      ExTree->Branch("SV_Mu1Track_Reco","TVector3",&_SV_Mu1TR);
      ExTree->Branch("SVerr_Mu1Track_Reco","TVector3",&_SVe_Mu1TR);

      ExTree->Branch("SV_Mu2Track_Reco","TVector3",&_SV_Mu2TR);
      ExTree->Branch("SVerr_Mu2Track_Reco","TVector3",&_SVe_Mu2TR);

      ExTree->Branch("PVerr_Reco","TVector3",&_PVeR); 
      ExTree->Branch("SVerr_Reco","TVector3",&_SVeR);
      ExTree->Branch("SVTerr_Reco","TVector3",&_SVTeR);

      ExTree->Branch("SV_Mu1Track_chi_Reco",&_SV1chiR   ,"_SV1chiR/D"); 
      ExTree->Branch("SV_Mu1Track_prob_Reco",&_SV1probR   ,"_SV1probR/D"); 

      ExTree->Branch("SV_Mu2Track_chi_Reco",&_SV2chiR   ,"_SV2chiR/D"); 
      ExTree->Branch("SV_Mu2Track_prob_Reco",&_SV2probR   ,"_SV2probR/D"); 

      ExTree->Branch("SVchi_Reco",&_SVchiR   ,"_SVchiR/D"); 
      ExTree->Branch("SVprob_Reco",&_SVprobR   ,"_SVprobR/D"); 
      ExTree->Branch("SVTchi_Reco",&_SVTchiR   ,"_SVTchiR/D"); 
      ExTree->Branch("SVTprob_Reco",&_SVTprobR   ,"_SVTprobR/D"); 
  
      ExTree->Branch("Lxy_Reco",&_LxyR   ,"_LxyR/D");
      ExTree->Branch("LxySig_Reco",&_LxySigR   ,"_LxySigR/D");
      ExTree->Branch("LxyT_Reco",&_LxyTR   ,"_LxyTR/D");
      ExTree->Branch("LxyTSig_Reco",&_LxyTSigR   ,"_LxyTSigR/D");
    
      ExTree->Branch("CosPoint2_Reco",&_cosp2R   ,"_cosp2R/D");
      ExTree->Branch("CosPoint3_Reco",&_cosp3R   ,"_cosp3R/D");

      ExTree->Branch("Ntracks_AroundMu1_Reco",&_Ntracks_Mu1_R,"_Ntracks_Mu1_R/I");
      ExTree->Branch("Ntracks_AroundMu2_Reco",&_Ntracks_Mu2_R,"_Ntracks_Mu2_R/I");

      ExTree->Branch("Ntracks_SVT_Reco",&_Ntracks_SVT_R,"_Ntracks_SVT_R/I");
      ExTree->Branch("Ntracks_SV1_Reco",&_Ntracks_SV1_R,"_Ntracks_SV1_R/I");
      ExTree->Branch("Ntracks_SV2_Reco",&_Ntracks_SV2_R,"_Ntracks_SV2_R/I");

      ExTree->Branch("NtracksPV_SVTCompatible_Reco",&_NtracksPV_SVT_R,"_NtracksPV_SVT_R/I");

      ExTree->Branch("dZ1_SVT_Reco",&_DZ1R   ,"_DZ1R/D");
      ExTree->Branch("dZ2_SVT_Reco",&_DZ2R   ,"_DZ2R/D");
      ExTree->Branch("dZ3_SVT_Reco",&_DZ3R   ,"_DZ3R/D");
      //
    }

    ExTree->Branch("IsOfflineMcMatched",&_IsMcMatched ,"_IsMcMatched/O");
  }

  if (debug) cout << "adding Offline branches" << endl;
  
  //Offline variables

  ExTree->Branch("IsOfflineReco",&_IsOffline,"_IsOffline/O");

  ExTree->Branch("IsTrigMatched_Offline",&_TriggerMatched,"_TriggerMatched/O");
  ExTree->Branch("IsDiMuFound_Offline",&_DiMuFound,"_DiMuFound/O");
  ExTree->Branch("IsTrackFound_Offline",&_TrackFound,"_TrackFound/O");
	
  _DiMu4Mom= new TLorentzVector(0.,0.,0.,0.);
  _DiMuPlusTrack4Mom_Mu= new TLorentzVector(0.,0.,0.,0.);
  _DiMuPlusTrack4Mom_Pi= new TLorentzVector(0.,0.,0.,0.);

  _Mu1_4Mom= new TLorentzVector(0.,0.,0.,0.);
  _Mu2_4Mom= new TLorentzVector(0.,0.,0.,0.);

  _MuTrack_4Mom_Mu= new TLorentzVector(0.,0.,0.,0.);
  _MuTrack_4Mom_Pi= new TLorentzVector(0.,0.,0.,0.);

  _Mu1_4Mom_Refit= new TLorentzVector(0.,0.,0.,0.);
  _Mu2_4Mom_Refit= new TLorentzVector(0.,0.,0.,0.);

  _MuTrack_4Mom_Mu_Refit= new TLorentzVector(0.,0.,0.,0.);
  _MuTrack_4Mom_Pi_Refit= new TLorentzVector(0.,0.,0.,0.);

  _PV= new TVector3(0.,0.,0.);
  _SV=new TVector3(0.,0.,0.);
  _SVT=new TVector3(0.,0.,0.);

  _SV_Mu1T= new TVector3(0.,0.,0.);
  _SVe_Mu1T= new TVector3(0.,0.,0.);
  _SV_Mu2T= new TVector3(0.,0.,0.);
  _SVe_Mu2T= new TVector3(0.,0.,0.);

  _PVe= new TVector3(0.,0.,0.);
  _SVe=new TVector3(0.,0.,0.);
  _SVTe=new TVector3(0.,0.,0.);

  ExTree->Branch("DiMu4Mom_Offline","TLorentzVector",&_DiMu4Mom); 
  ExTree->Branch("DiMuPlusTrack4Mom_Mu_Offline","TLorentzVector",&_DiMuPlusTrack4Mom_Mu); 
  ExTree->Branch("DiMuPlusTrack4Mom_Pi_Offline","TLorentzVector",&_DiMuPlusTrack4Mom_Pi); 

  ExTree->Branch("Mu1_4Mom_Offline","TLorentzVector",&_Mu1_4Mom); 
  ExTree->Branch("Mu2_4Mom_Offline","TLorentzVector",&_Mu2_4Mom); 
  ExTree->Branch("MuTrack_4Mom_Pi_Offline","TLorentzVector",&_MuTrack_4Mom_Pi); 
  ExTree->Branch("MuTrack_4Mom_Mu_Offline","TLorentzVector",&_MuTrack_4Mom_Mu); 

  ExTree->Branch("Mu1_4Mom_Refit_Offline","TLorentzVector",&_Mu1_4Mom_Refit); 
  ExTree->Branch("Mu2_4Mom_Refit_Offline","TLorentzVector",&_Mu2_4Mom_Refit); 
  ExTree->Branch("MuTrack_Refit_4Mom_Pi_Offline","TLorentzVector",&_MuTrack_4Mom_Pi_Refit); 
  ExTree->Branch("MuTrack_Refit_4Mom_Mu_Offline","TLorentzVector",&_MuTrack_4Mom_Mu_Refit); 

 //first offline mu   
  ExTree->Branch("IsTkMu_Offline_1",&_isTk1   ,"_isTk1/O");
  ExTree->Branch("IsGlbMu_Offline_1",&_isGlb1   ,"_isGlb1/O");
  ExTree->Branch("IsSAMu_Offline_1",&_isSA1   ,"_isSA1/O");
  ExTree->Branch("IsTMOMu_Offline_1",&_isTMO1   ,"_isTMO1/O");
  ExTree->Branch("IsTightMu_Offline_1",&_isTight1   ,"_isTight1/O");
  ExTree->Branch("IsPFMu_Offline_1",&_isPF1   ,"_isPF1/O");

  ExTree->Branch("nPixHits_Offline_1",&_npix1   ,"_npix1/I");
  ExTree->Branch("nTkHits_Offline_1",&_nTk1   ,"_nTk1/I");
  ExTree->Branch("nMuHits_Offline_1",&_nMu1   ,"_nMu1/I");
  ExTree->Branch("Q_Offline_1",&_q1   ,"_q1/I");

  ExTree->Branch("chiTk_Offline_1",&_chiTk1   ,"_chiTk1/D");
  //ExTree->Branch("chiTk_Refit_Offline_1",&_chiTk1_Refit   ,"_chiTk1_Refit/D");
  ExTree->Branch("chiMu_Offline_1",&_chiMu1   ,"_chiMu1/D");
  //

  //second offline mu
  ExTree->Branch("IsTkMu_Offline_2",&_isTk2   ,"_isTk2/O");
  ExTree->Branch("IsGlbMu_Offline_2",&_isGlb2   ,"_isGlb2/O");
  ExTree->Branch("IsSAMu_Offline_2",&_isSA2   ,"_isSA2/O");
  ExTree->Branch("IsTMOMu_Offline_2",&_isTMO2   ,"_isTMO2/O");
  ExTree->Branch("IsTightMu_Offline_2",&_isTight2   ,"_isTight2/O");
  ExTree->Branch("IsPFMu_Offline_2",&_isPF2   ,"_isPF2/O");

  ExTree->Branch("nPixHits_Offline_2",&_npix2   ,"_npix2/I");
  ExTree->Branch("nTkHits_Offline_2",&_nTk2   ,"_nTk2/I");
  ExTree->Branch("nMuHits_Offline_2",&_nMu2   ,"_nMu2/I");
  ExTree->Branch("Q_Offline_2",&_q2   ,"_q2/I");

  ExTree->Branch("chiTk_Offline_2",&_chiTk2   ,"_chiTk2/D");
  //ExTree->Branch("chiTk_Refit_Offline_2",&_chiTk2_Refit   ,"_chiTk2_Refit/D");
  ExTree->Branch("chiMu_Offline_2",&_chiMu2   ,"_chiMu2/D");
 //
 //third offline mu-track   
  ExTree->Branch("IsTkMu_Offline_3",&_isTk3   ,"_isTk3/O");
  ExTree->Branch("IsGlbMu_Offline_3",&_isGlb3   ,"_isGlb3/O");
  ExTree->Branch("IsSAMu_Offline_3",&_isSA3   ,"_isSA3/O");
  ExTree->Branch("IsTMOMu_Offline_3",&_isTMO3   ,"_isTMO3/O");
  ExTree->Branch("IsTightMu_Offline_3",&_isTight3   ,"_isTight3/O");
  ExTree->Branch("IsPFMu_Offline_3",&_isPF3   ,"_isPF3/O");

  ExTree->Branch("nPixHits_Offline_3",&_npix3   ,"_npix3/I");
  ExTree->Branch("nTkHits_Offline_3",&_nTk3   ,"_nTk3/I");
  ExTree->Branch("nMuHits_Offline_3",&_nMu3   ,"_nMu3/I");
  ExTree->Branch("Q_Offline_3",&_q3   ,"_q3/I");

  ExTree->Branch("chiTk_Offline_3",&_chiTk3   ,"_chiTk3/D");
  //ExTree->Branch("chiTk_Refit_Offline_3",&_chiTk3_Refit   ,"_chiTk3_Refit/D");
  ExTree->Branch("chiMu_Offline_3",&_chiMu3   ,"_chiMu3/D");

  ExTree->Branch("DCATrack_SV_Offline_3",&_DCA_SV   ,"_DCA_SV/D");

  ExTree->Branch("IP3D_SV_Offline",&_3D_IP_SV   ,"_3D_IP_SV/D");
  ExTree->Branch("IP3DSig_SV_Offline",&_3D_IPSig_SV   ,"_3D_IPSig_SV/D");

  ExTree->Branch("IP3D_PV_Offline",&_3D_IP_PV   ,"_3D_IP_PV/D");
  ExTree->Branch("IP3DSig_PV_Offline",&_3D_IPSig_PV   ,"_3D_IPSig_PV/D");

  ExTree->Branch("Ntracks_AroundMu1_Offline",&_Ntracks_Mu1,"_Ntracks_Mu1/I");
  ExTree->Branch("Ntracks_AroundMu2_Offline",&_Ntracks_Mu2,"_Ntracks_Mu2/I");

  ExTree->Branch("Ntracks_SVT_Offline",&_Ntracks_SVT,"_Ntracks_SVT/I");
  ExTree->Branch("Ntracks_SV1_Offline",&_Ntracks_SV1,"_Ntracks_SV1/I");
  ExTree->Branch("Ntracks_SV2_Offline",&_Ntracks_SV2,"_Ntracks_SV2/I");

  ExTree->Branch("NtracksPV_SVTCompatible_Offline",&_NtracksPV_SVT,"_NtracksPV_SVT/I");

  ExTree->Branch("dZ1_SVT_Offline",&_DZ1   ,"_DZ1/D");
  ExTree->Branch("dZ2_SVT_Offline",&_DZ2   ,"_DZ2/D");
  ExTree->Branch("dZ3_SVT_Offline",&_DZ3   ,"_DZ3/D");

  ExTree->Branch("Kink_Offline_1",&_kink1   ,"_kink1/D");
  ExTree->Branch("Kink_Offline_2",&_kink2   ,"_kink2/D");
  ExTree->Branch("Kink_Offline_3",&_kink3   ,"_kink3/D");

 //
 //Offline vertices

  ExTree->Branch("isValid_Mu1TrackSV_Offline",&_sv1tValid,"_sv1tValid/O");
  ExTree->Branch("isValid_Mu2TrackSV_Offline",&_sv2tValid,"_sv2tValid/O"); 

  ExTree->Branch("isValidSV_Offline",&_svValid,"_svValid/O"); 
  ExTree->Branch("isValidSVT_Offline",&_svtValid,"_svtValid/O"); 
  ExTree->Branch("isPVLeading_Offline",&_isPVLeading,"_isPVLeading/O");

  ExTree->Branch("PV_Offline","TVector3",&_PV); 
  ExTree->Branch("SV_Offline","TVector3",&_SV);

  ExTree->Branch("SV_Mu1Track_Offline","TVector3",&_SV_Mu1T);
  ExTree->Branch("SV_Mu2Track_Offline","TVector3",&_SV_Mu2T);

  ExTree->Branch("SVerr_Mu1Track_Offline","TVector3",&_SVe_Mu1T);
  ExTree->Branch("SVerr_Mu2Track_Offline","TVector3",&_SVe_Mu2T);

  ExTree->Branch("SVT_Offline","TVector3",&_SVT);

  ExTree->Branch("PVerr_Offline","TVector3",&_PVe); 
  ExTree->Branch("SVerr_Offline","TVector3",&_SVe);
  ExTree->Branch("SVTerr_Offline","TVector3",&_SVTe);
  
  ExTree->Branch("SV_Mu1Track_chi_Offline",&_SV1chi   ,"_SV1chi/D"); 
  ExTree->Branch("SV_Mu1Track_prob_Offline",&_SV1prob   ,"_SV1prob/D");

  ExTree->Branch("SV_Mu2Track_chi_Offline",&_SV2chi   ,"_SV2chi/D"); 
  ExTree->Branch("SV_Mu2Track_prob_Offline",&_SV2prob   ,"_SV2prob/D");

  ExTree->Branch("SVchi_Offline",&_SVchi   ,"_SVchi/D"); 
  ExTree->Branch("SVprob_Offline",&_SVprob   ,"_SVprob/D"); 
  ExTree->Branch("SVTchi_Offline",&_SVTchi   ,"_SVTchi/D"); 
  ExTree->Branch("SVTprob_Offline",&_SVTprob   ,"_SVTprob/D"); 

  ExTree->Branch("Lxy_Offline",&_Lxy   ,"_Lxy/D");
  ExTree->Branch("LxySig_Offline",&_LxySig   ,"_LxySig/D");
  ExTree->Branch("LxyT_Offline",&_LxyT   ,"_LxyT/D");
  ExTree->Branch("LxyTSig_Offline",&_LxyTSig   ,"_LxyTSig/D");

  ExTree->Branch("SumPt01_Offline",&_Sum01,"_Sum01/D");
  ExTree->Branch("SumPt03_Offline",&_Sum03,"_Sum03/D");
  ExTree->Branch("SumPt05_Offline",&_Sum05,"_Sum05/D");

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
  sprintf(title,"Tot= %i  Passed= %i",Total,Offline);
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
  sprintf(title,"Tot diMu Searches= %i  events with diMu= %i", Triggered,FoundDiMuTrig);
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
  sprintf(title,"Tot Track Searches= %i  events passed= %i", FoundDiMuTrig,Offline);
  
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

    delete _SV_Mu1TR;
    delete _SVe_Mu1TR;

    delete _SV_Mu2TR;
    delete _SVe_Mu2TR;

    delete _SVTeR;
    delete _SVeR;
    delete _PVeR;
  
    delete _MuTrack_4MomR;
    delete _Mu2_4MomR;
    delete _Mu1_4MomR;

    delete _MuTrack_4MomR_Refit;
    delete _Mu2_4MomR_Refit;
    delete _Mu1_4MomR_Refit;
     
    delete _DiMuPlusTrack4MomR;
    delete _DiMu4MomR;

    delete _Ds_4MomG;

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

  delete _SV_Mu1T;
  delete _SVe_Mu1T;

  delete _SV_Mu2T;
  delete _SVe_Mu2T;

  delete _SVTe;
  delete _SVe;
  delete _PVe;

  delete _MuTrack_4Mom_Mu;
  delete _MuTrack_4Mom_Pi;
  delete _Mu2_4Mom;
  delete _Mu1_4Mom;

  delete _MuTrack_4Mom_Mu_Refit;
  delete _MuTrack_4Mom_Pi_Refit;
  delete _Mu2_4Mom_Refit;
  delete _Mu1_4Mom_Refit;
 
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
  if (IsMC) std::cout << "Events selected offline and MC matched " << GenMatches  << std::endl;
}

#include "FWCore/Framework/interface/MakerMacros.h"  
DEFINE_FWK_MODULE( Tau3MuAnalysis_V2 );
