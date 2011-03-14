#ifndef Histograms_H
#define Histograms_H

/** \class Histograms
 *  No description available.
 *
 *  $Date: 2011/03/08 15:14:56 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - CERN
 */


#include <string>
#include <vector>
#include <iostream>

#include "TFile.h"
#include "TH1F.h"
#include "TH2F.h"
// #include "TProfile.h"
#include "TString.h"
#include "TMath.h"

using namespace std;


class HistoKin {
public:
  HistoKin(std::string name) : theName(name) {
    hPt = new TH1F(theName+"_hPt","Track Jet Pt (GeV)",100,0,200);
    hEta = new TH1F(theName+"_hEta","Track Jet Eta",50,-5,5);
    hPhi = new TH1F(theName+"_hPhi","track Jet Phi (rad)",100,0,6.28);
    hPt->Sumw2();
    hEta->Sumw2();
    hPhi->Sumw2();
  }


  HistoKin() : theName("") {
    hPt = 0;
    hEta = 0;
    hPhi = 0;
  }



  HistoKin(std::string name, TFile *file) : theName(name) {
    hPt = (TH1F *) file->Get(theName+"_hPt");
    hEta = (TH1F *) file->Get(theName+"_hEta");
    hPhi = (TH1F *) file->Get(theName+"_hPhi");
  }


  HistoKin * Clone(std::string name) {
    HistoKin *ret = new HistoKin();
    ret->theName = name;

    if(hPt != 0) hPt->Clone((ret->theName+"_hPt").Data());
    if(hEta != 0) hEta->Clone((ret->theName+"_hEta").Data());
    if(hPhi != 0) hPhi->Clone((ret->theName+"_hPhi").Data());

    return ret;
  }



  void Add(const HistoKin* histSet) {
    if(hPt != 0) hPt->Add(histSet->hPt);
    if(hEta != 0) hEta->Add(histSet->hEta);
    if(hPhi != 0) hPhi->Add(histSet->hPhi);
  }



  void Scale(double scaleFact) {
    if(hPt != 0) hPt->Scale(scaleFact);
    if(hEta != 0) hEta->Scale(scaleFact);
    if(hPhi != 0) hPhi->Scale(scaleFact);
  }


  void Write() {
    if(hPt != 0) hPt->Write();
    if(hEta != 0) hEta->Write();
    if(hPhi != 0) hPhi->Write();
  }
  
  void Fill(double pt, double eta, double phi, double weight) {
    hPt->Fill(pt, weight);
    hEta->Fill(eta, weight);
    hPhi->Fill(phi, weight);
  }

  /// Destructor
  virtual ~HistoKin() {}

  // Operations
  TString theName;

  TH1F *hPt;
  TH1F *hEta;
  TH1F *hPhi;

};




class HistoLept {
public:
  HistoLept(std::string name) : theName(name) {
    hKin = new HistoKin(name);
    hRelIso    = new TH1F(theName+"_hRelIso","Relative isolation",100,0,2);
    hDxy       = new TH1F(theName+"_hDxy","#Delta_{xy}",100,0,1);
    hDz        = new TH1F(theName+"_hDz","#Delta_{z}",100,-10,10);
    hType      = new TH1F(theName+"_hType","Muon type",3,0,3);
    hNLept     = new TH1F(theName+"_hNLept","# of leptons",10,0,10);
    hNPixelHits = new TH1F(theName+"_hNPixelHits","pippo",10,0,10);
    hNTkHits    = new TH1F(theName+"_hNTkHits","titolo",40,0,40);
    hNMuonHits  = new TH1F(theName+"_hNMuonHits","titolo",60,0,60);
    hNMatches  = new TH1F(theName+"_hNMatches","titolo",15,0,15);

 


    hRelIso->Sumw2();
    hDxy->Sumw2();
    hDz->Sumw2();
    hType->Sumw2();
    hNLept->Sumw2();
    hNPixelHits->Sumw2();
    hNTkHits->Sumw2();
    hNMuonHits->Sumw2();
    hNMatches->Sumw2();

 }


  HistoLept() : theName("") {
    hKin = 0;
    hRelIso = 0;
    hDxy = 0;
    hDz = 0;
    hType = 0;
    hNLept = 0;
    hNPixelHits = 0;
    hNTkHits = 0;
    hNMuonHits = 0;
    hNMatches = 0;



  }


  HistoLept(std::string name, TFile *file) : theName(name) {
    hKin       = new HistoKin(name, file);
    hPt        = hKin->hPt;
    hEta       = hKin->hEta;
    hPhi       = hKin->hPhi;
    hRelIso    = (TH1F *) file->Get(theName+"_hRelIso");
    hDxy       = (TH1F *) file->Get(theName+"_hDxy");
    hDz        = (TH1F *) file->Get(theName+"_hDz");
    hType      = (TH1F *) file->Get(theName+"_hType");
    hNLept     = (TH1F *) file->Get(theName+"_hNLept");
    hNPixelHits = (TH1F *) file->Get(theName+"_hNPixelHits");
    hNTkHits    = (TH1F *) file->Get(theName+"_hNTkHits");
    hNMuonHits  = (TH1F *) file->Get(theName+"_hNMuonHits");
    hNMatches   = (TH1F *) file->Get(theName+"_hNMatches");



 }


//   HistoLept * Clone(std::string name) {
//     HistoLept *ret = new HistoLept();
//     ret->theName = name;
//     hKin
//     if(hPt != 0) hPt->Clone((ret->theName+"_hPt").Data());
//     if(hEta != 0) hEta->Clone((ret->theName+"_hEta").Data());
//     if(hPhi != 0) hPhi->Clone((ret->theName+"_hPhi").Data());

//     return ret;
//   }



  void Add(const HistoLept* histSet) {
    if(hKin != 0) hKin->Add(histSet->hKin);
    if(hRelIso != 0) hRelIso->Add(histSet->hRelIso);
    if(hDxy != 0) hDxy->Add(histSet->hDxy);
    if(hDz != 0) hDz->Add(histSet->hDz);
    if(hType != 0) hType->Add(histSet->hType);
    if(hNLept != 0) hNLept->Add(histSet->hNLept);
    if(hNPixelHits != 0) hNPixelHits->Add(histSet->hNPixelHits);
    if(hNTkHits != 0) hNTkHits->Add(histSet->hNTkHits);
    if(hNMuonHits != 0) hNMuonHits->Add(histSet->hNMuonHits);
    if(hNMatches != 0) hNMatches->Add(histSet->hNMatches);


//     if(hPt != 0) hPt->Add(histSet->hPt);
//     if(hEta != 0) hEta->Add(histSet->hEta);
//     if(hPhi != 0) hPhi->Add(histSet->hPhi);
  }



  void Scale(double scaleFact) {
    if(hKin != 0) hKin->Scale(scaleFact);
    if(hRelIso != 0) hRelIso->Scale(scaleFact);
    if(hDxy != 0) hDxy->Scale(scaleFact);
    if(hDz != 0) hDz->Scale(scaleFact);
    if(hType != 0) hType->Scale(scaleFact);
    if(hNLept != 0) hNLept->Scale(scaleFact);
    if(hNPixelHits != 0) hNPixelHits->Scale(scaleFact);
    if(hNTkHits != 0) hNTkHits->Scale(scaleFact);
    if(hNMuonHits != 0) hNMuonHits->Scale(scaleFact);
    if(hNMatches != 0) hNMatches->Scale(scaleFact);


  }


  void Write() {
    if(hKin != 0) hKin->Write();
    if(hRelIso != 0) hRelIso->Write();
    if(hDxy != 0) hDxy->Write();
    if(hDz != 0) hDz->Write();
    if(hType != 0) hType->Write();
    if(hNLept != 0) hNLept->Write();
    if(hNPixelHits != 0) hNPixelHits->Write();
    if(hNTkHits != 0) hNTkHits->Write();
    if(hNMuonHits != 0) hNMuonHits->Write();
    if(hNMatches != 0) hNMatches->Write();


 }
  
  void Fill(double pt, double eta, double phi,
	    double relIso,
	    double dxy, double dz,
	    double type,
	    double nPxhits, double nTkhits, double nMuonHits, double nMatches,
	    double weight) {
    hKin->Fill(pt, eta, phi, weight);
    hRelIso->Fill(relIso,weight);
    hDxy->Fill(dxy,weight);
    hDz->Fill(dz, weight);
    hType->Fill(type, weight);
    hNPixelHits->Fill(nPxhits, weight);
    hNTkHits->Fill(nTkhits, weight);
    hNMuonHits->Fill(nMuonHits, weight);
    hNMatches->Fill(nMatches, weight);


  }

  void FillNLept(int num, int weight) {
    hNLept->Fill(num, weight);
  }

  /// Destructor
  virtual ~HistoLept() {}

  // Operations
  TString theName;

  HistoKin *hKin;
  TH1F *hPt;
  TH1F *hEta;
  TH1F *hPhi;

  TH1F *hRelIso;
  TH1F *hDxy;
  TH1F *hDz;
  TH1F *hType;
  TH1F *hNLept;
  TH1F *hNPixelHits;
  TH1F *hNTkHits;
  TH1F *hNMuonHits;
  TH1F *hNMatches;



};

#endif
