#ifndef LumiFileReaderByBX_H
#define LumiFileReaderByBX_H

#include "RunLumiIndex.h"
#include "RunLumiBXIndex.h"

#include <map>
#include <TString.h>
#include <TH1F.h>

/** \class LumiFileReaderByBX
 *  No description available.
 *
 *  $Date: 2011/08/27 12:45:54 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

class LumiFileReaderByBX {
public:
  /// Constructor
  LumiFileReaderByBX(const TString& dirBaseName);

  /// Destructor
  virtual ~LumiFileReaderByBX();

  bool readFileForRun(const int run);


  // Operations
  void readFile(const TString& fileName, int runMin = -1, int runMax = -1);

  // Operations
  void readFileNew(const TString& fileName, int runMin = -1, int runMax = -1);

  // Operations
  bool readRootFile(const TString& fileName, int runMin = -1, int runMax = -1);
  
  
  float getDelLumi(const RunLumiIndex& runAndLumi) const;

  float getRecLumi(const RunLumiIndex& runAndLumi) const;
  
  float getAvgInstLumi(const RunLumiIndex& runAndLumi) const;

  float getDelIntegral(const RunLumiIndex& from, const RunLumiIndex& to) const;
  
  float getRecIntegral(const RunLumiIndex& from, const RunLumiIndex& to) const;

  std::pair<float, float> getLumi(const RunLumiIndex& runAndLumi) const;


  float getDelLumi(const RunLumiBXIndex& runAndLumiAndBx) const;

  float getRecLumi(const RunLumiBXIndex& runAndLumiAndBx) const;
  
  float getAvgInstLumi(const RunLumiBXIndex& runAndLumiAndBx) const;

  float getDelIntegral(const RunLumiBXIndex& from, const RunLumiBXIndex& to) const;
  
  float getRecIntegral(const RunLumiBXIndex& from, const RunLumiBXIndex& to) const;

  std::pair<float, float> getLumi(const RunLumiBXIndex& runAndLumiAndBx) const;

  bool checkCache(int run) const;


  float computeAvgInstLumi(float) const;

  std::pair<float, float> getRecIntegralInLumiBin(float instLumiMin, float instLumiMax) const;

  TH1F * getRecLumiBins(int nbins, float min, float max) const;

  void convertToRootFile() const;


protected:

private:
  
  TString theDirBaseName;
  int cachedRun;

  std::map<RunLumiIndex, std::pair<float, float> > theLumiMap;
  std::map<RunLumiBXIndex, std::pair<float, float> > theLumiByBXMap;

  std::map<int, std::vector< std::vector<float> > > theLumiTable;
  

//   std::map<unsigned int, std::vector<unsigned int, std::vector<std::pair<float, float> > > > theRunLSBxLumi;




};
#endif

