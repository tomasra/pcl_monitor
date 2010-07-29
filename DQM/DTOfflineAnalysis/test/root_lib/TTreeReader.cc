/*
 *  See header file for a description of this class.
 *
 *  $Date: 2010/05/13 09:34:58 $
 *  $Revision: 1.6 $
 *  \author G. Cerminara - INFN Torino
 */

#include "TTreeReader.h"

#include "TString.h"
#include "TFile.h"
#include "TNtuple.h"
#include "DTSegmentObject.h"
#include "DTHitObject.h"
#include "DTMuObject.h"
#include "Histograms.h"
#include "Utils.h"


#include <iostream>
#include <sstream>
#include <vector>
#include <cmath>

using namespace std;


TTreeReader::TTreeReader(const TString& fileName, const TString& outputFile) : theOutFile(outputFile),
									       theGranularity(-1),
									       nevents(0),
									       filterEvents(0),
									       debug(0) {
  // open the file containing the tree
  TFile *file = new TFile(fileName.Data());
  if(file == 0) {
    cerr << "[TTreeReader]***Error: File: " << fileName << " does not exist!" << endl;
    return;
  }

  // Retrieve the TNtuple
  tree = (TNtuple *) file->Get("DTSegmentTree");

  segments = new TClonesArray("DTSegmentObject");
  
  cout << "Read File: " << fileName << endl;
  cout << "Opening tree: " << tree->GetName() << " with "
       << tree->GetEntries() << " entries" << endl;
  setBranchAddresses();

  // default values
  setGranularity("SL");
  
}

TTreeReader::~TTreeReader(){}



void TTreeReader::setBranchAddresses() {
  // set the addresses of the tree variables
  tree->SetBranchAddress("segments",&segments);
  tree->SetBranchAddress("muonCands",&muons);
  tree->SetBranchAddress("Run",&run);

}


TH2F *hDeltaSectVsDeltaStat = 0;
HSegment *hAll;

void TTreeReader::begin() {
  cout << "Begin" << endl;

  hDeltaSectVsDeltaStat = new TH2F("hDeltaSectVsDeltaStat","hDeltaSectVsDeltaStat", 4, 0, 4, 12, 0, 12);
  hAll = new HSegment("ALL");

  // build the histos with the desired granularity
  for(int wheel = -2; wheel != 3; ++wheel) {   // loop over wheels
    for(int station = 1; station != 5; ++station) { // loop over stations

//       TString setName = "AllSect";
//       DTDetId chId(wheel, station, 0, 0, 0, 0);
//       if(histosSeg[setName].find(chId) == histosSeg[setName].end()) {
// 	histosSeg[setName][chId] = new HSegment(Utils::getHistoNameFromDetIdAndSet(chId, setName));
//       }
//       if(histosRes[setName].find(chId) == histosRes[setName].end()) {
//       	histosRes[setName][chId] = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(chId, setName));
//       }

      for(int sector = 1; sector != 15; ++sector) { // loop over sectors
	if(station != 4 && (sector == 13 || sector == 14)) continue;

	// book the segment histos
	// loop over set of cuts
	for(map<TString, DTCut>::const_iterator set = cutSets.begin();   
	    set != cutSets.end();
	    ++set) {
	  TString setName = (*set).first;
	  //DTDetId chId(wheel, station, sector, 0, 0, 0);
	  DTDetId chId = buildDetid(wheel, station, sector, 0, 0, 0);
	  if(histosSeg[setName].find(chId) == histosSeg[setName].end()) {
	    histosSeg[setName][chId] = new HSegment(Utils::getHistoNameFromDetIdAndSet(chId, setName));
	  }
	}

	for(int sl = 1; sl != 4; ++sl) { // loop over SLs
	  if(station == 4 && sl == 2) continue;
	  for(int layer = 1; layer != 5; ++layer) {
	    DTDetId detId = buildDetid(wheel, station, sector, sl, layer, 0);
// 	    TString name = Utils::getHistoNameFromDetId(detId);
		
	    // loop over set of cuts
	    for(map<TString, DTCut>::const_iterator set = cutSets.begin();   
		set != cutSets.end();
		++set) {
	      TString setName = (*set).first;
	      if(histosRes[setName].find(detId) == histosRes[setName].end()) {
		cout << "book histo for: " << Utils::getHistoNameFromDetIdAndSet(detId, setName) << endl;
		histosRes[setName][detId] = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId, setName));
	      }
	    }

	  }
	}
      }
    }
  }
}

void TTreeReader::processEvent(int entry) {
  if(entry%10000 == 0 ||  debug > 2) {
    cout << "-----  Process event " << entry << endl;
  }

  for(int iSegm=0; iSegm < segments->GetEntriesFast(); iSegm++) { // loop over segments 

    DTSegmentObject *oneSeg = (DTSegmentObject *) segments->At(iSegm);

    if(iSegm != 0) {
      for(int iPrev = 0; iPrev < iSegm; ++iPrev) {
	DTSegmentObject *prevSeg = (DTSegmentObject *) segments->At(iPrev);
	hDeltaSectVsDeltaStat->Fill(fabs(prevSeg->station - oneSeg->station), fabs(prevSeg->sector - oneSeg->sector));	
      }
    }
    hAll->Fill(oneSeg->nHits,
	       oneSeg->nHitsPhi,
	       oneSeg->nHitsTheta,
	       oneSeg->proj,
	       oneSeg->phi,
	       oneSeg->theta,
	       -1,
	       oneSeg->chi2,
	       oneSeg->t0SegPhi,
	       oneSeg->t0SegTheta,
	       oneSeg->vDriftCorrPhi);

    bool passHqPhiV = false; 
    DTDetId chId = buildDetid(oneSeg->wheel, oneSeg->station, oneSeg->sector, 0, 0, 0);
    // select segments
    vector<TString> passedCuts;
    // loop over set of cuts
    for(map<TString, DTCut>::const_iterator set = cutSets.begin();   
	set != cutSets.end();
	++set) {
      if((*set).second.selectSegm(oneSeg)) {
	passedCuts.push_back((*set).first);
	// fill the segment related histos

	histosSeg[(*set).first][chId]->Fill(oneSeg->nHits,
					    oneSeg->nHitsPhi,
					    oneSeg->nHitsTheta,
					    oneSeg->proj,
					    oneSeg->phi,
					    oneSeg->theta,
					    -1,
					    oneSeg->chi2,
					    oneSeg->t0SegPhi,
					    oneSeg->t0SegTheta,
					    oneSeg->vDriftCorrPhi);
	if((*set).first == "hqPhiV") passHqPhiV = true;
      }
    }
    if(passedCuts.size() == 0) continue;

//     passHqPhiV = true;
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
      int segSl = hitObj->sl;
      if((theGranularity == 3 || theGranularity == 4) &&   hitObj->sl == 3) segSl = 1;
      DTDetId detIdForPlot = buildDetid(oneSeg->wheel, oneSeg->station, oneSeg->sector,
					segSl, hitObj->layer, hitObj->wire);
      vector<TString>::const_iterator cut =  passedCuts.begin();
//       for(// set<TString>::const_iterator cut = passedCuts.begin();
// 	  cut != passedCuts.end(); ++cut) {
      while(cut != passedCuts.end()) {
	histosRes[*cut][detIdForPlot]->Fill(hitObj->resDist, hitObj->distFromWire, hitObj->resPos,hitObj->X,
					    hitObj->Y, hitObj->angle, hitObj->sigmaPos);
	++cut;
      }
    }
  }  
}


void TTreeReader::end() {
  cout << "End, # processed events: " << nevents << endl;

  // Create the root file
  TFile *theFile = new TFile(theOutFile.Data(), "RECREATE");
  theFile->cd();

  // Write the histos
  for(map<TString, DTCut>::const_iterator cut = cutSets.begin();
      cut != cutSets.end(); ++cut) {
    map<DTDetId, HRes1DHits *> theHistosRes = histosRes[(*cut).first];
    for(map<DTDetId, HRes1DHits *>::const_iterator hist =  theHistosRes.begin();
	hist != theHistosRes.end(); ++hist) {
      (*hist).second->Write();
    }
    map<DTDetId, HSegment *> theHistosSeg = histosSeg[(*cut).first];
    for(map<DTDetId, HSegment *>::const_iterator hist =  theHistosSeg.begin();
	hist != theHistosSeg.end(); ++hist) {
      (*hist).second->Write();
    }
  }
  hDeltaSectVsDeltaStat->Write();
  hAll->Write();
  theFile->Close();
}

void TTreeReader::analyse(const int nEventMax) {
  int max = tree->GetEntries();
  if(nEventMax != -1) max = nEventMax;
  begin();
  for(int i = 0; i < max; i++) {

    tree->GetEntry(i);
    
    if (filterEvents==1) {
      bool tagEvent=false;
      // Event quality selection
      // Select data taking periods
      if (run< 50000) { // MC
	tagEvent=true;
      } else {  // data
	if (run < 137754) { //Initial period
	  continue;
	} else if (run < 139830) { //first round of corrections
	  continue;
	} else { //Second round of corrections
	  //continue;
	} 
    
	for(int iMu=0; iMu < muons->GetEntriesFast(); iMu++) { // loop over events
	  DTMuObject *oneMu = (DTMuObject *) muons->At(iMu);	
	
	  if (fabs(oneMu->eta)<1.2 && oneMu->type!=5) tagEvent=true;
	} 
      }
      if (!tagEvent) continue;
    }
  

    processEvent(i);
    nevents++;
  }
  end();
}




// build a detid depending on the wanted ganularity
DTDetId TTreeReader::buildDetid(int wheel, int station, int sector, int sl, int layer, int wire) const {
  if(theGranularity == 1) { // SL
    return DTDetId(wheel, station, sector, sl, 0, 0);
  } else if(theGranularity == 2) { // Station
    return DTDetId(wheel, station, 0, 0, 0, 0);
  } else if(theGranularity == 3) { // statByView : Sl3 is also merged with 1
    return DTDetId(wheel, station, 0, sl, 0, 0);
  } else if(theGranularity == 4) { // chamberByView : Sl3 is also merged with 1
    return DTDetId(wheel, station, sector, sl, 0, 0);
  } else if(theGranularity == 5) { // statBySL
    return DTDetId(wheel, station, 0, sl, 0, 0);
  }
  return DTDetId(0, 0, 0, 0, 0, 0);
  
}


void TTreeReader::setGranularity(const TString& granularity) {
  if(granularity == "SL" || granularity == "sl") {
    theGranularity = 1;
    cout << "Granularity: SL" << endl;
  } else if(granularity == "Station" || granularity == "station") {
    cout << "Granularity: Station" << endl;
    theGranularity = 2;
  } else if(granularity == "statByView") {
    cout << "Granularity: Station by view" << endl;
    theGranularity = 3;
  }  else if(granularity == "chamberByView") {
    cout << "Granularity: Chamber by view" << endl;
    theGranularity = 4;
  } else if(granularity == "statBySL") {
    cout << "Granularity: Station by SL" << endl;
    theGranularity = 5;
  }
}
// TString TTreeReader::getNameFromDetId(const DTDetId& detId) const {
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





void TTreeReader::setDebug(int dbg) {
  debug = dbg;
}



void TTreeReader::setCuts(const TString& set, const DTCut& cut) {
  cutSets[set] = cut;
  cout << "--- Set cut: " << set << endl;
  cout << cut << endl;

}
