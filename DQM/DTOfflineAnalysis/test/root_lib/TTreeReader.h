#ifndef TTreeReader_H
#define TTreeReader_H

/** \class TTreeReader
 *  No description available.
 *
 *  $Date: 2009/07/20 08:52:47 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - INFN Torino
 */

#include "TString.h"
#include "DTCut.h"
#include "DTDetId.h"
#include <map>


class TClonesArray;
class TNtuple;
class HRes1DHits;
class HSegment;

class TTreeReader {
public:
  /// Constructor
  TTreeReader(const TString& fileName, const TString& outputFile);

  /// Destructor
  virtual ~TTreeReader();

  // Operations
  // nEventMax = -1 -> All
  void analyse(const int nEventMax = -1);
  
  void setGranularity(const TString& granularity);
//   void setChamber(int wheel, int station, int sector);
//   void setSL(int sl);

  void setCuts(const TString&set, const DTCut& cut); 


  
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

  TNtuple *tree;

  TClonesArray *segments;

  // Histograms
  std::map<TString, std::map<DTDetId, HRes1DHits*> > histosRes;
  std::map<TString, std::map<DTDetId, HSegment*> > histosSeg;
  
  // 1 -> SL
  int theGranularity;
  
  int nevents;

  std::map<TString, DTCut> cutSets;   

  int debug;
};

#endif

