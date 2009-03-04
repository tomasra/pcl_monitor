#ifndef DTResolutionAnalysis_H
#define DTResolutionAnalysis_H

/** \class DTResolutionAnalysis
 *  DQM Analysis of rechit residuals: it compares the rechit distance from wire
 *  with the segment extrapolation.
 *  Only segments with 8 hits in phi view and 4 hits in the theta view (if available)
 *  are selected.<br>
 *  The plot produced are:<br>
 *      - residuals
 *      - meantimer (with the standard formula) for different position along the wire
 *      - time boxes for different position along the wire
 *  All histos are produce per SuperLayer.
 *
 *
 *  $Date: 2008/12/03 10:41:13 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "DataFormats/MuonDetId/interface/DTSuperLayerId.h"

#include <string>
#include <vector>
#include <map>

class HRes1DHits;
class TFile;
class TH1F;

class DTResolutionAnalysis {
public:
  /// Constructor
  DTResolutionAnalysis(const edm::ParameterSet& pset, TFile* file);

  /// Destructor
  virtual ~DTResolutionAnalysis();

  // Operations
  void analyze(const edm::Event& event, const edm::EventSetup& setup);
  void endJob();

protected:

private:
  TFile* theFile;

  bool debug;
  // Lable of 4D segments in the event
  std::string theRecHits4DLabel;
  // Lable of 1D rechits in the event
  std::string theRecHitLabel;
  

  // Book a set of histograms for a give sl
  void bookHistos(DTSuperLayerId slId);
  // Fill a set of histograms for a give sl 
  void fillHistos(DTSuperLayerId slId,
		  float dealtDist,
		  float distFromWire,
		  float deltaX,
		  float angle,
		  float sigma);

  std::map<DTSuperLayerId, HRes1DHits* > histosPerSL;
 
  // Switch for checking of noisy channels
  bool checkNoisyChannels;
};
#endif

