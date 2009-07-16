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



class TClonesArray;
class TNtuple;

class TTreeReader {
public:
  /// Constructor
  TTreeReader(const TString& fileName, const TString& outputFile);

  /// Destructor
  virtual ~TTreeReader();

  // Operations
  void analyse();
  
//   void setChamber(int wheel, int station, int sector);
//   void setSL(int sl);
//   void setMinNHits(int nHits);
//   void setSegmPhiAngle(float min, float max);
//   void setSegmThetaAngle(float min, float max);
  

  
protected:


private:
  void begin();
  void processEvent(int entry);
  void end();
  void setBranchAddresses();

  
  
  TString theOutFile;

  TNtuple *tree;

  TClonesArray *segments;

};

#endif

