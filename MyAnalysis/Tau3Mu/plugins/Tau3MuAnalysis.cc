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
  virtual void findBestDimuon( const edm::EventSetup&, MuonCollection&, MuonCollection&, MuonCollection&, TransientVertex&, Vertex&, double&, double&);
  virtual void findBestPiCand(const edm::Event&, const edm::EventSetup&, MuonCollection&, TransientVertex&, TLorentzVector&, bool&, double&, double&);
  virtual bool TriggerDecision(const edm::Event&);
  virtual bool isMu(const edm::Event&, const Track*);

  TH1F* hDiMuInvMass,* hGoodDiMuInvMass ;
  TH1F* hDiMuTrackInvMass,* hGoodDiMuTrackInvMass ;
  TH1F* hDiMuPHITrackInvMass,*hDiMuSBTrackInvMass;
  TH1F* hpt, *hptMu;
  double Total, Triggered, Offline;
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


Tau3MuAnalysis::Tau3MuAnalysis(const edm::ParameterSet& iConfig) {
  Total=0;
  Triggered=0;
  Offline=0;

}

Tau3MuAnalysis::~Tau3MuAnalysis() {}


//
// member functions
//
void Tau3MuAnalysis::findBestPiCand(const edm::Event& ev, const edm::EventSetup& iSetup, MuonCollection& dimu, TransientVertex& tv, TLorentzVector& pi, bool & isMuon, double& massmin, double& massmax){

  cout << "Looking for the pi track" << endl;

  edm::ESHandle<TransientTrackBuilder> Builder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", Builder);

  Handle<TrackCollection> tracks;
  ev.getByLabel("generalTracks", tracks);

  KalmanVertexFitter avf;

  float tmpProb=0.;

  for(TrackCollection::const_iterator it = tracks->begin();it != tracks->end(); ++it){

    if ((it->pt()==dimu[0].innerTrack()->pt() && it->eta()==dimu[0].innerTrack()->eta()) || (it->pt()==dimu[1].innerTrack()->pt() && it->eta()==dimu[1].innerTrack()->eta())) continue;

    if (!(it->quality(TrackBase::highPurity)) || it->pt()< 0.5) continue;

    TLorentzVector m1=TLorentzVector(dimu[0].px(),dimu[0].py(),dimu[0].pz(),dimu[0].energy());
    TLorentzVector m2=TLorentzVector(dimu[1].px(),dimu[1].py(),dimu[1].pz(),dimu[1].energy());
    TLorentzVector p=TLorentzVector(it->px(),it->py(),it->pz(),sqrt(0.1396*0.1396+it->p()*it->p()));
    TLorentzVector tot=m1+m2+p;

    if (tot.M() < massmin || tot.M()> massmax) continue;

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

    //cout << "chi " << vChi2 << " ndof " << vNDF <<" Vprob " << vProb <<endl;

    if (vProb>tmpProb  && vChi2/vNDF < 10){
      tmpProb=vProb;
      pi=p;
      isMuon=isMu(ev,&(*it));
	//TLorentzVector(it->px(),it->py(),it->pz(),sqrt(0.1396*0.1396+it->p()*it->p()));
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



void Tau3MuAnalysis::findBestDimuon( const edm::EventSetup& iSetup,MuonCollection& mup, MuonCollection& mum, MuonCollection& dimu, TransientVertex& dimuvtx, Vertex& primaryVertex, double& massmin, double& massmax){
  
  cout << "Finding the dimuon candidate" << endl;

  edm::ESHandle<TransientTrackBuilder> Builder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", Builder); 

  int plus=1000, minus=1000;
  float tmpProb=0.005;  

  KalmanVertexFitter avf;

  for(uint i=0; i < mup.size(); ++i){

    TransientVertex tmpvtx;

    reco::TrackRef inp = mup[i].innerTrack();

    if (!(inp.isNonnull() && inp.isAvailable())) continue;

    for (uint j=0; j<mum.size(); ++j){

      reco::TrackRef inm = mum[j].innerTrack();

      if (!(inm.isNonnull() && inm.isAvailable())) continue;

      std::vector<TransientTrack> tt;

      tt.push_back(Builder->build(inm));
      tt.push_back(Builder->build(inp));

      tmpvtx=avf.vertex(tt);

      if (!(tmpvtx.isValid())) continue;

      double vChi2 = tmpvtx.totalChiSquared();
      float vNDF = tmpvtx.degreesOfFreedom();

      float vProb(TMath::Prob(vChi2,(int)vNDF));

      TLorentzVector DiMu=TLorentzVector(mup[i].px()+ mum[j].px() , mup[i].py()+ mum[j].py(), mup[i].pz()+ mum[j].pz(), mup[i].energy()+ mum[j].energy());

      if (DiMu.M()> massmax || DiMu.M() < massmin) continue;

      pair<double,double> lxytmp=Compute_Lxy_and_Significance(primaryVertex,tmpvtx,DiMu);

      // cout <<"vertex prob " <<vProb << endl;

      if (vProb>tmpProb && lxytmp.first/lxytmp.second > 2 && vChi2/vNDF < 10){

	cout << "DiMu found!!" << endl;
	tmpProb=vProb;
	plus=i;
	minus=j;
	dimuvtx=tmpvtx;
      }      
    }
  }

  if (plus!=1000){
    dimu.push_back(mup[plus]);
    dimu.push_back(mum[minus]);
  }
}


pair<double,double> Tau3MuAnalysis::Compute_Lxy_and_Significance(Vertex & primaryVertex, TransientVertex &SV, TLorentzVector& DiMuMom){
  
  cout << "computing lxy and error" << endl;

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

  cout << "finding the 2mu vertex" << endl;

  KalmanVertexFitter avf;
  TransientVertex tv=avf.vertex(tt);

  if (tv.isValid()){
    p=tv.position();
    ep=tv.positionError();
  }

}


bool Tau3MuAnalysis::TriggerDecision(const edm::Event& ev){

  cout << "Reading Trigger decision" << endl;

  bool passed=false;

  // check fired HLT paths
  edm::Handle<edm::TriggerResults> hltresults;
  edm::InputTag trigResultsTag("TriggerResults","","HLT");
  ev.getByLabel(trigResultsTag,hltresults);
  //ev.getByLabel("TriggerResults", hltresults);

  if (hltresults.isValid()) {
    const edm::TriggerNames TrigNames_ = ev.triggerNames(*hltresults);
    const int ntrigs = hltresults->size();
    for (int itr=0; itr<ntrigs; itr++){
      if (!hltresults->accept(itr)) continue;
      TString trigName=TrigNames_.triggerName(itr);
      // cout<<"Found HLT path "<< trigName<<endl;
      if (trigName=="HLT_Dimuon0_Omega_Phi_v3" || trigName=="HLT_Dimuon0_Omega_Phi_v4" ) passed=true;
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

  if (triggered || 1){

    Triggered++;

    cout << "--- new event ---" << endl;

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
      //hNVertex->Fill(pvHandle->size());
    }
    
    // this is needed by the IPTools methods from the tracking group
    edm::ESHandle<TransientTrackBuilder> trackBuilder;
    iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder); 
    
    MuonCollection muPlus, muMinus;
    
    // check the validity of the collection
    if(muons.isValid()){
      
      for (MuonCollection::const_iterator recoMu = muons->begin();
	   recoMu!=muons->end(); ++recoMu){ // loop over all muons
	
	double eta = (*recoMu).eta();
	double phi = (*recoMu).phi();
	double pt = (*recoMu).pt();
	double q=(*recoMu).charge();

	
	string muonType = "";
	if(recoMu->isGlobalMuon()) muonType = " Glb";
	if(recoMu->isStandAloneMuon()) muonType = muonType + " STA";
	if(recoMu->isTrackerMuon()) muonType = muonType + " Trk";
	
	cout << "[MuonAnalysis] New Muon found:" << muonType << endl;
	cout << "-- eta: " << eta << " phi: " << phi << " pt: " << pt << " q: " << q << endl;       
	
        if (recoMu->pt() < 1) continue;
	if (recoMu->charge() < 0) muMinus.push_back(*recoMu);
	if (recoMu->charge() > 0) muPlus.push_back(*recoMu);
	
      }
    }
    
    //cout << "n q- " << muMinus.size() << " n q+ " << muPlus.size() << endl;

    MuonCollection BestDiMu;
    
    TLorentzVector DiMuMom=TLorentzVector(0.,0.,0.,0.);
    TLorentzVector pitrack=TLorentzVector(0.,0.,0.,0.);

    TLorentzVector DiMuTrackMom;
    
    TransientVertex tv;
    TransientVertex tv3;
    
    pair<double,double> lxy;

    double NDiMuons=muPlus.size()*muMinus.size();
    //histo ndimu

    double invMassMin=0,invMassMax=1.8;

    findBestDimuon(iSetup, muPlus, muMinus, BestDiMu, tv, primaryVertex,invMassMin,invMassMax);

    cout << "dimuons size " << BestDiMu.size() << endl;

    if (BestDiMu.size()!=2) return;

    bool TwoGood=false;

    if ((muon::isGoodMuon(BestDiMu[0], muon::TMOneStationTight)) && (muon::isGoodMuon(BestDiMu[1], muon::TMOneStationTight))) TwoGood=true; 
      
    DiMuMom=TLorentzVector(BestDiMu[0].px()+ BestDiMu[1].px() , BestDiMu[0].py()+ BestDiMu[1].py(), BestDiMu[0].pz()+ BestDiMu[1].pz(), BestDiMu[0].energy()+ BestDiMu[1].energy());
   
    cout << "dimuon mass " << DiMuMom.M() << endl;

    hDiMuInvMass->Fill(DiMuMom.M());
    if (TwoGood)  hGoodDiMuInvMass->Fill(DiMuMom.M());

    bool isAlsoMu=false;
    invMassMin=1.75;invMassMax=1.8;
    findBestPiCand(ev, iSetup, BestDiMu, tv3, pitrack, isAlsoMu,invMassMin,invMassMax);

    if (pitrack.Px() !=0){
      
      Offline++;
      DiMuTrackMom = DiMuMom+pitrack;
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
      cout << "total mass " << DiMuTrackMom.M() << endl;
      
      //lxy=Compute_Lxy_and_Significance(primaryVertex,tv,DiMuMom);

      /*      if (lxy.second !=0 && lxy.first/lxy.second > 1 ){
	cout << "" << endl;
	}*/
    }    
  }
}


// ------------ method called once each job just before starting event loop  ------------
void Tau3MuAnalysis::beginJob() {

  edm::Service<TFileService> fs;

  hpt= fs->make<TH1F>("TrackPT","Track pT",50,0,10);
  hptMu= fs->make<TH1F>("TrackMuPT","Track with MuId pT",50,0,10);

  hDiMuInvMass= fs->make<TH1F>("hDiMuInvMass","DiMuon Inv. Mass",40,0.9,1.2);
  hGoodDiMuInvMass= fs->make<TH1F>("hGoodDiMuInvMass","Good DiMuon Inv. Mass",40,0.9,1.2);

  hGoodDiMuTrackInvMass= fs->make<TH1F>("hGoodDiMuTrackInvMass","Good DiMuon+Track Inv. Mass",60,1.6,2.3);
  hDiMuTrackInvMass= fs->make<TH1F>("hDiMuTrackInvMass","DiMuon+Track Inv. Mass",60,1.6,2.3);

  hDiMuPHITrackInvMass= fs->make<TH1F>("hDiMuPHITrackInvMass","DiMuonPHI+Track Inv. Mass",60,1.7,2.3);
  hDiMuSBTrackInvMass= fs->make<TH1F>("hDiMuSBTrackInvMass","DiMuonSB+Track Inv. Mass",60,1.7,2.3);

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
