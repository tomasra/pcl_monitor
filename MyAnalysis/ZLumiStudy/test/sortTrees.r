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
  
    //fileBaseNames.push_back("/afs/cern.ch/user/d/dboerner/workspace/Zlumi/CMSSW_5_2_6/src/MyAnalysis/ZLumiStudy/test/files/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB1/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB2/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB3/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB4/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB5/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB6/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB7/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB8/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB9/ZLumiStudy");

  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/DoubleMuA/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/DY10_NoB/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/DY50_NoB/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/WJetsToLNu/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/WZ/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/ZZ2e2mu/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/ZZ2e2tau/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/ZZ2mu2tau/ZLumiStudy");
  fileBaseNames.push_back("/data1/ZLumiStudy/PROD120716_v0/ZZ4mu/ZLumiStudy");



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
    tree->SetEstimate(tree->GetEntries()+1);  // very important!!!
    
    Int_t nentries = (Int_t)tree->GetEntries();

    //Drawing variable RunNumber with no graphics option.
    //variable RunNumber stored in array fV1 (see TTree::Draw)
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
