#ifndef DTRecoEventFilter_H
#define DTRecoEventFilter_H

/** \class DTRecoEventFilter
 *  No description available.
 *
 *  $Date: 2008/12/03 10:41:13 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "HLTrigger/HLTcore/interface/HLTFilter.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include <string>



class DTRecoEventFilter : public HLTFilter {
public:
  /// Constructor
  DTRecoEventFilter(const edm::ParameterSet&);

  /// Destructor
  virtual ~DTRecoEventFilter();

  // Operations
  virtual bool filter(edm::Event& event, const edm::EventSetup& setup);
  
protected:

private:
  std::string theRecHits4DLabel;
  edm::InputTag theDigiLabel;
};
#endif

