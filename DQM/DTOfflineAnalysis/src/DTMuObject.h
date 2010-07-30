#ifndef DTMuObject_H
#define DTMuObject_H

/** \class DTMuObject
 *  No description available.
 *
 *  $Date: 2010/07/30 10:32:47 $
 *  $Revision: 1.3 $
 */

#if !defined(__CINT__)||  defined(__MAKECINT__)
#include "TObject.h"
#include "TArrayD.h"
#include "TClonesArray.h"
#endif

class DTMuObject : public TObject {
public:
  /// Constructor
  DTMuObject();

  /// Destructor
  virtual ~DTMuObject(){};


public:
  
  float eta;
  float phi;
  float qpt;
  
  int nMuHits;
  int nStaDTHits;
  int nGlbDTHits;
  int nStaDTValidHits;
  int nGlbDTValidHits;
  int nStripHits;
  int nPixHits;

  float normChi2tk;
  float normChi2sta;
  float normChi2glb;

  //  type:
  // 1 -> STA + GLB + TM
  // 2 -> STA + GLB
  // 3 -> STA + TM
  // 4 -> TM
  // 5 -> STA 
  int type;

  // selection
  // 1 -> GlobalMuonPromptTight
  int sel;



private:

  ClassDef(DTMuObject,2)
};
#endif

