#ifndef TTreeReader_H
#define TTreeReader_H

/** \class TTreeReader
 *  No description available.
 *
 *  $Date: 2011/02/13 22:24:33 $
 *  $Revision: 1.9 $
 *  \author G. Cerminara - INFN Torino
 */

#include "TString.h"
#include "DTCut.h"
#include "DTDetId.h"
#include <map>


class TClonesArray;
class HRes1DHits;
class HSegment;
class TTree;
class DTCalibrationMap;



class TTreeReader {
public:
  /// Constructor
  TTreeReader(const TString& fileName, const TString& outputFile);

  TTreeReader(TTree* tree, const TString& outputFile);

  /// Destructor
  virtual ~TTreeReader();

  // Operations
  // nEventMax = -1 -> All
  void analyse(const int nEventMax = -1);
  
  void setGranularity(const TString& granularity);
//   void setChamber(int wheel, int station, int sector);
//   void setSL(int sl);

  void setCuts(const TString&set, const DTCut& cut); 


  void setFilterEvents(int option) {
    filterEvents=option;
  }

  /// Hack to skip problematic SLs
  void setFilterSL(bool option) {
    filterSL=option;
  }  

  /// Deprecated; use a cut instead
  /// 1 : Select only R; -1: select only L; 0: both
  void setSelectLR(int option) {
    selectLR=option;
  }

  void setMinPt(float pt) {
    ptmin=pt;
  }
  
  void setRunRange(int runMin, int runMax) {
    runmin =runMin;
    runmax =runMax;
  }
  

  void setDebug(int debug);
  

  void setCalibrationMap(const std::string& filename,
			 const std::string& granularity,
			 unsigned int fields);

  
public:
  bool doStep1;
  int detail;

private:
  void begin();
  void processEvent(int entry);
  void end();
  void setBranchAddresses();

  DTDetId buildDetid(int wheel, int station, int sector, int sl, int layer, int wire) const;

//   TString getNameFromDetId(const DTDetId& detId) const;
  
  
  TString theOutFile;

  TTree *tree;

  TClonesArray *segments;
  TClonesArray *muons;
  int run;


  // Histograms
  std::map<TString, std::map<DTDetId, HRes1DHits*> > histosRes;
  std::map<TString, std::map<DTDetId, HRes1DHits*> > histosResS1;

  std::map<TString, std::map<DTDetId, HSegment*> > histosSeg;
  
  // 1 -> SL
  int theGranularity;
  
  int nevents;

  std::map<TString, DTCut> cutSets;   

  int filterEvents;
  int selectLR;    // -1 = L hits; 1=R hits; 0=both
  bool filterSL;   // skip predefined list of SLs
  float ptmin;
  int runmin;
  int runmax;
  int debug;

  bool readCalibTable;
  DTCalibrationMap *calibMap;

};

#endif

