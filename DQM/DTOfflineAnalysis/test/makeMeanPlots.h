//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Jul 23 15:59:01 2009 by ROOT version 5.22/00a
// from TTree res_tree/res_tree
// found on file: residualFits_hqPhiV.root
//////////////////////////////////////////////////////////

#ifndef makeMeanPlots_h
#define makeMeanPlots_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

class makeMeanPlots {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   Double_t        ttrig;
   Int_t           wheel;
   Int_t           station;
   Int_t           sector;
   Int_t           sl;
   Double_t        res_mean;
   Double_t        res_mean_err;
   Double_t        res_sigma1;
   Double_t        res_sigma2;
   Double_t        t0seg;
   Double_t        chi2;

   // List of branches
   TBranch        *b_ttrig;   //!
   TBranch        *b_theWheel;   //!
   TBranch        *b_theStation;   //!
   TBranch        *b_theSector;   //!
   TBranch        *b_theSL;   //!
   TBranch        *b_res_mean;   //!
   TBranch        *b_res_mean_err;   //!
   TBranch        *b_res_sigma1;   //!
   TBranch        *b_res_sigma2;   //!
   TBranch        *b_t0seg;   //!
   TBranch        *b_chi2;   //!

   makeMeanPlots(TTree *tree=0);
   virtual ~makeMeanPlots();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef makeMeanPlots_cxx
makeMeanPlots::makeMeanPlots(TTree *tree)
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("residualFits_hqPhiV.root");
      if (!f) {
         f = new TFile("residualFits_hqPhiV.root");
      }
      tree = (TTree*)gDirectory->Get("res_tree");

   }
   Init(tree);
}

makeMeanPlots::~makeMeanPlots()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t makeMeanPlots::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t makeMeanPlots::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (!fChain->InheritsFrom(TChain::Class()))  return centry;
   TChain *chain = (TChain*)fChain;
   if (chain->GetTreeNumber() != fCurrent) {
      fCurrent = chain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void makeMeanPlots::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("ttrig", &ttrig, &b_ttrig);
   fChain->SetBranchAddress("wheel", &wheel, &b_theWheel);
   fChain->SetBranchAddress("station", &station, &b_theStation);
   fChain->SetBranchAddress("sector", &sector, &b_theSector);
   fChain->SetBranchAddress("sl", &sl, &b_theSL);
   fChain->SetBranchAddress("res_mean", &res_mean, &b_res_mean);
   fChain->SetBranchAddress("res_mean_err", &res_mean_err, &b_res_mean_err);
   fChain->SetBranchAddress("res_sigma1", &res_sigma1, &b_res_sigma1);
   fChain->SetBranchAddress("res_sigma2", &res_sigma2, &b_res_sigma2);
   fChain->SetBranchAddress("t0seg", &t0seg, &b_t0seg);
   fChain->SetBranchAddress("chi2", &chi2, &b_chi2);
   Notify();
}

Bool_t makeMeanPlots::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void makeMeanPlots::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t makeMeanPlots::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef makeMeanPlots_cxx
