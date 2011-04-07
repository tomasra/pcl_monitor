#ifndef ZZllvvAnalyzer_H
#define ZZllvvAnalyzer_H

/** \class ZZllvvAnalyzer
 *  No description available.
 *
 *  $Date: 2011/03/14 18:05:18 $
 *  $Revision: 1.3 $
 *  \author G. Cerminara - CERN
 */
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"


class TFile;
class HistoLept;

class ZZllvvAnalyzer   : public edm::EDAnalyzer {
public:
  /// Constructor
  ZZllvvAnalyzer(const edm::ParameterSet& pSet);

  /// Destructor
  virtual ~ZZllvvAnalyzer();

protected:

  // Operations
  virtual void beginJob();

  virtual void beginRun(const edm::Run& run, const edm::EventSetup& eSetup);

  virtual void beginLuminosityBlock(const edm::LuminosityBlock & iLumi, const edm::EventSetup & iSetup);
  virtual void endLuminosityBlock(const edm::LuminosityBlock & iLumi, const edm::EventSetup & iSetup);

  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob();



private:

  int totNEvents;
  float weight;

  TFile *theFile;
  edm::InputTag source;
  edm::InputTag zmmInput;
  bool debug;
  edm::ParameterSet vertexSelection;

};
#endif

