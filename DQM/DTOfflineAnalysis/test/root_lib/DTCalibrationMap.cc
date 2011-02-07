
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2008/12/09 22:43:38 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - INFN Torino
 */

#include "DTCalibrationMap.h"

// #include "FWCore/Utilities/interface/Exception.h"
// #include "FWCore/ParameterSet/interface/ParameterSet.h"

#include <iostream>
#include <fstream>

#include <sstream>
#include <algorithm>
#include <iterator>

using namespace std;
using namespace edm;

DTCalibrationMap::DTCalibrationMap(const string& filename,
				   const string& granularity,
				   unsigned int fields) : calibConstFileName(filename),
							  calibConstGranularity(granularity),
							  nFields(fields) {

  // Initialize correctly the enum which specify the granularity for the calibration
  if(calibConstGranularity == "byWire") {
    theGranularity = byWire;
  } else if(calibConstGranularity == "byLayer"){
    theGranularity = byLayer;
  } else if(calibConstGranularity == "bySL") {
    theGranularity = bySL;
  } else {
    theGranularity = byChamber;
    if(!(calibConstGranularity == "byChamber")) {
      cout << "[DTCalibrationMap]###Warning: Check parameter calibConstGranularity: "
	   << calibConstGranularity << " options not available!" << endl;
    }
  }
  readConsts(calibConstFileName);
}



DTCalibrationMap::~DTCalibrationMap(){}



// Return the t_trig (ns) for a particular wire
float DTCalibrationMap::tTrig(DTDetId wireId) const {
 return getField(wireId, 0);
}



// Return the sigma of the t_trig (ns) for a particular wire
float DTCalibrationMap::sigma_tTrig(DTDetId wireId) const {
 return getField(wireId, 1);
}



// Return the kfactor for a particular wire
float DTCalibrationMap::kFactor(DTDetId wireId) const {
  return getField(wireId, 2);
}

 

// Return the mean drift velocity for a particular wire (cm/ns)
float DTCalibrationMap::meanVDrift(DTDetId wireId) const {
 return getField(wireId, 3);
}



// Return the sigma of the mean drift velocity for a particular wire (cm/ns)
float DTCalibrationMap::sigma_meanVDrift(DTDetId wireId) const {
 return getField(wireId, 4);
}



// Get a key to read calibration constants for a particular wire
// with the given granularity
DTCalibrationMap::Key DTCalibrationMap::getKey(DTDetId wireId) const {
  if (theGranularity == byChamber){
    return Key(wireId.wheel, wireId.station, wireId.sector, 0, 0, 0);
  } else if (theGranularity == bySL) {
    return Key(wireId.wheel, wireId.station, wireId.sector, wireId.sl, 0, 0); 
  } else if (theGranularity == byLayer) {
    return Key(wireId.wheel, wireId.station, wireId.sector, wireId.sl, wireId.layer, 0);  
  } else {
    return Key(wireId);
  }
}



// Get from the map the calibration constants for a particular key
const DTCalibrationMap::CalibConsts* DTCalibrationMap::getConsts(DTDetId wireId) const {
  // Create a cache
  static pair<Key, CalibConsts> cache;

  // Get the key
  Key theKey = getKey(wireId);

  // Check if the result is already cached
  if ( theKey == cache.first ) {
    return &(cache.second);
  }

  // Look for the given key into the map
  map<Key, CalibConsts>::const_iterator res = theMap.find(theKey);
  if (res != theMap.end()) {
    cache = (*res);
    return &((*res).second);
  } else {
    return 0;
  }
}
  


// Get a particular number (field) between all the calibration
// constants available for a particluar wire
float DTCalibrationMap::getField(DTDetId wireId, int field) const {
  const CalibConsts* cals = getConsts(wireId);
  if (cals == 0) {
    cout << "[DTCalibrationMap] ERROR:" << endl
	 << "No parameters for wire: " << wireId << endl
	 << "Check the " << calibConstFileName << " file!" << endl;
    return 99999;
  }

  return (*(cals))[field];
  
}




// Read the calibration consts from a file 
void DTCalibrationMap::readConsts(const string& inputFileName) {
   ifstream file(inputFileName.c_str());
   // Check if the file exists
   if(!file) {
    cout << "[DTCalibrationMap]***Warning: File: " << inputFileName 
	 << " not found in current directory!!!" << endl; 
   }

  string line;

  // The numbers to be read to build the key
  int wheel_id = 0;
  int station_id = 0;
  int sector_id = 0;
  int superlayer_id = 0;
  int layer_id = 0;
  int wire_id = 0;

  // Read all the lines
  while (getline(file,line)) {
    if( line == "" || line[0] == '#' ) continue; // Skip comments and empty lines
    stringstream linestr;
    linestr << line;

    pair<Key, CalibConsts> wireCalib;

    linestr >> wheel_id
	    >> station_id
	    >> sector_id
	    >> superlayer_id
	    >> layer_id
	    >> wire_id;
    
    // Build the key
    wireCalib.first =  Key( wheel_id, 
			    station_id, 
			    sector_id, 
			    superlayer_id, 
			    layer_id, 
			    wire_id);

    if(!checkGranularity(wireCalib.first))
       cout << "[DTCalibrationMap]***Warning: the CalibConstFile is not consistent with the selected granularity!" << endl;


    // Read the calibration constants
    copy(istream_iterator<float>(linestr),
	 istream_iterator<float>(),
	 back_inserter(wireCalib.second));
    
    if(wireCalib.second.size() !=  nFields){
      cout << "[DTCalibrationMap]***Warning: the CalibConstFile is not consistent with the number of fields!" << endl;
    }
    
    theMap.insert(wireCalib);
  }
}

// Add to the map the calibration consts for a given key 
void DTCalibrationMap::addCell(Key theKey, const CalibConsts& calibConst) {
  if(!checkGranularity(theKey))
    cout << "[DTCalibrationMap] ERROR:" << endl
	 << "The added key is not compatible with the selected granularity"
	 << endl;

  theMap[theKey] = calibConst;
}

// Write the calibration consts to a file 
void DTCalibrationMap::writeConsts(const string& outputFileName) const {
  ofstream out(outputFileName.c_str());
  for(map<Key,CalibConsts>::const_iterator iter = theMap.begin();
      iter != theMap.end() ; iter++) {
    
    out << (*iter).first.wheel << ' '
      << (*iter).first.station << ' '
      << (*iter).first.sector << ' '
      << (*iter).first.sl << ' '
      << (*iter).first.layer << ' '
      << (*iter).first.wire << ' ';
    copy((*iter).second.begin(), (*iter).second.end(),
	 ostream_iterator<float>(out, " "));
    out << endl;
  }
}


  // Check the consistency of a given key with the selected granularity
bool DTCalibrationMap::checkGranularity(Key aKey) const {
  bool ret = true;

  // Check that the key is consistent with the given granularity
  if(theGranularity == byChamber) {
    if(aKey.sl || aKey.layer || aKey.wire) {
      ret = false;
    }
  } else if(theGranularity == bySL) {
    if(aKey.layer || aKey.wire) {
      ret = false;
    }
  } else if(theGranularity == byLayer) {
    if(aKey.wire) {
      ret = false;
    }
  } else if(theGranularity == byWire) {
    if(aKey.wire == 0) {
      ret = false;
    }
  } 
  return ret;
}
