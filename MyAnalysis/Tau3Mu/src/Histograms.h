#ifndef Histograms_H
#define Histograms_H

#ifndef ROOTANALYSIS
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#endif

#include "TH1F.h"
#include "TH2F.h"
#include "TGraphAsymmErrors.h"

#include <iostream>
using namespace std; 

class HistoKin {
public:

#ifndef ROOTANALYSIS
  HistoKin(std::string name, TFileService& fs) : theName(name) {
    hPt     = fs.make<TH1F>(theName+"_hPt","Transv. Momentum; P_{T} (GeV/c^{2}); # events",100,0,50);
    hEta    = fs.make<TH1F>(theName+"_hEta","Pseudo rapidity; #eta; # events",50,-5,5);
    hPhi    = fs.make<TH1F>(theName+"_hPhi","Phi; #phi (rad); # events",100,0,6.28);
    hMass   = fs.make<TH1F>(theName+"_hMass","Mass; Mass (GeV/c^{2}); # events",100,0,10);
    hPtEta  = fs.make<TH2F>(theName+"_hPtEta","Pt vs Eta; #eta; p_{T} (GeV/c^{2})",50,-5,5,100,0,50);  
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
    hPtEta  = new TH2F(theName+"_hPtEta","Pt vs Eta",50,-5,5,100,0,50);  
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
    hPtEta = 0;
    hNObj = 0;
  }



  HistoKin(std::string name, std::string dir, TFile *file) : theName(name) {
    if(dir != "") {
      dir = dir + "/";
    }

    hPt = (TH1F *) file->Get(TString(dir) + theName+"_hPt");
    hEta = (TH1F *) file->Get(TString(dir) + theName+"_hEta");
    hPhi = (TH1F *) file->Get(TString(dir) + theName+"_hPhi");
    hPtEta = (TH2F *) file->Get(TString(dir) + theName+"_hPtEta");
    hMass = (TH1F *) file->Get(TString(dir) + theName+"_hMass");
    hNObj = (TH1F *) file->Get(TString(dir) + theName+"_hNObj");

  }


  HistoKin * Clone(std::string name) {
    HistoKin *ret = new HistoKin();
    ret->theName = name;

    if(hPt != 0) hPt->Clone((ret->theName+"_hPt").Data());
    if(hEta != 0) hEta->Clone((ret->theName+"_hEta").Data());
    if(hPhi != 0) hPhi->Clone((ret->theName+"_hPhi").Data());
    if(hPtEta != 0) hPtEta->Clone((ret->theName+"_hPtEta").Data());
    if(hMass != 0) hPhi->Clone((ret->theName+"_hMass").Data());
    if(hNObj != 0) hNObj->Clone((ret->theName+"_hNObj").Data());

    return ret;
  }



  void Add(const HistoKin* histSet) {
    if(hPt != 0) hPt->Add(histSet->hPt);
    if(hEta != 0) hEta->Add(histSet->hEta);
    if(hPhi != 0) hPhi->Add(histSet->hPhi);
    if(hPtEta != 0) hPtEta->Add(histSet->hPtEta);
    if(hMass != 0) hPhi->Add(histSet->hMass);
    if(hNObj != 0) hPhi->Add(histSet->hNObj);

  }



  void Scale(double scaleFact) {
    if(hPt != 0) hPt->Scale(scaleFact);
    if(hEta != 0) hEta->Scale(scaleFact);
    if(hPhi != 0) hPhi->Scale(scaleFact);
    if(hPtEta != 0) hPtEta->Scale(scaleFact);
    if(hMass != 0) hMass->Scale(scaleFact);
    if(hNObj != 0) hNObj->Scale(scaleFact);

  }


  void Write() {
    if(hPt != 0) hPt->Write();
    if(hEta != 0) hEta->Write();
    if(hPhi != 0) hPhi->Write();
    if(hPtEta != 0) hPtEta->Write();
    if(hMass != 0) hMass->Write();
    if(hNObj != 0) hNObj->Write();

  }
  
  void Fill(double pt, double eta, double phi, double mass, double weight) {
    hPt->Fill(pt, weight);
    hEta->Fill(eta, weight);
    hPhi->Fill(phi, weight);
    hPtEta->Fill(eta,pt,weight);
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
  TH2F *hPtEta;
  TH1F *hMass;
  TH1F *hNObj;
};









class HistoKinPair {
public:

#ifndef ROOTANALYSIS
  HistoKinPair(std::string name, float massMin, float massMax, TFileService& fs) : theName(name) {
    hPt1VsPt2     = fs.make<TH2F>(theName+"_hPt1VsPt2","Transv. Momentum; P^{1}_{T} (GeV); P^{2}_{T} ",100,0,50, 100,0,50);
    hDEta    = fs.make<TH1F>(theName+"_hDEta","Delta #eta; #Delta #eta; #events",50,0,5);
    hDPhi    = fs.make<TH1F>(theName+"_hDPhi","Delta #phi; #Delta #phi (rad); # events",100,0,3.14);
    hDPhiVsDEta = fs.make<TH2F>(theName+"_hDPhiVsDEta","Delta #phi vs Delta #eta; #Delta #eta; #Delta #phi (rad)",50,0,5 ,100,0,3.14);
    hDR    = fs.make<TH1F>(theName+"_hDR","Delta R; #Delta R; # events",100,0,6.28);
    hMass   = fs.make<TH1F>(theName+"_hMass","Mass (GeV)",200,massMin, massMax);
    hPt1VsPt2->Sumw2();
    hDEta->Sumw2();
    hDPhi->Sumw2();
    hDR->Sumw2();
    hMass->Sumw2();
  }

#endif
  
  


  HistoKinPair() : theName("") {
    hPt1VsPt2=0;
    hDEta=0;
    hDPhi=0;
    hDPhiVsDEta=0;
    hDR=0;
    hMass=0;

  }



  HistoKinPair(std::string name, std::string dir, TFile *file) : theName(name) {
    if(dir != "") {
      dir = dir + "/";
    }

    hPt1VsPt2   = (TH2F *) file->Get(dir + theName+"_hPt1VsPt2");
    hDEta       = (TH1F *) file->Get(dir + theName+"_hDEta");
    hDPhi       = (TH1F *) file->Get(dir + theName+"_hDPhi");
    hDPhiVsDEta = (TH2F *) file->Get(dir + theName+"_hDPhiVsDEta");
    hDR         = (TH1F *) file->Get(dir + theName+"_hDR");
    hMass       = (TH1F *) file->Get(dir + theName+"_hMass");


  }


//   HistoKinPair * Clone(std::string name) {
//     HistoKinPair *ret = new HistoKinPair();
//     ret->theName = name;

//     if(hPt != 0) hPt->Clone((ret->theName+"_hPt").Data());
//     if(hEta != 0) hEta->Clone((ret->theName+"_hEta").Data());
//     if(hPhi != 0) hPhi->Clone((ret->theName+"_hPhi").Data());
//     if(hMass != 0) hPhi->Clone((ret->theName+"_hMass").Data());
//     if(hNObj != 0) hNObj->Clone((ret->theName+"_hNObj").Data());

//     return ret;
//   }



//   void Add(const HistoKinPair* histSet) {
//     if(hPt != 0) hPt->Add(histSet->hPt);
//     if(hEta != 0) hEta->Add(histSet->hEta);
//     if(hPhi != 0) hPhi->Add(histSet->hPhi);
//     if(hMass != 0) hPhi->Add(histSet->hMass);
//     if(hNObj != 0) hPhi->Add(histSet->hNObj);

//   }



//   void Scale(double scaleFact) {
//     if(hPt != 0) hPt->Scale(scaleFact);
//     if(hEta != 0) hEta->Scale(scaleFact);
//     if(hPhi != 0) hPhi->Scale(scaleFact);
//     if(hMass != 0) hMass->Scale(scaleFact);
//     if(hNObj != 0) hNObj->Scale(scaleFact);

//   }


//   void Write() {
//     if(hPt != 0) hPt->Write();
//     if(hEta != 0) hEta->Write();
//     if(hPhi != 0) hPhi->Write();
//     if(hMass != 0) hMass->Write();
//     if(hNObj != 0) hNObj->Write();

//   }
  
  void Fill(double pt1, double pt2, double deltaPhi, double deltaEta, double deltaR, double mass, double weight) {
    hPt1VsPt2->Fill(pt2, pt1, weight);
    hDEta->Fill(deltaEta, weight);
    hDPhi->Fill(deltaPhi, weight);
    hDPhiVsDEta->Fill(deltaEta, deltaPhi, weight);
    hDR->Fill(deltaR, weight);
    hMass->Fill(mass, weight);
  }

  /// Destructor
  virtual ~HistoKinPair() {}

  // Operations
  TString theName;

  TH2F *hPt1VsPt2;
  TH1F *hDEta;
  TH1F *hDPhi;
  TH2F *hDPhiVsDEta;
  TH1F *hDR;
  TH1F *hMass;

};






class HistoImpactParam {
public:

#ifndef ROOTANALYSIS
  HistoImpactParam(std::string name, TFileService& fs) : theName(name) {
    hD0 = fs.make<TH1F>(theName+"_hD0","D0;d0 (cm);#events", 1000, 0, 1);
    hD0Err = fs.make<TH1F>(theName+"_hD0Err","D0;d0 (cm);#events", 100, 0, 0.1);
    hD0Sig = fs.make<TH1F>(theName+"_hD0Sig","D0;d0 (cm);#events", 1000, 0, 100);
  }

#endif
  
  


  HistoImpactParam() : theName("") {
    hD0 = 0;
    hD0Err = 0;
    hD0Sig = 0;
  }



  HistoImpactParam(std::string name, std::string dir, TFile *file) : theName(name) {
    if(dir != "") {
      dir = dir + "/";
    }

    hD0          = (TH1F *) file->Get(dir + theName+"_hD0");
    hD0Err       = (TH1F *) file->Get(dir + theName+"_hD0Err");
    hD0Sig       = (TH1F *) file->Get(dir + theName+"_hD0Sig");
  }


//   HistoImpactParam * Clone(std::string name) {
//     HistoImpactParam *ret = new HistoImpactParam();
//     ret->theName = name;

//     if(hPt != 0) hPt->Clone((ret->theName+"_hPt").Data());
//     if(hEta != 0) hEta->Clone((ret->theName+"_hEta").Data());
//     if(hPhi != 0) hPhi->Clone((ret->theName+"_hPhi").Data());
//     if(hMass != 0) hPhi->Clone((ret->theName+"_hMass").Data());
//     if(hNObj != 0) hNObj->Clone((ret->theName+"_hNObj").Data());

//     return ret;
//   }



//   void Add(const HistoImpactParam* histSet) {
//     if(hPt != 0) hPt->Add(histSet->hPt);
//     if(hEta != 0) hEta->Add(histSet->hEta);
//     if(hPhi != 0) hPhi->Add(histSet->hPhi);
//     if(hMass != 0) hPhi->Add(histSet->hMass);
//     if(hNObj != 0) hPhi->Add(histSet->hNObj);

//   }



//   void Scale(double scaleFact) {
//     if(hPt != 0) hPt->Scale(scaleFact);
//     if(hEta != 0) hEta->Scale(scaleFact);
//     if(hPhi != 0) hPhi->Scale(scaleFact);
//     if(hMass != 0) hMass->Scale(scaleFact);
//     if(hNObj != 0) hNObj->Scale(scaleFact);

//   }


//   void Write() {
//     if(hPt != 0) hPt->Write();
//     if(hEta != 0) hEta->Write();
//     if(hPhi != 0) hPhi->Write();
//     if(hMass != 0) hMass->Write();
//     if(hNObj != 0) hNObj->Write();

//   }
  
  void Fill(double d0, double d0Err, double weight) {
    hD0->Fill(d0, weight);
    hD0Err->Fill(d0Err, weight);
    hD0Sig->Fill(d0/d0Err, weight);
  }

  /// Destructor
  virtual ~HistoImpactParam() {}

  // Operations
  TString theName;

  TH1F *hD0;
  TH1F *hD0Err;
  TH1F *hD0Sig;

};




#endif


