#ifndef DTHitObject_H
#define DTHitObject_H

/** \class DTHitObject
 *  No description available.
 *
 *  $Date: 2010/06/07 17:08:49 $
 *  $Revision: 1.4 $
 *  \author G. Cerminara - INFN Torino
 */

#if !defined(__CINT__)||  defined(__MAKECINT__)
#include "TObject.h"
#endif



class DTHitObject : public TObject {
public:
  /// Constructor
  DTHitObject();

  DTHitObject(int wheel, int station, int sector, int sl, int layer, int wire);

  /// Destructor
  virtual ~DTHitObject();

  // Operations
  void setLocalPosition(double x, double y, double z);


protected:

public:

  // wire ID
//   int wheel;
//   int station;
//   int sector;
  short sl;
  short layer;
  short wire;

  // position in local RF
  float X;
  float Y;
  float Z;

  // residual on distance from the wire
  float resDist;
  // residual on distance from the wire - step 2
  float resDistS1;
  // residual on distance from the wire - step 1
  float resDistS2;
  // residual on position
  float resPos;
  // distance from the wire
  float distFromWire;
  // sigma on position
  float sigmaPos;
  // the angle
  float angle;
  // flag to label noisy channels
  bool isNoisyCell;
  // digi time (ns)
  float digiTime;
  // t0 from pulses
  float t0pulses;
  
  ClassDef(DTHitObject,1)
};
#endif

