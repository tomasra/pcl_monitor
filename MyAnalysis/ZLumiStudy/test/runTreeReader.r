


void runTreeReader() {
 
  if (! TString(gSystem->GetLibraries()).Contains("ZlumiTreeReader")) {
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/RunLumiBXIndex.cc+");
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/LumiFileReaderByBX.cc+");
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/ZlumiTreeReader.C+");
  }
  

  TFile *file = new TFile("/data1/d/dboerner/test/ZLumiStudy.root","r");
  TTree *tree = (TTree *) file->Get("Z2muTree/candTree");

  // FIXME: here implement a mechanism to select the input files (and possibli chain them) on the basis of the samples
  
  

  TSelector *selector = TSelector::GetSelector("ZlumiTreeReader");
  //   selector->Select()
  tree->Process(selector, "");

}
