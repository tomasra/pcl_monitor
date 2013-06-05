#ifndef Utils_H
#define Utils_H

/** \class Utils
 *  No description available.
 *
 *  $Date: 2009/09/11 10:53:22 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - INFN Torino
 */

#include "TString.h"

class DTDetId;
class TCanvas;

class Utils {
public:
  /// Constructor
  Utils();

  /// Destructor
  virtual ~Utils();

  // Operations
  static TString getHistoNameFromDetId(const DTDetId& detId);
  
  static TString getHistoNameFromDetIdAndSet(const DTDetId& detId, const TString& set);

  static TString getDTValidationHistoNameFromDetId(const DTDetId& detId, TString step="S3");
  
  static TCanvas * newCanvas(TString name,
			     TString title="",
			     int xdiv=0,
			     int ydiv=0,
			     int form = 1,
			     int w=-1);

  static TCanvas * newCanvas(TString name, int xdiv, int ydiv, int form, int w);
  static TCanvas * newCanvas(int xdiv, int ydiv, int form = 1);
  static TCanvas * newCanvas(int form = 1);
  static TCanvas * newCanvas(TString name, int form, int w=-1);


protected:

private:

};
#endif


  
