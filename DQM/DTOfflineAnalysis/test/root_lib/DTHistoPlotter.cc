/*
 *  See header file for a description of this class.
 *
 *  $Date: 2010/07/29 13:56:22 $
 *  $Revision: 1.5 $
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
#include "TTree.h"
#include "RooRealVar.h"
#include "RooGaussian.h"
#include "RooAddPdf.h"
#include "RooFormulaVar.h"
#include "RooDataHist.h"
#include "RooFitResult.h"
#include "RooPlot.h"
#include "RooFit.h"
#include "RooGlobalFunc.h"
#include "TPostScript.h"
#include "TAxis.h"
#include "TMath.h"

#include "DTDetId.h"
#include "Histograms.h"
#include "Utils.h"

using namespace std;

// Constructor
DTHistoPlotter::DTHistoPlotter() {
}


// Destructor
DTHistoPlotter::~DTHistoPlotter(){}


TH1F *DTHistoPlotter::plotRes(const int fileN,
			      const TString& set,
			      int wheel, int station, int sector, int sl,
			      const TString& drawOptions) {
  DTDetId detId(wheel, station, sector, sl, 0, 0);
  HRes1DHits *hRes = getHistoRes(fileN, set, detId);
  TH1F *histo = 0;
  if(drawOptions.Contains("central")) {
    histo = (TH1F*)hRes->hResDistVsDist->ProjectionY(hRes->hResDist->GetName(),20,80);
  } else {
    histo = hRes->hResDist;
  }
  if(histo !=0) {
    //     drawHisto(fileN, histo, drawOptions);
    //     histo->Fit("gaus","","",-0.1,0.1);
    fitAndDraw(fileN, histo);
  }
  return histo;
}


TH1F * DTHistoPlotter::plotChi24DSegm(const int fileN,
				      const TString& set,
				      int wheel, int station, int sector,
				      const TString& drawOptions) {
  DTDetId detId(wheel, station, sector, 0, 0, 0);
  HSegment *hSeg = getHistoSeg(fileN, set, detId);
  TH1F *histo = hSeg->hChi2;
  if(histo !=0) {
    drawHisto(fileN, histo, drawOptions);
  }
  return histo;
}

TH1F * DTHistoPlotter::plotNHitsSegm(const int fileN,
				     const TString& set,
				     int wheel, int station, int sector,
				     const TString& drawOptions) {
  DTDetId detId(wheel, station, sector, 0, 0, 0);
  HSegment *hSeg = getHistoSeg(fileN, set, detId);
  TH1F *histo = 0; //hSeg->hNHits; //FIXME to be updated
  if(histo !=0) {
    drawHisto(fileN, histo, drawOptions);
  }
  return histo;
}


TH1F * DTHistoPlotter::plotSegmAngleSLTheta(const int fileN,
					    const TString& set,
					    int wheel, int station, int sector,
					    const TString& drawOptions) {
  DTDetId detId(wheel, station, sector, 0, 0, 0);
  HSegment *hSeg = getHistoSeg(fileN, set, detId);
  TH1F *histo = hSeg->hThetaLoc;
  if(histo !=0) {
    drawHisto(fileN, histo, drawOptions);
  }
  return histo;
}


  
TH1F * DTHistoPlotter::plotSegmAngleSLPhi(const int fileN,
					  const TString& set,
					  int wheel, int station, int sector,
					  const TString& drawOptions) {
  DTDetId detId(wheel, station, sector, 0, 0, 0);
  HSegment *hSeg = getHistoSeg(fileN, set, detId);
  TH1F *histo = hSeg->hPhiLoc;
  if(histo !=0) {
    drawHisto(fileN, histo, drawOptions);
  }

    return histo;
  // Get the number of bins
  const int nBins = histo->GetNbinsX();

  TH1F *histoAbs = new TH1F("abs_phi", "abs phi", nBins/2,0., TMath::Pi()/2.);
  
  // Loop over all the bins
  for (int bin=0; bin<=nBins+1; bin++){
    histoAbs->Fill(fabs(histo->GetBinCenter(bin)-TMath::Pi()/2.), histo->GetBinContent(bin));
  }
  drawHisto(fileN, histoAbs, drawOptions);
  cout << "Mean angle: " << histoAbs->GetMean()*TMath::RadToDeg() << " vdrift: " << (1-(tan(histoAbs->GetMean())*0.65)/1.05)*54.3 << endl;
  return histo;

}



TH2F * DTHistoPlotter::plotNHitsPhiVsPhi(const int fileN,
					 const TString& set,
					 int wheel, int station, int sector,
					 const TString& drawOptions) {

  DTDetId detId(wheel, station, sector, 0, 0, 0);
  HSegment *hSeg = getHistoSeg(fileN, set, detId);
  TH2F *histo = hSeg->hNHitsPhiVsPhi;
  if(histo !=0) {
    drawHisto(fileN, histo, drawOptions);
  }
  return histo;
}


TH2F * DTHistoPlotter::plotNHitsThetaVsPhi(const int fileN,
					   const TString& set,
					   int wheel, int station, int sector,
					   const TString& drawOptions) {

  DTDetId detId(wheel, station, sector, 0, 0, 0);
  HSegment *hSeg = getHistoSeg(fileN, set, detId);
  TH2F *histo = hSeg->hNHitsThetaVsPhi;
  if(histo !=0) {
    drawHisto(fileN, histo, drawOptions);
  }
  return histo;
}



TH1F * DTHistoPlotter::plotProjSegm(const int fileN,
				    const TString& set,
				    int wheel, int station, int sector,
				    const TString& drawOptions) {

  DTDetId detId(wheel, station, sector, 0, 0, 0);
  HSegment *hSeg = getHistoSeg(fileN, set, detId);
  TH1F *histo = hSeg->hProj;
  if(histo !=0) {
    drawHisto(fileN, histo, drawOptions);
  }
  return histo;
}


TH1F * DTHistoPlotter::plotNHitsTheta(const int fileN,
				      const TString& set,
				      int wheel, int station, int sector,
				      const TString& drawOptions) {
  DTDetId detId(wheel, station, sector, 0, 0, 0);
  HSegment *hSeg = getHistoSeg(fileN, set, detId);
  TH1F *histo = 0; // hSeg->hNHitsTheta; //FIXME: to be updated
  if(histo !=0) {
    drawHisto(fileN, histo, drawOptions);
  }
  return histo;

}

TH1F * DTHistoPlotter::plotT0SegPhi(const int fileN,
				    const TString& set,
				    int wheel, int station, int sector,
				    const TString& drawOptions) {
  DTDetId detId(wheel, station, sector, 0, 0, 0);
  HSegment *hSeg = getHistoSeg(fileN, set, detId);
  TH1F *histo = 0; //hSeg->ht0Phi; //FIXME to be updated
  if(histo !=0) {
    drawHisto(fileN, histo, drawOptions);
  }
  return histo;

}

TH1F * DTHistoPlotter::plotSeg1D(const TString& hName,
				 const int fileN,
				 const TString& set,
				 int wheel, int station, int sector,
				 const TString& drawOptions) {
  DTDetId detId(wheel, station, sector, 0, 0, 0);
  HSegment *hSeg = getHistoSeg(fileN, set, detId);
  TH1F *histo = 0;

  //  if(hName == "NHits") histo = hSeg->hNHits; //FIXME to be updated
  //  else if(hName == "NHitsPhi") histo = hSeg->hNHitsPhi; //FIXME to be updated
  //  else if(hName == "NHitsTheta") histo = hSeg->hNHitsTheta; //FIXME to be updated
  //  else 
  if(hName == "Proj") histo = hSeg->hProj;
  else if(hName == "PhiLoc") histo = hSeg->hPhiLoc;
  else if(hName == "ThetaLoc") histo = hSeg->hThetaLoc;
  //  else if(hName == "ImpAngl") histo = hSeg->hImpAngl;
  else if(hName == "Chi2") histo = hSeg->hChi2;
  //  else if(hName == "t0Phi") histo = hSeg->ht0Phi; //FIXME to be updated
  //  else if(hName == "t0Theta") histo = hSeg->ht0Theta; //FIXME to be updated
  //  else if(hName == "DeltaT0") histo = hSeg->hDeltaT0; //FIXME to be updated
  else if(hName == "VDrift") histo = hSeg->hVDrift;
  else if(hName == "NSegm") histo = hSeg->hNSegm;
  else cout << "***Warning: Name of 1D plot not found!!!" << endl;
  if(histo !=0) {
    drawHisto(fileN, histo, drawOptions);
  }
  return histo;

}

TH2F * DTHistoPlotter::plotSeg2D(const TString& hName,
				 const int fileN,
				 const TString& set,
				 int wheel, int station, int sector,
				 const TString& drawOptions) {
  DTDetId detId(wheel, station, sector, 0, 0, 0);
  HSegment *hSeg = getHistoSeg(fileN, set, detId);
  TH2F *histo = 0;

  if(hName == "NHitsPhiVsPhi") histo = hSeg->hNHitsPhiVsPhi;
  else if(hName == "NHitsThetaVsPhi") histo = hSeg->hNHitsThetaVsPhi;
  else if(hName == "NHitsThetaVsTheta") histo = hSeg->hNHitsThetaVsTheta;
  else if(hName == "t0PhiVsPhi") histo = hSeg->ht0PhiVsPhi;
  else if(hName == "VDriftVsPhi") histo = hSeg->hVDriftVsPhi;
  else cout << "***Warning: Name of 2D plot not found!!!" << endl;

  if(histo !=0) {
    drawHisto(fileN, histo, drawOptions);
  }
  return histo;

}


TH1F * DTHistoPlotter::plotRes1D(const TString& hName,
				 const int fileN,
				 const TString& set,
				 int wheel, int station, int sector, int sl,
				 const TString& drawOptions) {
  DTDetId detId(wheel, station, sector, sl, 0, 0);
  HRes1DHits *hRes = getHistoRes(fileN, set, detId);
  TH1F *histo = 0;

  if(hName == "ResDist") histo = hRes->hResDist;
  else if(hName == "ResPos") histo = hRes->hResPos;
  else if(hName == "PullPos") histo = hRes->hPullPos;
  else cout << "***Warning: Name of 1D plot not found!!!" << endl;

  if(histo !=0) {
    drawHisto(fileN, histo, drawOptions);
  }
  return histo;

}

TH2F * DTHistoPlotter::plotRes2D(const TString& hName,
				 const int fileN,
				 const TString& set,
				 int wheel, int station, int sector, int sl,
				 const TString& drawOptions) {
  DTDetId detId(wheel, station, sector, sl, 0, 0);
  HRes1DHits *hRes = getHistoRes(fileN, set, detId);
  TH2F *histo = 0;

  if(hName == "ResDistVsDist") histo = hRes->hResDistVsDist;
  else if(hName == "ResDistVsAngle") histo = hRes->hResDistVsAngle;
  else if(hName == "ResPosVsAngle") histo = hRes->hResPosVsAngle;
  else if(hName == "ResDistVsY") histo = hRes->hResDistVsY;
  else cout << "***Warning: Name of 2D plot not found!!!" << endl;

  if(histo !=0) {
    drawHisto(fileN, histo, drawOptions);
  }
  return histo;

}


// TH2F * DTHistoPlotter::plotResVsDistToWire(int wheel, int station, int sector, int sl,
// 					   const TString& drawOptions) {
//   TString histoName = "hResDistVsDist_" +
//     getHistoNameSuffix(wheel, station, sector, sl);
//   TH2F *histo = plotHisto2D(histoName);
//   histo->GetYaxis()->SetRangeUser(-2,2);
//   if(drawOptions.Contains("profile") && histo != 0) {
//     TProfile* prof = histo->ProfileX();
//     prof->SetMarkerColor(2);
//     prof->SetLineColor(2);
//     prof->Draw("same");
//   }
//   return histo;
// }


// TProfile * DTHistoPlotter::plotResVsSLY(int wheel, int station, int sector, int sl,
// 					const TString& drawOptions) {
//   TProfile *profile;
//   TString histoName;
//   if(version == 0) { // FIXME: TO be removed...this is for file containing the TH3F and not the TProfiles

//     histoName = "hResDistVsPosInSL_" +
//       getHistoNameSuffix(wheel, station, sector, sl);
//     TH3F *histo = (TH3F *) theFile->Get(histoName.Data());
//     if(histo == 0) {
//       cout << "***Error: Histogram: " << histoName << " doesn't exist!" << endl;
//       return 0;
//     }
//     TH2D* proj1 = (TH2D*) histo->Project3D("zy");
//     profile = proj1->ProfileX();
//   } else if(version == 1) {
//     histoName = "hResDistVsYInSL_" +
//       getHistoNameSuffix(wheel, station, sector, sl);
//     profile = (TProfile *) theFile->Get(histoName.Data());
//   }
//   static int color;
//   TCanvas *c;
//   if(!drawOptions.Contains("same")) {
//     color = 1;
//     c = newCanvas("c_"+histoName+"_Y");
//     c->cd();
//     profile->SetLineColor(color);
//   } else {
//     color ++;
//     profile->SetLineColor(color);
//   }

//   profile->Draw(drawOptions.Data());
//   return profile;
// }



// TProfile * DTHistoPlotter::plotResVsSLX(int wheel, int station, int sector, int sl,
// 					const TString& drawOptions) {
//   TProfile *profile;
//   TString histoName;
//   if(version == 0) { // FIXME: TO be removed...this is for file containing the TH3F and not the TProfiles

//     histoName = "hResDistVsPosInSL_" +
//       getHistoNameSuffix(wheel, station, sector, sl);
//     TH3F *histo = (TH3F *) theFile->Get(histoName.Data());
//     if(histo == 0) {
//       cout << "***Error: Histogram: " << histoName << " doesn't exist!" << endl;
//       return 0;
//     }
//     TH2D* proj1 = (TH2D*) histo->Project3D("zx");
//     profile = proj1->ProfileX();
//   } else if(version == 1) {
//     histoName = "hResDistVsXInSL_" +
//       getHistoNameSuffix(wheel, station, sector, sl);
//     profile = (TProfile *) theFile->Get(histoName.Data());
//   }

//   static int color;
//   TCanvas *c;
//   if(!drawOptions.Contains("same")) {
//     color = 1;
//     c = newCanvas("c_"+histoName+"_X");
//     c->cd();
//     profile->SetLineColor(color);
//   } else {
//     color ++;
//     profile->SetLineColor(color);
//   }

//   profile->Draw(drawOptions.Data());
//   return profile;
// }



// TH1F * DTHistoPlotter::plotN4DSegm(int wheel, int station, int sector,
// 				   const TString& drawOptions) {
//   TString histoName = "hN4DSeg_" +
//     getHistoNameSuffix(wheel, station, sector);
//   return plotHisto(histoName, drawOptions);
// }
  





  
// TH1F * DTHistoPlotter::plotImpAngle(int wheel, int station, int sector,
// 				    const TString& drawOptions) {
//   TString histoName = "hImpAngle_" +
//     getHistoNameSuffix(wheel, station, sector);
//   return plotHisto(histoName, drawOptions);
// }


  


  
// TH2F * DTHistoPlotter::plotPosInChSegm4D(int wheel, int station, int sector,
// 					 const TString& drawOptions) {
//   TString histoName = "h4DSegmXvsYInCham_" +
//     getHistoNameSuffix(wheel, station, sector);
//   return plotHisto2D(histoName);
// }
  


// TH1F * DTHistoPlotter::plotPosXInChSegm4D(int wheel, int station, int sector,
// 					  const TString& drawOptions) {
//   TString histoName = "h4DSegmXvsYInCham_" +
//     getHistoNameSuffix(wheel, station, sector);
//   TH2F *histo = (TH2F *) theFile->Get(histoName.Data());
//   TH1F *projX = (TH1F*)histo->ProjectionX();
//     static int color;
//   TCanvas *c;
//   if(!drawOptions.Contains("same")) {
//     color = 1;
//     c = newCanvas("c_"+histoName+"_X");
//     c->cd();
//     projX->SetLineColor(color);
//   } else {
//     color ++;
//     projX->SetLineColor(color);
//   }

//   projX->Draw(drawOptions.Data());
//   return projX;
// }

// TH1F * DTHistoPlotter::plotPosYInChSegm4D(int wheel, int station, int sector,
// 					  const TString& drawOptions) {
//   TString histoName = "h4DSegmXvsYInCham_" +
//     getHistoNameSuffix(wheel, station, sector);
//   TH2F *histo = (TH2F *) theFile->Get(histoName.Data());
//   TH1F *projY = (TH1F*)histo->ProjectionY();
//     static int color;
//   TCanvas *c;
//   if(!drawOptions.Contains("same")) {
//     color = 1;
//     c = newCanvas("c_"+histoName+"_Y");
//     c->cd();
//     projY->SetLineColor(color);
//   } else {
//     color ++;
//     projY->SetLineColor(color);
//   }

//   projY->Draw(drawOptions.Data());
//   return projY;
// }
    

void DTHistoPlotter::printPDF() {
  TIter iter(gROOT->GetListOfCanvases());
  TCanvas *c;
  while( (c = (TCanvas *)iter()) ) {
    c->Print(0,"eps");
    TString command =  TString("epstopdf ") + TString(c->GetName()) + TString(".eps");
    gSystem->Exec(command.Data());
  }
}



// TString DTHistoPlotter::getHistoNameSuffix(int wheel, int station, int sector) {
//   string histoName;
//   stringstream theStream;
//   theStream << "W" <<wheel << "_St" << station << "_Sec" << sector;
//   theStream >> histoName;
//   return TString(histoName.c_str());
// }



// TString DTHistoPlotter::getHistoNameSuffix(int wheel, int station, int sector, int sl) {
//   string histoName;
//   stringstream theStream;
//   theStream << getHistoNameSuffix(wheel, station, sector) << "_SL" << sl;
//   theStream >> histoName;
//   return TString(histoName.c_str());
// }
  


// TString DTHistoPlotter::getHistoNameSuffix(int wheel, int station, int sector, int sl, int layer) {
//   string histoName;
//   stringstream theStream;
//   theStream << "Ch_" <<wheel << "_" << station << "_" << sector << "_SL" << sl << "_L" << layer << "_Wall";
//   theStream >> histoName;
//   return TString(histoName.c_str());
// }



// TString DTHistoPlotter::getHistoNameSuffix(int wheel, int station, int sector, int sl, int layer, int wire) {
//   string histoName;
//   stringstream theStream;
//   theStream << "Ch_" <<wheel << "_" << station << "_" << sector << "_SL" << sl << "_L" << layer << "_W" << wire;
//   theStream >> histoName;
//   return TString(histoName.c_str());
// }



// TH1F* DTHistoPlotter::plotHisto(const TString& histoName, const TString& drawOptions) {
//   TH1F *histo = (TH1F *) theFile->Get(histoName.Data());
//   if(histo == 0) {
//     cout << "***Error: Histogram: " << histoName << " doesn't exist!" << endl;
//     return 0;
//   }
//   static int color;
  
//   TCanvas *c;
//   if(!drawOptions.Contains("same")) {
//     color = 1;
//     c = newCanvas("c_"+histoName);
//     c->cd();
//     histo->SetLineColor(color);
//   } else {
//     color ++;
//     histo->SetLineColor(color);
//   }
//   histo->Draw(TString("h"+drawOptions).Data());

// //   if(drawOptions.Contains("fit")) {
// //     theFitter->fitTimeBox(histo);
// //   }


//   return histo;
// }




// TH2F* DTHistoPlotter::plotHisto2D(const TString& histoName, const TString& drawOptions) {
//   TH2F *histo = (TH2F *) theFile->Get(histoName.Data());
//   if(histo == 0) {
//     cout << "***Error: Histogram: " << histoName << " doesn't exist!" << endl;
//     return 0;
//   }
//   static int color;

//   TCanvas *c;
//   if(!drawOptions.Contains("same")) {
//     color = 1;
//     c = newCanvas("c_"+histoName);
//     c->cd();
//     histo->SetLineColor(color);
//   } else {
//     color ++;
//     histo->SetLineColor(color);
//   } 
//   histo->Draw(TString("h"+drawOptions).Data());
//   return histo;
// }






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

// TString DTHistoPlotter::getDirName(int wheel, int station, int sector) {
//   string dirName;
//   stringstream theStream;
//   theStream << "Wheel" <<wheel << "/Station" << station << "/Sector" << sector <<"/";
//   theStream >> dirName;
//   return TString(dirName.c_str());
// }



TCanvas *DTHistoPlotter::drawHisto(int fileIndex, TH1F *histo, const TString& drawOptions) {
  TCanvas *c = 0;
  static int color;
  stringstream str; str << "c_" << fileIndex << "_";
  TString canvPrefix(str.str().c_str());
  if(!drawOptions.Contains("same")) {
    color = 1;
    c = newCanvas(canvPrefix+TString(histo->GetName()));
    c->cd();
    histo->SetLineColor(color);
  } else {
    color ++;
    histo->SetLineColor(color);
  }
  histo->Draw(TString("h"+drawOptions).Data());
  return c;
}


TCanvas *DTHistoPlotter::drawHisto(int fileIndex, TH2F *histo, const TString& drawOptions) {
  TCanvas *c = 0;
  static int color;
  stringstream str; str << "c_" << fileIndex << "_";
  TString canvPrefix(str.str().c_str());
  if(!drawOptions.Contains("same")) {
    color = 1;
    c = newCanvas(canvPrefix+TString(histo->GetName()));
    c->cd();
    histo->SetLineColor(color);
  } else {
    color ++;
    histo->SetLineColor(color);
  }
  histo->Draw(TString("h"+drawOptions).Data());
  return c;
}




void DTHistoPlotter::addFile(int index, TFile *file) {
  files[index] = file;
}


HSegment * DTHistoPlotter::getHistoSeg(int fileN, const TString& set, const DTDetId& detId) {
  map<DTDetId, HSegment*> histoSet = histosSeg[fileN][set];
  if(histoSet.find(detId) == histoSet.end()) { // retrieve the histo and map it
    cout << "Get histo from file! " << endl;
    histosSeg[fileN][set][detId] = new HSegment(Utils::getHistoNameFromDetIdAndSet(detId, set), files[fileN]);
    histoSet = histosSeg[fileN][set];
  }
  return histoSet[detId];
}



HRes1DHits * DTHistoPlotter::getHistoRes(int fileN, const TString& set, const DTDetId& detId) {
  map<DTDetId, HRes1DHits*> histoSet = histosRes[fileN][set];
  if(histoSet.find(detId) == histoSet.end()) { // retrieve the histo and map it
    cout << "Get histo from file! " << endl;
    histosRes[fileN][set][detId] = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId, set), files[fileN]);
    histoSet = histosRes[fileN][set];
  }
  return histoSet[detId];
}


void DTHistoPlotter::fitAndDraw(int fileIndex, TH1F *histo) {
  // define the roofit objects
  RooRealVar x("x","residual",-1.,1.,"cm");
  RooRealVar mean("mean","mean",-0.3,0.3);
  RooRealVar sigma1("sigma1","sigma1",0.005,0.7);
  RooRealVar sigma2("sigma2","sigma2",0.005,0.7);

  RooRealVar frac("frac","frac",0.,1.);
  RooFormulaVar sigmaAM("sigmaAM","@0*@1+(1.-@0)*@2",RooArgList(frac,sigma1,sigma2));

  // perform the fit
  RooGaussian myg1("myg1","Gaussian distribution",x,mean,sigma1);
  RooGaussian myg2("myg2","Gaussian distribution",x,mean,sigma2);
  RooAddPdf myg("myg","myg",RooArgList(myg1,myg2),RooArgList(frac));

  RooDataHist hdata("hdata","Binned data",RooArgList(x),histo);

  RooPlot *xplot = x.frame();
  hdata.plotOn(xplot);


  double meanHisto = 0.;
  double rmsHisto = 0.;

  if(hdata.numEntries() != 0) {
  
    meanHisto = histo->GetMean();
    rmsHisto = histo->GetRMS();

    myg.fitTo(hdata,RooFit::Minos(1),RooFit::Range(meanHisto-1.5*rmsHisto,meanHisto+1.5*rmsHisto),RooFit::Save(0));
	    
    //RooPlot *xplot = x.frame();
    myg.plotOn(xplot);
    // set the statistics box
    myg.paramOn(xplot,RooFit::Layout(0.6, 1, 0.8));

  } else {
    cout << " Histo has no entries: " << hdata.numEntries() << endl;
  }
  stringstream str; str << "c_" << fileIndex << "_";
  TString canvPrefix(str.str().c_str());
  TCanvas *c = newCanvas(canvPrefix+TString(histo->GetName()));
  // write interesting values to tree
  xplot->SetTitle(histo->GetName());
  c->cd();
  xplot->Draw();
  cout << " MEAN: " << meanHisto << " RMS: " << rmsHisto << endl;
}



void DTHistoPlotter::fitAllInSet(const TString& set, const TString& options) {


  double ttrig = 0.;
  double res_mean = 0.;
  double res_mean_err = 0.;
  double res_sigma1 = 0.;
  double res_sigma2 = 0.;
  double t0seg = 0;
  double chi2 = 0.;
  int theWheel = 0;
  int theStation = 0;
  int theSector = 0;
  int theSL = 0;

  TTree res_tree("res_tree","res_tree");


  res_tree.Branch("ttrig",&ttrig,"ttrig/D");
  res_tree.Branch("wheel",&theWheel,"theWheel/I");
  res_tree.Branch("station",&theStation,"theStation/I");
  res_tree.Branch("sector",&theSector,"theSector/I");
  res_tree.Branch("sl",&theSL,"theSL/I");
  res_tree.Branch("res_mean",&res_mean,"res_mean/D");
  res_tree.Branch("res_mean_err",&res_mean_err,"res_mean_err/D");

//   res_tree.Branch("res_sigma",&res_sigma,"res_sigma/D");
  res_tree.Branch("res_sigma1",&res_sigma1,"res_sigma1/D");
  res_tree.Branch("res_sigma2",&res_sigma2,"res_sigma2/D"); 
  res_tree.Branch("t0seg",&t0seg,"t0seg/D");
  res_tree.Branch("chi2",&chi2,"chi2/D");

  
  // define the roofit objects
  RooRealVar x("x","residual",-1.,1.,"cm");

  RooRealVar mean("mean","mean",-0.3,0.3);

  RooRealVar sigma1("sigma1","sigma1",0.005,0.7);
  RooRealVar sigma2("sigma2","sigma2",0.005,0.7);

  RooRealVar frac("frac","frac",0.,1.);


  RooFormulaVar sigmaAM("sigmaAM","@0*@1+(1.-@0)*@2",RooArgList(frac,sigma1,sigma2));


  TCanvas *c = newCanvas("test");
  c->Draw();
  TString filePdfName = "/data/c/cerminar/data/DTAnalysis/DTCalibration/residualFits_" + set + ".ps";

  int count = 0;
  for(map<int, TFile*>::const_iterator file = files.begin();
      file != files.end(); ++file) {  // loop over the files
    ttrig = (double)(*file).first;
    for(int wheel = -2; wheel != 3; ++wheel) {   // loop over wheels
      theWheel = wheel;
      for(int station = 1; station != 5; ++station) { // loop over stations
	theStation = station;
	for(int sector = 1; sector != 15; ++sector) { // loop over sectors
	  if(station != 4 && (sector == 13 || sector == 14)) continue;
	  theSector = sector;	  
	  DTDetId chId(wheel, station, sector, 0, 0, 0);
	  HSegment *hSeg = getHistoSeg((*file).first, set, chId);
	  TH1F *ht0 = 0; //hSeg->ht0Phi; //FIXME to be updated
	  t0seg = computeHistoMedian(ht0);
	  for(int sl = 1; sl != 4; ++sl) { // loop over SLs
	    if(station == 4 && sl == 2) continue;
	    theSL = sl;

	    DTDetId detId(wheel, station, sector, sl, 0, 0);


	    HRes1DHits *hRes = getHistoRes((*file).first, set, detId);
	    TH1F *histo = 0;
	    if(options.Contains("central")) {
	      histo = (TH1F*)hRes->hResDistVsDist->ProjectionY(hRes->hResDist->GetName(),20,80);
	    } else {
	      histo = hRes->hResDist;
	    }

	    if(histo == 0) {
	      cout << " Histo is a null pointer!" << endl;
	      continue;
	    }

	    


	    // perform the fit
	    RooGaussian myg1("myg1","Gaussian distribution",x,mean,sigma1);
	    RooGaussian myg2("myg2","Gaussian distribution",x,mean,sigma2);
 	    RooAddPdf myg("myg","myg",RooArgList(myg1,myg2),RooArgList(frac));

	    RooDataHist hdata("hdata","Binned data",RooArgList(x),histo);
	    RooPlot xplot(x,x.getMin(),x.getMax(),x.getBins());
	    hdata.plotOn(&xplot);
	    
	    double meanHisto = 0.;
	    double rmsHisto = 0.;

	    if(hdata.numEntries() != 0) {
	      meanHisto = histo->GetMean();
	      rmsHisto = histo->GetRMS();

	      myg.fitTo(hdata,RooFit::Minos(1),RooFit::Range(meanHisto-1.5*rmsHisto,meanHisto+1.5*rmsHisto),
			RooFit::Save(0));

	      res_mean = mean.getVal();
	      res_mean_err = mean.getError();
	      res_sigma1 = sigma1.getVal();
	      res_sigma2 = sigma2.getVal();

	    
	      //RooPlot *xplot = x.frame();
	      myg.plotOn(&xplot);
	      // set the statistics box
	      myg.paramOn(&xplot,RooFit::Layout(0.6, 1, 0.8));
	      chi2 = xplot.chiSquare();
	    
	    } else {
	      cout << " Histo has no entries: " << hdata.numEntries() << endl;
	      res_mean = 0.;
	      res_mean_err = 0.;
	      res_sigma1 = 0.;
	      res_sigma2 = 0.;
	      chi2 = 0;
	    }

	    // give a name to the plot
  	    stringstream str; str << "c_" << (*file).first << "_";
 	    TString canvPrefix(str.str().c_str());
	    TString canvName = canvPrefix + TString(histo->GetName());
	    xplot.SetTitle(canvName.Data());

	    // write interesting values to tree
 	    res_tree.Fill();
 	    c->cd();
   	    xplot.Draw();
	    TString psName1 = filePdfName + "(";
	    if(count == 0) c->SaveAs(psName1.Data());
	    else c->SaveAs(filePdfName.Data());
	    count++;
	//     cout << "T0 seg: " << t0seg << endl;
// 	    int pippo;
// 	    cin >> pippo;
// 	    if(pippo == 2) goto end;
	    c->Clear();
	    delete hRes;
	    if(options.Contains("central")) delete histo;
	  }
	  delete hSeg;
	}
      }
    }
  }
  
  // close the ps file
  TString psName2 = filePdfName + ")";
  c->SaveAs(psName2.Data());


  // write the tree to file
  TString fileName = "/data/c/cerminar/data/DTAnalysis/DTCalibration/residualFits_" + set + ".root";
  TFile out(fileName.Data(),"RECREATE");
  out.cd();
  res_tree.Write();
  out.Close();

}


double DTHistoPlotter::computeHistoMedian(TH1F * histo) {
  // Get the x axis
//   TAxis * ax = histo->GetXaxis();
  // Get the number of bins
  const int nBins = histo->GetNbinsX();

  double cont[nBins];
  double x[nBins];

  // Loop over all the bins
  for (int bin=0; bin<=nBins+1; bin++){
    x[bin] = histo->GetBinCenter(bin);
    cont[bin] = histo->GetBinContent(bin);
  }

  return  TMath::Median(nBins, x, cont);
}

