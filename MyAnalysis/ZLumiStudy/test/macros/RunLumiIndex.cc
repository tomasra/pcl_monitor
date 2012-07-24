
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2011/08/27 12:45:54 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "RunLumiIndex.h"

RunLumiIndex::RunLumiIndex() : theRun(-1),
			       theLS(-1) {}


RunLumiIndex::RunLumiIndex(int aRun, int aLs) : theRun(aRun),
					      theLS(aLs) {}

RunLumiIndex::~RunLumiIndex(){}

bool RunLumiIndex::operator<(const RunLumiIndex& anIndex) const {
  if(theRun < anIndex.run()) return true;
  if(theRun == anIndex.run() && theLS < anIndex.lumiSection()) return true;
  return false;
  
}

int RunLumiIndex::run() const {
  return theRun;
}

int RunLumiIndex::lumiSection() const {
  return theLS;
}


