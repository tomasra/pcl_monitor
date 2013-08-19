
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2010/05/12 15:33:46 $
 *  $Revision: 1.3 $
 *  \author G. Cerminara - INFN Torino
 */

#include "DTSegmentAnalysis.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
// #include "Geometry/Vector/interface/Pi.h"

#include "DataFormats/DTRecHit/interface/DTRecSegment4DCollection.h"
#include "Histograms.h"

#include "TFile.h"
#include <vector>

#include <iterator>

using namespace edm;
using namespace std;

DTSegmentAnalysis::DTSegmentAnalysis(const ParameterSet& pset,
				     TFile* file) : theFile(file) {
  debug = pset.getUntrackedParameter<bool>("debug","false");
  // the name of the 4D rec hits collection
  theRecHits4DLabel = pset.getParameter<string>("recHits4DLabel");

  readVdrift =  pset.getParameter<bool>("readVdrift");
}




DTSegmentAnalysis::~DTSegmentAnalysis(){}


void DTSegmentAnalysis::analyze(const Event& event, const EventSetup& setup) {
  if(debug)
    cout << "[DTSegmentAnalysis] Analyze #Run: " << event.id().run()
	 << " #Event: " << event.id().event() << endl;


  // -- 4D segment analysis  -----------------------------------------------------
  // Get the 4D segment collection from the event
  edm::Handle<DTRecSegment4DCollection> all4DSegments;
  event.getByLabel(theRecHits4DLabel, all4DSegments);

  // Loop over all chambers containing a segment
  DTRecSegment4DCollection::id_iterator chamberId;
  for (chamberId = all4DSegments->id_begin();
       chamberId != all4DSegments->id_end();
       ++chamberId) {
    // Get the range for the corresponding ChamerId
    DTRecSegment4DCollection::range  range = all4DSegments->get(*chamberId);

    int nsegm = distance(range.first, range.second);
    histoPerChamber[*chamberId]->Fill(nsegm);

    if(debug)
      cout << "   Chamber: " << *chamberId << " has " << nsegm
	   << " 4D segments" << endl;

    // Loop over the rechits of this ChamberId
    for (DTRecSegment4DCollection::const_iterator segment4D = range.first;
	 segment4D!=range.second;
	 ++segment4D) {
      // Count the number of hits per segment:
      int nHits = 0;
      int nHitsPhi = 0 ;
      int nHitsTheta = 0 ;

      int projection = -1;

      float t0phi = -1;
      float t0theta = -1;
      
      float vDrift = -1;
      if((*segment4D).hasPhi()) {
	if(debug) cout << "  segment has phi projection" << endl;
	nHitsPhi += (*segment4D).phiSegment()->specificRecHits().size();
	nHits += nHitsPhi;
	projection = 1;
	t0phi = (*segment4D).phiSegment()->t0();
	if(readVdrift) {
	  if(t0phi != 0) {
	    int t0segn_10time_ns = static_cast<int>(t0phi*10);
	    float t0segn_ns =t0segn_10time_ns/10.;// time : just 0.1 ns resolution
	    float dvDrift0 = t0phi -  t0segn_ns;
	    float dvDrift = abs(dvDrift0);
	    int signvdrift = static_cast<int>(dvDrift*100);
	    if (signvdrift==1)  dvDrift = -(dvDrift - 0.01);
	    vDrift =-dvDrift*10.;
	    t0phi =  t0segn_ns ;
// 	    cout << " vdrift: " << vDrift << endl;
// 	    cout << " t0phi: " << t0phi << endl;
	  }
	}

      }

      if((*segment4D).hasZed()) {
	if(debug) cout << "  segment has z project" << endl;
	nHitsTheta += (*segment4D).zSegment()->specificRecHits().size();
	nHits += nHitsTheta;
	if(projection == -1) projection = 2;
	else projection = 3;
	t0theta = (*segment4D).zSegment()->t0();
      }

      //      LocalPoint segment4DLocalPos = (*segment4D).localPosition();
      LocalVector segment4DLocalDirection = (*segment4D).localDirection();


      histoPerChamber[(*chamberId)]->Fill(nHits,
					  nHitsPhi,
					  nHitsTheta,
					  projection,
					  segment4DLocalDirection.phi(),
					  segment4DLocalDirection.theta(),
					  -1,
					  (*segment4D).chi2()/(*segment4D).degreesOfFreedom(),
					  t0phi,
					  t0theta,
					  vDrift);
    }
  }
  
}

 
void DTSegmentAnalysis::endJob() {
  // Write all histos to file
  theFile->cd();

  for(map<DTChamberId, HSegment* >::const_iterator sectAndHisto =
	histoPerChamber.begin();
      sectAndHisto != histoPerChamber.end(); ++sectAndHisto) {
    (*sectAndHisto).second->Write();
  }
}



// BeginJob
void DTSegmentAnalysis::beginJob() {
  
  // book histos
  
  for(int wheel = -2; wheel != 3; ++wheel) { // Loop over wheel
    for(int station = 1; station != 5; ++station) { // Loop over stations
      for(int sector = 1; sector <= 14; ++sector) { // Loop over sectors
	if((sector == 13 || sector == 14) && station != 4) continue;
	stringstream histoName; histoName << "Wh" << wheel
					  << "_Sec" << sector
					  << "_St" << station;
	
	DTChamberId chamberID(wheel, station, sector);
	histoPerChamber[chamberID] = new HSegment(histoName.str());
      }
    }
  }
  

}
