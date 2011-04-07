#ifndef HistoStack_H
#define HistoStack_H

/** \class HistoStack
 *  Code to create histogram stacks.
 *
 *  $Date: 2011/03/14 18:05:53 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - NEU Boston & INFN Torino
 */

#include <map>
#include <set>
#include <vector>
// #include <utility>

#include "Number.h"

#include "TString.h"



class LumiNormalization;
class THStack;
class TLegend;
class TH1F;
class TH1;
class TStyle;

class HistoStack {
public:
  /// Constructor
  HistoStack(const LumiNormalization* lumiNorm, const TString& finalState,
	     const TString& inputDir, const TString& filePrefix);

  /// Destructor
  virtual ~HistoStack();

  void defineGroup(const TString& name, const TString& legendLabel,
		   bool isData, bool isSignal,
		   Color_t fcolor, Style_t fstyle = 1001);


  // Operations
  // Add an histo to the stack.
  // The histo is filled on the fly and the correct weight is taken from the LumiNormalization object
  Number add(const TString& sampleName, const TString& varName,
	     int nBins, float binMin, float binMax, double integral = -1.);

  // Add a prefilled histos to the stack
  // NOTE: the histo is not further scaled: this is supposed to be already done!
  Number add(const TString& sampleName, const TString& varName, TH1F* histo);

  // Draw the given stack
  THStack * draw(const TString& histoName, const TString& option = "");

  // Set the mass cut for histos created on the fly
  void setMassCut(double min, double max);

  // Set the axis titles for a given stack
  void setAxisTitles(const TString& varName, const TString& xTitle, const TString& yUnits);

  // Set additional cuts
  void addCut(const TString& cut);
  
  // Set all the cut list at once (do not append but overwrite)
  void resetCut(const TString& cut);

  // Get the whole cut string (if filling histos from an ntuple)
  TString getCut() const;

  // Set the name of the ntuple to be used to when filling histos from an ntuple
  void setNtupleName(const TString& newName);

  // Set the name of the brach of weights to be multiplied to the global event weight
  // (useful for the study of pdf systematics)
  void addMultiplicativeWeight(const TString& weightName);

  // Draw all the variables in the map
  void drawAll(const TString& option = "");

  // get the histo stored for a particular variable and for a particular sample
  TH1F *getHisto(const TString& sampleName, const TString& varName);

  // set the rebinning option for each variable
  void setRebin(const TString& varName, int reb);


  // samples can be assigned to groups: the correspondig histos are added and plotted with the same
  // fill and the same label in the lagend
  void assignToGroup(const TString& sampleName, const TString& groupName);

  // se the order for the legend of samples or groups
  void setLegendOrder(int order, const TString& sampleName);

  // Se the y range of the stack
  void setYRange(const TString& varName, double yLow, double yHigh);

  // Add a label in the top right corner
  void setLabel(const TString& varName, const TString& label);

  void setFillColor(const TString& sampleName, int color);


protected:

private:
  TString getPitchString(TH1 *histo, int prec) const;
  void setStyle(TH1 *histo) const;

  // create the stack "on-demand" when it's needed and stores it in the map
  THStack * createStack(const TString& varName);
  void buildLegend(const TString& varName);

  // The pointer to the normalization tool
  const LumiNormalization* theLumiNorm;
  const TString theFinalState;
  const TString theInputDir;
  const TString theFilePrefix;
  // Map of colors to be used for each sample
  std::map<TString, int> colorMap;

  std::map<TString, int> fillStyleMap;


  // The map of the stack for each variable
  std::map<TString, THStack *> stackMap;
  // Map of the histos inserted in the stack per sample and per variable 
  std::map<TString, std::map<TString, TH1F *> >histMapPerSample;
  // The map of the data hist for each sample.
  // If the histo is present it is superimposed to the stack
  std::map<TString, TH1F *> dataHistMap;
  // Map of the sum of the histos for each variable: it is used to draw the MC error band
  std::map<TString, TH1F *> sumForErrMap;
  // Pointer to the legend (this is cloned for each stack actually drawn)
  TLegend *leg;
  std::set<TString> legSet;
  // Mass cut
  double massMin;
  double massMax;
  // Map of units and labels to be used for each variable
  std::map<TString, TString> xAxisTitle;
  std::map<TString, TString> yAxisUnit;
  std::map<TString, TString> yAxisTitle;
  // Associate a label for the legend to each sample name
  std::map<TString, TString> legLabel;
  // keep track of samples already inserted in the stack and therefore in the legend
  std::set<TString> alreadyInLeg; 
  // Map of numbers for the rebinning of particular variables
  std::map<TString, int> rebinMap; 

  // the order of the samples or groups to be displayed in the stack
  std::map<TString, std::vector<TString> > theSamplesInOrderPerVar;

  std::map<int, TString> samplesOrderInLegend;
  

  // map between sample name and group name
  std::map<TString, TString> groupMap;

  std::map<TString, std::pair<double, double> > rangeMap;

  std::map<TString, TString> labelMap;



  TString theSelection;
  TString ntupleName;
  TString weightBr;

  TStyle *theStyle;

};
#endif

