#include "FWCore/Framework/interface/MakerMacros.h"

#include "DQM/DTOfflineAnalysis/interface/DTLocalRecoAnalysis.h"
DEFINE_FWK_MODULE(DTLocalRecoAnalysis);

#include "DQM/DTOfflineAnalysis/interface/DTLocalReco2DAnalysis.h"
DEFINE_FWK_MODULE(DTLocalReco2DAnalysis);

#include "DQM/DTOfflineAnalysis/interface/DTTimeAnalysis.h"
DEFINE_FWK_MODULE(DTTimeAnalysis);

#include <DQM/DTOfflineAnalysis/src/DTOfflineOccupancy.h>
DEFINE_FWK_MODULE(DTOfflineOccupancy);

// #include <DQM/DTOfflineAnalysis/src/BXDistanceFilter.h>
// DEFINE_FWK_MODULE(BXDistanceFilter);

// #include <DQM/DTOfflineAnalysis/src/EventListProducer.h>
// DEFINE_FWK_MODULE(EventListProducer);

#include <DQM/DTOfflineAnalysis/src/MuonAnalysis.h>
DEFINE_FWK_MODULE(MuonAnalysis);


#include "DQM/DTOfflineAnalysis/src/FEDSizeAnalysis.h"
DEFINE_FWK_MODULE(FEDSizeAnalysis);
