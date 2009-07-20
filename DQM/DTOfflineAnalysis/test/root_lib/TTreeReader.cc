/*
 *  See header file for a description of this class.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - INFN Torino
 */

#include "TTreeReader.h"

#include "TString.h"
#include "TFile.h"
#include "TNtuple.h"
#include "DTSegmentObject.h"
#include "DTHitObject.h"
#include "Histograms.h"



#include <iostream>
#include <sstream>


using namespace std;


TTreeReader::TTreeReader(const TString& fileName, const TString& outputFile) : theOutFile(outputFile),
									       theGranularity(-1),
									       nevents(0) {
  // open the file containing the tree
  TFile *file = new TFile(fileName.Data());
  // Retrieve the TNtuple
  tree = (TNtuple *) file->Get("DTSegmentTree");

  segments = new TClonesArray("DTSegmentObject");
  
  cout << "Read File: " << fileName << endl;
  cout << "Opening tree: " << tree->GetName() << " with "
       << tree->GetEntries() << " entries" << endl;
  setBranchAddresses();

  // default values
  setGranularity("SL");

  // set the cuts here
  NHITSMIN = 0;
  PHI_MIN = -9999.;
  PHI_MAX = 9999.;
  THETA_MIN = -9999.;
  THETA_MAX = 9999.;


}

TTreeReader::~TTreeReader(){}



void TTreeReader::setBranchAddresses() {
  // set the addresses of the tree variables
  tree->SetBranchAddress("segments",&segments);
}




void TTreeReader::begin() {
  cout << "Begin" << endl;

  // build the histos with the desired granularity
  for(int wheel = -2; wheel != 3; ++wheel) {   // loop over wheels
    for(int station = 1; station != 5; ++station) { // loop over stations
      for(int sector = 1; sector != 15; ++sector) { // loop over sectors
	if(station != 4 && (sector == 13 || sector == 14)) continue;
	for(int sl = 1; sl != 4; ++sl) { // loop over SLs
	  if(station == 4 && sl == 2) continue;
	  for(int layer = 1; layer != 5; ++layer) {
	    DTDetId detId = buildDetid(wheel, station, sector, sl, layer, 0);
	    if(histos.find(detId) == histos.end()) {
	      TString name = getNameFromDetId(detId);
	      histos[detId] = new HRes1DHits(name);
	    }
	  }
	}
      }
    }
  }
}

void TTreeReader::processEvent(int entry) {
  int debug = 0;
  if(entry%100 || debug > 2) {
    cout << "Process event " << entry << endl;
  }
  
  
  for(int iSegm=0; iSegm < segments->GetEntriesFast(); iSegm++) { // loop over segments 

    DTSegmentObject *oneSeg = (DTSegmentObject *) segments->At(iSegm);

    // select segments
    if(oneSeg->nHits < NHITSMIN) continue;
    if(oneSeg->phi < PHI_MIN || oneSeg->phi > PHI_MAX) continue;
    if(oneSeg->theta < THETA_MIN || oneSeg->theta > THETA_MAX) continue;
    

    for(int iHit = 0; iHit != oneSeg->nHits; ++iHit) { // loop over the hits belonging to the segment
      DTHitObject * hitObj = (DTHitObject *) oneSeg->hits->At(iHit);
      DTDetId detId(oneSeg->wheel, oneSeg->station, oneSeg->sector,
		    hitObj->sl, hitObj->layer, hitObj->wire);
      DTDetId detIdForPlot = buildDetid(oneSeg->wheel, oneSeg->station, oneSeg->sector,
					hitObj->sl, hitObj->layer, hitObj->wire);

      HRes1DHits *histoRes = histos[detIdForPlot];
      histoRes->Fill(hitObj->resDist, hitObj->distFromWire, hitObj->resPos,
		     hitObj->Y, hitObj->angle, hitObj->sigmaPos);
    }
  }  
}


void TTreeReader::end() {
  cout << "End, # processed events: " << nevents << endl;

  // Create the root file
  TFile *theFile = new TFile(theOutFile.Data(), "RECREATE");
  theFile->cd();

  // Write the histos
  for(map<DTDetId, HRes1DHits *>::const_iterator hist =  histos.begin();
      hist != histos.end(); ++hist) {
    (*hist).second->Write();
  }
  theFile->Close();
}

void TTreeReader::analyse(const int nEventMax) {
  int max = tree->GetEntries();
  if(nEventMax != -1) max = nEventMax;
  begin();
  for(int i = 0; i < max; i++) {
    tree->GetEntry(i);
    processEvent(i);
    nevents++;
  }
  end();
}




// build a detid depending on the wanted ganularity
DTDetId TTreeReader::buildDetid(int wheel, int station, int sector, int sl, int layer, int wire) const {
  if(theGranularity == 1) {
    return DTDetId(wheel, station, sector, sl, 0, 0);
  }
  
  return DTDetId(0, 0, 0, 0, 0, 0);
  
}


void TTreeReader::setGranularity(const TString& granularity) {
  if(granularity == "SL" || granularity == "sl") theGranularity = 1;
}


TString TTreeReader::getNameFromDetId(const DTDetId& detId) const {
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



void TTreeReader::setMinNHits(int nHits) {
  NHITSMIN = nHits;
}



void TTreeReader::setSegmPhiAngle(float min, float max) {
  PHI_MIN = min;
  PHI_MAX = max;
}



void TTreeReader::setSegmThetaAngle(float min, float max) {
  THETA_MIN = min;
  THETA_MAX = max;
}




