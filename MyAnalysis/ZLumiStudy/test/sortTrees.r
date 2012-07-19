#if !defined(__CINT) || defined(__MAKECINT__)

#include "TH1F.h"
#include "TH2F.h"

#include "TStyle.h"
#include "TString.h"
#include "TFile.h"
#include "TROOT.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "TGraphErrors.h"


// #include "HistoAlat.h"
#include <iostream>
#include <string>
#include <vector>

#include "TStopwatch.h"

#endif

using namespace std;

// Usage: .x sortTrees.r
// Simple utility to sort trees by run so that the lookup into the lumi tree is much faster

void sortTrees() {

  vector<TString> fileBaseNames;
  //  fileBaseNames.push_back("/data/Analysis/42X_BX_v0/DoubleMu-May10ReReco");
  
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB1/ZLumiStudy");
//   fileBaseNames.push_back("/data/Analysis/42X_BX_v0/DoubleMu-05Aug2011");
//   fileBaseNames.push_back("/data/Analysis/42X_BX_v0/DoubleMu-PromptReco-v6");
//   fileBaseNames.push_back("/data/Analysis/42X_BX_v0/SingleMu-05Aug2011");
//   fileBaseNames.push_back("/data/Analysis/42X_BX_v0/SingleMu-PromptReco-v4");
//   fileBaseNames.push_back("/data/Analysis/42X_BX_v0/SingleMu-May10ReReco");
//   fileBaseNames.push_back("/data/Analysis/42X_BX_v0/SingleMu-PromptReco-v6");
  


  for(vector<TString>::const_iterator basename = fileBaseNames.begin();
      basename != fileBaseNames.end(); ++basename) {
    
    TString oldName = (*basename) + ".root";
    TString newName = (*basename) + "_sorted.root";
    TFile oldFile(oldName.Data());
    TTree *tree = (TTree*) oldFile.Get("Z2muTree/candTree"); 
    
    Int_t nentries = (Int_t)tree->GetEntries();

    //Drawing variable pz with no graphics option.
    //variable pz stored in array fV1 (see TTree::Draw)
    tree->Draw("RunNumber","","goff");
    Int_t *index = new Int_t[nentries];
    //sort array containing run in decreasing order
    TMath::Sort(nentries,tree->GetV1(),index);
    
    //open new file to store the sorted Tree
    TFile f2(newName.Data(),"recreate");
    //Create an empty clone of the original tree
    // FIXME: we are losing the TDirectory structure in the file, this can be inproved.
    TTree *tsorted = (TTree*)tree->CloneTree(0);
    for (Int_t i=0;i<nentries;i++) {
      tree->GetEntry(index[i]);
      tsorted->Fill();
    }
    tsorted->Write();
    delete [] index;   
  }







}
