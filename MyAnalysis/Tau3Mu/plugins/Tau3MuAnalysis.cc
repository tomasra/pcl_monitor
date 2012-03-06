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
#include "TTree.h"
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

inline bool sortByPt(const reco::Candidate *part1, const reco::Candidate *part2) {

  return part1->pt() > part2->pt();
}

inline bool sortMuByPt(const reco::Muon mu1, const reco::Muon mu2) {

  return mu1.pt() > mu2.pt();
}

//-----------------------------------------------------------------
class Tau3MuAnalysis : public edm::EDAnalyzer {
public:
  explicit Tau3MuAnalysis(const edm::ParameterSet&);
  ~Tau3MuAnalysis();

private:
  virtual void beginJob();
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob();
  virtual void Initialize_TreeVars();
  virtual void vtx(std::vector<TransientTrack>&, GlobalPoint &, GlobalError &);
  virtual pair<double,double> Compute_Lxy_and_Significance(Vertex &, TransientVertex &, TLorentzVector&);
  virtual void findBestDimuon( const edm::EventSetup&, MuonCollection&, MuonCollection&, TransientVertex&, Vertex&);
  virtual void findBestPiCand(const edm::Event&, const edm::EventSetup&, MuonCollection&, TransientVertex&, Vertex&, TransientVertex&,pair<double,double>& ,TLorentzVector&, bool&,bool& ,int&);
  virtual bool TriggerDecision(const edm::Event&);
  virtual pair<bool,bool> isMu(const edm::Event&, const Track*);
  virtual int countTracksAround(const edm::Event&, const edm::EventSetup&, TLorentzVector*, double&, TransientVertex&);
  virtual pair<double,double> ComputeImpactParameterWrtPoint(TransientTrack& tt, Vertex&);
  virtual bool isMcMatched(const edm::Event&,TLorentzVector*);
  virtual bool isInPV(Vertex&, TLorentzVector&);

  TH1F* hDiMuInvMass,* hGoodDiMuInvMass;
  TH1F* hDiMuTrackInvMass,* hGoodDiMuTrackInvMass,*hTriMuInvMass ;

  TH1F* hpt, *hptMu,*hDiMuPt;
  TH1F* htotEff,* hDiMuEff, *hTrackEff;

  //
  double diMuMassMin, diMuMassMax, diMuLxyMin,diMuLxySigMin,diMuVtxChi2Max, diMuVprobMin;
  double diMuTrackMassMin, diMuTrackMassMax, diMuTrackLxyMin,diMuTrackLxySigMin,diMuTrackVtxChi2Max,diMuTrackVprobMin;
  double MinTrackPt, MinMuPt;
  double Trackd0Max,Trackd0SigMin;
  double DRTracks;

  double TrackMass;
  // Tree and variables
  TFile* thefile;
  std::string FileName;
  TTree *ExTree;
  TLorentzVector* _Mu1_4Mom,*_Mu2_4Mom,*_MuTrack_4Mom, *_DiMu4Mom, *_DiMuPlusTrack4Mom;
  int _Mu1Q,_Mu2Q,_Mu3Q;

  TVector3 *_PV,*_SV,*_SVT,*_PVe,*_SVe,*_SVTe;

  double _SVchi,_SVprob;
  double _SVTchi,_SVTprob;
  double _Lxy,_LxySig,_LxyT,_LxyTSig;
  double _d0T,_d0TSig;
  double _M3,_M2 ,_PtT,_dRdiMuT;
  int _NTracksInDr;
  bool _TrackIsMu;
  bool _Mu1IsGood,_Mu2IsGood,_TrackIsGoodMu;
  bool _IsMu1InPV, _IsMu2InPV,_IsMu3InPV;

  bool OnlyGenMatchInTree;

  std::vector<string> HLT_paths;
  std::string HLT_process;

  bool OnlyOppositeCharge;
  bool debug;

  double ndm, ndmv, ndmm, ndmlxy, ndmlxys, ndmchi, ndmvprob;
  double nt, ntq, ntm, ntd0, ntd0s,ntv, ntlxy, ntlxys, ntchi, ntvprob;

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

Tau3MuAnalysis::Tau3MuAnalysis(const edm::ParameterSet& cfg) {

  Total=0;
  Triggered=0;
  FoundDiMu=0;
  Offline=0;

  ndm=0; ndmv=0; ndmm=0; ndmlxy=0; ndmlxys=0; ndmchi=0; ndmvprob=0;
  nt=0; ntq=0; ntm=0; ntd0=0; ntd0s=0;ntv=0; ntlxy=0; ntlxys=0; ntchi=0; ntvprob=0;

  diMuMassMin= cfg.getParameter<double> ("DiMuMassMin"); 
  diMuMassMax= cfg.getParameter<double> ("DiMuMassMax");  
  diMuLxyMin = cfg.getParameter<double> ("DiMuLxyMin"); 
  diMuLxySigMin = cfg.getParameter<double> ("DiMuLxySigMin");
  diMuVtxChi2Max= cfg.getParameter<double> ("DiMuVtxChi2Max");
  diMuVprobMin= cfg.getParameter<double> ("DiMuVprobMin");
  
  diMuTrackMassMin= cfg.getParameter<double> ("DiMuTrackMassMin"); 
  diMuTrackMassMax= cfg.getParameter<double> ("DiMuTrackMassMax"); 
  diMuTrackLxyMin = cfg.getParameter<double> ("DiMuTrackLxyMin");
  diMuTrackLxySigMin = cfg.getParameter<double> ("DiMuTrackLxySigMin");
  diMuTrackVtxChi2Max= cfg.getParameter<double> ("DiMuTrackVtxChi2Max");
  diMuTrackVprobMin= cfg.getParameter<double> ("DiMuTrackVprobMin");

  MinMuPt=cfg.getParameter<double> ("MuPTCut");
  MinTrackPt=cfg.getParameter<double> ("TrackPTCut");

  HLT_paths = cfg.getParameter<std::vector<string> > ("HLT_paths");
  HLT_process = cfg.getParameter<std::string> ("HLT_process");

  OnlyGenMatchInTree= cfg.getParameter<bool> ("SaveOnlyGenMatchedVar");
  OnlyOppositeCharge= cfg.getParameter<bool> ("OnlyOppositeChargeMuons");
  TrackMass= cfg.getParameter<double> ("GuessForTrackMass");

  DRTracks=cfg.getParameter<double> ("MaxDrForTrackCount");

  Trackd0Max= cfg.getParameter<double> ("Trackd0Max");
  Trackd0SigMin= cfg.getParameter<double> ("Trackd0SigMin");

  debug=cfg.getParameter<bool> ("Debug");
  FileName = cfg.getParameter<std::string> ("OutFileName");
}

Tau3MuAnalysis::~Tau3MuAnalysis() {}

//
// member functions
//
void Tau3MuAnalysis::findBestPiCand(const edm::Event& ev, const edm::EventSetup& iSetup, MuonCollection& dimu ,TransientVertex& tv, Vertex& primaryVertex,TransientVertex& dimuvtx ,pair<double,double>& d0track, TLorentzVector& pi, bool & isMuon, bool& isGood ,int& q){

  if (debug) cout << "Looking for the pi track" << endl;

  edm::ESHandle<TransientTrackBuilder> Builder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", Builder);

  Handle<TrackCollection> tracks;
  ev.getByLabel("generalTracks", tracks);

  KalmanVertexFitter avf;

  double tmpProb=diMuTrackVprobMin;
  double Vp0=diMuTrackVprobMin;

  for(TrackCollection::const_iterator it = tracks->begin();it != tracks->end(); ++it){

    if ((it->pt()==dimu[0].innerTrack()->pt() && it->eta()==dimu[0].innerTrack()->eta()) || (it->pt()==dimu[1].innerTrack()->pt() && it->eta()==dimu[1].innerTrack()->eta())) continue;
    if (dimu[0].charge()==dimu[1].charge() && it->charge()==dimu[0].charge()) continue; //impossible to have a particle with charge +/- 3

    nt++;

    if (!(it->quality(TrackBase::highPurity)) || it->pt()< MinTrackPt) continue;

    ntq++;

    TLorentzVector m1=TLorentzVector(dimu[0].px(),dimu[0].py(),dimu[0].pz(),dimu[0].energy());
    TLorentzVector m2=TLorentzVector(dimu[1].px(),dimu[1].py(),dimu[1].pz(),dimu[1].energy());
    TLorentzVector p=TLorentzVector(it->px(),it->py(),it->pz(),sqrt(TrackMass*TrackMass+it->p()*it->p()));
    TLorentzVector tot=m1+m2+p;

    if (tot.M() < diMuTrackMassMin || tot.M()> diMuTrackMassMax) continue;
    ntm++;

    vector<TransientTrack> tt;
    TransientVertex tmpvtx;
    TransientTrack ttpi;

    tt.push_back(Builder->build(dimu[0].innerTrack()));
    tt.push_back(Builder->build(dimu[1].innerTrack()));
    tt.push_back(Builder->build(*it));
    ttpi=Builder->build(*it);

    Vertex diMuVtx=Vertex(tv);
    pair<double,double> d0tracktmp=ComputeImpactParameterWrtPoint(ttpi,diMuVtx);

    if (d0tracktmp.first > Trackd0Max) continue;
    ntd0++;

    if (d0tracktmp.first/d0tracktmp.second < Trackd0SigMin) continue; 
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


    pair<double,double> lxytmp=Compute_Lxy_and_Significance(primaryVertex,tmpvtx,tot);

    if (lxytmp.first < diMuTrackLxyMin) continue;
    ntlxy++;

    if (lxytmp.first/lxytmp.second < diMuTrackLxySigMin) continue;
    ntlxys++;

    if (vProb < tmpProb) continue;
    
    tmpProb=vProb;
    pi=p;
    isMuon=isMu(ev,&(*it)).first;
    isGood=isMu(ev,&(*it)).second;
    q=it->charge();
    tv=tmpvtx;
    d0track=d0tracktmp;      
  }
}

bool Tau3MuAnalysis::isInPV(Vertex& pv,TLorentzVector& track){

  bool inPV=false;
  for(std::vector<reco::TrackBaseRef>::const_iterator it = pv.tracks_begin() ; it != pv.tracks_end(); ++it ){
    if (!(it->isNonnull() && it->isAvailable())) continue;
    Track tr=*(it->get());
    TLorentzVector vect=TLorentzVector(tr.px(),tr.py(),tr.pz(),0);
    if (vect.DeltaR(track)<1.e-4) inPV=true;
  }
  return inPV;
}

bool Tau3MuAnalysis::isMcMatched(const edm::Event& ev,TLorentzVector* recov){

  if (debug) cout << "GEN-RECO Matching ...." << endl;

  bool ThreeMatches=false;
  std::vector<TLorentzVector> TheGenMus;

  //find the right gen muons

  string mcTruthCollection = "genParticles";
  edm::Handle< reco::GenParticleCollection > genParticleHandle;
  ev.getByLabel(mcTruthCollection,genParticleHandle) ;
  const reco::GenParticleCollection *genParticleCollection = genParticleHandle.product();

  reco::GenParticleCollection::const_iterator genPart;
  for(genPart=genParticleCollection->begin(); genPart!=genParticleCollection->end(); genPart++) {
    const reco::Candidate & cand = *genPart;

    if (abs(cand.pdgId())!=15) continue;

    int ndau=cand.numberOfDaughters();

    if (ndau<3) continue;

    for(int k = 0; k < ndau; ++ k) {
      TLorentzVector gen4mom;
      const Candidate * d = cand.daughter( k );
      int dauId = d->pdgId();
      if (abs(dauId)==13) {
	gen4mom.SetPxPyPzE(d->px(),d->py(),d->pz(),d->energy());
	TheGenMus.push_back(gen4mom);
      }
    }
  }

  if (TheGenMus.size()!=3) return ThreeMatches; //i.e false
  
  //see if they match reco muons
  bool RunMatch=true;

  std::vector<int> recoIndexes;
  std::vector<int> genIndexes;

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
      cout << "Gen Mu " << genIndexes[i] << " Matched with reco mu " << recoIndexes[i] << endl;
    }
  }

  if (genIndexes.size()==3) ThreeMatches=true;
  return ThreeMatches;
}




std::pair<bool,bool> Tau3MuAnalysis::isMu(const edm::Event& ev,const Track* p){
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
	  isGood=muon::isGoodMuon(*recoMu, muon::TMOneStationTight);
	  if (debug) cout << "3 muons" << endl;
	}	
      }
    }
  }
  return make_pair(ItIs,isGood);
}

int Tau3MuAnalysis::countTracksAround(const edm::Event& ev, const edm::EventSetup& iSetup,TLorentzVector* vec, double& dR, TransientVertex& sv ){


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

void Tau3MuAnalysis::findBestDimuon( const edm::EventSetup& iSetup,MuonCollection& muIn, MuonCollection& dimu, TransientVertex& dimuvtx, Vertex& primaryVertex){
  
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

    for (uint j=i+1; j<muIn.size(); ++j){

      reco::TrackRef intwo = muIn[j].innerTrack();

      if (!(intwo.isNonnull() && intwo.isAvailable())) continue;

      ndm++;

      if (OnlyOppositeCharge && muIn[i].charge()==muIn[j].charge()) continue;

      TLorentzVector DiMu=TLorentzVector(muIn[i].px()+ muIn[j].px() , muIn[i].py()+ muIn[j].py(), muIn[i].pz()+ muIn[j].pz(), muIn[i].energy()+ muIn[j].energy());

      if (DiMu.M()> diMuMassMax || DiMu.M() < diMuMassMin) continue;
      
      ndmm++;

      std::vector<TransientTrack> tt;

      tt.push_back(Builder->build(inone));
      tt.push_back(Builder->build(intwo));

      tmpvtx=avf.vertex(tt);

      if (!(tmpvtx.isValid())) continue;
      ndmv++;

      double vChi2 = tmpvtx.totalChiSquared();
      double vNDF = tmpvtx.degreesOfFreedom();

      double vProb(TMath::Prob(vChi2,(int)vNDF));

      if (vProb < Vp0) continue;
      ndmvprob++;

      if( vChi2/vNDF > diMuVtxChi2Max) continue;
      ndmchi++; 

      pair<double,double> lxytmp=Compute_Lxy_and_Significance(primaryVertex,tmpvtx,DiMu);

      if (debug) cout <<"vertex prob " <<vProb << endl;

      if (lxytmp.first < diMuLxyMin) continue;
      ndmlxy++;

      if (lxytmp.first/lxytmp.second < diMuLxySigMin) continue;
      ndmlxys++;

      if (vProb < tmpProb) continue;

      if (debug) cout << "DiMu found!!" << endl;
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


pair<double,double> Tau3MuAnalysis::Compute_Lxy_and_Significance(Vertex & primaryVertex, TransientVertex &SV, TLorentzVector& DiMuMom){
  
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

void Tau3MuAnalysis::vtx(std::vector<TransientTrack>& tt, GlobalPoint & p, GlobalError & ep){

  if (debug) cout << "finding the 2mu vertex" << endl;

  KalmanVertexFitter avf;
  TransientVertex tv=avf.vertex(tt);

  if (tv.isValid()){
    p=tv.position();
    ep=tv.positionError();
  }

}

std::pair<double,double> Tau3MuAnalysis::ComputeImpactParameterWrtPoint(TransientTrack& tt, Vertex& v){

  std::pair<double,double> d0valerr;

  std::pair<bool,Measurement1D> result = IPTools::absoluteImpactParameter3D(tt, v);
  double d0_val = result.second.value();
  double d0_err = result.second.error();
  d0valerr=make_pair(d0_val,d0_err);
  return d0valerr;
}



bool Tau3MuAnalysis::TriggerDecision(const edm::Event& ev){

  if (debug) cout << "Reading Trigger decision" << endl;

  bool passed=false;

  // check fired HLT paths
  edm::Handle<edm::TriggerResults> hltresults;
  edm::InputTag trigResultsTag("TriggerResults","",HLT_process);
  ev.getByLabel(trigResultsTag,hltresults);

  if (HLT_paths.size()==0){
    cout << "WARNING:No HLT Path Selected, the event will pass!!!" << endl;
    passed=true;
    return passed;
  }

  if (hltresults.isValid()) {
    const edm::TriggerNames TrigNames_ = ev.triggerNames(*hltresults);
    const int ntrigs = hltresults->size();
    for (int itr=0; itr<ntrigs; itr++){
      if (!hltresults->accept(itr)) continue;
      TString trigName=TrigNames_.triggerName(itr);
      if (debug) cout<<"Found HLT path "<< trigName<<endl;
      for (uint i=0; i<HLT_paths.size(); ++i){
	if (trigName==HLT_paths[i]) passed=true;
      }
      //      if (trigName=="HLT_Dimuon0_Omega_Phi_v3" || trigName=="HLT_Dimuon0_Omega_Phi_v4" || trigName=="HLT_Tau2Mu_RegPixTrack_v1") passed=true;
    }
  }
  else
    { 
      cout<<"Trigger results not found"<<endl;
    }

  if (passed) cout << "Passed!!!!!!" << endl;

  return passed;

}


// ------------ method called to for each event  ------------
void Tau3MuAnalysis::analyze(const edm::Event& ev, const edm::EventSetup& iSetup) {

  bool triggered=TriggerDecision(ev);

  Total++;

  if (triggered){

    Initialize_TreeVars();

    Triggered++;

    if (debug) cout << "--- new event ---" << endl;

    string theMuonLabel = "muons";
    string theVertexLabel = "offlinePrimaryVerticesWithBS";
    
    // get the muon container
    edm::Handle<MuonCollection> muons;
    ev.getByLabel(theMuonLabel,muons);
    
    // get the vertex collection
    edm::Handle< std::vector<reco::Vertex> > pvHandle;
    ev.getByLabel(theVertexLabel, pvHandle );
    
    // get the PV
    reco::Vertex primaryVertex;

    if(pvHandle.isValid()) {
      primaryVertex = pvHandle->at(0); 
    }
    
    // this is needed by the IPTools methods from the tracking group
    edm::ESHandle<TransientTrackBuilder> trackBuilder;
    iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder); 
    
    MuonCollection muPlus, muMinus, muSkim;
    
    // check the validity of the collection
    if(muons.isValid()){
      
      for (MuonCollection::const_iterator recoMu = muons->begin(); recoMu!=muons->end(); ++recoMu){ // loop over all muons
	
	double eta = (*recoMu).eta();
	double phi = (*recoMu).phi();
	double pt = (*recoMu).pt();
	double q=(*recoMu).charge();
	
	string muonType = "";
	if(recoMu->isGlobalMuon()) muonType = " Glb";
	if(recoMu->isStandAloneMuon()) muonType = muonType + " STA";
	if(recoMu->isTrackerMuon()) muonType = muonType + " Trk";
	
	if (debug) cout << "[MuonAnalysis] New Muon found:" << muonType << endl;
	if (debug) cout << "-- eta: " << eta << " phi: " << phi << " pt: " << pt << " q: " << q << endl;       
	
        if (recoMu->pt() < MinMuPt) continue;

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
    
    pair<double,double> d0track;
    pair<double,double> lxy2, lxy3;

    if (muSkim.size() < 2) return;

    findBestDimuon(iSetup, muSkim, BestDiMu, tv, primaryVertex);

    if (debug) cout << "dimuons size " << BestDiMu.size() << endl;

    if (BestDiMu.size()!=2) return;

    FoundDiMu++;

    bool TwoGood=false;
    bool Good1=false,Good2=false;
    int q1=0,q2=0,qtr=0;

    if ((muon::isGoodMuon(BestDiMu[0], muon::TMOneStationTight)) && (muon::isGoodMuon(BestDiMu[1], muon::TMOneStationTight))) TwoGood=true; 

    if (muon::isGoodMuon(BestDiMu[0], muon::TMOneStationTight)) Good1=true;    
    if (muon::isGoodMuon(BestDiMu[1], muon::TMOneStationTight)) Good2=true;

    Mu1Mom=TLorentzVector(BestDiMu[0].innerTrack()->px() , BestDiMu[0].innerTrack()->py(), BestDiMu[0].innerTrack()->pz(), BestDiMu[0].energy());
    Mu2Mom=TLorentzVector(BestDiMu[1].innerTrack()->px() , BestDiMu[1].innerTrack()->py(), BestDiMu[1].innerTrack()->pz(), BestDiMu[1].energy());

    q1=BestDiMu[0].charge();
    q2=BestDiMu[1].charge();

    DiMuMom=Mu1Mom+Mu2Mom;
     
    if (debug) cout << "dimuon mass " << DiMuMom.M() << endl;

    lxy2=Compute_Lxy_and_Significance(primaryVertex,tv,DiMuMom);

    double v2Chi2 = tv.totalChiSquared();
    double v2NDF  = tv.degreesOfFreedom();
    double v2Prob(TMath::Prob(v2Chi2,(int)v2NDF));

    bool isAlsoMu=false;
    bool isAlsoGoodMu=false;

    findBestPiCand(ev, iSetup, BestDiMu, tv3, primaryVertex,tv, d0track, pitrack, isAlsoMu, isAlsoGoodMu, qtr);

    if (pitrack.Px() !=0 ){

      Offline++;

      if (debug) cout << "track muon found" << endl;

      DiMuTrackMom = DiMuMom+pitrack;

      TLorentzVector TotMomArray[3]={Mu1Mom, Mu2Mom, pitrack};

      if (OnlyGenMatchInTree){
	bool isEventMatched=isMcMatched(ev,TotMomArray);
	if (!isEventMatched) return;
      }

      GenMatches++;

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

      _DiMu4Mom->SetPxPyPzE(DiMuMom.Px(),DiMuMom.Py(),DiMuMom.Pz(),DiMuMom.E());

      _DiMuPlusTrack4Mom->SetPxPyPzE(DiMuTrackMom.Px(),DiMuTrackMom.Py(),DiMuTrackMom.Pz(),DiMuTrackMom.E());

      _Mu2_4Mom->SetPxPyPzE(Mu2Mom.Px(),Mu2Mom.Py(),Mu2Mom.Pz(),Mu2Mom.E());
      _Mu1_4Mom->SetPxPyPzE(Mu1Mom.Px(),Mu1Mom.Py(),Mu1Mom.Pz(),Mu1Mom.E());
      _MuTrack_4Mom->SetPxPyPzE(pitrack.Px(),pitrack.Py(),pitrack.Pz(),pitrack.E());
      
      _M3=DiMuTrackMom.M();
      _M2=DiMuMom.M(); 
      _PtT=pitrack.Pt();
      _dRdiMuT=pitrack.DeltaR(DiMuMom);

      _Mu1Q=q1;
      _Mu2Q=q2;
      _Mu3Q=qtr;
      
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
      _d0TSig=d0track.first/d0track.second;
      
      _TrackIsMu=isAlsoMu;
      _TrackIsGoodMu=isAlsoGoodMu;

      _NTracksInDr=NDr;
      _Mu1IsGood=Good1;
      _Mu2IsGood=Good2;

      _IsMu1InPV =InPV1;
      _IsMu2InPV=InPV2;
      _IsMu3InPV=InPV3;

      ExTree->Fill();

      if (debug) cout << "Tree filled" << endl;
    }    
  }
}

void Tau3MuAnalysis::Initialize_TreeVars(){

  _DiMu4Mom->SetPxPyPzE(0.,0.,0.,0.);
  _DiMuPlusTrack4Mom->SetPxPyPzE(0.,0.,0.,0.);

  _Mu1_4Mom->SetPxPyPzE(0.,0.,0.,0.);
  _Mu2_4Mom->SetPxPyPzE(0.,0.,0.,0.);

  _MuTrack_4Mom->SetPxPyPzE(0.,0.,0.,0.);

  _Mu1Q=0;_Mu2Q=0;_Mu3Q=0;

  _PV->SetXYZ(0.,0.,0.);
  _SV->SetXYZ(0.,0.,0.);
  _SVT->SetXYZ(0.,0.,0.);


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
  _d0TSig=-99;

  _NTracksInDr=-1;

  _TrackIsMu=false;
  _Mu1IsGood=false;
  _Mu2IsGood=false;

  _TrackIsGoodMu=false;

  _IsMu1InPV=false;
  _IsMu2InPV=false;
  _IsMu3InPV=false;
}


// ------------ method called once each job just before starting event loop  ------------
void Tau3MuAnalysis::beginJob() {

  thefile = new TFile (FileName.c_str(), "RECREATE" );
  thefile->cd();

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

  ExTree->Branch("Mu1Q",&_Mu1Q   , "_Mu1Q/I");
  ExTree->Branch("Mu2Q",&_Mu2Q   , "_Mu2Q/I");
  ExTree->Branch("Mu3Q",&_Mu3Q   , "_Mu3Q/I");

  ExTree->Branch("NTracksInDr", &_NTracksInDr , "_NTracksInDr/I");
  
  ExTree->Branch("SVchi",&_SVchi   ,"_SVchi/D"); 
  ExTree->Branch("SVprob",&_SVprob   ,"_SVprob/D"); 
  ExTree->Branch("SVTchi",&_SVTchi   ,"_SVTchi/D"); 
  ExTree->Branch("SVTprob",&_SVTprob   ,"_SVTprob/D"); 

  ExTree->Branch("MinvDiMuT",&_M3   ,"_M3/D");
  ExTree->Branch("MinvDiMu",&_M2   ,"_M2/D");
  ExTree->Branch("PtTrack",&_PtT   ,"_PtT/D");
  ExTree->Branch("dRTrack-DiMu",&_dRdiMuT   ,"_dRdiMuT/D");

  ExTree->Branch("Lxy",&_Lxy   ,"_Lxy/D");
  ExTree->Branch("LxySig",&_LxySig   ,"_LxySig/D");
  ExTree->Branch("LxyT",&_LxyT   ,"_LxyT/D");
  ExTree->Branch("LxyTSig",&_LxyTSig   ,"_LxyTSig/D");
  ExTree->Branch("d0T",&_d0T   ,"_d0T/D");
  ExTree->Branch("d0TSig",&_d0TSig   ,"_d0TSig/D");

  ExTree->Branch("Mu1IsGood",&_Mu1IsGood   ,"_Mu1IsGood/B");
  ExTree->Branch("Mu2IsGood",&_Mu2IsGood   ,"_Mu2IsGood/B");
  ExTree->Branch("TrackIsGoodMu",&_TrackIsGoodMu   ,"_TrackIsGoodMu/B");
  ExTree->Branch("TrackIsMu",&_TrackIsMu ,"_TrackIsMu/B");

  ExTree->Branch("IsMu1InPV",&_IsMu1InPV ,"_IsMu1InPV/B");
  ExTree->Branch("IsMu2InPV",&_IsMu2InPV ,"_IsMu2InPV/B");
  ExTree->Branch("IsMu3InPV",&_IsMu3InPV ,"_IsMu3InPV/B");
 
  hpt= new TH1F("TrackPT","Track pT",250,0,50);
  hptMu= new TH1F("TrackMuPT","Track with MuId pT",250,0,50);

  hDiMuPt=new TH1F("hDiMuPt","DiMuonPt",250,0.,50);

  hDiMuInvMass= new TH1F("hDiMuInvMass","DiMuon Inv. Mass",100,diMuMassMin,diMuMassMax);
  hGoodDiMuInvMass= new TH1F("hGoodDiMuInvMass","Good DiMuon Inv. Mass",100,diMuMassMin,diMuMassMax);

  hTriMuInvMass= new TH1F("hTriMuInvMass","TriMuon Inv. Mass",100,1.6,2.3);

  hGoodDiMuTrackInvMass= new TH1F("hGoodDiMuTrackInvMass","Good DiMuon+Track Inv. Mass",100,diMuTrackMassMin,diMuTrackMassMax);
  hDiMuTrackInvMass= new TH1F("hDiMuTrackInvMass","DiMuon+Track Inv. Mass",100,diMuTrackMassMin,diMuTrackMassMax);

 
  if (OnlyGenMatchInTree)  htotEff=new TH1F("TotEff","Tot Eff",5,-0.5,4.5);

  if (!OnlyGenMatchInTree){
    htotEff=new TH1F("TotEff","Tot Eff",4,-0.5,3.5);
    hDiMuEff=new TH1F("DiMuEff","DiMuEff",8,-0.5,7.5);
    hTrackEff=new TH1F("TrackEff","TrackEff",11,-0.5,10.5);
  }

  hpt->Sumw2();
  hptMu->Sumw2();
  hDiMuPt->Sumw2();

  hDiMuInvMass->Sumw2();
  hGoodDiMuInvMass->Sumw2();

  hDiMuTrackInvMass->Sumw2();
  hGoodDiMuTrackInvMass->Sumw2();

}


// ------------ method called nce each job just after ending the event loop  ------------
void 
Tau3MuAnalysis::endJob() {

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

  if (OnlyGenMatchInTree){
    htotEff->SetBinContent(5, GenMatches/Total);
    htotEff->GetXaxis()->SetBinLabel(5,"GenMatched");
  }

  if (!OnlyGenMatchInTree){
  //Mu Eff
    sprintf(title,"TotDiMu= %5.2f  PassedDiMu= %5.2f",ndm,FoundDiMu);
    hDiMuEff->SetTitle(title);

    hDiMuEff->SetBinContent(1,1);
    hDiMuEff->GetXaxis()->SetBinLabel(1,"tot");

    if(ndm!=0) hDiMuEff->SetBinContent(2,ndmm/ndm);
    sprintf(title,"InvMassIn(%5.2f,%5.2f)",diMuMassMin, diMuMassMax);
    hDiMuEff->GetXaxis()->SetBinLabel(2,title);
    
    if(ndmm!=0) hDiMuEff->SetBinContent(3,ndmv/ndm);
    hDiMuEff->GetXaxis()->SetBinLabel(3,"Vertex Ok");
    
    if(ndmv!=0) hDiMuEff->SetBinContent(4,ndmvprob/ndm);
    sprintf(title,"Vprob > %5.2f ", diMuVprobMin);
    hDiMuEff->GetXaxis()->SetBinLabel(4,title);
    
    if(ndmvprob!=0) hDiMuEff->SetBinContent(5,ndmchi/ndm);
    sprintf(title,"ch2Vtx < %5.2f",diMuVtxChi2Max);
    hDiMuEff->GetXaxis()->SetBinLabel(5,title);
    
    if(ndmchi!=0) hDiMuEff->SetBinContent(6,ndmlxy/ndm);
    sprintf(title,"Lxy > %5.2f",diMuLxyMin);
    hDiMuEff->GetXaxis()->SetBinLabel(6,title);
    
    if(ndmlxy!=0) hDiMuEff->SetBinContent(7,ndmlxys/ndm);
    sprintf(title,"LxySig > %5.2f",diMuLxySigMin);
    hDiMuEff->GetXaxis()->SetBinLabel(7,title);
    
    if(ndmlxys!=0) hDiMuEff->SetBinContent(8,FoundDiMu/ndm);
    hDiMuEff->GetXaxis()->SetBinLabel(8,"Selected");
    
    //Tracks eff
    sprintf(title,"TotTracks= %5.2f  PassedTracks= %5.2f",nt,Offline);
    
    hTrackEff->SetTitle(title); 
    hTrackEff->SetBinContent(1,1);
    hTrackEff->GetXaxis()->SetBinLabel(1,"tot");
    
    if(nt!=0) hTrackEff->SetBinContent(2,ntq/nt);
    hTrackEff->GetXaxis()->SetBinLabel(2,"Quality Ok");
    
    if(ntq!=0) hTrackEff->SetBinContent(3,ntm/nt);
    sprintf(title,"InvMassIn(%5.2f,%5.2f)",diMuTrackMassMin,diMuTrackMassMax);
    hTrackEff->GetXaxis()->SetBinLabel(3,title);
    
    if(ntm!=0) hTrackEff->SetBinContent(4,ntd0/nt);
    sprintf(title,"d0 wrt SV < %5.2f",Trackd0Max);
    hTrackEff->GetXaxis()->SetBinLabel(4,title);
    
    if(ntd0!=0) hTrackEff->SetBinContent(5,ntd0s/nt);
    sprintf(title,"d0sig  > %5.2f",Trackd0SigMin);
    hTrackEff->GetXaxis()->SetBinLabel(5,title);
    
    if(ntd0s!=0) hTrackEff->SetBinContent(6,ntv/nt);
    hTrackEff->GetXaxis()->SetBinLabel(6,"Vertex Ok");
    
    if(ntv!=0) hTrackEff->SetBinContent(7,ntvprob/nt);
    sprintf(title,"Vprob > %5.2f ", diMuTrackVprobMin);
    hTrackEff->GetXaxis()->SetBinLabel(7,title);
    
    if(ntvprob!=0) hTrackEff->SetBinContent(8,ntchi/nt);
    sprintf(title,"ch2Vtx < %5.2f",diMuTrackVtxChi2Max);
    hTrackEff->GetXaxis()->SetBinLabel(8,title);
    
    if(ntchi!=0) hTrackEff->SetBinContent(9,ntlxy/nt);
    sprintf(title,"Lxy > %5.2f",diMuTrackLxyMin);
    hTrackEff->GetXaxis()->SetBinLabel(9,title);
    
    if(ntlxy!=0) hTrackEff->SetBinContent(10,ntlxys/nt);
    sprintf(title,"LxySig > %5.2f",diMuTrackLxySigMin);
    hTrackEff->GetXaxis()->SetBinLabel(10,title);
    
    if(ntlxys!=0) hTrackEff->SetBinContent(11,Offline/nt);
    hTrackEff->GetXaxis()->SetBinLabel(11,"Selected");
    
  }
  
  thefile->cd();

  //some control histos
  hpt->Write();
  hptMu->Write();
  hDiMuPt->Write();
  htotEff->Write();

  if (!OnlyGenMatchInTree){
    hDiMuEff->Write();
    hTrackEff->Write();
  }

  hDiMuInvMass->Write();
  hGoodDiMuInvMass->Write();
  hDiMuTrackInvMass->Write();
  hGoodDiMuTrackInvMass->Write();
  hTriMuInvMass->Write();

  thefile->Write();

  //thefile->Close();

  delete hpt;
  delete hptMu;
  delete hDiMuPt;
  delete htotEff;
  if (!OnlyGenMatchInTree){
    delete hDiMuEff;
    delete hTrackEff;
  }
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

  thefile->Close();
  delete thefile;
  
  //ExTree->Write();
  //hDiMuTrackInvMass->Write();
  //thefile.

  std::cout << "Total " << Total << std::endl;
  std::cout << "Triggered " << Triggered << std::endl;
  std::cout << "DiMu Found " << FoundDiMu << std::endl;
  std::cout << "DiMu+Track Found " << Offline << std::endl;
  if (OnlyGenMatchInTree) std::cout << "Events MC Matched " << GenMatches  << std::endl;
}

#include "FWCore/Framework/interface/MakerMacros.h"  
DEFINE_FWK_MODULE( Tau3MuAnalysis );
