#ifndef SampleGroup_H
#define SampleGroup_H

/** \class SampleGroup
 *  No description available.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - CERN
 */

#include "TString.h"
#include <vector>

class SampleGroup {
public:
  /// Constructor
  SampleGroup(const TString& name, const TString& legendLabel, const TString& latexLabel,
	      bool isData, bool isSignal,
	      Color_t fcolor, Style_t fstyle = 1001, bool superImpose = false);


  SampleGroup();


  /// Destructor
  virtual ~SampleGroup();


  // Operations
  void addSample(const TString& sample);

  const TString& name() const {
    return theName;
  }
  
  const TString& legendLabel() const {
    return theLegendLabel;
  }

  const TString& latexLabel() const {
    return theLatexLabel;
  }
  
  bool isData() const {
    return isDataFlag;
  }

  bool isSignal() const {
    return isSignalFlag;
  }

  Color_t color() const {
    return theColor;
  }

  Style_t fillStyle() const {
    return theFillStyle;
  }

  bool superImpose() const {
    return superImposeFlag;
  } 

  const std::vector<TString> & samples() const {
    return theSamples;
  }


protected:

private:

  TString theName;
  TString theLegendLabel;
  TString theLatexLabel;
  bool isDataFlag;
  bool isSignalFlag;
  Color_t theColor;
  Style_t theFillStyle;
  bool superImposeFlag;

  // list of samples belonging to the group
  std::vector<TString> theSamples;

};
#endif

