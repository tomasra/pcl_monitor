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
#include "root_lib/SampleGroup.h"
#include "root_lib/CutTableBuilder.h"

// #include "HistoAlat.h"
#include <iostream>
#include <string>
#endif



using namespace std;


// -----------------------------------------------------------
//TString baseInputDir = "/castor/cern.ch/cms/store/cmst3/user/cerminar/Analysis/ZZllvv_v01/";
TString inputDir = "/data/Analysis/ZZllvv_v01/";
TString selection = "anal3";

TString XSectionFile = "Xsection_v0.txt";
TString lumiFile = "Luminosity.txt";
TString finalState = "dimu";
bool dqApplied = true;
TString epoch = "all2010";

bool cut0 = false;
bool cut1 = true;

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
  style->SetPalette(1);
  style->cd(); 
  
  // --------------------------------
  
  vector<TString> samples;
  samples.push_back("MuRun2010A");
  samples.push_back("MuRun2010B");
  samples.push_back("H200");
  samples.push_back("H400");
  samples.push_back("ZZtoAnything_FlatPU");
  samples.push_back("WWtoAnything_PU2010");
  samples.push_back("WZtoAnything_FlatPU");
  samples.push_back("TToBLNu_tW-channel_FlatPU");
  samples.push_back("TToBLNu_t-channel_FlatPU");
  samples.push_back("TToBLNu_s-channel_FlatPU");
  samples.push_back("TTJets_madgraph_FlatPU");
  samples.push_back("WJetsToLNu_PU2010");
  samples.push_back("DYJetsToLL_PU2010");

  SampleGroup zjets("zjets","Z/#gamma*","$Z\\rightarrow ll$", false,false,kAzure-2);
  zjets.addSample("DYJetsToLL_PU2010");
  SampleGroup wjets("wjets","W+jets","$W+jets$",false,false,kGreen-3);
  wjets.addSample("WJetsToLNu_PU2010");
  SampleGroup ttbar("ttbar","t#bar t","$t\\bar{t}$",false,false,kRed+1); 
  ttbar.addSample("TTJets_madgraph_FlatPU");
  SampleGroup singlet("singlet","single-t","single$-t$", false,false,kMagenta);
  singlet.addSample("TToBLNu_tW-channel_FlatPU");
  singlet.addSample("TToBLNu_t-channel_FlatPU");
  singlet.addSample("TToBLNu_s-channel_FlatPU");
  SampleGroup wz("wz","WZ","$WZ$",false,false,kYellow-8);
  wz.addSample("WZtoAnything_FlatPU");
  SampleGroup ww("ww","WW","$WW$",false,false,kYellow-10);
  ww.addSample("WWtoAnything_PU2010");
  SampleGroup zz("zz","ZZ","$ZZ$",false,false,10);
  zz.addSample("ZZtoAnything_FlatPU");
  SampleGroup h400("h400","H (400GeV) x 10","H (400GeV)",false,true,kRed,0, true);
  h400.addSample("H400");
  SampleGroup h200("h200","H (200GeV) x 10","H (200GeV)",false,true,kBlue,0, true);
  h200.addSample("H200");
  SampleGroup data("data","data","data",true,false,1,0);
  data.addSample("MuRun2010A");
  data.addSample("MuRun2010B");


  // Get the normalization from MC xsection and overall normalization to the Z peak
  LumiNormalization lumiNorm(XSectionFile, lumiFile,
			     epoch, finalState, dqApplied,"");
  lumiNorm.addDataGroup(data);
  lumiNorm.normalizeToZPeak(false);

  CutTableBuilder cutTableBuild;
  cutTableBuild.addSampleGroup(zjets);
  cutTableBuild.addSampleGroup(wjets);
  cutTableBuild.addSampleGroup(ttbar);
  cutTableBuild.addSampleGroup(singlet);
  cutTableBuild.addSampleGroup(wz);
  cutTableBuild.addSampleGroup(ww);
  cutTableBuild.addSampleGroup(zz);
  cutTableBuild.addSampleGroup(h400);
  cutTableBuild.addSampleGroup(h200);
  cutTableBuild.addSampleGroup(data);

  cutTableBuild.setCut("preSkim", "pre-skim", 1);
  cutTableBuild.setCut("baseFilter", "base filter", 2);
  cutTableBuild.setCut("skim", "skim", 3);

  cutTableBuild.setCut("cut0", "di-lepton", 5);
  cutTableBuild.setCut("cut1", "mass (ll)", 7);
  cutTableBuild.setCut("jet0", "0 jets", 8);
  cutTableBuild.setCut("jet1", "1 jets", 9);
  

  HistoStack *stacker = new HistoStack(0, finalState, "", "");

  stacker->addGroup(zjets);
  stacker->addGroup(wjets);
  stacker->addGroup(ttbar);
  stacker->addGroup(singlet);
  stacker->addGroup(wz);
  stacker->addGroup(ww);
  stacker->addGroup(zz);
  stacker->addGroup(h400);
  stacker->addGroup(h200);
  stacker->addGroup(data);
 

  stacker->setLegendOrder(0,"data");
  stacker->setLegendOrder(1,"zjets");
  stacker->setLegendOrder(2,"wjets");
  stacker->setLegendOrder(3,"ttbar");
  stacker->setLegendOrder(4,"singlet");
  stacker->setLegendOrder(5,"wz");
  stacker->setLegendOrder(6,"ww");
  stacker->setLegendOrder(7,"zz");
  stacker->setLegendOrder(8,"h200");
  stacker->setLegendOrder(9,"h400");

//   stacker->setFillColor("signal",626);
//   stacker->setFillColor("ww_wz",594);
//   stacker->setFillColor("z_ll",kAzure-2);
//   stacker->setFillColor("others",922);
  style->SetMarkerSize(0.8);


  stacker->setAxisTitles("leadLeptPt_cut0","p_{T} [GeV]","GeV");


  stacker->setAxisTitles("redMETStd_cut0","reduced #slash E_{T} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdCompLong_cut0","reduced #slash (E_{T})_{L} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdCompPerp_cut0","reduced #slash (E_{T})_{T} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdRecoilCompLong_cut0","recoil R_{L} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdRecoilCompPerp_cut0","recoil R_{T} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdMetCompLong_cut0","MET (Calo Only) recoil R_{L} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdMetCompPerp_cut0","MET (Calo Only) recoil R_{T} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdSumJetCompLong_cut0","#Sigma jet recoil R_{L} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdSumJetCompPerp_cut0","#Sigma jet recoil R_{T} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdDileptonCompLong_cut0","di-lepton p_{T} L [GeV]","GeV");
  stacker->setAxisTitles("redMETStdDileptonCompPerp_cut0","di-lepton p_{T} T [GeV]","GeV");
  stacker->setAxisTitles("redMETStdRecoilTypeLong_cut0","recoil type","");
  stacker->setAxisTitles("redMETStdRecoilTypePerp_cut0","recoil type","");



  stacker->setAxisTitles("redMETStd_cut1","reduced #slash E_{T} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdCompLong_cut1","reduced #slash (E_{T})_{L} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdCompPerp_cut1","reduced #slash (E_{T})_{T} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdRecoilCompLong_cut1","recoil R_{L} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdRecoilCompPerp_cut1","recoil R_{T} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdMetCompLong_cut1","MET (Calo Only) recoil R_{L} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdMetCompPerp_cut1","MET (Calo Only) recoil R_{T} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdSumJetCompLong_cut1","#Sigma jet recoil R_{L} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdSumJetCompPerp_cut1","#Sigma jet recoil R_{T} [GeV]","GeV");
  stacker->setAxisTitles("redMETStdDileptonCompLong_cut1","di-lepton p_{T} L [GeV]","GeV");
  stacker->setAxisTitles("redMETStdDileptonCompPerp_cut1","di-lepton p_{T} T [GeV]","GeV");
  stacker->setAxisTitles("redMETStdRecoilTypeLong_cut1","recoil type","");
  stacker->setAxisTitles("redMETStdRecoilTypePerp_cut1","recoil type","");


  
  //  stacker->setAxisTitles("leadLeptPt","p_{T} [GeV]","GeV");
  TLine *lineStd = new TLine(0,0, -75,150);
  lineStd->SetLineColor(2);
  lineStd->SetLineStyle(2);
  lineStd->SetLineWidth(4);
  
  // Loop over all the samples
  for(vector<TString>::const_iterator sName = samples.begin(); sName != samples.end();
      sName++) {

    // Open the file
    TString filePrefix;


    TString fileName = inputDir+ selection +"/ZZllvvAnalyzer_"+ *sName +".root";
    TFile *file = new TFile(fileName.Data());

    float scaleFactor = lumiNorm.getScaleFactor(*sName);
    cout << "--- sample name: " << *sName << " scale factor: " << scaleFactor << endl;    
    double scaleForCutflow = scaleFactor;
    if(*sName == "H200" || *sName == "H400") scaleFactor = scaleFactor*10.;
    
    TH1F *hNVertexAll = (TH1F *) file->Get("hNVertexAll");
    hNVertexAll->Scale(scaleFactor);

    TH1F *hEventCounter = (TH1F*) file->Get("hEventCounter");
    hEventCounter->Scale(scaleForCutflow);
    cutTableBuild.getValuesFromHisto(*sName,hEventCounter);

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

    // plots reduced MET
    HistoRedMET *hRedMetStd_cut1  = new HistoRedMET("RedMetStd_cut1",file);
    hRedMetStd_cut1->Scale(scaleFactor);
    HistoRedMET *hRedMetStd_J0_cut1 = new HistoRedMET("RedMetStd_J0__cut1",file);
    hRedMetStd_J0_cut1->Scale(scaleFactor);
    HistoRedMET *hRedMetStd_J1_cut1 = new HistoRedMET("RedMetStd_J1_cut1",file);
    hRedMetStd_J1_cut1->Scale(scaleFactor);

    HistoRedMET *hRedMetTuneA_cut1 = new HistoRedMET("RedMetTuneA_cut1",file);
    hRedMetTuneA_cut1->Scale(scaleFactor);
    HistoRedMET *hRedMetTuneA_J0_cut1 = new HistoRedMET("RedMetTuneA_J0_cut1",file);
    hRedMetTuneA_J0_cut1->Scale(scaleFactor);
    HistoRedMET *hRedMetTuneA_J1_cut1 = new HistoRedMET("RedMetTuneA_J1_cut1",file);
    hRedMetTuneA_J1_cut1->Scale(scaleFactor);
    HistoRedMET *hRedMetTuneB_cut1 = new HistoRedMET("RedMetTuneB_cut1",file);
    hRedMetTuneB_cut1->Scale(scaleFactor);
    HistoRedMET *hRedMetTuneB_J0_cut1 = new HistoRedMET("RedMetTuneB_J0_cut1",file);
    hRedMetTuneB_J0_cut1->Scale(scaleFactor);
    HistoRedMET *hRedMetTuneB_J1_cut1 = new HistoRedMET("RedMetTuneB_J1_cut1",file);
    hRedMetTuneB_J1_cut1->Scale(scaleFactor);


    HistoKin *hJetKin_cut1        = new HistoKin("JetKin_cut1",file);
    hJetKin_cut1->Scale(scaleFactor);
    HistoKin *hMETKin_cut1        = new HistoKin("METKin_cut1",file);
    hMETKin_cut1->Scale(scaleFactor);

    if(cut0) {
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
    }

    if(cut1) {
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

      // std
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

      stacker->add(*sName, "redMETStdDilepSigmaPtCompLong_cut1", hRedMetStd_cut1->hDileptSigmaPtCompLong);
      stacker->add(*sName, "redMETStdDileptSigmaPtCompPerp_cut1", hRedMetStd_cut1->hDileptSigmaPtCompPerp);

      stacker->add(*sName, "redMETStdRecoilTypeLong_cut1", hRedMetStd_cut1->hRecoilTypeLong);
      stacker->add(*sName, "redMETStdRecoilTypePerp_cut1", hRedMetStd_cut1->hRecoilTypePerp);


      stacker->add(*sName, "redMETStd_J0_cut1", hRedMetStd_J0_cut1->hRedMET);
      stacker->add(*sName, "redMETStd_J0CompLong_cut1", hRedMetStd_J0_cut1->hRedMETCompLong);
      stacker->add(*sName, "redMETStd_J0CompPerp_cut1", hRedMetStd_J0_cut1->hRedMETCompPerp);
      stacker->add(*sName, "redMETStd_J0RecoilCompLong_cut1", hRedMetStd_J0_cut1->hRecoilCompLong);
      stacker->add(*sName, "redMETStd_J0RecoilCompPerp_cut1", hRedMetStd_J0_cut1->hRecoilCompPerp);
      stacker->add(*sName, "redMETStd_J0MetCompLong_cut1", hRedMetStd_J0_cut1->hMetCompLong);
      stacker->add(*sName, "redMETStd_J0MetCompPerp_cut1", hRedMetStd_J0_cut1->hMetCompPerp);
      stacker->add(*sName, "redMETStd_J0SumJetCompLong_cut1", hRedMetStd_J0_cut1->hSumJetCompLong);
      stacker->add(*sName, "redMETStd_J0SumJetCompPerp_cut1", hRedMetStd_J0_cut1->hSumJetCompPerp);
      stacker->add(*sName, "redMETStd_J0DileptonCompLong_cut1", hRedMetStd_J0_cut1->hDileptonCompLong);
      stacker->add(*sName, "redMETStd_J0DileptonCompPerp_cut1", hRedMetStd_J0_cut1->hDileptonCompPerp);
      stacker->add(*sName, "redMETStd_J0RecoilTypeLong_cut1", hRedMetStd_J0_cut1->hRecoilTypeLong);
      stacker->add(*sName, "redMETStd_J0RecoilTypePerp_cut1", hRedMetStd_J0_cut1->hRecoilTypePerp);

      stacker->add(*sName, "redMETStd_J1_cut1", hRedMetStd_J1_cut1->hRedMET);
      stacker->add(*sName, "redMETStd_J1CompLong_cut1", hRedMetStd_J1_cut1->hRedMETCompLong);
      stacker->add(*sName, "redMETStd_J1CompPerp_cut1", hRedMetStd_J1_cut1->hRedMETCompPerp);
      stacker->add(*sName, "redMETStd_J1RecoilCompLong_cut1", hRedMetStd_J1_cut1->hRecoilCompLong);
      stacker->add(*sName, "redMETStd_J1RecoilCompPerp_cut1", hRedMetStd_J1_cut1->hRecoilCompPerp);
      stacker->add(*sName, "redMETStd_J1MetCompLong_cut1", hRedMetStd_J1_cut1->hMetCompLong);
      stacker->add(*sName, "redMETStd_J1MetCompPerp_cut1", hRedMetStd_J1_cut1->hMetCompPerp);
      stacker->add(*sName, "redMETStd_J1SumJetCompLong_cut1", hRedMetStd_J1_cut1->hSumJetCompLong);
      stacker->add(*sName, "redMETStd_J1SumJetCompPerp_cut1", hRedMetStd_J1_cut1->hSumJetCompPerp);
      stacker->add(*sName, "redMETStd_J1DileptonCompLong_cut1", hRedMetStd_J1_cut1->hDileptonCompLong);
      stacker->add(*sName, "redMETStd_J1DileptonCompPerp_cut1", hRedMetStd_J1_cut1->hDileptonCompPerp);
      stacker->add(*sName, "redMETStd_J1RecoilTypeLong_cut1", hRedMetStd_J1_cut1->hRecoilTypeLong);
      stacker->add(*sName, "redMETStd_J1RecoilTypePerp_cut1", hRedMetStd_J1_cut1->hRecoilTypePerp);


      // tuneA
//       stacker->add(*sName, "redMETTuneA_cut1", hRedMetTuneA_cut1->hRedMET);
//       stacker->add(*sName, "redMETTuneACompLong_cut1", hRedMetTuneA_cut1->hRedMETCompLong);
//       stacker->add(*sName, "redMETTuneACompPerp_cut1", hRedMetTuneA_cut1->hRedMETCompPerp);
//       stacker->add(*sName, "redMETTuneARecoilCompLong_cut1", hRedMetTuneA_cut1->hRecoilCompLong);
//       stacker->add(*sName, "redMETTuneARecoilCompPerp_cut1", hRedMetTuneA_cut1->hRecoilCompPerp);
//       stacker->add(*sName, "redMETTuneAMetCompLong_cut1", hRedMetTuneA_cut1->hMetCompLong);
//       stacker->add(*sName, "redMETTuneAMetCompPerp_cut1", hRedMetTuneA_cut1->hMetCompPerp);
//       stacker->add(*sName, "redMETTuneASumJetCompLong_cut1", hRedMetTuneA_cut1->hSumJetCompLong);
//       stacker->add(*sName, "redMETTuneASumJetCompPerp_cut1", hRedMetTuneA_cut1->hSumJetCompPerp);
//       stacker->add(*sName, "redMETTuneADileptonCompLong_cut1", hRedMetTuneA_cut1->hDileptonCompLong);
//       stacker->add(*sName, "redMETTuneADileptonCompPerp_cut1", hRedMetTuneA_cut1->hDileptonCompPerp);
//       stacker->add(*sName, "redMETTuneARecoilTypeLong_cut1", hRedMetTuneA_cut1->hRecoilTypeLong);
//       stacker->add(*sName, "redMETTuneARecoilTypePerp_cut1", hRedMetTuneA_cut1->hRecoilTypePerp);

      stacker->add(*sName, "redMETTuneA_J0_cut1", hRedMetTuneA_J0_cut1->hRedMET);
      stacker->add(*sName, "redMETTuneA_J0CompLong_cut1", hRedMetTuneA_J0_cut1->hRedMETCompLong);
      stacker->add(*sName, "redMETTuneA_J0CompPerp_cut1", hRedMetTuneA_J0_cut1->hRedMETCompPerp);
      stacker->add(*sName, "redMETTuneA_J0RecoilCompLong_cut1", hRedMetTuneA_J0_cut1->hRecoilCompLong);
      stacker->add(*sName, "redMETTuneA_J0RecoilCompPerp_cut1", hRedMetTuneA_J0_cut1->hRecoilCompPerp);
      stacker->add(*sName, "redMETTuneA_J0MetCompLong_cut1", hRedMetTuneA_J0_cut1->hMetCompLong);
      stacker->add(*sName, "redMETTuneA_J0MetCompPerp_cut1", hRedMetTuneA_J0_cut1->hMetCompPerp);
      stacker->add(*sName, "redMETTuneA_J0SumJetCompLong_cut1", hRedMetTuneA_J0_cut1->hSumJetCompLong);
      stacker->add(*sName, "redMETTuneA_J0SumJetCompPerp_cut1", hRedMetTuneA_J0_cut1->hSumJetCompPerp);
      stacker->add(*sName, "redMETTuneA_J0DileptonCompLong_cut1", hRedMetTuneA_J0_cut1->hDileptonCompLong);
      stacker->add(*sName, "redMETTuneA_J0DileptonCompPerp_cut1", hRedMetTuneA_J0_cut1->hDileptonCompPerp);
      stacker->add(*sName, "redMETTuneA_J0RecoilTypeLong_cut1", hRedMetTuneA_J0_cut1->hRecoilTypeLong);
      stacker->add(*sName, "redMETTuneA_J0RecoilTypePerp_cut1", hRedMetTuneA_J0_cut1->hRecoilTypePerp);

      stacker->add(*sName, "redMETTuneA_J1_cut1", hRedMetTuneA_J1_cut1->hRedMET);
      stacker->add(*sName, "redMETTuneA_J1CompLong_cut1", hRedMetTuneA_J1_cut1->hRedMETCompLong);
      stacker->add(*sName, "redMETTuneA_J1CompPerp_cut1", hRedMetTuneA_J1_cut1->hRedMETCompPerp);
      stacker->add(*sName, "redMETTuneA_J1RecoilCompLong_cut1", hRedMetTuneA_J1_cut1->hRecoilCompLong);
      stacker->add(*sName, "redMETTuneA_J1RecoilCompPerp_cut1", hRedMetTuneA_J1_cut1->hRecoilCompPerp);
      stacker->add(*sName, "redMETTuneA_J1MetCompLong_cut1", hRedMetTuneA_J1_cut1->hMetCompLong);
      stacker->add(*sName, "redMETTuneA_J1MetCompPerp_cut1", hRedMetTuneA_J1_cut1->hMetCompPerp);
      stacker->add(*sName, "redMETTuneA_J1SumJetCompLong_cut1", hRedMetTuneA_J1_cut1->hSumJetCompLong);
      stacker->add(*sName, "redMETTuneA_J1SumJetCompPerp_cut1", hRedMetTuneA_J1_cut1->hSumJetCompPerp);
      stacker->add(*sName, "redMETTuneA_J1DileptonCompLong_cut1", hRedMetTuneA_J1_cut1->hDileptonCompLong);
      stacker->add(*sName, "redMETTuneA_J1DileptonCompPerp_cut1", hRedMetTuneA_J1_cut1->hDileptonCompPerp);
      stacker->add(*sName, "redMETTuneA_J1RecoilTypeLong_cut1", hRedMetTuneA_J1_cut1->hRecoilTypeLong);
      stacker->add(*sName, "redMETTuneA_J1RecoilTypePerp_cut1", hRedMetTuneA_J1_cut1->hRecoilTypePerp);


//       // tuneB
//       stacker->add(*sName, "redMETTuneB_cut1", hRedMetTuneB_cut1->hRedMET);
//       stacker->add(*sName, "redMETTuneBCompLong_cut1", hRedMetTuneB_cut1->hRedMETCompLong);
//       stacker->add(*sName, "redMETTuneBCompPerp_cut1", hRedMetTuneB_cut1->hRedMETCompPerp);
//       stacker->add(*sName, "redMETTuneBRecoilCompLong_cut1", hRedMetTuneB_cut1->hRecoilCompLong);
//       stacker->add(*sName, "redMETTuneBRecoilCompPerp_cut1", hRedMetTuneB_cut1->hRecoilCompPerp);
//       stacker->add(*sName, "redMETTuneBMetCompLong_cut1", hRedMetTuneB_cut1->hMetCompLong);
//       stacker->add(*sName, "redMETTuneBMetCompPerp_cut1", hRedMetTuneB_cut1->hMetCompPerp);
//       stacker->add(*sName, "redMETTuneBSumJetCompLong_cut1", hRedMetTuneB_cut1->hSumJetCompLong);
//       stacker->add(*sName, "redMETTuneBSumJetCompPerp_cut1", hRedMetTuneB_cut1->hSumJetCompPerp);
//       stacker->add(*sName, "redMETTuneBDileptonCompLong_cut1", hRedMetTuneB_cut1->hDileptonCompLong);
//       stacker->add(*sName, "redMETTuneBDileptonCompPerp_cut1", hRedMetTuneB_cut1->hDileptonCompPerp);
//       stacker->add(*sName, "redMETTuneBRecoilTypeLong_cut1", hRedMetTuneB_cut1->hRecoilTypeLong);
//       stacker->add(*sName, "redMETTuneBRecoilTypePerp_cut1", hRedMetTuneB_cut1->hRecoilTypePerp);

      stacker->add(*sName, "redMETTuneB_J0_cut1", hRedMetTuneB_J0_cut1->hRedMET);
      stacker->add(*sName, "redMETTuneB_J0CompLong_cut1", hRedMetTuneB_J0_cut1->hRedMETCompLong);
      stacker->add(*sName, "redMETTuneB_J0CompPerp_cut1", hRedMetTuneB_J0_cut1->hRedMETCompPerp);
      stacker->add(*sName, "redMETTuneB_J0RecoilCompLong_cut1", hRedMetTuneB_J0_cut1->hRecoilCompLong);
      stacker->add(*sName, "redMETTuneB_J0RecoilCompPerp_cut1", hRedMetTuneB_J0_cut1->hRecoilCompPerp);
      stacker->add(*sName, "redMETTuneB_J0MetCompLong_cut1", hRedMetTuneB_J0_cut1->hMetCompLong);
      stacker->add(*sName, "redMETTuneB_J0MetCompPerp_cut1", hRedMetTuneB_J0_cut1->hMetCompPerp);
      stacker->add(*sName, "redMETTuneB_J0SumJetCompLong_cut1", hRedMetTuneB_J0_cut1->hSumJetCompLong);
      stacker->add(*sName, "redMETTuneB_J0SumJetCompPerp_cut1", hRedMetTuneB_J0_cut1->hSumJetCompPerp);
      stacker->add(*sName, "redMETTuneB_J0DileptonCompLong_cut1", hRedMetTuneB_J0_cut1->hDileptonCompLong);
      stacker->add(*sName, "redMETTuneB_J0DileptonCompPerp_cut1", hRedMetTuneB_J0_cut1->hDileptonCompPerp);
      stacker->add(*sName, "redMETTuneB_J0RecoilTypeLong_cut1", hRedMetTuneB_J0_cut1->hRecoilTypeLong);
      stacker->add(*sName, "redMETTuneB_J0RecoilTypePerp_cut1", hRedMetTuneB_J0_cut1->hRecoilTypePerp);

      stacker->add(*sName, "redMETTuneB_J1_cut1", hRedMetTuneB_J1_cut1->hRedMET);
      stacker->add(*sName, "redMETTuneB_J1CompLong_cut1", hRedMetTuneB_J1_cut1->hRedMETCompLong);
      stacker->add(*sName, "redMETTuneB_J1CompPerp_cut1", hRedMetTuneB_J1_cut1->hRedMETCompPerp);
      stacker->add(*sName, "redMETTuneB_J1RecoilCompLong_cut1", hRedMetTuneB_J1_cut1->hRecoilCompLong);
      stacker->add(*sName, "redMETTuneB_J1RecoilCompPerp_cut1", hRedMetTuneB_J1_cut1->hRecoilCompPerp);
      stacker->add(*sName, "redMETTuneB_J1MetCompLong_cut1", hRedMetTuneB_J1_cut1->hMetCompLong);
      stacker->add(*sName, "redMETTuneB_J1MetCompPerp_cut1", hRedMetTuneB_J1_cut1->hMetCompPerp);
      stacker->add(*sName, "redMETTuneB_J1SumJetCompLong_cut1", hRedMetTuneB_J1_cut1->hSumJetCompLong);
      stacker->add(*sName, "redMETTuneB_J1SumJetCompPerp_cut1", hRedMetTuneB_J1_cut1->hSumJetCompPerp);
      stacker->add(*sName, "redMETTuneB_J1DileptonCompLong_cut1", hRedMetTuneB_J1_cut1->hDileptonCompLong);
      stacker->add(*sName, "redMETTuneB_J1DileptonCompPerp_cut1", hRedMetTuneB_J1_cut1->hDileptonCompPerp);
      stacker->add(*sName, "redMETTuneB_J1RecoilTypeLong_cut1", hRedMetTuneB_J1_cut1->hRecoilTypeLong);
      stacker->add(*sName, "redMETTuneB_J1RecoilTypePerp_cut1", hRedMetTuneB_J1_cut1->hRecoilTypePerp);



      stacker->add(*sName, "jetPt_cut1", hJetKin_cut1->hPt);
      stacker->add(*sName, "jetEta_cut1", hJetKin_cut1->hEta);
      stacker->add(*sName, "jetN_cut1", hJetKin_cut1->hNObj);

      stacker->add(*sName, "met_cut1", hMETKin_cut1->hPt);
      
      
      
    }


//     HistoLept *hSubLeadLept_cut1 = new HistoLept("MuonLead_cut1",file);
//     hLeadLept_cut1->Scale(scaleFactor);
//     stacker->add(*sName, "leadLeptPt_cut1", hLeadLept_cut1->hPt);

    stacker->add(*sName, "EventCounter", hEventCounter);
    stacker->add(*sName, "NVertex",hNVertexAll);

    
    newCanvas("c_" + *sName + TString("_diLeptVsRecoilLong"))->cd();
    hRedMetStd_cut1->hDileptonVsRecoilCompLong->Draw("COLZ");
    lineStd->Draw("same");
    newCanvas("c_" + *sName + TString("_diLeptVsRecoilPerp"))->cd();
    hRedMetStd_cut1->hDileptonVsRecoilCompPerp->Draw("COLZ");
    lineStd->Draw("same");

    newCanvas("c_" + *sName + TString("_J0_diLeptVsRecoilLong"))->cd();
    hRedMetStd_J0_cut1->hDileptonVsRecoilCompLong->Draw("COLZ");
    lineStd->Draw("same");
    newCanvas("c_" + *sName + TString("_J0_diLeptVsRecoilPerp"))->cd();
    hRedMetStd_J0_cut1->hDileptonVsRecoilCompPerp->Draw("COLZ");
    lineStd->Draw("same");

    newCanvas("c_" + *sName + TString("_J1_diLeptVsRecoilLong"))->cd();
    hRedMetStd_J1_cut1->hDileptonVsRecoilCompLong->Draw("COLZ");
    lineStd->Draw("same");
    newCanvas("c_" + *sName + TString("_J1_diLeptVsRecoilPerp"))->cd();
    hRedMetStd_J1_cut1->hDileptonVsRecoilCompPerp->Draw("COLZ");
    lineStd->Draw("same");

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
    
  //  stacker->drawAll("pre,d0lumi,dimu");
  stacker->drawAll();
  //  stacker->draw("NVertex");
  cout << "Normalization factor: " << lumiNorm.getNormalizationFactor() << endl;

  //cutTableBuild.printTableSampleVsCut();
  cutTableBuild.printTableCutVsSample();
}
