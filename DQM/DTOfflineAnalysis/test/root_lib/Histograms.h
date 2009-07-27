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


  ~HRes1DHits(){
    delete hResDist;
    delete hResDistVsDist;
    delete hResDistVsAngle;
    delete hResPos;
    delete hPullPos;
    delete hResPosVsAngle;
    delete hResDistVsY;
}

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



/// A set of histograms for 4D segments in Chamber RF
class HSegment{
 public:
  HSegment(const TString& name_){
    TString N = name_;
    name=N;

    hNHits    = new TH1F(N+"_hNHits", "# hits per segment ("+N+")", 20,0,20);
    hNHits->Sumw2();

    hNHitsPhi    = new TH1F(N+"_hNHitsPhi", "# hits phi per segment ("+N+")", 15,1,16);
    hNHitsPhi->Sumw2();

    hNHitsPhiVsPhi    = new TH2F(N+"_hNHitsPhiVsPhi", "# hits phi per segment vs #phi angle ("+N+")",
				 100, 0, 3.15,
				 15,1,16);

    hNHitsThetaVsPhi    = new TH2F(N+"_hNHitsThetaVsPhi", "# hits theta per segment vs #phi angle ("+N+")",
				   100, 0, 3.15,
				   15,1,16);


    
    hNHitsTheta    = new TH1F(N+"_hNHitsTheta", "# hits theta per segment ("+N+")", 15,1,16);
    hNHitsTheta->Sumw2();

    hNHitsThetaVsTheta    = new TH2F(N+"_hNHitsThetaVsTheta",
				     "# hits theta per segment vs #theta angle ("+N+")",
				     100, 1.5, 3.15,
				     15,1,16);

    hProj     = new TH1F(N+"_hProj", "# proj type ("+N+")",3,1,4); 
    hProj->Sumw2();

    hPhiLoc   = new TH1F( N+"_hPhiLoc", "#phi angle in chamber RF (x/z) in rad ("+N+")", 100, 0, 3.15);
    hPhiLoc->Sumw2();

    hThetaLoc = new TH1F( N+"_hThetaLoc", "#theta angle in chamber RF (y/z) in rad ("+N+")", 100, 1.5, 3.15);
    hThetaLoc->Sumw2();
    
    hImpAngl  = new TH1F(N+"_hImpAngle","Impact Angle (rad) ("+N+")",100, 0, 3.15);
    hImpAngl->Sumw2();

    hChi2     = new TH1F(N+"_hChi2","Chi2 ("+N+")",20,0,20);
    hChi2->Sumw2();

    ht0Phi    = new TH1F(N+"_ht0Phi","t0 segment phi ("+N+")",200,-100,100);
    ht0Phi->Sumw2();

    ht0Theta    = new TH1F(N+"_ht0Theta","t0 segment theta ("+N+")",200,-100,100);
    ht0Theta->Sumw2();

    ht0PhiVsPhi    = new TH2F(N+"_ht0PhiVsPhi","t0 segment phi ("+N+")",
			      100, 0, 3.15,
			      100,-100,100);
    
    hDeltaT0      = new TH1F(N+"_hDeltaT0","Delta t0 (ns)",100,-20,20);
    hDeltaT0->Sumw2();

    hVDrift = new TH1F(N+"_hVDrift", "V drift",100,-1,-0.96);
    hVDrift->Sumw2();
    
    hVDriftVsPhi = new TH2F(N+"_hVDriftVsPhi", "V_drift vs phi",
			    100, 0, 3.15,
			    100,-1,-0.96);

    hNSegm = new TH1F(N+"hNSegm","# of segments", 100, 0, 100);
    hNSegm->Sumw2();
  }
  
  HSegment(TString name_, TFile* file){
    name=name_;

    hNHits = (TH1F*) file->Get(name_+"_hNHits");
    hNHitsPhi = (TH1F*) file->Get(name_+"_hNHitsPhi");
    hNHitsPhiVsPhi = (TH2F*) file->Get(name_+"_hNHitsPhiVsPhi");
    hNHitsThetaVsPhi = (TH2F*) file->Get(name_+"_hNHitsThetaVsPhi");
    hNHitsTheta = (TH1F*) file->Get(name_+"_hNHitsTheta");
    hNHitsThetaVsTheta = (TH2F*) file->Get(name_+"_hNHitsThetaVsTheta");
    hProj = (TH1F*) file->Get(name_+"_hProj");
    hPhiLoc = (TH1F*) file->Get(name_+"_hPhiLoc");
    hThetaLoc = (TH1F*) file->Get(name_+"_hThetaLoc");
    hImpAngl = (TH1F*) file->Get(name_+"_hImpAngle");
    hChi2 = (TH1F*) file->Get(name_+"_hChi2");
    ht0Phi = (TH1F*) file->Get(name_+"_ht0Phi");
    ht0Theta = (TH1F*) file->Get(name_+"_ht0Theta");
    ht0PhiVsPhi = (TH2F*) file->Get(name_+"_ht0PhiVsPhi");
    hDeltaT0 = (TH1F*) file->Get(name_+"_hDeltaT0");
    hVDrift = (TH1F*) file->Get(name_+"_hVDrift");
    hVDriftVsPhi = (TH2F*) file->Get(name_+"_hVDriftVsPhi");
    hNSegm = (TH1F*) file->Get(name_+"_hNSegm");
  }


  ~HSegment(){}

  void Fill(int nsegm) {
    hNSegm->Fill(nsegm);
  }

  void Fill(int nHits,
	    int nHitsPhi,
	    int nHitsTheta,
	    int proj,
	    float phi,
	    float theta,
	    float impAngle,
	    float chi2,
	    float t0Phi,
	    float t0Theta,
	    float vDrift) {

    hNHits->Fill(nHits);
    hNHitsPhi->Fill(nHitsPhi);
    hNHitsPhiVsPhi->Fill(phi, nHitsPhi);
    hNHitsThetaVsPhi->Fill(phi, nHitsTheta);
    hNHitsTheta->Fill(nHitsTheta);
    hNHitsThetaVsTheta->Fill(theta, nHitsTheta);
    hProj->Fill(proj);
    hPhiLoc->Fill(phi);
    hThetaLoc->Fill(theta);
    hImpAngl->Fill(impAngle);
    hChi2->Fill(chi2);
    ht0Phi->Fill(t0Phi);
    ht0Theta->Fill(t0Theta);
    ht0PhiVsPhi->Fill(phi,t0Phi);
    hDeltaT0->Fill(t0Theta-t0Phi);
    hVDrift->Fill(vDrift);
    hVDriftVsPhi->Fill(phi,vDrift);

  }
  
  void Write() {
    hNHits->Write();
    hNHitsPhi->Write();
    hNHitsPhiVsPhi->Write();
    hNHitsThetaVsPhi->Write();
    hNHitsTheta->Write();
    hNHitsThetaVsTheta->Write();
    hProj->Write();
    hPhiLoc->Write();
    hThetaLoc->Write();
    hImpAngl->Write();
    hChi2->Write();
    ht0Phi->Write();
    ht0Theta->Write();
    ht0PhiVsPhi->Write();
    hDeltaT0->Write();
    hVDrift->Write();
    hVDriftVsPhi->Write();
    hNSegm->Write();
  }

  
 public:


  TH1F* hNHits;
  TH1F* hNHitsPhi;
  TH2F* hNHitsPhiVsPhi;
  TH2F* hNHitsThetaVsPhi;
  TH1F* hNHitsTheta;
  TH2F* hNHitsThetaVsTheta;
  TH1F* hProj;
  TH1F* hPhiLoc;
  TH1F* hThetaLoc;
  TH1F* hImpAngl;
  TH1F* hChi2;
  TH1F* ht0Phi;
  TH1F* ht0Theta;
  TH2F* ht0PhiVsPhi;
  TH1F* hDeltaT0;
  TH1F* hVDrift;
  TH2F* hVDriftVsPhi;
  TH1F* hNSegm;
  TString name;

};



#endif
