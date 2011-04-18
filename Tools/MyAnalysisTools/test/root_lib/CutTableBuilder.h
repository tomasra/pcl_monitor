#ifndef CutTableBuilder_H
#define CutTableBuilder_H

/** \class CutTableBuilder
 *  No description available.
 *
 *  $Date: 2008/03/13 17:45:22 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include <vector>
#include <map>


#include "TString.h"

#include "Number.h"

class SampleGroup;
class TH1F;


class CutTableBuilder {
public:
  /// Constructor
  CutTableBuilder();

  void addSampleGroup(const SampleGroup& group);

  // add the value for a given sample to the total # of events of the group to which the sample belongs
  void addValue(const TString& cutName, const TString& sampleName, const Number& number);
  
  void getValuesFromHisto(const TString& sampleName, const TH1F *histo);

  // Add a cut to the list of cuts for which you want to build the table
  // The parameters are:
  //    - name which identify the cut in the code
  //    - label to be used in the latex
  //    - bin number in the cutFlow histo
  void setCut(const TString& name, const TString& latexLabel, const int bin);

//   // get the # of events per a given sample after a given cut
//   Number getValue(const TString& cutName, const TString& sampleName) const;

  // print a table with one row per cut
  void printTableSampleVsCut();
  // print a table with one row per sample
  void printTableCutVsSample();


  // print the title of the table with one column per sample
  void printTitleSampleColumns(); 
  // print the title of the table with one column per cut
  void printTitleCutColumns();   

  void printCutLine(const TString& cutName);
  void printSampleLine(const TString& group);

  void setPrintError(bool set);

  /// Destructor
  virtual ~CutTableBuilder();

  // Operations

protected:

private:


  std::map<TString, std::map<TString, Number> > perCutPerSampleMap;
  std::map<TString, std::map<TString, Number> > perSamplePerCutMap;

  std::map<TString, SampleGroup> groupMap;
  std::map<TString, TString> sampleToGroupMap;
  std::vector<TString> groupNames;

  std::map<TString, TString> labelCutName;
  std::map<TString, int> cutBin;
  std::vector<TString> cuts;

  bool printError;

};
#endif

