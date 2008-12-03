
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2008/10/27 16:25:25 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - INFN Torino
 */

#include "DTTimeBoxMeanTimerAnalysis.h"
#include "Histograms.h"


#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"


#include "DataFormats/DTRecHit/interface/DTRecSegment4DCollection.h"
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

DTTimeBoxMeanTimerAnalysis::DTTimeBoxMeanTimerAnalysis(const ParameterSet& pset, TFile* file) : theFile(file) {
  debug = pset.getUntrackedParameter<bool>("debug","false");
  // the name of the 4D rec hits collection
  theRecHits4DLabel = pset.getParameter<string>("recHits4DLabel");
  theRecHitLabel = pset.getParameter<string>("recHitLabel");

   doSubtractT0 = pset.getUntrackedParameter<bool>("doSubtractT0","false");
  // Get the synchronizer
  if(doSubtractT0) {
  theSync = DTTTrigSyncFactory::get()->create(pset.getParameter<string>("tTrigMode"),
						pset.getParameter<ParameterSet>("tTrigModeConfig"));
  }else {
    theSync = 0;
  }

  checkNoisyChannels = pset.getUntrackedParameter<bool>("checkNoisyChannels","false");

}

DTTimeBoxMeanTimerAnalysis::~DTTimeBoxMeanTimerAnalysis(){}


void DTTimeBoxMeanTimerAnalysis::analyze(const Event& event, const EventSetup& setup) {
  if(debug)
    cout << "[DTTimeBoxMeanTimerAnalysis] Analyze #Run: " << event.id().run()
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
  
  if(doSubtractT0)
    theSync->setES(setup);


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
      if(debug)
   	cout<<"Looping on 4D rechits: -------------------------"<<endl;
      
      // If Statio != 4 skip RecHits with dimension != 4
      // For the Station 4 consider 2D RecHits
      if((*segment4D).dimension() != 4) {
	if(debug)
	  cout << "[DTTimeBoxMeanTimerAnalysis]***Warning: RecSegment dimension is not 4 but "
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
	  cout << "[DTTimeBoxMeanTimerAnalysis] Phi segments has: " << phiRecHits.size()
	       << " hits, skipping" << endl; // FIXME: info output
	continue;
      }
      copy(phiRecHits.begin(), phiRecHits.end(), back_inserter(recHits1D_S3));
      
      if((*segment4D).hasZed()) {
	const DTSLRecSegment2D* zSeg = (*segment4D).zSegment();
	vector<DTRecHit1D> zRecHits = zSeg->specificRecHits();
	if(zRecHits.size() != 4) {
	  if(debug)
	    cout << "[DTTimeBoxMeanTimerAnalysis] Theta segments has: " << zRecHits.size()
		 << " hits, skipping" << endl; // FIXME: info output
	  continue;
	}
	copy(zRecHits.begin(), zRecHits.end(), back_inserter(recHits1D_S3));
      }

      //Extrapolate the 4D segment position at the middle of each superlayer
      vector<LocalPoint> segPosAtSL;
      LocalPoint posMidSLinSL(0,0,0);
      //cout<<"seg4D local position "<< (*segment4D).localPosition()<<endl;
      //cout<<"seg4D local direction "<< (*segment4D).localDirection()<<endl;
      vector< const DTSuperLayer*> superLayers = chamber->superLayers();
      for(vector<const DTSuperLayer*>::const_iterator sl = superLayers.begin();
	  sl != superLayers.end();
	  sl++) 
	{
	  //cout<<"superlayer "<<(*sl)->id()<<endl;
	  LocalPoint posMidSLinCh = chamber->toLocal((*sl)->toGlobal(posMidSLinSL))  ;
	  LocalPoint segPosAtMidSL = (*segment4D).localPosition() 
	    + (*segment4D).localDirection()*posMidSLinCh.z()/cos((*segment4D).localDirection().theta());
	  //cout<<"position at middle sl "<<segPosAtMidSL<<endl;
	  segPosAtSL.push_back(segPosAtMidSL);
	}
  
      float cellLenght=-999;
      float time_SL1[4];
      float time_SL2[4];
      float time_SL3[4];
    
      // Loop over 1D RecHit inside 4D segment
      for(vector<DTRecHit1D>::const_iterator recHit1D = recHits1D_S3.begin();
	  recHit1D != recHits1D_S3.end();
	  recHit1D++) {

	if(debug)
	  cout<<"Looping on 1D rechits: -------------------------"<<endl;

	const DTWireId wireId = (*recHit1D).wireId();

	//store digi time for each layer to compute meantimer
	float digiTime = (*recHit1D).digiTime();
	double offset = 0;
	if(doSubtractT0) {
	  const DTLayer* layerFake = 0;//fake
	  const GlobalPoint glPtFake;//fake
	  offset = theSync->offset(layerFake, wireId, glPtFake);
	}
	if((wireId.superlayerId()).superLayer()==1)
	  {
	   time_SL1[((wireId.layerId()).layer())-1]=digiTime-offset;
	   //cout<<"SL1 "<<time_SL1[((wireId.layerId()).layer())-1]<<endl;
	  }
	else if((wireId.superlayerId()).superLayer()==2)
	  {
	  time_SL2[((wireId.layerId()).layer())-1]=digiTime-offset;
	  //cout<<"SL2 "<<time_SL1[((wireId.layerId()).layer())-1]<<endl;
	  }
	else if((wireId.superlayerId()).superLayer()==3)
	  {
	    time_SL3[((wireId.layerId()).layer())-1]=digiTime-offset;
	    //cout<<"SL3 "<<time_SL1[((wireId.layerId()).layer())-1]<<endl;
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
	cellLenght = (layer->specificTopology()).cellLenght();
	
	// Get wire position in chamber RF
	float wireX = layer->specificTopology().wirePosition(wireId.wire());
	LocalPoint wirePosInLay(wireX,0,0);
	GlobalPoint wirePosGlob = layer->toGlobal(wirePosInLay);
	LocalPoint wirePosInChamber = chamber->toLocal(wirePosGlob);

	// Segment position at Wire z in chamber local frame
	LocalPoint segPosAtZWire = (*segment4D).localPosition()
	  + (*segment4D).localDirection()*wirePosInChamber.z()/cos((*segment4D).localDirection().theta());

	// Get segment etrapolation pos. in layer RF
	//LocalPoint segPosExtrInLayer = layer->toLocal(chamber->toGlobal(segPosAtZWire));
	const DTSuperLayer* superlayer = chamber->superLayer(wireId.superlayerId());
	LocalPoint segPosExtrInSL = superlayer->toLocal(chamber->toGlobal(segPosAtZWire));

	fillHistoTB(wireId.superlayerId(),digiTime-offset,segPosExtrInSL.y(),cellLenght);
	if(debug) {
	  cout << "   Filling Time Box:        " <<  wireId.superlayerId()<< endl;
	  cout << "           offset (ns):     " << offset << endl;
	  cout << "           time(ns):        " << digiTime-offset<< endl;
	  cout << "           position y (cm): " << segPosExtrInSL.y()<<endl;
	}
	
      }// End of loop over 1D RecHit inside 4D segment
      
      //compute meantimer (with the standard fomula) for each superlayer (also for noisy channel!!!)
      float meanTimer=-999;
      for(int u=0;u<2;u++)
	{
	  meanTimer = (time_SL1[u]+time_SL1[u+2])*0.5 + time_SL1[u+1];
	  if(debug) {
	    cout << "   Filling MeanTimer :      " << (*chamberId) <<" Sl:1"<< endl;
	    cout << "           mean time (ns):  " << meanTimer << endl;
	    cout << "           position y (cm): " << segPosAtSL[0].y() <<endl;
	  }	  
	  fillHistoMT(DTSuperLayerId((*chamberId).wheel(),(*chamberId).station(),(*chamberId).sector(),1),meanTimer,segPosAtSL[0].y(),cellLenght);
	}
      if((*segment4D).hasZed())
	{
	  meanTimer=-999;
	  for(int u=0;u<2;u++)
	    {
	      meanTimer = (time_SL2[u]+time_SL2[u+2])*0.5 + time_SL2[u+1];
	      if(debug) {
		cout << "   Filling MeanTimer :      " << (*chamberId) <<" Sl:2"<< endl;
		cout << "           mean time (ns):  " << meanTimer << endl;
		cout << "           position x (cm): " << segPosAtSL[2].x() <<endl;
	      }	 
	      fillHistoMT(DTSuperLayerId((*chamberId).wheel(),(*chamberId).station(),(*chamberId).sector(),2),meanTimer,segPosAtSL[2].x(),cellLenght);
	    }
	}
      meanTimer=-999;
      for(int u=0;u<2;u++)
	{
	  meanTimer = (time_SL3[u]+time_SL3[u+2])*0.5 + time_SL3[u+1];
	  if(debug) {
	    cout << "   Filling MeanTimer :      " << (*chamberId) <<" Sl:3"<< endl;
	    cout << "           mean time (ns):  " << meanTimer << endl;
	    cout << "           position y (cm): " << segPosAtSL[1].y() <<endl;
	  }	  
	  fillHistoMT(DTSuperLayerId((*chamberId).wheel(),(*chamberId).station(),(*chamberId).sector(),3),meanTimer,segPosAtSL[1].y(),cellLenght);
	}
    }// End of loop over the segm4D of this ChamerId
 }
  // -----------------------------------------------------------------------------
}


// Book the meantimer histogram for a given SL
void DTTimeBoxMeanTimerAnalysis::bookHistoMT(DTSuperLayerId slId) {
  if(debug)
    cout << "   Booking meantimer histo for SL: " << slId << endl;

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
  TString N = slHistoName.c_str();
  histoMTPerSL[slId] = new HMeanTimer(slHistoName);
}

// Book the meantimer histogram for a given SL
void DTTimeBoxMeanTimerAnalysis::bookHistoTB(DTSuperLayerId slId) {
  if(debug)
    cout << "   Booking meantimer histo for SL: " << slId << endl;

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
  TString N = slHistoName.c_str();
  histoTBPerSL[slId] = new HTimeBoxes(slHistoName);
}

// Fill meantimer histogram for a given SL 
void DTTimeBoxMeanTimerAnalysis::fillHistoMT(DTSuperLayerId slId,
				     float meanTimer,
				     float ySegm,
				     float cellLenght) {
  // FIXME: optimization of the number of searches
  if(histoMTPerSL.find(slId) == histoMTPerSL.end()) {
    bookHistoMT(slId);
  }
  theFile->cd();
  histoMTPerSL[slId]->Fill(slId,meanTimer,ySegm,cellLenght);
}

void DTTimeBoxMeanTimerAnalysis::fillHistoTB(DTSuperLayerId slId,
				     float time,
				     float ySegm,
				     float cellLenght) {
  // FIXME: optimization of the number of searches
  if(histoTBPerSL.find(slId) == histoTBPerSL.end()) {
    bookHistoTB(slId);
  }
  theFile->cd();
  histoTBPerSL[slId]->Fill(slId,time,ySegm,cellLenght);
}




void DTTimeBoxMeanTimerAnalysis::endJob() {
  // Write all histos to file
  theFile->cd();
  for(map<DTSuperLayerId, HMeanTimer*>::const_iterator slIdAndHisto = histoMTPerSL.begin();
      slIdAndHisto != histoMTPerSL.end(); ++slIdAndHisto) {
    (*slIdAndHisto).second->Write();
  }
  for(map<DTSuperLayerId, HTimeBoxes*>::const_iterator slIdAndHisto = histoTBPerSL.begin();
      slIdAndHisto != histoTBPerSL.end(); ++slIdAndHisto) {
    (*slIdAndHisto).second->Write();
    }
}

