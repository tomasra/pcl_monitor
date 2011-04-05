/*
 *  See header file for a description of this class.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - CERN
 */

#include "Tools/MyAnalysisTools/src/ReducedMETComputer.h"

ReducedMETComputer::ReducedMETComputer(){}

ReducedMETComputer::~ReducedMETComputer(){}


void compute() {
  
  TVector2 lepton1(theLeptons[0].Px(), theLeptons[0].Py());
  TVector2 lepton2(theLeptons[1].Px(), theLeptons[1].Py());;
  
  TVector2 bisector = (lepton1.Unit()+lepton2.Unit()).Unit();
  TVector2 bisector_perp(bisector.Py(), -bisector.Px());
  if(lepton1 * bisector_perp < 0) {
    bisector_perp *= -1;
  }
  
  TVector2 dilepton = lepton1 + lepton2;
  
  double leptonProj_long = dilepton*bisector;
  double leptonProj_perp = dilepton*bisector_perp;

  for(vector<TLorentzVector>::const_iterator jetit = theJets.begin();
      jetit != theJets.end();
      ++jetit) {
    TVector2 jet((*jetit).Px(), (*jetit).Py());
    

    
  }

}
  


