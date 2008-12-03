#ifndef DTOfflineAnalysis_DTTimeAnalysis_H
#define DTOfflineAnalysis_DTTimeAnalysis_H

/*
 * \file DTTimeAnalysis.h
 *
 * $Date: 2007/02/19 12:15:37 $
 * $Revision: 1.2 $
 * \author M. Zanetti & G. Cerminara - INFN Padova & Torino
 *
*/

#include <FWCore/Framework/interface/EDAnalyzer.h>


#include <string>

// #include <fstream>
// #include <vector>


class DTTimeBoxAnalysis;
class DTTimeBoxMeanTimerAnalysis;
class TFile;

class DTTimeAnalysis: public edm::EDAnalyzer{

public:

/// Constructor
DTTimeAnalysis(const edm::ParameterSet& pset);

/// Destructor
virtual ~DTTimeAnalysis();

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
  DTTimeBoxAnalysis *theTimeBoxAnalysis;
  DTTimeBoxMeanTimerAnalysis *theTimeBoxMeanTimerAnalysis;
  
  bool doTimeBoxAnalysis;
  bool doTimeBoxMeanTimerAnalysis;
  
};

#endif
