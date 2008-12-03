#ifndef DTNDigiFilter_H
#define DTNDigiFilter_H

/** \class DTNDigiFilter
 *  No description available.
 *
 *  $Date: 2008/10/21 10:29:45 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "HLTrigger/HLTcore/interface/HLTFilter.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

#include <string>


class DTNDigiFilter : public HLTFilter {
public:
  /// Constructor
  DTNDigiFilter(const edm::ParameterSet&);

  /// Destructor
  virtual ~DTNDigiFilter();

  // Operations
  virtual bool filter(edm::Event& event, const edm::EventSetup& setup);
  
  void endJob();

protected:

private:
  edm::InputTag theDigiLabel;
  bool debug;
  int threshold;
  std::string granularity;
  std::string cutType;

  int allEvents;
  int keptEvents;
  


};
#endif

