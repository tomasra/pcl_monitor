#ifndef DTSegment2DAnalysis_H
#define DTSegment2DAnalysis_H

/** \class DTSegment2DAnalysis
 *  DQM 2DAnalysis of 4D DT segments, it produces plots about: <br>
 *      - number of segments per event <br>
 *      - position of the segments in chamber RF <br>
 *      - direction of the segments (theta and phi projections) <br>
 *      - reduced chi-square <br>
 *  All histos are produce per Chamber
 *
 *
 *  $Date: 2006/08/02 15:38:33 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "DataFormats/MuonDetId/interface/DTSuperLayerId.h"

#include <string>
#include <map>



class TFile;
class HSegment2D;

class DTSegment2DAnalysis {
public:
  /// Constructor
  DTSegment2DAnalysis(const edm::ParameterSet& pset, TFile* file);

  /// Destructor
  virtual ~DTSegment2DAnalysis();

  // Operations
  void analyze(const edm::Event& event, const edm::EventSetup& setup);
  void endJob();

protected:

private:
  TFile* theFile;

  bool debug;
  // Lable of 4D segments in the event
  std::string theRecHits2DLabel;

  // Book a set of histograms for a give sl
  void bookHistos(DTSuperLayerId slId);
  // Fill a set of histograms for a give sl 
  void fillHistos(DTSuperLayerId slId, int nsegm);
  void fillHistos(DTSuperLayerId slId,
		  float posX,
		  float angle,
		  float chi2);
  
  std::map<DTSuperLayerId, HSegment2D* > histosPerSL;


};
#endif

