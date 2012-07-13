#ifndef ZMuMuNtupleFactory_h
#define ZMuMuNtupleFactory_h

#include <vector>

#include <TFile.h>
#include <TString.h>
#include <TTree.h>

#include "DataFormats/Math/interface/LorentzVector.h"

class ZMuMuNtupleFactory{
  
 protected:
  
 public:

  ZMuMuNtupleFactory(TString namefile);

  ZMuMuNtupleFactory(TTree* outTree_input);

  ~ZMuMuNtupleFactory();

  // Actually fills the tree. needs to be called once per event (after all the various "Fill" methods). It also resets all the containers
  void FillEvent();

  // Writes the tree to file (if the tree is owned) and additionally stores a simple tree with counters
  void WriteNtuple(Int_t Nevt_gen); 

  void DumpBranches(TString filename) const;

  
  void createNewCandidate();

  // Fill global variables for the event: among them the event/lumi/bx ID
  void FillEventInfo(const Int_t RunNumber,
		     const Long64_t EventNumber,
		     const Int_t LumiNumber,
		     const int  bxNumber,
		     const Int_t IndexBestCand,
		     Int_t Nvtx,
		     Int_t NObsInt,
		     Float_t NTrueInt,
		     Float_t weight11,
		     Float_t weight12,
		     Float_t PFMET,
		     Int_t genFinalState,
		     Short_t trigWord);

  
  // Fill the kin variables for the Z candidate
  void FillZInfo(const Float_t ZMass, const Float_t ZPt);

  
  // Fill the variables for the leptons
  void FillLepInfo(const Float_t LepPt,
		   const Float_t LepEta,
		   const Float_t LepPhi,
		   const Int_t LepId,
		   const Float_t SIP,
		   bool isID,
		   float BDT,
		   short parentId);


  // Fill isolation variables for the leptons
  void FillLepIsolInfo(const Float_t LepchargedHadIso,
		       const Float_t LepneutralHadIso,
		       const Float_t LepphotonIso,
		       const Float_t LepcombRelIsoPF);


  //  void FillPhotonInfo(const Float_t PhotPt, const Float_t PhotEta, const Float_t PhotPhi); // KEEP COMMENTED

  // Fill the kin variables for the GEN Z
  void FillZGenInfo(const math::XYZTLorentzVector& Zp);


  // Fill the variables for the GEN leptons
  void FillLepGenInfo(Short_t Lep1Id, Short_t Lep2Id,
		      const math::XYZTLorentzVector& Lep1, const math::XYZTLorentzVector& Lep2);

 private:

  TTree* _outTree;
  Bool_t _internalTree;
  
  TFile* _outFile;

  void InitializeBranches();
  void InitializeVariables();

  Int_t _LeptonIndex;
  Int_t _LeptonIsoIndex;

  //Event variables
  Int_t _RunNumber;
  Long64_t _EventNumber;
  Int_t _LumiNumber;
  int _BXNumber;
  Int_t _IndexBestCand;


  Int_t _Nmu;
  Int_t _Nele;

  Int_t _Nvtx;
  Int_t _NObsInt;
  Float_t _NTrueInt;
  Float_t _PUWeight11;
  Float_t _PUWeight12;
  Float_t _PFMET;
  Int_t _genFinalState;
  Short_t _trigWord;



  //Z variables
  std::vector<Float_t> _ZMass;
  std::vector<Float_t> _ZPt;



  //Lepton variables
  std::vector<Float_t> _Lep1Pt;
  std::vector<Float_t> _Lep1Eta;
  std::vector<Float_t> _Lep1Phi;
  std::vector<Int_t>   _Lep1LepId;
  std::vector<Float_t> _Lep1SIP;
  std::vector<Bool_t>  _Lep1isID;
  std::vector<Float_t> _Lep1BDT;
  std::vector<Short_t> _Lep1ParentId;

  std::vector<Float_t> _Lep2Pt;
  std::vector<Float_t> _Lep2Eta;
  std::vector<Float_t> _Lep2Phi;
  std::vector<Int_t>   _Lep2LepId;
  std::vector<Float_t> _Lep2SIP;
  std::vector<Bool_t>  _Lep2isID;
  std::vector<Float_t> _Lep2BDT;
  std::vector<Short_t> _Lep2ParentId;



  //Lepton isolation variables
  std::vector<Float_t> _Lep1chargedHadIso;
  std::vector<Float_t> _Lep1neutralHadIso;
  std::vector<Float_t> _Lep1photonIso;
  std::vector<Float_t> _Lep1combRelIsoPF;

  std::vector<Float_t> _Lep2chargedHadIso;
  std::vector<Float_t> _Lep2neutralHadIso;
  std::vector<Float_t> _Lep2photonIso;
  std::vector<Float_t> _Lep2combRelIsoPF;

//   //Photon variables
//   std::vector<Float_t> _PhotPt;
//   std::vector<Float_t> _PhotEta;
//   std::vector<Float_t> _PhotPhi;


  Float_t _genZMass;
  Float_t _genZPt;

  Float_t _genLep1Pt;
  Float_t _genLep1Eta;
  Float_t _genLep1Phi;
  Short_t _genLep1Id;

  Float_t _genLep2Pt;
  Float_t _genLep2Eta;
  Float_t _genLep2Phi;
  Short_t _genLep2Id;


};

#endif
