#ifndef RunLumiBXIndex_H
#define RunLumiBXIndex_H

/** \class RunLumiBXIndex
 *  No description available.
 *
 *  $Date: 2011/08/27 12:45:54 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - CERN
 */

class RunLumiBXIndex {
public:
  /// Constructor
  RunLumiBXIndex();

  RunLumiBXIndex(int run, int ls, int bx);

  /// Destructor
  virtual ~RunLumiBXIndex();

  // Operations
  bool operator<(const RunLumiBXIndex& anIndex) const;

  int run() const;

  int lumiSection() const;

  int bx() const;
  
protected:

private:
  
  int theRun;
  int theLS;
  int theBX;

};
#endif

