#ifndef SimTreeReader_H
#define SimTreeReader_H

/** \class SimTreeReader
 *  No description available.
 *
 *  $Date: 2009/07/27 12:35:44 $
 *  $Revision: 1.3 $
 *  \author G. Cerminara - INFN Torino
 */

#include "TString.h"
#include "DTCut.h"
#include "DTDetId.h"
#include <map>


class TClonesArray;
class TTree;
class HRes1DHits;
class HSegment;

class SimTreeReader {
public:
  /// Constructor
  SimTreeReader(const TString& outputFile);

  /// Destructor
  virtual ~SimTreeReader();

  // Operations
  // nEventMax = -1 -> All
  void addInputFile(int index, const TString& fileName);

  void analyse(const int nEventMax = -1);
  
  void setGranularity(const TString& granularity);
//   void setChamber(int wheel, int station, int sector);
//   void setSL(int sl);

  void setCuts(const TString&set, const DTCut& cut); 


  
  void setDebug(int debug);
  

  

  
protected:


private:
  void begin();
  void processEvent(int fileIndex, int entry);
  void end();

  DTDetId buildDetid(int wheel, int station, int sector, int sl, int layer, int wire) const;

//   TString getNameFromDetId(const DTDetId& detId) const;
  
  
  TString theOutFile;

//   TTree *tree;

  TClonesArray *segments;

  // Histograms
//   std::map<TString, std::map<DTDetId, HRes1DHits*> > histosRes;
//   std::map<TString, std::map<DTDetId, HSegment*> > histosSeg;
  
  // 1 -> SL
  int theGranularity;
  
  int nevents;

  std::map<TString, DTCut> cutSets;   

  std::map<int, TTree *> treeMap;
  std::map<int, TClonesArray *> segmContMap;
  

  int debug;
};

#endif

