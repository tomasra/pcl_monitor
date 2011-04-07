#define ROOTANALYSIS
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
TString selection = "anal2";

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
  samples.push_back("H200");
  samples.push_back("ZZtoAnything_FlatPU");
  samples.push_back("WWtoAnything_PU2010");
  samples.push_back("WZtoAnything_FlatPU");
  samples.push_back("TToBLNu_tW-channel_FlatPU");
  samples.push_back("TToBLNu_t-channel_FlatPU");
  samples.push_back("TToBLNu_s-channel_FlatPU");
  samples.push_back("TTJets_madgraph_FlatPU");
  samples.push_back("WJetsToLNu_PU2010");
  samples.push_back("DYJetsToLL_PU2010");

  


  // Get the normalization from MC xsection and overall normalization to the Z peak
  LumiNormalization lumiNorm(XSectionFile, lumiFile,
			     epoch, finalState, dqApplied,"");
  lumiNorm.normalizeToZPeak(false);

  HistoStack *stacker = new HistoStack(0, finalState, "", "");

  stacker->defineGroup("zjets","Z/#gamma*",false,false,kAzure-2);
  stacker->defineGroup("wjets","W+jets",false,false,kGreen-3);
  stacker->defineGroup("ttbar","t#bar t",false,false,kRed+1); 
  stacker->defineGroup("singlet","single-t",false,false,kMagenta);
  stacker->defineGroup("wz","WZ",false,false,kYellow-8);
  stacker->defineGroup("ww","WW",false,false,kYellow-10);
  stacker->defineGroup("zz","ZZ",false,false,10);
  stacker->defineGroup("h400","H (400GeV)",false,true,kBlue+4,0);
  stacker->defineGroup("h200","H (200GeV)",false,true,kBlue,0);
  stacker->defineGroup("data","data",true,false,1,0);
 

  stacker->assignToGroup("DYJetsToLL_PU2010","zjets");
  stacker->assignToGroup("WJetsToLNu_PU2010","wjets");
  stacker->assignToGroup("TTJets_madgraph_FlatPU","ttbar");
  stacker->assignToGroup("TToBLNu_tW-channel_FlatPU","singlet");
  stacker->assignToGroup("TToBLNu_t-channel_FlatPU","singlet");
  stacker->assignToGroup("TToBLNu_s-channel_FlatPU","singlet");
  stacker->assignToGroup("H200","h200");
  stacker->assignToGroup("ZZtoAnything_FlatPU","zz");
  stacker->assignToGroup("WWtoAnything_PU2010","ww");
  stacker->assignToGroup("WZtoAnything_FlatPU","wz");
  stacker->assignToGroup("dataA","data");
  stacker->assignToGroup("dataB","data");



  stacker->setLegendOrder(0,"data");
  stacker->setLegendOrder(1,"zjets");
  stacker->setLegendOrder(2,"wjets");
  stacker->setLegendOrder(3,"ttbar");
  stacker->setLegendOrder(4,"singlet");
  stacker->setLegendOrder(5,"wz");
  stacker->setLegendOrder(6,"ww");
  stacker->setLegendOrder(7,"zz");
  stacker->setLegendOrder(8,"h200");

//   stacker->setFillColor("signal",626);
//   stacker->setFillColor("ww_wz",594);
//   stacker->setFillColor("z_ll",kAzure-2);
//   stacker->setFillColor("others",922);
  style->SetMarkerSize(0.8);


  stacker->setAxisTitles("leadLeptPt_cut0","p_{T} [GeV]","GeV");
  //  stacker->setAxisTitles("leadLeptPt","p_{T} [GeV]","GeV");

  // Loop over all the samples
  for(vector<TString>::const_iterator sName = samples.begin(); sName != samples.end();
      sName++) {

    // Open the file
    TString filePrefix;


    TString fileName = inputDir+ selection +"/ZZllvvAnalyzer_"+ *sName +".root";
    TFile *file = new TFile(fileName.Data());

    float scaleFactor = lumiNorm.getScaleFactor(*sName);
    cout << "--- sample name: " << *sName << " scale factor: " << scaleFactor << endl;    

    
    TH1F *hNVertexAll = (TH1F *) file->Get("hNVertexAll");
    hNVertexAll->Scale(scaleFactor);

    HistoLept *hMuonLead_cut0     = new HistoLept("MuonLead_cut0",file);
    hMuonLead_cut0->Scale(scaleFactor);
    HistoLept *hMuonSubLead_cut0  = new HistoLept("MuonSubLead_cut0",file);
    hMuonSubLead_cut0->Scale(scaleFactor);
    HistoKin *hDiLeptKin_cut0     = new HistoKin("DiLeptKin_cut0",file);
    hDiLeptKin_cut0->Scale(scaleFactor);
    HistoRedMET *hRedMetStd_cut0  = new HistoRedMET("RedMetStd_cut0",file);
    hRedMetStd_cut0->Scale(scaleFactor);
    HistoKin *hJetKin_cut0        = new HistoKin("JetKin_cut0",file);
    hJetKin_cut0->Scale(scaleFactor);
    HistoKin *hMETKin_cut0        = new HistoKin("METKin_cut0",file);
    hMETKin_cut0->Scale(scaleFactor);

    HistoLept *hMuonLead_cut1     = new HistoLept("MuonLead_cut1",file);
    hMuonLead_cut1->Scale(scaleFactor);
    HistoLept *hMuonSubLead_cut1  = new HistoLept("MuonSubLead_cut1",file);
    hMuonSubLead_cut1->Scale(scaleFactor);
    HistoKin *hDiLeptKin_cut1     = new HistoKin("DiLeptKin_cut1",file);
    hDiLeptKin_cut1->Scale(scaleFactor);
    HistoRedMET *hRedMetStd_cut1  = new HistoRedMET("RedMetStd_cut1",file);
    hRedMetStd_cut1->Scale(scaleFactor);
    HistoKin *hJetKin_cut1        = new HistoKin("JetKin_cut1",file);
    hJetKin_cut1->Scale(scaleFactor);
    HistoKin *hMETKin_cut1        = new HistoKin("METKin_cut1",file);
    hMETKin_cut1->Scale(scaleFactor);


    stacker->add(*sName, "leadLeptPt_cut0", hMuonLead_cut0->hPt);
    stacker->add(*sName, "leadLeptEta_cut0", hMuonLead_cut0->hEta);
    stacker->add(*sName, "leadLeptRelIso_cut0", hMuonLead_cut0->hRelIso);
    stacker->add(*sName, "leadLeptDxy_cut0", hMuonLead_cut0->hDxy);
    stacker->add(*sName, "leadLeptDz_cut0", hMuonLead_cut0->hDz);
    stacker->add(*sName, "leadLeptType_cut0", hMuonLead_cut0->hType);
    stacker->add(*sName, "leadLeptNPixelHits_cut0", hMuonLead_cut0->hNPixelHits);
    stacker->add(*sName, "leadLeptNTkHits_cut0", hMuonLead_cut0->hNTkHits);
    stacker->add(*sName, "leadLeptNMuonHits_cut0", hMuonLead_cut0->hNMuonHits);
    stacker->add(*sName, "leadLeptNMatches_cut0", hMuonLead_cut0->hNMatches);

    stacker->add(*sName, "subLeadLeptPt_cut0", hMuonSubLead_cut0->hPt);
    stacker->add(*sName, "subLeadLeptEta_cut0", hMuonSubLead_cut0->hEta);
    stacker->add(*sName, "subLeadLeptRelIso_cut0", hMuonSubLead_cut0->hRelIso);
    stacker->add(*sName, "subLeadLeptDxy_cut0", hMuonSubLead_cut0->hDxy);
    stacker->add(*sName, "subLeadLeptDz_cut0", hMuonSubLead_cut0->hDz);
    stacker->add(*sName, "subLeadLeptType_cut0", hMuonSubLead_cut0->hType);
    stacker->add(*sName, "subLeadLeptNPixelHits_cut0", hMuonSubLead_cut0->hNPixelHits);
    stacker->add(*sName, "subLeadLeptNTkHits_cut0", hMuonSubLead_cut0->hNTkHits);
    stacker->add(*sName, "subLeadLeptNMuonHits_cut0", hMuonSubLead_cut0->hNMuonHits);
    stacker->add(*sName, "subLeadLeptNMatches_cut0", hMuonSubLead_cut0->hNMatches);

    stacker->add(*sName, "diLeptPt_cut0", hDiLeptKin_cut0->hPt);
    stacker->add(*sName, "diLeptEta_cut0", hDiLeptKin_cut0->hEta);
    stacker->add(*sName, "diLeptMass_cut0", hDiLeptKin_cut0->hMass);

    stacker->add(*sName, "redMETStd_cut0", hRedMetStd_cut0->hRedMET);
    stacker->add(*sName, "redMETStdCompLong_cut0", hRedMetStd_cut0->hRedMETCompLong);
    stacker->add(*sName, "redMETStdCompPerp_cut0", hRedMetStd_cut0->hRedMETCompPerp);
    stacker->add(*sName, "redMETStdRecoilCompLong_cut0", hRedMetStd_cut0->hRecoilCompLong);
    stacker->add(*sName, "redMETStdRecoilCompPerp_cut0", hRedMetStd_cut0->hRecoilCompPerp);
    stacker->add(*sName, "redMETStdMetCompLong_cut0", hRedMetStd_cut0->hMetCompLong);
    stacker->add(*sName, "redMETStdMetCompPerp_cut0", hRedMetStd_cut0->hMetCompPerp);
    stacker->add(*sName, "redMETStdSumJetCompLong_cut0", hRedMetStd_cut0->hSumJetCompLong);
    stacker->add(*sName, "redMETStdSumJetCompPerp_cut0", hRedMetStd_cut0->hSumJetCompPerp);
    stacker->add(*sName, "redMETStdDileptonCompLong_cut0", hRedMetStd_cut0->hDileptonCompLong);
    stacker->add(*sName, "redMETStdDileptonCompPerp_cut0", hRedMetStd_cut0->hDileptonCompPerp);
    stacker->add(*sName, "redMETStdRecoilTypeLong_cut0", hRedMetStd_cut0->hRecoilTypeLong);
    stacker->add(*sName, "redMETStdRecoilTypePerp_cut0", hRedMetStd_cut0->hRecoilTypePerp);

    stacker->add(*sName, "jetPt_cut0", hJetKin_cut0->hPt);
    stacker->add(*sName, "jetEta_cut0", hJetKin_cut0->hEta);
    stacker->add(*sName, "jetN_cut0", hJetKin_cut0->hNObj);

    stacker->add(*sName, "met_cut0", hMETKin_cut0->hPt);

    stacker->add(*sName, "leadLeptPt_cut1", hMuonLead_cut1->hPt);
    stacker->add(*sName, "leadLeptEta_cut1", hMuonLead_cut1->hEta);
    stacker->add(*sName, "leadLeptRelIso_cut1", hMuonLead_cut1->hRelIso);
    stacker->add(*sName, "leadLeptDxy_cut1", hMuonLead_cut1->hDxy);
    stacker->add(*sName, "leadLeptDz_cut1", hMuonLead_cut1->hDz);
    stacker->add(*sName, "leadLeptType_cut1", hMuonLead_cut1->hType);
    stacker->add(*sName, "leadLeptNPixelHits_cut1", hMuonLead_cut1->hNPixelHits);
    stacker->add(*sName, "leadLeptNTkHits_cut1", hMuonLead_cut1->hNTkHits);
    stacker->add(*sName, "leadLeptNMuonHits_cut1", hMuonLead_cut1->hNMuonHits);
    stacker->add(*sName, "leadLeptNMatches_cut1", hMuonLead_cut1->hNMatches);

    stacker->add(*sName, "subLeadLeptPt_cut1", hMuonSubLead_cut1->hPt);
    stacker->add(*sName, "subLeadLeptEta_cut1", hMuonSubLead_cut1->hEta);
    stacker->add(*sName, "subLeadLeptRelIso_cut1", hMuonSubLead_cut1->hRelIso);
    stacker->add(*sName, "subLeadLeptDxy_cut1", hMuonSubLead_cut1->hDxy);
    stacker->add(*sName, "subLeadLeptDz_cut1", hMuonSubLead_cut1->hDz);
    stacker->add(*sName, "subLeadLeptType_cut1", hMuonSubLead_cut1->hType);
    stacker->add(*sName, "subLeadLeptNPixelHits_cut1", hMuonSubLead_cut1->hNPixelHits);
    stacker->add(*sName, "subLeadLeptNTkHits_cut1", hMuonSubLead_cut1->hNTkHits);
    stacker->add(*sName, "subLeadLeptNMuonHits_cut1", hMuonSubLead_cut1->hNMuonHits);
    stacker->add(*sName, "subLeadLeptNMatches_cut1", hMuonSubLead_cut1->hNMatches);

    stacker->add(*sName, "diLeptPt_cut1", hDiLeptKin_cut1->hPt);
    stacker->add(*sName, "diLeptEta_cut1", hDiLeptKin_cut1->hEta);
    stacker->add(*sName, "diLeptMass_cut1", hDiLeptKin_cut1->hMass);

    stacker->add(*sName, "redMETStd_cut1", hRedMetStd_cut1->hRedMET);
    stacker->add(*sName, "redMETStdCompLong_cut1", hRedMetStd_cut1->hRedMETCompLong);
    stacker->add(*sName, "redMETStdCompPerp_cut1", hRedMetStd_cut1->hRedMETCompPerp);
    stacker->add(*sName, "redMETStdRecoilCompLong_cut1", hRedMetStd_cut1->hRecoilCompLong);
    stacker->add(*sName, "redMETStdRecoilCompPerp_cut1", hRedMetStd_cut1->hRecoilCompPerp);
    stacker->add(*sName, "redMETStdMetCompLong_cut1", hRedMetStd_cut1->hMetCompLong);
    stacker->add(*sName, "redMETStdMetCompPerp_cut1", hRedMetStd_cut1->hMetCompPerp);
    stacker->add(*sName, "redMETStdSumJetCompLong_cut1", hRedMetStd_cut1->hSumJetCompLong);
    stacker->add(*sName, "redMETStdSumJetCompPerp_cut1", hRedMetStd_cut1->hSumJetCompPerp);
    stacker->add(*sName, "redMETStdDileptonCompLong_cut1", hRedMetStd_cut1->hDileptonCompLong);
    stacker->add(*sName, "redMETStdDileptonCompPerp_cut1", hRedMetStd_cut1->hDileptonCompPerp);
    stacker->add(*sName, "redMETStdRecoilTypeLong_cut1", hRedMetStd_cut1->hRecoilTypeLong);
    stacker->add(*sName, "redMETStdRecoilTypePerp_cut1", hRedMetStd_cut1->hRecoilTypePerp);

    stacker->add(*sName, "jetPt_cut1", hJetKin_cut1->hPt);
    stacker->add(*sName, "jetEta_cut1", hJetKin_cut1->hEta);
    stacker->add(*sName, "jetN_cut1", hJetKin_cut1->hNObj);

    stacker->add(*sName, "met_cut1", hMETKin_cut1->hPt);
    stacker->add(*sName, "NVertex",hNVertexAll);

//     HistoLept *hSubLeadLept_cut1 = new HistoLept("MuonLead_cut1",file);
//     hLeadLept_cut1->Scale(scaleFactor);
//     stacker->add(*sName, "leadLeptPt_cut1", hLeadLept_cut1->hPt);

    TH1F *hEventCounter = (TH1F*) file->Get("hEventCounter");
    hEventCounter->Scale(scaleFactor);
    stacker->add(*sName, "EventCounter", hEventCounter);

//     stacker->add(*sName, "muS1Eta", hMuonS1->hEta);
//     stacker->add(*sName, "muS1Phi", hMuonS1->hPhi);
//     stacker->add(*sName, "muS1Dxy", hMuonS1->hDxy);
//     stacker->add(*sName, "muS1Dz", hMuonS1->hDz);
//     stacker->add(*sName, "muS1Type", hMuonS1->hType);
//     stacker->add(*sName, "muS1NLept", hMuonS1->hNLept);
//     stacker->add(*sName, "muS1NPixelHits", hMuonS1->hNPixelHits);
//     stacker->add(*sName, "muS1NTkHits", hMuonS1->hNTkHits);
//     stacker->add(*sName, "muS1NMuonHits", hMuonS1->hNMuonHits);
//     stacker->add(*sName, "muS1NMatches", hMuonS1->hNMatches);

  }
    
  //stacker->drawAll();
  stacker->draw("NVertex");
  cout << "Normalization factor: " << lumiNorm.getNormalizationFactor() << endl;
}
