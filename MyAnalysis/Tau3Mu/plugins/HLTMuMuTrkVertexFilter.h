#ifndef HLTMuMuTrkVertexFilter_h
#define HLTMuMuTrkVertexFilter_h
//
// Package:    HLTstaging
// Class:      HLTMuMuTrkVertexFilter
// 
/**\class HLTMuMuTrkVertexFilter 

 HLT Filter for b to (mumu) + X

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  Nicolo Magini
//         Created:  Thu Nov  9 17:55:31 CET 2006
// Modified by Lotte Wilke
// Last Modification: 13.02.2007
//


// system include files
#include <memory>

#include "HLTrigger/HLTcore/interface/HLTFilter.h"

// ----------------------------------------------------------------------

namespace reco {
  class Candidate; 
  class Track;
}

class FreeTrajectoryState;
class MagneticField;
	
class HLTMuMuTrkVertexFilter : public HLTFilter {
 public:
  explicit HLTMuMuTrkVertexFilter(const edm::ParameterSet&);
  ~HLTMuMuTrkVertexFilter();
  
 private:
  virtual void beginJob() ;
  virtual bool hltFilter(edm::Event&, const edm::EventSetup&, trigger::TriggerFilterObjectWithRefs & filterproduct);
  virtual void endJob();
  virtual int overlap(const reco::Candidate&, const reco::Candidate&);
  virtual FreeTrajectoryState initialFreeState( const reco::Track&,const MagneticField*);
  
  edm::InputTag muCandLabel_;
  edm::InputTag trkCandLabel_; 
  edm::InputTag displacedMuVtxLabel_;

  const double thirdTrackMass_;
  const double maxEta_;
  const double minPt_;
  const double minInvMass_;
  const double maxInvMass_;
  const double maxNormalisedChi2_;
  const double minLxySignificance_;
  const double minCosinePointingAngle_;
  const double minVtxProb_;
  const double minD0Significance_;
  const bool fastAccept_;
  edm::InputTag beamSpotTag_;

};
#endif
