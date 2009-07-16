
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2009/07/16 12:16:17 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - INFN Torino
 */

#include "DTHitObject.h"
#include <iostream>
using namespace std;



  
DTHitObject::DTHitObject() : sl(0),
			     layer(0),
			     wire(0),
			     X(0.),
			     Y(0.),
			     Z(0.),
			     resDist(0.),
			     resPos(0.),
			     distFromWire(0.),
			     sigmaPos(0.),
			     angle(0.),
			     isNoisyCell(false),
			     digiTime(0.),
			     t0pulses(0.) {
}


DTHitObject::DTHitObject(int wheel, int station, int sector, int sl, int layer, int wire) : sl(sl),
											    layer(layer),
											    wire(wire),
											    X(0.),
											    Y(0.),
											    Z(0.),
											    resDist(0.),
											    resPos(0.),
											    distFromWire(0.),
											    sigmaPos(0.),
											    angle(0.),
											    isNoisyCell(false),
											    digiTime(0.),
											    t0pulses(0.) {

}




DTHitObject::~DTHitObject(){
}


void DTHitObject::setLocalPosition(double x, double y, double z) {
  X = x;
  Y = y;
  Z = z;
}



ClassImp(DTHitObject)
