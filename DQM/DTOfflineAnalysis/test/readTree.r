
#if !defined(__CINT__)||  defined(__MAKECINT__)
#include "TFile.h"
#include "TTree.h"
#include "TClonesArray.h"
#include "root_lib/DTSegmentObject.h"
#include "root_lib/DTHitObject.h"
#include "root_lib/TTreeReader.h"

#include "TSystem.h"
#include "TMath.h"
#include "TLorentzVector.h"
#endif

#include <iostream>

using namespace std;


// int NEVENTS = 500000;
int NEVENTS = -1;
//int NEVENTS = 1000;


string tag = "t0";
// string tag = "t-2";
// string tag = "t2";
// string tag = "t4";
// string tag = "t-4";

string version = "test";


int debug = 0;


// string inputFile = "/data/c/cerminar/data/DTAnalysis/DTCalibration/r67647_" + tag + "_V00/DTLocalRecoAnalysisStd_merged.root";
string inputFile = "/data/CMS/DtCalibrationGoodCollV9-100507-V03_Fix/DTLocalRecoAnalysisStd.root";

string outputFile = "test.root";

void readTree() {
  TTreeReader *reader = new TTreeReader(inputFile, outputFile);
  reader->setDebug(debug);
  reader->setGranularity("station");
  reader->setGranularity("statByView");
  reader->setGranularity("statBySL");
  //reader->setGranularity("chamberByView");

  // all segments
//   DTCut stdCut;
//   reader->setCuts("all",stdCut);
  // only segments with 12 hits
  DTCut hqCut;
  hqCut.setSegmNHits(5,100);
  hqCut.setSegmNHitsPhi(6,10);
  hqCut.setSegmNHitsTheta(4,6);
  reader->setCuts("Cut1",hqCut);

//   DTCut hqPhiCut;
//   hqPhiCut.setSegmNHitsPhi(7,9);
//   reader->setCuts("hqPhi",hqPhiCut);

//   DTCut hqPhiVCut;
//   hqPhiVCut.setSegmNHitsPhi(7,9);
//   hqPhiVCut.setSegmPhiAngle((90.-15.)*TMath::DegToRad(), (90.+15.)*TMath::DegToRad());
//   reader->setCuts("hqPhiV",hqPhiVCut);

//   DTCut hqPhiVVCut;
//   hqPhiVVCut.setSegmNHitsPhi(7,9);
//   hqPhiVVCut.setSegmNHitsTheta(4,5);
//   hqPhiVVCut.setSegmPhiAngle((90.-5.)*TMath::DegToRad(), (90.+5.)*TMath::DegToRad());
//   reader->setCuts("hqPhiVV",hqPhiVVCut);
               
  reader->analyse(NEVENTS);
}
