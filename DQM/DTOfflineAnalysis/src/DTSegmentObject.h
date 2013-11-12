#ifndef DTSegmentObject_H
#define DTSegmentObject_H

/** \class DTSegmentObject
 *  No description available.
 *
 *  $Date: 2013/06/05 07:34:40 $
 *  $Revision: 1.6 $
 *  \author G. Cerminara - INFN Torino
 */

#if !defined(__CINT__)||  defined(__MAKECINT__)
#include "TObject.h"
#include "TArrayF.h"
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
  DTHitObject * addAvailable1DHit(int wheel, int station, int sector, int sl, int layer, int wire);

  void setTTrig(int sl, double mean, double sigma, double kfact);
  double getTTrig(int sl, double& mean, double& sigma, double& kfact) const;
  double getTTrig(int sl) const;

  void setPositionInChamber(double x, double y, double z);
  void setGlobalPosition(float x, float y, float z);

//   const DTDetId chamberId() const;

protected:

public:
  
  // Chamber ID
  short wheel;
  short station;
  short sector;

  // projection type:
  // 1 -> phi only
  // 2 -> theta only
  // 3 -> phi AND theta
  short proj;
  // position in SL RF
  float Xsl;
  float Ysl;
  float Zsl;

  // angles in chamber RF
  float phi;
  float theta;

  // t0segment
  float t0SegPhi;
  float t0SegTheta;
  float dVDriftPhi;
  float vDriftCorrPhi;
  float vDriftCorrTheta;

  // nhits
  short nHits;
  short nHitsPhi;
  short nHitsTheta;


  // chi2
  float chi2;

//   // ttrig for the 3 SLs
  TArrayF tTrigMean;
  TArrayF tTrigSigma;
  TArrayF tTrigKfact;
  

  // the Collection of hits belonging to the segments
  TClonesArray *hits;


  // the Collection of available 1D hits
  short nAvailableHits;
  TClonesArray *availableHits;

  // Global coordinates
  float Xglob;
  float Yglob;
  float Zglob;

private:
//   static TClonesArray * s_hits;

  ClassDef(DTSegmentObject,2)
};
#endif

