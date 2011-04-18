
/*
 *  See header file for a description of this class.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - CERN
 */

#include "SampleGroup.h"

SampleGroup::SampleGroup(const TString& name, const TString& legendLabel, const TString& latexLabel,
			 bool isData, bool isSignal,
			 Color_t fcolor, Style_t fstyle, bool superImpose) :    theName(name),
										theLegendLabel(legendLabel),
										theLatexLabel(latexLabel),
										isDataFlag(isData),
										isSignalFlag(isSignal),
										theColor(fcolor),
										theFillStyle(fstyle),
										superImposeFlag(superImpose) {}

SampleGroup::SampleGroup() {}



SampleGroup::~SampleGroup(){}



void SampleGroup::addSample(const TString& sample) {
  theSamples.push_back(sample);
}
