#ifndef Histograms_H
#define Histograms_H

/** \class Histograms
 *  No description available.
 *
 *  $Date: 2011/03/14 18:05:18 $
 *  $Revision: 1.2 $
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

#ifndef ROOTANALYSIS
#include "CMGTools/HtoZZ2l2nu/interface/Utils.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#endif

using namespace std;


class HistoKin {
public:
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



  HistoKin(std::string name, TFile *file) : theName(name) {
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




class HistoLept {
public:
  HistoLept(std::string name) : theName(name) {
    hKin = new HistoKin(name);
    hRelIso    = new TH1F(theName+"_hRelIso","Relative isolation",100,0,1);
    hDxy       = new TH1F(theName+"_hDxy","#Delta_{xy}",100,0,1);
    hDz        = new TH1F(theName+"_hDz","#Delta_{z}",100,-10,10);
    hType      = new TH1F(theName+"_hType","Muon type",3,0,3);
    hNLept     = new TH1F(theName+"_hNLept","# of leptons",10,0,10);
    hNPixelHits = new TH1F(theName+"_hNPixelHits","# pixel hits",10,0,10);
    hNTkHits    = new TH1F(theName+"_hNTkHits","# Tk hits",40,0,40);
    hNMuonHits  = new TH1F(theName+"_hNMuonHits","# mu hits",60,0,60);
    hNMatches  = new TH1F(theName+"_hNMatches","# matches",15,0,15);


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
    hMass      = hKin->hMass;
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
  
  
#ifndef ROOTANALYSIS
  void Fill(const pat::Muon * muon, const reco::Vertex *vtx, double weight) {
    
    double relIso = Utils::computeRelIsolation(muon);
    int type  = Utils::muonType(muon);
    reco::TrackRef muonTrack = muon->innerTrack();
    double dz = muonTrack->dz(vtx->position());
    double dxy = muonTrack->dxy(vtx->position());

    Fill(muon->pt(), muon->eta(), muon->phi(),
	 relIso,
	 dz, dxy,
	 type,
	 muonTrack->hitPattern().numberOfValidPixelHits(),
	 muonTrack->hitPattern().numberOfValidTrackerHits(),
	 muonTrack->hitPattern().numberOfValidMuonHits(),
	 muon->numberOfMatches(),
	 weight);

  }

#endif


  void Fill(double pt, double eta, double phi,
	    double relIso,
	    double dxy, double dz,
	    double type,
	    double nPxhits, double nTkhits, double nMuonHits, double nMatches,
	    double weight) {
    hKin->Fill(pt, eta, phi, 1, weight);
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
  TH1F *hMass;

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


class HistoRedMET {
public:
  HistoRedMET(std::string name) : theName(name) {
    hRedMET = new TH1F(theName+ "_hRedMET","title",100,0,150);
    hRedMETCompLong = new TH1F(theName+ "_hRedMETCompLong","title",150,0,150);
    hRedMETCompPerp = new TH1F(theName+ "_hRedMETCompPerp","title",150,0,150);
    hRecoilCompLong = new TH1F(theName+ "_hRecoilCompLong","title",150,-150,150);
    hRecoilCompPerp = new TH1F(theName+ "_hRecoilCompPerp","title",150,-150,150);
    hMetCompLong = new TH1F(theName+ "_hMetCompLong","title",150,-150,150);
    hMetCompPerp = new TH1F(theName+ "_hMetCompPerp","title",150,-150,150);
    hSumJetCompLong = new TH1F(theName+ "_hSumJetCompLong","title",150,-150,150);
    hSumJetCompPerp = new TH1F(theName+ "_hSumJetCompPerp","title",150,-150,150);
    hDileptonCompLong = new TH1F(theName+ "_hDileptonCompLong","title",150,0,150);
    hDileptonCompPerp = new TH1F(theName+ "_hDileptonCompPerp","title",150,0,150);
    hRecoilTypeLong = new TH1F(theName+ "_hRecoilTypeLong","Type",2,0,2);
    hRecoilTypeLong->SetBinLabel(1,"Jet-Like");
    hRecoilTypeLong->SetBinLabel(2,"MET-Like");
    hRecoilTypePerp = new TH1F(theName+ "_hRecoilTypePerp","Type",2,0,2);
    hRecoilTypePerp->SetBinLabel(1,"Jet-Like");
    hRecoilTypePerp->SetBinLabel(2,"MET-Like");


    hRedMET->Sumw2();
    hRedMETCompLong->Sumw2();
    hRedMETCompPerp->Sumw2();
    hRecoilCompLong->Sumw2();
    hRecoilCompPerp->Sumw2();
    hMetCompLong->Sumw2();
    hMetCompPerp->Sumw2();
    hSumJetCompLong->Sumw2();
    hSumJetCompPerp->Sumw2();
    hDileptonCompLong->Sumw2();
    hDileptonCompPerp->Sumw2();
    hRecoilTypeLong->Sumw2();
    hRecoilTypePerp->Sumw2();

  }


  HistoRedMET() : theName("") {
    hRedMET = 0;
    hRedMETCompLong = 0;
    hRedMETCompPerp = 0;
    hRecoilCompLong = 0;
    hRecoilCompPerp = 0;
    hMetCompLong = 0;
    hMetCompPerp = 0;
    hSumJetCompLong = 0;
    hSumJetCompPerp = 0;
    hDileptonCompLong = 0;
    hDileptonCompPerp = 0;
    hRecoilTypeLong = 0;
    hRecoilTypePerp = 0;

  }



  HistoRedMET(std::string name, TFile *file) : theName(name) {
    hRedMET = (TH1F *) file->Get(theName+"_hRedMET");
    hRedMETCompLong = (TH1F *) file->Get(theName+"_hRedMETCompLong");
    hRedMETCompPerp = (TH1F *) file->Get(theName+"_hRedMETCompPerp");
    hRecoilCompLong = (TH1F *) file->Get(theName+"_hRecoilCompLong");
    hRecoilCompPerp = (TH1F *) file->Get(theName+"_hRecoilCompPerp");
    hMetCompLong = (TH1F *) file->Get(theName+"_hMetCompLong");
    hMetCompPerp = (TH1F *) file->Get(theName+"_hMetCompPerp");
    hSumJetCompLong = (TH1F *) file->Get(theName+"_hSumJetCompLong");
    hSumJetCompPerp = (TH1F *) file->Get(theName+"_hSumJetCompPerp");
    hDileptonCompLong = (TH1F *) file->Get(theName+"_hDileptonCompLong");
    hDileptonCompPerp = (TH1F *) file->Get(theName+"_hDileptonCompPerp");
    hRecoilTypeLong = (TH1F *) file->Get(theName+"_hRecoilTypeLong");
    hRecoilTypePerp = (TH1F *) file->Get(theName+"_hRecoilTypePerp");

  }


  HistoRedMET * Clone(std::string name) {
    HistoRedMET *ret = new HistoRedMET();
    ret->theName = name;

    if(hRedMET !=0) hRedMET->Clone((ret->theName+"_hRedMET").Data());
    if(hRedMETCompLong !=0) hRedMETCompLong->Clone((ret->theName+"_hRedMETCompLong").Data());
    if(hRedMETCompPerp !=0) hRedMETCompPerp->Clone((ret->theName+"_hRedMETCompPerp").Data());
    if(hRecoilCompLong !=0) hRecoilCompLong->Clone((ret->theName+"_hRecoilCompLong").Data());
    if(hRecoilCompPerp !=0) hRecoilCompPerp->Clone((ret->theName+"_hRecoilCompPerp").Data());
    if(hMetCompLong !=0) hMetCompLong->Clone((ret->theName+"_hMetCompLong").Data());
    if(hMetCompPerp !=0) hMetCompPerp->Clone((ret->theName+"_hMetCompPerp").Data());
    if(hSumJetCompLong !=0) hSumJetCompLong->Clone((ret->theName+"_hSumJetCompLong").Data());
    if(hSumJetCompPerp !=0) hSumJetCompPerp->Clone((ret->theName+"_hSumJetCompPerp").Data());
    if(hDileptonCompLong !=0) hDileptonCompLong->Clone((ret->theName+"_hDileptonCompLong").Data());
    if(hDileptonCompPerp !=0) hDileptonCompPerp->Clone((ret->theName+"_hDileptonCompPerp").Data());
    if(hRecoilTypeLong !=0) hRecoilTypeLong->Clone((ret->theName+"_hRecoilTypeLong").Data());
    if(hRecoilTypePerp !=0) hRecoilTypePerp->Clone((ret->theName+"_hRecoilTypePerp").Data());
    
    return ret;
  }



  void Add(const HistoRedMET* histSet) {
    if(hRedMET != 0) hRedMET->Add(histSet->hRedMET);
    if(hRedMETCompLong != 0) hRedMETCompLong->Add(histSet->hRedMETCompLong);
    if(hRedMETCompPerp != 0) hRedMETCompPerp->Add(histSet->hRedMETCompPerp);
    if(hRecoilCompLong != 0) hRecoilCompLong->Add(histSet->hRecoilCompLong);
    if(hRecoilCompPerp != 0) hRecoilCompPerp->Add(histSet->hRecoilCompPerp);
    if(hMetCompLong != 0) hMetCompLong->Add(histSet->hMetCompLong);
    if(hMetCompPerp != 0) hMetCompPerp->Add(histSet->hMetCompPerp);
    if(hSumJetCompLong != 0) hSumJetCompLong->Add(histSet->hSumJetCompLong);
    if(hSumJetCompPerp != 0) hSumJetCompPerp->Add(histSet->hSumJetCompPerp);
    if(hDileptonCompLong != 0) hDileptonCompLong->Add(histSet->hDileptonCompLong);
    if(hDileptonCompPerp != 0) hDileptonCompPerp->Add(histSet->hDileptonCompPerp);
    if(hRecoilTypeLong != 0) hRecoilTypeLong->Add(histSet->hRecoilTypeLong);
    if(hRecoilTypePerp != 0) hRecoilTypePerp->Add(histSet->hRecoilTypePerp);

  }



  void Scale(double scaleFact) {
    if(hRedMET != 0) hRedMET->Scale(scaleFact);
    if(hRedMETCompLong != 0) hRedMETCompLong->Scale(scaleFact);
    if(hRedMETCompPerp != 0) hRedMETCompPerp->Scale(scaleFact);
    if(hRecoilCompLong != 0) hRecoilCompLong->Scale(scaleFact);
    if(hRecoilCompPerp != 0) hRecoilCompPerp->Scale(scaleFact);
    if(hMetCompLong != 0) hMetCompLong->Scale(scaleFact);
    if(hMetCompPerp != 0) hMetCompPerp->Scale(scaleFact);
    if(hSumJetCompLong != 0) hSumJetCompLong->Scale(scaleFact);
    if(hSumJetCompPerp != 0) hSumJetCompPerp->Scale(scaleFact);
    if(hDileptonCompLong != 0) hDileptonCompLong->Scale(scaleFact);
    if(hDileptonCompPerp != 0) hDileptonCompPerp->Scale(scaleFact);
    if(hRecoilTypeLong != 0) hRecoilTypeLong->Scale(scaleFact);
    if(hRecoilTypePerp != 0) hRecoilTypePerp->Scale(scaleFact);

  }


  void Write() {
    if(hRedMET != 0) hRedMET->Write();
    if(hRedMETCompLong != 0) hRedMETCompLong->Write();
    if(hRedMETCompPerp != 0) hRedMETCompPerp->Write();
    if(hRecoilCompLong != 0) hRecoilCompLong->Write();
    if(hRecoilCompPerp != 0) hRecoilCompPerp->Write();
    if(hMetCompLong != 0) hMetCompLong->Write();
    if(hMetCompPerp != 0) hMetCompPerp->Write();
    if(hSumJetCompLong != 0) hSumJetCompLong->Write();
    if(hSumJetCompPerp != 0) hSumJetCompPerp->Write();
    if(hDileptonCompLong != 0) hDileptonCompLong->Write();
    if(hDileptonCompPerp != 0) hDileptonCompPerp->Write();
    if(hRecoilTypeLong != 0) hRecoilTypeLong->Write();
    if(hRecoilTypePerp != 0) hRecoilTypePerp->Write();

  }
  
  void Fill(double redmet,
	    double redmet_long, double redmet_perp,
	    double recoil_long, double recoil_perp,
	    double met_long, double met_perp,
	    double sumjet_long, double sumjet_perp,
	    double dilepton_long, double dilepton_perp,
	    double type_long, double type_perp,
	    double weight) {
    hRedMET->Fill(redmet, weight);
    hRedMETCompLong->Fill(redmet_long, weight);
    hRedMETCompPerp->Fill(redmet_perp, weight);
    hRecoilCompLong->Fill(recoil_long, weight);
    hRecoilCompPerp->Fill(recoil_perp, weight);
    hMetCompLong->Fill(met_long, weight);
    hMetCompPerp->Fill(met_perp, weight);
    hSumJetCompLong->Fill(sumjet_long, weight);
    hSumJetCompPerp->Fill(sumjet_perp, weight);
    hDileptonCompLong->Fill(dilepton_long, weight);
    hDileptonCompPerp->Fill(dilepton_perp, weight);
    hRecoilTypeLong->Fill(type_long, weight);
    hRecoilTypePerp->Fill(type_perp, weight);

  }

  /// Destructor
  virtual ~HistoRedMET() {}

  // Operations
  TString theName;

  TH1F *hRedMET;
  TH1F *hRedMETCompLong;
  TH1F *hRedMETCompPerp;
  TH1F *hRecoilCompLong;
  TH1F *hRecoilCompPerp;
  TH1F *hMetCompLong;
  TH1F *hMetCompPerp;
  TH1F *hSumJetCompLong;
  TH1F *hSumJetCompPerp;
  TH1F *hDileptonCompLong;
  TH1F *hDileptonCompPerp;
  TH1F *hRecoilTypeLong;
  TH1F *hRecoilTypePerp;

};



#endif
