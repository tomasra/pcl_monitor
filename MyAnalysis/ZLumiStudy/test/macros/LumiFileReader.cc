
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2011/08/27 12:45:55 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "LumiFileReader.h"
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <iostream>

using namespace std;

LumiFileReader::LumiFileReader(){}

LumiFileReader::~LumiFileReader(){}



// Operations
void LumiFileReader::readFile(const TString& fileName, int runMin, int runMax) {
  
  ifstream file(fileName.Data());
  string line;

  while (getline(file,line)) {
    if( line == "" || line[0] == '#' || line[0] == 'r'   ) continue; // Skip comments and empty lines
    stringstream linestr;
    linestr << line;
    int run = -1;
    int ls = -1;
    double delLumi = -1;
    double recLumi = -1;
    linestr >> run >> ls >> delLumi >> recLumi;
    if((runMin == -1 && runMax == -1 ) || (run >= runMin && run <= runMax)) {
      //cout << "run: " << run << " ls: " << " del lumi: " << delLumi << " rec lumi: " << recLumi << endl;
      theLumiMap[RunLumiIndex(run, ls)] = make_pair(delLumi, recLumi);
    }
  }

  cout << "File: " << fileName << " # of entries (run,ls) = " << theLumiMap.size() << endl;

}
  
double LumiFileReader::getDelLumi(const RunLumiIndex& runAndLumi) const {
  return getLumi(runAndLumi).first;
}

double LumiFileReader::getRecLumi(const RunLumiIndex& runAndLumi) const {
  return getLumi(runAndLumi).second;
}
  
double LumiFileReader::getAvgInstLumi(const RunLumiIndex& runAndLumi) const {
  return getDelLumi(runAndLumi)/23.;
}

  
double LumiFileReader::computeAvgInstLumi(double delLumi) const {
  return delLumi/23.;
}



double LumiFileReader::getDelIntegral(const RunLumiIndex& from, const RunLumiIndex& to) const {
  double sum = 0;
  for(map<RunLumiIndex, pair<double, double> >::const_iterator lumiInfo = theLumiMap.begin();
      lumiInfo != theLumiMap.end();
      ++lumiInfo) {
    if(from < (*lumiInfo).first && (*lumiInfo).first < to) {
      sum += (*lumiInfo).second.first;
    }
  }
  return sum;
}



double LumiFileReader::getRecIntegral(const RunLumiIndex& from, const RunLumiIndex& to) const {
  double sum = 0;
  for(map<RunLumiIndex, pair<double, double> >::const_iterator lumiInfo = theLumiMap.begin();
      lumiInfo != theLumiMap.end();
      ++lumiInfo) {
    if(from < (*lumiInfo).first && (*lumiInfo).first < to) {
      sum += (*lumiInfo).second.second;
    }
  }
  return sum;
}



pair<double, double> LumiFileReader::getRecIntegralInLumiBin(double instLumiMin, double instLumiMax) const {
  double sum = 0;
  
  double avgInstDelSum = 0;
  int couter = 0;
  
  for(map<RunLumiIndex, pair<double, double> >::const_iterator lumiInfo = theLumiMap.begin();
      lumiInfo != theLumiMap.end();
      ++lumiInfo) {
//     if((*lumiInfo).first.run() != 163817) continue; //FIXME
    if(computeAvgInstLumi((*lumiInfo).second.first) >= instLumiMin && computeAvgInstLumi((*lumiInfo).second.first) < instLumiMax) {
      
      sum += (*lumiInfo).second.second;
      avgInstDelSum += (*lumiInfo).second.first/23.;
      couter++;
    }
  }
  
  double meanAvgInstDel = avgInstDelSum/couter;
  return make_pair(sum, meanAvgInstDel);
}




pair<double, double> LumiFileReader::getLumi(const RunLumiIndex& runAndLumi) const {
  if(theLumiMap.find(runAndLumi) != theLumiMap.end()) {
    return (*(theLumiMap.find(runAndLumi))).second;
  } else {
    cout << "Warning: run:ls " << runAndLumi.run() << ":" << runAndLumi.lumiSection() << " not found!" << endl;
  }
  return make_pair(-1,-1);
}

  

