#define ROOTANALYSIS
#if !defined(__CINT) || defined(__MAKECINT__)

#include "TH1F.h"
#include "TStyle.h"
#include "TString.h"
#include "TFile.h"
#include "TROOT.h"
#include "../src/Histograms.h"
// #include "../zzllvv_analysis/HistoDiLeptons.hpp"
#include "macros.C"
// #include "root_lib/LumiNormalization.h"
// #include "root_lib/HistoStack.h"
// #include "root_lib/SampleGroup.h"
// #include "root_lib/CutTableBuilder.h"

// #include "HistoAlat.h"
#include <iostream>
#include <string>
#endif



using namespace std;


// -----------------------------------------------------------
//TString baseInputDir = "/castor/cern.ch/cms/store/cmst3/user/cerminar/Analysis/ZZllvv_v01/";
// -----------------------------------------------------------





void plotPtBins(const TH2F* histo) {
  TCanvas *cMuLeadPtBins = newCanvas("cMuLeadPtBins","cMuLeadPtBins");
  cMuLeadPtBins->SetLogy();
  TH1D *hProj_all = histo->ProjectionX("hProj_all",0,100);
  hProj_all->Draw("hist");
  
  TH1D *hProj_10 = histo->ProjectionX("hProj_10",20,100);
  hProj_10->SetLineColor(2);
  hProj_10->Draw("hist,same");

  TH1D *hProj_12 = histo->ProjectionX("hProj_12",24,100);
  hProj_12->SetLineColor(4);
  hProj_12->Draw("hist,same");


  
}


void plotPtBinsTrail(const TH2F* histo) {
  TCanvas *cMuTrailPtBins = newCanvas("cMuTrailPtBins","cMuTrailPtBins");
  cMuTrailPtBins->SetLogy();
  TH1D *hProj_all = histo->ProjectionX("hProj_all",0,100);
  hProj_all->Draw("hist");
  
  TH1D *hProj_10 = histo->ProjectionX("hProj_10",20,100);
  hProj_10->SetLineColor(2);
  hProj_10->Draw("hist,same");

  TH1D *hProj_12 = histo->ProjectionX("hProj_12",24,100);
  hProj_12->SetLineColor(4);
  hProj_12->Draw("hist,same");


  
}




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
  style->SetPalette(1);
  style->cd(); 
  
  // --------------------------------
  
  vector<TString> samples;
  samples.push_back("GenLevelAnalysis.root");


  TCanvas *cTauPt = newCanvas("cTauPt","cTauPt");
  TCanvas *cTauEta = newCanvas("cTauEta","cTauEta");

  TCanvas *cDsPt = newCanvas("cDsPt","cDsPt");
  TCanvas *cDsEta = newCanvas("cDsEta","cDsEta");

  TCanvas *cRecoDsPt = newCanvas("cRecoDsPt","cRecoDsPt");
  TCanvas *cRecoDsEta = newCanvas("cRecoDsEta","cRecoDsEta");
  TCanvas *cRecoDsM = newCanvas("cRecoDsM","cRecoDsM");



  TCanvas *cMuLeadPt = newCanvas("cMuLeadPt","cMuLeadPt");
  TCanvas *cMuLeadEta = newCanvas("cMuLeadEta","cMuLeadEta");

  TCanvas *cMuTrailPt = newCanvas("cMuTrailPt","cMuTrailPt");
  TCanvas *cMuTrailEta = newCanvas("cMuTrailEta","cMuTrailEta");


  TCanvas *cDsVsMuLeadPt = newCanvas("cDsVsMuLeadPt","cDsVsMuLeadPt");
  TCanvas *cClosestMuonDeltaPhi = newCanvas("cClosestMuonDeltaPhi","cClosestMuonDeltaPhi");
  TCanvas *cClosestMuonDeltaPhiVsEta = newCanvas("cClosestMuonDeltaPhiVsEta","cClosestMuonDeltaPhiVsEta");

  TCanvas *cClosestMuonDeltaEta = newCanvas("cClosestMuonDeltaEta","cClosestMuonDeltaEta");
  TCanvas *cClosestMuonDeltaR = newCanvas("cClosestMuonDeltaR","cClosestMuonDeltaR");

  TCanvas *cNRecoMuonAll = newCanvas("cNRecoMuonAll","cNRecoMuonAll");
  TCanvas *cNRecoMuonMatched = newCanvas("cNRecoMuonMatched","cNRecoMuonMatched");

  
  TCanvas *cEff3RecoVsPtDs = newCanvas("cEff3RecoVsPtDs", "cEff3RecoVsPtDs");
  TCanvas *cEff3RecoVsEtaDs = newCanvas("cEff3RecoVsEtaDs", "cEff3RecoVsEtaDs");
  TCanvas *cEff2RecoVsPtDs = newCanvas("cEff2RecoVsPtDs", "cEff2RecoVsPtDs");
  TCanvas *cEff2RecoVsEtaDs = newCanvas("cEff2RecoVsEtaDs", "cEff2RecoVsEtaDs");


  int index = 1;
  for(vector<TString>::const_iterator sample = samples.begin();
      sample != samples.end(); ++sample) {

    TFile *file = new TFile(*sample);
    cout << "file: " << file << endl;


    HistoKin * hKinTau = new HistoKin("Tau","genLevelAnalysis", file);
    cTauPt->cd();
    //hKinTau->hPt->Scale(1./hKinTau->hPt->Integral());
    hKinTau->hPt->Draw();
    cTauEta->cd();
    hKinTau->hEta->Draw();

    HistoKin * hKinDs = new HistoKin("Ds","genLevelAnalysis", file);
    cDsPt->cd();
    //hKinDs->hPt->Scale(1./hKinDs->hPt->Integral());
    hKinDs->hPt->Draw();
    cDsEta->cd();
    hKinDs->hEta->Draw();

    HistoKin * hKinRecoDs = new HistoKin("RecoDs","genLevelAnalysis", file);
    cRecoDsPt->cd();
    //hKinRecoDs->hPt->Scale(1./hKinRecoDs->hPt->Integral());
    hKinRecoDs->hPt->Draw();
    cRecoDsEta->cd();
    hKinRecoDs->hEta->Draw();
    cRecoDsM->cd();
    hKinRecoDs->hMass->Draw();



    HistoKin * hKinMuLead = new HistoKin("MuLead","genLevelAnalysis", file);
    cMuLeadPt->cd();
    //hKinMuLead->hPt->Scale(1./hKinMuLead->hPt->Integral());
    hKinMuLead->hPt->Draw();
    cMuLeadEta->cd();
    hKinMuLead->hEta->Draw();


    HistoKin * hKinMuTrail = new HistoKin("MuTrail","genLevelAnalysis", file);
    cMuTrailPt->cd();
    //hKinMuTrail->hPt->Scale(1./hKinMuTrail->hPt->Integral());
    hKinMuTrail->hPt->Draw();
    cMuTrailEta->cd();
    hKinMuTrail->hEta->Draw();


    HistoKinPair *hKinDsVsMuLead = new HistoKinPair("DsVsMuLead","genLevelAnalysis", file);
    cDsVsMuLeadPt->cd();
    plotAndProfileX(hKinDsVsMuLead->hPt1VsPt2, 0,50,true);
    plotPtBins(hKinDsVsMuLead->hPt1VsPt2);



    HistoKinPair *hKinClosestMuPhi =new HistoKinPair("ClosestMuPhi","genLevelAnalysis", file);
    cClosestMuonDeltaPhi->cd();
    hKinClosestMuPhi->hDPhi->Draw();
    cClosestMuonDeltaEta->cd();
    hKinClosestMuPhi->hDEta->Draw();
    cClosestMuonDeltaR->cd();
    hKinClosestMuPhi->hDR->Draw();
    cClosestMuonDeltaPhiVsEta->cd();
    plotAndProfileX(hKinClosestMuPhi->hDPhiVsDEta, 0,6,true);


    TH1F *hNRecoMuAll = (TH1F*) file->Get("genLevelAnalysis/hNRecoMuAll");
    cNRecoMuonAll->cd();
    hNRecoMuAll->Draw();

    TH1F *hNRecoMuMatched = (TH1F*) file->Get("genLevelAnalysis/hNRecoMuMatched");
    cNRecoMuonMatched->cd();
    hNRecoMuMatched->Draw();

    HistoKin * hKinDs3RecoMatched = new HistoKin("Ds3RecoMatched","genLevelAnalysis", file);
    cEff3RecoVsPtDs->cd();
    TH1F *hEff3RecoVsPtDs = (TH1F *) hKinDs3RecoMatched->hPt->Clone("hEff3RecoVsPtDs");
    hEff3RecoVsPtDs->Divide(hKinDs->hPt);
    hEff3RecoVsPtDs->Draw();

    cEff3RecoVsEtaDs->cd();
    TH1F *hEff3RecoVsEtaDs = (TH1F *) hKinDs3RecoMatched->hEta->Clone("hEff3RecoVsEtaDs");
    hEff3RecoVsEtaDs->Divide(hKinDs->hEta);
    hEff3RecoVsEtaDs->Draw();

    HistoKin * hKinDs2RecoMatched = new HistoKin("Ds2RecoMatched","genLevelAnalysis", file);
    cEff2RecoVsPtDs->cd();
    TH1F *hEff2RecoVsPtDs = (TH1F *) hKinDs2RecoMatched->hPt->Clone("hEff2RecoVsPtDs");
    hEff2RecoVsPtDs->Divide(hKinDs->hPt);
    hEff2RecoVsPtDs->Draw();

    cEff2RecoVsEtaDs->cd();
    TH1F *hEff2RecoVsEtaDs = (TH1F *) hKinDs2RecoMatched->hEta->Clone("hEff2RecoVsEtaDs");
    hEff2RecoVsEtaDs->Divide(hKinDs->hEta);
    hEff2RecoVsEtaDs->Draw();

  }

}
