
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2012/07/31 16:14:20 $
 *  $Revision: 1.9 $
 *  \author G. Cerminara - INFN Torino
 */

#include "TFile.h"
#include "TTree.h"
#include "TMath.h"
#include "LumiFileReaderByBX.h"
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <iostream>
#include <math.h>

using namespace std;

static const unsigned int NBXMAX = 3650;

const float LENGTH_LS = pow(2., 18) / 11246;

template <typename A, typename B>
A lexical_cast(const B& b)
{
  std::stringstream sstr;
  sstr << b;
  A a;
  sstr >> a;
  return a;
}


LumiFileReaderByBX::LumiFileReaderByBX(const TString& dirBaseName) : theDirBaseName(dirBaseName), cachedRun(-1) {}

LumiFileReaderByBX::~LumiFileReaderByBX(){}

// read the file from disk unless it is already cached.
// If the root file is already available for the run than it is used 
// otherwise the root file is created
bool LumiFileReaderByBX::readFileForRun(const int run, bool shouldreadCSV /*=false*/) {
  if(run != cachedRun) {
    // clean the cache
    // theLumiByBXMap.clear();
    theLumiTable.clear();
    Long_t runN = run;

    // put together the file name
    TString fileName = theDirBaseName + runN + TString(".csvt");

    cout << "--- read a new file for run: " << runN << endl;


    TString rootFileName = theDirBaseName + runN +  TString(".root");
    // read the file
    if (shouldreadCSV || !readRootFile(rootFileName,run, run+1)) {
      readCSVFileNew(fileName, run, run+1);
      //readCSVFile(fileName, run, run+1);
      convertToRootFile();
    }

    // add to the bins and total integrals
    //FIXME: ???

    // reassing the last cached run
    cachedRun = run;

    return true;
  }
  return false;

}


bool LumiFileReaderByBX::checkCache(int run) const {
  if(run != cachedRun)
        return true;

  return false;
    
}

bool LumiFileReaderByBX::check_RunFound(int run) const {
  map<int, vector< vector<float> > >::const_iterator lsContainer = theLumiTable.find(run);
  if (lsContainer == theLumiTable.end()) { // run does not exist
    return false;
  }
  
    return true;
}

bool LumiFileReaderByBX::check_LSFound(const RunLumiIndex& runAndLumi) const {
  map<int, vector< vector<float> > >::const_iterator lsContainer = theLumiTable.find(runAndLumi.run());

  if (!check_RunFound(runAndLumi.run())) return false;

  const vector< vector<float> >& run = lsContainer->second;
  const vector<float>& lumiSection = run[runAndLumi.lumiSection() - 1];

  if (runAndLumi.lumiSection() > (int)run.size() || runAndLumi.lumiSection() <= 0 || (int)lumiSection.size() == 0) { // run does not contain this LS
    return false;
  }

  return true;
}

bool LumiFileReaderByBX::check_BXFilled(const RunLumiBXIndex& runAndLumiAndBX) const {
  map<int, vector< vector<float> > >::const_iterator lsContainer = theLumiTable.find(runAndLumiAndBX.run());

  if (!check_RunFound(runAndLumiAndBX.run()) || !check_LSFound(RunLumiIndex(runAndLumiAndBX.run(), runAndLumiAndBX.lumiSection()))) return false;

  const vector< vector<float> >& run = lsContainer->second;

  const vector<float>& lumiSection = run[runAndLumiAndBX.lumiSection() - 1];
  if (runAndLumiAndBX.bx() >= (int)lumiSection.size() || (int)lumiSection.size() == 0) { // the vector of lumis by BX is not filled
    return false;
  }

  return true;
}


// Operations
void LumiFileReaderByBX::readCSVFileNew(const TString& fileName, int runMin, int runMax) {
  cout << "txt file: " << fileName << endl;

  bool debug = false;

  // open the txt file for a given run
  ifstream file(fileName.Data());
  int theRun = -1;


  // container of vector of lumis by BX for each LS
  vector< vector<float> > lsContainer;
  vector<float> lsRatioContainer;

  vector< std::pair<float,float> > lsTotalLumiContainer;

  getFillingScheme(runMin);

  cout << "##Begin readCSVFileNew\n";

  // loop over lines: each line corresponds to a LS
  int nLines = 0;
  string line;
  while (getline(file,line)) { // loop over lines
    if( line == "" || line[0] == '#' || line[0] == 'r'   ) continue; // Skip comments and empty lines


    if(debug) {
      cout << line << endl;
    }

    // count the # of lines
    nLines ++;
    
    stringstream linestr;
    linestr << line;

    // now read the content of the line: each field is separated by a comma and the
    // position determines its meaning
    int run = -1;
    int ls = -1;
    float delLumi = -1;
    float recLumi = -1;
    int bx = -1;
    float bxDelLumi = -1.;
    float bxRecLumi = -1.;
    float ratioRecDel = 1.;
    float sumBxDel = 0;
    float sumBxRec = 0;
    

    // cells are storing the various values and are separeted by commas
    string cell;
    int cellCounter = 0;

    // vector of lumis values by BX
    // element 0 stores the ratio del/rec the other store the recorded value for each BX
    vector<float> lumiByBx(NBXMAX);
    pair<float, float> totalLumi;    

    while(getline(linestr, cell, ',')) { // loop over cells
      stringstream cellstream;
      cellstream << cell;

      if(cellCounter == 0) { // this is the "run" field

	cellstream >> run;

	if(debug) {
	  cout << "---------------------------------------------------" << endl;
	  cout << "run: " << run << endl;
	}
	if(!(runMin == -1 && runMax == -1 ) && !(run >= runMin && run <= runMax)) {
	  return;
	}

	theRun = run; 

      } 

      else if(cellCounter == 1) { // LS field
	cellstream >> ls;
	if(debug) {
	  cout << "---------" << endl;
	  cout << "ls: " << ls << endl;
	}


	// FIXME: there are many 0 in LumiCal2 files...
	if(ls == 0) {
	  cout << "ERROR: lumi 0 found, skipping" << endl;
	  break;
	}
	
      }

      else if(cellCounter == 2) { // this is the date, we skip it for the moment
	// do nothing
      } 

      else if(cellCounter == 3) { // delivered lumi in this LS
	cellstream >> delLumi;
        totalLumi.first = delLumi;
      }

      else if(cellCounter == 4) { // recorded lumi in this LS
	cellstream >> recLumi;
        totalLumi.second = recLumi;

	// ratio of del/rec -> this is used to scale all the BX lumis
	if(delLumi != 0) ratioRecDel = recLumi/delLumi;
	else {
	  ratioRecDel = 0; // FIXME: check that this is the right choice
	  cout << "Warning: run " << run << " ls " << ls << " has delLumi " << delLumi << " and recLumi " << recLumi << endl;
	}
      }

      else if(cellCounter % 2 == 1) { // odd -> del lumi in this BX
	cellstream >> bx;

      }

      else if(cellCounter % 2 == 0) { // even -> BX #
	cellstream >> bxDelLumi;
	bxRecLumi = ratioRecDel*bxDelLumi;

	// sum over all the BX in the LS
	sumBxDel += bxDelLumi;
	sumBxRec += bxRecLumi;
	if(debug) cout << "BX: " << bx << " del lumi: " << bxDelLumi << " rec lumi: " << bxRecLumi << endl;
	lumiByBx[bx] = bxRecLumi;

      }

      cellCounter++;
    }


    if(ls == 0) {
      cout << "skipping LS 0" << endl;
      continue;
    }
    // now push back the vector with the BX lumis in the LS container
    int lastLumi = lsContainer.size();
    if(debug) cout << "last analyzed LS was: " << lastLumi << " now adding: " << ls << endl;

    // we fill also missing LSs with an empty vector
    for(int nMiss = lastLumi + 1; nMiss <= ls; ++nMiss) {
      if(debug) cout << "  add  empty LS: " << nMiss << endl;
      vector<float> empty;
      lsContainer.push_back(empty);
      lsRatioContainer.push_back(-1);
      lsTotalLumiContainer.push_back(make_pair(-1.f,-1.f));
    }

    // sanity check: compare the sum of the BXs with the integral in the lumi
    // FIXME: is the integral taking into account ONLY the colliding BXs?? (check!)
    // FIXME: lowering the threshold to 1% reveals many more problems: investigate

    if(fabs(sumBxRec*LENGTH_LS - recLumi)/recLumi > 0.05) {
       if(debug) cout << "WARNING: ls: " << ls
	   << " sum BX del: " << sumBxDel *LENGTH_LS<< " sumBxRec: " << sumBxRec*LENGTH_LS
	   << " total del: " << delLumi << " total rec: " << recLumi << endl;
      // in this case we SKIP the LS so that it won'tbe used for the computation of the 
    } //else {
      if(debug)  cout << "add filled LS: " << ls << " new size: " << lsContainer.size() << endl;
      lsContainer[ls - 1] = lumiByBx;
      lsRatioContainer[ls - 1] = ratioRecDel;
      lsTotalLumiContainer[ls - 1] = totalLumi;
    //}

  }
  
  cout << "##filling theRun=" << theRun << "\n";

  theLumiTable[theRun] = lsContainer;
  theLumiRatioByRunByLS[theRun] = lsRatioContainer;
  theTotalLumiByRun[theRun] = lsTotalLumiContainer;
  cout << "    run: " << theRun << " # ls: " << lsContainer.size() << endl;

}

void LumiFileReaderByBX::getFillingScheme(int run) {
  TString fileName = theDirBaseName + TString("/filling_schemes/") + Long_t(run) + TString(".txt");

  ifstream inf(fileName.Data());
  if (!inf.good()) {
    createFillingSchemeFile(run, fileName.Data());

    inf.open(fileName);
    if (!inf.good()) {
      cout << "WARNING: Failed to create filling scheme file: " << fileName.Data() << "\n";
      return;
    }
  }

  string line;
  int trueCount = 0;
  while (getline(inf, line)) {
    bool value = lexical_cast<bool>(line);
    theFillingScheme.push_back(value);  // starts with bx 1, so use : theFillingScheme[a-1] for bx=a
    //cout << value << " : " << theFillingScheme.size() - 1 << endl;
    if (theFillingScheme.back())
      trueCount++;
  }
  cout << "Got " << theFillingScheme.size() << " defined bx, " << trueCount << " active\n";
  while (theFillingScheme.size() < NBXMAX)
    theFillingScheme.push_back(false);
}

void LumiFileReaderByBX::createFillingSchemeFile(int run, const std::string& fileName) {
  const char *base = getenv("CMSSW_BASE");
  string execPath = "FillingScheme/";
  if (base) {
    execPath = base;
    execPath += "/src/MyAnalysis/ZLumiStudy/test/FillingScheme/";
  }
  execPath += "get_filling_scheme.py";

  string cmd = execPath + " " + lexical_cast<string>(run) + " " + fileName;
  cout << cmd << endl;
  system(cmd.c_str());
}

int LumiFileReaderByBX::getNumberLSs(const int run) const {
  if (!check_RunFound(run))
    return -1;

  map<int, vector< vector<float> > >::const_iterator lsContainer = theLumiTable.find(run);

  return (int)lsContainer->second.size();
}

int LumiFileReaderByBX::getNumberBX(const int run, const int ls) const {
  if (!check_RunFound(run) || !check_LSFound(RunLumiIndex(run, ls)))
    return -1;

  map<int, vector<vector<float> > >::const_iterator lsContainer = theLumiTable.find(run);
  vector< vector<float> > runContainer = lsContainer->second;
 
  int nBX = 0;
  for (int bx = 0; bx < (int)runContainer[ls-1].size(); bx++) {
    if (runContainer[ls-1][bx] != 0) {
      nBX++;
    }
  }

  return nBX;
}




bool LumiFileReaderByBX::readRootFile(const TString& fileName, int /*runMin*/, int /*runMax*/) {

  TFile *file = new TFile(fileName.Data());

  if(file->IsZombie()) return false;


  cout << "  ROOT file: " << fileName << endl;

  TTree *tree = (TTree*) file->Get("lsTree");
  

  int run = -1;
  int ls = -1;
  float ratio = -1;
  float bxLumiValues[NBXMAX] = {0};
  float totalDel = -1.f;
  float totalRec = -1.f;

  Bool_t activeBx[NBXMAX] = {0};

  tree->SetBranchAddress("run", &run);
  tree->SetBranchAddress("ls", &ls);
  tree->SetBranchAddress("ratio", &ratio);
  tree->SetBranchAddress("bxValues", bxLumiValues);
  tree->SetBranchAddress("activeBx", activeBx);
  tree->SetBranchAddress("totalDel", &totalDel);
  tree->SetBranchAddress("totalRec", &totalRec);

  vector< vector<float> > lsContainer(tree->GetEntries());
  vector<float> lsRatioContainer(tree->GetEntries());
  vector< pair<float,float> > lsTotalLumiContainer(tree->GetEntries());

  for(int entry = 0; entry != tree->GetEntries(); ++entry) {
    tree->GetEntry(entry);
    //cout << "Ratio after GetEntry: " << ratio << endl;
    if(ratio != -1 && ratio != 0 && !TMath::IsNaN(ratio)) {
      vector<float> lumiByBx(bxLumiValues,bxLumiValues+NBXMAX );
      lsContainer[ls -1] = lumiByBx;
    } else {
      if (check_RunFound(run) && check_LSFound(RunLumiIndex(run, ls))) {
      cout << "run: " << run << " ls " << ls << " ratio " << ratio << " has a wrong value" << endl;
      }
      vector<float> lumiByBx;
      lsContainer[ls -1 ]  = lumiByBx ;
    }

    lsTotalLumiContainer[ls - 1] = make_pair(totalDel, totalRec);
    lsRatioContainer[ls - 1] = ratio;
  }

  theFillingScheme.clear();
  int trueCount = 0;
  for (size_t i=0; i < NBXMAX; ++i) {
    theFillingScheme.push_back(activeBx[i]);
    if (activeBx[i])
      trueCount++;
    //cout << "Got: " << (theFillingScheme.back() ? "true" : "false") << endl;
  }
  cout << "Got " << trueCount << " active bx\n";

  //cout << "Ratio in ReadRootFile: " << ratio << " --- ls: " << ls << endl;

  cout << "   run: " << run << " # ls: " << lsContainer.size() << endl;
  theLumiTable[run] = lsContainer;
  theLumiRatioByRunByLS[run] = lsRatioContainer;
  theTotalLumiByRun[run] = lsTotalLumiContainer;
  file->Close();
  return true;
}


  
float LumiFileReaderByBX::getDelLumi(const RunLumiIndex& runAndLumi) const {
   return getLumi(runAndLumi).first*LENGTH_LS;
 }

float LumiFileReaderByBX::getRecLumi(const RunLumiIndex& runAndLumi) const {
   return getLumi(runAndLumi).second*LENGTH_LS;
 }
  
float LumiFileReaderByBX::getAvgInstLumi(const RunLumiIndex& runAndLumi) const {
   return getLumi(runAndLumi).first;
 }

  
float LumiFileReaderByBX::computeAvgInstLumi(float delLumi) const {
  return delLumi/LENGTH_LS;
}




// pair<float, float> LumiFileReaderByBX::getRecIntegralInLumiBin(float instLumiMin, float instLumiMax) const {
//   float sum = 0;
  
//   float avgInstDelSum = 0;
//   int couter = 0;
  
//   for(map<RunLumiIndex, pair<float, float> >::const_iterator lumiInfo = theLumiMap.begin();
//       lumiInfo != theLumiMap.end();
//       ++lumiInfo) {
// //     if((*lumiInfo).first.run() != 163817) continue; //FIXME
//     if(computeAvgInstLumi((*lumiInfo).second.first) >= instLumiMin && computeAvgInstLumi((*lumiInfo).second.first) < instLumiMax) {
      
//       sum += (*lumiInfo).second.second;
//       avgInstDelSum += (*lumiInfo).second.first/LENGTH_LS;
//       couter++;
//     }
//   }
  
//   float meanAvgInstDel = avgInstDelSum/couter;
//   return make_pair(sum, meanAvgInstDel);
// }


  
float LumiFileReaderByBX::getDelLumi(const RunLumiBXIndex& runAndLumiAndBx) const {
  return getLumi(runAndLumiAndBx).first*LENGTH_LS;
}

float LumiFileReaderByBX::getRecLumi(const RunLumiBXIndex& runAndLumiAndBx) const {
  return getLumi(runAndLumiAndBx).second*LENGTH_LS;
}
 
float LumiFileReaderByBX::getAvgInstLumi(const RunLumiBXIndex& runAndLumiAndBx) const { // ?
  return getLumi(runAndLumiAndBx).first;
}



pair<float, float> LumiFileReaderByBX::getLumi(const RunLumiBXIndex& runAndLumiAndBx) const {
  if (!check_RunFound(runAndLumiAndBx.run()) || !check_LSFound(RunLumiIndex(runAndLumiAndBx.run(), runAndLumiAndBx.lumiSection())) || !check_BXFilled(runAndLumiAndBx)) 
    return make_pair(-1.f, -1.f);

  map<int, vector< vector<float> > >::const_iterator lsContainer = theLumiTable.find(runAndLumiAndBx.run());
  map<int, vector<float> >::const_iterator lsRatioContainer = theLumiRatioByRunByLS.find(runAndLumiAndBx.run());
  const vector< vector<float> >& run = (*lsContainer).second;
  const vector<float>& lumiSection = run[runAndLumiAndBx.lumiSection() - 1];

  if (lsRatioContainer == theLumiRatioByRunByLS.end()) {
      cout << "Warning ratio: run " << runAndLumiAndBx.run() << " does not exists" << endl;
    return make_pair(-1.f, -1.f);
  }


  if (runAndLumiAndBx.lumiSection() > (int)(*lsRatioContainer).second.size() || (int)(*lsRatioContainer).second.size() == 0) { // the vector of ratios by LS is not filled
    cout << "Warning ratio: the vector of ratios by LS " << runAndLumiAndBx.lumiSection() << " is not filled" << endl;
  }

  float ratio = (*lsRatioContainer).second[runAndLumiAndBx.lumiSection() - 1];
  if (ratio == 0 || ratio == -1) {
    cout << "Warning: run " << runAndLumiAndBx.run() << " LS " << runAndLumiAndBx.lumiSection() << " invalid del/rec ratio: " << ratio << endl;
    return make_pair(-1.f, -1.f);
  }

  float recLumi = lumiSection[runAndLumiAndBx.bx()];
  float delLumi = recLumi/ratio; 
  return make_pair(delLumi, recLumi);
}

pair<float, float> LumiFileReaderByBX::getLumi(const RunLumiIndex& runAndLumi) const {
  if (!check_RunFound(runAndLumi.run()) || !check_LSFound(runAndLumi))
    return make_pair(-1.f, -1.f);

  map<int, vector< vector<float> > >::const_iterator lsContainer = theLumiTable.find(runAndLumi.run());
  map<int, vector<float> >::const_iterator lsRatioContainer = theLumiRatioByRunByLS.find(runAndLumi.run());
  const vector< vector<float> >& run = (*lsContainer).second;
  const vector<float>& lumiSection = run[runAndLumi.lumiSection() - 1];

  int nBX = getNumberBX(runAndLumi.run(), runAndLumi.lumiSection());
  if (nBX >= (int)lumiSection.size() || (int)lumiSection.size() == 0) { // the vector of lumis by BX is not filled
    cout << "Warning: run " << runAndLumi.run() << " LS " << runAndLumi.lumiSection()
   << ": the vector of lumis by BX is not filled" << endl;
    return make_pair(-1.f, -1.f);
  }

  if (lsRatioContainer == theLumiRatioByRunByLS.end()) {
      cout << "Warning ratio: run " << runAndLumi.run() << " does not exists" << endl;
    return make_pair(-1.f, -1.f);
  }

  if (runAndLumi.lumiSection() > (int)(*lsRatioContainer).second.size() || (int)(*lsRatioContainer).second.size() == 0) { // the vector of ratios by LS is not filled
    cout << "Warning ratio: the vector of ratios by LS " << runAndLumi.lumiSection() << " is not filled" << endl;
  }

  float ratio = (*lsRatioContainer).second[runAndLumi.lumiSection() - 1];
  if (ratio == 0 || ratio == -1) {
    cout << "Warning: run " << runAndLumi.run() << " LS " << runAndLumi.lumiSection() << " invalid del/rec ratio: " << ratio << endl;
    return make_pair(-1.f, -1.f);
  }

  // runAndLumiAndBX start mit 0 und end mit #bx
  RunLumiBXIndex start = RunLumiBXIndex(runAndLumi.run(), runAndLumi.lumiSection(), 0);
  RunLumiBXIndex end = RunLumiBXIndex(runAndLumi.run(), runAndLumi.lumiSection(), nBX);

  float recLumi = getRecIntegral(start, end);
  float delLumi = recLumi/ratio;

  return make_pair(delLumi, recLumi);
}


pair<float, float> LumiFileReaderByBX::getTotalLumi(const RunLumiIndex& runAndLumi) const {
  map<int, vector< pair<float, float> > >::const_iterator lsTotalLumiContainer = theTotalLumiByRun.find(runAndLumi.run());
  if (lsTotalLumiContainer == theTotalLumiByRun.end()) {
    cout << "Error: Run " << runAndLumi.run() << " not found for getTotalLumi" << endl;
    return make_pair(-1.f, -1.f);
  }

  const vector< pair<float, float> >& totalLumiContainer = lsTotalLumiContainer->second;
  if (runAndLumi.lumiSection() == 0 || runAndLumi.lumiSection() > (int)totalLumiContainer.size()) {
    cout << "Error: Lumi section " << runAndLumi.lumiSection() << " not found for getTotalLumi" << endl;
    return make_pair(-1.f, -1.f);
  }

  return totalLumiContainer[runAndLumi.lumiSection() - 1];
}

float LumiFileReaderByBX::getDelIntegral(const RunLumiBXIndex& from, const RunLumiBXIndex& to) const {
  
  float sum = 0;

  sum = getRecIntegral(from, to);
  if (sum == -1) {
    cout << "problem in calculation: getRecIntegral" << endl;
    return -1;
  }

  map<int, vector<float> >::const_iterator lsRatioContainer = theLumiRatioByRunByLS.find(from.run());

  if (lsRatioContainer == theLumiRatioByRunByLS.end()) {
      cout << "Warning ratio: run " << from.run() << " does not exists" << endl;
    return -1;
  }

  float ratio = (*lsRatioContainer).second[from.lumiSection() - 1];
  if (ratio == 0 || ratio == -1) {
    cout << "Warning: run " << from.run() << " LS " << from.lumiSection() << " invalid del/rec ratio: " << ratio << endl;
    return -1;
  } 

  sum /= ratio; 
  return sum;
}


float LumiFileReaderByBX::getDelIntegral(const RunLumiIndex& from) const {
  float sum = 0;
  
  int nBX = getNumberBX(from.run(), from.lumiSection());
  RunLumiBXIndex start = RunLumiBXIndex(from.run(), from.lumiSection(), 0);
  RunLumiBXIndex end = RunLumiBXIndex(from.run(), from.lumiSection(), nBX);
  sum = getDelIntegral(start, end);
  return sum;
}



float LumiFileReaderByBX::getRecIntegral(const RunLumiBXIndex& from, const RunLumiBXIndex& to) const {

  float sum = 0;
  
  if (from.run() != to.run()) {
    cout << "different run chosen" << endl;
    return -1;
  } 
  if (from.lumiSection() != to.lumiSection()) {
    cout << "different ls chosen " << from.lumiSection() << " : " << to.lumiSection() << endl;
    return -1;
  }

  int runNumber = from.run();
  int ls = from.lumiSection();

  map<int, vector< vector<float> > >::const_iterator lsContainer = theLumiTable.find(runNumber);
    if (lsContainer == theLumiTable.end()) { // run does not exist
      cout << "Warning: run " << runNumber << " does not exists" << endl;
      return -1;
    }

    const vector< vector<float> >& run = lsContainer->second;
    if (ls > (int)run.size() || ls <= 0) { // run does not contain this LS
      cout << "Warning: run " << runNumber << " does not contain LS " << ls << endl;
      return -1;
    }

    const vector<float>& lumiSection = run[ls - 1];

    for (int bx = from.bx(); bx <= to.bx(); bx++) {
      if (bx >= (int)lumiSection.size() || (int)lumiSection.size() == 0) { // the vector of lumis by BX is not filled
        cout << "Warning: run " << runNumber << " LS " << ls  << ": the vector of lumis by BX is not filled" << endl;
      return -1;
      }

      //cout << bx << " : " << lumiSection[bx];
      if (bx == 0) { // no information for bx == 0, so don't use it
        //cout << endl;
      }
      else if (theFillingScheme[bx-1]) { // start with bx 1
        sum += lumiSection[bx];
        //cout << " = " << sum << endl;
      }
      else {
        //cout << endl;
      }
    }
 
  return sum * LENGTH_LS;
}

float LumiFileReaderByBX::getRecIntegral(const RunLumiIndex& from) const {
  float sum = 0;

  int nBX = getNumberBX(from.run(), from.lumiSection());
  RunLumiBXIndex start = RunLumiBXIndex(from.run(), from.lumiSection(), 0);
  RunLumiBXIndex end = RunLumiBXIndex(from.run(), from.lumiSection(), nBX);
  sum = getRecIntegral(start, end);
  return sum;
} 



// pair<float, float> LumiFileReaderByBX::getRecIntegralInLumiBin(float instLumiMin, float instLumiMax) const {
//   float sum = 0;
  
//   float avgInstDelSum = 0;
//   int couter = 0;
  
//   for(map<RunLumiBXIndex, pair<float, float> >::const_iterator lumiInfo = theLumiByBXMap.begin();
//       lumiInfo != theLumiByBXMap.end();
//       ++lumiInfo) {
// //     if((*lumiInfo).first.run() != 163817) continue; //FIXME
//     if(computeAvgInstLumi((*lumiInfo).second.first) >= instLumiMin && computeAvgInstLumi((*lumiInfo).second.first) < instLumiMax) {
      
//       sum += (*lumiInfo).second.second;
//       avgInstDelSum += (*lumiInfo).second.first/LENGTH_LS;
//       couter++;
//     }
//   }
  
//   float meanAvgInstDel = avgInstDelSum/couter;
//   return make_pair(sum, meanAvgInstDel);
// }

TH1F * LumiFileReaderByBX::getRecLumiBins(int nbins, float min, float max) const {
  cout << "Fill the integrated lumi for run " << cachedRun << endl;
  //cout << "     # bins: " << nbins << " min: " << min << " max: " << max << endl;
  Long_t runN = cachedRun;
  TString hName = TString("hRec_") + runN;
  TH1F *histo = new TH1F(hName.Data(), "test", nbins, min, max);
  
//   // old format: here for compatibility...
//   // FIXME: remove
//   for(map<RunLumiBXIndex, pair<float, float> >::const_iterator lumiInfo = theLumiByBXMap.begin();
//       lumiInfo != theLumiByBXMap.end();
//       ++lumiInfo) {
//     //    cout << "BX: "  << lumiInfo->first.bx() << " del: " << (*lumiInfo).second.first << " rec: " << (*lumiInfo).second.second << endl;
//     //     cout << (*lumiInfo).second.second << endl;
//     histo->Fill((*lumiInfo).second.first, (*lumiInfo).second.second*LENGTH_LS);
//   }
  
  // new format
  for(map<int, vector< vector<float> > >::const_iterator run = theLumiTable.begin();
      run != theLumiTable.end(); ++run) {
    vector< vector<float> > lsContainer = (*run).second;
    vector<float> ratioContainer = (*theLumiRatioByRunByLS.find((*run).first)).second;

    for(vector< vector<float> >::const_iterator bxValues =  lsContainer.begin();
	bxValues != lsContainer.end(); ++bxValues) {
      int ls = bxValues - lsContainer.begin() + 1;

      vector<float> values = (*bxValues);
      if(values.size() != 0) {

	float ratio = ratioContainer[ls-1];

	for(unsigned int index = 0; index != values.size(); ++index) {
	  float recLumi = values[index];
	  float delLumi = 0;
	  if(ratio != 0) {
	    delLumi = recLumi/ratio;
	  } else {
	    cout << "Warning ls : BX : " << ls << ": " << index << " del: " << delLumi << " rec: " << recLumi << endl;
	  }
	  //cout << "BX: " << index << " del: " << delLumi << " rec: " << recLumi << endl;
    if (index == 0) { // no information for bx == 0, so don't use it
        //cout << endl;
      }
      else if (theFillingScheme[index-1]) { // start with bx 1
        histo->Fill(delLumi, recLumi*LENGTH_LS);
        //cout << " = " << sum << endl;
      }
      else {
        //cout << endl;
      }

	    // del Lumi per BX, weight with rec Lumi
	}
      }
    }
  }

  return histo;
  
}



void LumiFileReaderByBX::convertToRootFile() const {

  cout << "start converting" << endl;

   for(map<int, vector< vector<float> > >::const_iterator run = theLumiTable.begin();
       run != theLumiTable.end(); ++run) { // loop over runs

     stringstream str;
     str << theDirBaseName << (*run).first << ".root";
     TString fileName;
     str >> fileName;
     cout << "converting the lumi table to ROOT file: " << fileName << endl;

     TFile rootFile(fileName.Data(),"recreate");
     rootFile.cd();
     TTree *tree = new TTree("lsTree","The tree");

     // TODO:
     // Write run number (?) and activeBx array (TArrayC) directly in the
     // root file and not in the tree.
     
     int runn = (*run).first;
     int ls = -1;
     float bxLumiValues[NBXMAX] = {0};
     float ratio = -1;
     float totalRec = -1.f;
     float totalDel = -1.f;
     Bool_t activeBx[NBXMAX] = {0};
     
     tree->Branch("run", &runn,"run/I"); 
     tree->Branch("ls", &ls,"ls/I"); 
     tree->Branch("bxValues", bxLumiValues,"bxValues[3650]/F");
     tree->Branch("activeBx", activeBx, "activeBx[3650]/O");
     tree->Branch("ratio", &ratio,"ratio/F");
     tree->Branch("totalRec", &totalRec, "totalRec/F");
     tree->Branch("totalDel", &totalDel, "totalDel/F");

     for (size_t i=0; i < NBXMAX; ++i) {
       activeBx[i] = theFillingScheme[i];
     }
     

    vector< vector<float> > lsContainer = (*run).second;
    map<int, vector<float> >::const_iterator lumiRatioByLS = theLumiRatioByRunByLS.find((*run).first);
    const vector< pair<float,float> >& totalLumiContainer = theTotalLumiByRun.find(runn)->second;

    vector<float> ratioContainer = lumiRatioByLS->second;

    for(vector< vector<float> >::const_iterator bxValues = lsContainer.begin(); bxValues != lsContainer.end(); ++bxValues) { // loop over LSs
      ls = bxValues - lsContainer.begin() + 1;
      ratio = ratioContainer[ls -1];
      pair<float,float> totalLumi = totalLumiContainer[ls - 1];
      totalDel = totalLumi.first;
      totalRec = totalLumi.second;

      vector<float> values = (*bxValues);
      //        cout << values.size() << endl;
      if(values.size() != 0) {
        for(unsigned int index = 0; index != values.size(); ++index) {
          float recLumi = values[index];
          //	   float delLumi = recLumi/ratio;
          bxLumiValues[index] = recLumi;
          //cout << "BX: " << index << " del: " << delLumi << " rec: " << recLumi << endl;
          //	   histo->Fill(delLumi, recLumi*LENGTH_LS);
        }
        // FIXME: should become a variable size array
        for(unsigned index = values.size(); index != NBXMAX; ++index) {
          bxLumiValues[index] = 0;
        }
      }

      tree->Fill();
    }
  tree->Write();
  rootFile.Close();
}
   

   cout << "converting ready" << endl;

}

// // Operations
// void LumiFileReaderByBX::readCSVFile(const TString& fileName, int runMin, int runMax) {

//   cout << "    txt file: " << fileName << endl;

//   ifstream file(fileName.Data());
//   string line;

//   int nLines = 0;

//   while (getline(file,line)) {
//     if( line == "" || line[0] == '#' || line[0] == 'r'   ) continue; // Skip comments and empty lines
//     //cout << line << endl;
//     nLines ++;
    
//     stringstream linestr;
//     linestr << line;

//     int run = -1;
//     int ls = -1;
//     float delLumi = -1;
//     float recLumi = -1;
//     int bx = -1;
//     float bxDelLumi = -1.;
//     float bxRecLumi = -1.;

//     string cell;
//     int cellCounter = 0;
//     float ratioRecDel = 1.;

//     float sumBxDel = 0;
//     float sumBxRec = 0;


//     while(getline(linestr, cell, ',')) {
//       stringstream cellstream;
//       cellstream << cell;
//       if(cellCounter == 0) {
//  cellstream >> run;
// //   cout << "---------------------------------------------------" << endl;
// //   cout << "run: " << run << endl;
//  if(!(runMin == -1 && runMax == -1 ) && !(run >= runMin && run <= runMax)) return;

//       } else if(cellCounter == 1) {
//  cellstream >> ls;
// //   cout << "---------" << endl;
// //   cout << "ls: " << ls << endl;
  
//       }  else if(cellCounter == 2) {
//  cellstream >> delLumi;
//       } else if(cellCounter == 3) {
//  cellstream >> recLumi;
//  ratioRecDel = recLumi/delLumi;
//       } else if(cellCounter % 2 == 0) { // if pari
//  cellstream >> bx;
//       } else if(cellCounter % 2 == 1) { // if dispari
//  cellstream >> bxDelLumi;
//  sumBxDel += bxDelLumi;
//  bxRecLumi = ratioRecDel*bxDelLumi;
//  sumBxRec += bxRecLumi;
// //   cout << "BX: " << bx << " del luvi: " << bxDelLumi << " rec lumi: " << bxRecLumi << endl;
//  theLumiByBXMap[RunLumiBXIndex(run, ls, bx)] = make_pair(bxDelLumi, bxRecLumi);

//       }

//       cellCounter++;
      
//     }
//     if(fabs(sumBxRec*LENGTH_LS - recLumi)/recLumi > 0.05) {
      
//       cout << "WARNING: ls: " << ls
//     << " sum BX del: " << sumBxDel*LENGTH_LS << " sumBxRec: " << sumBxRec*LENGTH_LS
//     << " total del: " << delLumi << " total rec: " << recLumi << endl;
//     }
//   }

//   // cout << "# lines in the file: " << nLines << endl;
//   cout << "File: " << fileName << " # of entries (run,ls) = " << theLumiByBXMap.size() << endl;
  

// }



//pair<float, float> LumiFileReaderByBX::getLumi(const RunLumiBXIndex& runAndLumiAndBx) const {
////   // check which table was filled
////   if(theLumiByBXMap.find(runAndLumiAndBx) != theLumiByBXMap.end()) {
////     return (*(theLumiByBXMap.find(runAndLumiAndBx))).second;
////   } 
//
//  // get the vector of LSs for this run
//  map<int, vector< vector<float> > >::const_iterator lsContainer =
//    theLumiTable.find(runAndLumiAndBx.run());
//
//  // check if the run is actually found
//  if(lsContainer != theLumiTable.end()) { // run exists
//    
//    if((*lsContainer).second.size() >= runAndLumiAndBx.lumiSection()) { // run contains this LS
//      //cout << "r: " << runAndLumiAndBx.run() << " ls: " << runAndLumiAndBx.lumiSection() << " bx: " << runAndLumiAndBx.bx() << endl;
//      
//      //cout << " # BX: " << (*lsContainer).second[runAndLumiAndBx.lumiSection() - 1].size() << endl;
//      if((*lsContainer).second[runAndLumiAndBx.lumiSection() - 1].size() != 0) { // the vector of lumis by BX is filled
//
//  float ratio = (*lsContainer).second[runAndLumiAndBx.lumiSection() - 1][0];
//  //cout << "ratio: " << ratio << endl;
//  if(ratio != 0 && ratio != -1) {
//    float recLumi = (*lsContainer).second[runAndLumiAndBx.lumiSection() - 1][runAndLumiAndBx.bx()];
//    float delLumi = recLumi/ratio;
//    return make_pair(delLumi, recLumi);
//  }
//      }
//    } 
//
//    
//  } 
//
//  cout << "Warning: run:ls " << runAndLumiAndBx.run() << ":" << runAndLumiAndBx.lumiSection() << " not found!" << endl;
//  
//  return make_pair(-1,-1);
//}




// pair<float, float> LumiFileReaderByBX::getLumi(const RunLumiIndex& runAndLumi) const {
//   if(theLumiMap.find(runAndLumi) != theLumiMap.end()) {
//     return (*(theLumiMap.find(runAndLumi))).second;
//   } else {
//     cout << "Warning: run:ls " << runAndLumi.run() << ":" << runAndLumi.lumiSection() << " not found!" << endl;
//   }
//   return make_pair(-1,-1);
// }

  

//-------------------------------------------------------



// float LumiFileReaderByBX::getDelIntegral(const RunLumiIndex& from, const RunLumiIndex& to) const {
//   float sum = 0;
//   for(map<RunLumiIndex, pair<float, float> >::const_iterator lumiInfo = theLumiMap.begin();
//       lumiInfo != theLumiMap.end();
//       ++lumiInfo) {
//     if(from < (*lumiInfo).first && (*lumiInfo).first < to) {
//       sum += (*lumiInfo).second.first;
//     }
//   }
//   return sum;
// }



// float LumiFileReaderByBX::getRecIntegral(const RunLumiIndex& from, const RunLumiIndex& to) const {
//   float sum = 0;
//   for(map<RunLumiIndex, pair<float, float> >::const_iterator lumiInfo = theLumiMap.begin();
//       lumiInfo != theLumiMap.end();
//       ++lumiInfo) {
//     if(from < (*lumiInfo).first && (*lumiInfo).first < to) {
//       sum += (*lumiInfo).second.second;
//     }
//   }
//   return sum;
// }

