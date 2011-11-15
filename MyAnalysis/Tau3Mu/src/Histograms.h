#ifndef Histograms_H
#define Histograms_H

#ifndef ROOTANALYSIS
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#endif


#include <iostream>
using namespace std; 

class HistoKin {
public:

#ifndef ROOTANALYSIS
  HistoKin(std::string name, TFileService& fs) : theName(name) {
    hPt     = fs.make<TH1F>(theName+"_hPt","Transv. Momentum; Pt (GeV); # events",100,0,200);
    hEta    = fs.make<TH1F>(theName+"_hEta","Eta",50,-5,5);
    hPhi    = fs.make<TH1F>(theName+"_hPhi","Phi (rad)",100,0,6.28);
    hMass   = fs.make<TH1F>(theName+"_hMass","Mass (GeV)",200,0,500);
    hNObj   = fs.make<TH1F>(theName+"_hNObj","# objects", 50,0,50);
    hPt->Sumw2();
    hEta->Sumw2();
    hPhi->Sumw2();
    hMass->Sumw2();
  }

#endif
  
  
  HistoKin(std::string name) : theName(name) {
    hPt = new TH1F(theName+"_hPt","Pt (GeV)",100,0,200);
    hEta = new TH1F(theName+"_hEta","Eta",50,-5,5);
    hPhi = new TH1F(theName+"_hPhi","Phi (rad)",100,0,6.28);
    hMass = new TH1F(theName+"_hMass","Mass (GeV)",200,0,500);
    hNObj = new TH1F(theName+"_hNObj","# objects", 50,0,50);
    hPt->Sumw2();
    hEta->Sumw2();
    hPhi->Sumw2();
    hMass->Sumw2();
    hNObj->Sumw2();
  }





  HistoKin() : theName("") {
    hPt = 0;
    hEta = 0;
    hPhi = 0;
    hMass = 0;
    hNObj = 0;
  }



  HistoKin(std::string name, std::string dir, TFile *file) : theName(name) {
    file->cd(dir.c_str());
    
    hPt = (TH1F *) file->Get(theName+"_hPt");
    hEta = (TH1F *) file->Get(theName+"_hEta");
    hPhi = (TH1F *) file->Get(theName+"_hPhi");
    hMass = (TH1F *) file->Get(theName+"_hMass");
    hNObj = (TH1F *) file->Get(theName+"_hNObj");

  }


  HistoKin * Clone(std::string name) {
    HistoKin *ret = new HistoKin();
    ret->theName = name;

    if(hPt != 0) hPt->Clone((ret->theName+"_hPt").Data());
    if(hEta != 0) hEta->Clone((ret->theName+"_hEta").Data());
    if(hPhi != 0) hPhi->Clone((ret->theName+"_hPhi").Data());
    if(hMass != 0) hPhi->Clone((ret->theName+"_hMass").Data());
    if(hNObj != 0) hNObj->Clone((ret->theName+"_hNObj").Data());

    return ret;
  }



  void Add(const HistoKin* histSet) {
    if(hPt != 0) hPt->Add(histSet->hPt);
    if(hEta != 0) hEta->Add(histSet->hEta);
    if(hPhi != 0) hPhi->Add(histSet->hPhi);
    if(hMass != 0) hPhi->Add(histSet->hMass);
    if(hNObj != 0) hPhi->Add(histSet->hNObj);

  }



  void Scale(double scaleFact) {
    if(hPt != 0) hPt->Scale(scaleFact);
    if(hEta != 0) hEta->Scale(scaleFact);
    if(hPhi != 0) hPhi->Scale(scaleFact);
    if(hMass != 0) hMass->Scale(scaleFact);
    if(hNObj != 0) hNObj->Scale(scaleFact);

  }


  void Write() {
    if(hPt != 0) hPt->Write();
    if(hEta != 0) hEta->Write();
    if(hPhi != 0) hPhi->Write();
    if(hMass != 0) hMass->Write();
    if(hNObj != 0) hNObj->Write();

  }
  
  void Fill(double pt, double eta, double phi, double mass, double weight) {
    hPt->Fill(pt, weight);
    hEta->Fill(eta, weight);
    hPhi->Fill(phi, weight);
    hMass->Fill(mass, weight);
  }

  void FillNObj(int nObj, double weight) {
    hNObj->Fill(nObj, weight);
  }
  /// Destructor
  virtual ~HistoKin() {}

  // Operations
  TString theName;

  TH1F *hPt;
  TH1F *hEta;
  TH1F *hPhi;
  TH1F *hMass;
  TH1F *hNObj;
};


#endif
