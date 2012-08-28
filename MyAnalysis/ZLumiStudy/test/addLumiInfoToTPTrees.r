#if !defined(__CINT) || defined(__MAKECINT__)

#include "macros/RunLumiIndex.h"
#include "macros/RunLumiBXIndex.h"
#include "macros/LumiFileReaderByBX.h"
#include "TFile.h"
#include "TTree.h"
#include "TBranch.h"
#include <iostream>
#include "TROOT.h"
#include "TSystem.h"
//#include <string>
//#include <vector>
#endif         

using namespace std;

vector<TString> fileBaseNames;
TString outDir = "";
TString inputDir = "";



void addLumiInfoToTPTrees() {
 
  if (! TString(gSystem->GetLibraries()).Contains("RunLumiIndex")) {
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/RunLumiIndex.cc+");
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/RunLumiBXIndex.cc+");
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/LumiFileReaderByBX.cc+");
  }
  
  LumiFileReaderByBX lumiReader("/data1/ZLumiStudy/CalcLumi/Version0/");

  // ----- SETTINGS ------------------------------------
  gROOT->Macro("TPV0_SingleMu_Run2012A-PromptReco-v1_sorted.h");
  outDir = TString("/data1/ZLumiStudy/TagProbe/SingleMu_Run2012A-PromptReco-v1_lumi/");
  // ----- END SETTINGS ------------------------------------


  cout << "Input dir: " << inputDir << endl;
  cout << "Output dir: " << outDir << endl;
  cout << "# of files to be sorted: " << fileBaseNames.size() << endl;

  for(vector<TString>::const_iterator basename = fileBaseNames.begin();
      basename != fileBaseNames.end(); ++basename) {

    
    TString oldFileName = inputDir + (*basename) + ".root";
    TString newFileName = outDir + (*basename) + "_lumi.root";
    
    
    TFile *oldFile = new TFile(oldFileName.Data());
    TTree *oldTree = (TTree *) oldFile->Get("tpTree/fitter_tree");
    cout << "------" << endl;
    cout << "Old file: " << oldFileName << endl;
    cout << "New file: " << newFileName << endl;
    cout << "# entries orig. tree: " << oldTree->GetEntries() << endl;
    TFile *newFile = new TFile(newFileName.Data(), "recreate");
    newFile->mkdir("tpTree");
    newFile->cd("tpTree");
    TTree *tree = (TTree*)oldTree->CloneTree();
    
    float bxInstLumi = -1;

    TBranch *br=tree->Branch("bxInstLumi",&bxInstLumi,"bxInstLumi/F");
    int entries = tree->GetEntries();
    cout << "# entries: " << entries << endl;

    unsigned int run = 0;
    unsigned int ls = 0;
    unsigned int bx = 0;
    tree->SetBranchAddress("run",&run);
    tree->SetBranchAddress("lumi",&ls);
    tree->SetBranchAddress("bx",&bx);


    for(int entry = 0; entry != entries; ++entry) {
      tree->GetEntry(entry);
      
      //     cout << "entry: " << entry << endl;
      //     cout << "run: " << run << " ls: " << ls << " bx: " << bx << endl;
      lumiReader.readFileForRun(run);
      RunLumiBXIndex lumiBXIndex = RunLumiBXIndex(run, ls, bx);
      float avgLumi = lumiReader.getAvgInstLumi(lumiBXIndex);
      bxInstLumi = avgLumi;
      

      tree->Fill();
    }
    
    tree->SetEntries(br->GetEntries());

    newFile->cd("tpTree");
    tree->Write();
    newFile->Write();
    newFile->Close();
    oldFile->Close();

  }




//   TTree *tree = (TTree *) file->Get("tpTree/fitter_tree");
//   /*

//     TFile sortedFile(newName.Data(),"recreate");
//     sortedFile.mkdir("tpTree");
//     sortedFile.cd("tpTree");
//     //Create an empty clone of the original tree
//     // FIXME: we are losing the TDirectory structure in the file, this can be inproved.
//     TTree *tsorted = (TTree*)tree->CloneTree(0);
//   */

//   float bxInstLumi = -1;

//   TBranch *br=tree->Branch("bxInstLumi",&bxInstLumi,"bxInstLumi/F");
//   int entries = tree->GetEntries();
//   cout << "# entries: " << entries << endl;

//   unsigned int run = 0;
//   unsigned int ls = 0;
//   unsigned int bx = 0;
//   tree->SetBranchAddress("run",&run);
//   tree->SetBranchAddress("lumi",&ls);
//   tree->SetBranchAddress("bx",&bx);


//   for(int entry = 0; entry != entries; ++entry) {
//     tree->GetEntry(entry);

//     //     cout << "entry: " << entry << endl;
//     //     cout << "run: " << run << " ls: " << ls << " bx: " << bx << endl;
//     lumiReader.readFileForRun(run);
//     RunLumiBXIndex lumiBXIndex = RunLumiBXIndex(run, ls, bx);
//     float avgLumi = lumiReader.getAvgInstLumi(lumiBXIndex);
//     bxInstLumi = avgLumi;


//     tree->Fill();
//   }

//   tree->SetEntries(br->GetEntries());

//   file->Write();

//   file->Close();

	
}
