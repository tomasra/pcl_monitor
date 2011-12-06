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

   TCanvas *cEff3L1to3RecoGoodVsPtDs  = newCanvas("cEff3L1to3RecoGoodVsPtDs","cEff3L1to3RecoGoodVsPtDs");
  TCanvas *cEff2L1to3RecoGoodVsPtDs  = newCanvas("cEff2L1to3RecoGoodVsPtDs","cEff2L1to3RecoGoodVsPtDs");
  TCanvas *cEff2L13p5to3RecoGoodVsPtDs  = newCanvas("cEff2L13p5to3RecoGoodVsPtDs","cEff2L13p5to3RecoGoodVsPtDs");
  TCanvas *cEff2L15to3RecoGoodVsPtDs  = newCanvas("cEff2L15to3RecoGoodVsPtDs","cEff2L15to3RecoGoodVsPtDs");
  TCanvas *cEffHLTto3RecoGoodVsPtDs = newCanvas("cEffHLTto3RecoGoodVsPtDs","cEffHLTto3RecoGoodVsPtDs");
  TCanvas *cEff3L1to3RecoGoodVsEtaDs  = newCanvas("cEff3L1to3RecoGoodVsEtaDs","cEff3L1to3RecoGoodVsEtaDs");
  TCanvas *cEff2L1to3RecoGoodVsEtaDs  = newCanvas("cEff2L1to3RecoGoodVsEtaDs","cEff2L1to3RecoGoodVsEtaDs");
  TCanvas *cEff2L13p5to3RecoGoodVsEtaDs  = newCanvas("cEff2L13p5to3RecoGoodVsEtaDs","cEff2L13p5to3RecoGoodVsEtaDs");
  TCanvas *cEff2L15to3RecoGoodVsEtaDs  = newCanvas("cEff2L15to3RecoGoodVsEtaDs","cEff2L15to3RecoGoodVsEtaDs");
  TCanvas *cEffHLTto3RecoGoodVsEtaDs = newCanvas("cEffHLTto3RecoGoodVsEtaDs","cEffHLTto3RecoGoodVsEtaDs");
  TCanvas *cEff3L1to3RecoGoodVsPtEtaDs  = newCanvas("cEff3L1to3RecoGoodVsPtEtaDs","cEff3L1to3RecoGoodVsPtEtaDs");
  TCanvas *cEff2L1to3RecoGoodVsPtEtaDs  = newCanvas("cEff2L1to3RecoGoodVsPtEtaDs","cEff2L1to3RecoGoodVsPtEtaDs");
  TCanvas *cEff2L13p5to3RecoGoodVsPtEtaDs  = newCanvas("cEff2L13p5to3RecoGoodVsPtEtaDs","cEff2L13p5to3RecoGoodVsPtEtaDs");
  TCanvas *cEff2L15to3RecoGoodVsPtEtaDs  = newCanvas("cEff2L15to3RecoGoodVsPtEtaDs","cEff2L15to3RecoGoodVsPtEtaDs");
  TCanvas *cEffHLTto3RecoGoodVsPtEtaDs = newCanvas("cEffHLTto3RecoGoodVsPtEtaDs","cEffHLTto3RecoGoodVsPtEtaDs");

  TCanvas *cEff3L1toGenVsPtDs  = newCanvas("cEff3L1toGenVsPtDs","cEff3L1toGenVsPtDs");
  TCanvas *cEff2L1toGenVsPtDs  = newCanvas("cEff2L1toGenVsPtDs","cEff2L1toGenVsPtDs");
  TCanvas *cEff2L13p5toGenVsPtDs  = newCanvas("cEff2L13p5toGenVsPtDs","cEff2L13p5toGenVsPtDs");
  TCanvas *cEff2L15toGenVsPtDs  = newCanvas("cEff2L15toGenVsPtDs","cEff2L15toGenVsPtDs");
  TCanvas *cEffHLTtoGenVsPtDs = newCanvas("cEffHLTtoGenVsPtDs","cEffHLTtoGenVsPtDs");
  TCanvas *cEff3L1toGenVsEtaDs  = newCanvas("cEff3L1toGenVsEtaDs","cEff3L1toGenVsEtaDs");
  TCanvas *cEff2L1toGenVsEtaDs  = newCanvas("cEff2L1toGenVsEtaDs","cEff2L1toGenVsEtaDs");
  TCanvas *cEff2L13p5toGenVsEtaDs  = newCanvas("cEff2L13p5toGenVsEtaDs","cEff2L13p5toGenVsEtaDs");
  TCanvas *cEff2L15toGenVsEtaDs  = newCanvas("cEff2L15toGenVsEtaDs","cEff2L15toGenVsEtaDs");
  TCanvas *cEffHLTtoGenVsEtaDs = newCanvas("cEffHLTtoGenVsEtaDs","cEffHLTtoGenVsEtaDs");
  TCanvas *cEff3L1toGenVsPtEtaDs  = newCanvas("cEff3L1toGenVsPtEtaDs","cEff3L1toGenVsPtEtaDs");
  TCanvas *cEff2L1toGenVsPtEtaDs  = newCanvas("cEff2L1toGenVsPtEtaDs","cEff2L1toGenVsPtEtaDs");
  TCanvas *cEff2L13p5toGenVsPtEtaDs  = newCanvas("cEff2L13p5toGenVsPtEtaDs","cEff2L13p5toGenVsPtEtaDs");
  TCanvas *cEff2L15toGenVsPtEtaDs  = newCanvas("cEff2L15toGenVsPtEtaDs","cEff2L15toGenVsPtEtaDs");
  TCanvas *cEffHLTtoGenVsPtEtaDs = newCanvas("cEffHLTtoGenVsPtEtaDs","cEffHLTtoGenVsPtEtaDs");


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
    HistoKin * hKinDs3RecoGoodMatched = new HistoKin("Ds3RecoGoodMatched","genLevelAnalysis", file);
    cEff3RecoVsPtDs->cd();
    //TH1F *hEff3RecoVsPtDs = (TH1F *) hKinDs3RecoMatched->hPt->Clone("hEff3RecoVsPtDs");
    TGraphAsymmErrors *tgEff3RecoVsPtDs = new TGraphAsymmErrors;
    tgEff3RecoVsPtDs->SetTitle("Eff 3 Reco Muons vs Ds Pt");
    tgEff3RecoVsPtDs->SetName("tgEff3RecoVsPtDs");
    tgEff3RecoVsPtDs->Divide(hKinDs3RecoMatched->hPt,hKinDs->hPt);
    TGraphAsymmErrors *tgEff3RecoGoodVsPtDs = new TGraphAsymmErrors;
    tgEff3RecoGoodVsPtDs->SetTitle("Eff 3 Reco Good Muons vs Ds Pt");
    tgEff3RecoGoodVsPtDs->SetName("tgEff3RecoGoodVsPtDs");
    tgEff3RecoGoodVsPtDs->Divide(hKinDs3RecoGoodMatched->hPt,hKinDs->hPt);
    tgEff3RecoGoodVsPtDs->SetMarkerColor(2);
    //hEff3RecoVsPtDs->Divide(hKinDs->hPt);
    tgEff3RecoVsPtDs->Draw("AP");
    tgEff3RecoGoodVsPtDs->Draw("P");

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
    HistoKin * hKinDs3RecoGoodMatched3L1Matched = new HistoKin("Ds3RecoGoodMatched3L1Matched","genLevelAnalysis",file);
    cEff3L1to3RecoGoodVsEtaDs->cd();
    TGraphAsymmErrors *tgEff3L1to3RecoGoodVsEtaDs = new TGraphAsymmErrors;
    tgEff3L1to3RecoGoodVsEtaDs->SetTitle("Eff 3 L1 Muons Pt>0 wrt 3 Reco Muons, vs Ds Eta");
    tgEff3L1to3RecoGoodVsEtaDs->SetName("tgEff3L1to3RecoGoodVsEtaDs");
    tgEff3L1to3RecoGoodVsEtaDs->Divide(hKinDs3RecoGoodMatched3L1Matched->hEta,hKinDs3RecoGoodMatched->hEta);
    tgEff3L1to3RecoGoodVsEtaDs->Draw("AP");

    cEff3L1to3RecoGoodVsPtDs->cd();
    TGraphAsymmErrors *tgEff3L1to3RecoGoodVsPtDs = new TGraphAsymmErrors;
    tgEff3L1to3RecoGoodVsPtDs->SetTitle("Eff 3 L1 Muons Pt>0 wrt 3 Reco Muons, vs Ds Pt");
    tgEff3L1to3RecoGoodVsPtDs->SetName("tgEff3L1to3RecoGoodVsPtDs");
    tgEff3L1to3RecoGoodVsPtDs->Divide(hKinDs3RecoGoodMatched3L1Matched->hPt,hKinDs3RecoGoodMatched->hPt);
    tgEff3L1to3RecoGoodVsPtDs->Draw("AP");

    cEff3L1to3RecoGoodVsPtEtaDs->cd();
    TH2F *hEff3L1to3RecoGoodVsPtEtaDs = (TH2F*) hKinDs3RecoGoodMatched3L1Matched->hPtEta->Clone("hEff3L1to3RecoGoodVsPtEtaDs");
    hEff3L1to3RecoGoodVsPtEtaDs->Divide(hKinDs3RecoGoodMatched->hPtEta);
    hEff3L1to3RecoGoodVsPtEtaDs->Draw("colz");

    // 2 L1 Pt > 0
    HistoKin * hKinDs3RecoGoodMatched2L1Matched = new HistoKin("Ds3RecoGoodMatched2L1Matched","genLevelAnalysis",file);
    cEff2L1to3RecoGoodVsEtaDs->cd();
    TGraphAsymmErrors *tgEff2L1to3RecoGoodVsEtaDs = new TGraphAsymmErrors;
    tgEff2L1to3RecoGoodVsEtaDs->SetTitle("Eff 2 L1 Muons Pt>0 wrt 3 Reco Muons, vs Ds Eta");
    tgEff2L1to3RecoGoodVsEtaDs->SetName("tgEff2L1to3RecoGoodVsEtaDs");
    tgEff2L1to3RecoGoodVsEtaDs->Divide(hKinDs3RecoGoodMatched2L1Matched->hEta,hKinDs3RecoGoodMatched->hEta);
    tgEff2L1to3RecoGoodVsEtaDs->Draw("AP");

    cEff2L1to3RecoGoodVsPtDs->cd();
    TGraphAsymmErrors *tgEff2L1to3RecoGoodVsPtDs = new TGraphAsymmErrors;
    tgEff2L1to3RecoGoodVsPtDs->SetTitle("Eff 2 L1 Muons Pt>0 wrt 3 Reco Muons, vs Ds Pt");
    tgEff2L1to3RecoGoodVsPtDs->SetName("tgEff2L1to3RecoGoodVsPtDs");
    tgEff2L1to3RecoGoodVsPtDs->Divide(hKinDs3RecoGoodMatched2L1Matched->hPt,hKinDs3RecoGoodMatched->hPt);
    tgEff2L1to3RecoGoodVsPtDs->Draw("AP");

    cEff2L1to3RecoGoodVsPtEtaDs->cd();
    TH2F *hEff2L1to3RecoGoodVsPtEtaDs = (TH2F*) hKinDs3RecoGoodMatched2L1Matched->hPtEta->Clone("hEff2L1to3RecoGoodVsPtEtaDs");
    hEff2L1to3RecoGoodVsPtEtaDs->Divide(hKinDs3RecoGoodMatched->hPtEta);
    hEff2L1to3RecoGoodVsPtEtaDs->Draw("colz");

    // 2 L1 Pt >3.5
    HistoKin * hKinDs3RecoGoodMatched2L13p5Matched = new HistoKin("Ds3RecoGoodMatched2L13p5Matched","genLevelAnalysis",file);
    cEff2L13p5to3RecoGoodVsEtaDs->cd();
    TGraphAsymmErrors *tgEff2L13p5to3RecoGoodVsEtaDs = new TGraphAsymmErrors;
    tgEff2L13p5to3RecoGoodVsEtaDs->SetTitle("Eff 2 L1 Muons Pt>3.5 wrt 3 Reco Muons, vs Ds Eta");
    tgEff2L13p5to3RecoGoodVsEtaDs->SetName("tgEff2L1to3RecoGoodVsEtaDs");
    tgEff2L13p5to3RecoGoodVsEtaDs->Divide(hKinDs3RecoGoodMatched2L13p5Matched->hEta,hKinDs3RecoGoodMatched->hEta);
    tgEff2L13p5to3RecoGoodVsEtaDs->Draw("AP");

    cEff2L13p5to3RecoGoodVsPtDs->cd();
    TGraphAsymmErrors *tgEff2L13p5to3RecoGoodVsPtDs = new TGraphAsymmErrors;
    tgEff2L13p5to3RecoGoodVsPtDs->SetTitle("Eff 2 L1 Muons Pt>3.5 wrt 3 Reco Muons, vs Ds Pt");
    tgEff2L13p5to3RecoGoodVsPtDs->SetName("tgEff2L1to3RecoGoodVsPtDs");
    tgEff2L13p5to3RecoGoodVsPtDs->Divide(hKinDs3RecoGoodMatched2L13p5Matched->hPt,hKinDs3RecoGoodMatched->hPt);
    tgEff2L13p5to3RecoGoodVsPtDs->Draw("AP");

    cEff2L13p5to3RecoGoodVsPtEtaDs->cd();
    TH2F *hEff2L13p5to3RecoGoodVsPtEtaDs = (TH2F*) hKinDs3RecoGoodMatched2L13p5Matched->hPtEta->Clone("hEff2L13p5to3RecoGoodVsPtEtaDs");
    hEff2L13p5to3RecoGoodVsPtEtaDs->Divide(hKinDs3RecoGoodMatched->hPtEta);
    hEff2L13p5to3RecoGoodVsPtEtaDs->Draw("colz");

    // 2 L1 Pt > 5
    HistoKin * hKinDs3RecoGoodMatched2L15Matched = new HistoKin("Ds3RecoGoodMatched2L15Matched","genLevelAnalysis",file);
    cEff2L15to3RecoGoodVsEtaDs->cd();
    TGraphAsymmErrors *tgEff2L15to3RecoGoodVsEtaDs = new TGraphAsymmErrors;
    tgEff2L15to3RecoGoodVsEtaDs->SetTitle("Eff 2 L1 Muons Pt>5 wrt 3 Reco Muons, vs Ds Eta");
    tgEff2L15to3RecoGoodVsEtaDs->SetName("tgEff2L1to3RecoGoodVsEtaDs");
    tgEff2L15to3RecoGoodVsEtaDs->Divide(hKinDs3RecoGoodMatched2L15Matched->hEta,hKinDs3RecoGoodMatched->hEta);
    tgEff2L15to3RecoGoodVsEtaDs->Draw("AP");

    cEff2L15to3RecoGoodVsPtDs->cd();
    TGraphAsymmErrors *tgEff2L15to3RecoGoodVsPtDs = new TGraphAsymmErrors;
    tgEff2L15to3RecoGoodVsPtDs->SetTitle("Eff 2 L1 Muons Pt>5 wrt 3 Reco Muons, vs Ds Pt");
    tgEff2L15to3RecoGoodVsPtDs->SetName("tgEff2L1to3RecoGoodVsPtDs");
    tgEff2L15to3RecoGoodVsPtDs->Divide(hKinDs3RecoGoodMatched2L15Matched->hPt,hKinDs3RecoGoodMatched->hPt);
    tgEff2L15to3RecoGoodVsPtDs->Draw("AP");
    
    cEff2L15to3RecoGoodVsPtEtaDs->cd();
    TH2F *hEff2L15to3RecoGoodVsPtEtaDs = (TH2F*) hKinDs3RecoGoodMatched2L15Matched->hPtEta->Clone("hEff2L15to3RecoGoodVsPtEtaDs");
    hEff2L15to3RecoGoodVsPtEtaDs->Divide(hKinDs3RecoGoodMatched->hPtEta);
    hEff2L15to3RecoGoodVsPtEtaDs->Draw("colz");

    // HLT path
    HistoKin * hKinDs3RecoGoodMatchedHLTTau3Mu = new HistoKin("Ds3RecoGoodMatchedHLTTau3Mu","genLevelAnalysis",file);
    cEffHLTto3RecoGoodVsEtaDs->cd();
    TGraphAsymmErrors *tgEffHLTto3RecoGoodVsEtaDs = new TGraphAsymmErrors;
    tgEffHLTto3RecoGoodVsEtaDs->SetTitle("Eff HLT Tau->3mu wrt 3 Reco Muons, vs Ds Eta");
    tgEffHLTto3RecoGoodVsEtaDs->SetName("tgEff2L1to3RecoGoodVsEtaDs");
    tgEffHLTto3RecoGoodVsEtaDs->Divide(hKinDs3RecoGoodMatchedHLTTau3Mu->hEta,hKinDs3RecoGoodMatched->hEta);
    tgEffHLTto3RecoGoodVsEtaDs->Draw("AP");

    cEffHLTto3RecoGoodVsPtDs->cd();
    TGraphAsymmErrors *tgEffHLTto3RecoGoodVsPtDs = new TGraphAsymmErrors;
    tgEffHLTto3RecoGoodVsPtDs->SetTitle("Eff HLT Tau->3mu wrt 3 Reco Muons, vs Ds Pt");
    tgEffHLTto3RecoGoodVsPtDs->SetName("tgEff2L1to3RecoGoodVsPtDs");
    tgEffHLTto3RecoGoodVsPtDs->Divide(hKinDs3RecoGoodMatchedHLTTau3Mu->hPt,hKinDs3RecoGoodMatched->hPt);
    tgEffHLTto3RecoGoodVsPtDs->Draw("AP");
    
    cEffHLTto3RecoGoodVsPtEtaDs->cd();
    TH2F *hEffHLTto3RecoGoodVsPtEtaDs = (TH2F*) hKinDs3RecoGoodMatchedHLTTau3Mu->hPtEta->Clone("hEffHLTto3RecoGoodVsPtEtaDs");
    hEffHLTto3RecoGoodVsPtEtaDs->Divide(hKinDs3RecoGoodMatched->hPtEta);
    hEffHLTto3RecoGoodVsPtEtaDs->Draw("colz");
    





    // ===============trigger efficiencies wrt to gen
    //    3 L1 Pt>0
    HistoKin * hKinDs3L1Matched = new HistoKin("Ds3L1Matched","genLevelAnalysis",file);
    cEff3L1toGenVsEtaDs->cd();
    TGraphAsymmErrors *tgEff3L1toGenVsEtaDs = new TGraphAsymmErrors;
    tgEff3L1toGenVsEtaDs->SetTitle("Eff 3 L1 Muons Pt>0 wrt 3 Reco Muons, vs Ds Eta");
    tgEff3L1toGenVsEtaDs->SetName("tgEff3L1toGenVsEtaDs");
    tgEff3L1toGenVsEtaDs->Divide(hKinDs3L1Matched->hEta,hKinDs->hEta);
    tgEff3L1toGenVsEtaDs->Draw("AP");

    cEff3L1toGenVsPtDs->cd();
    TGraphAsymmErrors *tgEff3L1toGenVsPtDs = new TGraphAsymmErrors;
    tgEff3L1toGenVsPtDs->SetTitle("Eff 3 L1 Muons Pt>0 wrt 3 Reco Muons, vs Ds Pt");
    tgEff3L1toGenVsPtDs->SetName("tgEff3L1toGenVsPtDs");
    tgEff3L1toGenVsPtDs->Divide(hKinDs3L1Matched->hPt,hKinDs->hPt);
    tgEff3L1toGenVsPtDs->Draw("AP");

    cEff3L1toGenVsPtEtaDs->cd();
    TH2F *hEff3L1toGenVsPtEtaDs = (TH2F*) hKinDs3L1Matched->hPtEta->Clone("hEff3L1toGenVsPtEtaDs");
    hEff3L1toGenVsPtEtaDs->Divide(hKinDs->hPtEta);
    hEff3L1toGenVsPtEtaDs->Draw("colz");

    // 2 L1 Pt > 0
    HistoKin * hKinDs2L1Matched = new HistoKin("Ds2L1Matched","genLevelAnalysis",file);
    cEff2L1toGenVsEtaDs->cd();
    TGraphAsymmErrors *tgEff2L1toGenVsEtaDs = new TGraphAsymmErrors;
    tgEff2L1toGenVsEtaDs->SetTitle("Eff 2 L1 Muons Pt>0 wrt 3 Reco Muons, vs Ds Eta");
    tgEff2L1toGenVsEtaDs->SetName("tgEff2L1toGenVsEtaDs");
    tgEff2L1toGenVsEtaDs->Divide(hKinDs2L1Matched->hEta,hKinDs->hEta);
    tgEff2L1toGenVsEtaDs->Draw("AP");

    cEff2L1toGenVsPtDs->cd();
    TGraphAsymmErrors *tgEff2L1toGenVsPtDs = new TGraphAsymmErrors;
    tgEff2L1toGenVsPtDs->SetTitle("Eff 2 L1 Muons Pt>0 wrt 3 Reco Muons, vs Ds Pt");
    tgEff2L1toGenVsPtDs->SetName("tgEff2L1toGenVsPtDs");
    tgEff2L1toGenVsPtDs->Divide(hKinDs2L1Matched->hPt,hKinDs->hPt);
    tgEff2L1toGenVsPtDs->Draw("AP");

    cEff2L1toGenVsPtEtaDs->cd();
    TH2F *hEff2L1toGenVsPtEtaDs = (TH2F*) hKinDs2L1Matched->hPtEta->Clone("hEff2L1toGenVsPtEtaDs");
    hEff2L1toGenVsPtEtaDs->Divide(hKinDs->hPtEta);
    hEff2L1toGenVsPtEtaDs->Draw("colz");

    // 2 L1 Pt >3.5
    HistoKin * hKinDs2L13p5Matched = new HistoKin("Ds2L13p5Matched","genLevelAnalysis",file);
    cEff2L13p5toGenVsEtaDs->cd();
    TGraphAsymmErrors *tgEff2L13p5toGenVsEtaDs = new TGraphAsymmErrors;
    tgEff2L13p5toGenVsEtaDs->SetTitle("Eff 2 L1 Muons Pt>3.5 wrt 3 Reco Muons, vs Ds Eta");
    tgEff2L13p5toGenVsEtaDs->SetName("tgEff2L1toGenVsEtaDs");
    tgEff2L13p5toGenVsEtaDs->Divide(hKinDs2L13p5Matched->hEta,hKinDs->hEta);
    tgEff2L13p5toGenVsEtaDs->Draw("AP");

    cEff2L13p5toGenVsPtDs->cd();
    TGraphAsymmErrors *tgEff2L13p5toGenVsPtDs = new TGraphAsymmErrors;
    tgEff2L13p5toGenVsPtDs->SetTitle("Eff 2 L1 Muons Pt>3.5 wrt 3 Reco Muons, vs Ds Pt");
    tgEff2L13p5toGenVsPtDs->SetName("tgEff2L1toGenVsPtDs");
    tgEff2L13p5toGenVsPtDs->Divide(hKinDs2L13p5Matched->hPt,hKinDs->hPt);
    tgEff2L13p5toGenVsPtDs->Draw("AP");

    cEff2L13p5toGenVsPtEtaDs->cd();
    TH2F *hEff2L13p5toGenVsPtEtaDs = (TH2F*) hKinDs2L13p5Matched->hPtEta->Clone("hEff2L13p5toGenVsPtEtaDs");
    hEff2L13p5toGenVsPtEtaDs->Divide(hKinDs->hPtEta);
    hEff2L13p5toGenVsPtEtaDs->Draw("colz");

    // 2 L1 Pt > 5
    HistoKin * hKinDs2L15Matched = new HistoKin("Ds2L15Matched","genLevelAnalysis",file);
    cEff2L15toGenVsEtaDs->cd();
    TGraphAsymmErrors *tgEff2L15toGenVsEtaDs = new TGraphAsymmErrors;
    tgEff2L15toGenVsEtaDs->SetTitle("Eff 2 L1 Muons Pt>5 wrt 3 Reco Muons, vs Ds Eta");
    tgEff2L15toGenVsEtaDs->SetName("tgEff2L1toGenVsEtaDs");
    tgEff2L15toGenVsEtaDs->Divide(hKinDs2L15Matched->hEta,hKinDs->hEta);
    tgEff2L15toGenVsEtaDs->Draw("AP");

    cEff2L15toGenVsPtDs->cd();
    TGraphAsymmErrors *tgEff2L15toGenVsPtDs = new TGraphAsymmErrors;
    tgEff2L15toGenVsPtDs->SetTitle("Eff 2 L1 Muons Pt>5 wrt 3 Reco Muons, vs Ds Pt");
    tgEff2L15toGenVsPtDs->SetName("tgEff2L1toGenVsPtDs");
    tgEff2L15toGenVsPtDs->Divide(hKinDs2L15Matched->hPt,hKinDs->hPt);
    tgEff2L15toGenVsPtDs->Draw("AP");
    
    cEff2L15toGenVsPtEtaDs->cd();
    TH2F *hEff2L15toGenVsPtEtaDs = (TH2F*) hKinDs2L15Matched->hPtEta->Clone("hEff2L15toGenVsPtEtaDs");
    hEff2L15toGenVsPtEtaDs->Divide(hKinDs->hPtEta);
    hEff2L15toGenVsPtEtaDs->Draw("colz");

    // HLT path
    HistoKin * hKinDsHLTTau3Mu = new HistoKin("DsHLTTau3Mu","genLevelAnalysis",file);
    cEffHLTtoGenVsEtaDs->cd();
    TGraphAsymmErrors *tgEffHLTtoGenVsEtaDs = new TGraphAsymmErrors;
    tgEffHLTtoGenVsEtaDs->SetTitle("Eff HLT Tau->3mu wrt 3 Reco Muons, vs Ds Eta");
    tgEffHLTtoGenVsEtaDs->SetName("tgEff2L1toGenVsEtaDs");
    tgEffHLTtoGenVsEtaDs->Divide(hKinDsHLTTau3Mu->hEta,hKinDs->hEta);
    tgEffHLTtoGenVsEtaDs->Draw("AP");

    cEffHLTtoGenVsPtDs->cd();
    TGraphAsymmErrors *tgEffHLTtoGenVsPtDs = new TGraphAsymmErrors;
    tgEffHLTtoGenVsPtDs->SetTitle("Eff HLT Tau->3mu wrt 3 Reco Muons, vs Ds Pt");
    tgEffHLTtoGenVsPtDs->SetName("tgEff2L1toGenVsPtDs");
    tgEffHLTtoGenVsPtDs->Divide(hKinDsHLTTau3Mu->hPt,hKinDs->hPt);
    tgEffHLTtoGenVsPtDs->Draw("AP");
    
    cEffHLTtoGenVsPtEtaDs->cd();
    TH2F *hEffHLTtoGenVsPtEtaDs = (TH2F*) hKinDsHLTTau3Mu->hPtEta->Clone("hEffHLTtoGenVsPtEtaDs");
    hEffHLTtoGenVsPtEtaDs->Divide(hKinDs->hPtEta);
    hEffHLTtoGenVsPtEtaDs->Draw("colz");
    


        



  }

}
