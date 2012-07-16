


void runTreeReader() {
 
   if (! TString(gSystem->GetLibraries()).Contains("ZlumiTreeReader")) {
     gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/ZlumiTreeReader.C+");
   }
  
  TFile *file = new TFile("/data1/d/dboerner/test/ZLumiStudy.root","r");
  TTree *tree = (TTree *) file->Get("Z2muTree/candTree");
  tree->Process("ZlumiTreeReader.C+");

}
