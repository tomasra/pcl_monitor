#ifndef DTTreeBuilder_H
#define DTTreeBuilder_H

/** \class DTTreeBuilder
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
 *  $Date: 2010/05/12 15:24:25 $
 *  $Revision: 1.3 $
 *  \author G. Cerminara - INFN Torino
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "DataFormats/MuonDetId/interface/DTSuperLayerId.h"
#include <FWCore/Framework/interface/ESHandle.h>

#include <string>
#include <vector>
#include <map>

class TFile;
class TH1F;
class TTree;
class TClonesArray;
class DTTtrig;
class DTT0;

class DTTreeBuilder {
public:
  /// Constructor
  DTTreeBuilder(const edm::ParameterSet& pset, TFile* file);

  /// Destructor
  virtual ~DTTreeBuilder();

  // Operations
  void analyze(const edm::Event& event, const edm::EventSetup& setup);
  void beginJob();
  void endJob();

protected:

private:
  // gives an angle between 0 and Pi
  double angleBtwPiAndPi(double angle) const;

  // gives an angle between -Pi/2 and Pi/2
  double angleBtwHPiAndHPi(double angle) const;


  TFile* theFile;

  bool debug;
  // Lable of 4D segments in the event
  std::string theRecHits4DLabel;
  // Lable of 1D rechits in the event
  std::string theRecHitLabel;
  
  // Switch for checking of noisy channels
  bool checkNoisyChannels;


  TTree *theTree;
  TClonesArray *segmentArray;
  edm::ESHandle<DTTtrig> tTrigMap;
  edm::ESHandle<DTT0> t0Handle;

};
#endif

