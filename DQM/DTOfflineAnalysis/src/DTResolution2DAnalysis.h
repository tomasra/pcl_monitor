#ifndef DTResolution2DAnalysis_H
#define DTResolution2DAnalysis_H

/** \class DTResolution2DAnalysis
 *  DQM 2DAnalysis of rechit residuals: it compares the rechit distance from wire
 *  with the segment extrapolation.
 *  Only segments with 8 hits in phi view and 4 hits in the theta view (if available)
 *  are selected.<br>
 *  The plot produced are:<br>
 *      - residual on the distance from the wire <br>
 *      - residual on the distance from the wire vs distance from wire <br>
 *  All histos are produce per SuperLayer.
 *
 *
 *  $Date: 2006/08/02 15:36:47 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "DataFormats/MuonDetId/interface/DTSuperLayerId.h"

#include <string>
#include <vector>
#include <map>

class DTTTrigBaseSync;
class HRes2DSL;
class TFile;
class TH1F;

class DTResolution2DAnalysis {
public:
  /// Constructor
  DTResolution2DAnalysis(const edm::ParameterSet& pset, TFile* file);

  /// Destructor
  virtual ~DTResolution2DAnalysis();

  // Operations
  void analyze(const edm::Event& event, const edm::EventSetup& setup);
  void endJob();

protected:

private:
  TFile* theFile;

  bool debug;
  // Lable of 2D segments in the event
  std::string theRecHits2DLabel;
  // Lable of 1D rechits in the event
  std::string theRecHitLabel;
  

  // Book a set of histograms for a give sl
  void bookHistos(DTSuperLayerId slId);
  // Fill a set of histograms for a give sl 
  void fillHistos(DTSuperLayerId slId,
		  float distExtr,
		  float residual,
		  float xExtr);
  std::map<DTSuperLayerId, HRes2DSL* > histosPerSL;

  // Switch for checking of noisy channels
  bool checkNoisyChannels;

};
#endif

