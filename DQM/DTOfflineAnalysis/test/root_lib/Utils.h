#ifndef Utils_H
#define Utils_H

/** \class Utils
 *  No description available.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - INFN Torino
 */

#include "TString.h"

class DTDetId;

class Utils {
public:
  /// Constructor
  Utils();

  /// Destructor
  virtual ~Utils();

  // Operations
  static TString getHistoNameFromDetId(const DTDetId& detId);
  
  static TString getHistoNameFromDetIdAndSet(const DTDetId& detId, const TString& set);
  

protected:

private:

};
#endif

