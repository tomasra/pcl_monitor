
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2008/12/03 10:41:13 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "DQM/DTOfflineAnalysis/src/MuonAnalysis.h"

// Framework
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <DataFormats/DTDigi/interface/DTDigiCollection.h>
#include "DataFormats/DTRecHit/interface/DTRecHitCollection.h"


//Geometry
#include "DataFormats/GeometryVector/interface/Pi.h"
#include "DataFormats/MuonDetId/interface/DTChamberId.h"
#include "Geometry/DTGeometry/interface/DTGeometry.h"
#include "Geometry/Records/interface/MuonGeometryRecord.h"

//RecHit
#include "DataFormats/DTRecHit/interface/DTRecSegment4DCollection.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h" 
#include "DataFormats/MuonReco/interface/MuonEnergy.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include <FWCore/Framework/interface/LuminosityBlock.h>

#include <iterator>
#include "TGraph.h"
#include "TVector3.h"
#include "TMath.h"


using namespace edm;
using namespace std;
using namespace reco;

MuonAnalysis::MuonAnalysis(const edm::ParameterSet& pset) : nEvents(0) {

  debug = pset.getUntrackedParameter<bool>("debug","false");
  if(debug)
    cout << "[MuonAnalysis] Constructor called!" << endl;


  // names of the collection to be retrieved from the event
  theDigiLabel =  pset.getUntrackedParameter<InputTag>("dtDigiLabel");
  theRecHitLabel =  pset.getUntrackedParameter<InputTag>("dtRecHitLabel");
  theRecHits4DLabel = pset.getUntrackedParameter<InputTag>("dtRecHit4DLabel");
  theMuonLabel = pset.getUntrackedParameter<InputTag>("muonLabel");

  theFileName = pset.getUntrackedParameter<string>("rootFileName","MuonAnalysis.root");
}



MuonAnalysis::~MuonAnalysis(){
  if(debug)
    cout << "[MuonAnalysis] Destructor called!" << endl;
}


void MuonAnalysis::beginJob(const edm::EventSetup& context){

//   theFile = new TFile(theFileName.c_str(),"RECREATE");
//   theFile->cd();

  
 
}



void MuonAnalysis::endJob(){
  if(debug)
    cout<<"[MuonAnalysis] endjob called!"<<endl;
  
 cout << "[MuonAnalysis] # of analyzed events: " << nEvents << endl;
 

//  theFile->cd();
//  theFile->close();
 

}
  


void MuonAnalysis::analyze(const edm::Event& event, const edm::EventSetup& setup) {
//   if(debug)
  cout << "[MuonAnalysis] event: " <<  event.id().event()
       << " LS: " << event.getLuminosityBlock().luminosityBlock()
       << " run: " <<  event.id().run() << endl;



  nEvents++;

  // Take the STA muon container
  edm::Handle<MuonCollection> muons;
  event.getByLabel(theMuonLabel,muons);

  // check the validity of the collection
  if(muons.isValid()){
    for (MuonCollection::const_iterator recoMu = muons->begin();
	 recoMu!=muons->end(); ++recoMu){ // loop over all muons
      
      double eta = (*recoMu).eta();
      double phi = (*recoMu).phi();
      double pt = (*recoMu).pt();

      string muonType = "";
      if(recoMu->isGlobalMuon()) muonType = " Glb";
      if(recoMu->isStandAloneMuon()) muonType = muonType + " STA";
      if(recoMu->isTrackerMuon()) muonType = muonType + " Trk";
      
      cout << "[MuonAnalysis] New Muon found:" << muonType << endl;
      cout << "-- eta: " << eta << " phi: " << phi << " pt: " << pt << endl;

      // --------------------------------------------------------
      // get all the mu energy deposits
      MuonEnergy muEnergy = (*recoMu).calEnergy();
      cout << "-- Energy deposits: " << endl;

      // ECAL
      string ecalLabel = "EB";
      if(fabs(recoMu->eta()) > 1.479) ecalLabel = "EE";
      cout << "   " << ecalLabel << " energy: " << muEnergy.em << endl;
      cout << "   " << ecalLabel << " (3x3) energy: " << muEnergy.emS9 << endl;
      
      // HCAL 
      string hcalLabel = "HB";
      if(fabs(recoMu->eta()) > 1.4) ecalLabel = "HE";
      cout << "   " << hcalLabel << " energy: " << muEnergy.had << endl;
      cout << "   " << hcalLabel << " (3x3) energy: " << muEnergy.hadS9 << endl;
      
      // HO (eta() < 1.26)
      cout << "   HO energy: " << muEnergy.ho << endl;
      cout << "   HO (3x3) energy: " << muEnergy.hoS9 << endl;
      
  
      // build the transient track
      edm::ESHandle<TransientTrackBuilder> theTTBuilder;
      setup.get<TransientTrackRecord>().get("TransientTrackBuilder",theTTBuilder);
      TransientTrack transTrack;
  
      if(recoMu->isGlobalMuon())
	transTrack = theTTBuilder->build(recoMu->globalTrack());
      if(recoMu->isTrackerMuon() && !(recoMu->isGlobalMuon()))
	transTrack = theTTBuilder->build(recoMu->innerTrack());
      if(recoMu->isStandAloneMuon() && !(recoMu->isGlobalMuon()))
	transTrack = theTTBuilder->build(recoMu->outerTrack());

      TrajectoryStateOnSurface tsos;
      tsos = transTrack.impactPointState();

      // section for vertex pointing muon
      cout << "-- TSOS position x: " <<  tsos.globalPosition().x()
	   << " y: " <<   tsos.globalPosition().y()
	   << " z: " <<   tsos.globalPosition().z()
	   << " dr: " << fabs(tsos.globalPosition().perp()) << endl;

    }
  }

  // Get the 4D segment collection from the event
  edm::Handle<DTRecSegment4DCollection> all4DSegments;
  event.getByLabel(theRecHits4DLabel, all4DSegments);
  
  // check the validity of the collection
  if(all4DSegments.isValid()) {
    // Loop over all chambers containing a segment
    DTRecSegment4DCollection::id_iterator chamberId;
    for (chamberId = all4DSegments->id_begin();
	 chamberId != all4DSegments->id_end();
	 ++chamberId) {
      // Get the range for the corresponding ChamerId
      DTRecSegment4DCollection::range  range = all4DSegments->get(*chamberId);
      int nsegm = distance(range.first, range.second);
//       if(debug)
      cout << "   Ch: " << *chamberId << " has " << nsegm << " 4D segments" << endl;

      //       // Get the chamber
      //       const DTChamber* chamber = dtGeom->chamber(*chamberId);
      
      // Loop over the rechits of this ChamerId
      for(DTRecSegment4DCollection::const_iterator segment4D = range.first;
	  segment4D!=range.second;
	  ++segment4D) {
	cout << "      --- DT seg. dim.: " << (*segment4D).dimension() 
	     << " phi: " << (*segment4D).localDirection().phi() << " -> " << angleBtwPiAndPi((*segment4D).localDirection().phi())
	     << " theta: " << (*segment4D).localDirection().theta() << " -> " << angleBtwPiAndPi((*segment4D).localDirection().theta())
	     << " chi2/ndof: " << (*segment4D).chi2()/(*segment4D).degreesOfFreedom() << endl;
	  
	if((*segment4D).hasPhi()) {
	  cout << "           Phi proj. # hits: " << (*segment4D).phiSegment()->specificRecHits().size()
	       << " t0: " << (*segment4D).phiSegment()->t0()
	       << " vdrift: " << (*segment4D).phiSegment()->vDrift()
	       << endl;
	}
	if((*segment4D).hasZed()) {
	  cout << "           Theta proj. # hits: " << (*segment4D).zSegment()->specificRecHits().size()
	       << " t0: " << (*segment4D).zSegment()->t0()
	       << " vdrift: " << (*segment4D).zSegment()->vDrift()
	       << endl;
	}
      }
    }
  } else {
    cout << "[MuonAnalysis]***Error: collection " << theRecHits4DLabel << " is not valid" << endl;
  }

}

double MuonAnalysis::angleBtwPiAndPi(double angle) const {
  while(angle >= TMath::Pi()) angle -= TMath::Pi();
  while(angle < 0.) angle += TMath::Pi();
  return angle;
}

