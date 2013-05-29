/*
 *  See header file for a description of this class.
 *
 *  $Date: 2010/05/08 11:01:13 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - INFN Torino
 */

#include "FEDNtupleReader.h"
#include "FEDNumbering.h"

#include "TString.h"
#include "TFile.h"
#include "TNtuple.h"
#include "Utils.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TSQLResult.h"
#include "TSQLRow.h"
#include "TCanvas.h"
#include <iostream>
#include <sstream>
#include <vector>
#include <stdlib.h>

using namespace std;


FEDNtupleReader::FEDNtupleReader(const TString& fileName, const TString& outputFile) : theInFile(fileName),
										       theOutFile(outputFile),
										       nevents(0),
										       maxEvents(-1),
										       debug(0) {
//   // open the file containing the tree
  TFile *file = new TFile(fileName.Data());
  if(file == 0) {
    cerr << "[FEDNtupleReader]***Error: File: " << fileName << " does not exist!" << endl;
    return;
  }

  // Retrieve the TNtuple
  tree = (TNtuple *) file->Get("FEDSizeNtuple");

  cout << "Read File: " << fileName << endl;
  cout << "Opening tree: " << tree->GetName() << " with "
       << tree->GetEntries() << " entries" << endl;
  setBranchAddresses();

}

FEDNtupleReader::~FEDNtupleReader(){}



void FEDNtupleReader::setBranchAddresses() {
  // set the addresses of the tree variables
}




void FEDNtupleReader::begin() {
  cout << "Begin" << endl;

}

void FEDNtupleReader::processEvent(int entry) {
  if(entry%100000 == 0 ||  debug > 2) {
    cout << "-----  Process event " << entry << endl;
  }

  

  
 }


void FEDNtupleReader::end() {
  cout << "End, # processed events: " << nevents << endl;

  // Create the root file
  TFile *theFile = new TFile(theOutFile.Data(), "RECREATE");
  theFile->cd();

  // Write the histos
  theFile->Close();
}

void FEDNtupleReader::analyse(const int nEventMax) {
  int max = tree->GetEntries();
  if(nEventMax != -1) max = nEventMax;
  begin();
  for(int i = 0; i < max; i++) {
    tree->GetEntry(i);
    processEvent(i);
    nevents++;
  }
  end();
}




void FEDNtupleReader::setDebug(int debug) {
  this->debug = debug;
}

TH1F *FEDNtupleReader::drawTH1F(const TString& name, const TString& formula, const TString& selection,
				int nBins, float binMin, float binMax, const TString& option) {

//   if(maxEvents == -1) maxEvents = tree->GetEntries();
//   cout << "# events to be processed: " << maxEvents << endl;

//   // Create the new histo to be added to the stack
//   TH1F * hNew = new TH1F(name.Data(),name.Data(),nBins, binMin, binMax);
//   hNew->Sumw2();

//   TString fedRange;
//   if(!detToFEDRange(formula, fedRange)) {
//     fedRange = formula;
//   }


//   // decide whether the fields should be summed or not
//   bool doSum = false;
//   if(option.Contains("sum") || option.Contains("SUM")) {
//     doSum = true;
//   }

     
//   int modulo = 100000;
//   int nev = 0;
//   while(nev < maxEvents) {
//     cout << "Query starting from: " << nev << " on # ev: " << modulo << endl;

//     TSQLResult * query = tree->Query(fedRange.Data(), selection, "", modulo, nev);

//     // get the # of fields in the query
//     int nfields = query->GetFieldCount();

//     // Fill the histo
//     TSQLRow * row = 0;
//     while ((row = query->Next())) {
// //       if(nev % 1000 == 0) 
// //       cout << "# processing event: " << nev << endl;
//       float variable = 0;
//       float weight = 1.0;
    
//       // add all fields
//       for(int i = 0; i != nfields; ++i) {
// 	if(doSum) variable += atof(row->GetField(i));
// 	else hNew->Fill(atof(row->GetField(i)));
//       }
//       if(doSum)hNew->Fill(variable,weight);
//       delete row;
//       ++nev;
//     }
//     delete query;
//   }

//   tree->ResetBranchAddresses();
//   cout << " # processed events: " << nev << endl;
  if(theHistoMap1D.find(name) == theHistoMap1D.end()) {
    addTH1F(name, formula, selection, nBins, binMin, binMax, option);
  } else {
    cout << "Histo already booked!Check if filled!" << endl;
  }

  runQueries(maxEvents,selection);

  return  drawTH1F(name, option);

}



TH2F *FEDNtupleReader::drawTH2F(const TString& name,
				const TString& formulaX, const TString& formulaY, 
				const TString& selection,
				int nBinsX, float binMinX, float binMaxX,
				int nBinsY, float binMinY, float binMaxY,
				const TString& option) {

  if(theHistoMap2D.find(name) == theHistoMap2D.end()) {
    addTH2F(name, formulaX, formulaY, selection, nBinsX, binMinX, binMaxX,
	    nBinsY, binMinY, binMaxY, option);
  } else {
    cout << "Histo already booked!Check if filled!" << endl;
  }

  runQueries(maxEvents,selection);
  return  drawTH2F(name, option);

}




bool FEDNtupleReader::detToFEDRange(const TString& detName, TString &fedRange) const {
  stringstream ret;
  int count = 0;
  for(int fed = 0; fed != 1024; ++fed) {
    if(string(detName.Data()) == FEDNumbering::fromDet(fed)) {
      if(count == 0) {
	ret << "FED" << fed;
      } else {
	ret << "+FED" << fed;
      }
      count++;
    }
  }
  fedRange = TString(ret.str().c_str());
  if(count != 0) { 
    cout << "Det: " << detName << " FED range: " << fedRange << endl;
    return true;
  }
  return false;
}



void FEDNtupleReader::addTH1F(const TString& name, const TString& formula, const TString& selection,
			      int nBins, float binMin, float binMax, const TString& option) {
  theQueryName.push_back(name);

  // Create the new histo to be added to the stack
  TH1F * hNew = new TH1F(name.Data(),name.Data(),nBins, binMin, binMax);
  hNew->SetBit(TH1::kCanRebin);
  hNew->Sumw2();
  // add to map
  theHistoMap1D[name] = hNew;

  the1DHistos.push_back(hNew);
  the2DHistos.push_back(NULL);

  // get the feds to be queried
  TString fedRange;
  if(!detToFEDRange(formula, fedRange)) {
    fedRange = formula;
  }
  
  if(the1DHistos.size() == 1) { // this is the 1st query added
    theQuery = fedRange;
  } else {
    theQuery = theQuery + ":" + fedRange;
  }

  int nFields = fedRange.CountChar(':') + 1;
  theNFields.push_back(nFields);
  theNFieldsX.push_back(nFields);

  theOptions.push_back(option);

}

void FEDNtupleReader::addTH2F(const TString& name,
				const TString& formulaX, const TString& formulaY, 
				const TString& selection,
				int nBinsX, float binMinX, float binMaxX,
				int nBinsY, float binMinY, float binMaxY,
				const TString& option) {
  theQueryName.push_back(name);
  // Create the new histo to be added to the stack
  TH2F * hNew = new TH2F(name.Data(),name.Data(),
			 nBinsX, binMinX, binMaxX,
			 nBinsY, binMinY, binMaxY);
  hNew->SetBit(TH1::kCanRebin);
  // add to map
  theHistoMap2D[name] = hNew;

  the1DHistos.push_back(NULL);
  the2DHistos.push_back(hNew);


  TString fedRangeX;
  if(!detToFEDRange(formulaX, fedRangeX)) {
    fedRangeX = formulaX;
  }
  int nFieldsX = fedRangeX.CountChar(':') + 1;

  TString fedRangeY;
  if(!detToFEDRange(formulaY, fedRangeY)) {
    fedRangeY = formulaY;
  }
  int nFieldsY = fedRangeY.CountChar(':') + 1;
  cout << "# of fields X: " <<   nFieldsX << " Y: " << nFieldsY << endl; 

  TString fedRange = fedRangeX + ":" + fedRangeY;
  
  if(the1DHistos.size() == 1) { // this is the 1st query added
    theQuery = fedRange;
  } else {
    theQuery = theQuery + ":" + fedRange;
  }

  theNFields.push_back(nFieldsX+nFieldsY);
  theNFieldsX.push_back(nFieldsX);

  theOptions.push_back(option);

}


void FEDNtupleReader::runQueries(int maxEv, const TString& selection) {
  maxEvents = maxEv;
  if(maxEvents == -1) maxEvents = tree->GetEntries();

  int modulo = 100000;
  int nev = 0;
  int niter = 0;
  while(nev < maxEvents && niter*modulo < maxEvents) {
    cout << "Query " << niter << " starting from: " << niter*modulo << " on # ev: " << modulo << endl;
    if(debug > 2) cout << "   " << theQuery << endl;

    TSQLResult * query = tree->Query(theQuery.Data(), selection, "", modulo, niter*modulo);
    niter++;
    // Fill the histo
    TSQLRow * row = 0;
    while ((row = query->Next())) {
      if(debug > 2) cout << "Entry: " << nev << endl;
      int previousFields = 0;
      // loop over all subqueries
      for(unsigned int qu = 0; qu != theQueryName.size(); ++qu) {
	if(debug > 2) cout << "- Query: " << theQueryName[qu] << endl;

	// retireve the # fields
	int nFields = theNFields[qu];
	int nFieldsX = theNFieldsX[qu];
	int nFieldsY =  nFields - nFieldsX;
	if(debug > 2) cout << "  total # of fields: " << nFields << endl;
	
	TString option = theOptions[qu];

	if(nFieldsY == 0) { // 1D hitsto
	  if(debug > 2) cout << "  query is 1D" << endl;
	  TH1F *hNew = the1DHistos[qu];
	  float variable = 0;
	  float weight = 1.0;

	  // decide whether the fields should be summed or not
	  bool doSum = false;
	  if(option.Contains("sum") || option.Contains("SUM")) {
	    doSum = true;
	  }
	  // add all fields
	  for(int i = previousFields; i != previousFields+nFields; ++i) {
	    if(debug > 2) cout << "   field: " << i << " value: " << atof(row->GetField(i)) << endl;
	    if(doSum) variable += atof(row->GetField(i));
	    else hNew->Fill(atof(row->GetField(i)));
	  }
	  if(doSum)hNew->Fill(variable,weight);
	} else { // 2D histo
	  if(debug > 2) cout << "  query is 2D" << endl;
	  TH2F *hNew = the2DHistos[qu];
	  float variableX = 0;
	  float variableY = 0;
	  float weight = 1.0;

	  // add all fields
	  for(int i = previousFields; i != previousFields+nFieldsX; ++i) {
	    if(debug > 2) cout << "    field: " << i << " is X" << " value: " << atof(row->GetField(i)) <<endl;
	    variableX += atof(row->GetField(i));
	  }
	  for(int i = previousFields+nFieldsX; i != previousFields+nFieldsX+nFieldsY; ++i) {
	    if(debug > 2) cout << "    field: " << i << " is Y" << " value: " << atof(row->GetField(i)) <<endl;
	    variableY += atof(row->GetField(i));
	  }
	  hNew->Fill(variableX, variableY, weight);
	}
	previousFields += nFields;
      }
      delete row;
      ++nev;
    }
    
    delete query;
  }    
  tree->ResetBranchAddresses();
  cout << " # processed events: " << nev << endl;

  // draw all histos
   for(unsigned int qu = 0; qu != theQueryName.size(); ++qu) {
	if(debug > 2) cout << "- Query: " << theQueryName[qu] << endl;
	TH1F *histo1D = the1DHistos[qu];
	if(histo1D != NULL) {
	  drawTH1F(theQueryName[qu], theOptions[qu]);
	}
	TH2F *histo2D = the2DHistos[qu];
	if(histo2D != NULL) {
	  drawTH2F(theQueryName[qu], theOptions[qu]);
	}
   }


  // reset all queries
  theQuery = "";
  theNFields.clear();
  theNFieldsX.clear();
  theOptions.clear();
  theQueryName.clear();
  the1DHistos.clear();
  the2DHistos.clear();

}


TH1F *FEDNtupleReader::getTH1F(const TString& name) {
  map<TString, TH1F *>::iterator hist = theHistoMap1D.find(name);
  if(hist == theHistoMap1D.end()) {
    cout << "Histo: " << name << " not found!!!" << endl;
    return 0;
  }
  return (*hist).second;
}


TH2F *FEDNtupleReader::getTH2F(const TString& name) {
  map<TString, TH2F *>::iterator hist = theHistoMap2D.find(name);
  if(hist == theHistoMap2D.end()) {
    cout << "Histo: " << name << " not found!!!" << endl;
    return 0;
  }
  return (*hist).second;
}


TH1F *FEDNtupleReader::drawTH1F(const TString& name, const TString& option) {
  TH1F *hNew = getTH1F(name);
  if(hNew == 0) return 0;
  if(!option.Contains("same") || !option.Contains("SAME")) {
    TCanvas *c = Utils::newCanvas(name, 1);
    c->cd();
    if(option.Contains("logx")) c->SetLogx();
    if(option.Contains("logy")) c->SetLogy();
  }
  hNew->Draw(option.Data());
  return hNew;
}


TH2F *FEDNtupleReader::drawTH2F(const TString& name, const TString& option) {
  TH2F *hNew = getTH2F(name);
  if(hNew == 0) return 0;
  if(!option.Contains("same") || !option.Contains("SAME")) {
    TCanvas *c = Utils::newCanvas(name, 1);
    c->cd();
    if(option.Contains("logx")) c->SetLogx();
    if(option.Contains("logy")) c->SetLogy();
  }
  hNew->Draw(option.Data());
  return hNew;
}
