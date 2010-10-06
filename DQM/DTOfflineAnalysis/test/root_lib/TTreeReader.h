#ifndef TTreeReader_H
#define TTreeReader_H

/** \class TTreeReader
 *  No description available.
 *
 *  $Date: 2010/07/29 17:14:25 $
 *  $Revision: 1.5 $
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
  
  void setMinPt(float pt) {
    ptmin=pt;
  }
  
  void setDebug(int debug);
  

  

  
protected:


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
  std::map<TString, std::map<DTDetId, HSegment*> > histosSeg;
  
  // 1 -> SL
  int theGranularity;
  
  int nevents;

  std::map<TString, DTCut> cutSets;   

  int filterEvents;
  float ptmin;
  int debug;
};

#endif

