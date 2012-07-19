
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2012/03/05 21:43:17 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "RunLumiBXIndex.h"

RunLumiBXIndex::RunLumiBXIndex() : theRun(-1),
				   theLS(-1),
				   theBX(-1) {}


RunLumiBXIndex::RunLumiBXIndex(int aRun, int aLs, int aBx) : theRun(aRun),
							  theLS(aLs),
							  theBX(aBx) {}

RunLumiBXIndex::~RunLumiBXIndex(){}

bool RunLumiBXIndex::operator<(const RunLumiBXIndex& anIndex) const {
  if(theRun < anIndex.run()) return true;
  if(theRun == anIndex.run() && theLS < anIndex.lumiSection()) return true;
  if(theRun == anIndex.run() && theLS == anIndex.lumiSection() && theBX < anIndex.bx()) return true;
  return false;
  
}

int RunLumiBXIndex::run() const {
  return theRun;
}

int RunLumiBXIndex::lumiSection() const {
  return theLS;
}


int RunLumiBXIndex::bx() const {
  return theBX;
}
