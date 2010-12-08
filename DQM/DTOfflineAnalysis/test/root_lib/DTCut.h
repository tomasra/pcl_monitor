#ifndef DTCut_H
#define DTCut_H

/** \class DTCut
 *  No description available.
 *
 *  $Date: 2009/07/27 12:35:32 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include <iostream>


class DTSegmentObject;
class DTHitObject;

class DTCut {
public:
  /// Constructor
  DTCut();

  /// Destructor
  virtual ~DTCut();


  void setSegmNHits(int min, int max);
  void setSegmNHitsPhi(int min, int max);
  void setSegmNHitsTheta(int min, int max);

  void setSegmPhiAngle(float min, float max);
  void setSegmThetaAngle(float min, float max);

  // Operations
  bool selectSegm(const DTSegmentObject* oneSeg) const;
  bool selectHit(const DTHitObject* oneHit) const;

  // set the cuts here
  int nHits_min;
  int nHits_max;
  int nHitsPhi_min;
  int nHitsPhi_max;
  int nHitsTheta_min;
  int nHitsTheta_max;
  double phi_min;
  double phi_max;
  double theta_min;
  double theta_max;

  int selectLR;
  

protected:

private:

};


std::ostream& operator<<( std::ostream& os, const DTCut& cut );

#endif

