#ifndef ReducedMETComputer_H
#define ReducedMETComputer_H

/** \class ReducedMETComputer
 *  No description available.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - CERN
 */

class ReducedMETComputer {
public:
  /// Constructor
  ReducedMETComputer(const std::vector<TLorentzVector>& leptons,
		     const std::vector<TLorentzVector>& jets,
		     const TLorentzVector& met);

  /// Destructor
  virtual ~ReducedMETComputer();

  
  

protected:

private:
  
  std::vector<TLorentzVector> theLeptons;
  std::vector<TLorentzVector> theJets;
  TLorentzVector theMET;
  

};
#endif

