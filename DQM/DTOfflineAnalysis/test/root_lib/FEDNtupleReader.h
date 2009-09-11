#ifndef FEDNtupleReader_H
#define FEDNtupleReader_H

/** \class FEDNtupleReader
 *  No description available.
 *
 *  $Date: 2009/07/27 12:35:44 $
 *  $Revision: 1.3 $
 *  \author G. Cerminara - INFN Torino
 */

#include "TString.h"

#include <map>
#include <vector>


class TNtuple;
class TH1F;
class TH2F;

class FEDNtupleReader {
public:
  /// Constructor
  FEDNtupleReader(const TString& fileName, const TString& outputFile);

  /// Destructor
  virtual ~FEDNtupleReader();

  // Operations
  // nEventMax = -1 -> All
  void analyse(const int nEventMax = -1);

  
  void setDebug(int debug);
  

  
  TH1F *drawTH1F(const TString& name, const TString& formula, const TString& selection,
		 int nBins, float binMin, float binMax, const TString& option);

  TH2F *drawTH2F(const TString& name,
		 const TString& formulaX, const TString& formulaY, 
		 const TString& selection,
		 int nBinsX, float binMinX, float binMaxX,
		 int nBinsY, float binMinY, float binMaxY,
		 const TString& option);


  bool detToFEDRange(const TString& detName, TString& fedRange) const;

  void setMaxEvents(int maxEv) {
    maxEvents = maxEv;
  }


  void addTH1F(const TString& name, const TString& formula, const TString& selection,
			      int nBins, float binMin, float binMax, const TString& option);
  void addTH2F(const TString& name,
	       const TString& formulaX, const TString& formulaY, 
	       const TString& selection,
	       int nBinsX, float binMinX, float binMaxX,
	       int nBinsY, float binMinY, float binMaxY,
	       const TString& option);
  void runQueries(int maxEv, const TString& selection = "");
  
  TH1F *getTH1F(const TString& name);

  TH2F *getTH2F(const TString& name);

  TH1F *drawTH1F(const TString& name, const TString& option);

  TH2F *drawTH2F(const TString& name, const TString& option);

protected:


private:
  void begin();
  void processEvent(int entry);
  void end();
  void setBranchAddresses();


//   TString getNameFromDetId(const DTDetId& detId) const;
  
  TString theInFile;
  
  TString theOutFile;

  TNtuple *tree;


  
  int nevents;

  int maxEvents;
  int debug;

  TString theQuery;
  std::vector<int> theNFields;
  std::vector<int> theNFieldsX;  
  std::vector<TString> theOptions;
  std::vector<TH1F *> the1DHistos;
  std::vector<TH2F *> the2DHistos;
  std::vector<TString> theQueryName;
  std::map<TString, TH1F *> theHistoMap1D;
  std::map<TString, TH2F *> theHistoMap2D;


};

#endif

