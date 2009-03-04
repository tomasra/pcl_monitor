#ifndef DTSegmentAnalysis_H
#define DTSegmentAnalysis_H

/** \class DTSegmentAnalysis
 *  DQM Analysis of 4D DT segments, it produces plots about: <br>
 *      - number of segments per event <br>
 *      - position of the segments in chamber RF <br>
 *      - direction of the segments (theta and phi projections) <br>
 *      - reduced chi-square <br>
 *  All histos are produce per Chamber
 *
 *
 *  $Date: 2008/12/03 10:41:13 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "DataFormats/MuonDetId/interface/DTChamberId.h"
#include <DataFormats/MuonDetId/interface/DTSuperLayerId.h>

#include <string>
#include <map>



class TFile;
class HSegment;
class TH1F;

class DTSegmentAnalysis {
public:
  /// Constructor
  DTSegmentAnalysis(const edm::ParameterSet& pset, TFile* file);

  /// Destructor
  virtual ~DTSegmentAnalysis();

  // Operations
  void beginJob(const edm::EventSetup& setup);
  void analyze(const edm::Event& event, const edm::EventSetup& setup);
  void endJob();
  
protected:

private:
  TFile* theFile;

  bool debug;
  // Lable of 4D segments in the event
  std::string theRecHits4DLabel;

  std::map<DTChamberId, HSegment* > histoPerChamber;
  bool readVdrift;


};
#endif

