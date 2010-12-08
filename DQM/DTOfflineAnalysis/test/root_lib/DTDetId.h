#ifndef DTDetId_H
#define DTDetId_H

/** \class DTDetId
 *  No description available.
 *
 *  $Date: 2009/07/20 08:52:46 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */
#include <iosfwd>


class DTDetId {
public:
  /// Constructor
  // NOTE: use 0 for all
  DTDetId(int aWheel, int aStation, int aSector, int aSl, int aLayer, int aWire);

  /// Destructor
  virtual ~DTDetId();
  
  // strict ordering 
  bool operator<(const DTDetId& aDetId) const;

  // Equality
  bool operator==(const DTDetId& aDetId) const;

  
//   bool matchesGranularity(const int granularity, const DTDetId& detid) const;

  // Operations
  int wheel;
  int station;
  int sector;
  int sl;
  int layer;
  int wire;
protected:

private:

  

};

std::ostream& operator<<( std::ostream& os, const DTDetId& id );

#endif


