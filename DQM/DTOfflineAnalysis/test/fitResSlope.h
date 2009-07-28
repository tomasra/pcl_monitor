//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Jul 23 15:59:01 2009 by ROOT version 5.22/00a
// from TTree res_tree/res_tree
// found on file: residualFits_hqPhiV.root
//////////////////////////////////////////////////////////

#ifndef fitResSlope_h
#define fitResSlope_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

class fitResSlope {

 public :
  fitResSlope(TTree *tree=0);

  ~fitResSlope();

  Int_t    Cut(Long64_t entry);
  Int_t    GetEntry(Long64_t entry);
  Long64_t LoadTree(Long64_t entry);
  void     Init(TTree *tree);
  void     Loop();
  Bool_t   Notify();
  void     Show(Long64_t entry = -1);
  void     DumpCorrection(const char *filename);

 private:
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

  Double_t        ttrigCorr[5][14][4][3];

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

};

#endif

