
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2008/03/13 17:45:22 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include <sys/types.h>
#include <dirent.h>
#include <errno.h>
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
//#include <set>
#include <iomanip>


#include "Number.h"
#include "CutTableBuilder.h"
#include "SampleGroup.h"
#include "TH1F.h"


using namespace std;


CutTableBuilder::CutTableBuilder() : printError(true) {
}


CutTableBuilder::~CutTableBuilder(){
  cout << "destructor" << endl;
}



void CutTableBuilder::addSampleGroup(const SampleGroup& group) {
  groupMap[group.name()] = group;
  vector<TString> samples = group.samples();
  for(vector<TString>::const_iterator sample = samples.begin();
      sample != samples.end(); ++sample) {
    sampleToGroupMap[*sample] = group.name();
  }
  groupNames.push_back(group.name());
}






void CutTableBuilder::addValue(const TString& cutName, const TString& sampleName, const Number& number) {
  TString groupName = sampleToGroupMap[sampleName];
  SampleGroup group = groupMap[groupName];
  perCutPerSampleMap[cutName][groupName] += number;
  perSamplePerCutMap[groupName][cutName] += number;

  if(!group.isData()) {
    perCutPerSampleMap[cutName]["totMC"] += number;
    perSamplePerCutMap["totMC"][cutName] += number;
    if(!group.isSignal()) {
      perCutPerSampleMap[cutName]["totMCBck"] += number;
      perSamplePerCutMap["totMCBck"][cutName] += number;
    }
  }
}



void CutTableBuilder::getValuesFromHisto(const TString& sampleName, const TH1F *histo) {
  // loop over all cuts which have been set
  for(vector<TString>::const_iterator cut = cuts.begin();
      cut != cuts.end(); ++cut) {
    int bin = cutBin[*cut];
    double nEvent = histo->GetBinContent(bin);
    double nEventError =  histo->GetBinError(bin);
    Number events(nEvent, nEventError);
    addValue(*cut, sampleName, events);
  }
}



void CutTableBuilder::setCut(const TString& name, const TString& latexLabel, const int bin) {
  cuts.push_back(name);
  labelCutName[name] = latexLabel;
  cutBin[name] = bin;
}




// Number CutTableBuilder::getValue(const TString& cutName, const TString& sampleName) const {
//   map<TString, TString>::const_iterator lookforgroup = sampleToGroupMap.find(sampleName);
//   if(lookforgroup != sampleToGroupMap.end()) {
//     map<TString, Number> cutValueMap = perSamplePerCutMap.find(lookforgroup->second)->second;
//     map<TString, Number>::const_iterator lookforcut = cutValueMap->find(cutName);
//     if(lookforcut != cutValueMap.end()) {
//       return lookforcut->second;
//     } else {
//       cout << "[CutTableBuilder]***Error: cut " << cutName << " not found!" << endl;
//     }
//   } else {
//     cout << "[CutTableBuilder]***Error: sample " << sampleName << " not found!" << endl;
//   }
//   return Number(-1,-1);
// }


void CutTableBuilder::printTableSampleVsCut() {
  printTitleSampleColumns();
  for(vector<TString>::const_iterator cut = cuts.begin();
      cut != cuts.end();
      ++cut) {
    printCutLine(*cut);
  }
}

void CutTableBuilder::printTableCutVsSample() {
  printTitleCutColumns();
  vector<TString> allgroups = groupNames;
  allgroups.push_back("totMC");
  allgroups.push_back("totMCBck");
  // loop over all groups and display the latex label
  for(vector<TString>::const_iterator groupname = allgroups.begin();
      groupname != allgroups.end();
      ++groupname) {
    printSampleLine(*groupname);
    
  }
  
}

void CutTableBuilder::printTitleCutColumns() {
  cout << " Sample ";
  // loop over all groups and display the latex label
  for(vector<TString>::const_iterator cut = cuts.begin();
      cut != cuts.end();
      ++cut) {
    cout << " & " <<  labelCutName[*cut];
  }
  cout << " \\\\" << endl;
}


void CutTableBuilder::printTitleSampleColumns() {
  cout << " Cut ";
  // loop over all groups and display the latex label
  for(vector<TString>::const_iterator groupname = groupNames.begin();
      groupname != groupNames.end();
      ++groupname) {
    cout << " & " <<  groupMap[*groupname].latexLabel();
  }
  cout << " & tot MC bck & tot MC \\\\" << endl;
}

void CutTableBuilder::printCutLine(const TString& cutName) {
  // set the precision
  int prec = cout.precision();
  cout.setf(ios::fixed);
  cout << setprecision(2);

  cout << labelCutName[cutName];
  std::map<TString, Number> valuesPerGroup = perCutPerSampleMap[cutName];
  vector<TString> allgroups = groupNames;
  allgroups.push_back("totMC");
  allgroups.push_back("totMCBck");

  // loop over all groups and display the number
  for(vector<TString>::const_iterator groupname = allgroups.begin();
      groupname != allgroups.end();
      ++groupname) {
    Number numevent = valuesPerGroup[*groupname];
    cout << " & $" <<  numevent.number();
    if(printError) cout << " \\pm " << numevent.error();
    cout << "$ ";
  }
  cout << " \\\\" << endl;
  
  // reset the precision
  cout << setprecision(prec);
}


void CutTableBuilder::printSampleLine(const TString& group) {
  // Get the numbers associated to this sample
  map<TString, Number> perCutNumber = perSamplePerCutMap[group];

  // Set the cout precision
  int prec = cout.precision();
  cout.setf(ios::fixed);
  cout  <<  setprecision(2);
  if(group == "totMC") {
    cout << "MC Tot.";
  } else if(group == "totMCBck") {
    cout << "MC Tot. Bck.";
  } else {
    cout << groupMap[group].latexLabel();
  }
  // Loop over the cuts
  for(vector<TString>::const_iterator cut = cuts.begin();
      cut != cuts.end(); ++cut) {
    cout << " & $" << perCutNumber[*cut].number();
    if(printError) {
      cout << " \\pm " << perCutNumber[*cut].error();
    }
    cout << "$ ";
  } 
  cout << " \\\\" << endl;
  cout << setprecision(prec);
}




void CutTableBuilder::setPrintError(bool set) {
  printError = set;
}
