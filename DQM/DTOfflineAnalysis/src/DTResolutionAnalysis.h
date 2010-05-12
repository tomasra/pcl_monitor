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
 *  $Date: 2009/04/14 17:32:06 $
 *  $Revision: 1.3 $
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
  void beginJob();
  void endJob();

protected:

private:
  // gives an angle between 0 and PI
  double angleBtwPiAndPi(double angle) const;


  TFile* theFile;

  bool debug;
  // Lable of 4D segments in the event
  std::string theRecHits4DLabel;
  // Lable of 1D rechits in the event
  std::string theRecHitLabel;
  

  // Book a set of histograms for a give sl
  void bookHistos(DTSuperLayerId slId);

  std::map<DTSuperLayerId, HRes1DHits* > histosPerSL;
  std::map<DTSuperLayerId, HRes1DHits* > histosPerSL_angle5;
  std::map<DTSuperLayerId, HRes1DHits* > histosPerSL_angle15to20;
  std::map<DTSuperLayerId, HRes1DHits* > histosPerSL_angle25to30;
 
  // Switch for checking of noisy channels
  bool checkNoisyChannels;
};
#endif

