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
  virtual void vtx(std::vector<TransientTrack>&, GlobalPoint &, GlobalError &);
  virtual pair<double,double> Compute_Lxy_and_Significance(Vertex &, TransientVertex &, TLorentzVector&);
  virtual void findBestDimuon( const edm::EventSetup&, MuonCollection&, MuonCollection&, TransientVertex&, Vertex&);
  virtual void findBestPiCand(const edm::Event&, const edm::EventSetup&, MuonCollection&, TransientVertex&, Vertex&, TLorentzVector&, bool&);
  virtual bool TriggerDecision(const edm::Event&);
  virtual bool isMu(const edm::Event&, const Track*);
  virtual int countTracksAround(const edm::Event&, TLorentzVector*, double&);

  TH1F* hDiMuInvMass,* hGoodDiMuInvMass ;
  TH1F* hDiMuTrackInvMass,* hGoodDiMuTrackInvMass ;
  TH1F* hDiMuPHITrackInvMass,*hDiMuSBTrackInvMass;
  TH1F* hpt, *hptMu;
  TH1F* hchi2,*hchi3, *hlxy2, *hlxy3, *hvprob2, *hvprob3, *hlxys2, *hlxys3,*hdistv2v3;
  TH1F* hMaxDistance;
  TH2F* hNtracksVsDR;
  double Total, Triggered, Offline;
  double diMuMassMin, diMuMassMax, diMuLxyMin,diMuLxySigMin,diMuVtxChi2, diMuVprobMin;
  double diMuTrackMassMin, diMuTrackMassMax, diMuTrackLxyMin,diMuTrackLxySigMin,diMuTrackVtxChi2,diMuTrackVprobMin;
  double MinTrackPt, MinMuPt;
  double TrackMass;

  std::vector<string> HLT_paths;
  std::string HLT_process;

  bool OnlyOppositeCharge;
  bool debug;
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
  Offline=0;

  diMuMassMin= cfg.getParameter<double> ("DiMuMassMin"); 
  diMuMassMax= cfg.getParameter<double> ("DiMuMassMax");  
  diMuLxyMin = cfg.getParameter<double> ("DiMuLxyMin"); 
  diMuLxySigMin = cfg.getParameter<double> ("DiMuLxySigMin");
  diMuVtxChi2= cfg.getParameter<double> ("DiMuVtxChi2Max");
  diMuVprobMin= cfg.getParameter<double> ("DiMuVprobMin");
  
  diMuTrackMassMin= cfg.getParameter<double> ("DiMuTrackMassMin"); 
  diMuTrackMassMax= cfg.getParameter<double> ("DiMuTrackMassMax"); 
  diMuTrackLxyMin = cfg.getParameter<double> ("DiMuTrackLxyMin");
  diMuTrackLxySigMin = cfg.getParameter<double> ("DiMuTrackLxySigMin");
  diMuTrackVtxChi2= cfg.getParameter<double> ("DiMuTrackVtxChi2Max");
  diMuTrackVprobMin= cfg.getParameter<double> ("DiMuTrackVprobMin");

  MinMuPt=cfg.getParameter<double> ("MuPTCut");
  MinTrackPt=cfg.getParameter<double> ("TrackPTCut");

  HLT_paths = cfg.getParameter<std::vector<string> > ("HLT_paths");
  HLT_process = cfg.getParameter<std::string> ("HLT_process");

  OnlyOppositeCharge= cfg.getParameter<bool> ("OnlyOppositeChargeMuons");
  TrackMass= cfg.getParameter<double> ("GuessForTrackMass");

  debug=cfg.getParameter<bool> ("Debug");

}

Tau3MuAnalysis::~Tau3MuAnalysis() {}

//
// member functions
//
void Tau3MuAnalysis::findBestPiCand(const edm::Event& ev, const edm::EventSetup& iSetup, MuonCollection& dimu, TransientVertex& tv, Vertex& primaryVertex, TLorentzVector& pi, bool & isMuon){

  if (debug) cout << "Looking for the pi track" << endl;

  edm::ESHandle<TransientTrackBuilder> Builder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", Builder);

  Handle<TrackCollection> tracks;
  ev.getByLabel("generalTracks", tracks);

  KalmanVertexFitter avf;

  float tmpProb=diMuTrackVprobMin;

  for(TrackCollection::const_iterator it = tracks->begin();it != tracks->end(); ++it){

    if ((it->pt()==dimu[0].innerTrack()->pt() && it->eta()==dimu[0].innerTrack()->eta()) || (it->pt()==dimu[1].innerTrack()->pt() && it->eta()==dimu[1].innerTrack()->eta())) continue;
    if (dimu[0].charge()==dimu[1].charge() && it->charge()==dimu[0].charge()) continue; //impossible to have a particle with charge +/- 3

    if (!(it->quality(TrackBase::highPurity)) || it->pt()< MinTrackPt) continue;

    TLorentzVector m1=TLorentzVector(dimu[0].px(),dimu[0].py(),dimu[0].pz(),dimu[0].energy());
    TLorentzVector m2=TLorentzVector(dimu[1].px(),dimu[1].py(),dimu[1].pz(),dimu[1].energy());
    TLorentzVector p=TLorentzVector(it->px(),it->py(),it->pz(),sqrt(TrackMass*TrackMass+it->p()*it->p()));
    TLorentzVector tot=m1+m2+p;

    if (tot.M() < diMuTrackMassMin || tot.M()> diMuTrackMassMax) continue;

    vector<TransientTrack> tt;
    TransientVertex tmpvtx;

    tt.push_back(Builder->build(dimu[0].innerTrack()));
    tt.push_back(Builder->build(dimu[1].innerTrack()));
    tt.push_back(Builder->build(*it));

    tmpvtx=avf.vertex(tt);
    
    if (!tmpvtx.isValid()) continue;
    
    float vChi2 = tmpvtx.totalChiSquared();
    float vNDF  = tmpvtx.degreesOfFreedom();
    float vProb(TMath::Prob(vChi2,(int)vNDF));

    pair<double,double> lxytmp=Compute_Lxy_and_Significance(primaryVertex,tmpvtx,tot);
    
    if (vProb>tmpProb && lxytmp.first > diMuTrackLxyMin && lxytmp.first/lxytmp.second > diMuTrackLxySigMin && vChi2/vNDF < diMuTrackVtxChi2 ){
      tmpProb=vProb;
      pi=p;
      isMuon=isMu(ev,&(*it));
      tv=tmpvtx;
    }      
  }
}


bool Tau3MuAnalysis::isMu(const edm::Event& ev,const Track* p){
  bool ItIs=false;
  edm::Handle<MuonCollection> muons;
  ev.getByLabel("muons",muons);
  for (MuonCollection::const_iterator recoMu = muons->begin();
       recoMu!=muons->end(); ++recoMu){
    if(recoMu->isGlobalMuon() || recoMu->isTrackerMuon()){
      reco::TrackRef inp = recoMu->innerTrack();
      if (inp.isNonnull() && inp.isAvailable()){
	if (inp->pt()==p->pt() && inp->eta()==p->eta()) ItIs=true;

      }
    }
  }
  return ItIs;
}

int Tau3MuAnalysis::countTracksAround(const edm::Event& ev, TLorentzVector* vec, double& dR){

  int N=0;
  Handle<TrackCollection> tracks;
  ev.getByLabel("generalTracks", tracks);
  TLorentzVector TotMom= vec[0]+vec[1]+vec[2];

  for(TrackCollection::const_iterator it = tracks->begin();it != tracks->end(); ++it){
    bool isIn=false;
    TLorentzVector tvec=TLorentzVector(it->px(),it->py(),it->pz(),sqrt(0.1396*0.1396+it->p()*it->p()));
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

  float tmpProb=diMuVprobMin;  

  KalmanVertexFitter avf;

  for(uint i=0; i < (muIn.size()-1); ++i){

    TransientVertex tmpvtx;

    reco::TrackRef inone = muIn[i].innerTrack();

    if (!(inone.isNonnull() && inone.isAvailable())) continue;

    for (uint j=i+1; j<muIn.size(); ++j){

      reco::TrackRef intwo = muIn[j].innerTrack();

      if (!(intwo.isNonnull() && intwo.isAvailable())) continue;

      if (OnlyOppositeCharge && muIn[i].charge()==muIn[j].charge()) continue;

      std::vector<TransientTrack> tt;

      tt.push_back(Builder->build(inone));
      tt.push_back(Builder->build(intwo));

      tmpvtx=avf.vertex(tt);

      if (!(tmpvtx.isValid())) continue;

      double vChi2 = tmpvtx.totalChiSquared();
      float vNDF = tmpvtx.degreesOfFreedom();

      float vProb(TMath::Prob(vChi2,(int)vNDF));

      TLorentzVector DiMu=TLorentzVector(muIn[i].px()+ muIn[j].px() , muIn[i].py()+ muIn[j].py(), muIn[i].pz()+ muIn[j].pz(), muIn[i].energy()+ muIn[j].energy());

      if (DiMu.M()> diMuMassMax || DiMu.M() < diMuMassMin) continue;

      pair<double,double> lxytmp=Compute_Lxy_and_Significance(primaryVertex,tmpvtx,DiMu);

      if (debug) cout <<"vertex prob " <<vProb << endl;

      if (vProb>tmpProb && lxytmp.first > diMuLxyMin && lxytmp.first/lxytmp.second > diMuLxySigMin  && vChi2/vNDF < diMuVtxChi2){
	if (debug) cout << "DiMu found!!" << endl;
	tmpProb=vProb;
	one=i;
	two=j;
	dimuvtx=tmpvtx;
      }      
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
    
    pair<double,double> lxy2, lxy3;

    if (muSkim.size() < 2) return;

    findBestDimuon(iSetup, muSkim, BestDiMu, tv, primaryVertex);

    if (debug) cout << "dimuons size " << BestDiMu.size() << endl;

    if (BestDiMu.size()!=2) return;

    bool TwoGood=false;

    if ((muon::isGoodMuon(BestDiMu[0], muon::TMOneStationTight)) && (muon::isGoodMuon(BestDiMu[1], muon::TMOneStationTight))) TwoGood=true; 
      
    Mu1Mom=TLorentzVector(BestDiMu[0].px() , BestDiMu[0].py(), BestDiMu[0].pz(), BestDiMu[0].energy());
    Mu2Mom=TLorentzVector(BestDiMu[1].px() , BestDiMu[1].py(), BestDiMu[1].pz(), BestDiMu[1].energy());

    DiMuMom=Mu1Mom+Mu2Mom;
      //=TLorentzVector(BestDiMu[0].px()+ BestDiMu[1].px() , BestDiMu[0].py()+ BestDiMu[1].py(), BestDiMu[0].pz()+ BestDiMu[1].pz(), BestDiMu[0].energy()+ BestDiMu[1].energy());
   
    if (debug) cout << "dimuon mass " << DiMuMom.M() << endl;

    hDiMuInvMass->Fill(DiMuMom.M());

    lxy2=Compute_Lxy_and_Significance(primaryVertex,tv,DiMuMom);

    float v2Chi2 = tv.totalChiSquared();
    float v2NDF  = tv.degreesOfFreedom();
    float v2Prob(TMath::Prob(v2Chi2,(int)v2NDF));

    //fill some dimuon histos
    hchi2->Fill(v2Chi2);
    hlxy2->Fill(lxy2.first);
    hlxys2->Fill(lxy2.first/lxy2.second);
    hvprob2->Fill(v2Prob);

    if (TwoGood)  hGoodDiMuInvMass->Fill(DiMuMom.M());

    bool isAlsoMu=false;

    findBestPiCand(ev, iSetup, BestDiMu, tv3, primaryVertex, pitrack, isAlsoMu);

    if (pitrack.Px() !=0){

      double Dr1,Dr2;
      Dr1=pitrack.DeltaR(Mu1Mom);
      Dr2=pitrack.DeltaR(Mu2Mom);
      if (Dr1>Dr2) hMaxDistance->Fill(Dr1);
      else hMaxDistance->Fill(Dr2);

      DiMuTrackMom = DiMuMom+pitrack;

      TLorentzVector TotMomArray[3]={Mu1Mom, Mu2Mom, pitrack};

      double drs[]={0.1,0.2,0.3,0.4,0.5,0.6};
      int sizer=sizeof(drs)/sizeof(drs[0]);

      for (int i=0; i< sizer; ++i){
	int Ntracks = countTracksAround(ev,TotMomArray,drs[i]);
	hNtracksVsDR->Fill(drs[i],Ntracks);
      }

      lxy3=Compute_Lxy_and_Significance(primaryVertex,tv3,DiMuTrackMom);

      float v3Chi2 = tv3.totalChiSquared();
      float v3NDF  = tv3.degreesOfFreedom();
      float v3Prob(TMath::Prob(v3Chi2,(int)v3NDF));

      //fill some dimuon histos
      hchi3->Fill(v3Chi2);
      hlxy3->Fill(lxy3.first);
      hlxys3->Fill(lxy3.first/lxy3.second);
      hvprob3->Fill(v3Prob);      
      hdistv2v3->Fill(abs(lxy2.first-lxy3.first));

      Offline++;
      hDiMuTrackInvMass->Fill(DiMuTrackMom.M());
      
      if (TwoGood)  {
	hGoodDiMuTrackInvMass->Fill(DiMuTrackMom.M());
	if (DiMuMom.M()>1 && DiMuMom.M()<1.05) {
	  hDiMuPHITrackInvMass->Fill(DiMuTrackMom.M());
	  hpt->Fill(DiMuTrackMom.Pt());
	  if (isAlsoMu)hptMu->Fill(DiMuTrackMom.Pt());
	}
	else hDiMuSBTrackInvMass->Fill(DiMuTrackMom.M());
      }
      if (debug) cout << "total mass " << DiMuTrackMom.M() << endl;
    }    
  }
}


// ------------ method called once each job just before starting event loop  ------------
void Tau3MuAnalysis::beginJob() {

  edm::Service<TFileService> fs;

  hpt= fs->make<TH1F>("TrackPT","Track pT",50,0,10);
  hptMu= fs->make<TH1F>("TrackMuPT","Track with MuId pT",50,0,10);

  hDiMuInvMass= fs->make<TH1F>("hDiMuInvMass","DiMuon Inv. Mass",100,0.,2);
  hGoodDiMuInvMass= fs->make<TH1F>("hGoodDiMuInvMass","Good DiMuon Inv. Mass",100,0.,2);

  hGoodDiMuTrackInvMass= fs->make<TH1F>("hGoodDiMuTrackInvMass","Good DiMuon+Track Inv. Mass",60,1.6,2.3);
  hDiMuTrackInvMass= fs->make<TH1F>("hDiMuTrackInvMass","DiMuon+Track Inv. Mass",60,1.6,2.3);

  hDiMuPHITrackInvMass= fs->make<TH1F>("hDiMuPHITrackInvMass","DiMuonPHI+Track Inv. Mass",60,1.7,2.3);
  hDiMuSBTrackInvMass= fs->make<TH1F>("hDiMuSBTrackInvMass","DiMuonSB+Track Inv. Mass",60,1.7,2.3);

  hchi2= fs->make<TH1F>("chi2DiMu","chi2 DiMu vtx",100,0,10);
  hchi3= fs->make<TH1F>("chi2DiMuTrack","chi2 DiMu+Track vtx",100,0,10);
  hlxy2= fs->make<TH1F>("lxyDiMu","lxy DiMu",100,-0.2,0.5);
  hlxy3 =fs->make<TH1F>("lxyDiMuT","lxy DiMu+Track",100,-0.2,0.5);
  hvprob2= fs->make<TH1F>("VpDiMu","Vprob DiMu",100,0,1);
  hvprob3 =fs->make<TH1F>("VpDiMuT","Vprob DiMu+Track",100,0,1);
  hlxys2 =fs->make<TH1F>("lxySDiMu","lxy Sig. DiMu",200,0,20);
  hlxys3=fs->make<TH1F>("lxySDiMuT","lxy Sig. DiMu+Track",200,0,20);
  hdistv2v3=fs->make<TH1F>("LxyDiff","lxy(DiMu)-lxy(DiMu+Track)",200,-0.5,0.5);
  hMaxDistance=fs->make<TH1F>("MaxDist","Max dR Mu-Track",100,0,0.2);
  hNtracksVsDR=fs->make<TH2F>("NtracksInDr","Number of tracks vs DR wrt DiMu+Track 4Mom",7,0.1,0.7,51,0,50);

  hpt->Sumw2();
  hptMu->Sumw2();

  hDiMuPHITrackInvMass->Sumw2();
  hDiMuSBTrackInvMass->Sumw2();

  hDiMuInvMass->Sumw2();
  hGoodDiMuInvMass->Sumw2();

  hDiMuTrackInvMass->Sumw2();
  hGoodDiMuTrackInvMass->Sumw2();

}


// ------------ method called nce each job just after ending the event loop  ------------
void 
Tau3MuAnalysis::endJob() {
  std::cout << "Total " << Total << std::endl;
  std::cout << "Triggered " << Triggered << std::endl;
  std::cout << "Offline " << Offline << std::endl; 
}

#include "FWCore/Framework/interface/MakerMacros.h"  
DEFINE_FWK_MODULE( Tau3MuAnalysis );
