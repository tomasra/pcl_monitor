/*
 *  See header file for a description of this class.
 *
 *  $Date: 2009/07/27 12:35:44 $
 *  $Revision: 1.3 $
 *  \author G. Cerminara - INFN Torino
 */

#include "SimTreeReader.h"

#include "TString.h"
#include "TFile.h"
#include "TNtuple.h"
#include "DTSegmentObject.h"
#include "DTHitObject.h"
#include "Histograms.h"
#include "Utils.h"


#include <iostream>
#include <sstream>
#include <vector>
using namespace std;


SimTreeReader::SimTreeReader(const TString& outputFile) : theOutFile(outputFile),
							  theGranularity(-1),
							  nevents(0),
							  debug(0) {
  // open the file containing the tree
  
  // default values
  setGranularity("SL");

}



void SimTreeReader::addInputFile(int index, const TString& fileName) {
  TFile *file = new TFile(fileName.Data());
  if(file == 0) {
    cerr << "[SimTreeReader]***Error: File: " << fileName << " does not exist!" << endl;
    return;
  }
  
  // Retrieve the TNtuple
  treeMap[index] = (TTree *) file->Get("DTSegmentTree");
  
  segmContMap[index] = new TClonesArray("DTSegmentObject");
  
  cout << "Read File: " << fileName << endl;
  cout << "Opening tree: " <<   treeMap[index]->GetName() << " with "
       <<   treeMap[index]->GetEntries() << " entries" << endl;

  treeMap[index]->SetBranchAddress("segments",&segmContMap[index]);

}




SimTreeReader::~SimTreeReader(){}





void SimTreeReader::begin() {
  cout << "Begin" << endl;
}

void SimTreeReader::processEvent(int fileIndex, int entry) {
  if(entry%100000 == 0 ||  debug > 2) {
    cout << "-----  Process event " << entry << endl;
  }
  
  // point to the right collection
  segments = segmContMap[fileIndex];

  
  for(int iSegm=0; iSegm < segments->GetEntriesFast(); iSegm++) { // loop over segments 

    DTSegmentObject *oneSeg = (DTSegmentObject *) segments->At(iSegm);

    bool passHqPhiV = false; 
    DTDetId chId(oneSeg->wheel, oneSeg->station, oneSeg->sector, 0, 0, 0);
    // select segments
    vector<TString> passedCuts;
    // loop over set of cuts
    for(map<TString, DTCut>::const_iterator set = cutSets.begin();   
	set != cutSets.end();
	++set) {
      if((*set).second.selectSegm(oneSeg)) {
	passedCuts.push_back((*set).first);
	if((*set).first == "hqPhiV") passHqPhiV = true;
      }
    }
    if(passedCuts.size() == 0) continue;

    if(passHqPhiV && debug > 5) {
      cout << "--- New Segment: " << endl;
      cout << chId << endl;
      cout << " pos: X: " << oneSeg->Xsl << " Y: " << oneSeg->Ysl << " Z: " << oneSeg->Zsl << endl;
      cout << " theta: " << oneSeg->theta << " phi: " << oneSeg->phi << endl;
      for(int i = 0; i != 3; ++i) {
	cout << " ttrig SL" << i+1 << ": "
	     << oneSeg->tTrigMean[i] + oneSeg->tTrigKfact[i] * oneSeg->tTrigSigma[i] << endl;
      }
    }

     
    for(int iHit = 0; iHit != oneSeg->nHits; ++iHit) { // loop over the hits belonging to the segment
      DTHitObject * hitObj = (DTHitObject *) oneSeg->hits->At(iHit);
      DTDetId detId(oneSeg->wheel, oneSeg->station, oneSeg->sector,
		    hitObj->sl, hitObj->layer, hitObj->wire);
      if(passHqPhiV && debug > 5) {
	cout << "  - Hit on wire: " << detId << endl;
	cout << "       pos X: " << hitObj->X << " Y: " << hitObj->Y << " Z: " << hitObj->Z << endl;
	cout << "       res dist: " << hitObj->resDist << endl;
	cout << "       digi time: " << hitObj->digiTime << endl;
      }
    }
  }  
}


void SimTreeReader::end() {
  cout << "End, # processed events: " << nevents << endl;

  // Create the root file
  TFile *theFile = new TFile(theOutFile.Data(), "RECREATE");
  theFile->cd();

  theFile->Close();
}

void SimTreeReader::analyse(const int nEventMax) {
  int fileIndex = 0;
  TTree *tree = treeMap[fileIndex]; 
  int max = tree->GetEntries();
  if(nEventMax != -1) max = nEventMax;
  begin();
  for(int i = 0; i < max; i++) {
    tree->GetEntry(i);
    processEvent(fileIndex, i);
    nevents++;
  }
  end();
}




// build a detid depending on the wanted ganularity
DTDetId SimTreeReader::buildDetid(int wheel, int station, int sector, int sl, int layer, int wire) const {
  if(theGranularity == 1) {
    return DTDetId(wheel, station, sector, sl, 0, 0);
  }
  
  return DTDetId(0, 0, 0, 0, 0, 0);
  
}


void SimTreeReader::setGranularity(const TString& granularity) {
  if(granularity == "SL" || granularity == "sl") theGranularity = 1;
}


// TString SimTreeReader::getNameFromDetId(const DTDetId& detId) const {
//   stringstream wheelStr; 
//   if(detId.wheel == 0) wheelStr << "all";
//   else wheelStr << detId.wheel;

//   stringstream stationStr; 
//   if(detId.station == 0) stationStr << "all";
//   else stationStr << detId.station;

//   stringstream sectorStr; 
//   if(detId.sector == 0) sectorStr << "all";
//   else sectorStr << detId.sector;

//   stringstream slStr; 
//   if(detId.sl == 0) slStr << "all";
//   else slStr << detId.sl;

//   stringstream layerStr; 
//   if(detId.layer == 0) layerStr << "all";
//   else layerStr << detId.layer;

//   string namestr = "Wh" + wheelStr.str() +
//     "_St" + stationStr.str() + 
//     "_Se" + sectorStr.str();
    
//   if(detId.sl != 0) {
//     namestr = namestr + "_SL" + slStr.str();
//   }
//   if(detId.layer != 0) {
//     namestr = namestr + "_L" + layerStr.str();
//   }

//   return TString(namestr.c_str());
// }





void SimTreeReader::setDebug(int dbg) {
  debug = dbg;
}



void SimTreeReader::setCuts(const TString& set, const DTCut& cut) {
  cutSets[set] = cut;
  cout << "--- Set cut: " << set << endl;
  cout << cut << endl;

}
