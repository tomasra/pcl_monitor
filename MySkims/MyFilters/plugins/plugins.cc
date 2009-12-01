#include "FWCore/Framework/interface/MakerMacros.h"

#include <MySkims/MyFilters/src/TriggerPathFilter.h>
DEFINE_FWK_MODULE(TriggerPathFilter);

#include <MySkims/MyFilters/src/BxNumberFilter.h>
DEFINE_FWK_MODULE(BxNumberFilter);

// #include <MySkims/MyFilters/src/BXDistanceFilter.h>
// DEFINE_FWK_MODULE(BXDistanceFilter);

#include "MySkims/MyFilters/src/TriggerSourceFilter.h"
DEFINE_FWK_MODULE(TriggerSourceFilter);

#include <MySkims/MyFilters/src/DTNDigiFilter.h>
DEFINE_FWK_MODULE(DTNDigiFilter);

















