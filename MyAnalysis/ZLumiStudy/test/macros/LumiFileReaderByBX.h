#ifndef LumiFileReaderByBX_H
#define LumiFileReaderByBX_H

#include "RunLumiIndex.h"
#include "RunLumiBXIndex.h"

#include <map>
#include <TString.h>
#include <TH1F.h>

extern const float LENGTH_LS;

/** \class LumiFileReaderByBX
 *  This class reads the csv lumi files produced by lumiCalc2.py, convert them in root files (smaller and faster for the access) 
 *  and serves all the lumi information necessary for analysis.
 *  NOTE: to keep the memory @ a reasonable level the lumi data are loaded for 1 run @ the time and are kept in memory.
 *  For better performance it is therefore advisable to sort the analysis trees by run # (see the script 'sortTrees.r' for this.
 *
 *  HOWTO:
 *  lumiMap.checkCache(run) -> check if run already in memory
 *  lumiMap.readFileForRun(run) -> read a new run in memory	
 *  TH1F *histo = lumiMap.getRecLumiBins(nBins, binMin, binMax); -> gets the integal lumi by bin of inst. lumi
 *  RunLumiBXIndex runAndLumiAndBx(run, ls, bx); -> create an index for the lookup
 *  double instLumi = lumiMap.getAvgInstLumi(runAndLumiAndBx); -> get the Instantaneous lumi (averaged on the LS)
 *
 *  
 *  $Date: 2012/08/22 19:54:23 $
 *  $Revision: 1.8 $
 *  \author G. Cerminara - CERN
 */


class LumiFileReaderByBX {
public:
  /// Constructor
  /// The input parameter is the directory containing the csv/root luminosity files
  LumiFileReaderByBX(const TString& dirBaseName = "");

  /// Destructor
  virtual ~LumiFileReaderByBX();

  void setDirBaseName(const TString& dirBaseName);

  // read the file from disk unless it is already cached.
  // If the root file is already available for the run than it is used 
  // otherwise the root file is created
  bool readFileForRun(const int run, bool shouldreadCSV = false);

  // if the run is alredy cached return "false" otherwise "true" (don't ask me the logic...I don't remember!!!)
  bool checkCache(int run) const; 

  bool check_RunFound(int run) const;
  bool check_LSFound(const RunLumiIndex& runAndLumi) const;
  bool check_BXFilled(const RunLumiBXIndex& runAndLumiAndBx) const;
  bool isGood();

  float getDelLumi(const RunLumiIndex& runAndLumi) const;
  float getRecLumi(const RunLumiIndex& runAndLumi) const;
  float getAvgInstLumi(const RunLumiIndex& runAndLumi) const;
  float getDelIntegral(const RunLumiIndex& from) const;
  float getRecIntegral(const RunLumiIndex& from) const;
  std::pair<float, float> getLumi(const RunLumiIndex& runAndLumi) const;
  std::pair<float, float> getTotalLumi(const RunLumiIndex& runAndLumi) const;


  float getDelLumi(const RunLumiBXIndex& runAndLumiAndBx) const;

  float getRecLumi(const RunLumiBXIndex& runAndLumiAndBx) const;
  
  float getAvgInstLumi(const RunLumiBXIndex& runAndLumiAndBx) const;

  float getDelIntegral(const RunLumiBXIndex& from, const RunLumiBXIndex& to) const;
  
  float getRecIntegral(const RunLumiBXIndex& from, const RunLumiBXIndex& to) const;


  // returns a pair where first is the delivered inst lumi for a given BX and second is the inst recorded.
  // this looks for the values in 'theLumiTable'
  std::pair<float, float> getLumi(const RunLumiBXIndex& runAndLumiAndBx) const;

  float computeAvgInstLumi(float) const;

  //   std::pair<float, float> getRecIntegralInLumiBin(float instLumiMin, float instLumiMax) const;



  // Returns an histogram with the integrated luminosity for each of the "instantaneus" luminosity bins
  // defined using the 3 input parameters.
  // The integrals are computed starting from the "theLumiTable" content: therefore summing all the BX values
  // NOTE: we studied that the integrals computed the BX values of the recorded lumi are equivalenty to those returned forFIXME: should check that this is equivalent to the integral computed starting from the LS values in the CSV file
  TH1F * getRecLumiBins(int nbins, float min, float max) const;

  int getNumberLSs(const int run) const;
  int getNumberBX(const int run, const int ls) const;


protected:

private:

  // reads the CSV file
  //   void readCSVFile(const TString& fileName, int runMin = -1, int runMax = -1);

  // reads the CSV file and fills the theLumiTable container
  // FIXME: find out what changed....I don't remember anymore...
  void readCSVFileNew(const TString& fileName, int runMin = -1, int runMax = -1);

  // call the get_filling_scheme.py program to get the filling scheme for a run
  void getFillingScheme(int run);
  void createFillingSchemeFile(int run, const std::string& fileName);

  // read a root file from disk. The file name will be 1234.root where 1234 is the run #
  // in case the file is not found the function returns 'false'
  bool readRootFile(const TString& fileName, int runMin = -1, int runMax = -1);

  // dumps the tables (theLumiTable) currently in memory to a root file for future usage without passing by the CSV
  void convertToRootFile() const;

  
  TString theDirBaseName;
  int cachedRun;
  bool foundRun;

  //   std::map<RunLumiIndex, std::pair<float, float> > theLumiMap;
  //   std::map<RunLumiBXIndex, std::pair<float, float> > theLumiByBXMap;


  // For each run # (key of the map) stores a vector of *inst* lumi by BX for each LS.
  // NOTES: 
  // - the vector of BXes contains one number for BX (including not filled ones) representing the *recorded* lumi.
  //   The element '0' is the ratio recorded/delivered of the LS (assuming that dead times are evenly split
  // - the vector of LSs has one entry for each LS including those not actually in the CSVT file (containing an empty vector) 
  std::map<int, std::vector< std::vector<float> > > theLumiTable;
  std::map<int, std::vector< float > > theLumiRatioByRunByLS;

  std::map<int, std::vector< std::pair<float,float> > > theTotalLumiByRun;

  std::vector<bool> theFillingScheme;

//   std::map<unsigned int, std::vector<unsigned int, std::vector<std::pair<float, float> > > > theRunLSBxLumi;




};
#endif

