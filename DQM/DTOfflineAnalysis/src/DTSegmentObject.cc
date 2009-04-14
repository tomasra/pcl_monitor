/*
 *  See header file for a description of this class.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - INFN Torino
 */

#include "DTSegmentObject.h"
#include "DTHitObject.h"

#include <iostream>

using namespace std;




DTSegmentObject::DTSegmentObject() : wheel(0),
				     station(0),
				     sector(0),
				     proj(-1),
				     Xsl(0.),
				     Ysl(0.),
				     Zsl(0.),
				     phi(0.),
				     theta(0.),
				     t0SegPhi(0.),
				     t0SegTheta(0.),
				     vDriftCorrPhi(0.),
				     vDriftCorrTheta(0.),
				     nHits(0),
				     nHitsPhi(0),
				     nHitsTheta(0),
				     chi2(0.),
				     hitCounter(0),
				     tTrig(3),
				     tTrigMean(3),
				     tTrigSigma(3),
				     tTrigKfact(3) {
  hits = new TClonesArray("DTHitObject");
  cout << "Default constructor" << endl;
}


DTSegmentObject::DTSegmentObject(int wheel, int station, int sector) : wheel(wheel),
								       station(station),
								       sector(sector),
								       proj(-1),
								       Xsl(0.),
								       Ysl(0.),
								       Zsl(0.),
								       phi(0.),
								       theta(0.),
								       t0SegPhi(0.),
								       t0SegTheta(0.),
								       vDriftCorrPhi(0.),
								       vDriftCorrTheta(0.),
								       nHits(0),
								       nHitsPhi(0),
								       nHitsTheta(0),
								       chi2(0.),
								       hitCounter(0),
								       tTrig(3),
								       tTrigMean(3),
								       tTrigSigma(3),
								       tTrigKfact(3) {
  hits = new TClonesArray("DTHitObject");
  cout << "Constructor" << endl;
}

DTSegmentObject::DTSegmentObject(const DTSegmentObject& segmObj) : wheel(segmObj.wheel),
								   station(segmObj.station),
								   sector(segmObj.sector),
								   proj(segmObj.proj),
								   Xsl(segmObj.Xsl),
								   Ysl(segmObj.Ysl),
								   Zsl(segmObj.Zsl),
								   phi(segmObj.phi),
								   theta(segmObj.theta),
								   t0SegPhi(segmObj.t0SegPhi),
								   t0SegTheta(segmObj.t0SegTheta),
								   vDriftCorrPhi(segmObj.vDriftCorrPhi),
								   vDriftCorrTheta(segmObj.vDriftCorrTheta),
								   nHits(segmObj.nHits),
								   nHitsPhi(segmObj.nHitsPhi),
								   nHitsTheta(segmObj.nHitsTheta),
								   chi2(segmObj.chi2),
								   hitCounter(segmObj.hitCounter),
								   tTrig(segmObj.tTrig),
								   tTrigMean(segmObj.tTrigMean),
								   tTrigSigma(segmObj.tTrigSigma),
								   tTrigKfact(segmObj.tTrigKfact) {
  hits = new TClonesArray(*(segmObj.hits));
  cout << "copy constructor" << endl;
}



DTSegmentObject::~DTSegmentObject(){
  cout << "Destructor" << endl;
//   delete hits;
}



  // Operations
void DTSegmentObject::add1DHit(const DTHitObject& hit) {
  (*hits)[hitCounter++] = new DTHitObject(hit);
  nHits++;
  if(hit.sl == 2) {
    nHitsTheta++;
  } else {
    nHitsPhi++;
  }
}



void DTSegmentObject::setTTrig(int sl, double ttrig, double mean, double sigma, double kfact) {
  tTrig.AddAt(ttrig,sl);
  tTrigMean.AddAt(mean,sl);
  tTrigSigma.AddAt(sigma, sl);
  tTrigKfact.AddAt(kfact, sl);
}
  

void DTSegmentObject::setPositionInChamber(double x, double y, double z) {
 Xsl = x;
 Ysl = y;
 Zsl = z;
}



ClassImp(DTSegmentObject)
