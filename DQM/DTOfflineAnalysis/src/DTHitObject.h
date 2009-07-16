#ifndef DTHitObject_H
#define DTHitObject_H

/** \class DTHitObject
 *  No description available.
 *
 *  $Date: 2009/07/16 12:16:17 $
 *  $Revision: 1.2 $
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
  int sl;
  int layer;
  int wire;

  // position in local RF
  double X;
  double Y;
  double Z;

  // residual on distance from the wire
  double resDist;
  // residual on position
  double resPos;
  // distance from the wire
  double distFromWire;
  // sigma on position
  double sigmaPos;
  // the angle
  double angle;
  // flag to label noisy channels
  bool isNoisyCell;
  // digi time (ns)
  double digiTime;
  // t0 from pulses
  double t0pulses;
  
  ClassDef(DTHitObject,1)
};
#endif

