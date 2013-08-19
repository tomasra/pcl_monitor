
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2010/05/12 15:33:46 $
 *  $Revision: 1.4 $
 *  \author G. Cerminara - INFN Torino
 */

#include "DTResolutionAnalysis.h"
#include "Histograms.h"


#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"
// #include "Geometry/Vector/interface/Pi.h"

#include "DataFormats/DTRecHit/interface/DTRecSegment4DCollection.h"
#include "DataFormats/DTRecHit/interface/DTRecHitCollection.h"

#include "Geometry/DTGeometry/interface/DTGeometry.h"
#include "Geometry/Records/interface/MuonGeometryRecord.h"

#include "CondFormats/DataRecord/interface/DTStatusFlagRcd.h"
#include "CondFormats/DTObjects/interface/DTStatusFlag.h"

#include <iterator>
#include <vector>

#include "TFile.h"
#include "TMath.h"

using namespace edm;
using namespace std;

DTResolutionAnalysis::DTResolutionAnalysis(const ParameterSet& pset, TFile* file) : theFile(file) {
  debug = pset.getUntrackedParameter<bool>("debug","false");
  // the name of the 4D rec hits collection
  theRecHits4DLabel = pset.getParameter<string>("recHits4DLabel");
  theRecHitLabel = pset.getParameter<string>("recHitLabel");

  checkNoisyChannels = pset.getUntrackedParameter<bool>("checkNoisyChannels","false");
}

DTResolutionAnalysis::~DTResolutionAnalysis(){}


void DTResolutionAnalysis::analyze(const Event& event, const EventSetup& setup) {
  if(debug)
    cout << "[DTResolutionAnalysis] Analyze #Run: " << event.id().run()
	 << " #Event: " << event.id().event() << endl;

  // Get the 4D segment collection from the event
  edm::Handle<DTRecSegment4DCollection> all4DSegments;
  event.getByLabel(theRecHits4DLabel, all4DSegments);

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

  // Loop over all chambers containing a segment
  DTRecSegment4DCollection::id_iterator chamberId;
  for (chamberId = all4DSegments->id_begin();
       chamberId != all4DSegments->id_end();
       ++chamberId) {
    // Get the range for the corresponding ChamerId
    DTRecSegment4DCollection::range  range = all4DSegments->get(*chamberId);
    int nsegm = distance(range.first, range.second);
    if(debug)
      cout << "   Chamber: " << *chamberId << " has " << nsegm
	   << " 4D segments" << endl;
    // Get the chamber
    const DTChamber* chamber = dtGeom->chamber(*chamberId);

    // Loop over the rechits of this ChamerId
    for (DTRecSegment4DCollection::const_iterator segment4D = range.first;
	 segment4D!=range.second;
	 ++segment4D) {
      if(debug){
   	cout<<"Looping on 4D rechits: -------------------------"<<endl;
	cout << "   == RecSegment dimension: " << (*segment4D).dimension() << endl;
      }
      // If Statio != 4 skip RecHits with dimension != 4
      // For the Station 4 consider 2D RecHits
      if((*segment4D).dimension() != 4) {
	if(debug)
	  cout << "[DTResolutionAnalysis]***Warning: RecSegment dimension is not 4 but "
	       << (*segment4D).dimension() << ", skipping!" << endl;
	continue;
      } 

      // Get all 1D RecHits at step 3 within the 4D segment
      vector<DTRecHit1D> recHits1D_S3;
    

      // Get 1D RecHits at Step 3 and select only events with
      // 8 hits in phi and 4 hits in theta (if any)
      const DTChamberRecSegment2D* phiSeg = (*segment4D).phiSegment();
      vector<DTRecHit1D> phiRecHits = phiSeg->specificRecHits();
      if(phiRecHits.size() != 8) {
	if(debug)
	  cout << "[DTResolutionAnalysis] Phi segments has: " << phiRecHits.size()
	       << " hits, skipping" << endl; // FIXME: info output
	continue;
      }
      copy(phiRecHits.begin(), phiRecHits.end(), back_inserter(recHits1D_S3));
      
      if((*segment4D).hasZed()) {
	const DTSLRecSegment2D* zSeg = (*segment4D).zSegment();
	vector<DTRecHit1D> zRecHits = zSeg->specificRecHits();
	if(zRecHits.size() != 4) {
	  if(debug)
	    cout << "[DTResolutionAnalysis] Theta segments has: " << zRecHits.size()
		 << " hits, skipping" << endl; // FIXME: info output
	  continue;
	}
	copy(zRecHits.begin(), zRecHits.end(), back_inserter(recHits1D_S3));
      }

      
      // Loop over 1D RecHit inside 4D segment
      for(vector<DTRecHit1D>::const_iterator recHit1D = recHits1D_S3.begin();
	  recHit1D != recHits1D_S3.end();
	  recHit1D++) {
	const DTWireId wireId = (*recHit1D).wireId();
	if(debug) {
	  cout<<"Looping on 1D rechits: -------------------------"<<endl;
	  cout << wireId << endl;
	}


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
	const DTLayer* layer = (chamber->superLayer(wireId.superlayerId()))->layer(wireId.layerId());
	float wireX = layer->specificTopology().wirePosition(wireId.wire());

	float hitY = (*recHit1D).localPosition().y();

	
	// Distance of the 1D rechit from the wire
	//float distRecHitToWire = fabs(wireX - (*recHit1D).localPosition().x());
	float distRecHitToWire = fabs(wireX - (*recHit1D).localPosition().x());
	
	// Extrapolate the segment to the z of the wire
	
	// Get wire position in chamber RF
	LocalPoint wirePosInLay(wireX,(*recHit1D).localPosition().y(),(*recHit1D).localPosition().z());
	GlobalPoint wirePosGlob = layer->toGlobal(wirePosInLay);
	LocalPoint wirePosInChamber = chamber->toLocal(wirePosGlob);

	// Segment position at Wire z in chamber local frame
	LocalPoint segPosAtZWire = (*segment4D).localPosition()
	  + (*segment4D).localDirection()*wirePosInChamber.z()/cos((*segment4D).localDirection().theta());

	// Compute the distance of the segment from the wire
	int sl = wireId.superlayer();
  

	double distSegmToWire = -1;	
	float deltaX = (*recHit1D).localPosition().x() - (layer->toLocal(chamber->toGlobal(segPosAtZWire))).x();
	float angle = -1;
	if(sl == 1 || sl == 3) {
	  // RPhi SL
	  distSegmToWire = fabs(wirePosInChamber.x() - segPosAtZWire.x());
	  angle = angleBtwPiAndPi((*segment4D).localDirection().phi());
	} else if(sl == 2) {
	  // RZ SL
	  //x in layer and y in chamber are in opposite direction in sl theta
	  distSegmToWire = fabs(segPosAtZWire.y() - wirePosInChamber.y());
	  angle = angleBtwPiAndPi((*segment4D).localDirection().theta());
	}

	if(debug) {
	  cout << "--- Layer reference frame: " << endl;
	  cout << "      wire x: " << wireX << endl;
	  cout << "      rechit x: " << (*recHit1D).localPosition().x() << endl;
	  cout << "      segment x: " << (layer->toLocal(chamber->toGlobal(segPosAtZWire))).x() << endl;
	  cout << " - dist hit-wire: " << (*recHit1D).localPosition().x() - wireX << endl;
	  cout << " - dist segm-wire: " << (layer->toLocal(chamber->toGlobal(segPosAtZWire))).x() - wireX << endl;
	  cout << " - delta x: " << (*recHit1D).localPosition().x() - (layer->toLocal(chamber->toGlobal(segPosAtZWire))).x() << endl;

	  cout << "--- Chamber reference frame: " << endl;
	  cout << "      wire x: " << wirePosInChamber.x() << endl;
	  cout << "      rechit x: " << (chamber->toLocal(layer->toGlobal((*recHit1D).localPosition()))).x() << endl;
	  cout << "      segment x: " << segPosAtZWire.x() << endl;
	  cout << " - dist hit-wire: " << (chamber->toLocal(layer->toGlobal((*recHit1D).localPosition()))).x() - wirePosInChamber.x() << endl;
	  cout << " - dist segm-wire: " << segPosAtZWire.x()-wirePosInChamber.x() << endl;
	  cout << " - delta x: " << (chamber->toLocal(layer->toGlobal((*recHit1D).localPosition()))).x() - segPosAtZWire.x() << endl;
	  

	}


	if(fabs(distSegmToWire) > 10)
	  cout << "  Warning: dist segment-wire: " << distSegmToWire << endl;

	//double residual = distRecHitToWire - distSegmToWire;

	// Get segment etrapolation pos. in layer RF
	//LocalPoint segPosExtrInLayer = layer->toLocal(chamber->toGlobal(segPosAtZWire));
	//	const DTSuperLayer* superlayer = chamber->superLayer(wireId.superlayerId());
	//	LocalPoint segPosExtrInSL = superlayer->toLocal(chamber->toGlobal(segPosAtZWire));

	
	
	// plots for different angles
	theFile->cd();
	HRes1DHits * histoPtr = 0;
	if(fabs(angle) < 5.*TMath::Pi()/180.) {
	  histoPtr = histosPerSL_angle5[wireId.superlayerId()];
	} else if(fabs(angle) > 15*TMath::Pi()/180. && fabs(angle) < 20*TMath::Pi()/180.) {
	  histoPtr = histosPerSL_angle15to20[wireId.superlayerId()];
	} else if(fabs(angle) > 25*TMath::Pi()/180. && fabs(angle) < 30*TMath::Pi()/180.) {
	  histoPtr = histosPerSL_angle25to30[wireId.superlayerId()];
	}

	histoPtr->Fill(distRecHitToWire - distSegmToWire,
		       distSegmToWire,
		       deltaX,
		       hitY,
		       angle,
		       sqrt((*recHit1D).localPositionError().xx()));

	histosPerSL[wireId.superlayerId()]->Fill(distRecHitToWire - distSegmToWire,
						 distSegmToWire,
						 deltaX,
						 hitY,
						 angle,
						 sqrt((*recHit1D).localPositionError().xx()));

	if(debug) {
	  cout << "     Dist. segment extrapolation from wire (cm): " << distSegmToWire << endl;
	  cout << "     Dist. RecHit from wire (cm): " << distRecHitToWire << endl;
	  cout << "     Residual (cm): " << distRecHitToWire - distSegmToWire << endl;
	  cout << "     deltaX: " << deltaX << endl;	  
	}

      }// End of loop over 1D RecHit inside 4D segment
      
    }// End of loop over the segm4D of this ChamerId
 }
  // -----------------------------------------------------------------------------


  



}


  
// Book a set of histograms for a given SL
void DTResolutionAnalysis::bookHistos(DTSuperLayerId slId) {
  if(debug)
    cout << "   Booking histos for SL: " << slId << endl;

  // Compose the chamber name
  stringstream wheel; wheel << slId.wheel();	
  stringstream station; station << slId.station();	
  stringstream sector; sector << slId.sector();	
  stringstream superLayer; superLayer << slId.superlayer();	

  
  string slHistoName =
    "W" + wheel.str() +
    "_Sec" + sector.str() +
    "_St" + station.str() +
    "_SL" + superLayer.str();
  theFile->cd();
  histosPerSL[slId] = new HRes1DHits(slHistoName);

  string slHistoName_angle5 = "angle5_" + slHistoName;
  histosPerSL_angle5[slId] = new HRes1DHits(slHistoName_angle5);

  string slHistoName_angle15to20 = "angle15to20_" + slHistoName;
  histosPerSL_angle15to20[slId] = new HRes1DHits(slHistoName_angle15to20);

  string slHistoName_angle25to30 = "angle25to30_" + slHistoName;
  histosPerSL_angle25to30[slId] = new HRes1DHits(slHistoName_angle25to30);


}


void DTResolutionAnalysis::endJob() {
  // Write all histos to file
  theFile->cd();
  for(map<DTSuperLayerId, HRes1DHits* >::const_iterator slIdAndHisto = histosPerSL.begin();
      slIdAndHisto != histosPerSL.end(); ++slIdAndHisto) {
    (*slIdAndHisto).second->Write();
  }

  for(map<DTSuperLayerId, HRes1DHits* >::const_iterator slIdAndHisto = histosPerSL_angle5.begin();
      slIdAndHisto != histosPerSL_angle5.end(); ++slIdAndHisto) {
    (*slIdAndHisto).second->Write();
  }

  for(map<DTSuperLayerId, HRes1DHits* >::const_iterator slIdAndHisto = histosPerSL_angle15to20.begin();
      slIdAndHisto != histosPerSL_angle15to20.end(); ++slIdAndHisto) {
    (*slIdAndHisto).second->Write();
  }

  for(map<DTSuperLayerId, HRes1DHits* >::const_iterator slIdAndHisto = histosPerSL_angle25to30.begin();
      slIdAndHisto != histosPerSL_angle25to30.end(); ++slIdAndHisto) {
    (*slIdAndHisto).second->Write();
  }
}








// BeginJob
void DTResolutionAnalysis::beginJob() {
  
  // book histos
  for(int wheel = -2; wheel != 3; ++wheel) { // Loop over wheel
    for(int station = 1; station != 5; ++station) { // Loop over stations
      for(int sector = 1; sector <= 14; ++sector) { // Loop over sectors
	if((sector == 13 || sector == 14) && station != 4) continue;
	for(int sl = 1; sl !=4; ++sl) { // loop over SLs
	  if(sl == 2 && station == 4) continue;
	  DTSuperLayerId slId(wheel, station, sector, sl);
	  bookHistos(slId);
	}
      }
    }
  }
}


double DTResolutionAnalysis::angleBtwPiAndPi(double angle) const {
  while(angle >= TMath::Pi()) angle -= TMath::Pi();
  while(angle < 0.) angle += TMath::Pi();
  return angle;
}
