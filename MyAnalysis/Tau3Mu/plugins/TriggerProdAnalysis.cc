

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
class TriggerProdAnalysis : public edm::EDAnalyzer {
public:
  explicit TriggerProdAnalysis(const edm::ParameterSet&);
  ~TriggerProdAnalysis();

private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;


  edm::InputTag l1ExtraParticlesIntag;
  edm::InputTag inputTr;
  edm::InputTag DisplacedVertexTag_;
  edm::InputTag beamSpotTag_;
  edm::InputTag L3muCandLabel_;
  edm::InputTag L3muDisplVtxCandLabel_;

//   HistoKin *hKinDs;
//   HistoKin *hKinRecoDs;
//   HistoKin *hKinRecoTau;

//   HistoKin *hKinDs3RecoMatched;
//   HistoKin *hKinDs2RecoMatched;

//   HistoKin *hKinDs3RecoGoodMatched;
//   HistoKin *hKinDs2RecoGoodMatched;

//   HistoImpactParam *hd0MuonGood;
//   HistoImpactParam *hd0MuonGoodMatched;


//   HistoKin *hKinTau;
//   HistoKin *hKinMu;
//   HistoKin *hKinMuLead;
//   HistoKin *hKinMuTrail;
//   HistoKin *hKinPhi;
//   HistoKin *hKinPi;
//   HistoKinPair *hKinDsVsMuLead;
//   HistoKinPair *hKinClosestMuPhi;


//   TH1F *hNRecoMuAll;
//   TH1F *hNRecoMuMatched;
//   TH1F *hNRecoMuGoodAll;
//   TH1F *hNRecoMuGoodMatched;

//   TH1F *hNRecoTkMuMatched;

//   HistoKin *hKinDs3RecoMatched3L1Matched;
//   HistoKin *hKinDs3RecoMatched2L1Matched;
//   HistoKin *hKinDs3RecoMatched2L13p5Matched;
//   HistoKin *hKinDs3RecoMatched2L15Matched;
//   HistoKin *hKinDs3RecoMatchedHLTTau3Mu;


//   TH1F *hNVertex;

//   HistoKin *hKinDs3L1Matched;
//   HistoKin *hKinDs2L1Matched;
//   HistoKin *hKinDs2L13p5Matched;
//   HistoKin *hKinDs2L15Matched;
//   HistoKin *hKinDsHLTTau3Mu;
//   HistoKin *hKinDsHLTTau2MuPixTrack;
//   HistoKin *hKinDsHLTTau2MuRegionalPixelTrack;
//   HistoKin *hKinDsHLTTau2MuRegionalPixelTrackTight;
//   HistoKin *hKinDsHLTTau2MuRegionalPixelTrackAnd3RecoMu;
//   HistoKin *hKinDsHLTTau2MuRegionalPixelTrackAnd2RecoMu;

  HistoVertex *hHLTDiMuonVertex;

  int counter;
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


TriggerProdAnalysis::TriggerProdAnalysis(const edm::ParameterSet& iConfig) {
  counter = 0;
  countInAccept = 0;
  counterMoreThan3Muons = 0;
  counterMoreThanOneds = 0;
  counterTaus = 0;
  l1ExtraParticlesIntag = iConfig.getUntrackedParameter<edm::InputTag>("l1ExtraParticles",
								       edm::InputTag("l1extraParticles",""));
  inputTr               = iConfig.getUntrackedParameter<edm::InputTag>("TriggerResults",
								       edm::InputTag("TriggerResults", "", "HLT"));
  DisplacedVertexTag_   = iConfig.getUntrackedParameter<edm::InputTag>("diMuDisplacedVertex",
								       edm::InputTag("hltDisplacedmumuVtxProducerTauTo2Mu"));
  L3muDisplVtxCandLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("diMuDisplacedVertexFiltLabel",
									edm::InputTag("hltDisplacedmumuFilterTauTo2Mu::reHLT"));
  beamSpotTag_          = iConfig.getUntrackedParameter<edm::InputTag>("beamSpot",
								       edm::InputTag("offlineBeamSpot"));
  L3muCandLabel_        = iConfig.getUntrackedParameter<edm::InputTag>("l3MuonCands",
								       edm::InputTag("hltL3MuonCandidates::reHLT"));
  debug                 = iConfig.getUntrackedParameter<bool>("debug", false);

}

TriggerProdAnalysis::~TriggerProdAnalysis() {}


//
// member functions
//

// ------------ method called to for each event  ------------
void TriggerProdAnalysis::analyze(const edm::Event& ev, const edm::EventSetup& iSetup) {
  float weight = 1.;

  // ------------------------------------------------------------------------------------------------
  // trigger analysis

  // some counters/flags from trigger info
  int nL1Muons=0;
  int nL1MuonsPt3p5=0;
  int nL1MuonsPt5=0;
  bool tau3MuTrig = false;
  bool tau2MuPixTrack = false;
  bool tau2MuRegionalPixTrack = false;
  bool tau2MuRegionalPixTrackTight = false;


  // count number of L1 Muons at correct BX
  // no matching to reco by now. it will require some attention for multiples match, and the phi at MS2
  edm::Handle<l1extra::L1MuonParticleCollection> l1Muon; 
  ev.getByLabel(l1ExtraParticlesIntag, l1Muon);

  for(l1extra::L1MuonParticleCollection::const_iterator it=l1Muon->begin(); it!=l1Muon->end(); it++){
    if (it->bx()==0){             
      double l1pt=it->et();
      //double eta=it->eta();
      //double phi=it->phi();
      //double charge=it->charge();
      nL1Muons++;
      if (l1pt>=3.5) nL1MuonsPt3p5++;
      if (l1pt>=5.0) nL1MuonsPt5++;
    }
  }
  if(debug) cout<<"Found "<<nL1Muons<<" L1 Muons"<<endl;

  // check fired HLT paths
  edm::Handle<edm::TriggerResults> hltresults;
  ev.getByLabel(inputTr, hltresults);

  if (hltresults.isValid()) {
    const edm::TriggerNames TrigNames_ = ev.triggerNames(*hltresults);
    const int ntrigs = hltresults->size();
    for (int itr=0; itr<ntrigs; itr++){
      TString trigName=TrigNames_.triggerName(itr);
      if(debug) cout<<"Found HLT path "<< trigName<<endl;
      if (!hltresults->accept(itr)) continue;
      if(debug) cout << " accepted" << endl;
      // TString trigName=TrigNames_.triggerName(itr);

      // cout<<"Found HLT path "<< trigName<<endl;
      if(trigName=="HLT_TripleMu0_TauTo3Mu_v1") tau3MuTrig=true;
      if(trigName=="HLT_Tau2Mu_RegPixTrack_v1") tau2MuRegionalPixTrack=true;
      if(trigName=="HLT_Tau2Mu_RegPixTrack_v2") tau2MuRegionalPixTrackTight=true;

      if(trigName=="HLT_DoubleMu0Eta2p1_TauTo2Mu_Track_v1") tau2MuPixTrack=true;
    }
  }
  else
    { 
      cout<<"Trigger results not found"<<endl;
    }
  

  // Trigger products analysis

  // get displaced vertices formed by 2 L3 muons
  reco::VertexCollection displacedVertexColl;
  edm::Handle<reco::VertexCollection> displacedVertexCollHandle;
  bool foundVertexColl = ev.getByLabel(DisplacedVertexTag_, displacedVertexCollHandle);
  if(foundVertexColl) displacedVertexColl = *displacedVertexCollHandle;

 // get beam spot
  reco::BeamSpot vertexBeamSpot;
  edm::Handle<reco::BeamSpot> recoBeamSpotHandle;
  ev.getByLabel(beamSpotTag_,recoBeamSpotHandle);
  vertexBeamSpot = *recoBeamSpotHandle;

  // loop over vertex collection
  for(reco::VertexCollection::iterator it = displacedVertexColl.begin(); it!= displacedVertexColl.end(); it++){
          reco::Vertex displacedVertex = *it;

	  float normChi2 = displacedVertex.normalizedChi2();
	  double vtxProb = 0.0;
	  if( (displacedVertex.chi2()>=0.0) && (displacedVertex.ndof()>0) ) vtxProb = TMath::Prob(displacedVertex.chi2(), displacedVertex.ndof() );


	  reco::Vertex::Point vpoint=displacedVertex.position();
	  //translate to global point, should be improved
	  GlobalPoint secondaryVertex (vpoint.x(), vpoint.y(), vpoint.z());

	  reco::Vertex::Error verr = displacedVertex.error();
	  // translate to global error, should be improved
	  GlobalError err(verr.At(0,0), verr.At(1,0), verr.At(1,1), verr.At(2,0), verr.At(2,1), verr.At(2,2) );

	  GlobalPoint displacementFromBeamspot( -1*((vertexBeamSpot.x0() -  secondaryVertex.x()) +
						    (secondaryVertex.z() - vertexBeamSpot.z0()) * vertexBeamSpot.dxdz()),
						-1*((vertexBeamSpot.y0() - secondaryVertex.y())+
						    (secondaryVertex.z() - vertexBeamSpot.z0()) * vertexBeamSpot.dydz()), 0);
        
          float lxy = displacementFromBeamspot.perp();
          float lxyerr = sqrt(err.rerr(displacementFromBeamspot));
        
	  float significance = lxy/lxyerr;
	  // FIXME: add plots lxy and signif vs Pt Ds
	  hHLTDiMuonVertex->Fill(normChi2, vtxProb, lxy, significance, 0, weight);

  }



  // get all l3 mu candidates
  edm::Handle<RecoChargedCandidateCollection> l3mucands;
  ev.getByLabel (L3muCandLabel_,l3mucands);
  if (l3mucands.isValid()){
    if (l3mucands->size()==2) {
      //for (RecoChargedCandidateCollection::const_iterator mucand1=mucands->begin(), endCand1=mucands->end(); mucand1!=endCand1; ++mucand1) {
      TLorentzVector mu1p4=TLorentzVector((*l3mucands)[0].px(),(*l3mucands)[0].py(),(*l3mucands)[0].pz(),(*l3mucands)[0].energy());
      TLorentzVector mu2p4=TLorentzVector((*l3mucands)[1].px(),(*l3mucands)[1].py(),(*l3mucands)[1].pz(),(*l3mucands)[1].energy());
      TLorentzVector DiMu = mu1p4+mu2p4;
      double DiMuMass=(mu1p4+mu2p4).M();
      cout<<endl;
      cout<<"Found L3 muons with mass "<<DiMuMass<<endl;
      //hDiMuInvMass0->Fill(DiMuMass);
    }
  }



  // get the l3 candidates passing the displaced vertex cut
  edm::Handle<trigger::TriggerFilterObjectWithRefs> l3muvtxcands;
  ev.getByLabel(L3muDisplVtxCandLabel_,l3muvtxcands);
  if (l3muvtxcands.isValid()){
    std::vector<RecoChargedCandidateRef> tr;
    l3muvtxcands->getObjects(trigger::TriggerMuon, tr);
    if (tr.size()==2){
      double DiMuMass=(tr[0]->p4()+tr[1]->p4()).mass();
      cout<<endl;
      cout<<"Found L3 muons with displaced vertex with mass "<<DiMuMass<<endl;
      //      hDiMuInvMass1->Fill(DiMuMass);
    }
  }






}

// ------------ method called once each job just before starting event loop  ------------
void TriggerProdAnalysis::beginJob() {
  cout << "begin job" << endl;
  edm::Service<TFileService> fs;

  hHLTDiMuonVertex = new HistoVertex("HLTDiMuonVertex",*fs);

}


// ------------ method called nce each job just after ending the event loop  ------------
void 
TriggerProdAnalysis::endJob() {
  cout << "Total # events: " << counter << endl;
}



#include "FWCore/Framework/interface/MakerMacros.h"  
DEFINE_FWK_MODULE( TriggerProdAnalysis );
