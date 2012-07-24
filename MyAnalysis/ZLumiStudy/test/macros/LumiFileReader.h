#ifndef LumiFileReader_H
#define LumiFileReader_H

#include "RunLumiIndex.h"

#include <map>
#include <TString.h>

/** \class LumiFileReader
 *  No description available.
 *
 *  $Date: 2011/08/27 12:45:54 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

class LumiFileReader {
public:
  /// Constructor
  LumiFileReader();

  /// Destructor
  virtual ~LumiFileReader();

  // Operations
  void readFile(const TString& fileName, int runMin = -1, int runMax = -1);
  
  double getDelLumi(const RunLumiIndex& runAndLumi) const;

  double getRecLumi(const RunLumiIndex& runAndLumi) const;
  
  double getAvgInstLumi(const RunLumiIndex& runAndLumi) const;

  double getDelIntegral(const RunLumiIndex& from, const RunLumiIndex& to) const;
  
  double getRecIntegral(const RunLumiIndex& from, const RunLumiIndex& to) const;

  std::pair<double, double> getLumi(const RunLumiIndex& runAndLumi) const;

  double computeAvgInstLumi(double) const;

  std::pair<double, double> getRecIntegralInLumiBin(double instLumiMin, double instLumiMax) const;

protected:

private:
  
  std::map<RunLumiIndex, std::pair<double, double> > theLumiMap;

};
#endif

