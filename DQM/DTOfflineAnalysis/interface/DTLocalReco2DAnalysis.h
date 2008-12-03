#ifndef DTOffline2DAnalysis_DTLocalReco2DAnalysis_H
#define DTOffline2DAnalysis_DTLocalReco2DAnalysis_H

/*
 * \file DTLocalReco2DAnalysis.h
 *
 * $Date: 2007/02/19 12:15:36 $
 * $Revision: 1.2 $
 * \author M. Zanetti & G. Cerminara - INFN Padova & Torino
 *
*/

#include <FWCore/Framework/interface/EDAnalyzer.h>


#include <string>

// #include <fstream>
// #include <vector>


class DTSegment2DAnalysis;
class DTResolution2DAnalysis;
class TFile;

class DTLocalReco2DAnalysis: public edm::EDAnalyzer{

public:

/// Constructor
DTLocalReco2DAnalysis(const edm::ParameterSet& pset);

/// Destructor
virtual ~DTLocalReco2DAnalysis();

protected:

/// Analyze
void analyze(const edm::Event& event, const edm::EventSetup& setup);

// BeginJob
void beginJob(const edm::EventSetup& setup);

// EndJob
void endJob();

private:
  TFile *theFile;

  // Switch for verbosity
  bool debug;
  std::string theRootFileName;

  // Classes doing the analysis
  DTSegment2DAnalysis *theSegment2DAnalysis;
  DTResolution2DAnalysis *theResolution2DAnalysis;
  
  bool doSegment2DAnalysis;
  bool doResolution2DAnalysis;
  
};

#endif
