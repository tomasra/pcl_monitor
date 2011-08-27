
/*
 *  See header file for a description of this class.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - INFN Torino
 */

#include "RunLumiIndex.h"

RunLumiIndex::RunLumiIndex() : theRun(-1),
			       theLS(-1) {}


RunLumiIndex::RunLumiIndex(int run, int ls) : theRun(run),
					      theLS(ls) {}

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


