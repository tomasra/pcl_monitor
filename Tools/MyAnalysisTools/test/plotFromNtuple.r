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
#include "root_lib/LikelihoodDisc.h"

// #include "HistoAlat.h"
#include <iostream>
#include <string>

#include "TMVA/Factory.h"
#include "TMVA/MethodCategory.h"
#include "TMVA/Reader.h"

#endif



using namespace std;
using namespace TMVA;


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

bool toUnity = false;

// -----------------------------------------------------------


// TMVA configuration -------------------------------------------------------------------
TString cutForTraining = "category == 1 && pass >= 1 && hasTrigger == 1 && redmet > 30";
//TString cutForEvaluation = "category == 1 && pass >= 3 && hasTrigger == 1 && redmet > 39";
TString cutForEvaluation = "category == 1 && pass >= 3 && hasTrigger == 1 && redmet > 57";
// TString cutForEvaluation = "category == 1 && pass >= 1";

bool doLikelihood = false;
bool doTMVA = false;
bool doCategories = false;
bool doEvaluate = false;
bool doTraining = false;
// end TMVA configuration -------------------------------------------------------------------



void plot1DHistos(TH1 *hSign, TH1 *hBck, int rebin = 1, bool flip = false, bool scale = true );


void addPlainHisto(TFile *file, HistoStack* stacker, double scaleFactor,
		   const TString& sampleName, const TString& varName, const TString& hname, bool toUnity = false) {
  
  TH1F* histo = (TH1F *) file->Get(hname.Data());
  if(toUnity) {
    scaleFactor = 1./histo->Integral();
  }
  histo->Scale(scaleFactor);
  stacker->add(sampleName, varName, histo);
}

void plotFromNtuple() {
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
  style->SetLabelSize(0.055, "XYZ");
  style->cd(); 
  
  // --------------------------------
  vector<TString> samples;

  
//   // sel3
//   samples.push_back("DoubleMuon-v3");
//   samples.push_back("DoubleMuon-v5");
//   samples.push_back("DoubleMuon-v6");
//   samples.push_back("DoubleMuon-v7");
//   samples.push_back("DoubleMuon-v8");
//   samples.push_back("DoubleMuon-v9");
//   samples.push_back("WWtoAnything_Spring11");
//   samples.push_back("WZtoAnything_Spring11");
//   samples.push_back("ZZtoAnything_Spring11");
//   samples.push_back("TTJets_madgraph_Spring11");
//   samples.push_back("TToBLNu_s-channel_Spring11");
//   samples.push_back("TToBLNu_t-channel_Spring11");
//   samples.push_back("TToBLNu_tW-channel_Spring11");
//   samples.push_back("DYToMuMu_M-20_Spring11");
//   samples.push_back("GluGluToHToWWTo2L2Nu_M-200_Spring11");
//   samples.push_back("GluGluToHToWWTo2L2Nu_M-400_Spring11");
//   samples.push_back("GluGluToHToZZTo2L2Nu_M-200_Spring11");
//   samples.push_back("GluGluToHToZZTo2L2Nu_M-400_Spring11");
//   inputDir = "/tmp/cerminar/";
//   selection = "sel3/";
//   epoch = "data2011";
//   XSectionFile = "xsec_mumunoqcdsamples_Spring11.txt";
//   XSectionFile = "xsec1.txt";


//   // sel4
//   inputDir = "/tmp/cerminar/";
//   selection = "sel4/";
//   bool doLikelihood = false;
//   samples.push_back("DoubleMuMay10ReReco");
//   samples.push_back("DoubleMuPromptReco");
//   samples.push_back("WWTo2L2Nu");
//   samples.push_back("WZTo3LNu");
//   samples.push_back("ZZto2l2Nu");
//   samples.push_back("TTJets");
//   samples.push_back("SingleT_tW");
//   samples.push_back("SingleTbar_tW");
//   samples.push_back("WJetsToLNu");
//   samples.push_back("DYJetsToLL");
//   samples.push_back("GGtoH200toWWto2L2Nu");
//   samples.push_back("GGtoH200toZZto2L2Nu");
//   samples.push_back("GGtoH300toZZto2L2Nu");
//   samples.push_back("GGtoH500toZZto2L2Nu");
//   XSectionFile = "xsec_42X.txt";
//   epoch = "data2011-EPS";

//   // sel5
//   inputDir = "/tmp/cerminar/";
//   selection = "sel5/";
//   samples.push_back("DoubleMuMay10ReReco");
//   samples.push_back("DoubleMuPromptReco");
//   samples.push_back("WWTo2L2Nu");
//   samples.push_back("WZTo3LNu");
//   samples.push_back("ZZto2l2Nu");
//   samples.push_back("TTJets");
//   samples.push_back("SingleT_tW");
//   samples.push_back("SingleTbar_tW");
//   samples.push_back("WJetsToLNu");
//   samples.push_back("DYJetsToLL");
//   samples.push_back("GGtoH200toWWto2L2Nu");
//   samples.push_back("GGtoH200toZZto2L2Nu");
//   samples.push_back("VBFtoH200toZZto2L2Nu");
//   samples.push_back("GGtoH300toZZto2L2Nu");
//   samples.push_back("VBFtoH300toZZto2L2Nu");
//   samples.push_back("GGtoH500toZZto2L2Nu");
//   samples.push_back("VBFtoH500toZZto2L2Nu");
//   XSectionFile = "xsec_42X_110810.txt";
//   epoch = "data2011-EPS";

//   // sel6
//   inputDir = "/tmp/cerminar/";
//   selection = "sel6/";

//   samples.push_back("DoubleMu05AugReReco");
//   samples.push_back("DoubleMuMay10ReReco");
//   samples.push_back("DoubleMuPromptRecov4");
//   samples.push_back("DoubleMuPromptRecov6_172620_173244");
  

//   samples.push_back("WW");
//   samples.push_back("WZ");
//   samples.push_back("ZZ");
//   samples.push_back("TTJets");
//   samples.push_back("SingleTbar_tW");
//   samples.push_back("SingleTbar_t");
//   samples.push_back("SingleT_tW");
//   samples.push_back("SingleT_t");
  
//   samples.push_back("WJetsToLNu");
//   samples.push_back("DYJetsToLL");
//   samples.push_back("GGtoH200toWWto2L2Nu");
//   samples.push_back("GGtoH200toZZto2L2Nu");
//   samples.push_back("VBFtoH200toZZto2L2Nu");

//   samples.push_back("GGtoH300toWWto2L2Nu");
//   samples.push_back("GGtoH300toZZto2L2Nu");
//   samples.push_back("VBFtoH300toZZto2L2Nu");

//   samples.push_back("GGtoH500toWWto2L2Nu");
//   samples.push_back("GGtoH500toZZto2L2Nu");
//   samples.push_back("VBFtoH500toZZto2L2Nu");


//   XSectionFile = "xsec_42X_110823.txt";
//   epoch = "data2011-sel6";

  // sel7
  inputDir = "/data/Analysis/rootuples";
  selection = "sel7/";

  samples.push_back("DoubleMu05AugReReco");
  samples.push_back("DoubleMuMay10ReReco");
  samples.push_back("DoubleMuPromptRecov4");
  samples.push_back("DoubleMuPromptRecov6_172620_173244");
  

  samples.push_back("WW");
  samples.push_back("WZ");
  samples.push_back("ZZ");
  samples.push_back("TTJets");
  samples.push_back("SingleTbar_tW");
  samples.push_back("SingleTbar_t");
  samples.push_back("SingleT_tW");
  samples.push_back("SingleT_t");
  
  samples.push_back("WJetsToLNu");
  samples.push_back("DYJetsToLL");
  samples.push_back("GGtoH200toWWto2L2Nu");
  samples.push_back("GGtoH200toZZto2L2Nu");
  samples.push_back("VBFtoH200toZZto2L2Nu");

  samples.push_back("GGtoH300toWWto2L2Nu");
  samples.push_back("GGtoH300toZZto2L2Nu");
  samples.push_back("VBFtoH300toZZto2L2Nu");

  samples.push_back("GGtoH500toWWto2L2Nu");
  samples.push_back("GGtoH500toZZto2L2Nu");
  samples.push_back("VBFtoH500toZZto2L2Nu");


  XSectionFile = "xsec_42X_110823.txt";
  epoch = "data2011-sel7";


//   samples.push_back("VBFtoH200toZZto2L2Nu");
//   samples.push_back("VBFtoH400toZZto2L2Nu");

//   samples.push_back("DoubleElectronMay10ReReco");
//   samples.push_back("DoubleElectronPromptReco");
//   samples.push_back("MuEGMay10ReReco");
//   samples.push_back("MuEGPromptReco");







  // define the groups of samples

  SampleGroup zjets("zjets","Z/#gamma^{*}+jets#rightarrow ll","$Z\\rightarrow ll$", false,false,831);
  zjets.addSample("DYJetsToLL_PU2010");
  zjets.addSample("DYToMuMu_M-20_Spring11");
  zjets.addSample("DYJetsToLL");

  SampleGroup wjets("wjets","W+jets","$W+jets$",false,false,809);
  wjets.addSample("WJetsToLNu_PU2010");
  wjets.addSample("WJetsToLNu");

  SampleGroup ttbar("ttbar","t#bar t","$t\\bar{t}$",false,false,8); 
  ttbar.addSample("TTJets_madgraph_FlatPU");
  ttbar.addSample("TTJets_madgraph_Spring11");
  ttbar.addSample("TTJets");

  SampleGroup singlet("singlet","single-t","single$-t$", false,false,kSpring+4);
  singlet.addSample("TToBLNu_tW-channel_FlatPU");
  singlet.addSample("TToBLNu_t-channel_FlatPU");
  singlet.addSample("TToBLNu_s-channel_FlatPU");
  singlet.addSample("TToBLNu_s-channel_Spring11");
  singlet.addSample("TToBLNu_t-channel_Spring11");
  singlet.addSample("TToBLNu_tW-channel_Spring11");
  singlet.addSample("SingleT_tW");
  singlet.addSample("SingleTbar_tW");
  singlet.addSample("SingleTbar_tW");
  singlet.addSample("SingleTbar_t");
  singlet.addSample("SingleT_tW");
  singlet.addSample("SingleT_t");

  SampleGroup wz("wz","WZ","$WZ$",false,false,596);
  wz.addSample("WZtoAnything_FlatPU");
  wz.addSample("WZtoAnything_Spring11");
  wz.addSample("WZTo3LNu");
  wz.addSample("WZ");

  SampleGroup ww("ww","WW","$WW$",false,false,592);
  ww.addSample("WWtoAnything_PU2010");
  ww.addSample("WWtoAnything_Spring11");
  ww.addSample("WWTo2L2Nu");
  ww.addSample("WW");

  SampleGroup zz("zz","ZZ","$ZZ$",false,false,590);
  zz.addSample("ZZtoAnything_FlatPU");
  zz.addSample("ZZtoAnything_Spring11");
  zz.addSample("ZZto2l2Nu");
  zz.addSample("ZZ");


  SampleGroup h200("h200","H (200GeV)","H (200GeV)",false,true,kGray,0, true);
  h200.addSample("H200");
  h200.addSample("GluGluToHToZZTo2L2Nu_M-200_Spring11");
  h200.addSample("GluGluToHToWWTo2L2Nu_M-200_Spring11");
  h200.addSample("GGtoH200toWWto2L2Nu");
  h200.addSample("GGtoH200toZZto2L2Nu");
  h200.addSample("VBFtoH200toZZto2L2Nu");

// 	"tag":"q#bar{q}#rightarrow H(200)#rightarrow ZZ",
//         "isdata":false,
// 	"spimpose":true,
// 	"color":"kOrange",
// 	"lwidth":2,
// 	"line":2,
// 	"fill":0,
// 	"marker":1,
// 	"data":[
// 	     {	
// 		"dtag":"VBFtoH200toZZto2L2Nu",


  SampleGroup h300("h300","H (300GeV)","H (300GeV)",false,true,50,0, true);
  h300.addSample("GGtoH300toZZto2L2Nu");
  h300.addSample("VBFtoH300toZZto2L2Nu");
  h200.addSample("GGtoH300toWWto2L2Nu");



  SampleGroup h400("h400","H (400GeV)","H (400GeV)",false,true,kRed,0, true);
  h400.addSample("H400");
  h400.addSample("GluGluToHToZZTo2L2Nu_M-400_Spring11");
  h400.addSample("GluGluToHToWWTo2L2Nu_M-400_Spring11");

  SampleGroup h500("h500","H (500GeV)","H (500GeV)",false,true,kRed,0, true);
  h500.addSample("H500");
  h500.addSample("GluGluToHToZZTo2L2Nu_M-500_Spring11");
  h500.addSample("GluGluToHToWWTo2L2Nu_M-500_Spring11");
  h500.addSample("GGtoH500toZZto2L2Nu");
  h500.addSample("VBFtoH500toZZto2L2Nu");
  h200.addSample("GGtoH500toWWto2L2Nu");
  

  SampleGroup data("data","data","data",true,false,1,0);
  data.addSample("MuRun2010A");
  data.addSample("MuRun2010B");
  data.addSample("DoubleMuon-v3");
  data.addSample("DoubleMuon-v5");
  data.addSample("DoubleMuon-v6");
  data.addSample("DoubleMuon-v7");
  data.addSample("DoubleMuon-v8");
  data.addSample("DoubleMuon-v9");
  data.addSample("DoubleMuMay10ReReco");
  data.addSample("DoubleMuPromptReco");
  data.addSample("DoubleMu05AugReReco");
  data.addSample("DoubleMuMay10ReReco");
  data.addSample("DoubleMuPromptRecov4");
  data.addSample("DoubleMuPromptRecov6_172620_173244");



  // Get the normalization from MC xsection and overall normalization to the Z peak
  LumiNormalization lumiNorm(XSectionFile, lumiFile,
			     epoch, finalState, dqApplied,"");
  lumiNorm.addDataGroup(data);
  lumiNorm.normalizeToZPeak(false);

  HistoStack *stacker = new HistoStack(&lumiNorm, finalState, inputDir+"/"+selection, "");

  stacker->addGroup(zjets);
  stacker->addGroup(wjets);
  stacker->addGroup(ttbar);
  stacker->addGroup(singlet);
  stacker->addGroup(wz);
  stacker->addGroup(ww);
  stacker->addGroup(zz);
  stacker->addGroup(h200);
  stacker->addGroup(h300);
  stacker->addGroup(h400);
  stacker->addGroup(h500);
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
  stacker->setLegendOrder(9,"h300");
  stacker->setLegendOrder(10,"h500");

//   stacker->setFillColor("signal",626);
//   stacker->setFillColor("ww_wz",594);
//   stacker->setFillColor("z_ll",kAzure-2);
//   stacker->setFillColor("others",922);
  style->SetMarkerSize(0.8);



  
  //  stacker->setAxisTitles("leadLeptPt","p_{T} [GeV]","GeV");
  TLine *lineStd = new TLine(0,0, -75,150);
  lineStd->SetLineColor(2);
  lineStd->SetLineStyle(2);
  lineStd->SetLineWidth(4);
  //{UNKNOWN=0,MUMU=1,EE=2,EMU=3};
  TString category = "category == 1";

  stacker->addCut("ll", category);
  stacker->addCut("zll", category + " && zmass > 76 && zmass < 106");
  stacker->addCut("zll_lveto", category + " && zmass > 76 && zmass < 106 && pass > 1000");
  stacker->addCut("zll_lveto_bveto", category + " && zmass > 76 && zmass < 106 && pass > 3000");
  



//   stacker->addCut("mumu_lveto","category == 1 && hasTrigger == 1 && pass >= 2");
//   stacker->addCut("mumu_lveto_nob","category == 1 && hasTrigger == 1 && pass >= 3");
//   stacker->addCut("mumu_lveto_nob_redmetL","category == 1 && hasTrigger == 1 && pass >= 3 && redmet > 39");
//   stacker->addCut("mumu_lveto_nob_redmetT","category == 1 && hasTrigger == 1 && pass >= 3 && redmet > 57");


//   stacker->addCut("mumu_j0","category == 1 && nJets15 == 0");
//   stacker->addCut("mumu_j1","category == 1 && nJets15 == 1");

//   stacker->addCut("mumu_ja0","category == 1 && nJets30 == 0");
//   stacker->addCut("mumu_j0_redmet","category == 1 && nJets15 == 0 && redmet > 39");
//   stacker->addCut("mumu_redmet","category == 1  && redmet > 39");

  stacker->setAxisTitles("zmass_zll", "M(ll) (GeV)","GeV");
  stacker->setAxisTitles("zmass_zll_lveto", "M(ll) (GeV)","GeV");
  stacker->setAxisTitles("zmass_zll_lveto_bveto", "M(ll) (GeV)","GeV");

  stacker->setAxisTitles("redmet_zll", "red-E^{miss}_{T} (GeV)","GeV");
  stacker->setAxisTitles("redmet_zll_lveto", "red-E^{miss}_{T} (GeV)","GeV");
  stacker->setAxisTitles("redmet_zll_lveto_bveto", "red-E^{miss}_{T} (GeV)","GeV");



  stacker->setAxisTitles("zpt_mumu_lveto_nob", "p_{T}(Z)","GeV");
  stacker->setAxisTitles("mtSumLMet_mumu_lveto_nob","#SigmaM_{T}(l-#slash{E}_{T})","GeV");
  stacker->setAxisTitles("deltaRLept_mumu_lveto_nob","#Delta R(l_{1},l_{2})","");
  stacker->setAxisTitles("deltaPhiLeadZ_mumu_lveto_nob","#Delta#phi(#it{lead}-l,Z)","rad");

  stacker->setAxisTitles("zpt_mumu_lveto_nob_redmetL", "p_{T}(Z)","GeV");
  stacker->setAxisTitles("mtSumLMet_mumu_lveto_nob_redmetL","#SigmaM_{T}(l-#slash{E}_{T})","GeV");
  stacker->setAxisTitles("deltaRLept_mumu_lveto_nob_redmetL","#Delta R(l_{1},l_{2})","");
  stacker->setAxisTitles("deltaPhiLeadZ_mumu_lveto_nob_redmetL","#Delta#phi(#it{lead}-l,Z)","rad");

  stacker->setAxisTitles("zpt_mumu_lveto_nob_redmetT", "p_{T}(Z)","GeV");
  stacker->setAxisTitles("mtSumLMet_mumu_lveto_nob_redmetT","#SigmaM_{T}(l-#slash{E}_{T})","GeV");
  stacker->setAxisTitles("deltaRLept_mumu_lveto_nob_redmetT","#Delta R(l_{1},l_{2})","");
  stacker->setAxisTitles("deltaPhiLeadZ_mumu_lveto_nob_redmetT","#Delta#phi(#it{lead}-l,Z)","rad");



  // Loop over all the samples
  for(vector<TString>::const_iterator sName = samples.begin(); sName != samples.end();
      sName++) {


    stacker->add(*sName, "category", "", 4, 0, 4);

    stacker->add(*sName, "zmass", "ll",             100, 30, 200);
    stacker->add(*sName, "zmass", "zll",            100, 76, 106);
    stacker->add(*sName, "zmass", "zll_lveto",      100, 76, 106);
    stacker->add(*sName, "zmass", "zll_lveto_bveto",100, 76, 106);

    stacker->add(*sName, "redmet", "zll",            100, 0, 500);
    stacker->add(*sName, "redmet", "zll_lveto",      100, 0, 500);
    stacker->add(*sName, "redmet", "zll_lveto_bveto",100, 0, 500);

    

    continue;
    
    // MVA input variables
    
    stacker->add(*sName, "mtSumLMet", "mumu_lveto_nob",100, 0, 1000);
    stacker->add(*sName, "deltaPhiLeadZ", "mumu_lveto_nob",15, 0, 1.5);
    stacker->add(*sName, "deltaRLept", "mumu_lveto_nob",50, 0, 6);

    stacker->add(*sName, "mtSumLMet", "mumu_lveto_nob_redmetL",100, 0, 1000);
    stacker->add(*sName, "deltaPhiLeadZ", "mumu_lveto_nob_redmetL",15, 0, 1.5);
    stacker->add(*sName, "deltaRLept", "mumu_lveto_nob_redmetL",50, 0, 6);

    stacker->add(*sName, "mtSumLMet", "mumu_lveto_nob_redmetT",100, 0, 1000);
    stacker->add(*sName, "deltaPhiLeadZ", "mumu_lveto_nob_redmetT",15, 0, 1.5);
    stacker->add(*sName, "deltaRLept", "mumu_lveto_nob_redmetT",50, 0, 6);




    /*
//     stacker->add(*sName, "met", "mumu",100, 0, 500);
    stacker->add(*sName, "redmet", "mumu",100, 0, 500);
    stacker->add(*sName, "redmet", "mumu_j0",100, 0, 500);


    stacker->add(*sName, "zpt", "mumu",100, 0, 1000);
    stacker->add(*sName, "zpt", "mumu_j0",100, 0, 1000);
    stacker->add(*sName, "zpt", "mumu_j0_redmet",100, 0, 1000);



    //    stacker->add(*sName, "met", "mumu_j0",100, 0, 500);

//     stacker->add(*sName, "redmet", "mumu_j1",100, 0, 500);
*/
    /*    stacker->add(*sName, "zmass", "mumu",100, 60, 120);

    stacker->add(*sName, "zmass", "mumu",100, 60, 120);
    stacker->add(*sName, "zmass", "mumu_trig",100, 60, 120);
    stacker->add(*sName, "zmass", "mumu_lveto",100, 60, 120);
    stacker->add(*sName, "zmass", "mumu_lveto_nob",100, 60, 120);
    */

    stacker->add(*sName, "zmass", "mumu_lveto_nob_redmetT",100, 60, 120);
    /*


    stacker->add(*sName, "zmass", "mumu_j0",100, 60, 120);
    stacker->add(*sName, "zmass", "mumu_redmet",100, 60, 120);



    
    stacker->add(*sName, "mtSumLMet", "mumu",100, 0, 1000);
    stacker->add(*sName, "mtSumLMet", "mumu_j0",100, 0, 1000);
    stacker->add(*sName, "mtSumLMet", "mumu_redmet",100, 0, 1000);

    stacker->add(*sName, "deltaPhiLeadZ", "mumu",15, 0, 1.5);
    stacker->add(*sName, "deltaPhiLeadZ", "mumu_j0",15, 0, 1.5);
    stacker->add(*sName, "deltaPhiLeadZ", "mumu_redmet",15, 0, 1.5);



//     stacker->add(*sName, "deltaPhiZMet", "mumu",50, -3.14, 3.14);
//     stacker->add(*sName, "deltaPhiZMet", "mumu_redmet",50, -3.14, 3.14);

//     stacker->add(*sName, "leadLeptCosThetaStar", "mumu",50, -1, 1);
//     stacker->add(*sName, "leadLeptCosThetaStar", "mumu_redmet",50, -1, 1);

    stacker->add(*sName, "deltaRLept", "mumu",50, 0, 6);
    stacker->add(*sName, "deltaRLept", "mumu_redmet",50, 0, 6);
    */
//     stacker->add(*sName, "zpt/met", "mumu",50, 0, 10);
//     stacker->add(*sName, "zpt/met", "mumu_redmet",50, 0, 10);

//     stacker->add(*sName, "subleadLeptPt", "mumu",50, 0, 300);
//     stacker->add(*sName, "subleadLeptPt", "mumu_redmet",50, 0, 300);

//     stacker->add(*sName, "leadLeptPt+subleadLeptPt", "mumu",50, 0, 300);
//     stacker->add(*sName, "leadLeptPt+subleadLeptPt", "mumu_redmet",50, 0, 300);

//     stacker->add(*sName, "leadLeptCosThetaStar", "mumu",100, -1, 1);
//     stacker->add(*sName, "leadLeptCosThetaStar", "mumu_redmet",100, -1, 1);

//     stacker->add(*sName, "mtSumLMet", "mumu",100, 0, 1000);
//     stacker->add(*sName, "deltaPhiZMet", "mumu",100, -3.6, 3.6);
//     stacker->add(*sName, "leadLeptCosThetaStar", "mumu",100, -1, 1);
//     stacker->add(*sName, "subleadLeptCosThetaStar", "mumu",100, -1, 1);
//     stacker->add(*sName, "leadLeptDeltaPhiStar", "mumu",100, -3.6, 3.6);
//     stacker->add(*sName, "subleadLeptDeltaPhiStar", "mumu",100, -3.6, 3.6);
//     stacker->add(*sName, "deltaPhiLeadZ", "mumu",100, -3.6, 3.6);
//     stacker->add(*sName, "deltaPhiNoLeadZ", "mumu",100, -3.6, 3.6);
//     stacker->add(*sName, "deltaPhiLeadMET", "mumu",100, -3.6, 3.6);
//     stacker->add(*sName, "deltaPhiNoLeadMET", "mumu",100, -3.6, 3.6);

//     stacker->add(*sName, "mInvTot", "mumu",100, 0, 1000);
//     stacker->add(*sName, "mTransMETZ", "mumu",100, 0, 1000);
//     stacker->add(*sName, "minMInvTot", "mumu",100, 0, 1000);

//     stacker->add(*sName, "nJets15", "mumu",50, 0, 50);
//     stacker->add(*sName, "nJets30", "mumu",50, 0, 50);

//     stacker->add(*sName, "met", "mumu_j0",100, 0, 500);
//     stacker->add(*sName, "mtSumLMet", "mumu_j0",100, 0, 1000);
//     stacker->add(*sName, "mtSumLMet", "mumu_j0_redmet",100, 0, 1000);

//     stacker->add(*sName, "zpt", "mumu_j0_redmet",100, 0, 1000);
//     stacker->add(*sName, "mtSumLMet", "mumu_redmet",100, 0, 1000);

//     stacker->add(*sName, "zpt", "mumu_redmet",100, 0, 1000);
//     stacker->add(*sName, "subleadLeptPt", "mumu_redmet",100, 0, 500);
//     stacker->add(*sName, "leadLeptPt", "mumu_redmet",100, 0, 500);
  }
    
  //  stacker->drawAll("pre,d0lumi,dimu");



  // ==============================================================================
  // define signal and backgorund samples to be used for the MVA

  SampleGroup bckgSamples("background","background","background",false,false,kRed);
  //     // Spring11
  //     bckgSamples.addSample("WZtoAnything_Spring11");
  //     bckgSamples.addSample("WWtoAnything_Spring11");
  //     bckgSamples.addSample("ZZtoAnything_Spring11");
  //     // Summer11
  bckgSamples.addSample("WWTo2L2Nu");
  bckgSamples.addSample("WZTo3LNu");
  bckgSamples.addSample("ZZto2l2Nu");

    
  SampleGroup sigSamples("signal","signal","signal",false,false,kGreen);
  //     // Spring11
  //     sigSamples.addSample("GluGluToHToZZTo2L2Nu_M-400_Spring11");
  //     sigSamples.addSample("GluGluToHToWWTo2L2Nu_M-400_Spring11");
  //     //     sigSamples.addSample("GluGluToHToZZTo2L2Nu_M-200_Spring11");
  //     //     sigSamples.addSample("GluGluToHToWWTo2L2Nu_M-200_Spring11");
  //     // Summer11
  // M200
//   sigSamples.addSample("GGtoH200toWWto2L2Nu");
//   sigSamples.addSample("GGtoH200toZZto2L2Nu");
  // M300
  sigSamples.addSample("GGtoH300toZZto2L2Nu");



  if(doTMVA) {
    
    if(doTraining) {

      TFile *tmvaOutput = TFile::Open("TMVA.root","recreate");
      Factory *factory = new Factory("MVAnalysis",tmvaOutput,"");

      // set the input trees for signal
      vector<TString> sigSampleNames = sigSamples.samples();
      for(vector<TString>::const_iterator sampleName = sigSampleNames.begin();
	  sampleName != sigSampleNames.end(); sampleName++) { // loop over all signal samples

	// get the scale factor
	float scaleFactor = lumiNorm.getScaleFactor(*sampleName); // FIXME: check when applying further selections
	// get the tree
	TString fileName = inputDir+ selection +"/"+ *sampleName +".root";
	TFile *file = new TFile(fileName.Data());
	TTree *tree = (TTree*)file->Get("DiLeptNtuple");
	factory->AddSignalTree(tree, scaleFactor);
      
      }

      // set the input trees for background
      vector<TString> bckgSampleNames = bckgSamples.samples();
      for(vector<TString>::const_iterator sampleName = bckgSampleNames.begin();
	  sampleName != bckgSampleNames.end(); sampleName++) { // loop over all bckg samples

	// get the scale factor
	float scaleFactor = lumiNorm.getScaleFactor(*sampleName); // FIXME: check when applying further selections
	// get the tree
	TString fileName = inputDir+ selection +"/"+ *sampleName +".root";
	TFile *file = new TFile(fileName.Data());
	TTree *tree = (TTree*)file->Get("DiLeptNtuple");
	factory->AddBackgroundTree(tree, scaleFactor);
      
      }
      factory->AddVariable("zpt", "p_{T}(Z)","GeV",'F');
      factory->AddVariable("deltaRLept", "#Delta R(l_{1},l_{2})","",'F');
      factory->AddVariable("mtSumLMet", "#SigmaM_{T}(l-#slash{E}_{T})","GeV",'F');
      factory->AddVariable("deltaPhiLeadZ", "#Delta#phi(#it{lead}-l,Z)","rad",'F');

      //     factory->AddSpectator("zmass");
      factory->AddSpectator("nJets15");
    
      // set the  wwight expression
      factory->SetWeightExpression("weight"); // FIXME: use weight 1 samples?

      TCut baseSelection(cutForTraining.Data());
    
      factory->PrepareTrainingAndTestTree(baseSelection, "SplitMode=Random");

      if(doCategories) {

	MethodCategory* category = (MethodCategory*) factory->BookMethod(TMVA::Types::kCategory, "jBins", "");
	category->AddMethod("nJets15 == 0", "zpt:deltaRLept:mtSumLMet:deltaPhiLeadZ:",
			    TMVA::Types::kLikelihood, "Likelihood_j0", "H:V:Nbins=25:NbinsSig[3]=15");
	category->AddMethod("nJets15 == 1", "zpt:deltaRLept:mtSumLMet:deltaPhiLeadZ:",
			    TMVA::Types::kLikelihood, "Likelihood_j1", "H:V:Nbins=30");
	category->AddMethod("nJets15 >= 2", "zpt:deltaRLept:mtSumLMet:deltaPhiLeadZ:",
			    TMVA::Types::kLikelihood, "Likelihood_j2", "H:V:Nbins=30:NbinsSig[3]=15");
      
	MethodCategory* category2 = (MethodCategory*) factory->BookMethod(TMVA::Types::kCategory, "jBins2", "");
	category2->AddMethod("nJets15 == 0", "deltaRLept:mtSumLMet:deltaPhiLeadZ:",
			     TMVA::Types::kLikelihood, "Likelihood2_j0", "H:V:Nbins=25:NbinsSig[2]=15");
	category2->AddMethod("nJets15 == 1", "deltaRLept:mtSumLMet:deltaPhiLeadZ:",
			     TMVA::Types::kLikelihood, "Likelihood2_j1", "H:V:Nbins=30");
	category2->AddMethod("nJets15 >= 2", "deltaRLept:mtSumLMet:deltaPhiLeadZ:",
			     TMVA::Types::kLikelihood, "Likelihood2_j2", "H:V:Nbins=30:NbinsSig[2]=15");


      } else {
	factory->BookMethod(TMVA::Types::kLikelihood,"TMVALikelihood_1",
			    "H:V:Nbins=30:NbinsSig[3]=15");

	factory->BookMethod(TMVA::Types::kLikelihood,"TMVALikelihood_2",
			    "H:V:Nbins=30");

	//       factory->BookMethod(TMVA::Types::kLikelihood,"TMVALikelihood_3",
	// 			  "H:V:TransformOutput=True");
      }

      //     factory->BookMethod(TMVA::Types::kLikelihood,"TMVALikelihood_1",
      // 			  "H:V:Nbins=30:NbinsSig[3]=15:TransformOutput=True");

    
      factory->TrainAllMethods();
      factory->TestAllMethods();
      factory->EvaluateAllMethods();

      tmvaOutput->Close();
    }
    
    if(doEvaluate) {

      
      stacker->setAxisTitles("TMVALikelihood","LL output","");
      stacker->setYRange("TMVALikelihood",0.01, 20);
      stacker->setAxisTitles("TMVALikelihood_j0","LL output","");
      stacker->setYRange("TMVALikelihood_j0",0.005, 7);
      stacker->setAxisTitles("TMVALikelihood_j1","LL output","");
      stacker->setYRange("TMVALikelihood_j1",0.01, 20);
      stacker->setAxisTitles("TMVALikelihood_j2","LL output","");
      stacker->setYRange("TMVALikelihood_j2",0.01, 20);

      // ==========================================================
      // use the discriminant that was just created
      Reader* reader = new Reader("V");
      float zpt = -1;
      float deltaRLept = -1;
      float mtSumLMet = -1;
      float deltaPhiLeadZ = -1;
      float nJets15 = -1;
      float weight = -1;

      reader->AddVariable("zpt", &zpt);
      reader->AddVariable("deltaRLept", &deltaRLept);
      reader->AddVariable("mtSumLMet", &mtSumLMet);
      reader->AddVariable("deltaPhiLeadZ", &deltaPhiLeadZ);
    
      reader->AddSpectator("nJets15", &nJets15);
    
      reader->BookMVA("MVA","weights/MVAnalysis_jBins2.weights.xml");
    
      // Loop over all the samples
      for(vector<TString>::const_iterator sName = samples.begin(); sName != samples.end();
	  sName++) {
	float scaleFactor = lumiNorm.getScaleFactor(*sName);
	cout << "--- sample name: " << *sName << " scale factor: " << scaleFactor << endl;    
	//if(*sName == "H200" || *sName == "H400") scaleFactor = scaleFactor*10.; // FIXME      

	TString hName = "hDisc_" +  *sName;
	TH1F* hDisc = new TH1F(hName.Data(),"TMVA disc",30,0,1);
	hDisc->Sumw2();

	TString hNameJ0 = "hDisc_" +  *sName + "_j0";
	TH1F* hDiscJ0 = new TH1F(hNameJ0.Data(),"TMVA disc (0 jets)",15,0,1);
	hDiscJ0->Sumw2();
	
	TString hNameJ1 = "hDisc_" +  *sName + "_j1";
	TH1F* hDiscJ1 = new TH1F(hNameJ1.Data(),"TMVA disc (1 jets)",15,0,1);
	hDiscJ1->Sumw2();

	TString hNameJ2 = "hDisc_" +  *sName + "_j2";
	TH1F* hDiscJ2 = new TH1F(hNameJ2.Data(),"TMVA disc (2 jets)",15,0,1);
	hDiscJ2->Sumw2();
      
      
	TString fileName = TString(inputDir) + TString(selection) +"/" + *sName +".root";
	TFile *file = new TFile(fileName.Data());
	TTree *tree = (TTree*) file->Get("DiLeptNtuple");

	//       TString nameNew = "/tmp/cerminar/" + *sName +".root";
	//       TFile dump(nameNew.Data(),"recreate");
	TTree *selTree = tree->CopyTree(cutForEvaluation.Data());
      
	cout << "# entries: " << tree->GetEntries() << endl;
	cout << "# seleceted entries: " << selTree->GetEntries() << endl;

	selTree->SetBranchAddress("zpt", &zpt);
	selTree->SetBranchAddress("deltaRLept", &deltaRLept);
	selTree->SetBranchAddress("mtSumLMet", &mtSumLMet);
	selTree->SetBranchAddress("deltaPhiLeadZ", &deltaPhiLeadZ);
	selTree->SetBranchAddress("nJets15", &nJets15);
	selTree->SetBranchAddress("weight", &weight);

	// loop over all entries
	for(int entry  = 0; entry != selTree->GetEntries(); ++entry) {
	  selTree->GetEntry(entry);
	  float disc = reader->EvaluateMVA("MVA");
	  hDisc->Fill(disc, weight);

	  if(nJets15 == 0) {
	    hDiscJ0->Fill(disc, weight);
	  } else if(nJets15 == 1) {
	    hDiscJ1->Fill(disc, weight);
	  } else if(nJets15 >= 2) {
	    hDiscJ2->Fill(disc, weight);
	  }

	}
	tree->ResetBranchAddresses();
	file->Close();
	hDisc->Scale(scaleFactor);
	stacker->add(*sName, "TMVALikelihood", hDisc);
	hDiscJ0->Scale(scaleFactor);
	stacker->add(*sName, "TMVALikelihood_j0", hDiscJ0);
	hDiscJ1->Scale(scaleFactor);
	stacker->add(*sName, "TMVALikelihood_j1", hDiscJ1);
	hDiscJ2->Scale(scaleFactor);
	stacker->add(*sName, "TMVALikelihood_j2", hDiscJ2);
	

	//       dump.Close();

      }
    }
  }


  if(doLikelihood) {

    // deltaRLept
    // mtSumLMet
    // deltaPhiLZ
    // deltaPhiLeadZ



    LikelihoodDisc likelihoodDisk(&lumiNorm, sigSamples, bckgSamples);
    likelihoodDisk.separateSamples(false);
    likelihoodDisk.setSelectionCuts("category == 1 && redmet > 60 && nJets15 >= 2");
    //    likelihoodDisk.setSelectionCuts("category == 1 && redmet > 43");

    TCanvas * ctemp = newCanvas("Temporary Canvas for fits",2); 
    ctemp->cd();

    double binsForZpt[11] = {40,50,60,70,80,90,100,115,145,200,500};
    likelihoodDisk.addVariable("L0", "zpt", "Pt_{ll} (GeV)", 10, 40,540,binsForZpt, "gaus");

    double binsFormtSumLMet[12] = {0,50,75,100,125,150,175,200,225,250,500,1000};
    likelihoodDisk.addVariable("L1", "mtSumLMet", "#Sum(M_T(#ell-MET))) (GeV)", 11, 0, 1000, binsFormtSumLMet,"pol2");


    likelihoodDisk.addVariable("L4", "deltaPhiLeadZ", "#Sum(M_T(#ell-MET))) (GeV)", 15, 0, 1.5, "pol5");

    likelihoodDisk.addVariable("L9", "deltaRLept", "#Sum(M_T(#ell-MET))) (GeV)", 30, 1, 3.5, "pol8");


    pair<TH1D *, TH1D *> pdfL0 = likelihoodDisk.getPdf("L0");
    plot1DHistos(pdfL0.first,pdfL0.second,1,true,false);
    pair<TH1D *, TF1 *> lrL0 = likelihoodDisk.getLR("L0");
    newCanvas(lrL0.first->GetName(),1);
    lrL0.first->Draw();


    pair<TH1D *, TH1D *> pdfL1 = likelihoodDisk.getPdf("L1");
    plot1DHistos(pdfL1.first,pdfL1.second,1,true,false);
    pair<TH1D *, TF1 *> lrL1 = likelihoodDisk.getLR("L1");
    newCanvas(lrL1.first->GetName(),1);
    lrL1.first->Draw();

    pair<TH1D *, TH1D *> pdfL4 = likelihoodDisk.getPdf("L4");
    plot1DHistos(pdfL4.first,pdfL4.second,1,false,false);
    pair<TH1D *, TF1 *> lrL4 = likelihoodDisk.getLR("L4");
    newCanvas(lrL4.first->GetName(),1);
    lrL4.first->Draw();


    pair<TH1D *, TH1D *> pdfL9 = likelihoodDisk.getPdf("L9");
    plot1DHistos(pdfL9.first,pdfL9.second,1,false,false);
    pair<TH1D *, TF1 *> lrL9 = likelihoodDisk.getLR("L9");
    newCanvas(lrL9.first->GetName(),1);
    lrL9.first->Draw();



//     likelihoodDisk.addVariable("L2", "deltaPhiZMet", "#Sum(M_T(#ell-MET))) (GeV)", 25, -3.14, 3.14, "pol4");
//     pair<TH1D *, TH1D *> pdfL2 = likelihoodDisk.getPdf("L2");
//     plot1DHistos(pdfL2.first,pdfL2.second,1,false,false);
//     pair<TH1D *, TF1 *> lrL2 = likelihoodDisk.getLR("L2");
//     newCanvas(lrL2.first->GetName(),1);
//     lrL2.first->Draw();


//     likelihoodDisk.addVariable("L3", "leadLeptCosThetaStar", "#Sum(M_T(#ell-MET))) (GeV)", 25, -1, 1, "pol4");
//     pair<TH1D *, TH1D *> pdfL3 = likelihoodDisk.getPdf("L3");
//     plot1DHistos(pdfL3.first,pdfL3.second,1,false,false);
//     pair<TH1D *, TF1 *> lrL3 = likelihoodDisk.getLR("L3");
//     newCanvas(lrL3.first->GetName(),1);
//     lrL3.first->Draw();

//     likelihoodDisk.addVariable("L4", "deltaPhiLeadZ", "#Sum(M_T(#ell-MET))) (GeV)", 25, -3.14, 3.14, "pol4");
//     pair<TH1D *, TH1D *> pdfL4 = likelihoodDisk.getPdf("L4");
//     plot1DHistos(pdfL4.first,pdfL4.second,1,false,false);
//     pair<TH1D *, TF1 *> lrL4 = likelihoodDisk.getLR("L4");
//     newCanvas(lrL4.first->GetName(),1);
//     lrL4.first->Draw();

//     likelihoodDisk.addVariable("L5", "deltaPhiLeadMET", "#Sum(M_T(#ell-MET))) (GeV)", 25, -3.14, 3.14, "pol4");
//     pair<TH1D *, TH1D *> pdfL5 = likelihoodDisk.getPdf("L5");
//     plot1DHistos(pdfL5.first,pdfL5.second,1,false,false);
//     pair<TH1D *, TF1 *> lrL5 = likelihoodDisk.getLR("L5");
//     newCanvas(lrL5.first->GetName(),1);
//     lrL5.first->Draw();

//     likelihoodDisk.addVariable("L6", "mInvTot", "#Sum(M_T(#ell-MET))) (GeV)", 50, 0, 1000, "pol4");
//     pair<TH1D *, TH1D *> pdfL6 = likelihoodDisk.getPdf("L6");
//     plot1DHistos(pdfL6.first,pdfL6.second,1,false,false);
//     pair<TH1D *, TF1 *> lrL6 = likelihoodDisk.getLR("L6");
//     newCanvas(lrL6.first->GetName(),1);
//     lrL6.first->Draw();

//     likelihoodDisk.addVariable("L7", "mTransMETZ", "#Sum(M_T(#ell-MET))) (GeV)", 50, 0, 1000, "pol4");
//     pair<TH1D *, TH1D *> pdfL7 = likelihoodDisk.getPdf("L7");
//     plot1DHistos(pdfL7.first,pdfL7.second,1,false,false);
//     pair<TH1D *, TF1 *> lrL7 = likelihoodDisk.getLR("L7");
//     newCanvas(lrL7.first->GetName(),1);
//     lrL7.first->Draw();

//     likelihoodDisk.addVariable("L8", "minMInvTot", "#Sum(M_T(#ell-MET))) (GeV)", 50, 0, 1000, "pol4");
//     pair<TH1D *, TH1D *> pdfL8 = likelihoodDisk.getPdf("L8");
//     plot1DHistos(pdfL8.first,pdfL8.second,1,false,false);
//     pair<TH1D *, TF1 *> lrL8 = likelihoodDisk.getLR("L8");
//     newCanvas(lrL8.first->GetName(),1);
//     lrL8.first->Draw();

//     likelihoodDisk.addVariable("L9", "deltaRLept", "#Sum(M_T(#ell-MET))) (GeV)", 50, 0, 6, "pol4");
//     pair<TH1D *, TH1D *> pdfL9 = likelihoodDisk.getPdf("L9");
//     plot1DHistos(pdfL9.first,pdfL9.second,1,false,false);
//     pair<TH1D *, TF1 *> lrL9 = likelihoodDisk.getLR("L9");
//     newCanvas(lrL9.first->GetName(),1);
//     lrL9.first->Draw();

//     likelihoodDisk.addVariable("L10", "zpt/met", "#Sum(M_T(#ell-MET))) (GeV)", 50, 0, 10, "pol4");
//     pair<TH1D *, TH1D *> pdfL10 = likelihoodDisk.getPdf("L10");
//     plot1DHistos(pdfL10.first,pdfL10.second,1,false,false);
//     pair<TH1D *, TF1 *> lrL10 = likelihoodDisk.getLR("L10");
//     newCanvas(lrL10.first->GetName(),1);
//     lrL10.first->Draw();



    // evaluate the performace on all samples
    vector<TString> likelihoodComposition;
    likelihoodComposition.push_back("L0");
    likelihoodComposition.push_back("L1");
    likelihoodComposition.push_back("L4");
    likelihoodComposition.push_back("L9");

    likelihoodDisk.setSelectionCuts("category == 1 && redmet > 60");
    // Loop over all the samples
    for(vector<TString>::const_iterator sName = samples.begin(); sName != samples.end();
	sName++) {

      TString fileName = inputDir+ selection +"/"+ *sName +".root";
      TFile *file = new TFile(fileName.Data());
      TTree *tree = (TTree*)file->Get("DiLeptNtuple");
      
      TH1F *lHisto = likelihoodDisk.evaluate(likelihoodComposition, tree, *sName,10);
      stacker->add(*sName, "likelihood", lHisto);
      //file->Close();
    }



    likelihoodDisk.setSelectionCuts("category == 1 && redmet > 60 && nJets15 == 0");
    // Loop over all the samples
    for(vector<TString>::const_iterator sName = samples.begin(); sName != samples.end();
	sName++) {

      TString fileName = inputDir+ selection +"/"+ *sName +".root";
      TFile *file = new TFile(fileName.Data());
      TTree *tree = (TTree*)file->Get("DiLeptNtuple");
      
      TH1F *lHisto = likelihoodDisk.evaluate(likelihoodComposition, tree, *sName,10);
      stacker->add(*sName, "likelihood_j0", lHisto);


      //file->Close();
    }

    likelihoodDisk.setSelectionCuts("category == 1 && redmet > 60 && nJets15 == 1");
    // Loop over all the samples
    for(vector<TString>::const_iterator sName = samples.begin(); sName != samples.end();
	sName++) {

      TString fileName = inputDir+ selection +"/"+ *sName +".root";
      TFile *file = new TFile(fileName.Data());
      TTree *tree = (TTree*)file->Get("DiLeptNtuple");
      
      TH1F *lHisto = likelihoodDisk.evaluate(likelihoodComposition, tree, *sName,10);
      stacker->add(*sName, "likelihood_j1", lHisto);


      //file->Close();
    }

    likelihoodDisk.setSelectionCuts("category == 1 && redmet > 60 && nJets15 >= 2");
    // Loop over all the samples
    for(vector<TString>::const_iterator sName = samples.begin(); sName != samples.end();
	sName++) {

      TString fileName = inputDir+ selection +"/"+ *sName +".root";
      TFile *file = new TFile(fileName.Data());
      TTree *tree = (TTree*)file->Get("DiLeptNtuple");
      
      TH1F *lHisto = likelihoodDisk.evaluate(likelihoodComposition, tree, *sName,10);
      stacker->add(*sName, "likelihood_j2", lHisto);


      //file->Close();
    }


  }



  TString options = "pre,lumi,channel,doRatio";

  if(toUnity) options+= "nostack";
  stacker->drawAll(options);
  //  stacker->draw("NVertex");
  cout << "Normalization factor: " << lumiNorm.getNormalizationFactor() << endl;


}

void plot1DHistos(TH1 *hSign, TH1 *hBck, int rebin, bool flip, bool scale) { 
  if(hBck == 0 || hSign == 0) return; 
 
  // Clone the two histos 
  TH1F *hSignC = (TH1F *)hSign->Clone(); 
  TH1F *hBckC = (TH1F *)hBck->Clone(); 
 
  if(rebin != 1) { 
    hSignC->Rebin(rebin); 
    hBckC->Rebin(rebin); 
  } 
 
  // Normalize them to 1 
  if(scale) { 
    hSignC->Scale(1./hSignC->Integral()); 
    hBckC->Scale(1./hBckC->Integral()); 
  } 
//   cout << "New Signal integral is: " << hSignC->Integral() << endl; 
//   cout << "New Background integral is: " << hBckC->Integral() << endl; 
 
  // Create the new canvas 
  int form = 2; 
  TCanvas * c1 = newCanvas(hSign->GetName(),form); 
  c1->cd(); 
 
  // Set the style 
  setStyle(hBckC); 
  hBckC->SetFillColor(50); 
  hBckC->SetFillStyle(3002); 
  
  setStyle(hSignC); 
  hSignC->SetFillColor(8); 
  hSignC->SetFillStyle(3002); 

  TH1F *hFirst = 0; 
  TH1F *hSecond = 0; 
 
  if(flip == false) {  
    hFirst = hBckC; 
    hSecond = hSignC; 
  } else { 
    hFirst = hSignC; 
    hSecond = hBckC; 
  } 
  //hFirst->GetXaxis()->SetTitle("likelihood output"); 
  hFirst->Draw("hist"); 
  hSecond->Draw("same,hist"); 
   
 
 
  TLegend *leg = getLegend(0.7,0.85); 
  leg->AddEntry(hSignC,"signal","F"); 
  leg->AddEntry(hBckC, "background", "F"); 
  leg->Draw("same"); 
 
  bool plotRatio = true;
  if(plotRatio) { 
    TString ratioName = TString(hSign->GetName())+"_ratio"; 
    newCanvas(ratioName.Data(),form); 
    // Clone the two histos 
    TH1F *hSignC2 = (TH1F *)hSign->Clone(); 
    TH1F *hBckC2 = (TH1F *)hBck->Clone(); 
    hSignC2->Scale(1./hSignC2->Integral()); 
    hBckC2->Scale(1./hBckC2->Integral()); 
    hSignC2->Divide(hBckC2); 
    hSignC2->Draw(); 
 
  } 
 
 
 
} 



// [3] new TCanvas
// (class TCanvas*)0x559d050
// root [4] DiLeptNtuple->Draw("deltaRLept:mtSumLMet","weight*(category == 1 && redmet > 43)","")
// (Long64_t)5264
// root [5] DiLeptNtuple->Draw("deltaPhiLZ:mtSumLMet","weight*(category == 1 && redmet > 43)","")
// Error in <TTreeFormula::Compile>:  Bad numerical expression : "deltaPhiLZ"
// (Long64_t)(-1)
// root [6] DiLeptNtuple->Draw("deltaPhiLeadZ:mtSumLMet","weight*(category == 1 && redmet > 43)","")
// (Long64_t)5264
// root [7] DiLeptNtuple->Draw("deltaPhiLeadZ:deltaRLept","weight*(category == 1 && redmet > 43)","")
// (Long64_t)5264
