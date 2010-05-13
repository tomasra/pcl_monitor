/*
 *  See header file for a description of this class.
 *
 *  $Date: 2009/07/16 14:47:09 $
 *  $Revision: 1.3 $
 */

#include "DTMuObject.h"

using namespace std;

DTMuObject::DTMuObject() : 
  eta(-999),
  phi(-999),
  qpt(-999),
  wheel(-999),
  station(-999),
  sector(-999),
  nMuHits(-999),
  nStripHits(-999),
  nPixHits(-999),
  normChi2tk(-999),
  normChi2sta(-999),
  normChi2glb(-999),
  type(-999),
  sel(-999){
}


ClassImp(DTMuObject)
