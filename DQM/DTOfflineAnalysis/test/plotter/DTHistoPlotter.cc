/*
 *  See header file for a description of this class.
 *
 *  $Date: 2008/12/03 10:41:16 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "DTHistoPlotter.h"

#include <iostream>
#include <stdio.h>
#include <sstream>
#include <string>

#include "TFile.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TCollection.h"
#include "TSystem.h"
#include "TF1.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TProfile.h"

using namespace std;

// Constructor
DTHistoPlotter::DTHistoPlotter( TFile *file) : theFile(file) {
  version = 1;
}


// Destructor
DTHistoPlotter::~DTHistoPlotter(){}


TH1F *DTHistoPlotter::plotRes(int wheel, int station, int sector, int sl,
	      const TString& drawOptions) {
  TString histoName = "hResDist_" +
    getHistoNameSuffix(wheel, station, sector, sl);
  TH1F *histo = plotHisto(histoName, drawOptions);
  if(histo !=0) {
    double min = -1.;
    double max = 1.;
    histo->GetXaxis()->SetRangeUser(min,max);
    histo->Fit("gaus","R");
  }
  return histo;
}



TH2F * DTHistoPlotter::plotResVsDistToWire(int wheel, int station, int sector, int sl,
					   const TString& drawOptions) {
  TString histoName = "hResDistVsDist_" +
    getHistoNameSuffix(wheel, station, sector, sl);
  TH2F *histo = plotHisto2D(histoName);
  histo->GetYaxis()->SetRangeUser(-2,2);
  if(drawOptions.Contains("profile") && histo != 0) {
    TProfile* prof = histo->ProfileX();
    prof->SetMarkerColor(2);
    prof->SetLineColor(2);
    prof->Draw("same");
  }
  return histo;
}


TProfile * DTHistoPlotter::plotResVsSLY(int wheel, int station, int sector, int sl,
					const TString& drawOptions) {
  TProfile *profile = 0;
  TString histoName;
  if(version == 0) { // FIXME: TO be removed...this is for file containing the TH3F and not the TProfiles

    histoName = "hResDistVsPosInSL_" +
      getHistoNameSuffix(wheel, station, sector, sl);
    TH3F *histo = (TH3F *) theFile->Get(histoName.Data());
    if(histo == 0) {
      cout << "***Error: Histogram: " << histoName << " doesn't exist!" << endl;
      return 0;
    }
    TH2D* proj1 = (TH2D*) histo->Project3D("zy");
    profile = proj1->ProfileX();
  } else if(version == 1) {
    histoName = "hResDistVsYInSL_" +
      getHistoNameSuffix(wheel, station, sector, sl);
    profile = (TProfile *) theFile->Get(histoName.Data());
  }
  static int color;
  TCanvas *c;
  if(!drawOptions.Contains("same")) {
    color = 1;
    c = newCanvas("c_"+histoName+"_Y");
    c->cd();
    profile->SetLineColor(color);
  } else {
    color ++;
    profile->SetLineColor(color);
  }

  profile->Draw(drawOptions.Data());
  return profile;
}



TProfile * DTHistoPlotter::plotResVsSLX(int wheel, int station, int sector, int sl,
					const TString& drawOptions) {
  TProfile *profile = 0;
  TString histoName;
  if(version == 0) { // FIXME: TO be removed...this is for file containing the TH3F and not the TProfiles

    histoName = "hResDistVsPosInSL_" +
      getHistoNameSuffix(wheel, station, sector, sl);
    TH3F *histo = (TH3F *) theFile->Get(histoName.Data());
    if(histo == 0) {
      cout << "***Error: Histogram: " << histoName << " doesn't exist!" << endl;
      return 0;
    }
    TH2D* proj1 = (TH2D*) histo->Project3D("zx");
    profile = proj1->ProfileX();
  } else if(version == 1) {
    histoName = "hResDistVsXInSL_" +
      getHistoNameSuffix(wheel, station, sector, sl);
    profile = (TProfile *) theFile->Get(histoName.Data());
  }

  static int color;
  TCanvas *c;
  if(!drawOptions.Contains("same")) {
    color = 1;
    c = newCanvas("c_"+histoName+"_X");
    c->cd();
    profile->SetLineColor(color);
  } else {
    color ++;
    profile->SetLineColor(color);
  }

  profile->Draw(drawOptions.Data());
  return profile;
}



TH1F * DTHistoPlotter::plotN4DSegm(int wheel, int station, int sector,
				   const TString& drawOptions) {
  TString histoName = "hN4DSeg_" +
    getHistoNameSuffix(wheel, station, sector);
  return plotHisto(histoName, drawOptions);
}
  



TH1F * DTHistoPlotter::plotChi24DSegm(int wheel, int station, int sector,
				      const TString& drawOptions) {
  TString histoName = "h4DChi2_" +
    getHistoNameSuffix(wheel, station, sector);
  return plotHisto(histoName, drawOptions);
}


  
TH1F * DTHistoPlotter::plotImpAngle(int wheel, int station, int sector,
				    const TString& drawOptions) {
  TString histoName = "hImpAngle_" +
    getHistoNameSuffix(wheel, station, sector);
  return plotHisto(histoName, drawOptions);
}


  
TH1F * DTHistoPlotter::plotSegmAngleSLTheta(int wheel, int station, int sector,
					    const TString& drawOptions) {
  TString histoName = "h4DSegmThetaAngle_" +
    getHistoNameSuffix(wheel, station, sector);
  return plotHisto(histoName, drawOptions);
}


  
TH1F * DTHistoPlotter::plotSegmAngleSLPhi(int wheel, int station, int sector,
					  const TString& drawOptions) {
  TString histoName = "h4DSegmPhiAngle_" +
    getHistoNameSuffix(wheel, station, sector);
  return plotHisto(histoName, drawOptions);
}


  
TH2F * DTHistoPlotter::plotPosInChSegm4D(int wheel, int station, int sector,
					 const TString& drawOptions) {
  TString histoName = "h4DSegmXvsYInCham_" +
    getHistoNameSuffix(wheel, station, sector);
  return plotHisto2D(histoName);
}
  


TH1F * DTHistoPlotter::plotPosXInChSegm4D(int wheel, int station, int sector,
					  const TString& drawOptions) {
  TString histoName = "h4DSegmXvsYInCham_" +
    getHistoNameSuffix(wheel, station, sector);
  TH2F *histo = (TH2F *) theFile->Get(histoName.Data());
  TH1F *projX = (TH1F*)histo->ProjectionX();
    static int color;
  TCanvas *c;
  if(!drawOptions.Contains("same")) {
    color = 1;
    c = newCanvas("c_"+histoName+"_X");
    c->cd();
    projX->SetLineColor(color);
  } else {
    color ++;
    projX->SetLineColor(color);
  }

  projX->Draw(drawOptions.Data());
  return projX;
}

TH1F * DTHistoPlotter::plotPosYInChSegm4D(int wheel, int station, int sector,
					  const TString& drawOptions) {
  TString histoName = "h4DSegmXvsYInCham_" +
    getHistoNameSuffix(wheel, station, sector);
  TH2F *histo = (TH2F *) theFile->Get(histoName.Data());
  TH1F *projY = (TH1F*)histo->ProjectionY();
    static int color;
  TCanvas *c;
  if(!drawOptions.Contains("same")) {
    color = 1;
    c = newCanvas("c_"+histoName+"_Y");
    c->cd();
    projY->SetLineColor(color);
  } else {
    color ++;
    projY->SetLineColor(color);
  }

  projY->Draw(drawOptions.Data());
  return projY;
}
    

void DTHistoPlotter::printPDF() {
  TIter iter(gROOT->GetListOfCanvases());
  TCanvas *c;
  while( (c = (TCanvas *)iter()) ) {
    c->Print(0,"eps");
    TString command =  TString("epstopdf ") + TString(c->GetName()) + TString(".eps");
    gSystem->Exec(command.Data());
  }
}



TString DTHistoPlotter::getHistoNameSuffix(int wheel, int station, int sector) {
  string histoName;
  stringstream theStream;
  theStream << "W" <<wheel << "_St" << station << "_Sec" << sector;
  theStream >> histoName;
  return TString(histoName.c_str());
}



TString DTHistoPlotter::getHistoNameSuffix(int wheel, int station, int sector, int sl) {
  string histoName;
  stringstream theStream;
  theStream << getHistoNameSuffix(wheel, station, sector) << "_SL" << sl;
  theStream >> histoName;
  return TString(histoName.c_str());
}
  


TString DTHistoPlotter::getHistoNameSuffix(int wheel, int station, int sector, int sl, int layer) {
  string histoName;
  stringstream theStream;
  theStream << "Ch_" <<wheel << "_" << station << "_" << sector << "_SL" << sl << "_L" << layer << "_Wall";
  theStream >> histoName;
  return TString(histoName.c_str());
}



TString DTHistoPlotter::getHistoNameSuffix(int wheel, int station, int sector, int sl, int layer, int wire) {
  string histoName;
  stringstream theStream;
  theStream << "Ch_" <<wheel << "_" << station << "_" << sector << "_SL" << sl << "_L" << layer << "_W" << wire;
  theStream >> histoName;
  return TString(histoName.c_str());
}



TH1F* DTHistoPlotter::plotHisto(const TString& histoName, const TString& drawOptions) {
  TH1F *histo = (TH1F *) theFile->Get(histoName.Data());
  if(histo == 0) {
    cout << "***Error: Histogram: " << histoName << " doesn't exist!" << endl;
    return 0;
  }
  static int color;
  
  TCanvas *c;
  if(!drawOptions.Contains("same")) {
    color = 1;
    c = newCanvas("c_"+histoName);
    c->cd();
    histo->SetLineColor(color);
  } else {
    color ++;
    histo->SetLineColor(color);
  }
  histo->Draw(TString("h"+drawOptions).Data());

//   if(drawOptions.Contains("fit")) {
//     theFitter->fitTimeBox(histo);
//   }


  return histo;
}




TH2F* DTHistoPlotter::plotHisto2D(const TString& histoName, const TString& drawOptions) {
  TH2F *histo = (TH2F *) theFile->Get(histoName.Data());
  if(histo == 0) {
    cout << "***Error: Histogram: " << histoName << " doesn't exist!" << endl;
    return 0;
  }
  static int color;

  TCanvas *c;
  if(!drawOptions.Contains("same")) {
    color = 1;
    c = newCanvas("c_"+histoName);
    c->cd();
    histo->SetLineColor(color);
  } else {
    color ++;
    histo->SetLineColor(color);
  } 
  histo->Draw(TString("h"+drawOptions).Data());
  return histo;
}






TCanvas * DTHistoPlotter::newCanvas(TString name, TString title,
				    int xdiv, int ydiv, int form, int w){
  static int i = 1;
  if (name == "") {
    name = TString("Canvas "+i);
    i++;
  }
  TCanvas *c = 0;
  if (title == "") title = name;
  if (w<0) {
    c = new TCanvas(name,title, form);
  } else {
    c = new TCanvas(name,title,form,w);
  }
  if (xdiv*ydiv!=0) c->Divide(xdiv,ydiv);
  c->cd(1);
  return c;
}

TCanvas * DTHistoPlotter::newCanvas(TString name, int xdiv, int ydiv, int form, int w) {
  return newCanvas(name, name,xdiv,ydiv,form,w);
}
TCanvas * DTHistoPlotter::newCanvas(int xdiv, int ydiv, int form) {
  return newCanvas("","",xdiv,ydiv,form);
}
TCanvas * DTHistoPlotter::newCanvas(int form)
{
  return newCanvas(0,0,form);
}

TCanvas * DTHistoPlotter::newCanvas(TString name, int form, int w)
{
  return newCanvas(name, name, 0,0,form,w);
}

TString DTHistoPlotter::getDirName(int wheel, int station, int sector) {
  string dirName;
  stringstream theStream;
  theStream << "Wheel" <<wheel << "/Station" << station << "/Sector" << sector <<"/";
  theStream >> dirName;
  return TString(dirName.c_str());
}
