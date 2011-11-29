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
  TCanvas *cEff3RecoVsPtEtaDs = newCanvas("cEff3RecoVsPtEtaDs","cEff3RecoVsPtEtaDs");
  TCanvas *cEff2RecoVsPtDs = newCanvas("cEff2RecoVsPtDs", "cEff2RecoVsPtDs");
  TCanvas *cEff2RecoVsEtaDs = newCanvas("cEff2RecoVsEtaDs", "cEff2RecoVsEtaDs");
  TCanvas *cEff2RecoVsPtEtaDs = newCanvas("cEff2RecoVsPtEtaDs","cEff2RecoVsPtEtaDs");

  TCanvas *cEff3L1to3RecoVsPtDs  = newCanvas("cEff3L1to3RecoVsPtDs","cEff3L1to3RecoVsPtDs");
  TCanvas *cEff2L1to3RecoVsPtDs  = newCanvas("cEff2L1to3RecoVsPtDs"",cEff2L1to3RecoVsPtDs");
  TCanvas *cEff2L13p5to3RecoVsPtDs  = newCanvas("cEff2L13p5to3RecoVsPtDs","cEff2L13p5to3RecoVsPtDs");
  TCanvas *cEff2L15to3RecoVsPtDs  = newCanvas("cEff2L15to3RecoVsPtDs","cEff2L15to3RecoVsPtDs");
  TCanvas *cEffHLTto3RecoVsPtDs = newCanvas("cEffHLTto3RecoVsPtDs","cEffHLTto3RecoVsPtDs");
  TCanvas *cEff3L1to3RecoVsEtaDs  = newCanvas("cEff3L1to3RecoVsEtaDs","cEff3L1to3RecoVsEtaDs");
  TCanvas *cEff2L1to3RecoVsEtaDs  = newCanvas("cEff2L1to3RecoVsEtaDs"",cEff2L1to3RecoVsEtaDs");
  TCanvas *cEff2L13p5to3RecoVsEtaDs  = newCanvas("cEff2L13p5to3RecoVsEtaDs","cEff2L13p5to3RecoVsEtaDs");
  TCanvas *cEff2L15to3RecoVsEtaDs  = newCanvas("cEff2L15to3RecoVsEtaDs","cEff2L15to3RecoVsEtaDs");
  TCanvas *cEffHLTto3RecoVsEtaDs = newCanvas("cEffHLTto3RecoVsEtaDs","cEffHLTto3RecoVsEtaDs");
  TCanvas *cEff3L1to3RecoVsPtEtaDs  = newCanvas("cEff3L1to3RecoVsPtEtaDs","cEff3L1to3RecoVsPtEtaDs");
  TCanvas *cEff2L1to3RecoVsPtEtaDs  = newCanvas("cEff2L1to3RecoVsPtEtaDs"",cEff2L1to3RecoVsPtEtaDs");
  TCanvas *cEff2L13p5to3RecoVsPtEtaDs  = newCanvas("cEff2L13p5to3RecoVsPtEtaDs","cEff2L13p5to3RecoVsPtEtaDs");
  TCanvas *cEff2L15to3RecoVsPtEtaDs  = newCanvas("cEff2L15to3RecoVsPtEtaDs","cEff2L15to3RecoVsPtEtaDs");
  TCanvas *cEffHLTto3RecoVsPtEtaDs = newCanvas("cEffHLTto3RecoVsPtEtaDs","cEffHLTto3RecoVsPtEtaDs");


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
    //TH1F *hEff3RecoVsPtDs = (TH1F *) hKinDs3RecoMatched->hPt->Clone("hEff3RecoVsPtDs");
    TGraphAsymmErrors *tgEff3RecoVsPtDs = new TGraphAsymmErrors;
    tgEff3RecoVsPtDs->SetTitle("Eff 3 Reco Muons vs Ds Pt");
    tgEff3RecoVsPtDs->SetName("tgEff3RecoVsPtDs");
    tgEff3RecoVsPtDs->Divide(hKinDs3RecoMatched->hPt,hKinDs->hPt);
    //hEff3RecoVsPtDs->Divide(hKinDs->hPt);
    tgEff3RecoVsPtDs->Draw("AP");

    cEff3RecoVsEtaDs->cd();
    //TH1F *hEff3RecoVsEtaDs = (TH1F *) hKinDs3RecoMatched->hEta->Clone("hEff3RecoVsEtaDs");
    TGraphAsymmErrors *tgEff3RecoVsEtaDs = new TGraphAsymmErrors;
    tgEff3RecoVsEtaDs->SetTitle("Eff 3 Reco Muons vs Ds Eta");
    tgEff3RecoVsEtaDs->SetName("tgEff3RecoVsEtaDs");
    tgEff3RecoVsEtaDs->Divide(hKinDs3RecoMatched->hEta,hKinDs->hEta);
    tgEff3RecoVsEtaDs->Draw("AP");

    cEff3RecoVsPtEtaDs->cd();
    TH2F *hEff3RecoVsPtEtaDs = (TH2F *) hKinDs3RecoMatched->hPtEta->Clone("hEff3RecoVsPtEtaDs");
    hEff3RecoVsPtEtaDs->Divide(hKinDs->hPtEta);
    hEff3RecoVsPtEtaDs->Draw("colz");

    HistoKin * hKinDs2RecoMatched = new HistoKin("Ds2RecoMatched","genLevelAnalysis", file);
    cEff2RecoVsPtDs->cd();
    //TH1F *hEff2RecoVsPtDs = (TH1F *) hKinDs2RecoMatched->hPt->Clone("hEff2RecoVsPtDs");
    TGraphAsymmErrors *tgEff2RecoVsPtDs = new TGraphAsymmErrors;
    tgEff2RecoVsPtDs->SetTitle("Eff 2 Reco Muon vs Ds Pt");
    tgEff2RecoVsPtDs->SetName("tgEff2RecoVsPtDs");
    tgEff2RecoVsPtDs->Divide(hKinDs2RecoMatched->hPt,hKinDs->hPt);
    tgEff2RecoVsPtDs->Draw("AP");

    cEff2RecoVsEtaDs->cd();
    //TH1F *hEff2RecoVsEtaDs = (TH1F *) hKinDs2RecoMatched->hEta->Clone("hEff2RecoVsEtaDs");
    TGraphAsymmErrors *tgEff2RecoVsEtaDs = new TGraphAsymmErrors;
    tgEff2RecoVsEtaDs->SetTitle("Eff 2 Reco Muon vs Ds Eta");
    tgEff2RecoVsEtaDs->SetName("tgEff2RecoVsEtaDs");
    tgEff2RecoVsEtaDs->Divide(hKinDs2RecoMatched->hEta,hKinDs->hEta);
    tgEff2RecoVsEtaDs->Draw("AP");

    cEff2RecoVsPtEtaDs->cd();
    TH2F *hEff2RecoVsPtEtaDs = (TH2F *) hKinDs2RecoMatched->hPtEta->Clone("hEff2RecoVsPtEtaDs");
    hEff2RecoVsPtEtaDs->Divide(hKinDs->hPtEta);
    hEff2RecoVsPtEtaDs->Draw("colz");



    // ===============trigger efficiencies wrt to reco
    //    3 L1 Pt>0
    HistoKin * hKinDs3RecoMatched3L1Matched = new HistoKin("Ds3RecoMatched3L1Matched","genLevelAnalysis",file);
    cEff3L1to3RecoVsEtaDs->cd();
    TGraphAsymmErrors *tgEff3L1to3RecoVsEtaDs = new TGraphAsymmErrors;
    tgEff3L1to3RecoVsEtaDs->SetTitle("Eff 3 L1 Muons Pt>0 wrt 3 Reco Muons, vs Ds Eta");
    tgEff3L1to3RecoVsEtaDs->SetName("tgEff3L1to3RecoVsEtaDs");
    tgEff3L1to3RecoVsEtaDs->Divide(hKinDs3RecoMatched3L1Matched->hEta,hKinDs3RecoMatched->hEta);
    tgEff3L1to3RecoVsEtaDs->Draw("AP");

    cEff3L1to3RecoVsPtDs->cd();
    TGraphAsymmErrors *tgEff3L1to3RecoVsPtDs = new TGraphAsymmErrors;
    tgEff3L1to3RecoVsPtDs->SetTitle("Eff 3 L1 Muons Pt>0 wrt 3 Reco Muons, vs Ds Pt");
    tgEff3L1to3RecoVsPtDs->SetName("tgEff3L1to3RecoVsPtDs");
    tgEff3L1to3RecoVsPtDs->Divide(hKinDs3RecoMatched3L1Matched->hPt,hKinDs3RecoMatched->hPt);
    tgEff3L1to3RecoVsPtDs->Draw("AP");

    cEff3L1to3RecoVsPtEtaDs->cd();
    TH2F *hEff3L1to3RecoVsPtEtaDs = (TH2F*) hKinDs3RecoMatched3L1Matched->hPtEta->Clone("hEff3L1to3RecoVsPtEtaDs");
    hEff3L1to3RecoVsPtEtaDs->Divide(hKinDs3RecoMatched->hPtEta);
    hEff3L1to3RecoVsPtEtaDs->Draw("colz");

    // 2 L1 Pt > 0
    HistoKin * hKinDs3RecoMatched2L1Matched = new HistoKin("Ds3RecoMatched2L1Matched","genLevelAnalysis",file);
    cEff2L1to3RecoVsEtaDs->cd();
    TGraphAsymmErrors *tgEff2L1to3RecoVsEtaDs = new TGraphAsymmErrors;
    tgEff2L1to3RecoVsEtaDs->SetTitle("Eff 2 L1 Muons Pt>0 wrt 3 Reco Muons, vs Ds Eta");
    tgEff2L1to3RecoVsEtaDs->SetName("tgEff2L1to3RecoVsEtaDs");
    tgEff2L1to3RecoVsEtaDs->Divide(hKinDs3RecoMatched2L1Matched->hEta,hKinDs3RecoMatched->hEta);
    tgEff2L1to3RecoVsEtaDs->Draw("AP");

    cEff2L1to3RecoVsPtDs->cd();
    TGraphAsymmErrors *tgEff2L1to3RecoVsPtDs = new TGraphAsymmErrors;
    tgEff2L1to3RecoVsPtDs->SetTitle("Eff 2 L1 Muons Pt>0 wrt 3 Reco Muons, vs Ds Pt");
    tgEff2L1to3RecoVsPtDs->SetName("tgEff2L1to3RecoVsPtDs");
    tgEff2L1to3RecoVsPtDs->Divide(hKinDs3RecoMatched2L1Matched->hPt,hKinDs3RecoMatched->hPt);
    tgEff2L1to3RecoVsPtDs->Draw("AP");

    cEff2L1to3RecoVsPtEtaDs->cd();
    TH2F *hEff2L1to3RecoVsPtEtaDs = (TH2F*) hKinDs3RecoMatched2L1Matched->hPtEta->Clone("hEff2L1to3RecoVsPtEtaDs");
    hEff2L1to3RecoVsPtEtaDs->Divide(hKinDs3RecoMatched->hPtEta);
    hEff2L1to3RecoVsPtEtaDs->Draw("colz");

    // 2 L1 Pt >3.5
    HistoKin * hKinDs3RecoMatched2L13p5Matched = new HistoKin("Ds3RecoMatched2L13p5Matched","genLevelAnalysis",file);
    cEff2L13p5to3RecoVsEtaDs->cd();
    TGraphAsymmErrors *tgEff2L13p5to3RecoVsEtaDs = new TGraphAsymmErrors;
    tgEff2L13p5to3RecoVsEtaDs->SetTitle("Eff 2 L1 Muons Pt>3.5 wrt 3 Reco Muons, vs Ds Eta");
    tgEff2L13p5to3RecoVsEtaDs->SetName("tgEff2L1to3RecoVsEtaDs");
    tgEff2L13p5to3RecoVsEtaDs->Divide(hKinDs3RecoMatched2L13p5Matched->hEta,hKinDs3RecoMatched->hEta);
    tgEff2L13p5to3RecoVsEtaDs->Draw("AP");

    cEff2L13p5to3RecoVsPtDs->cd();
    TGraphAsymmErrors *tgEff2L13p5to3RecoVsPtDs = new TGraphAsymmErrors;
    tgEff2L13p5to3RecoVsPtDs->SetTitle("Eff 2 L1 Muons Pt>3.5 wrt 3 Reco Muons, vs Ds Pt");
    tgEff2L13p5to3RecoVsPtDs->SetName("tgEff2L1to3RecoVsPtDs");
    tgEff2L13p5to3RecoVsPtDs->Divide(hKinDs3RecoMatched2L13p5Matched->hPt,hKinDs3RecoMatched->hPt);
    tgEff2L13p5to3RecoVsPtDs->Draw("AP");

    cEff2L13p5to3RecoVsPtEtaDs->cd();
    TH2F *hEff2L13p5to3RecoVsPtEtaDs = (TH2F*) hKinDs3RecoMatched2L13p5Matched->hPtEta->Clone("hEff2L13p5to3RecoVsPtEtaDs");
    hEff2L13p5to3RecoVsPtEtaDs->Divide(hKinDs3RecoMatched->hPtEta);
    hEff2L13p5to3RecoVsPtEtaDs->Draw("colz");

    // 2 L1 Pt > 5
    HistoKin * hKinDs3RecoMatched2L15Matched = new HistoKin("Ds3RecoMatched2L15Matched","genLevelAnalysis",file);
    cEff2L15to3RecoVsEtaDs->cd();
    TGraphAsymmErrors *tgEff2L15to3RecoVsEtaDs = new TGraphAsymmErrors;
    tgEff2L15to3RecoVsEtaDs->SetTitle("Eff 2 L1 Muons Pt>5 wrt 3 Reco Muons, vs Ds Eta");
    tgEff2L15to3RecoVsEtaDs->SetName("tgEff2L1to3RecoVsEtaDs");
    tgEff2L15to3RecoVsEtaDs->Divide(hKinDs3RecoMatched2L15Matched->hEta,hKinDs3RecoMatched->hEta);
    tgEff2L15to3RecoVsEtaDs->Draw("AP");

    cEff2L15to3RecoVsPtDs->cd();
    TGraphAsymmErrors *tgEff2L15to3RecoVsPtDs = new TGraphAsymmErrors;
    tgEff2L15to3RecoVsPtDs->SetTitle("Eff 2 L1 Muons Pt>5 wrt 3 Reco Muons, vs Ds Pt");
    tgEff2L15to3RecoVsPtDs->SetName("tgEff2L1to3RecoVsPtDs");
    tgEff2L15to3RecoVsPtDs->Divide(hKinDs3RecoMatched2L15Matched->hPt,hKinDs3RecoMatched->hPt);
    tgEff2L15to3RecoVsPtDs->Draw("AP");
    
    cEff2L15to3RecoVsPtEtaDs->cd();
    TH2F *hEff2L15to3RecoVsPtEtaDs = (TH2F*) hKinDs3RecoMatched2L15Matched->hPtEta->Clone("hEff2L15to3RecoVsPtEtaDs");
    hEff2L15to3RecoVsPtEtaDs->Divide(hKinDs3RecoMatched->hPtEta);
    hEff2L15to3RecoVsPtEtaDs->Draw("colz");

    // HLT path
    HistoKin * hKinDs3RecoMatchedHLTTau3Mu = new HistoKin("Ds3RecoMatchedHLTTau3Mu","genLevelAnalysis",file);
    cEffHLTto3RecoVsEtaDs->cd();
    TGraphAsymmErrors *tgEffHLTto3RecoVsEtaDs = new TGraphAsymmErrors;
    tgEffHLTto3RecoVsEtaDs->SetTitle("Eff HLT Tau->3mu wrt 3 Reco Muons, vs Ds Eta");
    tgEffHLTto3RecoVsEtaDs->SetName("tgEff2L1to3RecoVsEtaDs");
    tgEffHLTto3RecoVsEtaDs->Divide(hKinDs3RecoMatchedHLTTau3Mu->hEta,hKinDs3RecoMatched->hEta);
    tgEffHLTto3RecoVsEtaDs->Draw("AP");

    cEffHLTto3RecoVsPtDs->cd();
    TGraphAsymmErrors *tgEffHLTto3RecoVsPtDs = new TGraphAsymmErrors;
    tgEffHLTto3RecoVsPtDs->SetTitle("Eff HLT Tau->3mu wrt 3 Reco Muons, vs Ds Pt");
    tgEffHLTto3RecoVsPtDs->SetName("tgEff2L1to3RecoVsPtDs");
    tgEffHLTto3RecoVsPtDs->Divide(hKinDs3RecoMatchedHLTTau3Mu->hPt,hKinDs3RecoMatched->hPt);
    tgEffHLTto3RecoVsPtDs->Draw("AP");
    
    cEffHLTto3RecoVsPtEtaDs->cd();
    TH2F *hEffHLTto3RecoVsPtEtaDs = (TH2F*) hKinDs3RecoMatchedHLTTau3Mu->hPtEta->Clone("hEffHLTto3RecoVsPtEtaDs");
    hEffHLTto3RecoVsPtEtaDs->Divide(hKinDs3RecoMatched->hPtEta);
    hEffHLTto3RecoVsPtEtaDs->Draw("colz");
    





  }

}
