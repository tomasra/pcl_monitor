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

  // all runs 2012 A or B
  string run2012A = "run2012A:190645,190646,190659,190679,190688,190702,190703,190704,190705,190706,190707,190708,190710,190733,190736,190738,191043,191046,191056,191057,191062,191090,191201,191202,191226,191247,191248,191264,191271,191276,191277,191367,191411,191691,191695,191718,191720,191721,191726,191800,191810,191811,191830,191833,191834,191837,191839,191842,191845,191849,191856,191857,191858,191859,193093,193112,193123,193124,193192,193193,193207,193334,193336,193541,193556,193557,193575,193621";
  string run2012B = "run2012B:193834,193835,193836,193998,193999,194027,194050,194051,194052,194075,194076,194108,194115,194117,194119,194120,194150,194151,194153,194199,194210,194223,194224,194225,194270,194303,194304,194305,194314,194315,194317,194424,194428,194429,194439,194455,194464,194479,194480,194533,194619,194631,194643,194644,194691,194699,194702,194704,194711,194712,194735,194778,194789,194790,194825,194896,194897,194912,194914,194915,195013,195014,195015,195016,195099,195109,195110,195111,195112,195113,195114,195115,195147,195163,195164,195165,195251,195265,195266,195303,195304,195378,195390,195396,195397,195398,195399,195529,195530,195540,195551,195552,195633,195634,195644,195645,195647,195649,195655,195656,195658,195749,195757,195758,195774,195775,195776,195841,195868,195915,195916,195917,195918,195919,195923,195925,195926,195929,195930,195937,195947,195948,195950,195963,195970,196019,196027,196046,196047,196048,196197,196199,196200,196202,196203,196218,196239,196249,196250,196252,196334,196349,196357,196359,196362,196363,196364,196437,196438,196452,196453,196495,196509,196531";

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
  chain->Process(selector, run2012B.c_str());


}
