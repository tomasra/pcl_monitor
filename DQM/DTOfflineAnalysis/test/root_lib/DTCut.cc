
/*
 *  See header file for a description of this class.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - INFN Torino
 */

#include "DTCut.h"
#include "DTSegmentObject.h"
#include <iostream>

using namespace std;


DTCut::DTCut() :  nHits_min(0),
		  nHits_max(100),
		  nHitsPhi_min(0),
		  nHitsPhi_max(100),
		  nHitsTheta_min(0),
		  nHitsTheta_max(100),
		  phi_min(-9999),
		  phi_max(9999),
		  theta_min(-9999),
		  theta_max(9999) {}

DTCut::~DTCut(){}



void DTCut::setSegmNHits(int min, int max) {
  nHits_min = min;
  nHits_max = max;
}


void DTCut::setSegmNHitsPhi(int min, int max) {
  nHitsPhi_min = min;
  nHitsPhi_max = max;
}


void DTCut::setSegmNHitsTheta(int min, int max) {
  nHitsTheta_min = min;
  nHitsTheta_max = max;
}


void DTCut::setSegmPhiAngle(float min, float max) {
  phi_min = min;
  phi_max = max;
}



void DTCut::setSegmThetaAngle(float min, float max) {
  theta_min = min;
  theta_max = max;
}

// Operations
bool DTCut::selectSegm(const DTSegmentObject* oneSeg) const {
   // select segments
//   cout << " Cutting on segment: " << endl;
//   cout << "       # hits: " << oneSeg->nHits
//        << " phi: " << oneSeg->phi
//        << " theta: " << oneSeg->theta << endl;
//   cout << " range min: " << nHits_min << " max: " << nHits_max << endl;

  if(oneSeg->nHits < nHits_min ||  oneSeg->nHits > nHits_max) return false;
  if(oneSeg->nHitsPhi < nHitsPhi_min ||  oneSeg->nHitsPhi > nHitsPhi_max) return false;
  if(oneSeg->nHitsTheta < nHitsTheta_min ||  oneSeg->nHitsTheta > nHitsTheta_max) return false;
  if(oneSeg->phi < phi_min || oneSeg->phi > phi_max) return false;
  if(oneSeg->theta < theta_min || oneSeg->theta > theta_max) return false;

  return true;
}




ostream& operator<<(ostream& os, const DTCut& cut ){

  os << "cut: " << endl
     << " nHits " << cut.nHits_min << " to " << cut.nHits_max << endl
     << " nHits phi: " << cut.nHitsPhi_min << " to " << cut.nHitsPhi_max << endl
     << " nHits theta: " << cut.nHitsTheta_min << " to " << cut.nHitsTheta_max << endl
     << " phi (rad): " << cut.phi_min << " to " << cut.phi_max << endl
     << " theta (rad): " << cut.theta_min << " to " << cut.theta_max << endl;

  return os;
}
