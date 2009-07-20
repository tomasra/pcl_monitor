#ifndef TTreeReader_H
#define TTreeReader_H

/** \class TTreeReader
 *  No description available.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - INFN Torino
 */

#include "TString.h"

#include "DTDetId.h"
#include <map>


class TClonesArray;
class TNtuple;
class HRes1DHits;


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
  void setMinNHits(int nHits);
  void setSegmPhiAngle(float min, float max);
  void setSegmThetaAngle(float min, float max);

  

  

  
protected:


private:
  void begin();
  void processEvent(int entry);
  void end();
  void setBranchAddresses();

  DTDetId buildDetid(int wheel, int station, int sector, int sl, int layer, int wire) const;

  TString getNameFromDetId(const DTDetId& detId) const;
  
  
  TString theOutFile;

  TNtuple *tree;

  TClonesArray *segments;

  // Histograms
  std::map<DTDetId, HRes1DHits*> histos;
  
  // 1 -> SL
  int theGranularity;
  
  int nevents;

  // set the cuts here
  int NHITSMIN;
  double PHI_MIN;
  double PHI_MAX;
  double THETA_MIN;
  double THETA_MAX;
  

};

#endif

