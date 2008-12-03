
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2008/10/27 16:25:25 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - INFN Torino
 */

#include "DTResolution2DAnalysis.h"
#include "Histograms.h"


#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"
// #include "Geometry/Vector/interface/Pi.h"

#include "DataFormats/DTRecHit/interface/DTRecSegment2DCollection.h"
#include "DataFormats/DTRecHit/interface/DTRecHitCollection.h"

#include "Geometry/DTGeometry/interface/DTGeometry.h"
#include "Geometry/Records/interface/MuonGeometryRecord.h"

#include "CalibMuon/DTDigiSync/interface/DTTTrigSyncFactory.h"
#include "CalibMuon/DTDigiSync/interface/DTTTrigBaseSync.h"
#include "CondFormats/DataRecord/interface/DTStatusFlagRcd.h"
#include "CondFormats/DTObjects/interface/DTStatusFlag.h"

#include <iterator>
#include <vector>

#include "TFile.h"

using namespace edm;
using namespace std;

DTResolution2DAnalysis::DTResolution2DAnalysis(const ParameterSet& pset, TFile* file) : theFile(file) {
  debug = pset.getUntrackedParameter<bool>("debug","false");
  // the name of the 4D rec hits collection
  theRecHits2DLabel = pset.getParameter<string>("recHits2DLabel");
  theRecHitLabel = pset.getParameter<string>("recHitLabel");

  checkNoisyChannels = pset.getUntrackedParameter<bool>("checkNoisyChannels","false");

}

DTResolution2DAnalysis::~DTResolution2DAnalysis(){}


void DTResolution2DAnalysis::analyze(const Event& event, const EventSetup& setup) {
  if(debug)
    cout << "[DTResolution2DAnalysis] Analyze #Run: " << event.id().run()
	 << " #Event: " << event.id().event() << endl;

  // Get the 4D segment collection from the event
  edm::Handle<DTRecSegment2DCollection> segment2Ds;
  event.getByLabel(theRecHits2DLabel, segment2Ds);

  // Get the rechit collection from the event
  Handle<DTRecHitCollection> dtRecHits;
  event.getByLabel(theRecHitLabel, dtRecHits);

  // Get the DT Geometry
  ESHandle<DTGeometry> dtGeom;
  setup.get<MuonGeometryRecord>().get(dtGeom);
  
  // Get the map of noisy channels
  ESHandle<DTStatusFlag> statusMap;
  if(checkNoisyChannels) {
    setup.get<DTStatusFlagRcd>().get(statusMap);
    }
  

  DTRecSegment2DCollection::id_iterator slId;
  for (slId = segment2Ds->id_begin();
       slId != segment2Ds->id_end();
       ++slId){
    
    DTRecSegment2DCollection::range range = segment2Ds->get(*slId);
    int nsegm = distance(range.first, range.second);
    if(debug)
      cout << "   Sl: " << *slId << " has " << nsegm
	   << " 2D segments" << endl;
    // Get the sl
    const DTSuperLayer* sl = dtGeom->superLayer(*slId);
    
    // Loop over the recHits of this slId
    for (DTRecSegment2DCollection::const_iterator segment2D = range.first;
	 segment2D!=range.second;
	 ++segment2D){
      if(debug)
	cout << "   == RecSegment dimension: " << (*segment2D).dimension() << endl;
      // Check the dimension
	if((*segment2D).dimension() != 2) {
	  cout << "[DTSegment2DQuality]***Error: This is not 2D segment!!!" << endl;
	  abort();
	}

      // Get all 1D RecHits at step 3 within the 2D segment
	vector<DTRecHit1D> recHits1D_S2= (*segment2D).specificRecHits();;
    
      // Get 1D RecHits at Step 3 and select only events with
      // 8 hits in phi and 4 hits in theta (if any)
      if(recHits1D_S2.size() != 4) {
	if(debug)
	  cout << "[DTResolution2DAnalysis] segments has: " << recHits1D_S2.size()
	       << " hits, skipping" << endl; // FIXME: info output
	continue;
      }

      // Loop over 1D RecHit inside 2D segment
      for(vector<DTRecHit1D>::const_iterator recHit1D = recHits1D_S2.begin();
	  recHit1D != recHits1D_S2.end();
	  recHit1D++) {
	const DTWireId wireId = (*recHit1D).wireId();
	 
	// Check for noisy channels and skip them
	if(checkNoisyChannels) {
	  bool isNoisy = false;
	  bool isFEMasked = false;
	  bool isTDCMasked = false;
	  bool isTrigMask = false;
	  bool isDead = false;
	  bool isNohv = false;
	  statusMap->cellStatus(wireId, isNoisy, isFEMasked, isTDCMasked, isTrigMask, isDead, isNohv);
	  if(isNoisy) {
	    if(debug)
	      cout << "Wire: " << wireId << " is noisy, skipping!" << endl;
	    continue;
	  }      
	}

	// Get the layer and the wire position
	const DTLayer* layer = sl->layer(wireId.layerId());
	float wireX = layer->specificTopology().wirePosition(wireId.wire());
	
	// Distance of the 1D rechit from the wire
	//float distRecHitToWire = fabs(wireX - (*recHit1D).localPosition().x());
	float distRecHitToWire = wireX - (*recHit1D).localPosition().x();
	
	LocalPoint segmPos = (*segment2D).localPosition();
	// Extrapolate the segment to the z of the wire
	
	// Get wire position in sl RF
	LocalPoint wirePosInLay(wireX,0,0);
	GlobalPoint wirePosGlob = layer->toGlobal(wirePosInLay);
	LocalPoint wirePosInSl = sl->toLocal(wirePosGlob);

	// Segment position at Wire z in sl local frame
	LocalPoint segPosAtZWire = (*segment2D).localPosition()
	  + (*segment2D).localDirection()*wirePosInSl.z()/cos((*segment2D).localDirection().theta());

	double distSegmToWire = wirePosInSl.x() - segPosAtZWire.x();

	if(distSegmToWire > 2.1)
	  cout << "  Warning: dist segment-wire: " << distSegmToWire << endl;

	//double residual = distRecHitToWire - distSegmToWire;

	fillHistos(wireId.superlayerId(), distSegmToWire, distRecHitToWire, segmPos.x());
      
	if(debug) {
	  cout << "     Dist. segment extrapolation - wire (cm): " << distSegmToWire << endl;
	  cout << "     Dist. RecHit - wire (cm): " << distRecHitToWire << endl;
	  cout << "     Residual (cm): " << distRecHitToWire - distSegmToWire << endl;
	}
			  
      }// End of loop over 1D RecHit inside 2D segment
      
    }// End of loop over the segm2D of this slId
 }
  // -----------------------------------------------------------------------------
}


  
// Book a set of histograms for a given SL
void DTResolution2DAnalysis::bookHistos(DTSuperLayerId slId) {
  if(debug)
    cout << "   Booking histos for SL: " << slId << endl;

  // Compose the chamber name
  stringstream wheel; wheel << slId.wheel();	
  stringstream station; station << slId.station();	
  stringstream sector; sector << slId.sector();	
  stringstream superLayer; superLayer << slId.superlayer();	

  
  string slHistoName =
    "_W" + wheel.str() +
    "_St" + station.str() +
    "_Sec" + sector.str() +
    "_SL" + superLayer.str();
  theFile->cd();
  histosPerSL[slId] = new HRes2DSL(slHistoName);
}

// Fill a set of histograms for a given SL 
void DTResolution2DAnalysis::fillHistos(DTSuperLayerId slId,
				      float distExtr,
				      float distRecHit,
				      float xExtr) {
  // FIXME: optimization of the number of searches
  if(histosPerSL.find(slId) == histosPerSL.end()) {
    bookHistos(slId);
  }
  theFile->cd();
  histosPerSL[slId]->Fill(distExtr, distRecHit, xExtr);                          
}




void DTResolution2DAnalysis::endJob() {
  // Write all histos to file
  theFile->cd();
  for(map<DTSuperLayerId, HRes2DSL* >::const_iterator slIdAndHisto = histosPerSL.begin();
      slIdAndHisto != histosPerSL.end(); ++slIdAndHisto) {
    (*slIdAndHisto).second->Write();
  }
}

