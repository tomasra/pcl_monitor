
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2011/02/13 22:47:08 $
 *  $Revision: 1.19 $
 *  \author G. Cerminara - INFN Torino
 */

#include "DTTreeBuilder.h"
#include "DTSegmentObject.h"
#include "DTHitObject.h"
#include "DTMuObject.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"
// #include "Geometry/Vector/interface/Pi.h"

#include "DataFormats/DTRecHit/interface/DTRecSegment4DCollection.h"
#include "DataFormats/DTRecHit/interface/DTRecSegment2DCollection.h"
#include "DataFormats/DTRecHit/interface/DTRecHitCollection.h"

#include "RecoLocalMuon/DTRecHit/interface/DTRecHitAlgoFactory.h"

#include "Geometry/DTGeometry/interface/DTGeometry.h"
#include "Geometry/Records/interface/MuonGeometryRecord.h"

#include "CondFormats/DataRecord/interface/DTStatusFlagRcd.h"
#include "CondFormats/DTObjects/interface/DTStatusFlag.h"
#include <CondFormats/DTObjects/interface/DTTtrig.h>
#include <CondFormats/DataRecord/interface/DTTtrigRcd.h>
#include "CondFormats/DTObjects/interface/DTT0.h"
#include "CondFormats/DataRecord/interface/DTT0Rcd.h"
#include "CondFormats/DataRecord/interface/DTMtimeRcd.h"
#include "CondFormats/DTObjects/interface/DTMtime.h"

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
 #include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "DataFormats/SiPixelCluster/interface/SiPixelCluster.h"

#include <iterator>
#include <vector>

#include "TFile.h"
#include "TMath.h"
#include "TTree.h"
#include "TClonesArray.h"


using namespace edm;
using namespace std;
using namespace reco;

DTTreeBuilder::DTTreeBuilder(const ParameterSet& pset, TFile* file) : 
  theFile(file),
  BX(-999),
  //  pix(-999),
  runN(-1),
  eventN(-1)
{
  debug = pset.getUntrackedParameter<bool>("debug","false");
  // the name of the 4D rec hits collection
  theRecHits4DLabel = pset.getParameter<string>("recHits4DLabel");
  theRecHits2DLabel = pset.getParameter<string>("recHits2DLabel");
  theRecHitLabel = pset.getParameter<string>("recHitLabel");
  theMuonLabel = pset.getParameter<string>("muonLabel");

  checkNoisyChannels = pset.getUntrackedParameter<bool>("checkNoisyChannels","false");
  algoName = pset.getParameter<string>("recAlgo");
  theAlgo = DTRecHitAlgoFactory::get()->create(algoName,pset.getParameter<ParameterSet>("recAlgoConfig"));

}

DTTreeBuilder::~DTTreeBuilder(){}


void DTTreeBuilder::analyze(const Event& event, const EventSetup& setup) {
  if(debug)
    cout << "[DTTreeBuilder] Analyze #Run: " << event.id().run()
	 << " #Event: " << event.id().event() << endl;

  // get the BX, run, event...
  BX = event.bunchCrossing();
  runN = event.id().run();
  eventN = event.id().event();

  // Get the 4D segment collection from the event
  edm::Handle<DTRecSegment4DCollection> all4DSegments;
  event.getByLabel(theRecHits4DLabel, all4DSegments);

  // Get the 2D segment collection from the event
  edm::Handle<DTRecSegment2DCollection> all2DSegments;
  if (theRecHits2DLabel!="") {
    event.getByLabel(theRecHits2DLabel, all2DSegments);
  }
  
  // Get the DT rechit collection from the event
  Handle<DTRecHitCollection> dtRecHits;
  event.getByLabel(theRecHitLabel, dtRecHits);


  edm::Handle<reco::VertexCollection> vertex; 
  event.getByLabel("goodPrimaryVertices", vertex);

  // Get the pixel cluster collection
//   Handle<edmNew::DetSetVector<SiPixelCluster> > clusterColl; 
// //   event.getByLabel("siPixelClusters", clusterColl); //name hardcoded beacuse I am lazy...
// //   pix = clusterColl->size();
//   pix=-1;

  // Get the DT Geometry
  ESHandle<DTGeometry> dtGeom;
  setup.get<MuonGeometryRecord>().get(dtGeom);
  
  // Get the map of noisy channels
  ESHandle<DTStatusFlag> statusMap;
  if(checkNoisyChannels) {
    setup.get<DTStatusFlagRcd>().get(statusMap);
  }

  setup.get<DTTtrigRcd>().get(tTrigMap);
  setup.get<DTT0Rcd>().get(t0Handle);


  // Get the map of ttrig from the Setup
  setup.get<DTMtimeRcd>().get(mTimeHandle);
  const DTMtime *mTimeMap = &*mTimeHandle;


  int segmCounter = 0;



  // Loop over all chambers containing a 4D segment
  for (DTRecSegment4DCollection::id_iterator chamberId = all4DSegments->id_begin(); chamberId != all4DSegments->id_end(); ++chamberId) {
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

      // NA: For the time being, keep ALL 4D segments
      // If Statio != 4 skip RecHits with dimension != 4
      // For the Station 4 consider 2D RecHits
//       if((*segment4D).dimension() != 4) {
// 	if(debug)
// 	  cout << "[DTTreeBuilder]***Warning: RecSegment dimension is not 4 but "
// 	       << (*segment4D).dimension() << ", skipping!" << endl;
// 	continue;
//       }
      

      // Get all 1D RecHits at step 3 within the 4D segment
      vector<DTRecHit1D> recHits1D_S3;

      // Create the segment object
      DTSegmentObject * segmObj = new((*segmentArray)[segmCounter++]) DTSegmentObject((*chamberId).wheel(), (*chamberId).station(), (*chamberId).sector());
      LocalPoint segment4DLocalPos = (*segment4D).localPosition();
      segmObj->setPositionInChamber(segment4DLocalPos.x(), segment4DLocalPos.y(), segment4DLocalPos.z());

      float dxdz =angleBtwHPiAndHPi(std::atan2((*segment4D).localDirection().x(),(*segment4D).localDirection().z()));
      float dydz = angleBtwHPiAndHPi(std::atan2((*segment4D).localDirection().y(),(*segment4D).localDirection().z()));      

      segmObj->phi = dxdz;
      segmObj->theta = dydz;
      segmObj->chi2 = (*segment4D).chi2()/(*segment4D).degreesOfFreedom();

      GlobalPoint segment4DGlobalPos = chamber->toGlobal(segment4DLocalPos);
      segmObj->setGlobalPosition(segment4DGlobalPos.x(), segment4DGlobalPos.y(), segment4DGlobalPos.z());


      int projection = -1;


//       float t0phi = -1;
//       float t0theta = -1;
//       float vDrift = -1;




      if((*segment4D).hasPhi()) {
	if(debug) cout << "  segment has phi projection" << endl;
	DTSuperLayerId supLayIdPhi1((*chamberId), 1);
	DTSuperLayerId supLayIdPhi2((*chamberId), 3);
	float hitResolution = 0;//FIXME: should use this!	
	// get the vdrift of the 2 phi SLs and take the average
	float vDrift1 = 0.;
	// vdrift is cm/ns , resolution is cm
	mTimeMap->get(supLayIdPhi1,
		      vDrift1,
		      hitResolution,
		      DTVelocityUnits::cm_per_ns);

	float vDrift2 = 0.;
	// vdrift is cm/ns , resolution is cm
	mTimeMap->get(supLayIdPhi2,
		      vDrift2,
		      hitResolution,
		      DTVelocityUnits::cm_per_ns);

	float vdrift = vDrift1 + vDrift2 / 2.;

	const DTChamberRecSegment2D* phiSeg = (*segment4D).phiSegment();
	vector<DTRecHit1D> phiRecHits = phiSeg->specificRecHits();
	copy(phiRecHits.begin(), phiRecHits.end(), back_inserter(recHits1D_S3));
	projection = 1;
	// 	segmObj->vDriftCorrPhi = (*segment4D).phiSegment()->vDrift();
	float dVdrift = (*segment4D).phiSegment()->vDrift();
	if ((*segment4D).phiSegment()->ist0Valid()) {
	  segmObj->vDriftCorrPhi =  vdrift*(1. - dVdrift);
	  segmObj->t0SegPhi = (*segment4D).phiSegment()->t0(); 
	} else {
	  segmObj->vDriftCorrPhi =  -1.;
	  segmObj->t0SegPhi = -1.;
	}
      }



      if((*segment4D).hasZed()) {
	DTSuperLayerId supLayIdTheta((*chamberId), 2);
	float hitResolution = 0;//FIXME: should use this!	
	// get the vdrift of the 2 phi SLs and take the average
	float vdrift = 0.;
	// vdrift is cm/ns , resolution is cm
	mTimeMap->get(supLayIdTheta,
		      vdrift,
		      hitResolution,
		      DTVelocityUnits::cm_per_ns);


	const DTSLRecSegment2D* zSeg = (*segment4D).zSegment();
	vector<DTRecHit1D> zRecHits = zSeg->specificRecHits();
	copy(zRecHits.begin(), zRecHits.end(), back_inserter(recHits1D_S3));
	if(projection == -1) projection = 2;
	else projection = 3;
	// 	segmObj->t0SegTheta = (*segment4D).zSegment()->t0();
	float dVdrift = (*segment4D).zSegment()->vDrift();
	if ((*segment4D).zSegment()->ist0Valid()) {
	  segmObj->vDriftCorrTheta =  vdrift*(1. - dVdrift);
	  segmObj->t0SegTheta = (*segment4D).zSegment()->t0();
	} else {
	  segmObj->vDriftCorrTheta =  -1.;
	  segmObj->t0SegTheta = -1.;
	}
	// 	segmObj->vDriftCorrTheta = (*segment4D).zSegment()->vDrift();
      }

      segmObj->proj = projection;

      for(int sl = 1; sl != 4; ++sl) {
	DTSuperLayerId supLayId((*chamberId), sl);
	//	float ttrig = 0.;
	float mean = 0.;
	float sigma = 0.;
	float kFact = 0.0;
	// FIXME: port to 31X interface
	tTrigMap->get(supLayId, mean, sigma, kFact, DTTimeUnits::ns); 
	//ttrig = mean + kFact*sigma;
	segmObj->setTTrig(sl, mean, sigma, kFact);
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

	
	DTHitObject *hitObj = segmObj->add1DHit(wireId.wheel(), wireId.station(), wireId.sector(),
					       wireId.superLayer(), wireId.layer(), wireId.wire());
	
	
	hitObj->digiTime = (*recHit1D).digiTime() ;

	float t0 = 0;
	float t0rms = 0;
	// Read the t0 from pulses for this wire (ns)
	t0Handle->get(wireId,
		      t0,
		      t0rms,
		      DTTimeUnits::ns);

	hitObj->t0pulses = t0;

	// Check for noisy channels and skip them
	if(checkNoisyChannels) {
	  bool isNoisy = false;
	  bool isFEMasked = false;
	  bool isTDCMasked = false;bool isTrigMask = false;
	  bool isDead = false;
	  bool isNohv = false;
	  statusMap->cellStatus(wireId, isNoisy, isFEMasked, isTDCMasked, isTrigMask, isDead, isNohv);
	  hitObj->isNoisyCell = isNoisy;
	}

	// Get the layer and the wire position
	const DTLayer* layer = (chamber->superLayer(wireId.superlayerId()))->layer(wireId.layerId());
	float wireX = layer->specificTopology().wirePosition(wireId.wire());


	
	// Distance of the 1D rechit from the wire
	//float distRecHitToWire = fabs(wireX - (*recHit1D).localPosition().x());
	float distRecHitToWire = fabs(wireX - (*recHit1D).localPosition().x());
	
	// Extrapolate the segment to the z of the wire
	
	// Get wire position in chamber RF
	LocalPoint wirePosInLay(wireX,(*recHit1D).localPosition().y(),(*recHit1D).localPosition().z());
	GlobalPoint wirePosGlob = layer->toGlobal(wirePosInLay);
	LocalPoint wirePosInChamber = chamber->toLocal(wirePosGlob);
// 	cout << "Wire: " << wireId << " z: " << wirePosInChamber.z() << endl;

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
	  angle = dxdz;
	} else if(sl == 2) {
	  // RZ SL
	  //x in layer and y in chamber are in opposite direction in sl theta
	  distSegmToWire = fabs(segPosAtZWire.y() - wirePosInChamber.y());
	  angle = dydz;
	}



	if(fabs(distSegmToWire) > 10)
	  cout << "  Warning: dist segment-wire: " << distSegmToWire << endl;

	//double residual = distRecHitToWire - distSegmToWire;

	// Get segment etrapolation pos. in layer RF
	//LocalPoint segPosExtrInLayer = layer->toLocal(chamber->toGlobal(segPosAtZWire));
	//	const DTSuperLayer* superlayer = chamber->superLayer(wireId.superlayerId());
	//	LocalPoint segPosExtrInSL = superlayer->toLocal(chamber->toGlobal(segPosAtZWire));	

	// create the DTHitObject
	hitObj->setLocalPosition((*recHit1D).localPosition().x(),
				(*recHit1D).localPosition().y(),
				(*recHit1D).localPosition().z());
	
	hitObj->resDist = distRecHitToWire - distSegmToWire;
	hitObj->resPos = deltaX;
	hitObj->distFromWire = distSegmToWire;
	hitObj->sigmaPos = sqrt((*recHit1D).localPositionError().xx());
	hitObj->angle = angle;


	// Re-reconstruct hits at different steps
	
	// 1.step
	DTDigi digi(wireId.wire(), double((*recHit1D).digiTime()));
	LocalPoint leftPoint;
	LocalPoint rightPoint;
	LocalError error;
	theAlgo->setES(setup);
	float dS1 =-1.;
	if (theAlgo->compute(layer, digi, leftPoint, rightPoint, error)){
	  dS1 = (leftPoint-rightPoint).mag()/2.;
	  hitObj->resDistS1=dS1 - distSegmToWire;
	}

	// 2. step
	float dS2 =-1.;
	// Beware, lin algo just copies input RH to output RH, does not to the actual job!
	// FIXME simple hack for the time being. Should rather rebuild the S1 hit from dS1!
	if (algoName=="DTLinearDriftFromDBAlgo") {
	  dS2 = dS1;
	} else {
	  DTRecHit1D rhS2 = (*recHit1D);
	  if (theAlgo->compute(layer, (*recHit1D), angle, rhS2)) {
	    dS2 = fabs(wireX - rhS2.localPosition().x());
	  }
	}

	if (dS2>=0.) {
	  hitObj->resDistS2=dS2 - distSegmToWire;
	}

	// 3. step: re-reco (crossckeck)
	//	float dS3 =-1.;
	DTRecHit1D rhS3 = (*recHit1D);
	//	GlobalPoint pos = chamber->toGlobal(segPosAtZWire);
// 	if (theAlgo->compute(layer, (*recHit1D), angle, pos, rhS3)) {
// 	  dS3 = fabs(wireX - rhS3.localPosition().x());
// 	}

// 	if (fabs(dS3 - distRecHitToWire) > 0.0005) {  
// 	  // FIXME must check why!!!
// 	  cout << endl << "WARNING: " << distRecHitToWire << " S1=" << dS1 << " S2=" << dS2 << " S3=" << dS3 
// 	       << " diff recomputed S3:" <<  dS3 - distRecHitToWire<< endl << endl;

// 	}
	
      }// End of loop over 1D RecHit inside 4D segment
      
      // Add the DTSegmentObject to the TClonesArray
      if(debug) cout << "Add new segment with # hits: " << segmObj->hits->GetEntriesFast() << endl;
      if(debug) cout << "    new # of segments is: " << segmCounter << endl;

      

      // Add available 1D hits for this chamber
      
      for (int sl = 1; sl <=3; ++sl) {
	if ((*chamberId).station()==4 && sl==3) continue;
	for (int layer = 1; layer <=4; ++layer) {
	  DTLayerId lId((*chamberId),sl,layer);
	  DTRecHitCollection::range range = dtRecHits->get(lId);
	  for (DTRecHitCollection::const_iterator recHit1D = range.first; recHit1D!=range.second; ++recHit1D) {
	    DTWireId wireId = (*recHit1D).wireId();
	    DTHitObject *hitObj = segmObj->addAvailable1DHit(wireId.wheel(), wireId.station(), wireId.sector(),wireId.superLayer(), wireId.layer(), wireId.wire());
	    
	    hitObj->digiTime = (*recHit1D).digiTime() ;
	    hitObj->setLocalPosition((*recHit1D).localPosition().x(),
				     (*recHit1D).localPosition().y(),
				     (*recHit1D).localPosition().z());
	    hitObj->distFromWire = ((*recHit1D).localPosition(DTEnums::Right)-(*recHit1D).localPosition(DTEnums::Left)).mag()/2.;
	    
	    hitObj->sigmaPos = sqrt((*recHit1D).localPositionError().xx());

	  }
	}
      }
      

    }// End of loop over the segm4D of this ChamerId
  }


  // 2D segments
  //----------------------------------------------------------------------
  if (theRecHits2DLabel!="") {
    int segm2DCounter = 0;  
    for (DTRecSegment2DCollection::id_iterator slId = all2DSegments->id_begin(); slId != all2DSegments->id_end(); ++slId) { // loop over SLs with segments
      DTRecSegment2DCollection::range  range = all2DSegments->get(*slId);
      int nsegm = distance(range.first, range.second);
      if(debug)
	cout << "   SL: " << *slId << " has " << nsegm
	     << " 2D segments" << endl;
      // Get the SL
      const DTSuperLayer* sl = dtGeom->superLayer(*slId);


      for (DTRecSegment2DCollection::const_iterator segment2D = range.first;
	   segment2D!=range.second; ++segment2D) { // Loop over the segments in this SL
	if(debug){
	  cout<<"Looping on 2D segments: -------------------------"<<endl;
	}


	// Get all 1D RecHits at step 2 within the 2D segment
	vector<DTRecHit1D> recHits1D_S2;

	// Create the segment object
	DTSegmentObject * segmObj = new((*segment2DArray)[segm2DCounter++]) DTSegmentObject((*slId).wheel(), (*slId).station(), (*slId).sector());
	LocalPoint segment2DLocalPos = (*segment2D).localPosition();
	segmObj->setPositionInChamber(segment2DLocalPos.x(), segment2DLocalPos.y(), segment2DLocalPos.z());

	float dxdz =angleBtwHPiAndHPi(std::atan2((*segment2D).localDirection().x(),(*segment2D).localDirection().z()));

	segmObj->phi = dxdz;
	segmObj->theta = 0;
	segmObj->chi2 = (*segment2D).chi2()/(*segment2D).degreesOfFreedom();
      
	int projection = -1;

	if((*slId).superLayer()==2) {
	  projection = 2;
	} else {
	  projection = 1;
	}
      
	recHits1D_S2 = segment2D->specificRecHits();
	segmObj->proj = projection;


	// Loop over 1D RecHit inside 2D segment
	for(vector<DTRecHit1D>::const_iterator recHit1D = recHits1D_S2.begin();
	    recHit1D != recHits1D_S2.end();
	    recHit1D++) {
	  const DTWireId wireId = (*recHit1D).wireId();
	  if(debug) {
	    cout<<"Looping on 1D rechits: -------------------------"<<endl;
	    cout << wireId << endl;
	  }

	
	  DTHitObject *hitObj = segmObj->add1DHit(wireId.wheel(), wireId.station(), wireId.sector(),
						  wireId.superLayer(), wireId.layer(), wireId.wire());
	
	
	  hitObj->digiTime = (*recHit1D).digiTime() ;

	  float t0 = 0;
	  float t0rms = 0;
	  // Read the t0 from pulses for this wire (ns)
	  t0Handle->get(wireId,
			t0,
			t0rms,
			DTTimeUnits::ns);

	  hitObj->t0pulses = t0;

	  // Check for noisy channels and skip them
	  if(checkNoisyChannels) {
	    bool isNoisy = false;
	    bool isFEMasked = false;
	    bool isTDCMasked = false;
	    bool isTrigMask = false;
	    bool isDead = false;
	    bool isNohv = false;
	    statusMap->cellStatus(wireId, isNoisy, isFEMasked, isTDCMasked, isTrigMask, isDead, isNohv);
	    hitObj->isNoisyCell = isNoisy;
	  }

	  // Get the layer and the wire position
	  const DTLayer* layer = sl->layer(wireId.layerId());
	  float wireX = layer->specificTopology().wirePosition(wireId.wire());


	
	  // Distance of the 1D rechit from the wire
	  //float distRecHitToWire = fabs(wireX - (*recHit1D).localPosition().x());
	  float distRecHitToWire = fabs(wireX - (*recHit1D).localPosition().x());
	
	  // Extrapolate the segment to the z of the wire
	
	  // Get wire position in SL RF
	  LocalPoint wirePosInLay(wireX,0,0);
	  GlobalPoint wirePosGlob = layer->toGlobal(wirePosInLay);
	  LocalPoint wirePosInSl = sl->toLocal(wirePosGlob);
	  // 	cout << "Wire: " << wireId << " z: " << wirePosInChamber.z() << endl;

	  // Segment position at Wire z in SL local frame
	  LocalPoint segPosAtZWire = (*segment2D).localPosition()
	    + (*segment2D).localDirection()*wirePosInSl.z()/cos((*segment2D).localDirection().theta());
  

	  float deltaX = (*recHit1D).localPosition().x() - (layer->toLocal(sl->toGlobal(segPosAtZWire))).x();
	  float angle = -1;
	  double distSegmToWire = fabs(wirePosInSl.x() - segPosAtZWire.x());
	  angle = dxdz;

	  // 	cout << wireId << " wiX=" << wireX << " drhw=" << distRecHitToWire 
	  // 	     << " wposL=" << wirePosInLay 
	  // 	     << " wposSl=" << wirePosInSl << endl
	  // 	     << " segPosAtZWire=" << segPosAtZWire
	  // 	     << " deltaX " << deltaX 
	  // 	     << " distSegmToWire " << distSegmToWire <<endl
	  // 	     << " theta=" <<(*segment2D).localDirection().theta()
	  // 	     << " angle=" <<angle <<endl <<endl;


	  if(fabs(distSegmToWire) > 10)
	    cout << "  Warning: dist segment-wire: " << distSegmToWire << endl;
	
	
	  // plots for different angles
	  theFile->cd();

	  // FIXME
	  // create the DTHitObject
	  hitObj->setLocalPosition((*recHit1D).localPosition().x(),
				   (*recHit1D).localPosition().y(),
				   (*recHit1D).localPosition().z());
	
	  hitObj->resDist = distRecHitToWire - distSegmToWire;
	  hitObj->resPos = deltaX;
	  hitObj->distFromWire = distSegmToWire;
	  hitObj->sigmaPos = sqrt((*recHit1D).localPositionError().xx());
	  hitObj->angle = angle;	

	}// End of loop over 1D RecHit inside 2D segment
      
	if(debug) cout << "Add new segment with # hits: " << segmObj->hits->GetEntriesFast() << endl;
	if(debug) cout << "    new # of segments is: " << segm2DCounter << endl;

      }// End of loop over the segm2D of this ChamerId
    }
  }
  


  // Look at muons -----------------------------------------------------------------------------

  Handle<MuonCollection> muons;
  event.getByLabel(theMuonLabel, muons);

  int muCounter = 0;

  if(muons.isValid()) {
    for (MuonCollection::const_iterator muon = muons->begin();
	 muon!=muons->end(); ++muon) { // loop over all muons

      DTMuObject * muObj = new((*muArray)[muCounter++]) DTMuObject();

      muObj->eta = (*muon).eta();
      muObj->phi = (*muon).phi();
      muObj->qpt = (*muon).pt()*(*muon).charge();

      if(debug)
	cout << "muon eta, phi:" << muObj->eta << " " << muObj->phi << endl;
      
      if (muon->isGlobalMuon()) {
	
	// Info from the GLB fit
	const HitPattern& hitP = (*muon).globalTrack()->hitPattern();

	muObj->nStripHits =hitP.numberOfValidStripHits();
	muObj->nPixHits   =hitP.numberOfValidPixelHits();
	muObj->nMuHits    =hitP.numberOfValidMuonHits();
	muObj->nGlbDTValidHits = hitP.numberOfValidMuonDTHits();

	muObj->nGlbDTHits = hitP.numberOfValidMuonDTHits()+hitP.numberOfBadMuonDTHits();


	// Info from the STA fit
	const HitPattern& hitPSTA = (*muon).outerTrack()->hitPattern();
	muObj->nStaDTValidHits = hitPSTA.numberOfValidMuonDTHits();
	muObj->nStaDTHits = hitPSTA.numberOfValidMuonDTHits() + hitPSTA.numberOfBadMuonDTHits();

      } else {
	if (muon->isStandAloneMuon()) { // STA Only
	  const HitPattern& hitP = (*muon).outerTrack()->hitPattern();

	  muObj->nMuHits    = hitP.numberOfValidMuonHits();	
	  muObj->nStaDTValidHits = hitP.numberOfValidMuonDTHits();
	  muObj->nStaDTHits = hitP.numberOfValidMuonDTHits() + hitP.numberOfBadMuonDTHits();

	}
	if (muon->isTrackerMuon()) { // TK Only
	  muObj->nStripHits =( *muon).innerTrack()->hitPattern().numberOfValidStripHits();
	  muObj->nPixHits   = (*muon).innerTrack()->hitPattern().numberOfValidPixelHits();
	}
      }
      
      
      float normChi2tk  = -1;
      float normChi2sta = -1;
      float normChi2glb = -1;
      int type = 0;      
      if(muon->isStandAloneMuon()) {
	normChi2sta = (*muon).outerTrack()->normalizedChi2();
	if(muon->isGlobalMuon()) {
	  normChi2tk = (*muon).innerTrack()->normalizedChi2();
	  normChi2glb = (*muon).globalTrack()->normalizedChi2();
	  if(muon->isTrackerMuon()) { 
	   type = 1; // STA + GLB + TM
	  } else type = 2; // STA + GLB
	} else {
	  if(muon->isTrackerMuon()) {
	    normChi2tk = (*muon).innerTrack()->normalizedChi2();
	    type = 3;  // STA + TM
	  } else type= 5; // STA
	} 
      } else {
	if(muon->isTrackerMuon()) type = 4; // TM
	normChi2tk = (*muon).innerTrack()->normalizedChi2();
      }
          

      muObj->normChi2tk=normChi2tk;
      muObj->normChi2sta=normChi2sta;
      muObj->normChi2glb=normChi2glb;
      muObj->type=type;

      // If you look at MuonSegmentMatcher class you will see a lot of interesting quantities to look at!
      // you can get the list of matched info using matches()
      // hChamberMatched->Fill(muon->numberOfChambers());

      int sel = 0;
      //      if(muon::isGoodMuon(*muon,muon::GlobalMuonPromptTight)) sel=1;
      if(muon::isTightMuon(*muon,vertex->front())) sel=1;

      muObj->sel = sel;
    }
  }


  theTree->Fill();
//   cout << " clear the array" << endl;
  segmentArray->Delete();
  segment2DArray->Delete();
  muArray->Delete();
  

}


  


void DTTreeBuilder::endJob() {
  // Write all histos to file
  cout << "# of entries in the tree: " << theTree->GetEntries() << endl;
  theFile->cd();
  theTree->Write();
}








// BeginJob
void DTTreeBuilder::beginJob() {
  // create the tree
  theFile->cd();
  
  segmentArray = new TClonesArray("DTSegmentObject");
  segment2DArray = new TClonesArray("DTSegmentObject");
  muArray = new TClonesArray("DTMuObject");


  theTree = new TTree("DTSegmentTree","DTSegmentTree");
  theTree->SetAutoSave(10000000);

  theTree->Branch("segments", "TClonesArray", &segmentArray); 
  if (theRecHits2DLabel!="") {
    theTree->Branch("segments2D", "TClonesArray", &segment2DArray); 
  }
  theTree->Branch("muonCands", "TClonesArray", &muArray);
  theTree->Branch("BX", &BX, "BX/I");
  //  theTree->Branch("Pix", &pix, "Pix/I");
  theTree->Branch("Run", &runN, "Run/I");
  theTree->Branch("Event", &eventN, "Event/I");
}


double DTTreeBuilder::angleBtwPiAndPi(double angle) const {
  while(angle >= TMath::Pi()) angle -= TMath::Pi();
  while(angle < 0.) angle += TMath::Pi();
  return angle;
}

double DTTreeBuilder::angleBtwHPiAndHPi(double angle) const {
  while(angle >= TMath::PiOver2()) angle -= TMath::Pi();
  while(angle < -TMath::PiOver2()) angle += TMath::Pi();
  return angle;
}


