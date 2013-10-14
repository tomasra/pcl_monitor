#ifndef Utils_H
#define Utils_H

/** \class Utils
 *  No description available.
 *
 *  $Date: 2013/06/05 07:36:32 $
 *  $Revision: 1.3 $
 *  \author G. Cerminara - INFN Torino
 */

#include "TString.h"

class DTDetId;
class TCanvas;

namespace Utils {

  // Operations
  TString getHistoNameFromDetId(const DTDetId& detId);
  
  TString getHistoNameFromDetIdAndSet(const DTDetId& detId, const TString& set);

  TString getDTValidationHistoNameFromDetId(const DTDetId& detId, TString step="S3");
  
  TCanvas * newCanvas(TString name,
		      TString title="",
		      int xdiv=0,
		      int ydiv=0,
		      int form = 1,
		      int w=-1);

  TCanvas * newCanvas(TString name, int xdiv, int ydiv, int form, int w);
  TCanvas * newCanvas(int xdiv, int ydiv, int form = 1);
  TCanvas * newCanvas(int form = 1);
  TCanvas * newCanvas(TString name, int form, int w=-1);

  void newName(TNamed* obj);


};
#endif


  
