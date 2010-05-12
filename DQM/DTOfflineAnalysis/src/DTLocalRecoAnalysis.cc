/*
 * \file DTLocalRecoAnalysis.cc
 * 
 * $Date: 2009/04/14 17:32:06 $
 * $Revision: 1.3 $
 * \author M. Zanetti - INFN Padova
 *
*/

#include "DQM/DTOfflineAnalysis/interface/DTLocalRecoAnalysis.h"
#include "DQM/DTOfflineAnalysis/src/DTSegmentAnalysis.h"
#include "DQM/DTOfflineAnalysis/src/DTResolutionAnalysis.h"
#include "DQM/DTOfflineAnalysis/src/DTTreeBuilder.h"

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


DTLocalRecoAnalysis::DTLocalRecoAnalysis(const ParameterSet& pset) : theSegmentAnalysis(0),
								     theResolutionAnalysis(0) {
  debug = pset.getUntrackedParameter<bool>("debug", "false");

  if(debug)
    cout << "[DTLocalRecoAnalysis] Constructor called!" << endl;

  theRootFileName = pset.getUntrackedParameter<string>("rootFileName", "DTLocalRecoAnalysis.root");
  theFile = new TFile(theRootFileName.c_str(), "RECREATE");

  doSegmentAnalysis = pset.getUntrackedParameter<bool>("doSegmentAnalysis", "false");
  doResolutionAnalysis = pset.getUntrackedParameter<bool>("doResolutionAnalysis", "false");
  doTreeBuilder = pset.getUntrackedParameter<bool>("doTreeBuilder", "false");

  // Create the classes which really make the analysis
  if(doSegmentAnalysis)
    theSegmentAnalysis =
      new DTSegmentAnalysis(pset.getParameter<ParameterSet>("segmentAnalysisConfig"), theFile);
  if(doResolutionAnalysis)
    theResolutionAnalysis =
      new DTResolutionAnalysis(pset.getParameter<ParameterSet>("resolutionAnalysisConfig"), theFile);
  if(doTreeBuilder)
    theTreeBuilder =
      new DTTreeBuilder(pset.getParameter<ParameterSet>("treeBuilderConfig"), theFile);


}

DTLocalRecoAnalysis::~DTLocalRecoAnalysis(){
  if(debug)
    cout << "[DTLocalRecoAnalysis] Destructor called!" << endl;
  //   logFile.close();

}

void DTLocalRecoAnalysis::beginJob(){

  //dbe->
  if(doSegmentAnalysis)
    theSegmentAnalysis->beginJob();
  if(doResolutionAnalysis)
    theResolutionAnalysis->beginJob();
  if(doTreeBuilder)
    theTreeBuilder->beginJob();


}

void DTLocalRecoAnalysis::endJob() {
  if(doSegmentAnalysis)
    theSegmentAnalysis->endJob();
  if(doResolutionAnalysis)
    theResolutionAnalysis->endJob();
  if(doTreeBuilder)
    theTreeBuilder->endJob();
  
  

 theFile->Close();
}

void DTLocalRecoAnalysis::analyze(const Event& event, const EventSetup& setup){
  if(debug)
    cout << "--- [DTLocalRecoAnalysis] Analyze Run: " << event.id().run()
	 << " #Event: " << event.id().event() << endl;

  if(doSegmentAnalysis)
    theSegmentAnalysis->analyze(event, setup);

  if(doResolutionAnalysis)
    theResolutionAnalysis->analyze(event, setup);

  if(doTreeBuilder)
    theTreeBuilder->analyze(event, setup);


}

