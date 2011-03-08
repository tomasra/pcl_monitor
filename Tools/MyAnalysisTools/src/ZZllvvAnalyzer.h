#ifndef ZZllvvAnalyzer_H
#define ZZllvvAnalyzer_H

/** \class ZZllvvAnalyzer
 *  No description available.
 *
 *  $Date: 2011/03/04 18:10:33 $
 *  $Revision: 1.1 $
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

  // Operations
  virtual void beginJob();

  virtual void beginRun(const edm::Run& run, const edm::EventSetup& eSetup);
  
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob();

protected:

private:

  int totNEvents;
  float weight;

  TFile *theFile;
  
//   HistoLept *muonS1;

};
#endif

