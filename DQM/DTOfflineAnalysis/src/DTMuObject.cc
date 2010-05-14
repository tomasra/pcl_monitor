/*
 *  See header file for a description of this class.
 *
 *  $Date: 2010/05/13 17:59:16 $
 *  $Revision: 1.1 $
 */

#include "DTMuObject.h"

using namespace std;

DTMuObject::DTMuObject() : 
  eta(-999),
  phi(-999),
  qpt(-999),
  nMuHits(-1),
  nStripHits(-1),
  nPixHits(-1),
  normChi2tk(-1.),
  normChi2sta(-1.),
  normChi2glb(-1.),
  type(-1),
  sel(-1){
}


ClassImp(DTMuObject)
