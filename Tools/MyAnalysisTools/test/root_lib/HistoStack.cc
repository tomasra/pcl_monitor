/*
 *  See header file for a description of this class.
 *
 *  $Date: 2007/12/04 00:11:38 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - NEU Boston & INFN Torino
 */

#include "HistoStack.h"
#include "LumiNormalization.h"
#include "THStack.h"
#include "TLegend.h"
#include "TFile.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TNtuple.h"
#include "TStyle.h"
#include "TH1.h"
#include "TSQLResult.h"
#include "TSQLRow.h"
#include "TPaveText.h"
#include "TMath.h"
#include "TROOT.h"

#include <iostream>
#include <iomanip>
#include <sstream>

using namespace std;


// Contructor
HistoStack::HistoStack(const LumiNormalization* lumiNorm, const TString& finalState,
		       const TString& inputDir, const TString& filePrefix) : theLumiNorm(lumiNorm),
									     theFinalState(finalState),
									     theInputDir(inputDir),
									     theFilePrefix(filePrefix),
									     massMin(-1),
									     massMax(9999999),
									     theSelection(""),
									     ntupleName("DiLeptNtuple"),
									     weightBr(":weight") {
  // Fill the color map
  colorMap["zz"] = 11;
  colorMap["zz_llll"] = 12;
  colorMap["zz_llvv"] = 11;
  colorMap["wz"] = 10;
  colorMap["ww"] = 9;
  colorMap["tt"] = 6;
  colorMap["ztt_130-250"] = 7;
  colorMap["ztt_60-130"] = 7;
  colorMap["ztt_15-60"] = 7;
  colorMap["z_130-250"] = 3;
  colorMap["z_60-130"] = 3;
  colorMap["z_15-60"] = 3;
  colorMap["wgamma_prod"] = 42;
  colorMap["wgamma_rad"] = 42;
  colorMap["wgamma"] = 42;
  colorMap["wjets"] = 46;
  colorMap["wjets_w0lp"] = 46;
  colorMap["wjets_w1lp"] = 46;
  colorMap["wjets_w2lp"] = 46;
  colorMap["wjets_w3lp"] = 46;
  colorMap["wjets_w4lp"] = 46;
  colorMap["wjets_w5lp"] = 46;
  colorMap["ww_wz"] = 11;
  colorMap["z_ll"] = -1;
  colorMap["signal"] = -1;
  colorMap["others"] = 1;
  colorMap["z_tt"] = 7;
  colorMap["wjets_gp"] = 46;
  colorMap["H400"] = 0;
  colorMap["QCD"] = 400;

  fillStyleMap["z_ll"] = 3004;
  fillStyleMap["others"] = 3005;
  fillStyleMap["signal"] = 0;

  // Fill the color map
  legLabel["zz_llll"] = "ZZ #rightarrow 4l";
  legLabel["zz_llvv"] = "ZZ #rightarrow 2l 2#nu";
  legLabel["wz"] = "WZ";
  legLabel["ww"] = "WW";
  legLabel["zz"] = "ZZ";
  legLabel["ZZ"] = "ZZ";

  legLabel["tt"] = "t#bar t";
  legLabel["ztt_130-250"] = "Z #rightarrow #tau #tau";
  legLabel["ztt_60-130"] = "Z #rightarrow #tau #tau";
  legLabel["ztt_15-60"] = "Z #rightarrow #tau #tau";
  legLabel["z_130-250"] = "Z #rightarrow ll";
  legLabel["z_60-130"] = "Z #rightarrow ll";
  legLabel["z_15-60"] = "Z #rightarrow ll";
  legLabel["wgamma_prod"] = "W+#gamma";
  legLabel["wgamma_rad"] = "W+#gamma";
  legLabel["wgamma"] = "W+#gamma";
  legLabel["wjets"] = "W+jets";
  legLabel["wjets_w0lp"] = "W+jets";
  legLabel["wjets_w1lp"] = "W+jets";
  legLabel["wjets_w2lp"] = "W+jets";
  legLabel["wjets_w3lp"] = "W+jets";
  legLabel["wjets_w4lp"] = "W+jets";
  legLabel["wjets_w5lp"] = "W+jets";
  legLabel["data"] = "data";
  legLabel["z_ll"] = "Z/#gamma*";
  legLabel["others"] = "other bckg.";
  legLabel["signal"] = "ZZ";
  legLabel["ww_wz"] = "WW/WZ";
  legLabel["z_tt"] = "Z #rightarrow #tau #tau";
  legLabel["wjets_gp"] = "W+jets";
  legLabel["H400"] = "H (400GeV)";
  legLabel["QCD"] = "QCD (p_{T} > 15 GeV)";


  // Create the legend

  // legend in a box  
//   leg = new TLegend(0.83,0.70,0.995,0.995);

//   leg->SetFillColor(0);
//   leg->SetBorderSize(1);

  // legend with no box
  leg = new TLegend(0.62,0.65,0.95,0.95);

  leg->SetFillColor(0);
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
//   leg->SetTextSize(30);
  theStyle = gStyle;

}




HistoStack::~HistoStack(){
  // Clean up some memory
  for(map<TString, THStack *>::const_iterator stack =  stackMap.begin();
      stack != stackMap.end(); ++stack) {
    delete (*stack).second;
  }
  for(map<TString, TH1F *>::const_iterator hist =  dataHistMap.begin();
      hist != dataHistMap.end(); ++hist) {
    delete (*hist).second;
  }
  for(map<TString, TH1F *>::const_iterator hist = sumForErrMap.begin();
      hist != sumForErrMap.end(); ++hist) {
    delete (*hist).second;
  }
  delete leg;



}


// Set the mass cut for histos created on the fly
void HistoStack::setMassCut(double min, double max) {
  massMin = min;
  massMax = max;
  
  stringstream tmp;
  tmp << " DiLeptMinv > " << min << " && DiLeptMinv < " << max;
//   tmp >> theSelection;
  theSelection = tmp.str();
}



// Add a prefilled histos to the stack
// NOTE: the histo is not further scaled: this is supposed to be already done!
Number HistoStack::add(const TString& sampleName, const TString& varName, TH1F* histo) {
  if(histo == 0) { // check that this is a valid pointer
    cout << "[HistoStack]Warning: histo for variable: " << varName << " has non-valid pointer" << endl;
    return Number(-1,-1);
  }
  TString option = "";  

  // If a rebin option has been set witht the methos setRebin then we rebin the histo
  map<TString, int>::const_iterator rebin = rebinMap.find(varName);
  if(rebin != rebinMap.end()) {
    histo->Rebin((*rebin).second);
  }


  // Add the MC histo to the histo sum used to display the stack error
  if(!sampleName.Contains("data")) {
     if(sumForErrMap.find(varName) == sumForErrMap.end()) {
       TString hSumName = varName+"_sum";
       TH1F *hSum = (TH1F *)histo->Clone(hSumName.Data());
       sumForErrMap[varName] = hSum;
     } else {
       sumForErrMap[varName]->Add(histo);
     }
   }

   // check if the sample is assigned to any group
   TString groupName;
   if(groupMap.find(sampleName) !=  groupMap.end()) {
     groupName = groupMap[sampleName];
   } else {
     groupName = sampleName;
   }
   
  
  // Set the fill color for MC histos and marker style for data histos
  if(groupName != "data") {
    int color = colorMap.find(groupName)->second;
    if(color != -1) {
      histo->SetFillColor(color);
    } else {
      int fillStyle = fillStyleMap[groupName];
      if(fillStyle != -1) {
	histo->SetFillColor(1);
	histo->SetFillStyle(fillStyle);
      }
    }
    option = "hist";
  } else {
    histo->SetMarkerStyle(theStyle->GetMarkerStyle());
    histo->SetMarkerSize(theStyle->GetMarkerSize());
    histo->SetLineWidth(2);
  }

//   // Add the MC histo to the stack (and create the stack in case it doesn't exist)
//   if(groupName != "data") {
//     THStack * hs =0;
//     if(stackMap.find(varName) == stackMap.end()) {
//       hs = new THStack(varName.Data(), varName.Data());
//       hs->SetMinimum(0.001);
//       stackMap[varName] = hs;
//     } else {
//       hs = stackMap[varName];
//     }
//     hs->Add(histo,option.Data());
//   } else { // Store the data histo
//     dataHistMap[varName] = histo;
//   }

  // Store the data histo
  if(groupName == "data") {
    dataHistMap[varName] = histo;
  }

  //Add the histo to the map of histograms per sample so that it can be retrieved by the user
  // if the sample is in a group the histos are added
  map<TString, map<TString, TH1F *> >::iterator sampleAndHistoMap = histMapPerSample.find(groupName);
  
  if(sampleAndHistoMap != histMapPerSample.end()) {
    map<TString, TH1F *> histMp = sampleAndHistoMap->second;
    if(histMp.find(varName) != histMp.end()) {
      histMapPerSample[groupName][varName]->Add(histo);
    } else {
      histMapPerSample[groupName][varName] = histo;
      //add the sample to the list used to keep the order
      theSamplesInOrderPerVar[varName].push_back(groupName);
    }
  } else {
    histMapPerSample[groupName][varName] = histo;
    //add the sample to the list used to keep the order
    theSamplesInOrderPerVar[varName].push_back(groupName);
  }


  
//   // Add an entry to the legend
//   if(legSet.find(groupName) == legSet.end()) {
//     TString legendLabel = legLabel[groupName];
//     if(groupName == "data") {
//       if(alreadyInLeg.find(legendLabel) == alreadyInLeg.end()) {
// 	leg->AddEntry(histo,legendLabel.Data(),"pl");
// 	alreadyInLeg.insert(legendLabel);
//       }
//     } else {
//       if(alreadyInLeg.find(legendLabel) == alreadyInLeg.end()) {
// 	leg->AddEntry(histo,legendLabel.Data(),"F"); 
// 	alreadyInLeg.insert(legendLabel);
//       }
//     }
//     legSet.insert(groupName);
//   }
  
  // Build the yAxis title
  if(yAxisUnit.find(varName) != yAxisUnit.end() || yAxisTitle.find(varName) == yAxisTitle.end()) {
    TString pitch = getPitchString(histo,2);
    TString yTitle = "events/"+pitch+" "+yAxisUnit[varName];
    yAxisTitle[varName] = yTitle;
  }
  
//   double integral = 0;
  double sq_integral_error = 0;
  // Compute the error on the histo integral
  for(int i = 1; i <= histo->GetNbinsX(); ++i) {
//     integral += histo->GetBinContent(i);
    sq_integral_error += TMath::Power(histo->GetBinError(i),2.);
  }
  double integ_error = sqrt(sq_integral_error);


  // Print the histo integral
  int prec = cout.precision();
  cout.setf(ios::fixed);
  cout << sampleName
       << " # of weighted ev. (integral): " << setprecision(4) << histo->Integral()
       << " +/- " <<  integ_error << endl;
  cout << setprecision(prec);
  cout << " # entries: " << histo->GetEntries() << endl;
  return  Number(histo->Integral(),integ_error);
}


// Add an histo to the stack.
// The histo is filled on the fly and the correct weight is taken from the LumiNormalization object
Number HistoStack::add(const TString& sampleName, const TString& varName,
		       int nBins, float binMin, float binMax, double integral) {
  double scaleF = 1;
  // Build the file name of the file containing the tree
  TString fileName = theInputDir;
  if(sampleName == "data") {
    fileName = theInputDir+"/"+theFilePrefix+"_data_"+theFinalState+".root";
  } else {
    fileName = theInputDir+"/"+theFilePrefix+"_mc_"+sampleName+"_"+theFinalState+".root";
//     scaleF = 0.99;
  }

    // Open the file and retriev the ntuple
  TFile *file = new TFile(fileName.Data());// FIXME: file pointer should be stored
  TNtuple *ntuple = (TNtuple*)file->Get(ntupleName.Data());
  ntuple->AddFriend("KinemNtuple");



  // Append the weight to the formula to be used in the query
  TString formula = varName+weightBr;

  // Create the new histo to be added to the stack
  TH1F * hNew = new TH1F(varName.Data(),varName.Data(),nBins, binMin, binMax);
  hNew->Sumw2();
  // Create an utility histo to keep track of the weights to compute the integral and its error
  TH1F *hError = new TH1F("error", "error", 1,0.5, 1.5);
  hError->Sumw2();

  cout << "Selection: " << theSelection << endl;
  // Create 
  TSQLResult * query = ntuple->Query(formula.Data(), theSelection);
  // Check that the query contains the right number of field:
  // (2 fields: the variable and the weight
  if (query->GetFieldCount() != 2) {
    cout << "[HistoStack] Error: Invalid formula" << endl;
    delete query;
    file->Close();
    return Number(-1, -1);
  }

  // Fill the histo
  TSQLRow * row = 0;
  while ((row = query->Next())) {
    float variable = -999999;
    float weight = 1.0;

    variable = atof(row->GetField(0));
    weight = atof(row->GetField(1));
    hNew->Fill(variable*scaleF,weight);
    hError->Fill(1,weight);
    delete row;
  }
  
  // Get the scale factor
  double scale = 1;
  if(sampleName != "data") {
    scale = theLumiNorm->getScaleFactor(sampleName);
    hNew->Scale(scale);
  }

  if(integral != -1) {
    if(hNew->Integral() != 0) {
      hNew->Scale(integral/hNew->Integral());
    }
  }
  

  
//   // Print the histo integral
//   int prec = cout.precision();
//   cout.setf(ios::fixed);
//   cout << sampleName
//        << " # of weighted ev: " << setprecision(4) << scale*hError->Integral(-1,2)
//        << " +/- " <<  scale*hError->GetBinError(1) << endl;
//   cout << setprecision(prec);

  ntuple->ResetBranchAddresses(); //FIXME: probably not useful

  delete query;
  
  return add(sampleName, varName, hNew);
}


THStack * HistoStack::draw(const TString& varName, const TString& option) {
  bool doChi2 = false;
  if(option.Contains("chi2",TString::kIgnoreCase)) doChi2 = true;
  bool doKS = false;
  if(option.Contains("ks",TString::kIgnoreCase)) doKS = true;
  bool doLog = true;
  if(option.Contains("nolog",TString::kIgnoreCase)) doLog = false;
  bool pre = false;
  if(option.Contains("pre",TString::kIgnoreCase)) pre = true;
  bool printChannel = false;
  if(option.Contains("channel",TString::kIgnoreCase)) printChannel = true;
  bool d0lumi = false;
  if(option.Contains("d0lumi",TString::kIgnoreCase)) d0lumi = true;
  bool doLabel = false;
  if(option.Contains("label",TString::kIgnoreCase)) doLabel = true;

  cout << "Drawing: " << varName << endl;
//   if(stackMap.find(varName) == stackMap.end()) return 0;
  if(sumForErrMap.find(varName) == sumForErrMap.end()) return 0;

  TString canvasName = "cStack_"+varName;
  TCanvas *c1 = 0;
  // Check that a canvas has a unique name
  if(gROOT->GetListOfCanvases()->FindObject(canvasName.Data()) == 0) {
    c1 = new TCanvas(canvasName.Data(), canvasName.Data());
  } else { // Add an index to the canvas name
    int index = 0;
    TString newCanvasName;
    do {
      newCanvasName = canvasName+"_n";
      newCanvasName+=index;
      index++;
    } while(gROOT->GetListOfCanvases()->FindObject(newCanvasName.Data()) != 0);
    c1 = new TCanvas(newCanvasName.Data(), newCanvasName.Data());
  }

  c1->cd();
  if(doLog)
    c1->SetLogy();
  THStack *stack = createStack(varName);//stackMap.find(varName)->second;
  TH1F *hSumE = sumForErrMap.find(varName)->second;
  stack->SetMinimum(0.01);
  if(dataHistMap.find(varName) != dataHistMap.end()) {
    cout << "D1" << endl;
    setStyle(dataHistMap.find(varName)->second);
    dataHistMap.find(varName)->second->SetMinimum(0.001);
//     dataHistMap.find(varName)->second->Draw("E1");
    dataHistMap.find(varName)->second->Draw("E1");

    TH1F *dataHist =  dataHistMap.find(varName)->second;
     // Add the axis titles
    if(xAxisTitle.find(varName) != xAxisTitle.end()) {
      TString xTit = xAxisTitle.find(varName)->second;
      TString yTit = yAxisTitle.find(varName)->second;
      dataHist->GetXaxis()->SetTitle(xTit.Data());
      dataHist->GetYaxis()->SetTitle(yTit.Data());
    }
//     dataHistMap.find(varName)->second->GetYaxis()->SetRangeUser(axisYL, axisYU+plusRange);


    stack->Draw("same");

//     yAxis->SetRangeUser(0,18);
//     stack->Draw("same");

// stack->GetMinimum(),
//  			stack->GetMaximum()+(stack->GetMaximum()-stack->GetMinimum())/10.);


    // Superimpose an histo to show the stack error bars
//     hSumE->SetFillColor(1);
//     hSumE->SetFillStyle(3002);
    setStyle(hSumE);
    hSumE->SetMarkerStyle(1);
    hSumE->SetLineColor(1);
    hSumE->SetFillStyle(3003);
    hSumE->SetFillColor(1);
    hSumE->Draw("same,E2");
    dataHistMap.find(varName)->second->Draw("same,E1");

    double axisXU, axisXL, axisYU, axisYL;
    TAxis *yAxis = stack->GetYaxis(); // Misterious need of root to set the axis range
    //cout << (int)yAxis << endl;

    c1->GetRangeAxis(axisXL, axisYL, axisXU, axisYU);
//     cout << " YRange from: " << axisYL << " to: " << axisYU << endl;
    double yRange = axisYU - axisYL;
    double plusRange = yRange/20.;

    if(rangeMap.find(varName) != rangeMap.end()) {
      pair<double, double> range = rangeMap[varName];
      dataHistMap.find(varName)->second->GetYaxis()->SetRangeUser(range.first, range.second);
    } else {
      if(!doLog && d0lumi)
	dataHistMap.find(varName)->second->GetYaxis()->SetRangeUser(axisYL, axisYU+plusRange);
    }

    if(doChi2) {
      double chi2Prob = dataHistMap.find(varName)->second->Chi2Test(hSumE, "UU");
      TPaveText *chiText = new TPaveText(0.16,0.95,0.78, 0.99, "blNDC");
      stringstream tmp;
      tmp << "#chi^{2} prob: " << chi2Prob;
      string text = tmp.str();
      chiText->AddText(text.c_str());
      chiText->SetFillColor(0);
      chiText->SetTextSize(theStyle->GetTextSize());
      chiText->Draw("same");
    }
    if(doKS) {
      char ks_result[100];
      sprintf (ks_result, "K-S test: %.4f",dataHistMap.find(varName)->second->KolmogorovTest(hSumE) );
//       TPaveText *pt = new TPaveText(0.64,0.91,0.77,0.99,"blNDC");
      TPaveText *pt = new TPaveText(0.16,0.95,0.5, 0.99, "blNDC");
      pt->SetName("ks_test");
//       pt->SetBorderSize(1);
      pt->SetFillColor(0);
      pt->AddText(ks_result);
      pt->SetTextSize(theStyle->GetTextSize());
      pt->Draw("SAME");
    }

    if(doLabel) {
      TPaveText *labelAorB = new TPaveText(0.88,0.91,0.92, 0.95, "blNDC");
      labelAorB->SetFillColor(0);
      if(labelMap.find(varName) != labelMap.end()) {
	labelAorB->AddText(labelMap[varName]);
	labelAorB->SetTextSize(theStyle->GetTextSize());
	labelAorB->Draw("SAME");
      } else {
	cout << "[HistoStack]***Warning: no label set for variable: " << varName << endl;
      }
    }
    if(d0lumi) {
      TPaveText *pt_pre = new TPaveText(0.18,0.93,0.60, 0.96, "blNDC");
      if(!printChannel ) {
	pt_pre->AddText("CMS 2.7 fb^{-1}");
      } else {
	if(theFinalState == "diem") {
	  pt_pre->AddText("CMS 2.7 fb^{-1}:    e^{+}e^{-}");
	} else if(theFinalState == "dimu") {
	  pt_pre->AddText("CMS 2.7 fb^{-1}:    #mu^{+}#mu^{-}");
	} else {
	  cerr << "[HistoStack]***Error: final state not recognized for printing channel name: "
	       << theFinalState << endl;
	}
      }
      pt_pre->SetFillColor(0);
      pt_pre->SetFillStyle(0);
      pt_pre->SetLineStyle(0);
      pt_pre->SetLineColor(0);
      pt_pre->SetLineWidth(0);

      pt_pre->SetTextAlign(12);
      pt_pre->SetTextColor(1); 
      pt_pre->SetTextFont(theStyle->GetTextFont());
      pt_pre->SetTextSize(theStyle->GetTextSize());
      pt_pre->Draw("SAME");
      
      
    } else if(pre) {
//       TPaveText *t1 = new TPaveText();
//     t1->SetTextFont(62);
//     t1->SetTextColor(1);   // 4
//     t1->SetTextAlign(12);
//     t1->SetTextSize(0.06);
//     t1->DrawTextNDC(0.38,0.92,"D#oslash Run II Preliminary 2.2 fb^{-1}"); 
//     t1->Draw("SAME");
      TPaveText *pt_pre = new TPaveText(0.15,0.957,0.58, 0.997, "blNDC");
      if(!printChannel ) {
	pt_pre->AddText("CMS Preliminary 2.7 fb^{-1}");
      } else {
	if(theFinalState == "diem") {
	  pt_pre->AddText("CMS Preliminary 2.7 fb^{-1}:    e^{+}e^{-}");
	} else if(theFinalState == "dimu") {
	  pt_pre->AddText("CMS Preliminary 2.7 fb^{-1}:    #mu^{+}#mu^{-}");
	} else {
	  cerr << "[HistoStack]***Error: final state not recognized for printing channel name: "
	       << theFinalState << endl;
	}
      }
      pt_pre->SetFillColor(0);
      pt_pre->SetTextAlign(12);
      pt_pre->SetTextColor(1); 
      pt_pre->SetTextFont(theStyle->GetTextFont());
      pt_pre->SetTextSize(theStyle->GetTextSize());
      pt_pre->Draw("SAME");
    } else if(printChannel) {
      TPaveText *pt_pre = new TPaveText(0.15,0.956,0.58, 0.996, "blNDC");
      if(theFinalState == "diem") {
	pt_pre->AddText("e^{+}e^{-}");
      } else if(theFinalState == "dimu") {
	pt_pre->AddText("#mu^{+}#mu^{-}");
      } else {
	cerr << "[HistoStack]***Error: final state not recognized for printing channel name: "
	     << theFinalState << endl;
      }
      pt_pre->SetFillColor(0);
      pt_pre->SetTextAlign(12);
      pt_pre->SetTextColor(1); 
      pt_pre->SetTextFont(theStyle->GetTextFont());
      pt_pre->SetTextSize(theStyle->GetTextSize());
      pt_pre->Draw("SAME");
    }
  } else {
    cout << "D2" << endl;
    stack->Draw();
    setStyle(hSumE);
    hSumE->SetMarkerStyle(1);
    hSumE->SetLineColor(1);
    hSumE->SetFillStyle(3003);
    hSumE->SetFillColor(1);
    hSumE->Draw("same,E2");

  }
 

  // Add the axis titles
  if(xAxisTitle.find(varName) != xAxisTitle.end()) {
    TString xTit = xAxisTitle.find(varName)->second;
    TString yTit = yAxisTitle.find(varName)->second;
    stack->GetXaxis()->SetTitle(xTit.Data());
    stack->GetYaxis()->SetTitle(yTit.Data());
    cout << "add axis" << endl;
    cout <<  stack->GetYaxis()->GetTitle() << endl;
  } else {
    cout << "no axis title defined" << endl;
  }
  
  // Add the legend
  TLegend *tmpLeg = (TLegend*)leg->Clone();
  tmpLeg->Draw("same");
  return stack;
}


void HistoStack::setAxisTitles(const TString& varName, const TString& xTitle, const TString& yUnits) {
  xAxisTitle[varName] = xTitle;
  yAxisUnit[varName] = yUnits;
}


TString HistoStack::getPitchString(TH1 *histo, int prec) const {
//   float min = histo->GetXaxis()->GetXmin();
//   float max = histo->GetXaxis()->GetXmax();
//   int nbins = histo->GetXaxis()->GetNbins();
//   float pitch = (max - min)/nbins;
  float pitch = histo->GetBinWidth(1);
  stringstream ss;
  ss << setprecision(prec);
  ss << pitch;
  TString buffer;
  ss >> buffer;
  return buffer;
}



// Set the style of the axis of an histo created before setting the current style
void HistoStack::setStyle(TH1 *histo) const  {
  histo->GetXaxis()->SetTitleFont(gStyle->GetTitleFont());
  histo->GetXaxis()->SetTitleSize(gStyle->GetTitleFontSize());
  histo->GetXaxis()->SetLabelFont(gStyle->GetLabelFont());
  histo->GetXaxis()->SetLabelSize(gStyle->GetLabelSize());
  histo->GetXaxis()->SetLabelOffset(gStyle->GetLabelOffset("X"));
  histo->GetXaxis()->SetNdivisions(gStyle->GetNdivisions("X"),"X");

  histo->GetYaxis()->SetTitleFont(gStyle->GetTitleFont());
  histo->GetYaxis()->SetTitleSize(gStyle->GetTitleFontSize());
  histo->GetYaxis()->SetLabelFont(gStyle->GetLabelFont());
  histo->GetYaxis()->SetLabelSize(gStyle->GetLabelSize());
  histo->GetYaxis()->SetLabelOffset(gStyle->GetLabelOffset("Y"));
  histo->GetYaxis()->SetNdivisions(gStyle->GetNdivisions("Y"),"Y");



}


void HistoStack::addCut(const TString& cut) {
  theSelection += " && " + cut;
}

void HistoStack::resetCut(const TString& cut) {
  theSelection = cut;
}

TString HistoStack::getCut() const {
  return theSelection;
}


void HistoStack::drawAll(const TString& option) {
  for(map<TString, TH1F *>::const_iterator stack = sumForErrMap.begin();
      stack != sumForErrMap.end(); ++stack) {
    draw((*stack).first, option);
  }
}



void HistoStack::setNtupleName(const TString& newName) {
  ntupleName = newName;
}


void HistoStack::addMultiplicativeWeight(const TString& weightName) {
  weightBr = ":weight*"+weightName;
}



TH1F *HistoStack::getHisto(const TString& sampleName, const TString& varName) {
  return histMapPerSample[sampleName][varName];
}



void HistoStack::setRebin(const TString& varName, int reb) {
  rebinMap[varName] = reb;
}


// create the stack "on-demand" when it's needed and stores it in the map
THStack * HistoStack::createStack(const TString& varName) {
  buildLegend(varName);
  THStack * hs =0;
  TString option = "hist";

  if(stackMap.find(varName) == stackMap.end()) {
    hs = new THStack(varName.Data(), varName.Data());
    hs->SetMinimum(0.001);
    
    // Get the list of samples for this variable in the correct order
    vector<TString> orderedSamples = theSamplesInOrderPerVar[varName];
    // loop over the samples and add them to the stack
    for(vector<TString>::const_iterator samp = orderedSamples.begin();
	samp != orderedSamples.end(); ++samp) {
      if((*samp).Contains("data")) continue;
      hs->Add(histMapPerSample[*samp][varName],option.Data());
      if(varName == "alat_corr_reduced_t") {
	TH1F *histo = histMapPerSample[*samp][varName];
	double maxBB = 14;
	if(theFinalState == "dimu") maxBB = 13;
	
	double integral = (histo->GetBinWidth(maxBB)/2.)*histo->GetBinContent(maxBB) + (histo->GetBinWidth(maxBB-1)/2.)*histo->GetBinContent(maxBB-1) + (histo->GetBinWidth(maxBB-2)/2.)*histo->GetBinContent(maxBB-2) + histo->GetBinContent(maxBB+1);
	cout << "DBG: " <<  *samp << " integ: " << integral << endl;
	
      }


    }
    stackMap[varName] = hs;

  } else {
    hs = stackMap[varName];
  }
  return hs;  

//   // Add the MC histo to the stack (and create the stack in case it doesn't exist)
//   if(sampleName != "data") {
//     THStack * hs =0;
//     if(stackMap.find(varName) == stackMap.end()) {
//       hs = new THStack(varName.Data(), varName.Data());
//       hs->SetMinimum(0.001);
//       stackMap[varName] = hs;
//     } else {
//       hs = stackMap[varName];
//     }
//     hs->Add(histo,option.Data());
//   } else { // Store the data histo
//     dataHistMap[varName] = histo;
//   }
}


void HistoStack::assignToGroup(const TString& sampleName, const TString& groupName) {
  groupMap[sampleName] = groupName;
}


void HistoStack::buildLegend(const TString& varName) {
  
  // Get the list of samples for this variable in the correct order
  vector<TString> orderedSamples = theSamplesInOrderPerVar[varName];
  if(samplesOrderInLegend.size() != 0) {
    orderedSamples.clear();
    for(map<int, TString>::const_iterator sampleForLegend = samplesOrderInLegend.begin();
	sampleForLegend != samplesOrderInLegend.end();
	++sampleForLegend) {
      orderedSamples.push_back((*sampleForLegend).second);
    }
  }
  
  
  // loop over the samples and add them to the stack
  for(vector<TString>::const_iterator samp = orderedSamples.begin();
      samp != orderedSamples.end(); ++samp) {
    if(legSet.find(*samp) == legSet.end()) {
      TString legendLabel = legLabel[*samp];
      TH1F *histo = histMapPerSample[*samp][varName];
      if(*samp == "data") {
	leg->AddEntry(histo,legendLabel.Data(),"pl");
      } else {
	leg->AddEntry(histo,legendLabel.Data(),"F"); 
      }
      legSet.insert(*samp);
    }
  }
}


// se the order for the legend of samples or groups
void HistoStack::setLegendOrder(int order, const TString& sampleName) {
  samplesOrderInLegend[order] = sampleName;
}



// Se the y range of the stack
void HistoStack::setYRange(const TString& varName,double yLow, double yHigh) {
  rangeMap[varName] = make_pair(yLow,yHigh);
}



void HistoStack::setLabel(const TString& varName, const TString& label) {
  labelMap[varName] = label;
}




void HistoStack::setFillColor(const TString& sampleName, int color) {
  colorMap[sampleName] = color;
}
