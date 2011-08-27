
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

  TFile *file = new TFile("outFile.root");
  
  TGraphErrors *gSigma = (TGraphErrors*) file->Get("gSigma");
  newCanvas("c_gSigma", "c_gSigma");
  gSigma->SetMarkerStyle(20);
  gSigma->Draw("AP");
  //gSigma->GeYaxis()->SetTitle("effective x-sec [ub]");
  
  TH1F *hSigma = (TH1F*)  file->Get("hSigma");
  newCanvas("c_hSigma", "c_hSigma");
  hSigma->Draw();
  hSigma->GetYaxis()->SetTitle("effective x-section [ub]");

  TH1F *hEventPerLumi = (TH1F*)  file->Get("hEventPerLumi");
  newCanvas("c_hEventPerLumi", "c_hEventPerLumi");
  hEventPerLumi->Draw();
  hEventPerLumi->GetYaxis()->SetTitle("# events");

  TH1F *hRecLumiInteg = (TH1F*)  file->Get("hRecLumiInteg");
  newCanvas("c_hRecLumiInteg", "c_hRecLumiInteg");
  hRecLumiInteg->Draw();
  hRecLumiInteg->GetYaxis()->SetTitle("recorded lumi [1/ub]");
  hRecLumiInteg->GetXaxis()->SetTitle("avg. inst. lumi [Hz/ub]");

  //  newCanvas("c_gSigma", "c_gSigma");

}
