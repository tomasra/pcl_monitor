string to_string(int i)
{
    stringstream sstr;
    sstr << i;
    return sstr.str();
} 



void runTreeReader() {
  gSystem->AddIncludePath("-I$ROOFITSYS/include");
 if (! TString(gSystem->GetLibraries()).Contains("ZlumiTreeReader")) {
    

    gSystem->Load("libRooFit");
  
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/RunLumiIndex.cc+g");
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/RunLumiBXIndex.cc+g");
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/LumiFileReaderByBX.cc+g");

    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/ZPeakFit.C+g");
    gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/ZlumiTreeReader.C+g");
  }
  
  int maxRunNumber = 1;
  int run_Number = 0;

  TChain* chain = new TChain("candTree");  // change in "candTree" when using the sorted-root-Files
  //chain->Add("/data1/d/dboerner/test/ZLumiStudy.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuA/ZLumiStudy_sorted.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB1/ZLumiStudy_sorted.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB2/ZLumiStudy_sorted.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB3/ZLumiStudy_sorted.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB4/ZLumiStudy_sorted.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB5/ZLumiStudy_sorted.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB6/ZLumiStudy_sorted.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB7/ZLumiStudy_sorted.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB8/ZLumiStudy_sorted.root");
  chain->Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB9/ZLumiStudy_sorted.root");

  TSelector *selector = TSelector::GetSelector("ZlumiTreeReader.C+");
    //   selector->Select()

  int runs[23] = {194050, 194051, 194052, 194424, 194428, 194429, 194455, 194464, 194479, 194480, 194691, 194699, 194702, 194711, 194712, 195396, 195397, 195398, 195399, 195947, 195950, 196452, 196453};

// run over all or some runs
 /* const TString fileName = "/afs/cern.ch/user/d/dboerner/workspace/Zlumi/CMSSW_5_2_6/src/MyAnalysis/ZLumiStudy/test/macros/runnumberSorted.txt";
  ifstream file(fileName.Data());
  string line;
  while (getline(file,line) && run_Number < maxRunNumber) {
    TSelector *selector = TSelector::GetSelector("ZlumiTreeReader.C+");
    stringstream linestr;
    linestr << line;
    run_Number ++;
    chain->Process(selector, line.c_str());
  } */

// run over special runs
  for (size_t i = 0; i < 23 ; i++) {
 //   TSelector* selector = TSelector::GetSelector("ZlumiTreeReader.C+");
    cout << runs[i] << endl;
    chain->Process(selector, to_string(runs[i]).c_str());
  } 
  


// run over one run
 // chain->Process(selector, "194210");


}
