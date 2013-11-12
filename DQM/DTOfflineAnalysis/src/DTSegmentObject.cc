/*
 *  See header file for a description of this class.
 *
 *  $Date: 2011/02/07 21:57:49 $
 *  $Revision: 1.5 $
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
				     dVDriftPhi(0.),
				     vDriftCorrPhi(0.),
				     vDriftCorrTheta(0.),
				     nHits(0),
				     nHitsPhi(0),
				     nHitsTheta(0),
				     chi2(0.),
				     tTrigMean(3),
				     tTrigSigma(3),
				     tTrigKfact(3),
				     nAvailableHits(0),
				     Xglob(0.),
				     Yglob(0.),
				     Zglob(0.)
{
  hits = new TClonesArray("DTHitObject");
  availableHits = new TClonesArray("DTHitObject");
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
								       dVDriftPhi(0.),
								       vDriftCorrPhi(0.),
								       vDriftCorrTheta(0.),
								       nHits(0),
								       nHitsPhi(0),
								       nHitsTheta(0),
								       chi2(0.),
								       tTrigMean(3),
								       tTrigSigma(3),
								       tTrigKfact(3),
								       nAvailableHits(0),
								       Xglob(0.),
								       Yglob(0.),
								       Zglob(0.)
{
  hits = new TClonesArray("DTHitObject");
  availableHits = new TClonesArray("DTHitObject");
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
								   dVDriftPhi(segmObj.dVDriftPhi),
								   vDriftCorrPhi(segmObj.vDriftCorrPhi),
								   vDriftCorrTheta(segmObj.vDriftCorrTheta),
								   nHits(segmObj.nHits),
								   nHitsPhi(segmObj.nHitsPhi),
								   nHitsTheta(segmObj.nHitsTheta),
								   chi2(segmObj.chi2),
								   tTrigMean(segmObj.tTrigMean),
								   tTrigSigma(segmObj.tTrigSigma),
								   tTrigKfact(segmObj.tTrigKfact),
								   nAvailableHits(0),
								   Xglob(0.),
								   Yglob(0.),
								   Zglob(0.)
{
// new TClonesArray(*(segmObj.hits));
  hits = (TClonesArray *) segmObj.hits->Clone();
  availableHits = (TClonesArray *) segmObj.availableHits->Clone();
}



DTSegmentObject::~DTSegmentObject(){
//   hits->Delete();
//   hits->SetOwner(kTRUE);
//   hits->Clear();
  delete hits;
  delete availableHits;
  
}


DTHitObject* DTSegmentObject::add1DHit(int wheel, int station, int sector, int sl, int layer, int wire) {
  if(wheel != this->wheel || station != this->station || sector != this->sector) {
    cout << "[DTSegmentObject::add1DHit]***Error: hits doesn't belong to this segment!" << endl;
  }

  DTHitObject* ret = new((*hits)[nHits++]) DTHitObject(wheel, station, sector, sl, layer, wire);
  

  if(sl == 2) {
    nHitsTheta++;
  } else {
    nHitsPhi++;
  }

  return ret;
}



  // Operations
void DTSegmentObject::add1DHit(const DTHitObject& hit) {
  (*hits)[nHits++] = new DTHitObject(hit);
  if(hit.sl == 2) {
    nHitsTheta++;
  } else {
    nHitsPhi++;
  }
}


DTHitObject* DTSegmentObject::addAvailable1DHit(int wheel, int station, int sector, int sl, int layer, int wire) {
  if(wheel != this->wheel || station != this->station || sector != this->sector) {
    cout << "[DTSegmentObject::addAvailable1DHit]***Error: hits doesn't belong to segment's chamber!" << endl;
  }

  DTHitObject* ret = new((*availableHits)[nAvailableHits++]) DTHitObject(wheel, station, sector, sl, layer, wire);

  return ret;
}



void DTSegmentObject::setTTrig(int sl, double mean, double sigma, double kfact) {
  tTrigMean.AddAt(mean,sl-1);
  tTrigSigma.AddAt(sigma, sl-1);
  tTrigKfact.AddAt(kfact, sl-1);
}
  

void DTSegmentObject::setPositionInChamber(double x, double y, double z) {
 Xsl = x;
 Ysl = y;
 Zsl = z;
}

void DTSegmentObject::setGlobalPosition(float x, float y, float z) {
 Xglob = x;
 Yglob = y;
 Zglob = z;
}


double DTSegmentObject::getTTrig(int sl, double& mean, double& sigma, double& kfact) const {
  mean = tTrigMean[sl-1];
  sigma = tTrigSigma[sl-1];
  kfact = tTrigKfact[sl-1];
  return mean+kfact*sigma;
}



double DTSegmentObject::getTTrig(int sl) const  {
  double mean, sigma, kfact;
  return getTTrig(sl, mean, sigma, kfact);
}


// const DTDetId DTSegmentObject::chamberId() const {
//   return DTDetId(wheel, station, sector, 0, 0, 0);
// }




ClassImp(DTSegmentObject)
