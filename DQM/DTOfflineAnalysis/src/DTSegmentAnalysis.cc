
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2008/10/27 16:25:25 $
 *  $Revision: 1.5 $
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
       ++chamberId){
    // Get the range for the corresponding ChamerId
    DTRecSegment4DCollection::range  range = all4DSegments->get(*chamberId);
    int nsegm = distance(range.first, range.second);
    if(debug)
      cout << "   Chamber: " << *chamberId << " has " << nsegm
	   << " 4D segments" << endl;
    fillHistos(*chamberId, nsegm);

    // Loop over the rechits of this ChamberId
    for (DTRecSegment4DCollection::const_iterator segment4D = range.first;
	 segment4D!=range.second;
	 ++segment4D){
      // Count the number of hits per segment:
      int nHits = 0;
      if((*segment4D).hasPhi()) {
	if(debug) cout << "  segment has phi projection" << endl;
	nHits += (*segment4D).phiSegment()->specificRecHits().size();
	
	if(hT0CorrPerSL.find(DTSuperLayerId(*chamberId,1)) == hT0CorrPerSL.end()) {
	  bookHistos(DTSuperLayerId(*chamberId,1));
	  bookHistos(DTSuperLayerId(*chamberId,3));
	}
	cout << "D1" << endl;
	hT0CorrPerSL[DTSuperLayerId(*chamberId,1)]->Fill((*segment4D).phiSegment()->t0());
	cout << "D2" << endl;
	hT0CorrPerSL[DTSuperLayerId(*chamberId,3)]->Fill((*segment4D).phiSegment()->t0());
	cout << "D3" << endl;
      }
      if((*segment4D).hasZed()) {
	if(debug) cout << "  segment has z project" << endl;

	nHits += (*segment4D).zSegment()->specificRecHits().size();
	if(hT0CorrPerSL.find(DTSuperLayerId(*chamberId,2)) == hT0CorrPerSL.end()) {
	  bookHistos(DTSuperLayerId(*chamberId,2));
	}
	cout << "D4" << endl;
	hT0CorrPerSL[DTSuperLayerId(*chamberId,2)]->Fill((*segment4D).zSegment()->t0());
	cout << "D5" << endl;
      }
      fillHistoNHits(*chamberId,nHits);



      //Check the quality of the segment
      if(((*segment4D).hasPhi() && !(*segment4D).hasZed()) && (debug)) {
	cout << "[DTSegmentAnalysis] Segment has only Phi projection!" << endl;
      }
      if((!(*segment4D).hasPhi() && (*segment4D).hasZed()) && (debug)) {
	cout << "[DTSegmentAnalysis] Segment has only Theta projection!" << endl;
      }

      return; // FIXME
      if((*chamberId).station()!=4 ) {
	  const DTSLRecSegment2D* thetaSeg = (*segment4D).zSegment();
	  vector<DTRecHit1D> thetaRecHits = thetaSeg->specificRecHits();
	  if((thetaRecHits.size() != 4)) {
	    if(debug)
	      cout << "[DTSegmentAnalysis] Theta segments has: " << thetaRecHits.size()
		   << " hits, skipping" << endl; // FIXME: info output
	    if(thetaRecHits.size()>4)
	      cout<< "[DTSegmentAnalysis] Warning! theta segments has:"<<thetaRecHits.size()<<"hits" <<endl;
	    continue;
	  }
	}
      const DTChamberRecSegment2D* phiSeg = (*segment4D).phiSegment();
      vector<DTRecHit1D> phiRecHits = phiSeg->specificRecHits();
      if(phiRecHits.size() != 8) {
	if(debug)
	  cout << "[DTSegmentAnalysis] Phi segments has: " << phiRecHits.size()
	       << " hits, skipping" << endl; // FIXME: info output
	if(phiRecHits.size()>8)
	  cout<< "[DTSegmentAnalysis] Warning! phi segments has:"<<phiRecHits.size()<<"hits" <<endl; 
	continue;
      }

      LocalPoint segment4DLocalPos = (*segment4D).localPosition();
      LocalVector segment4DLocalDirection = (*segment4D).localDirection();

      //Check for segment with big angle
      if((180 - segment4DLocalDirection.theta()* 180./Geom::pi() > 65)&& debug) {
	cout << "----------" << endl;
	cout << "Segment has Impact angle: = " << 180 - segment4DLocalDirection.theta()* 180./Geom::pi()  << endl;
	if((*segment4D).hasPhi()) {
	  cout << "    Phi Angle: " << atan(segment4DLocalDirection.x()/segment4DLocalDirection.z())* 180./Geom::pi() << endl;
	  const DTChamberRecSegment2D* phiSeg = (*segment4D).phiSegment();
	  vector<DTRecHit1D> phiRecHits = phiSeg->specificRecHits();
	  cout << "  #Phi Hits: " << phiRecHits.size() <<endl;
	  for(vector<DTRecHit1D>::const_iterator hit = phiRecHits.begin();
	      hit != phiRecHits.end(); hit++) {
	    cout << "      Hit in wire: " << (*hit).wireId() << endl;
	  }
	}
	if((*segment4D).hasZed()) {
	  cout << "    Theta Angle: " << atan(segment4DLocalDirection.y()/segment4DLocalDirection.z())* 180./Geom::pi() << endl;
	  const DTSLRecSegment2D* thetaSeg = (*segment4D).zSegment();
	  vector<DTRecHit1D> thetaRecHits = thetaSeg->specificRecHits();
	  cout << "  #Theta Hits: " << thetaRecHits.size() <<endl;
	  for(vector<DTRecHit1D>::const_iterator hit = thetaRecHits.begin();
	      hit != thetaRecHits.end(); hit++) {
	    cout << "      Hit in wire: " << (*hit).wireId() << endl;
	  }
	}

	cout << "----------" << endl;
      }
	
      if (segment4DLocalDirection.z()) {
	fillHistos(*chamberId,
		   segment4DLocalPos.x(), 
		   segment4DLocalPos.y(),
		   atan(segment4DLocalDirection.x()/segment4DLocalDirection.z())* 180./Geom::pi(),
		   atan(segment4DLocalDirection.y()/segment4DLocalDirection.z())* 180./Geom::pi(),
		   180 - segment4DLocalDirection.theta()* 180./Geom::pi(),
		   (*segment4D).chi2()/(*segment4D).degreesOfFreedom());
      } else {
	cout << "[DTSegmentAnalysis] Warning: segment local direction is: "
	     << segment4DLocalDirection << endl;
      }
    }
  }
}

  
// Book a set of histograms for a give chamber
void DTSegmentAnalysis::bookHistos(DTChamberId chamberId) {
  if(debug)
    cout << "   Booking histos for chamber: " << chamberId << endl;

  // Compose the chamber name
  stringstream wheel; wheel << chamberId.wheel();	
  stringstream station; station << chamberId.station();	
  stringstream sector; sector << chamberId.sector();	
  //   stringstream superLayer; superLayer << chamberId.superlayer();	
  //   stringstream layer; layer << chamberId.layer();	
  
  string chamberHistoName =
    "_W" + wheel.str() +
    "_St" + station.str() +
    "_Sec" + sector.str();
  theFile->cd();
  // Create the monitor elements
  histosPerCh[chamberId] =  new HSegment(chamberHistoName);
  histosNHits[chamberId] = new TH1F(string("hHHitsPerSegment"+chamberHistoName).c_str(),
				    "# hits per segment", 25,0,25);
  histosNHits[chamberId]->Sumw2();
}

void DTSegmentAnalysis::bookHistos(DTSuperLayerId slId) {
  if(debug)
    cout << "   Booking histos for SL: " << slId << endl;

  // Compose the chamber name
  stringstream wheel; wheel << slId.wheel();	
  stringstream station; station << slId.station();	
  stringstream sector; sector << slId.sector();	
  stringstream superLayer; superLayer << slId.superlayer();	
//   stringstream layer; layer << slId.layer();	
  
  string chamberHistoName =
    "DeltaT0_W" + wheel.str() +
    "_St" + station.str() +
    "_Sec" + sector.str() +
    "_SL" + superLayer.str();

  theFile->cd();
  // Create the monitor elements
  hT0CorrPerSL[slId] =  new TH1F(chamberHistoName.c_str(), chamberHistoName.c_str(), 100, -50, 50);
  hT0CorrPerSL[slId]->Sumw2();
}


// Fill a set of histograms for a give chamber 
void DTSegmentAnalysis::fillHistos(DTChamberId chamberId, int nsegm) {
  // FIXME: optimization of the number of searches
  if(histosPerCh.find(chamberId) == histosPerCh.end()) {
    bookHistos(chamberId);
  }
  theFile->cd();
  histosPerCh[chamberId]->Fill(nsegm);
}

// Fill a set of histograms for a give chamber 
void DTSegmentAnalysis::fillHistoNHits(DTChamberId chamberId, int nHits) {
  // FIXME: optimization of the number of searches
  if(histosPerCh.find(chamberId) == histosPerCh.end()) {
    bookHistos(chamberId);
  }
  theFile->cd();
  histosNHits[chamberId]->Fill(nHits);
}


// Fill a set of histograms for a give chamber 
void DTSegmentAnalysis::fillHistos(DTChamberId chamberId,
				   float posX,
				   float posY,
				   float phi,
				   float theta,
				   float impAngle,
				   float chi2) {
  // FIXME: optimization of the number of searches
  if(histosPerCh.find(chamberId) == histosPerCh.end()) {
    bookHistos(chamberId);
  }
  theFile->cd();
  histosPerCh[chamberId]->Fill(posX,
			       posY,
			       phi,
			       theta,
			       impAngle,
			       chi2);
}

void DTSegmentAnalysis::endJob() {
  // Write all histos to file
  theFile->cd();
  for(map<DTChamberId, HSegment* >::const_iterator chIdAndHisto = histosPerCh.begin();
      chIdAndHisto != histosPerCh.end(); ++chIdAndHisto) {
    (*chIdAndHisto).second->Write();
  }
  for(map<DTChamberId, TH1F *>::const_iterator chIdAndHistoNHits = histosNHits.begin();
      chIdAndHistoNHits!= histosNHits.end(); ++chIdAndHistoNHits) {
    (*chIdAndHistoNHits).second->Write();
  }

  for(map<DTSuperLayerId, TH1F *>::const_iterator slAndT0histo = hT0CorrPerSL.begin();
      slAndT0histo != hT0CorrPerSL.end(); ++slAndT0histo) {
    (*slAndT0histo).second->Write();
  }
}

