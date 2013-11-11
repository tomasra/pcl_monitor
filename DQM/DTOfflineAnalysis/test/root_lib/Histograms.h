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
  HRes1DHits(const TString& name_, int detail_=999) : 
    hResDist(0),
    hResDistVsDist(0),
    hResDistVsAngle(0),
    hResDistVsTheta(0),
    hResPos(0),
    hResDistVsX(0),
    hResDistVsCell(0),
    hResDistVsY(0),
    detail(detail_)
  {
    TString N = name_;
    name=N;
    hResDist = new TH1F(N+"_hResDist", 
			N+"_hResDist", 
			//"Res dist from wire",
			400, -1, 1);

    hResPos = new TH1F(N+"_hResPos", N+"_hResPos", 200, -0.4, 0.4);


    if (detail>1) {
      
      hResDistVsDist = new TH2F(N+"_hResDistVsDist",
				N+"_hResDistVsDist",
				//"Res dist from wire vs dist",
				100, 0, 2.5, 200, -0.4, 0.4);

      hResDistVsAngle = new TH2F(N+"_hResDistVsAngle",
				 N+"_hResDistVsAngle",
				 //"Res dist from wire vs angle",
				 200,-1.,1., 200, -0.2, 0.2);

      hResDistVsTheta = new TH2F(N+"_hResDistVsTheta",
				 N+"_hResDistVsTheta",
				 //"Res dist from wire vs angle",
				 200,-1.5,1, 200, -0.2, 0.2);

    
      hResDistVsX = new TH2F(N+"_hResDistVsX",
			     N+"_hResDistVsX",
			     //"Res. dist from wire vs X",
			     100, -210, 210, 600, -0.4, 0.4);

      hResDistVsCell = new TH2F(N+"_hResDistVsCell",
				N+"_hResDistVsCell",
				//"Res. dist from wire vs X",
				100, 0., 100., 600, 0.4, 0.4);

      hResDistVsY = new TH2F(N+"_hResDistVsY",
			     N+"_hResDistVsY",
			     //"Res. dist from wire vs Y",
			     100, -210, 210, 600, -0.4, 0.4);
    }
    

    
//     hPullPos = new TH1F(N+"_hPullPos", "Pulls on position", 100, -5, 5);

//     hResPosVsAngle = new TH2F(N+"_hResPosVsAngle",
// 			       "Res dist from wire vs angle",
// 			       100,-3.15,3.15, 200, -0.4, 0.4);



    
  }

  HRes1DHits(TString name_, TFile* file, int detail_=999){
    name=name_;
    detail=detail_;

    hResDist = (TH1F *) file->Get(name_+"_hResDist");
    hResDistVsDist = (TH2F *) file->Get(name_+"_hResDistVsDist");
    hResDistVsAngle = (TH2F *) file->Get(name_+"_hResDistVsAngle");
    hResDistVsTheta = (TH2F *) file->Get(name_+"_hResDistVsTheta");

    hResDistVsX = (TH2F *) file->Get(name_+"_hResDistVsX");
    hResDistVsCell = (TH2F *) file->Get(name_+"_hResDistVsCell");
    hResDistVsY = (TH2F *) file->Get(name_+"_hResDistVsY");
    hResPos = (TH1F *) file->Get(name_+"_hResPos");
//     hPullPos = (TH1F *) file->Get(name_+"_hPullPos");
//     hResPosVsAngle = (TH2F *) file->Get(name_+"_hResPosVsAngle");

    if (hResDist) {
      hResDist->SetXTitle("|d_{hit}|-|d_{seg}| (cm)");
      if (hResDistVsDist!=0) {
	hResDistVsDist->SetXTitle("|d_{seg}| (cm)");
	hResDistVsDist->SetYTitle("|d_{hit}|-|d_{seg}| (cm)");
	hResDistVsAngle->SetXTitle("#alpha (rad)");
	hResDistVsAngle->SetYTitle("|d_{hit}|-|d_{seg}| (cm)");
	hResDistVsX->SetXTitle("Local X (cm)");
	hResDistVsX->SetYTitle("|d_{hit}|-|d_{seg}| (cm)");
	hResDistVsCell->SetXTitle("Cell");
	hResDistVsCell->SetYTitle("|d_{hit}|-|d_{seg}| (cm)");
	hResDistVsY->SetXTitle("Local Y (cm)");
	hResDistVsY->SetYTitle("|d_{hit}|-|d_{seg}| (cm)");
	hResDistVsTheta->SetYTitle("phi |d_{hit}|-|d_{seg}| (cm) vs angle in theta SL");
      }
    }
  }


  ~HRes1DHits(){
    delete hResDist;
    delete hResDistVsDist;
    delete hResDistVsAngle;
    delete hResDistVsTheta;
    delete hResDistVsX;
    delete hResDistVsCell;
    delete hResDistVsY;
    delete hResPos;
//     delete hPullPos;
//     delete hResPosVsAngle;
}

  void Fill(float deltaDist, float distFromWire, float deltaX, float hitX, float hitY, float angle, float sigma, float angleTheta, int cell) {
    hResDist->Fill(deltaDist);
    hResPos->Fill(deltaX);

    if (detail>1) {
      hResDistVsDist->Fill(distFromWire, deltaDist);
      hResDistVsAngle->Fill(angle, deltaDist);
      hResDistVsTheta->Fill(angleTheta, deltaDist);
      hResDistVsX->Fill(hitX, deltaDist);
      hResDistVsCell->Fill(hitX, cell);
      hResDistVsY->Fill(hitY, deltaDist);
      //     hPullPos->Fill(deltaX/sigma);
      //     hResPosVsAngle->Fill(angle, deltaX);
    }
  }
  
  void Write() {
    hResDist->Write();
    hResPos->Write();
      
    if (detail>1) {
      hResDistVsDist->Write();
      hResDistVsAngle->Write();
      hResDistVsTheta->Write();
      hResDistVsX->Write();
      hResDistVsCell->Write();
      hResDistVsY->Write();
      //     hPullPos->Write();
      //     hResPosVsAngle->Write();
    }
  }
  

  
 public:

  TH1F * hResDist;
  TH2F * hResDistVsDist;
  TH2F * hResDistVsAngle;
  TH2F * hResDistVsTheta;

  TH1F * hResPos;
  TH1F * hPullPos;
  TH2F * hResPosVsAngle;

  TH2F * hResDistVsX;
  TH2F * hResDistVsCell;
  TH2F * hResDistVsY;
  TString name;
  int detail;
};



/// A set of histograms for 4D segments in Chamber RF
class HSegment{
 public:
  HSegment(const TString& name_, int detail_=999) :
    hNHits(0),
    hNHitsPhiVsPhi(0),
    hNHitsThetaVsPhi(0),
    hNHitsThetaVsTheta(0),
    hProj(0),
    hPhiLoc(0),
    hThetaLoc(0),
    hChi2(0),
//     ht0Phi(0),
//     ht0Theta(0),
//     hDeltaT0(0),
    ht0(0),
    ht0PhiVsPhi(0),
    hVDriftVsPhi(0),
    hVDriftVsX(0),
    hVDriftVsY(0),
    hNSegm(0),
    detail(detail_)
    
  {
    TString N = name_;
    name=N;

//     hNHits    = new TH1F(N+"_hNHits", "# hits per segment ("+N+")", 20,0,20);
    hNHits = new TH2F(N+"_hNHits", "# hits per segment ("+N+")", 12,0,12, 6,0,6);
    hNHits->Sumw2();

    if (detail<=1) return;

    // ----------------------------------------------------------------------

//     hNHitsPhi    = new TH1F(N+"_hNHitsPhi", "# hits phi per segment ("+N+")", 15,1,16);
//     hNHitsPhi->Sumw2();

    hNHitsPhiVsPhi    = new TH2F(N+"_hNHitsPhiVsPhi", "# hits phi per segment vs #phi angle ("+N+")",
				 100, -1.58, 1.58,
				 15,1,16);

    hNHitsThetaVsPhi    = new TH2F(N+"_hNHitsThetaVsPhi", "# hits theta per segment vs #phi angle ("+N+")",
				   100, -1.58, 1.58,
				   15,1,16);
    
//     hNHitsTheta    = new TH1F(N+"_hNHitsTheta", "# hits theta per segment ("+N+")", 15,1,16);
//     hNHitsTheta->Sumw2();

    hNHitsThetaVsTheta    = new TH2F(N+"_hNHitsThetaVsTheta",
				     "# hits theta per segment vs #theta angle ("+N+")",
				     100, -1.58, 1.58,
				     15,1,16);

    hProj     = new TH1F(N+"_hProj", "# proj type ("+N+")",3,1,4); 
    hProj->Sumw2();

    hPhiLoc   = new TH1F( N+"_hPhiLoc", "#phi angle in chamber RF (x/z) in rad ("+N+")", 100, -1.5, 1.5);
    hPhiLoc->Sumw2();

    hThetaLoc = new TH1F( N+"_hThetaLoc", "#theta angle in chamber RF (y/z) in rad ("+N+")", 100, -1.5, 1.5);
    hThetaLoc->Sumw2();
    
//     hImpAngl  = new TH1F(N+"_hImpAngle","Impact Angle (rad) ("+N+")",100, 0, 3.15);
//     hImpAngl->Sumw2();

    hChi2     = new TH1F(N+"_hChi2","Chi2 ("+N+")",20,0,20);
    hChi2->Sumw2();

//     ht0Phi    = new TH1F(N+"_ht0Phi","t0 segment phi ("+N+")",200,-100,100);
//     ht0Phi->Sumw2();

//     ht0Theta    = new TH1F(N+"_ht0Theta","t0 segment theta ("+N+")",200,-100,100);
//     ht0Theta->Sumw2();

    ht0 = new TH2F(N+"_ht0","t0",100,-25,25,100,-25,25);

    ht0PhiVsPhi = new TH2F(N+"_ht0PhiVsPhi","t0 segment phi ("+N+")",
			   100, -1., 1.,
			   100,-25,25);
    
//     hDeltaT0      = new TH1F(N+"_hDeltaT0","Delta t0 (ns)",100,-20,20);
//     hDeltaT0->Sumw2();

    hVDrift = new TH1F(N+"_hVDrift", "V drift",100,0.0047, 0.0060);
    hVDrift->Sumw2();
    
    hVDriftVsPhi = new TH2F(N+"_hVDriftVsPhi", "V_drift vs phi",
			    100, -1.58, 1.58,
			    100,0.0047, 0.0060);

    hVDriftVsX = new TH2F(N+"_hVDriftVsX", "V_drift vs X",
			  200, -200, 200,
			  100, 0.0047, 0.0060);

    hVDriftVsY = new TH2F(N+"_hVDriftVsY", "V_drift vs Y",
			  200, -200, 200,
			  100, 0.0047, 0.0060);

//     hNSegm = new TH1F(N+"hNSegm","# of segments", 100, 0, 100);
//     hNSegm->Sumw2();
  }
  
  HSegment(TString name_, TFile* file){
    name=name_;

    hNHits = (TH2F*) file->Get(name_+"_hNHits");
//     hNHitsPhi = (TH1F*) file->Get(name_+"_hNHitsPhi");
    hNHitsPhiVsPhi = (TH2F*) file->Get(name_+"_hNHitsPhiVsPhi");
    hNHitsThetaVsPhi = (TH2F*) file->Get(name_+"_hNHitsThetaVsPhi");
//     hNHitsTheta = (TH1F*) file->Get(name_+"_hNHitsTheta");
    hNHitsThetaVsTheta = (TH2F*) file->Get(name_+"_hNHitsThetaVsTheta");
    hProj = (TH1F*) file->Get(name_+"_hProj");
    hPhiLoc = (TH1F*) file->Get(name_+"_hPhiLoc");
    hThetaLoc = (TH1F*) file->Get(name_+"_hThetaLoc");
//     hImpAngl = (TH1F*) file->Get(name_+"_hImpAngle");
    hChi2 = (TH1F*) file->Get(name_+"_hChi2");
//     ht0Phi = (TH1F*) file->Get(name_+"_ht0Phi");
//     ht0Theta = (TH1F*) file->Get(name_+"_ht0Theta");
    ht0 = (TH2F*) file->Get(name_+"_ht0");
    ht0PhiVsPhi = (TH2F*) file->Get(name_+"_ht0PhiVsPhi");
//     hDeltaT0 = (TH1F*) file->Get(name_+"_hDeltaT0");
    hVDrift = (TH1F*) file->Get(name_+"_hVDrift");
    hVDriftVsPhi = (TH2F*) file->Get(name_+"_hVDriftVsPhi");
    hVDriftVsX = (TH2F*) file->Get(name_+"_hVDriftVsX");
    hVDriftVsY = (TH2F*) file->Get(name_+"_hVDriftVsY");
//     hNSegm = (TH1F*) file->Get(name_+"_hNSegm");

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
	    float vDrift,
	    float Xsl,
	    float Ysl) {

    hNHits->Fill(nHitsPhi, nHitsTheta);
    
    if (detail>1) {
      //     hNHitsPhi->Fill(nHitsPhi);
      hNHitsPhiVsPhi->Fill(phi, nHitsPhi);
      hNHitsThetaVsPhi->Fill(phi, nHitsTheta);
      //     hNHitsTheta->Fill(nHitsTheta);
      hNHitsThetaVsTheta->Fill(theta, nHitsTheta);
      hProj->Fill(proj);
      hPhiLoc->Fill(phi);
      hThetaLoc->Fill(theta);
      //     hImpAngl->Fill(impAngle);
      hChi2->Fill(chi2);
      ht0->Fill(t0Phi,t0Theta);
//       ht0Phi->Fill(t0Phi);
//       ht0Theta->Fill(t0Theta);
      ht0PhiVsPhi->Fill(phi,t0Phi);
//       hDeltaT0->Fill(t0Theta-t0Phi);
      if (vDrift!=0.) {
	hVDrift->Fill(vDrift);
	hVDriftVsPhi->Fill(phi,vDrift);
	hVDriftVsX->Fill(Xsl,vDrift);
	hVDriftVsY->Fill(Ysl,vDrift);
      }
    }    
  }
  
  void Write() {
    hNHits->Write();
//     hNHitsPhi->Write();
    if (detail>1) {
      hNHitsPhiVsPhi->Write();
      hNHitsThetaVsPhi->Write();
      //     hNHitsTheta->Write();
      hNHitsThetaVsTheta->Write();
      hProj->Write();
      hPhiLoc->Write();
      hThetaLoc->Write();
      //     hImpAngl->Write();
      hChi2->Write();
      ht0->Write();
//       ht0Phi->Write();
//       ht0Theta->Write();
      ht0PhiVsPhi->Write();
//       hDeltaT0->Write();
      hVDrift->Write();
      hVDriftVsPhi->Write();
      hVDriftVsX->Write();
      hVDriftVsY->Write();
      //    hNSegm->Write();
    }
  }
  
 public:


  TH2F* hNHits;
//   TH1F* hNHitsPhi;
  TH2F* hNHitsPhiVsPhi;
  TH2F* hNHitsThetaVsPhi;
//   TH1F* hNHitsTheta;
  TH2F* hNHitsThetaVsTheta;
  TH1F* hProj;
  TH1F* hPhiLoc;
  TH1F* hThetaLoc;
//   TH1F* hImpAngl;
  TH1F* hChi2;
  TH2F* ht0;
//   TH1F* ht0Phi;
//   TH1F* ht0Theta;
  TH2F* ht0PhiVsPhi;
//   TH1F* hDeltaT0;
  TH1F* hVDrift;
  TH2F* hVDriftVsPhi;
  TH2F* hVDriftVsX;
  TH2F* hVDriftVsY;
  TH1F* hNSegm;
  TString name;
  int detail;

};



#endif
