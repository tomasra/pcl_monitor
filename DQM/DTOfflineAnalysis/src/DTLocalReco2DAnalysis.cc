/*
 * \file DTLocalRecoAnalysis.cc
 * 
 * $Date: 2008/10/27 16:25:25 $
 * $Revision: 1.2 $
 * \author M. Zanetti - INFN Padova
 *
*/

#include "DQM/DTOfflineAnalysis/interface/DTLocalReco2DAnalysis.h"
#include "DQM/DTOfflineAnalysis/src/DTSegment2DAnalysis.h"
#include "DQM/DTOfflineAnalysis/src/DTResolution2DAnalysis.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"


#include "TFile.h"
// #include <DataFormats/DTDigi/interface/DTDigi.h>
// #include <DataFormats/DTDigi/interface/DTDigiCollection.h>
// #include <DataFormats/MuonDetId/interface/DTLayerId.h>

#include <iostream>

using namespace std;
using namespace edm;


DTLocalReco2DAnalysis::DTLocalReco2DAnalysis(const ParameterSet& pset) : theSegment2DAnalysis(0),
								     theResolution2DAnalysis(0) {
  debug = pset.getUntrackedParameter<bool>("debug", "false");

  if(debug)
    cout << "[DTLocalReco2DAnalysis] Constructor called!" << endl;

  theRootFileName = pset.getUntrackedParameter<string>("rootFileName", "DTLocalReco2DAnalysis.root");
  theFile = new TFile(theRootFileName.c_str(), "RECREATE");

  doSegment2DAnalysis = pset.getUntrackedParameter<bool>("doSegment2DAnalysis", "false");
  doResolution2DAnalysis = pset.getUntrackedParameter<bool>("doResolution2DAnalysis", "false");
  
  // Create the classes which really make the analysis
  if(doSegment2DAnalysis)
    theSegment2DAnalysis =
      new DTSegment2DAnalysis(pset.getParameter<ParameterSet>("segment2DAnalysisConfig"), theFile);
  if(doResolution2DAnalysis)
    theResolution2DAnalysis =
      new DTResolution2DAnalysis(pset.getParameter<ParameterSet>("resolution2DAnalysisConfig"), theFile);
}

DTLocalReco2DAnalysis::~DTLocalReco2DAnalysis(){
  if(debug)
    cout << "[DTLocalReco2DAnalysis] Destructor called!" << endl;
  //   logFile.close();

}

void DTLocalReco2DAnalysis::beginJob(const EventSetup& setup){

  //dbe->


}

void DTLocalReco2DAnalysis::endJob() {
  if(doSegment2DAnalysis)
    theSegment2DAnalysis->endJob();
  if(doResolution2DAnalysis)
    theResolution2DAnalysis->endJob();
 theFile->Close();
}

void DTLocalReco2DAnalysis::analyze(const Event& event, const EventSetup& setup){
  cout << "--- [DTLocalReco2DAnalysis] Analyze Run: " << event.id().run()
       << " #Event: " << event.id().event() << endl;

  if(doSegment2DAnalysis)
    theSegment2DAnalysis->analyze(event, setup);

  if(doResolution2DAnalysis)
    theResolution2DAnalysis->analyze(event, setup);

}

