
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2008/10/27 16:25:25 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - INFN Torino
 */

#include "DTSegment2DAnalysis.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
// #include "Geometry/Vector/interface/Pi.h"

#include "DataFormats/DTRecHit/interface/DTRecSegment2DCollection.h"
#include "Histograms.h"

#include "TFile.h"
#include <vector>

#include <iterator>

using namespace edm;
using namespace std;

DTSegment2DAnalysis::DTSegment2DAnalysis(const ParameterSet& pset,
				     TFile* file) : theFile(file) {
				       debug = pset.getUntrackedParameter<bool>("debug","false");
				       // the name of the 2D rec hits collection
				       theRecHits2DLabel = pset.getParameter<string>("recHits2DLabel");
				     }

DTSegment2DAnalysis::~DTSegment2DAnalysis(){}


void DTSegment2DAnalysis::analyze(const Event& event, const EventSetup& setup) {
  if(debug)
    cout << "[DTSegment2DAnalysis] Analyze #Run: " << event.id().run()
	 << " #Event: " << event.id().event() << endl;


  // -- 2D segment analysis  -----------------------------------------------------
  // Get the 2D segment collection from the event
  edm::Handle<DTRecSegment2DCollection> all2DSegments;
  event.getByLabel(theRecHits2DLabel, all2DSegments);

 // Loop over all sls containing a segment
  DTRecSegment2DCollection::id_iterator slId;
  for (slId = all2DSegments->id_begin();
       slId != all2DSegments->id_end();
       ++slId){ 

    // Get the range for the corresponding slId
    DTRecSegment2DCollection::range range = all2DSegments->get(*slId);
    int nsegm = distance(range.first, range.second);
    if (debug)
      cout << "   Superlayer: " << *slId << " has " << nsegm
	   << " 2D segments" << endl;
    fillHistos(*slId, nsegm);

    // Loop over the rechits of this slId
    for (DTRecSegment2DCollection::const_iterator segment2D = range.first;
	 segment2D!=range.second;
	 ++segment2D){
      vector<DTRecHit1D> recHits = (*segment2D).specificRecHits();
      if(recHits.size() != 4) {
	if(debug)
	  cout << "[DTSegment2DAnalysis] Segments has: " << recHits.size()
	       << " hits, skipping" << endl; // FIXME: info output
	continue;
      }

      LocalPoint segment2DLocalPos = (*segment2D).localPosition();
      LocalVector segment2DLocalDirection = (*segment2D).localDirection();
      if((atan(segment2DLocalDirection.x()/segment2DLocalDirection.z())* 180./Geom::pi() > 65) && debug)
	{
	  cout << "Segment has angle: = " << atan(segment2DLocalDirection.x()/segment2DLocalDirection.z())* 180./Geom::pi()  << endl;
	  cout << "  # Hits: " << recHits.size() <<endl;
	  for(vector<DTRecHit1D>::const_iterator hit = recHits.begin();
	      hit != recHits.end(); hit++) {
	    cout << "      hit in wire: " << (*hit).wireId() << endl;
	  }
	}
      if (segment2DLocalDirection.z()) {
	fillHistos(*slId,
		   segment2DLocalPos.x(), 
		   atan(segment2DLocalDirection.x()/segment2DLocalDirection.z())* 180./Geom::pi(),
		   (*segment2D).chi2()/(*segment2D).degreesOfFreedom());
      } else {
	cout << "[DTSegment2DAnalysis] Warning: segment local direction is: "
	     << segment2DLocalDirection << endl;
      }
    }
  }
}

// -----------------------------------------------------------------------------
  
// Book a set of histograms for a give sl
void DTSegment2DAnalysis::bookHistos(DTSuperLayerId slId) {
  if(debug)
     cout << "   Booking histos for sl: " << slId << endl;

  // Compose the sl name
  DTChamberId chamberId = slId.chamberId();
  stringstream wheel; wheel << chamberId.wheel();	
  stringstream station; station << chamberId.station();	
  stringstream sector; sector << chamberId.sector();	
  stringstream superLayer; superLayer << slId.superlayer();	
  
  string superLayerHistoName =
    "_W" + wheel.str() +
    "_St" + station.str() +
    "_Sec" + sector.str() +
    "_SL" + superLayer.str();
  theFile->cd();
  // Create the monitor elements
  histosPerSL[slId] =  new HSegment2D(superLayerHistoName);
}



// Fill a set of histograms for a give sl 
void DTSegment2DAnalysis::fillHistos(DTSuperLayerId slId, int nsegm) {
  // FIXME: optimization of the number of searches
  if(histosPerSL.find(slId) == histosPerSL.end()) {
    bookHistos(slId);
  }
  theFile->cd();
  histosPerSL[slId]->Fill(nsegm);
}


// Fill a set of histograms for a give sl 
void DTSegment2DAnalysis::fillHistos(DTSuperLayerId slId,
				   float posX,
				   float angle,
				   float chi2) {
  // FIXME: optimization of the number of searches
  if(histosPerSL.find(slId) == histosPerSL.end()) {
    bookHistos(slId);
  }
  theFile->cd();
  histosPerSL[slId]->Fill(posX,angle,chi2);
}

void DTSegment2DAnalysis::endJob() {
  // Write all histos to file
  theFile->cd();
  for(map<DTSuperLayerId, HSegment2D* >::const_iterator slIdAndHisto = histosPerSL.begin();
      slIdAndHisto != histosPerSL.end(); ++slIdAndHisto) {
    (*slIdAndHisto).second->Write();
  }
}

