{  
  gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/RunLumiBXIndex.cc+");
  gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/LumiFileReaderByBX.cc+");
  LumiFileReaderByBX reader("/data1/ZLumiStudy/CalcLumi/Version0/");

  int run = 194210;

  reader.readFileForRun(run);
  
  int nLSs = reader.getNumberLSs(run);
  cout << "# LSs:  " << nLSs << endl;
  
  for(int ls = 0; ls != nLSs; ++ls) { // loop over all the LSs
    for(int bx = 0; bx != 3650; ++bx) {
      RunLumiBXIndex index(run, ls, bx);
      
      cout << "run " << run << " ls " << ls << " bx " << bx << endl;
      cout << "    del lumi: " << reader.getDelLumi(index) << endl;

      //float getRecLumi(const RunLumiBXIndex& runAndLumiAndBx) const;
  
      //float getAvgInstLumi(const RunLumiBXIndex& runAndLumiAndBx) const;
      
    }
  }



}
