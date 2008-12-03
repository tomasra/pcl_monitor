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
 *  $Date: 2006/08/02 15:41:50 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - INFN Torino
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "DataFormats/MuonDetId/interface/DTSuperLayerId.h"

#include <string>
#include <vector>
#include <map>

class HResSL;
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
		  float distExtr,
		  float residual,
		  float xExtr,
		  float yExtr);

  std::map<DTSuperLayerId, HResSL* > histosPerSL;
 
  // Switch for checking of noisy channels
  bool checkNoisyChannels;
};
#endif

