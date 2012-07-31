{ 

  gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/RunLumiIndex.cc+g");
  gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/RunLumiBXIndex.cc+g");
  gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/LumiFileReaderByBX.cc+g");
  LumiFileReaderByBX reader("/data1/ZLumiStudy/CalcLumi/Version0/");

  int run = 194210;
  const float LENGTH_LS = 1.0e18 / 11246; 
  cout << LENGTH_LS << endl;

  reader.readFileForRun(run);
  if (!reader.check_RunFound(run)) {
    cout << "run " << run << " not found " << endl;
    return 0;
  }


  TH1F* histDel = new TH1F("DelLumi", "; difference; Events", 100, 0, 0.05);
  TH1F* histDelLumi = new TH1F("DelLumiDiff", "; difference; Events", 100, 500, 3500);
  TH1F* histRec = new TH1F("RecLumi", "; difference; Events", 100, 0, 0.05);
  TH1F* histRecLumi = new TH1F("RecLumiDiff", "; difference; Events", 100, 500, 3500);
  TH2F* hist_ls_delLumi = new TH2F("ls_Lumi", "; ls; difference", 555, 0, 555, 100, 1000, 3500);
  TH2F* hist_ls_recLumi = new TH2F("ls_recLumi", "; ls; difference", 555, 0, 555, 100, 1000, 3500);
  
  int nLSs = reader.getNumberLSs(run);
  cout << "# LSs:  " << nLSs << endl;

  float del_all = 0;

  RunLumiIndex startDel;
  RunLumiIndex endDel;


    for (int ls = 1; ls <= nLSs; ls++) {
      //int nBX = reader.getNumberBX(run, ls);

      if (!reader.check_LSFound(RunLumiIndex(run,ls))) {
        cout << "LS " << ls << " for run " << run << " not found" << endl;
        continue;
      }

      startDel = RunLumiIndex(run, ls);
      endDel = RunLumiIndex(run, ls);

      float sumDel_all = reader.getDelIntegral(startDel, endDel);
      float sumRec_all = reader.getRecIntegral(startDel, endDel);

      pair<float, float> totalLumi = reader.getTotalLumi(RunLumiIndex(run, ls));

      float diff_Del = (sumDel_all * LENGTH_LS - totalLumi.first);
      float diff_Rec = (sumRec_all * LENGTH_LS - totalLumi.second);
    
      histDel->Fill(diff_Del / totalLumi.first);
      histDelLumi->Fill(diff_Del);
      histRec->Fill(diff_Rec / totalLumi.second);
      histRecLumi->Fill(diff_Rec);
      hist_ls_delLumi->Fill(ls, diff_Del);
      hist_ls_recLumi->Fill(ls, diff_Rec);
    }

    TCanvas* c1 = new TCanvas("DelLumi", "DelLumi", 1200, 600);
    c1->Divide(2,1);
    c1->cd(1);
    histDelLumi->Draw();
    c1->cd(2);
    histDel->Draw();
    c1->Update();

    TCanvas *c2 = new TCanvas("RecLumi", "RecLumi", 1200, 600);
    c2->Divide(2,1);
    c2->cd(1);
    histRecLumi->Draw();
    c2->cd(2);
    histRec->Draw();
    c2->Update();

    TCanvas* c3 = new TCanvas("ls_Lumi", "ls_Lumi");
    hist_ls_delLumi->Draw();

    TCanvas* c3 = new TCanvas("ls_recLumi", "ls_recLumi");
    hist_ls_recLumi->Draw();
    

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
