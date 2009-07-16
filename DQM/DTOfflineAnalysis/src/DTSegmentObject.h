#ifndef DTSegmentObject_H
#define DTSegmentObject_H

/** \class DTSegmentObject
 *  No description available.
 *
 *  $Date: 2009/07/16 12:16:17 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - INFN Torino
 */

#if !defined(__CINT__)||  defined(__MAKECINT__)
#include "TObject.h"
#include "TArrayD.h"
#include "TClonesArray.h"
#endif

#include "DTHitObject.h"


class DTSegmentObject : public TObject {
public:
  /// Constructor
  DTSegmentObject();

  /// Constructor
  DTSegmentObject(int wheel, int station, int sector);

  DTSegmentObject(const DTSegmentObject& segmObj);

  /// Destructor
  virtual ~DTSegmentObject();

  // Operations
  void add1DHit(const DTHitObject& hit);

  DTHitObject * add1DHit(int wheel, int station, int sector, int sl, int layer, int wire);

  void setTTrig(int sl, double mean, double sigma, double kfact);
  double getTTrig(int sl, double& mean, double& sigma, double& kfact) const;
  double getTTrig(int sl) const;

  void setPositionInChamber(double x, double y, double z);

protected:

public:
  
  // Chamber ID
  int wheel;
  int station;
  int sector;

  // projection type:
  // 1 -> phi only
  // 2 -> theta only
  // 3 -> phi AND theta
  int proj;
  // position in SL RF
  double Xsl;
  double Ysl;
  double Zsl;

  // angles in chamber RF
  double phi;
  double theta;
  // t0segment
  double t0SegPhi;
  double t0SegTheta;
  double vDriftCorrPhi;
  double vDriftCorrTheta;

  // nhits
  int nHits;
  int nHitsPhi;
  int nHitsTheta;


  // chi2
  double chi2;

//   // ttrig for the 3 SLs
  TArrayD tTrigMean;
  TArrayD tTrigSigma;
  TArrayD tTrigKfact;
  

  //   // the Collection of hits
  TClonesArray *hits;


private:
//   static TClonesArray * s_hits;

  ClassDef(DTSegmentObject,1)
};
#endif

