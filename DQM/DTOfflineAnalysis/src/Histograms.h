#ifndef RecoLocalMuon_Histograms_H
#define RecoLocalMuon_Histograms_H

/** \class Histograms
 *  Collection of histograms for DT RecHit and Segment test.
 *
 *  $Date: 2008/10/27 16:25:25 $
 *  $Revision: 1.5 $
 *  \author G. Cerminara - INFN Torino
 */


#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TFile.h"
#include "TString.h"

#include <string>
#include <math.h>
#include "DataFormats/MuonDetId/interface/DTSuperLayerId.h"


/// A set of histograms of residuals for 1D RecHits (using 4D segment as reference)
class HRes2DSL{
 public:
  HRes2DSL(std::string name_){
    TString N = name_.c_str();
    name=N;

    // Residuals on position and on distance (also vs position, vs distance, and in different X regions)
    hResDist = new TH1F ("hResDist"+N, "Residuals on the distance from wire fabs(rec_hit) - fabs(segm_extr) (cm)",
			 200, -0.4, 0.4);
    hResDist_1of3X = new TH1F ("hResDist_1of3X"+N, "Residuals on the distance from wire fabs(rec_hit) - fabs(segm_extr) (cm)",
			       200, -0.4, 0.4);
    hResDist_2of3X = new TH1F ("hResDist_2of3X"+N, "Residuals on the distance from wire fabs(rec_hit) - fabs(segm_extr) (cm)",
			       200, -0.4, 0.4);
    hResDist_3of3X = new TH1F ("hResDist_3of3X"+N, "Residuals on the distance from wire fabs(rec_hit) - fabs(segm_extr) (cm)",
			       200, -0.4, 0.4);
    hResDistVsDist = new TH2F("hResDistVsDist"+N,
			      "Residuals on the distance (cm) from wire fabs(rec_hit) - fabs(segm_extr) vs position (cm)", 100, 0, 2.5, 200, -0.4, 0.4);
    hResPos = new TH1F ("hResPos"+N, "Residuals on the position (cm) from wire (rec_hit - segm_extr) (cm)",
			 200, -0.4, 0.4);
    hResPos_xpos = new TH1F ("hResPos_xpos"+N, "x>0: Residuals on the position (cm) from wire (rec_hit - segm_extr) (cm)",
			 200, -0.4, 0.4);
    hResPos_xneg = new TH1F ("hResPos_xneg"+N, "x<0: Residuals on the position (cm) from wire (rec_hit - segm_extr) (cm)",
			 200, -0.4, 0.4);
    hResPosVsPos = new TH2F("hResPosVsPos"+N,
			      "Residuals on the position (cm) from wire (rec_hit - segm_extr) vs position (cm)", 100, -2.5, 2.5, 200, -0.4, 0.4);
    hResDistVsXInSL = new TProfile("hResDistVsXInSL"+N,
				   "Residuals on the distance (cm) from wire (rec_hit - segm_extr) vs X (cm) in SL RF",
				   200, -300, 300);
  }
  
  HRes2DSL(TString name_, TFile* file){
    name=name_;
    hResDist = (TH1F *) file->Get("hResDist"+name);
    hResDist_1of3X = (TH1F *) file->Get("hResDist_1of3X"+name);
    hResDist_2of3X = (TH1F *) file->Get("hResDist_2of3X"+name);
    hResDist_3of3X = (TH1F *) file->Get("hResDist_3of3X"+name);
    hResDistVsDist = (TH2F *) file->Get("hResDistVsDist"+name);
    hResPos = (TH1F *) file->Get("hResPos"+name);
    hResPos_xpos = (TH1F *) file->Get("hResPos_xpos"+name);
    hResPos_xneg = (TH1F *) file->Get("hResPos_xneg"+name);
    hResPosVsPos = (TH2F *) file->Get("hResPosVsPos"+name);
    //     hResDistVsPosInSL = (TH3F *) file->Get("hResDistVsPosInSL"+name);
    hResDistVsXInSL = (TProfile*) file->Get("hResDistVsXInSL"+name);
  }


  ~HRes2DSL(){}

  void Fill(float distExtr,
	    float distRecHit,
	    float xExtr) {
    hResDist->Fill(fabs(distRecHit)-fabs(distExtr));
    if(xExtr<(-50))
      hResDist_1of3X->Fill(fabs(distRecHit)-fabs(distExtr));
    else if(xExtr<50)
      hResDist_2of3X->Fill(fabs(distRecHit)-fabs(distExtr));
    else
      hResDist_3of3X->Fill(fabs(distRecHit)-fabs(distExtr));

    hResDistVsDist->Fill(distExtr, fabs(distRecHit)-fabs(distExtr));
    hResPos->Fill(distRecHit-distExtr);
    if(distRecHit>0)
      hResPos_xpos->Fill(distRecHit-distExtr);
    else
      hResPos_xneg->Fill(distRecHit-distExtr);
    hResPosVsPos->Fill(distExtr, distRecHit-distExtr);
//  hResDistVsPosInSL->Fill(xExtr, yExtr, residual);
    hResDistVsXInSL->Fill(xExtr, fabs(distRecHit)-fabs(distExtr));

  }
  
  void Write() {
    hResDist->Write();     
    hResDist_1of3X->Write();     
    hResDist_2of3X->Write();     
    hResDist_3of3X->Write();     
    hResDistVsDist->Write();      
    hResPos->Write();     
    hResPos_xpos->Write();     
    hResPos_xneg->Write();     
    hResPosVsPos->Write();      
//     hResDistVsPosInSL->Write();   
    hResDistVsXInSL->Write(); 
  }

  
 public:
  TH1F *hResDist;
  TH1F *hResDist_1of3X;
  TH1F *hResDist_2of3X;
  TH1F *hResDist_3of3X;
  TH2F *hResDistVsDist;
  TH1F *hResPos;
  TH1F *hResPos_xpos;
  TH1F *hResPos_xneg;
  TH2F *hResPosVsPos;
//   TH3F *hResDistVsPosInSL;

  TProfile *hResDistVsXInSL;

  TString name;

};



//---------------------------------------------------------------------------------------
/// A set of histograms of residuals for 1D RecHits (using 4D segment as reference)
class HResSL{
 public:
  HResSL(std::string name_){
    TString N = name_.c_str();
    name=N;

    hRes2DSL = new HRes2DSL(name_);
    hResDistVsYInSL = new TProfile("hResDistVsYInSL"+N,
				   "Residuals on the distance (cm) from wire (rec_hit - segm_extr) vs Y (cm) in SL RF",
				   200, -300, 300);
  }
  
  HResSL(TString name_, TFile* file){
    name=name_;
    hRes2DSL =  new HRes2DSL(name, file);
    hResDistVsYInSL = (TProfile*) file->Get("hResDistVsYInSL"+name);
  }


  ~HResSL(){}

  void Fill(float distExtr,
	    float distRecHit,
	    float xExtr,
	    float yExtr) {
    hRes2DSL->Fill(distExtr,distRecHit,xExtr);
    hResDistVsYInSL->Fill(yExtr, fabs(distRecHit)-fabs(distExtr));

  }
  
  void Write() {
    hRes2DSL->Write();
    hResDistVsYInSL->Write(); 
  }

  
 public:
  HRes2DSL *hRes2DSL;
  TProfile *hResDistVsYInSL;

  TString name;

};



//---------------------------------------------------------------------------------------
/// A set of histograms for 2D segments in SL RF
class HSegment2D{
 public:
  HSegment2D(std::string name_){
    TString N = name_.c_str();
    name=N;
    hNSeg           = new TH1F("hNSeg"+N,
				 "# of segments per event", 50, 0, 50);
    hNSeg->Sumw2();
    hSegmXInCham    = new TH1F("hSegmXInCham"+N,
 				 " Segment X position (cm) in SL RF", 200, -200, 200);
    hSegmPhiAngle   = new TH1F("hSegmPhiAngle"+N,
				 " Segment x/z Direction (deg) in SL RF", 200, -10, 40);
    hSegmPhiAngle->Sumw2();
    hChi2           = new TH1F("hChi2"+N,
				 " Segment reduced Chi2", 90, 0, 30);
    hChi2->Sumw2();
  }
  
  HSegment2D(TString name_, TFile* file){
    name=name_;
    hNSeg           = (TH1F*) file->Get("hNSeg"+name_);
    hSegmXInCham    = (TH1F*) file->Get("hSegmXInCham"+name_);
    hSegmPhiAngle   = (TH1F*) file->Get("hSegmPhiAngle"+name_);
    hChi2           = (TH1F*) file->Get("hChi2"+name_);
  }


  ~HSegment2D(){}

  void Fill(int nsegm) {
     hNSeg->Fill(nsegm);
  }

  void Fill( float posX,
	     float angle,
	     float chi2) {
    hSegmXInCham->Fill(posX);
    hSegmPhiAngle->Fill(angle);
    hChi2->Fill(chi2);
  }
  
  void Write() {
    hNSeg->Write();          
    hSegmXInCham->Write();   
    hSegmPhiAngle->Write();  
    hChi2->Write();          
  }

  
 public:

  TH1F* hNSeg;
  TH1F* hSegmXInCham;
  TH1F* hSegmPhiAngle;
  TH1F* hChi2;

  TString name;

};

//---------------------------------------------------------------------------------------
/// A set of histograms for 4D segments in Chamber RF
class HSegment{
 public:
  HSegment(std::string name_){
    TString N = name_.c_str();
    name=N;

    hSegment2D      = new HSegment2D(name_);
    hSegmYInCham    = new TH1F("hSegmYInCham"+N,
 				 " Segment Y position (cm) in Chamber RF",
 				 200, -200, 200);
    hSegmThetaAngle = new TH1F("hSegmThetaAngle"+N,
				 " Segment y/z Direction (deg) in Chamber RF",
				 180, -50, 50);
    hSegmThetaAngle->Sumw2();
   hSegmXvsYInCham = new TH2F("hSegmXvsYInCham"+N,
				 " Segment position (cm) in Chamber RF",
				 100, -200, 200, 100, -200, 200);
    hImpAngle         = new TH1F("hImpAngle"+N,
				 "Impact Angle (deg)",
				 400, -100, 100);
    
  }
  
  HSegment(TString name_, TFile* file){
    name=name_;
    hSegment2D      = new HSegment2D(name_,file);
    hSegmYInCham    = (TH1F*) file->Get("hSegmYInCham"+name_);
    hSegmThetaAngle = (TH1F*) file->Get("hSegmThetaAngle"+name_);
    hSegmXvsYInCham = (TH2F*) file->Get("hSegmXvsYInCham"+name_);
    hImpAngle         = (TH1F*) file->Get("hImpAngle"+name_);
  }


  ~HSegment(){}

  void Fill(int nsegm) {
     hSegment2D->Fill(nsegm);
  }

  void Fill( float posX,
	     float posY,
	     float phi,
	     float theta,
	     float impAngle,
	     float chi2) {
    hSegment2D->Fill(posX,phi,chi2);
    hSegmYInCham->Fill(posY);
    hSegmThetaAngle->Fill(theta);
    hSegmXvsYInCham->Fill(posX, posY);
    hImpAngle->Fill(impAngle);
  }
  
  void Write() {
    hSegment2D->Write();
    hSegmYInCham->Write();   
    hSegmThetaAngle->Write();
    hSegmXvsYInCham->Write();
    hImpAngle->Write();
  }

  
 public:

  HSegment2D* hSegment2D;
  TH1F* hSegmYInCham;
  TH1F* hSegmThetaAngle;
  TH2F* hSegmXvsYInCham;
  TH1F* hImpAngle;

  TString name;

};

//---------------------------------------------------------------------------------------
/// A set of histograms of meantimer for different y regions
class HMeanTimer{
 public:
  HMeanTimer(std::string name_){
    TString N = name_.c_str();
    name=N;
    hMeanTimer = new TH1F("hMeanTimer"+N, "Mean Timer", 400, 0, 800);
    hMeanTimer_1of3Y = new TH1F("hMeanTimer_1of3Y"+N, "Mean Timer 1of3Y", 400, 0, 800);
    hMeanTimer_2of3Y = new TH1F("hMeanTimer_2of3Y"+N, "Mean Timer 2of3Y", 400, 0, 800);
    hMeanTimer_3of3Y = new TH1F("hMeanTimer_3of3Y"+N, "Mean Timer 3of3Y", 400, 0, 800);
  }
  
  HMeanTimer(TString name_, TFile* file){
    name=name_;
    hMeanTimer = (TH1F*) file->Get("hMeanTimer"+name_);
    hMeanTimer_1of3Y = (TH1F*) file->Get("hMeanTimer_1of3Y"+name_);
    hMeanTimer_2of3Y = (TH1F*) file->Get("hMeanTimer_2of3Y"+name_);
    hMeanTimer_3of3Y = (TH1F*) file->Get("hMeanTimer_3of3Y"+name_);
  }


  ~HMeanTimer(){}

  void Fill(DTSuperLayerId slId,
	    float meanTimer,
	    float ySegm,
	    float cellLenght) {

    ySegm= ySegm + cellLenght/2.0;
    if(ySegm<0.33*cellLenght)
      hMeanTimer_1of3Y->Fill(meanTimer);                          
    else if(ySegm<0.66*cellLenght)
      hMeanTimer_2of3Y->Fill(meanTimer);                          
    else 
      hMeanTimer_3of3Y->Fill(meanTimer);                          
    hMeanTimer->Fill(meanTimer);
  }
  
  void Write() {
    hMeanTimer_1of3Y->Write();
    hMeanTimer_2of3Y->Write();
    hMeanTimer_3of3Y->Write();
    hMeanTimer->Write();
  }

  
 public:

  TH1F* hMeanTimer_1of3Y;
  TH1F* hMeanTimer_2of3Y;
  TH1F* hMeanTimer_3of3Y;
  TH1F* hMeanTimer;

  TString name;

};


//---------------------------------------------------------------------------------------
/// A set of histograms of time boxes for different y regions
class HTimeBoxes{
 public:
  HTimeBoxes(std::string name_){
    TString N = name_.c_str();
    name=N;
    //hTimeBox = new TH1F("hTimeBox"+N, " Time Box", 400, 0, 800);
    hTimeBox_1of3Y = new TH1F("hTimeBox_1of3Y"+N, " Time Box 1of3Y", 400, 0, 800);
    hTimeBox_2of3Y = new TH1F("hTimeBox_2of3Y"+N, " Time Box 2of3Y", 400, 0, 800);
    hTimeBox_3of3Y = new TH1F("hTimeBox_3of3Y"+N, " Time Box 3of3Y", 400, 0, 800);
  }
  
  HTimeBoxes(TString name_, TFile* file){
    name=name_;
    //hTimeBox = (TH1F*) file->Get("hTimeBox"+name_);
    hTimeBox_1of3Y = (TH1F*) file->Get("hTimeBox_1of3Y"+name_);
    hTimeBox_2of3Y = (TH1F*) file->Get("hTimeBox_2of3Y"+name_);
    hTimeBox_3of3Y = (TH1F*) file->Get("hTimeBox_3of3Y"+name_);
  }


  ~HTimeBoxes(){}

  void Fill(DTSuperLayerId slId,
	    float meanTimer,
	    float ySegm,
	    float cellLenght) {

    ySegm= ySegm + cellLenght/2.0;
    if(ySegm<0.33*cellLenght)
      hTimeBox_1of3Y->Fill(meanTimer);                          
    else if(ySegm<0.66*cellLenght)
      hTimeBox_2of3Y->Fill(meanTimer);                          
    else 
      hTimeBox_3of3Y->Fill(meanTimer);                          
    //hTimeBox->Fill(meanTimer);
  }
  
  void Write() {
    hTimeBox_1of3Y->Write();
    hTimeBox_2of3Y->Write();
    hTimeBox_3of3Y->Write();
    //hTimeBox->Write();
  }

  
 public:

  TH1F* hTimeBox_1of3Y;
  TH1F* hTimeBox_2of3Y;
  TH1F* hTimeBox_3of3Y;
  //TH1F* hTimeBox;

  TString name;

};



/// A set of histograms of meantimer for different y regions
class HMeanTime{
 public:
  HMeanTime(std::string name_){
    TString N = name_.c_str();
    name=N;
    hMeanTimer123 = new TH1F(N+"_hMeanTimer123", "Mean Timer 123", 192, 200, 500);
    hMeanTimer123->Sumw2();
    hMeanTimer234 = new TH1F(N+"_hMeanTimer234", "Mean Timer 234", 192, 200, 500);
    hMeanTimer234->Sumw2();
    hMeanTimer = new TH1F(N+"_hMeanTimer", "Mean Timer", 192, 200, 500);
    hMeanTimer->Sumw2();
    hMeanTimer123vs234 = new TH2F(N+"_hMeanTimer123vs234", "Mean Timer 123 vs 234",
				  192, 200, 500, 192, 200, 500);
  }
  
  HMeanTime(TString name_, TFile* file){
    name=name_;
    hMeanTimer123 = (TH1F*) file->Get(name+"_hMeanTimer123");
    hMeanTimer234 = (TH1F*) file->Get(name+"_hMeanTimer234");
    hMeanTimer = (TH1F*) file->Get(name+"_hMeanTimer");
    hMeanTimer123vs234 = (TH2F*) file->Get(name+"_hMeanTimer123vs234");
  }


  ~HMeanTime(){}

  void Fill(double meanT123, double meanT234) {
    if(meanT123>-1)
      hMeanTimer123->Fill(meanT123);
    if(meanT234>-1)
    hMeanTimer234->Fill(meanT234);
    if(meanT123>-1 && meanT234>-1) {
      hMeanTimer->Fill(meanT123);
      hMeanTimer->Fill(meanT234);
      hMeanTimer123vs234->Fill(meanT234, meanT123);
    }
  }
  
  void Write() {
    hMeanTimer123->Write();
    hMeanTimer234->Write();
    hMeanTimer->Write();
    hMeanTimer123vs234->Write();
  }

  
 public:

  TH1F* hMeanTimer123;
  TH1F* hMeanTimer234;
  TH1F* hMeanTimer;
  TH2F* hMeanTimer123vs234;

  TString name;

};


















/// A set of histograms of meantimer for different y regions
class HBxDistance{
 public:
  HBxDistance(std::string name_){
    TString N = name_.c_str();
    name=N;
    hBXDistance = new TH1F(N+"_hBxDistance", "BX distance", 5000, 0, 5000);
    hBXDistance->Sumw2();
  }
  
  HBxDistance(TString name_, TFile* file){
    name=name_;
    hBXDistance = (TH1F*) file->Get(name+"_hBxDistance");
  }


  ~HBxDistance(){}

  void Fill(int distance) {
    hBXDistance->Fill(distance);
  }
  
  void Write() {
    hBXDistance->Write();
  }

  
 public:

  TH1F* hBXDistance;

  TString name;

};



#endif



