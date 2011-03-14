
#if !defined(__CINT) || defined(__MAKECINT__)

#include "TH1F.h"
#include "TStyle.h"
#include "TString.h"
#include "TFile.h"
#include "TROOT.h"
#include "../interface/Histograms.h"
// #include "../zzllvv_analysis/HistoDiLeptons.hpp"
#include "macros.C"
#include "root_lib/LumiNormalization.h"
#include "root_lib/HistoStack.h"
// #include "HistoAlat.h"
#include <iostream>
#include <string>
#endif



using namespace std;


// -----------------------------------------------------------
//TString baseInputDir = "/castor/cern.ch/cms/store/cmst3/user/cerminar/Analysis/ZZllvv_v01/";
TString inputDir = "/data/Analysis/ZZllvv_v01/";
TString selection = "anal0";

TString XSectionFile = "Xsection_v0.txt";
TString lumiFile = "Luminosity.txt";
TString finalState = "dimu";
bool dqApplied = true;
TString epoch = "all2010";


// -----------------------------------------------------------











void plot() {
  gROOT->LoadMacro("macros.C");


  // --------------------------------
  // set the style
   gStyle->Reset();
  // Get the style and apply it
  TStyle * style = getStyle("d0style");
  //   style->SetOptTitle(1);
  style->SetPadGridX(false);
  style->SetPadGridY(false);
  style->SetOptStat(0);

  style->SetMarkerSize(0.5);
  style->SetTitleOffset(0.85,"X");
  style->SetPadBottomMargin(0.16);
  style->SetPadRightMargin(0.05);

  style->cd(); 
  
  // --------------------------------
  
  vector<TString> samples;
  samples.push_back("dataA");
  samples.push_back("dataB");
  samples.push_back("H400");


  samples.push_back("ZZ");
  samples.push_back("WW");
//   samples.push_back("QCDMu15PU");
//   samples.push_back("TTbarPU");
//   samples.push_back("WJetsPU");
  samples.push_back("ZJetsPU");



  // Get the normalization from MC xsection and overall normalization to the Z peak
  LumiNormalization lumiNorm(XSectionFile, lumiFile,
			     epoch, finalState, dqApplied,"");
  lumiNorm.normalizeToZPeak(false);

  HistoStack *stacker = new HistoStack(0, finalState, "", "");

  stacker->setAxisTitles("muS1Pt","p_{T} [GeV]","GeV");
    //    stacker->setRebin("zmass",2);
  stacker->assignToGroup("dataA", "data");
  stacker->assignToGroup("dataB", "data");
  stacker->assignToGroup("ZJetsPU","z_ll");
  stacker->assignToGroup("ZZ","zz");
  stacker->assignToGroup("WW","ww");
  stacker->assignToGroup("H400","H400");
  stacker->assignToGroup("QCDMu15PU","QCD");
  stacker->assignToGroup("TTbarPU","tt");
  stacker->assignToGroup("WJetsPU","wjets");

  //  stacker->assignToGroup("run2010B", "data");




  stacker->setLegendOrder(0,"data");
  stacker->setLegendOrder(1,"zz");
  stacker->setLegendOrder(2,"ww");
  stacker->setLegendOrder(3,"z_ll");
  stacker->setLegendOrder(4,"H400");
  stacker->setLegendOrder(5,"QCD");
  stacker->setLegendOrder(6,"tt");
  stacker->setLegendOrder(7,"wjets");
  
//   stacker->setLegendOrder(4,"signal");
//   stacker->setLegendOrder(3,"ww_wz");

//   stacker->setLegendOrder(2,"others");

  stacker->setFillColor("signal",626);
  stacker->setFillColor("ww_wz",594);
  stacker->setFillColor("z_ll",410);
  stacker->setFillColor("others",922);
  style->SetMarkerSize(0.8);



  // Loop over all the samples
  for(vector<TString>::const_iterator sName = samples.begin(); sName != samples.end();
      sName++) {

    // Open the file
    TString filePrefix;


    TString fileName = inputDir+ selection +"/ZZllvvAnalyzer_"+ *sName +".root";
    TFile *file = new TFile(fileName.Data());

    float scaleFactor = lumiNorm.getScaleFactor(*sName);
    cout << "--- sample name: " << *sName << " scale factor: " << scaleFactor << endl;    

    HistoLept *hMuonS1 = new HistoLept("MuonS1",file);
    hMuonS1->Scale(scaleFactor);
    stacker->add(*sName, "muS1Pt", hMuonS1->hPt);
    stacker->add(*sName, "muS1Eta", hMuonS1->hEta);
    stacker->add(*sName, "muS1Phi", hMuonS1->hPhi);
    stacker->add(*sName, "muS1Dxy", hMuonS1->hDxy);
    stacker->add(*sName, "muS1Dz", hMuonS1->hDz);
    stacker->add(*sName, "muS1Type", hMuonS1->hType);
    stacker->add(*sName, "muS1NLept", hMuonS1->hNLept);
    stacker->add(*sName, "muS1NPixelHits", hMuonS1->hNPixelHits);
    stacker->add(*sName, "muS1NTkHits", hMuonS1->hNTkHits);
    stacker->add(*sName, "muS1NMuonHits", hMuonS1->hNMuonHits);
    stacker->add(*sName, "muS1NMatches", hMuonS1->hNMatches);

  }
    
  stacker->drawAll();
  cout << "Normalization factor: " << lumiNorm.getNormalizationFactor() << endl;
}
