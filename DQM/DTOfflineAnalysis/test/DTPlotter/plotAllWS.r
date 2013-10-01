void plotAllWS(TString filename, int sector, int sl) {

   if (! TString(gSystem->GetLibraries()).Contains("DTDetId_cc")) {
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/Histograms.h");
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/DTDetId.cc+");
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/Utils.cc+");
     gROOT->LoadMacro("macros2.C");
   }


   bool doResVsDist = true;
   bool doResVsAngle = false;

   

  TStyle * style = getStyle("tdr");
  style->cd();  
  setPalette();
  opt2Dplot = "col";
  float nsigma = 2;

  TFile *file = new TFile(filename);


  HRes1DHits* hRes[5][4]; // W, S;  
  for (int wheel = -2; wheel<=2; ++wheel) {
    for (int station = 1; station<=3; ++station) {
      int iW = wheel+2;
      int iSt= station-1;
      DTDetId detId2(wheel, station, sector, sl, 0, 0);
      hRes[iW][iSt] = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId2, "Cut1"),file);
    }
  }


  if (doResVsDist) {
    TCanvas* c1= new TCanvas("c1",filename+"_AllWSResVsDist",1375,800);
    c1->Divide(5,3);


    for (int wheel = -2; wheel<=2; ++wheel) {
      for (int station = 1; station<=3; ++station) {
	int iW = wheel+2;
	int iSt= station-1;

	int ipad=iW+1 + (2-iSt)*5;
	c1->cd(ipad); ++ipad;
	plotAndProfileX(hRes[iW][iSt]->hResDistVsDist,1,1,1,-.1, .1, 0, 2.1);
      }
    }
  }
  

  if (doResVsAngle) {
    TCanvas* c1= new TCanvas("c1",filename+"_AllWSResVsAngle",1375,800);
    c1->Divide(5,3);


    for (int wheel = -2; wheel<=2; ++wheel) {
      for (int station = 1; station<=3; ++station) {
	int iW = wheel+2;
	int iSt= station-1;

	int ipad=iW+1 + (2-iSt)*5;
	c1->cd(ipad); ++ipad;
	plotAndProfileX(hRes[iW][iSt]->hResDistVsDist,1,1,1,-.1, .1, 0, 2.1); // FIXME
      }
    }
  }



}

