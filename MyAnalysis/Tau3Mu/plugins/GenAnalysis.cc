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

inline bool sortByPt(const reco::Candidate *part1, const reco::Candidate *part2) {

  return part1->pt() > part2->pt();
}

inline bool sortMuByPt(const reco::Muon mu1, const reco::Muon mu2) {

  return mu1.pt() > mu2.pt();
}

//-----------------------------------------------------------------
class GenAnalysis : public edm::EDAnalyzer {
public:
  explicit GenAnalysis(const edm::ParameterSet&);
  ~GenAnalysis();

private:
  virtual void beginJob();
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob();
  virtual void beginRun(edm::Run const&, edm::EventSetup const&);
  virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
  virtual void Initialize_TreeVars(); 
  virtual double Compute_Lxy(TVector3 *, TVector3 *, TLorentzVector*);
  virtual bool TriggerDecision(const edm::Event&);
  
  string theVertexLabel;
  bool debug;

  int  Total,Triggered;

  TH1F* hDiMuInvMass,* hGoodDiMuInvMass;
 
  //
  
  TFile* thefile;

  std::string FileName;

  TTree *ExTree;

  TLorentzVector *_Mu1_4Mom,*_Mu2_4Mom,*_MuTrack_4Mom, *_DiMu4Mom, *_DiMuPlusTrack4Mom;

  int _Mu1Q,_Mu2Q,_Mu3Q;
  int _Ds_Mom;

  TVector3 *_PV,*_SV;
  double _Lxy;
 
  bool _TrigBit[10];

  std::vector<string> HLT_paths;
  std::string HLT_process;


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

GenAnalysis::GenAnalysis(const edm::ParameterSet& cfg) {

  FileName = cfg.getParameter<std::string> ("OutFileName");
  HLT_paths = cfg.getParameter<std::vector<string> > ("HLT_paths");
  HLT_process = cfg.getParameter<std::string> ("HLT_process");
}

GenAnalysis::~GenAnalysis() {}

double GenAnalysis::Compute_Lxy(TVector3 * primaryVertex, TVector3 *v, TLorentzVector* DiMuMom){
  
  if (debug) cout << "computing lxy and error" << endl;


  double lxy=((v->X()-primaryVertex->X())*DiMuMom->Px()+(v->Y()-primaryVertex->Y())*DiMuMom->Py())*DiMuMom->M()/pow(DiMuMom->Pt(),2);

  return lxy;

}

bool GenAnalysis::TriggerDecision(const edm::Event& ev){

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
void GenAnalysis::analyze(const edm::Event& ev, const edm::EventSetup& iSetup) {

  Initialize_TreeVars();

  bool triggered=TriggerDecision(ev);

  cout << "----new event  " << endl;
  Total++;

  if (triggered)  Triggered++;
    
    string mcTruthCollection = "genParticles";
    edm::Handle< reco::GenParticleCollection > genParticleHandle;
    ev.getByLabel(mcTruthCollection,genParticleHandle) ;

    if (!(genParticleHandle.isValid())) return;

    const reco::GenParticleCollection *genParticleCollection = genParticleHandle.product();

    reco::GenParticleCollection::const_iterator genPart;

    for(genPart=genParticleCollection->begin(); genPart!=genParticleCollection->end(); genPart++) {
      const reco::Candidate & cand = *genPart;

      if (abs(cand.pdgId())!= 431) continue;

      //cout << " Ds Vtx " << cand.vx() << endl;
      _Ds_Mom=cand.mother()->pdgId();
      //cout << "Ds mom " << _Ds_Mom << endl;
      _DiMuPlusTrack4Mom->SetPtEtaPhiM(cand.pt(),cand.eta(),cand.phi(),cand.mass());

      _PV->SetXYZ(cand.vx(),cand.vy(),cand.vz());

      //if (1) cout << "Mom Id " << cand.pdgId() << endl;      

      int ndau=cand.numberOfDaughters();
      
      if (ndau<2) continue;
      
      for(int k = 0; k < ndau; ++ k) {

	TLorentzVector gen4mom;

	const Candidate * d = cand.daughter( k );
	int dauId = d->pdgId();

	if (abs(dauId)!=333 && abs(dauId)!=211 ) continue;

	if (dauId==333){
	  if (1) cout << "Phi found!" << endl;
	  int ndauphi=d->numberOfDaughters();
	  _DiMu4Mom->SetPtEtaPhiM(d->pt(),d->eta(),d->phi(),d->mass());

	  int mucount=0;
	  for(int k1 = 0; k1 < ndauphi; ++ k1) {
	    const Candidate * d1 = d->daughter( k1 );
	    int dauphiId = d1->pdgId();

	    if (abs(dauphiId)==13) {
	      mucount++;
	      if (mucount==1) {_Mu1_4Mom->SetPtEtaPhiM(d1->pt(),d1->eta(),d1->phi(),d1->mass()); _Mu1Q=d1->charge();}
	      if (mucount==2) {_Mu2_4Mom->SetPtEtaPhiM(d1->pt(),d1->eta(),d1->phi(),d1->mass()); _Mu2Q=d1->charge();}
	    }
	  }
	}

	if (abs(dauId)==211) {
	  _SV->SetXYZ(d->vx(),d->vy(),d->vz());
	  _Mu3Q=d->charge();
	  _MuTrack_4Mom->SetPtEtaPhiM(d->pt(),d->eta(),d->phi(),d->mass());
	}
      }
    }

    if (_Mu1_4Mom->Pt()!=0 && _Mu2_4Mom->Pt()!=0 && _MuTrack_4Mom->Pt()!=0) {
      _Lxy=Compute_Lxy(_PV,_SV,_DiMuPlusTrack4Mom);
      ExTree->Fill();
    }
}

void GenAnalysis::Initialize_TreeVars(){
  debug=false;

  for (int k=0; k<10; k++){
    _TrigBit[k]=false;
  }

  _Ds_Mom=0;
  _DiMu4Mom->SetPtEtaPhiM(0.,0.,0.,0.);
  _DiMuPlusTrack4Mom->SetPtEtaPhiM(0.,0.,0.,0.);

  _Mu1_4Mom->SetPtEtaPhiM(0.,0.,0.,0.);
  _Mu2_4Mom->SetPtEtaPhiM(0.,0.,0.,0.);

  _MuTrack_4Mom->SetPtEtaPhiM(0.,0.,0.,0.);

  _Mu1Q=0;_Mu2Q=0;_Mu3Q=0;

  _PV->SetXYZ(0.,0.,0.);
  _SV->SetXYZ(0.,0.,0.);
  
  _Lxy=-99;
 
 
}


// ------------ method called once each job just before starting event loop  ------------
void GenAnalysis::beginJob() {

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

  ExTree->Branch("Ds_Mother",&_Ds_Mom   , "_Ds_Mom/I");

  ExTree->Branch("Mu1Q",&_Mu1Q   , "_Mu1Q/I");
  ExTree->Branch("Mu2Q",&_Mu2Q   , "_Mu2Q/I");
  ExTree->Branch("Mu3Q",&_Mu3Q   , "_Mu3Q/I");

  ExTree->Branch("Lxy",&_Lxy   ,"_Lxy/D");
 
}




void 
GenAnalysis::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup)
{
}

void 
GenAnalysis::beginLuminosityBlock(edm::LuminosityBlock const& iLumi, edm::EventSetup const& iSetup)
{
}



// ------------ method called nce each job just after ending the event loop  ------------
void 
GenAnalysis::endJob() {

  thefile->cd();
  ExTree->Write();  
  delete ExTree;
  thefile->Close();
  delete thefile;
  
}

#include "FWCore/Framework/interface/MakerMacros.h"  
DEFINE_FWK_MODULE( GenAnalysis );
