
#if !defined(__CINT__)||  defined(__MAKECINT__)
#include "TFile.h"
#include "TTree.h"
#include "TClonesArray.h"
#include "root_lib/DTSegmentObject.h"
#include "root_lib/DTHitObject.h"
#include "root_lib/TTreeReader.h"

#include "TSystem.h"
#include "TLorentzVector.h"
#endif

#include <iostream>

using namespace std;

string inputFile = "DTLocalRecoAnalysisStd.root";
// string inputFile = "DTLocalRecoAnalysisT0Seg.root";



void readTree() {
  TTreeReader *reader = new TTreeReader(inputFile, "test.root");
  reader->analyse(-1);
}
