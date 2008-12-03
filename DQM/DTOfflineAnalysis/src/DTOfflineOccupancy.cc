
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2008/10/21 10:29:45 $
 *  $Revision: 1.1 $
 *  \author G. Mila - INFN Torino
 */

#include "DQM/DTOfflineAnalysis/src/DTOfflineOccupancy.h"
#include "DQM/DTOfflineAnalysis/src/HistoStationOccupancy.h"

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

#include <iterator>
#include "TGraph.h"
#include "TVector3.h"

using namespace edm;
using namespace std;

DTOfflineOccupancy::DTOfflineOccupancy(const edm::ParameterSet& pset) : nEvents(0) {

  debug = pset.getUntrackedParameter<bool>("debug","false");
  if(debug)
    cout << "[DTOfflineOccupancy] Constructor called!" << endl;


  // names of the collection to be retrieved from the event
  theDigiLabel =  pset.getParameter<InputTag>("dtDigiLabel");
  theRecHitLabel =  pset.getParameter<InputTag>("dtRecHitLabel");
  theRecHits4DLabel = pset.getParameter<InputTag>("dtRecHit4DLabel");

  theFileName = pset.getUntrackedParameter<string>("rootFileName","DTOfflineOccupancy.root");
  mode = pset.getUntrackedParameter<string>("mode","");
}



DTOfflineOccupancy::~DTOfflineOccupancy(){
  if(debug)
    cout << "[DTOfflineOccupancy] Destructor called!" << endl;
}


void DTOfflineOccupancy::beginJob(const edm::EventSetup& context){

  theFile = new TFile(theFileName.c_str(),"RECREATE");
  theFile->cd();
  // --------------------------------------------
  int nDigi_MB1 = 200;
  double xMinDigi_MB1 = 0;
  double xMaxDigi_MB1 = 500;

  int nDigi_MB2 = 200;
  double xMinDigi_MB2 = 0;
  double xMaxDigi_MB2 = 500;

  int nDigi_MB3 = 200;
  double xMinDigi_MB3 = 0;
  double xMaxDigi_MB3 = 500;

  int nDigi_MB4 = 200;
  double xMinDigi_MB4 = 0;
  double xMaxDigi_MB4 = 500;

  // --------------------------------------------
  int n1DHits_MB1 = 200;
  double xMin1DHits_MB1 = 0;
  double xMax1DHits_MB1 = 500;

  int n1DHits_MB2 = 200;
  double xMin1DHits_MB2 = 0;
  double xMax1DHits_MB2 = 500;

  int n1DHits_MB3 = 200;
  double xMin1DHits_MB3 = 0;
  double xMax1DHits_MB3 = 300;

  int n1DHits_MB4 = 200;
  double xMin1DHits_MB4 = 0;
  double xMax1DHits_MB4 = 300;

  // --------------------------------------------
  int n4DSegm_MB1 = 20;
  double xMin4DSegm_MB1 = 0;
  double xMax4DSegm_MB1 = 20;

  int n4DSegm_MB2 = 20;
  double xMin4DSegm_MB2 = 0;
  double xMax4DSegm_MB2 = 20;

  int n4DSegm_MB3 = 20;
  double xMin4DSegm_MB3 = 0;
  double xMax4DSegm_MB3 = 20;

  int n4DSegm_MB4 = 20;
  double xMin4DSegm_MB4 = 0;
  double xMax4DSegm_MB4 = 20;


  if(mode == "halo") {
    nDigi_MB1 = 50;
    xMinDigi_MB1 = 0;
    xMaxDigi_MB1 = 50;

    nDigi_MB2 = 50;
    xMinDigi_MB2 = 0;
    xMaxDigi_MB2 = 50;

    nDigi_MB3 = 50;
    xMinDigi_MB3 = 0;
    xMaxDigi_MB3 = 50;

    nDigi_MB4 = 50;
    xMinDigi_MB4 = 0;
    xMaxDigi_MB4 = 50;

    // --------------------------------------------
    n1DHits_MB1 = 50;
    xMin1DHits_MB1 = 0;
    xMax1DHits_MB1 = 50;

    n1DHits_MB2 = 50;
    xMin1DHits_MB2 = 0;
    xMax1DHits_MB2 = 50;

    n1DHits_MB3 = 50;
    xMin1DHits_MB3 = 0;
    xMax1DHits_MB3 = 50;

    n1DHits_MB4 = 50;
    xMin1DHits_MB4 = 0;
    xMax1DHits_MB4 = 50;

    // --------------------------------------------
    n4DSegm_MB1 = 20;
    xMin4DSegm_MB1 = 0;
    xMax4DSegm_MB1 = 20;

    n4DSegm_MB2 = 20;
    xMin4DSegm_MB2 = 0;
    xMax4DSegm_MB2 = 20;

    n4DSegm_MB3 = 20;
    xMin4DSegm_MB3 = 0;
    xMax4DSegm_MB3 = 20;

    n4DSegm_MB4 = 20;
    xMin4DSegm_MB4 = 0;
    xMax4DSegm_MB4 = 20;
  }




  histo_digi_allMB1 = new HistoStationOccupancy("digi_allMB1",nDigi_MB1,xMinDigi_MB1,xMaxDigi_MB1);
  histo_digi_allMB1_allSL = new HistoStationOccupancy("digi_allMB1_allSL",nDigi_MB1,xMinDigi_MB1,xMaxDigi_MB1);
  histo_digi_allMB1_SL1 = new HistoStationOccupancy("digi_allMB1_SL1",nDigi_MB1,xMinDigi_MB1,xMaxDigi_MB1);
  histo_digi_allMB1_SL2 = new HistoStationOccupancy("digi_allMB1_SL2",nDigi_MB1,xMinDigi_MB1,xMaxDigi_MB1);
  histo_digi_allMB1_SL3 = new HistoStationOccupancy("digi_allMB1_SL3",nDigi_MB1,xMinDigi_MB1,xMaxDigi_MB1);

  histo_digi_allMB2 = new HistoStationOccupancy("digi_allMB2",nDigi_MB2,xMinDigi_MB2,xMaxDigi_MB2);
  histo_digi_allMB3 = new HistoStationOccupancy("digi_allMB3",nDigi_MB3,xMinDigi_MB3,xMaxDigi_MB3);
  histo_digi_allMB4 = new HistoStationOccupancy("digi_allMB4",nDigi_MB4,xMinDigi_MB4,xMaxDigi_MB4);

  histo_1Dhits_allMB1 = new HistoStationOccupancy("1Dhits_allMB1",n1DHits_MB1,xMin1DHits_MB1,xMax1DHits_MB1);
  histo_1Dhits_allMB2 = new HistoStationOccupancy("1Dhits_allMB2",n1DHits_MB2,xMin1DHits_MB2,xMax1DHits_MB2);
  histo_1Dhits_allMB3 = new HistoStationOccupancy("1Dhits_allMB3",n1DHits_MB3,xMin1DHits_MB3,xMax1DHits_MB3);
  histo_1Dhits_allMB4 = new HistoStationOccupancy("1Dhits_allMB4",n1DHits_MB4,xMin1DHits_MB4,xMax1DHits_MB4);

  histo_4Dsegm_allMB1 = new HistoStationOccupancy("4Dsegm_allMB1",n4DSegm_MB1,xMin4DSegm_MB1,xMax4DSegm_MB1);
  histo_4Dsegm_allMB2 = new HistoStationOccupancy("4Dsegm_allMB2",n4DSegm_MB2,xMin4DSegm_MB2,xMax4DSegm_MB2);
  histo_4Dsegm_allMB3 = new HistoStationOccupancy("4Dsegm_allMB3",n4DSegm_MB3,xMin4DSegm_MB3,xMax4DSegm_MB3);
  histo_4Dsegm_allMB4 = new HistoStationOccupancy("4Dsegm_allMB4",n4DSegm_MB4,xMin4DSegm_MB4,xMax4DSegm_MB4);

  // fill the map of EB energies from mail
  ebEnergyPerEvent[7995] = 160877;
  ebEnergyPerEvent[8282] = 134478;
  ebEnergyPerEvent[8551] = 131549;
  ebEnergyPerEvent[8853] = 138412;
  ebEnergyPerEvent[9116] = 174497;
  ebEnergyPerEvent[9414] = 165883;
  ebEnergyPerEvent[9694] = 161762;
  ebEnergyPerEvent[9999] = 158901;
  ebEnergyPerEvent[10295] = 164418;
  ebEnergyPerEvent[11971] = 147695;
  ebEnergyPerEvent[12261] = 133891;
  ebEnergyPerEvent[13073] = 105622;


 
}



void DTOfflineOccupancy::endJob(){
 if(debug)
    cout<<"[DTOfflineOccupancy] endjob called!"<<endl;
 
 cout << "[DTOfflineOccupancy] # of analyzed events: " << nEvents << endl;


 theFile->cd();

 // build the correlation plot between EB energy and MB3 # of digis
 const int corrSize = ebEnergyPerEvent.size();
 double ebEner[13];
 double dtDigis[13];

 int index = 0;
 for(map<int, double>::const_iterator eventAndEnergy = ebEnergyPerEvent.begin();
     eventAndEnergy != ebEnergyPerEvent.end(); ++eventAndEnergy) {
   ebEner[index] = (*eventAndEnergy).second;
   dtDigis[index] = numMB3DigisPerEvent[(*eventAndEnergy).first];
   ++index;
 }


 TGraph *ebVsDTCorr = new TGraph(corrSize, ebEner, dtDigis);
 ebVsDTCorr->SetName("ebVsDTCorr");
 ebVsDTCorr->Write();

 histo_digi_allMB1->write();
 histo_digi_allMB1_allSL->write();
 histo_digi_allMB1_SL1->write();
 histo_digi_allMB1_SL2->write();
 histo_digi_allMB1_SL3->write();

 histo_digi_allMB2->write();
 histo_digi_allMB3->write();
 histo_digi_allMB4->write();

 histo_1Dhits_allMB1->write();
 histo_1Dhits_allMB2->write();
 histo_1Dhits_allMB3->write();
 histo_1Dhits_allMB4->write();

 histo_4Dsegm_allMB1->write();
 histo_4Dsegm_allMB2->write();
 histo_4Dsegm_allMB3->write();
 histo_4Dsegm_allMB4->write();
 theFile->Close();

}
  


void DTOfflineOccupancy::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  nEvents++;
  bool doBaricenter = false;

  if(debug)
    cout << "[DTOfflineOccupancy] Analyze #Run: " << event.id().run()
	 << " #Event: " << event.id().event() << endl;
  if(!(event.id().event()%1000) && debug)
    {
      cout << "[DTOfflineOccupancy] Analyze #Run: " << event.id().run()
	   << " #Event: " << event.id().event() << endl;
    }

  map<DTChamberId, int> nDigisPerChamber;
  map<DTSuperLayerId, int> nDigisPerSL;
  map<DTChamberId, int> n1DHitsPerChamber;
  map<DTChamberId, int> n4DHitsPerChamber;

  // Digi collection
  edm::Handle<DTDigiCollection> dtdigis;
  event.getByLabel(theDigiLabel, dtdigis);

  // Get the 1D rechit collection from the event
  Handle<DTRecHitCollection> dt1DRecHits;
  event.getByLabel(theRecHitLabel, dt1DRecHits);

  // Get the 4D segment collection from the event
  edm::Handle<DTRecSegment4DCollection> all4DSegments;
  event.getByLabel(theRecHits4DLabel, all4DSegments);


  // Get the DT Geometry
  ESHandle<DTGeometry> dtGeom;
  setup.get<MuonGeometryRecord>().get(dtGeom);
  


  // ----------------------------------------------------------------------
  // Digi analysis

  DTDigiCollection::DigiRangeIterator dtLayerId_It;
  for (dtLayerId_It=dtdigis->begin(); dtLayerId_It!=dtdigis->end(); ++dtLayerId_It) { // Loop over layers
    DTChamberId chId = ((*dtLayerId_It).first).chamberId();
    DTSuperLayerId slId = ((*dtLayerId_It).first).superlayerId();
    int nDigisPerLayer = 0;
    
    nDigisPerLayer += distance(((*dtLayerId_It).second).first, ((*dtLayerId_It).second).second);
    nDigisPerChamber[chId] += nDigisPerLayer;
    nDigisPerSL[slId] += nDigisPerLayer;

//     for (DTDigiCollection::const_iterator digiIt = ((*dtLayerId_It).second).first;
// 	 digiIt!=((*dtLayerId_It).second).second; ++digiIt) { // Loop over all digis
//     }

  }


  // ----------------------------------------------------------------------
  // 1D hit analysis

  std::map<int, std::pair<double, double> > coordBaricenter;
  std::map<int, double> zBaricenter;
  std::map<int, double> counterBaricenter;
  std::map<int, TVector3> resultBaricenter;


  // Iterate over all detunits
  DTRecHitCollection::id_iterator detUnitIt;
  for (detUnitIt = dt1DRecHits->id_begin();
       detUnitIt != dt1DRecHits->id_end();
       ++detUnitIt){
    DTLayerId layId = *detUnitIt;
    DTChamberId chId = layId.chamberId();

    // Get the GeomDet from the setup
    const DTLayer* layer = dtGeom->layer(*detUnitIt);

    // Get the range for the corresponding LayerId
    DTRecHitCollection::range  range = dt1DRecHits->get((*detUnitIt));

    int n1DHitsPerLayer = distance(range.first, range.second);
    n1DHitsPerChamber[chId] += n1DHitsPerLayer;

    // Loop over the rechits of this DetUnit
    for (DTRecHitCollection::const_iterator rechit = range.first;
	 rechit!=range.second;
	   ++rechit){
      // Get the wireId of the rechit
      DTWireId wireId = (*rechit).wireId();

      if(doBaricenter && layId.station() == 3) {
	GlobalPoint glbPoint = layer->toGlobal((*rechit).localPosition());
	coordBaricenter[wireId.wheel()].first += glbPoint.x();
	coordBaricenter[wireId.wheel()].second += glbPoint.y();
	zBaricenter[wireId.wheel()] += glbPoint.z();
	counterBaricenter[wireId.wheel()]++;
      }
    }
  }

  if(doBaricenter) {
    for(int wheel = -2; wheel != 3; ++wheel) {
      TVector3 bariceter(coordBaricenter[wheel].first/counterBaricenter[wheel], 
			 coordBaricenter[wheel].second/counterBaricenter[wheel],
			 zBaricenter[wheel]/counterBaricenter[wheel]);
      resultBaricenter[wheel] = bariceter;
      cout << " wheel: " << wheel << " baricenter x: " << bariceter.x()
	   << " y: " << bariceter.y() << " z: " << bariceter.z() << endl;

    }
  }

  // ----------------------------------------------------------------------
  // 4D segment analysis

  // Loop over all chambers containing a segment
  DTRecSegment4DCollection::id_iterator chamberId;
  for (chamberId = all4DSegments->id_begin();
       chamberId != all4DSegments->id_end();
       ++chamberId){
    // Get the range for the corresponding ChamerId
    DTRecSegment4DCollection::range  range = all4DSegments->get(*chamberId);
    int nsegm = distance(range.first, range.second);
    n4DHitsPerChamber[*chamberId] = nsegm;
//      // Loop over the rechits of this ChamerId
//     for (DTRecSegment4DCollection::const_iterator segment4D = range.first;
// 	 segment4D!=range.second;
// 	   ++segment4D){
//     } //loop over segments
  } // loop over chambers



  // Plot the results:
  double totalNDigiSt3 = 0.;
  for(map<DTChamberId, int>::const_iterator nDigisCh = nDigisPerChamber.begin();
      nDigisCh != nDigisPerChamber.end(); ++nDigisCh) {
    DTChamberId chId = (*nDigisCh).first;
    int num = (*nDigisCh).second;
    if(chId.station() == 1) {
      histo_digi_allMB1->fill(num, chId.sector());
    } else if(chId.station() == 2) {
      histo_digi_allMB2->fill(num, chId.sector());
    } else if(chId.station() == 3) {
      histo_digi_allMB3->fill(num, chId.sector());
//       totalNDigiSt3 += num;
    } else if(chId.station() == 4) {
      histo_digi_allMB4->fill(num, chId.sector());
    }
  }

  for(map<DTSuperLayerId, int>::const_iterator digiPerSL = nDigisPerSL.begin();
      digiPerSL != nDigisPerSL.end(); ++digiPerSL) {
    DTSuperLayerId slId = (*digiPerSL).first;
    int num = (*digiPerSL).second;
    
    if(slId.station() == 1) {
      histo_digi_allMB1_allSL->fill(num, slId.sector());
      if(slId.superlayer() == 1) {
	histo_digi_allMB1_SL1->fill(num, slId.sector());
      } else if(slId.superlayer() == 2) {
	histo_digi_allMB1_SL2->fill(num, slId.sector());
      } else if(slId.superlayer() == 3) {
	histo_digi_allMB1_SL3->fill(num, slId.sector());
      }
    }
  }
  



  for(map<DTChamberId, int>::const_iterator n1DHitsCh = n1DHitsPerChamber.begin();
      n1DHitsCh != n1DHitsPerChamber.end(); ++n1DHitsCh) {
    DTChamberId chId = (*n1DHitsCh).first;
    int num = (*n1DHitsCh).second;
    if(chId.station() == 1) {
      histo_1Dhits_allMB1->fill(num, chId.sector());
    } else if(chId.station() == 2) {
      histo_1Dhits_allMB2->fill(num, chId.sector());
    } else if(chId.station() == 3) {
      totalNDigiSt3 += num;
      histo_1Dhits_allMB3->fill(num, chId.sector());
    } else if(chId.station() == 4) {
      histo_1Dhits_allMB4->fill(num, chId.sector());
    }
  }


  numMB3DigisPerEvent[(int)event.id().event()] = totalNDigiSt3;


  for(map<DTChamberId, int>::const_iterator n4DHitsCh = n4DHitsPerChamber.begin();
      n4DHitsCh != n4DHitsPerChamber.end(); ++n4DHitsCh) {
    DTChamberId chId = (*n4DHitsCh).first;
    int num = (*n4DHitsCh).second;
    if(chId.station() == 1) {
      histo_4Dsegm_allMB1->fill(num, chId.sector());
    } else if(chId.station() == 2) {
      histo_4Dsegm_allMB2->fill(num, chId.sector());
    } else if(chId.station() == 3) {
      histo_4Dsegm_allMB3->fill(num, chId.sector());
    } else if(chId.station() == 4) {
      histo_4Dsegm_allMB4->fill(num, chId.sector());
    }
  }


  


}

