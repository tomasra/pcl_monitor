
/*
 *  See header file for a description of this class.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - INFN Torino
 */

#include "Utils.h"

#include "DTDetId.h"

#include <sstream>

using namespace std;

Utils::Utils(){}

Utils::~Utils(){}

TString Utils::getHistoNameFromDetId(const DTDetId& detId) {
  stringstream wheelStr; 
  if(detId.wheel == 0) wheelStr << "all";
  else wheelStr << detId.wheel;

  stringstream stationStr; 
  if(detId.station == 0) stationStr << "all";
  else stationStr << detId.station;

  stringstream sectorStr; 
  if(detId.sector == 0) sectorStr << "all";
  else sectorStr << detId.sector;

  stringstream slStr; 
  if(detId.sl == 0) slStr << "all";
  else slStr << detId.sl;

  stringstream layerStr; 
  if(detId.layer == 0) layerStr << "all";
  else layerStr << detId.layer;

  string namestr = "Wh" + wheelStr.str() +
    "_St" + stationStr.str() + 
    "_Se" + sectorStr.str();
    
  if(detId.sl != 0) {
    namestr = namestr + "_SL" + slStr.str();
  }
  if(detId.layer != 0) {
    namestr = namestr + "_L" + layerStr.str();
  }

  return TString(namestr.c_str());
}


TString Utils::getHistoNameFromDetIdAndSet(const DTDetId& detId, const TString& set) {
  return Utils::getHistoNameFromDetId(detId) + "_" + set;
}


