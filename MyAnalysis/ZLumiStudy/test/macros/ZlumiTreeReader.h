//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Jul 13 17:21:10 2012 by ROOT version 5.32/00
// from TTree candTree/Event Summary
// found on file: /data1/d/dboerner/test/ZLumiTreeReaderStudy.root
//////////////////////////////////////////////////////////

#ifndef ZlumiTreeReader_h
#define ZlumiTreeReader_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include "LumiFileReaderByBX.h"
#include "HistoZ.h"

// Header file for the classes stored in the TTree if any.
#include <vector>
#include <set>

// Fixed size dimensions of array or collections stored in the TTree if any.

// define struct so that we have same histograms for different cuts
struct PerCutHistograms
{
   HistoZ* hAll;
   vector<HistoZ*> hByBin;

   TH1F* xSection_fitVExpo;
   TH1F* xSection_fit2VExpo;
   TH1F* xSection_fit2VExpoMin70;
   TH1F* xSection_count;

   TH1F* ptZ;
   TH1F* massZ_selected;
   TH1F* numZPerEvent;

   TH1F* ptL1;
   TH1F* etaL1;
   TH1F* phiL1;
   TH1F* isoL1;
   TH1F* sipL1;

   TH1F* ptL2;
   TH1F* etaL2;
   TH1F* phiL2;
   TH1F* isoL2;
   TH1F* sipL2;

   TProfile* nVtx_delLumi;
   TProfile* nVtx_pileUp;
   TProfile* ls_delLumi;

   TH1F* eff;
}; 


#define NUM_CUTS 5

#define NO_CUT 0
#define ISOLATION_CUT 1
#define NO_ISOLATION_CUT 2
#define ETA_AND_ISOLATION_CUT 3
#define ETA_AND_NO_ISOLATION_CUT 4




class ZlumiTreeReader : public TSelector {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain

   // Declaration of leaf types
   Int_t           RunNumber;
   Long64_t        EventNumber;
   Int_t           LumiNumber;
   Int_t           BXNumber;
   Int_t           iBC;
   Int_t           Nmu;
   Int_t           Nele;
   Int_t           Nvtx;
   Int_t           NObsInt;
   Float_t         NTrueInt;
   Float_t         PUWeight11;
   Float_t         PUWeight12;
   Float_t         PFMET;
   Int_t           genFinalState;
   Short_t         trigWord;
   vector<float>   *ZMass;
   vector<float>   *ZPt;
   vector<float>   *Lep1Pt;
   vector<float>   *Lep1Eta;
   vector<float>   *Lep1Phi;
   vector<int>     *Lep1LepId; // -13
   vector<float>   *Lep1SIP;
   vector<bool>    *Lep1isID; // 0 or 1 
   vector<float>   *Lep1BDT; // 0
   vector<short>   *Lep1ParentId;
   vector<float>   *Lep2Pt;
   vector<float>   *Lep2Eta;
   vector<float>   *Lep2Phi;
   vector<int>     *Lep2LepId;
   vector<float>   *Lep2SIP;
   vector<bool>    *Lep2isID;
   vector<float>   *Lep2BDT;
   vector<short>   *Lep2ParentId;
   vector<float>   *Lep1chargedHadIso;
   vector<float>   *Lep1neutralHadIso;
   vector<float>   *Lep1photonIso;
   vector<float>   *Lep1combRelIsoPF;
   vector<float>   *Lep2chargedHadIso;
   vector<float>   *Lep2neutralHadIso;
   vector<float>   *Lep2photonIso;
   vector<float>   *Lep2combRelIsoPF;
   Float_t         GenZMass;
   Float_t         GenZPt;
   Float_t         GenLep1Pt;
   Float_t         GenLep1Eta;
   Float_t         GenLep1Phi;
   Short_t         GenLep1Id;
   Float_t         GenLep2Pt;
   Float_t         GenLep2Eta;
   Float_t         GenLep2Phi;
   Short_t         GenLep2Id;

   // List of branches
   TBranch        *b_RunNumber;   //!
   TBranch        *b_EventNumber;   //!
   TBranch        *b_LumiNumber;   //!
   TBranch        *b_BXNumber;   //!
   TBranch        *b_iBC;   //!
   TBranch        *b_Nmu;   //!
   TBranch        *b_Nele;   //!
   TBranch        *b_Nvtx;   //!
   TBranch        *b_NObsInt;   //!
   TBranch        *b_NTrueInt;   //!
   TBranch        *b_PUWeight11;   //!
   TBranch        *b_PUWeight12;   //!
   TBranch        *b_PFMET;   //!
   TBranch        *b_genFinalState;   //!
   TBranch        *b_trigWord;   //!
   TBranch        *b_ZMass;   //!
   TBranch        *b_ZPt;   //!
   TBranch        *b_Lep1Pt;   //!
   TBranch        *b_Lep1Eta;   //!
   TBranch        *b_Lep1Phi;   //!
   TBranch        *b_Lep1LepId;   //!
   TBranch        *b_Lep1SIP;   //!
   TBranch        *b_Lep1isID;   //!
   TBranch        *b_Lep1BDT;   //!
   TBranch        *b_Lep1ParentId;   //!
   TBranch        *b_Lep2Pt;   //!
   TBranch        *b_Lep2Eta;   //!
   TBranch        *b_Lep2Phi;   //!
   TBranch        *b_Lep2LepId;   //!
   TBranch        *b_Lep2SIP;   //!
   TBranch        *b_Lep2isID;   //!
   TBranch        *b_Lep2BDT;   //!
   TBranch        *b_Lep2ParentId;   //!
   TBranch        *b_Lep1chargedHadIso;   //!
   TBranch        *b_Lep1neutralHadIso;   //!
   TBranch        *b_Lep1photonIso;   //!
   TBranch        *b_Lep1combRelIsoPF;   //!
   TBranch        *b_Lep2chargedHadIso;   //!
   TBranch        *b_Lep2neutralHadIso;   //!
   TBranch        *b_Lep2photonIso;   //!
   TBranch        *b_Lep2combRelIsoPF;   //!
   TBranch        *b_GenZMass;   //!
   TBranch        *b_GenZPt;   //!
   TBranch        *b_GenLep1Pt;   //!
   TBranch        *b_GenLep1Eta;   //!
   TBranch        *b_GenLep1Phi;   //!
   TBranch        *b_GenLep1Id;   //!
   TBranch        *b_GenLep2Pt;   //!
   TBranch        *b_GenLep2Eta;   //!
   TBranch        *b_GenLep2Phi;   //!
   TBranch        *b_GenLep2Id;   //!

   ZlumiTreeReader(TTree * /*tree*/ =0) : fChain(0) { }
   virtual ~ZlumiTreeReader() { }
   virtual Int_t   Version() const { return 2; }
   virtual void    Begin(TTree *tree);
   virtual void    SlaveBegin(TTree *tree);
   virtual void    Init(TTree *tree);
   virtual Bool_t  Notify();
   virtual Bool_t  Process(Long64_t entry);
   virtual Int_t   GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
   virtual void    SetOption(const char *option) { fOption = option; }
   virtual void    SetObject(TObject *obj) { fObject = obj; }
   virtual void    SetInputList(TList *input) { fInput = input; }
   virtual TList  *GetOutputList() const { return fOutput; }
   virtual void    SlaveTerminate();
   virtual void    Terminate();

   std::map<int,int> ls_Zcount;

   ClassDef(ZlumiTreeReader,0);

   bool analyseCut(/*SIP*/ float sip, /*Pt*/ float pt, /*eta*/ float eta, /*Iso*/ float iso, /*ZMass*/ float massZ_min, float massZ_max, int index_Z);

   PerCutHistograms histsPerCut[NUM_CUTS];


   void CreatePerCutHists();
   void FillPerCutHist(size_t index, int index_Z, RunLumiBXIndex lumiBXIndex);
   void DrawPerCutHists();
   void DeletePerCutHists();

   void ParseOption(const std::string& opt);

   bool useSingleRun;
   int  singleRun;
   std::set<int> runsToUse;
   std::set<int> runNotFound;
   std::string processName;

   std::map<int, LumiFileReaderByBX> lumiReader;

   TFile* myFile;

   TH1F* hLumiIntegralsByBin;

   vector<pair<float,float> > hByBinLimits;

   TH1F* wholeMassZ_selected;

   TH1F* cutflow;
};

#endif

#ifdef ZlumiTreeReader_cxx
void ZlumiTreeReader::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   ZMass = 0;
   ZPt = 0;
   Lep1Pt = 0;
   Lep1Eta = 0;
   Lep1Phi = 0;
   Lep1LepId = 0;
   Lep1SIP = 0;
   Lep1isID = 0;
   Lep1BDT = 0;
   Lep1ParentId = 0;
   Lep2Pt = 0;
   Lep2Eta = 0;
   Lep2Phi = 0;
   Lep2LepId = 0;
   Lep2SIP = 0;
   Lep2isID = 0;
   Lep2BDT = 0;
   Lep2ParentId = 0;
   Lep1chargedHadIso = 0;
   Lep1neutralHadIso = 0;
   Lep1photonIso = 0;
   Lep1combRelIsoPF = 0;
   Lep2chargedHadIso = 0;
   Lep2neutralHadIso = 0;
   Lep2photonIso = 0;
   Lep2combRelIsoPF = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("RunNumber", &RunNumber, &b_RunNumber);
   fChain->SetBranchAddress("EventNumber", &EventNumber, &b_EventNumber);
   fChain->SetBranchAddress("LumiNumber", &LumiNumber, &b_LumiNumber);
   fChain->SetBranchAddress("BXNumber", &BXNumber, &b_BXNumber);
   fChain->SetBranchAddress("iBC", &iBC, &b_iBC);
   fChain->SetBranchAddress("Nmu", &Nmu, &b_Nmu);
   fChain->SetBranchAddress("Nele", &Nele, &b_Nele);
   fChain->SetBranchAddress("Nvtx", &Nvtx, &b_Nvtx);
   fChain->SetBranchAddress("NObsInt", &NObsInt, &b_NObsInt);
   fChain->SetBranchAddress("NTrueInt", &NTrueInt, &b_NTrueInt);
   fChain->SetBranchAddress("PUWeight11", &PUWeight11, &b_PUWeight11);
   fChain->SetBranchAddress("PUWeight12", &PUWeight12, &b_PUWeight12);
   fChain->SetBranchAddress("PFMET", &PFMET, &b_PFMET);
   fChain->SetBranchAddress("genFinalState", &genFinalState, &b_genFinalState);
   fChain->SetBranchAddress("trigWord", &trigWord, &b_trigWord);
   fChain->SetBranchAddress("ZMass", &ZMass, &b_ZMass);
   fChain->SetBranchAddress("ZPt", &ZPt, &b_ZPt);
   fChain->SetBranchAddress("Lep1Pt", &Lep1Pt, &b_Lep1Pt);
   fChain->SetBranchAddress("Lep1Eta", &Lep1Eta, &b_Lep1Eta);
   fChain->SetBranchAddress("Lep1Phi", &Lep1Phi, &b_Lep1Phi);
   fChain->SetBranchAddress("Lep1LepId", &Lep1LepId, &b_Lep1LepId);
   fChain->SetBranchAddress("Lep1SIP", &Lep1SIP, &b_Lep1SIP);
   fChain->SetBranchAddress("Lep1isID", &Lep1isID, &b_Lep1isID);
   fChain->SetBranchAddress("Lep1BDT", &Lep1BDT, &b_Lep1BDT);
   fChain->SetBranchAddress("Lep1ParentId", &Lep1ParentId, &b_Lep1ParentId);
   fChain->SetBranchAddress("Lep2Pt", &Lep2Pt, &b_Lep2Pt);
   fChain->SetBranchAddress("Lep2Eta", &Lep2Eta, &b_Lep2Eta);
   fChain->SetBranchAddress("Lep2Phi", &Lep2Phi, &b_Lep2Phi);
   fChain->SetBranchAddress("Lep2LepId", &Lep2LepId, &b_Lep2LepId);
   fChain->SetBranchAddress("Lep2SIP", &Lep2SIP, &b_Lep2SIP);
   fChain->SetBranchAddress("Lep2isID", &Lep2isID, &b_Lep2isID);
   fChain->SetBranchAddress("Lep2BDT", &Lep2BDT, &b_Lep2BDT);
   fChain->SetBranchAddress("Lep2ParentId", &Lep2ParentId, &b_Lep2ParentId);
   fChain->SetBranchAddress("Lep1chargedHadIso", &Lep1chargedHadIso, &b_Lep1chargedHadIso);
   fChain->SetBranchAddress("Lep1neutralHadIso", &Lep1neutralHadIso, &b_Lep1neutralHadIso);
   fChain->SetBranchAddress("Lep1photonIso", &Lep1photonIso, &b_Lep1photonIso);
   fChain->SetBranchAddress("Lep1combRelIsoPF", &Lep1combRelIsoPF, &b_Lep1combRelIsoPF);
   fChain->SetBranchAddress("Lep2chargedHadIso", &Lep2chargedHadIso, &b_Lep2chargedHadIso);
   fChain->SetBranchAddress("Lep2neutralHadIso", &Lep2neutralHadIso, &b_Lep2neutralHadIso);
   fChain->SetBranchAddress("Lep2photonIso", &Lep2photonIso, &b_Lep2photonIso);
   fChain->SetBranchAddress("Lep2combRelIsoPF", &Lep2combRelIsoPF, &b_Lep2combRelIsoPF);
   fChain->SetBranchAddress("GenZMass", &GenZMass, &b_GenZMass);
   fChain->SetBranchAddress("GenZPt", &GenZPt, &b_GenZPt);
   fChain->SetBranchAddress("GenLep1Pt", &GenLep1Pt, &b_GenLep1Pt);
   fChain->SetBranchAddress("GenLep1Eta", &GenLep1Eta, &b_GenLep1Eta);
   fChain->SetBranchAddress("GenLep1Phi", &GenLep1Phi, &b_GenLep1Phi);
   fChain->SetBranchAddress("GenLep1Id", &GenLep1Id, &b_GenLep1Id);
   fChain->SetBranchAddress("GenLep2Pt", &GenLep2Pt, &b_GenLep2Pt);
   fChain->SetBranchAddress("GenLep2Eta", &GenLep2Eta, &b_GenLep2Eta);
   fChain->SetBranchAddress("GenLep2Phi", &GenLep2Phi, &b_GenLep2Phi);
   fChain->SetBranchAddress("GenLep2Id", &GenLep2Id, &b_GenLep2Id);
}

Bool_t ZlumiTreeReader::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}


#endif // #ifdef ZlumiTreeReader_cxx
