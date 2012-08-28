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



  //#include "SingleMu_Run2012B-PromptReco-v1.h"

//#include "test.h"
vector<TString> fileBaseNames;
TString outDir = "";
TString inputDir = "";



void sortTPTrees() {

// 2012A
 // gROOT->Macro("TPV0_SingleMu_Run2012A-PromptReco-v1.h");
 // outDir = TString("/data1/ZLumiStudy/TagProbe/SingleMu_Run2012A-PromptReco-v1/");
// 2012B
    gROOT->Macro("TPV0_SingleMu_Run2012B-PromptReco-v1.h");
    outDir = TString("/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1/");
  
  cout << "Input dir: " << inputDir << endl;
  cout << "Output dir: " << outDir << endl;
  cout << "# of files to be sorted: " << fileBaseNames.size() << endl;
  

//   fileBaseNames.push_back("/data/Analysis/42X_BX_v0/DoubleMu-05Aug2011");
//   fileBaseNames.push_back("/data/Analysis/42X_BX_v0/DoubleMu-PromptReco-v6");
//   fileBaseNames.push_back("/data/Analysis/42X_BX_v0/SingleMu-05Aug2011");
//   fileBaseNames.push_back("/data/Analysis/42X_BX_v0/SingleMu-PromptReco-v4");
//   fileBaseNames.push_back("/data/Analysis/42X_BX_v0/SingleMu-May10ReReco");
//   fileBaseNames.push_back("/data/Analysis/42X_BX_v0/SingleMu-PromptReco-v6");



  for(vector<TString>::const_iterator basename = fileBaseNames.begin();
      basename != fileBaseNames.end(); ++basename) {
    
    TString oldName = inputDir + (*basename) + ".root";
    TString newName = outDir + (*basename) + "_sorted.root";

    cout << "Input: " << oldName << endl;
    cout << "Output: " << newName << endl;

    TFile *oldFile = TFile::Open(oldName.Data());

    oldFile->cd("tpTree");
    TTree *tree = (TTree*) gDirectory->Get("fitter_tree");
    cout << "opened tree: " << tree->GetName() << " with " << tree->GetEntries() << " entries" << endl;

    tree->SetEstimate(tree->GetEntries()+1);  // very important!!!
    
    Int_t nentries = (Int_t)tree->GetEntries();

    //Drawing variable RunNumber with no graphics option.
    //variable RunNumber stored in array fV1 (see TTree::Draw)
    tree->Draw("run","","goff");
    Int_t *index = new Int_t[nentries];
    //sort array containing run in decreasing order
    TMath::Sort(nentries,tree->GetV1(),index);
    
    //open new file to store the sorted Tree
    TFile sortedFile(newName.Data(),"recreate");
    sortedFile.mkdir("tpTree");
    sortedFile.cd("tpTree");
    //Create an empty clone of the original tree
    // FIXME: we are losing the TDirectory structure in the file, this can be inproved.
    TTree *tsorted = (TTree*)tree->CloneTree(0);
    for (Int_t i=0;i<nentries;i++) {
      tree->GetEntry(index[i]);
      tsorted->Fill();
    }
    tsorted->Write();
    delete [] index;   
    oldFile->Close();
    
  }







}
