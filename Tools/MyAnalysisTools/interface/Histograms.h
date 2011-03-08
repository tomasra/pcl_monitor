#ifndef Histograms_H
#define Histograms_H

/** \class Histograms
 *  No description available.
 *
 *  $Date: $
 *  $Revision: $
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
    hPt = new TH1F(theName+"_hPt","Track Jet Pt (GeV)",100,0,100);
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
    
  }


  HistoLept() : theName("") {
    hKin = 0;
  }



  HistoLept(std::string name, TFile *file) : theName(name) {
    hKin = new HistoKin(name, file);
//     hPt = hKin->hPt;
//     hEta = hKin->hEta;
//     hPhi = hKin->hPhi
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
    hKin->Add(histSet->hKin);

//     if(hPt != 0) hPt->Add(histSet->hPt);
//     if(hEta != 0) hEta->Add(histSet->hEta);
//     if(hPhi != 0) hPhi->Add(histSet->hPhi);
  }



  void Scale(double scaleFact) {
    hKin->Scale(scaleFact);
  }


  void Write() {
    hKin->Write();
  }
  
  void Fill(double pt, double eta, double phi, double weight) {
    hKin->Fill(pt, eta, phi, weight);
  }

  /// Destructor
  virtual ~HistoLept() {}

  // Operations
  TString theName;

  HistoKin *hKin;

};

#endif
