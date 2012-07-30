{ 

  gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/RunLumiIndex.cc+g");
  gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/RunLumiBXIndex.cc+g");
  gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/LumiFileReaderByBX.cc+g");
  LumiFileReaderByBX reader("/data1/ZLumiStudy/CalcLumi/Version0/");

  int run = 194210;

  reader.readFileForRun(run);

  TH1F* histDel = new TH1F("DelLumi", "; differnce [GeV]; Events", 100, -1, 25);
  TH1F* histRec = new TH1F("RecLumi", "; differnce [GeV]; Events", 100, -1, 25);
  
  int nLSs = reader.getNumberLSs(run);
  cout << "# LSs:  " << nLSs << endl;

  float del_all = 0;

  RunLumiIndex startDel;
  RunLumiIndex endDel;

    for (int ls = 1; ls <= nLSs; ls++) {
      //int nBX = reader.getNumberBX(run, ls);
      startDel = RunLumiIndex(run, ls);
      endDel = RunLumiIndex(run, ls);

      float sumDel_all = reader.getDelIntegral(startDel, endDel);
      float sumRec_all = reader.getRecIntegral(startDel, endDel);

      pair<float, float> totalLumi = reader.getTotalLumi(RunLumiIndex(run, ls));

      float diff_Del = (sumDel_all * 23. - totalLumi.first) / totalLumi.first;
      float diff_Rec = (sumRec_all * 23. - totalLumi.second) / totalLumi.second;

      if (diff_Del > 10) {
        cout << "diff_Del too big for run : ls " << run << " : " << ls << endl;
      }
      if (diff_Rec > 10) {
        cout << "diff_Rec too big for run : ls " << run << " : " << ls << endl;
      }

      histDel->Fill(diff_Del);
      histRec->Fill(diff_Rec);
    }

    histDel->Draw();

    TCanvas *c2 = new TCanvas("c2", "", 600, 600);
    histRec->Draw();
    

 /* for(int ls = 3; ls <= 3; ++ls) { // loop over all the LSs
    for(int bx = 0; bx <= 50; ++bx) {
     RunLumiBXIndex index(run, ls, bx);
      
      cout << "run " << run << " ls " << ls << " bx " << bx << endl;
      cout << "    del lumi: " << reader.getDelLumi(index) << endl; */
//
//      //float getRecLumi(const RunLumiBXIndex& runAndLumiAndBx) const;
//  
//      //float getAvgInstLumi(const RunLumiBXIndex& runAndLumiAndBx) const;
      
    }
  }



}
