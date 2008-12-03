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
 *  $Date: 2007/02/21 10:58:38 $
 *  $Revision: 1.3 $
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
  void analyze(const edm::Event& event, const edm::EventSetup& setup);
  void endJob();

protected:

private:
  TFile* theFile;

  bool debug;
  // Lable of 4D segments in the event
  std::string theRecHits4DLabel;

  // Book a set of histograms for a give chamber
  void bookHistos(DTChamberId chamberId);
  void bookHistos(DTSuperLayerId slId);

  // Fill a set of histograms for a give chamber 
  void fillHistos(DTChamberId chamberId, int nsegm);
  void fillHistos(DTChamberId chamberId,
		  float posX,
		  float posY,
		  float phi,
		  float theta,
		  float impAngle,
		  float chi2);
  void fillHistoNHits(DTChamberId chamberId, int nHits);

  std::map<DTChamberId, HSegment* > histosPerCh;
  std::map<DTChamberId, TH1F *> histosNHits;
  std::map<DTSuperLayerId, TH1F *> hT0CorrPerSL;

};
#endif

