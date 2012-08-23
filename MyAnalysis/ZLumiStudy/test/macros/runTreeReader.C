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
  
  bool do_all = false;
  int maxRunNumber = 5;
  int run_Number = 0;

  TChain* chain = new TChain("candTree");
  
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

  // all runs from the presentation
  string pres = "presentationRuns:194050,194051,194052,194424,194428,194429,194455,194464,194479,194480,194691,194699,194702,194711,194712,195396,195397,195398,195399,195947,195950,196452,196453";

  // all runs
  const TString fileName = "/afs/cern.ch/user/d/dboerner/workspace/Zlumi/CMSSW_5_2_6/src/MyAnalysis/ZLumiStudy/test/macros/runnumberSorted.txt";
  ifstream file(fileName.Data());
  string line;
  string all = "allRuns";
  if (!do_all) {
    all += "_";
    all += to_string(maxRunNumber);
  }
  all += ":";

  while (getline(file,line) && (run_Number < maxRunNumber || do_all)) {
    stringstream linestr;
    linestr << line;
    run_Number ++;
    all += line;
    all += ",";
  }
  all = all.substr(0, all.length() - 1);


// select one special <runnumber>, pres.c_str() or all.c_str()
  chain->Process(selector, "194210");


}
