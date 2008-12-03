
#if !defined(__CINT__)||  defined(__MAKECINT__)
#include "TCanvas.h"
#include "TROOT.h"
#include "TSystem.h"
#include "macros.C"
#include "../src/HistoStationOccupancy.h"
#include "TFile.h"
#include "TGraph.h"
#endif

void plotHistos() {
  gROOT->LoadMacro("macros.C");
  TStyle * style = getStyle("d0style");
  // Style options
  //  style->SetOptStat(0);
  style->SetMarkerSize(1.8);

  style->SetOptStat("eMi");
//   style->SetOptFit(101);
//   style->SetOptTitle(1);
  style->SetLabelSize(0.05, "XYZ");

  style->cd();

  // retrieve the histos from the file
  TFile *file = new TFile("DTOfflineOccupancy_halo.root");
  HistoStationOccupancy *histo_digi_allMB1 = new HistoStationOccupancy("digi_allMB1",file);
  HistoStationOccupancy *histo_digi_allMB1_allSL = new HistoStationOccupancy("digi_allMB1_allSL",file);
  HistoStationOccupancy *histo_digi_allMB1_SL1 = new HistoStationOccupancy("digi_allMB1_SL1",file);
  HistoStationOccupancy *histo_digi_allMB1_SL2 = new HistoStationOccupancy("digi_allMB1_SL2",file);
  HistoStationOccupancy *histo_digi_allMB1_SL3 = new HistoStationOccupancy("digi_allMB1_SL3",file);


  HistoStationOccupancy *histo_digi_allMB2 = new HistoStationOccupancy("digi_allMB2",file);
  HistoStationOccupancy *histo_digi_allMB3 = new HistoStationOccupancy("digi_allMB3",file);
  HistoStationOccupancy *histo_digi_allMB4 = new HistoStationOccupancy("digi_allMB4",file);

  HistoStationOccupancy *histo_1Dhits_allMB1 = new HistoStationOccupancy("1Dhits_allMB1",file);
  HistoStationOccupancy *histo_1Dhits_allMB2 = new HistoStationOccupancy("1Dhits_allMB2",file);
  HistoStationOccupancy *histo_1Dhits_allMB3 = new HistoStationOccupancy("1Dhits_allMB3",file);
  HistoStationOccupancy *histo_1Dhits_allMB4 = new HistoStationOccupancy("1Dhits_allMB4",file);

  HistoStationOccupancy *histo_4Dsegm_allMB1 = new HistoStationOccupancy("4Dsegm_allMB1",file);
  HistoStationOccupancy *histo_4Dsegm_allMB2 = new HistoStationOccupancy("4Dsegm_allMB2",file);
  HistoStationOccupancy *histo_4Dsegm_allMB3 = new HistoStationOccupancy("4Dsegm_allMB3",file);
  HistoStationOccupancy *histo_4Dsegm_allMB4 = new HistoStationOccupancy("4Dsegm_allMB4",file);

  TGraph *hEBEnVsDTDigi = (TGraph *) file->Get("ebVsDTCorr");




  TCanvas *cMB1 = newCanvas("cMB1",3,1,1000,300);
  cMB1->cd(1);
  setStyle(histo_digi_allMB1->hOccup);
  histo_digi_allMB1->hOccup->GetXaxis()->SetTitle("# of digis per chamber");
  histo_digi_allMB1->hOccup->Draw();
  cMB1->cd(2);
  setStyle(histo_1Dhits_allMB1->hOccup);
  histo_1Dhits_allMB1->hOccup->Draw();
  histo_1Dhits_allMB1->hOccup->GetXaxis()->SetTitle("# of hits per chamber");
  cMB1->cd(3);
  setStyle(histo_4Dsegm_allMB1->hOccup);
  histo_4Dsegm_allMB1->hOccup->Draw();
  histo_4Dsegm_allMB1->hOccup->GetXaxis()->SetTitle("# of segments per chamber");

  TCanvas *cMB2 = newCanvas("cMB2",3,1,1000,300);
  cMB2->cd(1);
  setStyle(histo_digi_allMB2->hOccup);
  histo_digi_allMB2->hOccup->GetXaxis()->SetTitle("# of digis per chamber");
  histo_digi_allMB2->hOccup->Draw();
  cMB2->cd(2);
  setStyle(histo_1Dhits_allMB2->hOccup);
  histo_1Dhits_allMB2->hOccup->Draw();
  histo_1Dhits_allMB2->hOccup->GetXaxis()->SetTitle("# of hits per chamber");
  cMB2->cd(3);
  setStyle(histo_4Dsegm_allMB2->hOccup);
  histo_4Dsegm_allMB2->hOccup->Draw();
  histo_4Dsegm_allMB2->hOccup->GetXaxis()->SetTitle("# of segments per chamber");

  TCanvas *cMB3 = newCanvas("cMB3",3,1,1000,300);
  cMB3->cd(1);
  setStyle(histo_digi_allMB3->hOccup);
  histo_digi_allMB3->hOccup->GetXaxis()->SetTitle("# of digis per chamber");
  histo_digi_allMB3->hOccup->Draw();
  cMB3->cd(2);
  setStyle(histo_1Dhits_allMB3->hOccup);
  histo_1Dhits_allMB3->hOccup->Draw();
  histo_1Dhits_allMB3->hOccup->GetXaxis()->SetTitle("# of hits per chamber");
  cMB3->cd(3);
  setStyle(histo_4Dsegm_allMB3->hOccup);
  histo_4Dsegm_allMB3->hOccup->Draw();
  histo_4Dsegm_allMB3->hOccup->GetXaxis()->SetTitle("# of segments per chamber");

  TCanvas *cMB4 = newCanvas("cMB4",3,1,1000,300);
  cMB4->cd(1);
  setStyle(histo_digi_allMB4->hOccup);
  histo_digi_allMB4->hOccup->GetXaxis()->SetTitle("# of digis per chamber");  
  histo_digi_allMB4->hOccup->Draw();
  cMB4->cd(2);
  setStyle(histo_1Dhits_allMB4->hOccup);
  histo_1Dhits_allMB4->hOccup->Draw();
  histo_1Dhits_allMB4->hOccup->GetXaxis()->SetTitle("# of hits per chamber");
  cMB4->cd(3);
  setStyle(histo_4Dsegm_allMB4->hOccup);
  histo_4Dsegm_allMB4->hOccup->Draw();
  histo_4Dsegm_allMB4->hOccup->GetXaxis()->SetTitle("# of segments per chamber");




  TCanvas *cOccupVsSectMB1 = newCanvas("cOccupVsSectMB1","cOccupVsSectMB1",1);
  setStyle(histo_digi_allMB1->hOccupVsSect);
  histo_digi_allMB1->hOccupVsSect->GetXaxis()->SetTitle("Sector");
  histo_digi_allMB1->hOccupVsSect->GetYaxis()->SetTitle("chamber occupancy per event");
  histo_digi_allMB1->hOccupVsSect->Draw("BOX");

  TCanvas *cOccupVsSectMB2 = newCanvas("cOccupVsSectMB2","cOccupVsSectMB2",1);
  setStyle(histo_digi_allMB2->hOccupVsSect);
  histo_digi_allMB2->hOccupVsSect->GetXaxis()->SetTitle("Sector");
  histo_digi_allMB2->hOccupVsSect->GetYaxis()->SetTitle("chamber occupancy per event");
  histo_digi_allMB2->hOccupVsSect->Draw("BOX");

  TCanvas *cOccupVsSectMB3 = newCanvas("cOccupVsSectMB3","cOccupVsSectMB3",1);
  setStyle(histo_digi_allMB3->hOccupVsSect);
  histo_digi_allMB3->hOccupVsSect->GetXaxis()->SetTitle("Sector");
  histo_digi_allMB3->hOccupVsSect->GetYaxis()->SetTitle("chamber occupancy per event");
  histo_digi_allMB3->hOccupVsSect->Draw("BOX");

  TCanvas *cOccupVsSectMB4 = newCanvas("cOccupVsSectMB4","cOccupVsSectMB4",1);
  setStyle(histo_digi_allMB4->hOccupVsSect);
  histo_digi_allMB4->hOccupVsSect->GetXaxis()->SetTitle("Sector");
  histo_digi_allMB4->hOccupVsSect->GetYaxis()->SetTitle("chamber occupancy per event");
  histo_digi_allMB4->hOccupVsSect->Draw("BOX");


  
  TCanvas *cMB1SLs = newCanvas("cMB1SLs","cMB1SLs",1);
  setStyle(histo_digi_allMB1_allSL->hOccup);
  histo_digi_allMB1_allSL->hOccup->Draw();

  histo_digi_allMB1_SL1->hOccup->Add(histo_digi_allMB1_SL3->hOccup);
  histo_digi_allMB1_SL1->hOccup->SetLineColor(2);
  setStyle(histo_digi_allMB1_SL1->hOccup);
  histo_digi_allMB1_SL1->hOccup->Draw("same");
  setStyle(histo_digi_allMB1_SL2->hOccup);
  histo_digi_allMB1_SL2->hOccup->SetLineColor(kBlue);
  histo_digi_allMB1_SL2->hOccup->Draw("same");

  TCanvas *cEBEnVsDTDigi =  newCanvas("cEBEnVsDTDigi","cEBEnVsDTDigi",1);
  hEBEnVsDTDigi->SetMarkerStyle(20);
  hEBEnVsDTDigi->SetMarkerSize(1.);
  hEBEnVsDTDigi->Draw("AP");



}
