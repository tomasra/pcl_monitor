// -*- C++ -*-
//
// Package:    ZTreeMaker
// Class:      ZTreeMaker
// 
/**\class ZTreeMaker ZTreeMaker.cc HZZ4lAnalysis/ZTreeMaker/src/ZTreeMaker.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Stefano Casasso,,,
//         Created:  Tue Feb 28 14:33:03 CET 2012
// $Id: ZTreeMaker.cc,v 1.44 2012/07/08 09:23:02 namapane Exp $
//
//


// system include files
#include <memory>
#include <cmath>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include <FWCore/Framework/interface/ESHandle.h>
#include <FWCore/Framework/interface/LuminosityBlock.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <DataFormats/Common/interface/TriggerResults.h>
#include <FWCore/Common/interface/TriggerNames.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>

#include <DataFormats/Common/interface/View.h>
#include <DataFormats/Candidate/interface/Candidate.h>
#include <DataFormats/PatCandidates/interface/CompositeCandidate.h>
#include <DataFormats/PatCandidates/interface/Muon.h>
#include <DataFormats/PatCandidates/interface/Electron.h>
#include <DataFormats/METReco/interface/PFMET.h>
#include <DataFormats/METReco/interface/PFMETCollection.h>
#include <AnalysisDataFormats/CMGTools/interface/BaseMET.h>
#include <DataFormats/Math/interface/LorentzVector.h>
#include <DataFormats/VertexReco/interface/Vertex.h>
#include <CommonTools/UtilAlgos/interface/TFileService.h>
#include <DataFormats/Common/interface/MergeableCounter.h>
#include <DataFormats/VertexReco/interface/Vertex.h>
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

#include <ZZAnalysis/AnalysisStep/interface/DaughterDataHelpers.h>
#include <ZZAnalysis/AnalysisStep/interface/FinalStates.h>
#include <ZZAnalysis/AnalysisStep/interface/MCHistoryTools.h>
#include <ZZAnalysis/AnalysisStep/interface/PUReweight.h>


#include <AnalysisDataFormats/CMGTools/interface/Photon.h>

#include "MyAnalysis/ZLumiStudy/src/ZMuMuConfigHelper.h"
#include "MyAnalysis/ZLumiStudy/src/ZMuMuNtupleFactory.h"

namespace {
  bool writePhotons = false;  // Write photons in the tree. FIXME: make this configurable
}


using namespace std;
using namespace edm;
//
// class declaration
//
class ZTreeMaker : public edm::EDAnalyzer {
public:
  explicit ZTreeMaker(const edm::ParameterSet&);
  ~ZTreeMaker();
  
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  
  
private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void FillCandidate(const pat::CompositeCandidate& higgs, bool evtPass);
//   virtual void FillPhoton(const cmg::Photon& photon);
  virtual void endJob() ;
  
  virtual void beginRun(edm::Run const&, edm::EventSetup const&);
  virtual void endRun(edm::Run const&, edm::EventSetup const&);
  virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
  virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

  // ----------member data ---------------------------
  ZMuMuConfigHelper myHelper;
  int theChannel;
  std::string theCandLabel;
  TString theFileName;

  ZMuMuNtupleFactory *myTree;
  TH1F *hCounter;

  Bool_t isMC;

  bool applyTrigger;    // Only events passing trigger
  bool applySkim;       //  "     "      "     skim
  bool skipEmptyEvents; // Skip events whith no candidate in the collection

  PUReweight reweight;

  //counters
  Float_t Nevt_Gen;
  // FIXME: can deine many others

};

//
// constructors and destructor
//
ZTreeMaker::ZTreeMaker(const edm::ParameterSet& pset) : myHelper(pset) {
  theCandLabel = pset.getUntrackedParameter<string>("CandCollection");
  theChannel = myHelper.channel();
  theFileName = pset.getUntrackedParameter<string>("fileName");
  skipEmptyEvents = pset.getParameter<bool>("skipEmptyEvents");
  
  if (skipEmptyEvents) {
    applyTrigger=true;
    applySkim=false; //FIXME: not using the skim infrastructure for the moment
    
    cout << "[ZTreeMaker] INFO: Will skip events not passing the trigger selection!" << endl;
  } else {
    applyTrigger=false;
    applySkim=false;    
  }

  isMC = myHelper.isMC();
  if(isMC) {
    cout << "[ZTreeMaker] INFO: running on MC!" << endl;
  } else {
    cout << "[ZTreeMaker] INFO: running on DATA!" << endl;
  }

  // initialize the counters
  Nevt_Gen = 0;

}

ZTreeMaker::~ZTreeMaker() {}


//
// member functions
//

// ------------ method called for each event  ------------
void ZTreeMaker::analyze(const edm::Event& event, const edm::EventSetup& eSetup) {

  Handle<vector<reco::Vertex> >  vertexs;
  event.getByLabel("offlinePrimaryVertices",vertexs);
  
  //----------------------------------------------------------------------
  // Analyze MC history. THIS HAS TO BE DONE BEFORE ANY RETURN STATEMENT
  // (eg skim or trigger), in order to update the gen counters correctly!!!
  int nObsInt  = -1;
  float nTrueInt = -1.;
  Float_t weight1 = 1.;
  Float_t weight2 = 1.;
  Int_t genFinalState = -1;


  std::vector<const reco::Candidate *> genZs;
  std::vector<const reco::Candidate *> genZLeps;
  if (isMC) {
    string PUWeightTag = "vertexWeight2011AB"; //FIXME pass this with a config parameter
    edm::Handle<double> PUWeight;
    event.getByLabel(PUWeightTag, PUWeight);
    weight1 = (*PUWeight);

    Handle<std::vector< PileupSummaryInfo > >  PupInfo;
    event.getByLabel(edm::InputTag("addPileupInfo"), PupInfo);

    std::vector<PileupSummaryInfo>::const_iterator PVI;
    for(PVI = PupInfo->begin(); PVI != PupInfo->end(); ++PVI) {
      if(PVI->getBunchCrossing() == 0) { 
	nObsInt  = PVI->getPU_NumInteractions();
	nTrueInt = PVI->getTrueNumInteractions();
	break;
      } 
    }

    // FIXME: how does this work???
    int source = myHelper.sampleType();
    int target = myHelper.setup();
    weight2 = reweight.weight(source,target,nTrueInt);

    // FIXME: this need to be  removed/revised 
    MCHistoryTools mch(event);
    genFinalState = mch.genFinalState();
      
    // FIXME: need to check how this is selected
    genZs = mch.genZs();
    genZLeps = mch.genZLeps();
  }
  //----------------------------------------------------------------------

  //Get candidate collection
  edm::Handle<edm::View<pat::CompositeCandidate> > candHandle;
  event.getByLabel(theCandLabel, candHandle);
  const edm::View<pat::CompositeCandidate>* cands = candHandle.product();

  //This is very important in order not to carry information from the previous event. 
  // NOTHING IN THE NTUPLE MUST BE FILLED BEFORE THIS!
  //because the cleaning of the ntuple objects is done at the FillEvent()!

  if (skipEmptyEvents) {
    if (cands->size() == 0) return; // Skip events with no candidate
  } else { 
    if (cands->size() == 0 && genFinalState!=theChannel) return; // Skip empty events of the "wrong" gen final state
  }
  
 
  if (isMC) {
    // Fill the MC truth information
    myTree->FillZGenInfo(genZs.at(0)->p4());
    myTree->FillLepGenInfo(genZLeps.at(0)->pdgId(), genZLeps.at(1)->pdgId(),
			   genZLeps.at(0)->p4(), genZLeps.at(1)->p4());
  }

  // Apply MC filter (skip event)
  if (isMC && !(myHelper.passMCFilter(event))) return;

  // Apply skim
  Short_t trigWord=0;
  // FIXME: check this allows the possibility to define several paths for diffrent selections...
  bool evtPassSkim = myHelper.passSkim(event, trigWord);
  if (applySkim && !evtPassSkim) {
    bool debug = true;
    if(debug) cout << "[ZTreeMaker] Event didn't pass the skim!" << endl;
    return;
  }

  // Apply trigger request (skip event)
  bool evtPassTrigger = myHelper.passTrigger(event, trigWord);
  if (applyTrigger && !evtPassTrigger) return;

  //Counter to find the best candidate
  Int_t NbestCand = -1;
  Int_t CandCounter = 0;

  for( edm::View<pat::CompositeCandidate>::const_iterator cand = cands->begin(); cand != cands->end(); ++cand) {
    FillCandidate(*cand, evtPassTrigger&&evtPassSkim);

    if(cand->userFloat("isBestCand")) NbestCand = CandCounter;
    else CandCounter++;
  }

  // cmgPhotons

//   if (writePhotons) {
//     edm::Handle<vector<cmg::Photon> > photons;
//     if (event.getByLabel("cmgPhotonSel",photons)) {
//       //cout << "Photons: " << photons->size() <<endl;
//       for( vector<cmg::Photon>::const_iterator ph = photons->begin(); ph != photons->end(); ++ph) {
// 	//cout << "photon: pt= " << ph->pt() << endl;
// 	if(ph->pt() > 2. && fabs(ph->eta()) < 2.8) FillPhoton(*ph);
//       }
//     }
//   }

  //MET info
//   Handle<reco::PFMETCollection> pfmetcoll;
//   event.getByLabel("patMETs", pfmetcoll);
//   float pfmet = -1;
//   if(pfmetcoll.isValid()){
//     const reco::PFMETCollection *pfmetcol = pfmetcoll.product();
//     const reco::PFMET *pfmetObj = &(pfmetcol->front());
//     pfmet = pfmetObj->pt();
//     //cout << pfmet << endl;
//   }

  Handle<vector<cmg::BaseMET> > pfmetcoll;
  event.getByLabel("cmgPFMET", pfmetcoll);
  float pfmet = -1;
  if(pfmetcoll.isValid()){
    pfmet = pfmetcoll->front().pt();
  }


  //Save general event info in the tree. This must be done after the loop on the candidates so that we know the best candidate position in the list
  myTree->FillEventInfo(event.id().run(),
			event.id().event(),
			event.luminosityBlock(),
			event.eventAuxiliary().bunchCrossing(),
			NbestCand,
			vertexs->size(),
			nObsInt,
			nTrueInt,
			weight1,
			weight2,
			pfmet,
			genFinalState,
			trigWord);

  myTree->FillEvent();

  return;
}

// void ZTreeMaker::FillPhoton(const cmg::Photon& photon)
// {
//   const Float_t photPt  = photon.pt();
//   const Float_t photEta = photon.eta();
//   const Float_t photPhi = photon.phi();

//   myTree->FillPhotonInfo(photPt, photEta, photPhi);

//   return;
// }

void ZTreeMaker::FillCandidate(const pat::CompositeCandidate& cand, bool evtPass)
{
  //Initialize a new candidate into the tree
  myTree->createNewCandidate();

  const Float_t ZMass = cand.p4().mass();
  const Float_t ZPt = cand.p4().pt();

  myTree->FillZInfo(ZMass, ZPt);
  
  vector<const reco::Candidate*> leptons(2);
  vector<string> labels(2);

  const reco::Candidate* ZLp = cand.daughter(0);
  const reco::Candidate* ZLn = cand.daughter(1);
  string ZLpLabel = "d0.";
  string ZLnLabel = "d1.";
  if (ZLp->charge() < 0 && ZLp->charge()*ZLn->charge()<0) {
      swap(ZLp,ZLn);
      swap(ZLpLabel,ZLnLabel);
  } 
  leptons[0]=ZLp;
  leptons[1]=ZLn;
  labels[0]=ZLpLabel;
  labels[1]=ZLnLabel;
  
  cout << "A"<< endl;
  // Retrieve the userFloat of the leptons in vectors ordered in the same way.
  vector<float> SIP(2);
  vector<float> PFChargedHadIso(2);
  vector<float> PFNeutralHadIso(2);
  vector<float> PFPhotonIso(2);
  vector<float> combRelIsoPF(2);
  vector<bool>  isID(2);




  for (unsigned int i=0; i<leptons.size(); ++i){
    SIP[i]             = userdatahelpers::getUserFloat(leptons[i],"SIP");
    PFChargedHadIso[i] = userdatahelpers::getUserFloat(leptons[i],"PFChargedHadIso");
    PFNeutralHadIso[i] = userdatahelpers::getUserFloat(leptons[i],"PFNeutralHadIso");
    PFPhotonIso[i]     = userdatahelpers::getUserFloat(leptons[i],"PFPhotonIso");
    isID[i]            = userdatahelpers::getUserFloat(leptons[i],"ID");
    cout << "1" << endl;

    if (theChannel==ZL) {
      combRelIsoPF[i]    = userdatahelpers::getUserFloat(leptons[i],"combRelIsoPF");
      //FIXME cannot take labels[i]+"SIP", that info only attached to the Z!!
    } else {
      combRelIsoPF[i]    = cand.userFloat(labels[i]+"combRelIsoPFFSRCorr"); // Note: the FSR-corrected iso is attached to the Z, not to the lepton!
      // Check that I don't mess up with labels[] and leptons[]
      assert(SIP[i] == cand.userFloat(labels[i]+"SIP"));
    }

    cout << "2" << endl;
    //Fill the info on the lepton candidates  
    myTree->FillLepInfo(leptons[i]->pt(),
			leptons[i]->eta(),
			leptons[i]->phi(),
			leptons[i]->pdgId(),
			SIP[i],
			isID[i],
			userdatahelpers::getUserFloat(leptons[i],"BDT"),
			userdatahelpers::getUserFloat(leptons[i],"MCParentCode"));

    cout << "3" << endl;
    //Isolation variables
    myTree->FillLepIsolInfo(PFChargedHadIso[i],
			    PFNeutralHadIso[i],
			    PFPhotonIso[i], 
			    combRelIsoPF[i]);
  }

  cout << "B"<< endl;
}



// ------------ method called once each job just before starting event loop  ------------
void ZTreeMaker::beginJob()
{
  edm::Service<TFileService> fs;
  myTree = new ZMuMuNtupleFactory( fs->make<TTree>(theFileName,"Event Summary"));
  hCounter = fs->make<TH1F>("Counters", "Counters", 20, 0., 20.);
}

// ------------ method called once each job just after ending the event loop  ------------
void ZTreeMaker::endJob()
{
  hCounter->SetBinContent(1 ,Nevt_Gen);
  hCounter->GetXaxis()->SetBinLabel(1 ,"Nevt_Gen");

  return;
}

// ------------ method called when starting to processes a run  ------------
void ZTreeMaker::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void ZTreeMaker::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void ZTreeMaker::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void ZTreeMaker::endLuminosityBlock(edm::LuminosityBlock const& iLumi, edm::EventSetup const& iSetup)
{
  Float_t Nevt_preskim = -1.;
  edm::Handle<edm::MergeableCounter> preSkimCounter;
  if (iLumi.getByLabel("preSkimCounter", preSkimCounter)) { // Counter before skim. Does not exist for non-skimmed samples.
    Nevt_preskim = preSkimCounter->value;
  }  
  
  edm::Handle<edm::MergeableCounter> prePathCounter;
  iLumi.getByLabel("prePathCounter", prePathCounter);       // Counter of input events in the input pattuple

  // Nevt_gen: this is the number before any skim
  if (Nevt_preskim>=0.) {
    Nevt_Gen = Nevt_Gen + Nevt_preskim; 
  } else {
    Nevt_Gen = Nevt_Gen + prePathCounter->value;    
  }
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void ZTreeMaker::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(ZTreeMaker);
