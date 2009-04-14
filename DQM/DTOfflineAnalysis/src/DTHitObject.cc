
/*
 *  See header file for a description of this class.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - INFN Torino
 */

#include "DTHitObject.h"



  
DTHitObject::DTHitObject() : wheel(0),
			     station(0),
			     sector(0),
			     sl(0),
			     layer(0),
			     wire(0),
			     X(0.),
			     Y(0.),
			     Z(0.),
			     resDist(0.),
			     resPos(0.),
			     distFromWire(0.),
			     sigmaPos(0.),
			     angle(0.) {}


DTHitObject::DTHitObject(int wheel, int station, int sector, int sl, int layer, int wire) : wheel(wheel),
											    station(station),
											    sector(sector),
											    sl(sl),
											    layer(layer),
											    wire(wire),
											    X(0.),
											    Y(0.),
											    Z(0.),
											    resDist(0.),
											    resPos(0.),
											    distFromWire(0.),
											    sigmaPos(0.),
											    angle(0.) {}




DTHitObject::~DTHitObject(){}


void DTHitObject::setLocalPosition(double x, double y, double z) {
  X = x;
  Y = y;
  Z = z;
}



ClassImp(DTHitObject)
