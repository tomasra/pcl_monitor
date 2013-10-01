void plot12s(TString filename, int wheel, int station, int sl, int layer) {

   if (! TString(gSystem->GetLibraries()).Contains("DTDetId_cc")) {
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/Histograms.h");
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/DTDetId.cc+");
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/Utils.cc+");
     gROOT->LoadMacro("macros2.C");
   }

 
  //  TStyle * style = getStyle("myStyle");
  TStyle * style = getStyle("tdr");
  style->cd();  
  gStyle->SetPalette(5);
  gStyle->SetStatFormat("4.3g");
  gStyle->SetFitFormat("4.3g");
    opt2Dplot = "col";
    //opt2Dplot = "";

  TFile *file = new TFile(filename);

  gStyle->SetStatFormat("2.1g");

  HRes1DHits* hResTheta[13];
  for (int sector = 1; sector<=12; ++sector) {
    DTDetId detId2(wheel, station, sector, sl, layer, 0);
    hResTheta[sector] = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId2, "Cut1"),file);
  }
  

  float nsigma = 2;

  

  TCanvas* c1= new TCanvas("c1",filename+"_Theta",1100,800);
  c1->Divide(4,3);
  

  for (int sector = 1; sector<=12; ++sector) {  
    c1->cd(sector);
    hResTheta[sector]->hResDist->Rebin(2);
    //    hResTheta[sector]->hResDist->SetTitle("");
    TF1* fphi=drawGFit(hResTheta[sector]->hResDist, nsigma, -0.3, 0.3); 
  }
}
