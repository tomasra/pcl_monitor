#include <cassert>
#include <iostream>

#include "ZMuMuNtupleFactory.h"

///--- Constructor ---
ZMuMuNtupleFactory::ZMuMuNtupleFactory(TString fileName) {
  //---- create output tree ----
  _internalTree = true;
  _outFile = new TFile(fileName,"RECREATE");
  _outTree = new TTree("SimpleTree","SimpleTree");
  InitializeVariables();
  InitializeBranches();
}

ZMuMuNtupleFactory::ZMuMuNtupleFactory(TTree* outTree_input) {
  //---- create output tree ----
  _internalTree = false;
  _outTree = outTree_input;
  InitializeVariables();
  InitializeBranches();
}

///--- Destructor ---
ZMuMuNtupleFactory::~ZMuMuNtupleFactory() {
  //---- destroy everything ----
  if(_internalTree){
    delete _outTree;
    delete _outFile;
  }
}



// Actually fills the tree. needs to be called once per event (after all the various "Fill" methods). It also resets all the containers
void ZMuMuNtupleFactory::FillEvent() {
  _outTree->Fill();

  //Z variables
  _ZMass.clear();
  _ZPt.clear();

  //Lepton variables
  _Lep1Pt.clear();
  _Lep1Eta.clear();
  _Lep1Phi.clear();
  _Lep1LepId.clear();
  _Lep1SIP.clear();
  _Lep1isID.clear();
  _Lep1ParentId.clear();

  _Lep2Pt.clear();
  _Lep2Eta.clear();
  _Lep2Phi.clear();
  _Lep2LepId.clear();
  _Lep2SIP.clear();
  _Lep2isID.clear();
  _Lep2ParentId.clear();

  //Lepton isolation variables
  _Lep1chargedHadIso.clear();
  _Lep1neutralHadIso.clear();
  _Lep1photonIso.clear();
  _Lep1combRelIsoPF.clear();
  _Lep1combRelIsoPFFSRCorr.clear();

  _Lep2chargedHadIso.clear();
  _Lep2neutralHadIso.clear();
  _Lep2photonIso.clear();
  _Lep2combRelIsoPF.clear();
  _Lep2combRelIsoPFFSRCorr.clear();

  InitializeVariables();


  return;
}

// Writes the tree to file (if the tree is owned) and additionally stores a simple tree with counters
void ZMuMuNtupleFactory::WriteNtuple(Int_t Nevt_Gen) {
  if(_internalTree){
    _outFile->cd();
    _outTree->Write();

    TTree *_countTree = new TTree("countTree","countTree");
    //General variables in separate tree
    _countTree->Branch("Nevt_Gen",&Nevt_Gen,"Nevt_Gen/I");
    
    _countTree->Fill();
    _countTree->Write();
    _outFile->Write();
  }

  return;
}

///---- Write to a text file branches declaration ----
void ZMuMuNtupleFactory::DumpBranches(TString filename) const
{
  //----- symply use MakeClass
  _outTree->MakeClass(filename);
  return;
}

void ZMuMuNtupleFactory::InitializeVariables() {
  //Event variables
  _RunNumber = 0;
  _EventNumber = 0;
  _LumiNumber = 0;
  _BXNumber = 0;
  _IndexBestCand = 0;


  _Nvtx = 0;
  _NGoodVtx = 0;
  _NObsInt =0;
  _NTrueInt =0;
  _PUWeight11 =0;
  _PUWeight12 =0;
  _genFinalState =0;
  _trigWord =0;


  _genZMass = -1;
  _genZPt = -1;
  
  _genLep1Pt = -1.;
  _genLep1Eta = -1.;
  _genLep1Phi = -1.;
  _genLep1Id = 0;

  _genLep2Pt = -1.;
  _genLep2Eta = -1.;
  _genLep2Phi = -1.;
  _genLep2Id = 0;


  return;
}

void ZMuMuNtupleFactory::InitializeBranches()
{
  //Event variables
  _outTree->Branch("RunNumber",&_RunNumber,"RunNumber/I");
  _outTree->Branch("EventNumber",&_EventNumber,"EventNumber/L");
  _outTree->Branch("LumiNumber",&_LumiNumber,"LumiNumber/I");
  _outTree->Branch("BXNumber",&_BXNumber,"BXNumber/I");
  _outTree->Branch("iBC",&_IndexBestCand,"iBC/I");

  _outTree->Branch("Nvtx",&_Nvtx,"Nvtx/I");
  _outTree->Branch("NGoodVtx",&_NGoodVtx,"NGoodVtx/I");
  _outTree->Branch("NObsInt",&_NObsInt,"NObsInt/I");
  _outTree->Branch("NTrueInt",&_NTrueInt,"NTrueInt/F");
  _outTree->Branch("PUWeight11",&_PUWeight11,"PUWeight11/F");
  _outTree->Branch("PUWeight12",&_PUWeight12,"PUWeight12/F");
  _outTree->Branch("PFMET",&_PFMET,"PFMET/F");
  _outTree->Branch("genFinalState",&_genFinalState,"genFinalState/I");
  _outTree->Branch("trigWord",&_trigWord,"trigWord/S");


  //Z variables
  _outTree->Branch("ZMass",&_ZMass);
  _outTree->Branch("ZPt",&_ZPt);


  //Lepton variables
  _outTree->Branch("Lep1Pt",&_Lep1Pt);
  _outTree->Branch("Lep1Eta",&_Lep1Eta);
  _outTree->Branch("Lep1Phi",&_Lep1Phi);
  _outTree->Branch("Lep1LepId",&_Lep1LepId);
  _outTree->Branch("Lep1SIP",&_Lep1SIP);
  _outTree->Branch("Lep1isID",&_Lep1isID);
  _outTree->Branch("Lep1ParentId",&_Lep1ParentId);

  _outTree->Branch("Lep2Pt",&_Lep2Pt);
  _outTree->Branch("Lep2Eta",&_Lep2Eta);
  _outTree->Branch("Lep2Phi",&_Lep2Phi);
  _outTree->Branch("Lep2LepId",&_Lep2LepId);
  _outTree->Branch("Lep2SIP",&_Lep2SIP);
  _outTree->Branch("Lep2isID",&_Lep2isID);
  _outTree->Branch("Lep2ParentId",&_Lep2ParentId);


  //Lepton isolation variables
  _outTree->Branch("Lep1chargedHadIso",&_Lep1chargedHadIso);
  _outTree->Branch("Lep1neutralHadIso",&_Lep1neutralHadIso);
  _outTree->Branch("Lep1photonIso",&_Lep1photonIso);
  _outTree->Branch("Lep1combRelIsoPF",&_Lep1combRelIsoPF);
  _outTree->Branch("Lep1combRelIsoPFFSRCorr",&_Lep1combRelIsoPFFSRCorr);

  _outTree->Branch("Lep2chargedHadIso",&_Lep2chargedHadIso);
  _outTree->Branch("Lep2neutralHadIso",&_Lep2neutralHadIso);
  _outTree->Branch("Lep2photonIso",&_Lep2photonIso);
  _outTree->Branch("Lep2combRelIsoPF",&_Lep2combRelIsoPF);
  _outTree->Branch("Lep2combRelIsoPFFSRCorr",&_Lep2combRelIsoPFFSRCorr);

//   //Photon variables
//   _outTree->Branch("PhotPt",&_PhotPt);
//   _outTree->Branch("PhotEta",&_PhotEta);
//   _outTree->Branch("PhotPhi",&_PhotPhi);


  _outTree->Branch("GenZMass",&_genZMass,"GenZMass/F");
  _outTree->Branch("GenZPt",&_genZPt,"GenZPt/F");


  _outTree->Branch("GenLep1Pt",&_genLep1Pt,"GenLep1Pt/F");
  _outTree->Branch("GenLep1Eta",&_genLep1Eta,"GenLep1Eta/F");
  _outTree->Branch("GenLep1Phi",&_genLep1Phi,"GenLep1Phi/F");
  _outTree->Branch("GenLep1Id",&_genLep1Id,"GenLep1Id/S");

  _outTree->Branch("GenLep2Pt",&_genLep2Pt,"GenLep2Pt/F");
  _outTree->Branch("GenLep2Eta",&_genLep2Eta,"GenLep2Eta/F");
  _outTree->Branch("GenLep2Phi",&_genLep2Phi,"GenLep2Phi/F");
  _outTree->Branch("GenLep2Id",&_genLep2Id,"GenLep2Id/S");


  return;
}

// to be called for each new candidate: reset the lepton counters
void ZMuMuNtupleFactory::createNewCandidate()
{
  _LeptonIndex = 1;
  _LeptonIsoIndex = 1;

  return;
}



// Fill the kin variables for the GEN Z
void ZMuMuNtupleFactory::FillZGenInfo(const math::XYZTLorentzVector& pZ) {
  _genZMass = pZ.M();
  _genZPt = pZ.Pt();

  return;
}

// Fill the variables for the GEN leptons
void ZMuMuNtupleFactory::FillLepGenInfo(Short_t Lep1Id,
					Short_t Lep2Id, 
					const math::XYZTLorentzVector& Lep1,
					const math::XYZTLorentzVector& Lep2) {
  _genLep1Pt = Lep1.Pt();
  _genLep1Eta = Lep1.Eta();
  _genLep1Phi = Lep1.Phi();
  _genLep1Id  = Lep1Id;

  _genLep2Pt = Lep2.Pt();
  _genLep2Eta = Lep2.Eta();
  _genLep2Phi = Lep2.Phi();
  _genLep2Id  = Lep2Id;

  return;
}



// Fill global variables for the event: among them the event/lumi/bx ID
void ZMuMuNtupleFactory::FillEventInfo(const Int_t RunNumber,
				       const Long64_t EventNumber,
				       const Int_t LumiNumber, 
				       const int bxNumber,
				       const Int_t IndexBestCand, //FIXME: how to fill this?
				       Int_t Nvtx, 
				       Int_t NGoodVtx,
				       Int_t NObsInt,
				       Float_t NTrueInt,
				       Float_t weight11,
				       Float_t weight12,
				       const Float_t PFMET,
				       Int_t genFinalState,
				       Short_t trigWord) {
  _RunNumber = RunNumber;
  _EventNumber = EventNumber;
  _LumiNumber = LumiNumber;
  _BXNumber = bxNumber;
  _IndexBestCand = IndexBestCand;
  _Nvtx = Nvtx;
  _NGoodVtx = NGoodVtx;
  _NObsInt =NObsInt;
  _NTrueInt =NTrueInt;
  _PUWeight11 =weight11;
  _PUWeight12 =weight12;
  _PFMET = PFMET;
  _genFinalState = genFinalState;
  _trigWord = trigWord;
  return;
}





// Fill the kin variables for the Z candidate
void ZMuMuNtupleFactory::FillZInfo(const Float_t ZMass, const Float_t ZPt) {
  _ZMass.push_back(ZMass);
  _ZPt.push_back(ZPt);

  return;
}


// Fill the variables for the leptons
void ZMuMuNtupleFactory::FillLepInfo(const Float_t LepPt,
				     const Float_t LepEta,
				     const Float_t LepPhi,
				     const Int_t LepId,
				     const Float_t LepSIP,
				     bool isID,
				     short parentId) {
  switch(_LeptonIndex){

  case 1:
    _Lep1Pt.push_back(LepPt);
    _Lep1Eta.push_back(LepEta);
    _Lep1Phi.push_back(LepPhi);
    _Lep1LepId.push_back(LepId);
    _Lep1SIP.push_back(LepSIP);
    _Lep1isID.push_back(isID);
    _Lep1ParentId.push_back(parentId);
    break;

  case 2:
    _Lep2Pt.push_back(LepPt);
    _Lep2Eta.push_back(LepEta);
    _Lep2Phi.push_back(LepPhi);
    _Lep2LepId.push_back(LepId);
    _Lep2SIP.push_back(LepSIP);
    _Lep2isID.push_back(isID);
    _Lep2ParentId.push_back(parentId);
    break;
  

  default:
    std::cout << "Error in indexing the muons! Will abort..." << std::endl;
    assert(0);
  }

  _LeptonIndex++;

  return;
}

// Fill isolation variables for the leptons
void ZMuMuNtupleFactory::FillLepIsolInfo(const Float_t LepchargedHadIso,
					 const Float_t LepneutralHadIso,
					 const Float_t LepphotonIso,
					 const Float_t LepcombRelIsoPF,
					 const Float_t LepcombRelIsoPFFSRCorr) {

  switch(_LeptonIsoIndex){

  case 1:
    _Lep1chargedHadIso.push_back(LepchargedHadIso);
    _Lep1neutralHadIso.push_back(LepneutralHadIso);
    _Lep1photonIso.push_back(LepphotonIso);
    _Lep1combRelIsoPF.push_back(LepcombRelIsoPF);
    _Lep1combRelIsoPFFSRCorr.push_back(LepcombRelIsoPFFSRCorr);
    break;

  case 2:
    _Lep2chargedHadIso.push_back(LepchargedHadIso);
    _Lep2neutralHadIso.push_back(LepneutralHadIso);
    _Lep2photonIso.push_back(LepphotonIso);
    _Lep2combRelIsoPFFSRCorr.push_back(LepcombRelIsoPFFSRCorr);
    break;



  default:
    std::cout << "Error in indexing the muon isolation variables! Will abort..." << std::endl;
    assert(0);
  }

  _LeptonIsoIndex++;

  return;
}

// void ZMuMuNtupleFactory::FillPhotonInfo(const Float_t PhotPt, const Float_t PhotEta, const Float_t PhotPhi)
// {

//   _PhotPt.push_back(PhotPt);
//   _PhotEta.push_back(PhotEta);
//   _PhotPhi.push_back(PhotPhi);

//   return;
// }
