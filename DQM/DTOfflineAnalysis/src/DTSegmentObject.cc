/*
 *  See header file for a description of this class.
 *
 *  $Date: 2009/04/14 17:32:06 $
 *  $Revision: 1.1 $
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
// new TClonesArray(*(segmObj.hits));
  hits = (TClonesArray *) segmObj.hits->Clone();
}



DTSegmentObject::~DTSegmentObject(){
//   hits->Delete();
//   hits->SetOwner(kTRUE);
//   hits->Clear();
  delete hits;
  
}


DTHitObject* DTSegmentObject::add1DHit(int wheel, int station, int sector, int sl, int layer, int wire) {
  DTHitObject* ret = new((*hits)[hitCounter++]) DTHitObject(wheel, station, sector, sl, layer, wire);
  nHits++;
  if(sl == 2) {
    nHitsTheta++;
  } else {
    nHitsPhi++;
  }

  return ret;
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
  tTrig.AddAt(ttrig,sl-1);
  tTrigMean.AddAt(mean,sl-1);
  tTrigSigma.AddAt(sigma, sl-1);
  tTrigKfact.AddAt(kfact, sl-1);
}
  

void DTSegmentObject::setPositionInChamber(double x, double y, double z) {
 Xsl = x;
 Ysl = y;
 Zsl = z;
}



ClassImp(DTSegmentObject)
