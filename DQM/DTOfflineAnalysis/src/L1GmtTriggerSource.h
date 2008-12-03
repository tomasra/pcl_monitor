#ifndef L1GmtTriggerSource_H
#define L1GmtTriggerSource_H

/** \class L1GmtTriggerSource
 *  No description available.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - INFN Torino
 */


#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

class HBxDistance;
class TFile;

class L1GmtTriggerSource : public edm::EDAnalyzer {
public:
  explicit L1GmtTriggerSource(const edm::ParameterSet&);
  ~L1GmtTriggerSource();


private:
  virtual void beginJob(const edm::EventSetup&) ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  int bxDist(const std::pair<int, int>& previousId, const std::pair<int, int>& currentId) const;


  // ----------member data ---------------------------
  edm::InputTag m_GMTInputTag;
  edm::InputTag inputLabel;
  
  std::pair<int, int> prevOrbtAndBxAll;
  std::pair<int, int> prevOrbtAndBxDT;
  std::pair<int, int> prevOrbtAndBxRPC;
  std::pair<int, int> prevOrbtAndBxDTorRPC;
  std::pair<int, int> prevOrbtAndBxDTonly;
  std::pair<int, int> prevOrbtAndBxRPConly;

  HBxDistance *hDT;
  HBxDistance *hAll;
  HBxDistance *hDTorRPC;
  HBxDistance *hRPC;
  HBxDistance *hDTonly;
  HBxDistance *hRPConly;

  TFile *theFile;
  
  bool debug;

};



#endif



























