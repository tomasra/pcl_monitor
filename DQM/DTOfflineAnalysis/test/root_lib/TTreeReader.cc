/*
 *  See header file for a description of this class.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - INFN Torino
 */

#include "TTreeReader.h"

#include "TString.h"
#include "TFile.h"
#include "TNtuple.h"
#include "DTSegmentObject.h"
#include "DTHitObject.h"

#include <iostream>



using namespace std;


TTreeReader::TTreeReader(const TString& fileName, const TString& outputFile) : theOutFile(outputFile) {
  // open the file containing the tree
  TFile *file = new TFile(fileName.Data());
  // Retrieve the TNtuple
  tree = (TNtuple *) file->Get("DTSegmentTree");

  segments = new TClonesArray("DTSegmentObject");
  
  cout << "Read File: " << fileName << endl;
  cout << "Opening tree: " << tree->GetName() << " with "
       << tree->GetEntries() << " entries" << endl;
  setBranchAddresses();

}

TTreeReader::~TTreeReader(){}



void TTreeReader::setBranchAddresses() {
  // set the addresses of the tree variables
  tree->SetBranchAddress("segments",&segments);
}




void TTreeReader::begin() {
  cout << "Begin" << endl;
}

void TTreeReader::processEvent(int entry) {
  int debug = 4;
  if(entry%100 || debug > 2) {
    cout << "Process event " << entry << endl;
  }
  
  // set the cuts here
  int NSEGMMIN = 12;
  double PHI_MIN = -9999.;
  double PHI_MAX = 9999.;
  double THETA_MIN = -9999.;
  double THETA_MAX = 9999.;
  
  cout << "  - # of segments: " << segments->GetEntriesFast() << endl;
  for(int iSegm=0; iSegm < segments->GetEntriesFast(); iSegm++) { // loop over segments 

    DTSegmentObject *oneSeg = (DTSegmentObject *) segments->At(iSegm);
//     if(debug > 2) cout << "   - Segment " << iSegm << " # hits: " << oneSeg->nHits << endl;
    
    // select segments
    if(oneSeg->nHits < NSEGMMIN) continue;
    if(oneSeg->phi < PHI_MIN || oneSeg->phi > PHI_MAX) continue;
    if(oneSeg->theta < THETA_MIN || oneSeg->theta > THETA_MAX) continue;
    

    for(int iHit = 0; iHit != oneSeg->nHits; ++iHit) { // loop over the hits belonging to the segment
      DTHitObject * hitObj = (DTHitObject *) oneSeg->hits->At(iHit);
      cout << "      hit: " << hitObj->resDist << endl;
    }
  }  
}


void TTreeReader::end() {
  cout << "End" << endl;

  // Create the root file
  TFile *theFile = new TFile(theOutFile.Data(), "RECREATE");
  theFile->cd();

  // Write the histos
  //   hMCPair->Write();
}

void TTreeReader::analyse() {
  begin();
  for(int i = 0; i < tree->GetEntries(); i++) {
    tree->GetEntry(i);
    processEvent(i);
  }
  end();
}

