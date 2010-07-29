#ifndef DTOfflineOccupancy_H
#define DTOfflineOccupancy_H

/** \class DTOfflineOccupancy
 *  Offline analysis
 *
 *  $Date: 2008/12/03 10:41:13 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <FWCore/Framework/interface/EDAnalyzer.h>
#include "FWCore/Utilities/interface/InputTag.h"

#include <string>
#include <vector>
#include <map>

class HistoStationOccupancy;
class TFile;

class DTOfflineOccupancy: public edm::EDAnalyzer{
public:
  /// Constructor
  DTOfflineOccupancy(const edm::ParameterSet& pset);

  /// Destructor
  virtual ~DTOfflineOccupancy();

  /// book the histos
  void beginJob(const edm::EventSetup& c);

  /// Endjob
  void endJob();

  // Operations
  void analyze(const edm::Event& event, const edm::EventSetup& setup);

protected:

private:


  // Switch for verbosity
  bool debug;

  // The label to retrieve the digis 
  edm::InputTag theDigiLabel;
  edm::InputTag theRecHitLabel;

  // Lable of 4D segments in the event
  edm::InputTag theRecHits4DLabel;

  HistoStationOccupancy *histo_digi_allMB1;
  HistoStationOccupancy *histo_digi_allMB1_allSL;
  HistoStationOccupancy *histo_digi_allMB1_SL1;
  HistoStationOccupancy *histo_digi_allMB1_SL2;
  HistoStationOccupancy *histo_digi_allMB1_SL3;



  HistoStationOccupancy *histo_digi_allMB2;
  HistoStationOccupancy *histo_digi_allMB3;
  HistoStationOccupancy *histo_digi_allMB4;

  HistoStationOccupancy *histo_1Dhits_allMB1;
  HistoStationOccupancy *histo_1Dhits_allMB2;
  HistoStationOccupancy *histo_1Dhits_allMB3;
  HistoStationOccupancy *histo_1Dhits_allMB4;

  HistoStationOccupancy *histo_4Dsegm_allMB1;
  HistoStationOccupancy *histo_4Dsegm_allMB2;
  HistoStationOccupancy *histo_4Dsegm_allMB3;
  HistoStationOccupancy *histo_4Dsegm_allMB4;

  std::string theFileName;
  TFile *theFile;

  std::map<int, double> ebEnergyPerEvent;
  std::map<int, double> numMB3DigisPerEvent;

  int nEvents;
  std::string mode;

};
#endif

