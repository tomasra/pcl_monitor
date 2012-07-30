
void runTreeReader() {
 
 if (! TString(gSystem->GetLibraries()).Contains("ZlumiTreeReader")) {
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/RunLumiIndex.cc+g");
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/RunLumiBXIndex.cc+g");
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/LumiFileReaderByBX.cc+g");
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/ZlumiTreeReader.C+g");
  }
  
  int maxRunNumber = 5;
  int run_Number = 0;

  TChain* chain = new TChain("Z2muTree/candTree");  // change in "candTree" when using the sorted-root-Files
  chain->Add("/data1/d/dboerner/test/ZLumiStudy.root");
 /* chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuA/ZLumiStudy.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB1/ZLumiStudy.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB2/ZLumiStudy.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB3/ZLumiStudy.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB4/ZLumiStudy.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB5/ZLumiStudy.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB6/ZLumiStudy.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB7/ZLumiStudy.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB8/ZLumiStudy.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB9/ZLumiStudy.root"); */

  TSelector *selector = TSelector::GetSelector("ZlumiTreeReader");

/*  const TString fileName = "/afs/cern.ch/user/d/dboerner/workspace/Zlumi/CMSSW_5_2_6/src/MyAnalysis/ZLumiStudy/test/macros/runnumberSorted.txt";
  ifstream file(fileName.Data());
  string line;
  while (getline(file,line) && run_Number < maxRunNumber) {
    stringstream linestr;
    linestr << line;
    run_Number ++;
    chain->Process(selector, line.c_str());
  }  */
  
  //   selector->Select()
  chain->Process(selector, "194210");

}
