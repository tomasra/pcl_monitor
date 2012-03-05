
#if !defined(__CINT) || defined(__MAKECINT__)

#include "TH1F.h"
#include "TStyle.h"
#include "TString.h"
#include "TFile.h"
#include "TROOT.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "TGraphErrors.h"

//#include "macros.C"
//#include "root_lib/LumiFileReader.h"

// #include "HistoAlat.h"
#include <iostream>
#include <string>
#include <vector>
#endif


bool doOverlap = true;

// Usage: .x plot.r
// Simple macro that draws the results from the root files produced by the previus step

void plot() {
  gROOT->LoadMacro("macros.C");
  // set the style
   gStyle->Reset();
  // Get the style and apply it
  TStyle * style = getStyle("tdr");
  //   style->SetOptTitle(1);
  style->SetPadGridX(false);
  style->SetPadGridY(false);
  style->SetOptStat(0);

  style->SetMarkerSize(0.5);
  style->SetTitleOffset(0.85,"X");
  style->SetPadBottomMargin(0.16);
  style->SetPadRightMargin(0.05);
  style->SetPalette(1);
  style->cd(); 

  TFile *file_lc1 = new TFile("outFile_lc1.root");
  TFile *file_lc2 = new TFile("outFile_lc2.root");

  
  TGraphErrors *gSigma = (TGraphErrors*) file_lc1->Get("gSigma");
  TGraphErrors *gSigma_2 = 0; 
  if(doOverlap) gSigma_2 = (TGraphErrors*) file_lc2->Get("gSigma");
  newCanvas("c_gSigma", "c_gSigma");
  gSigma->SetMarkerStyle(20);
  gSigma->Draw("AP");
  if(gSigma_2 != 0) {
    gSigma_2->SetMarkerColor(kRed);
    gSigma_2->SetMarkerStyle(20);
    gSigma_2->Draw("P");
  }
  //gSigma->GeYaxis()->SetTitle("effective x-sec [ub]");
  
  TH1F *hSigma = (TH1F*)  file_lc1->Get("hSigma");
  newCanvas("c_hSigma", "c_hSigma");
  hSigma->Draw();
  hSigma->GetYaxis()->SetTitle("effective x-section [ub]");

  TH1F *hEventPerLumi = (TH1F*)  file_lc1->Get("hEventPerLumi");
  TH1F *hEventPerLumi_2 = 0;
  if(doOverlap) hEventPerLumi_2 = (TH1F*)  file_lc2->Get("hEventPerLumi");
  newCanvas("c_hEventPerLumi", "c_hEventPerLumi");
  hEventPerLumi->Draw();
  hEventPerLumi->GetYaxis()->SetTitle("# events");
  if(hEventPerLumi_2 != 0) {
    hEventPerLumi_2->SetLineColor(kRed);
    hEventPerLumi_2->Draw("same");
  }
  TH1F *hRecLumiInteg = (TH1F*)  file_lc1->Get("hRecLumiInteg");
  TH1F *hRecLumiInteg_2 = 0;
  if(doOverlap) hRecLumiInteg_2 = (TH1F*)  file_lc2->Get("hRecLumiInteg");
  newCanvas("c_hRecLumiInteg", "c_hRecLumiInteg");
  hRecLumiInteg->Draw();
  hRecLumiInteg->GetYaxis()->SetTitle("recorded lumi [1/ub]");
  hRecLumiInteg->GetXaxis()->SetTitle("avg. inst. lumi [Hz/ub]");
  if(hRecLumiInteg_2 != 0) {
    hRecLumiInteg_2->SetLineColor(kRed);
    hRecLumiInteg_2->Draw("same");
  }
  //  newCanvas("c_gSigma", "c_gSigma");

}
