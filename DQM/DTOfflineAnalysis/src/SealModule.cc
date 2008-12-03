#include "FWCore/Framework/interface/MakerMacros.h"

#include "DQM/DTOfflineAnalysis/interface/DTLocalRecoAnalysis.h"
DEFINE_ANOTHER_FWK_MODULE(DTLocalRecoAnalysis);

#include "DQM/DTOfflineAnalysis/interface/DTLocalReco2DAnalysis.h"
DEFINE_ANOTHER_FWK_MODULE(DTLocalReco2DAnalysis);

#include "DQM/DTOfflineAnalysis/interface/DTTimeAnalysis.h"
DEFINE_ANOTHER_FWK_MODULE(DTTimeAnalysis);

#include <DQM/DTOfflineAnalysis/src/DTOfflineOccupancy.h>
DEFINE_FWK_MODULE(DTOfflineOccupancy);

#include <DQM/DTOfflineAnalysis/src/TriggerPathFilter.h>
DEFINE_FWK_MODULE(TriggerPathFilter);

#include <DQM/DTOfflineAnalysis/src/BxNumberFilter.h>
DEFINE_FWK_MODULE(BxNumberFilter);

#include <DQM/DTOfflineAnalysis/src/BXDistanceFilter.h>
DEFINE_FWK_MODULE(BXDistanceFilter);

#include <DQM/DTOfflineAnalysis/src/EventListProducer.h>
DEFINE_FWK_MODULE(EventListProducer);

#include "DQM/DTOfflineAnalysis/src/TriggerSourceFilter.h"
DEFINE_FWK_MODULE(TriggerSourceFilter);

#include <DQM/DTOfflineAnalysis/src/DTNDigiFilter.h>
DEFINE_FWK_MODULE(DTNDigiFilter);
