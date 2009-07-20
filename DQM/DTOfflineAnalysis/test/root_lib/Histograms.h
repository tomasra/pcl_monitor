#ifndef Histograms_H
#define Histograms_H

#include "TH1F.h"
#include "TH2F.h"
#include "TString.h"
#include "TFile.h"

#include <iostream>
using namespace std;


/// A set of histograms of meantimer for different y regions
class HRes1DHits{
 public:
  HRes1DHits(const TString& name_){
    TString N = name_;
    name=N;
    cout << "HRes1DHits called!" << endl;
    hResDist = new TH1F(N+"_hResDist", "Res dist from wire fabs(rec_hit) - fabs(segm_extr) (cm)",
			400, -1, 1);
    
    hResDistVsDist = new TH2F(N+"_hResDistVsDist",
			      "Res dist from wire fabs(rec_hit) - fabs(segm_extr) vs dist",
			      100, 0, 2.5, 200, -0.4, 0.4);

    hResDistVsAngle = new TH2F(N+"_hResDistVsAngle",
			       "Res dist from wire vs angle",
			       100,-3.15,3.15, 200, -0.4, 0.4);
    
    hResPos = new TH1F(N+"_hResPos", "Res. on position", 200, -0.4, 0.4);
    
    hPullPos = new TH1F(N+"_hPullPos", "Pulls on position", 100, -5, 5);

    hResPosVsAngle = new TH2F(N+"_hResPosVsAngle",
			       "Res dist from wire vs angle",
			       100,-3.15,3.15, 200, -0.4, 0.4);

    hResDistVsY = new TH2F(N+"_hResDistVsY",
			   "Res. dist from wire vs Y",
			   200, -200, 200, 200, -0.4, 0.4);



  }
  
  HRes1DHits(TString name_, TFile* file){
    name=name_;

    hResDist = (TH1F *) file->Get(name_+"_hResDist");
    hResDistVsDist = (TH2F *) file->Get(name_+"_hResDistVsDist");
    hResDistVsAngle = (TH2F *) file->Get(name_+"_hResDistVsAngle");
    hResPos = (TH1F *) file->Get(name_+"_hResPos");
    hPullPos = (TH1F *) file->Get(name_+"_hPullPos");
    hResPosVsAngle = (TH2F *) file->Get(name_+"_hResPosVsAngle");
    hResDistVsY = (TH2F *) file->Get(name_+"_hResDistVsY");
  }


  ~HRes1DHits(){}

  void Fill(float dealtDist, float distFromWire, float deltaX, float hitY, float angle, float sigma) {
    hResDist->Fill(dealtDist);
    hResDistVsDist->Fill(distFromWire, dealtDist);
    hResDistVsAngle->Fill(angle, dealtDist);
    hResPos->Fill(deltaX);
    hPullPos->Fill(deltaX/sigma);
    hResPosVsAngle->Fill(angle, deltaX);
    hResDistVsY->Fill(hitY, dealtDist);

  }
  
  void Write() {
    hResDist->Write();
    hResDistVsDist->Write();
    hResDistVsAngle->Write();
    hResPos->Write();
    hPullPos->Write();
    hResPosVsAngle->Write();
    hResDistVsY->Write();
  }

  
 public:

  TH1F * hResDist;
  TH2F * hResDistVsDist;
  TH2F * hResDistVsAngle;
  TH1F * hResPos;
  TH1F * hPullPos;
  TH2F * hResPosVsAngle;
  TH2F * hResDistVsY;
  TString name;

};



#endif
