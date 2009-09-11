
/*
 *  See header file for a description of this class.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - INFN Torino
 */

#include "DQM/DTOfflineAnalysis/src/FEDSizeAnalysis.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"
#include <DataFormats/FEDRawData/interface/FEDRawData.h>
#include <DataFormats/FEDRawData/interface/FEDNumbering.h>
#include <DataFormats/FEDRawData/interface/FEDRawDataCollection.h>
#include <DataFormats/Common/interface/Handle.h>

#include <sstream>
#include <iostream>

#include "TFile.h"
#include "TNtuple.h"


using namespace std;
using namespace edm;


FEDSizeAnalysis::FEDSizeAnalysis(const ParameterSet& pset) {
  theRootFileName = pset.getUntrackedParameter<string>("rootFileName", "FEDSizeAnalysis.root");
  inputLabel = pset.getUntrackedParameter<InputTag>("inputLabel",InputTag("source"));

}

FEDSizeAnalysis::~FEDSizeAnalysis(){}



void FEDSizeAnalysis::beginJob(const EventSetup& setup) {


  stringstream branches;
  branches << "LS:event";

  // loop over all FEDS to check what is assigned
  for (int id=0; id != 1024; ++id) {
    
    // skip FEDs not assigned
    if(!FEDNumbering::inRange(id)) continue;

    feds.push_back(id);
//     if(feds.size() == 1) 
//       branches << "FED" << id;
//     else 
    branches << ":FED" << id;
  }
  
  // create the root file
  theFile = new TFile(theRootFileName.c_str(), "RECREATE");
  theNtuple =  new TNtuple("FEDSizeNtuple", "FED sizes", branches.str().c_str());



}


void FEDSizeAnalysis::endJob() {
  theFile->cd();
  theNtuple->Write();
  theFile->Close();
}


void FEDSizeAnalysis::analyze(const edm::Event& event, const edm::EventSetup& setup) {

  // get the raw data collection
  Handle<FEDRawDataCollection> rawdata;
  event.getByLabel(inputLabel, rawdata);
  const int nCols = feds.size()+2;

  float *values = new float[nCols];

  int i = 0;
  values[i++] = event.luminosityBlock();
    values[i++] = event.id().event();
  // loop over all FEDS
  for(vector<int>::const_iterator fed = feds.begin(); fed != feds.end(); ++fed) {
    // get the payload of this fed
    const FEDRawData& feddata = rawdata->FEDData(*fed);
    // get the event size
//     cout << i << " FED: " << *fed << " size: " << feddata.size() << endl;
    values[i++] = feddata.size();
  }

  // fill the ntuple
  theNtuple->Fill(values);
  delete [] values;

}
