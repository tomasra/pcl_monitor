// C++ includes
#include <iostream>
#include <stdio.h>

// ROOT includes
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>

#include "fitResSlope.C"

int main(int argc, char* argv[]) {

  char inputFileName[150];
  if ( argc < 2 ){
    std::cout << "missing argument: type -h for more info" << std::endl; 
    return 0;
  }

  char *root_filename;
  char *db_filename;

  for(Int_t i=1;i<argc;i++){

    char *pchar = argv[i];

    switch(pchar[0]){

    case '-':{

      switch(pchar[1]){

      case 'f':
	root_filename = argv[i+1];
	cout << "Root File name used in this job " << root_filename << endl;
	break;

      case 'h':
	cout << "Program that calculates ttrig corrections and appends them to a" << endl;
	cout << "txt file. Please provide the root file name with residuals with the -f" << endl;
	cout << "option and a DB to be changed with the -d option." << endl;
	return 0;
	break;

      case 'd':
	db_filename = argv[i+1];
	break;

      }
    }
    }

  }

 TChain *theChain = new TChain("res_tree");

  for(int i=1;i<argc;i++) {
    theChain->Add(root_filename);
    //printf("Processing:%s\n",argv[i]);
  }

  fitResSlope res_corrections(theChain);
  res_corrections.Loop();
//   res_corrections.DumpCorrection(db_filename);

  return 1;
}
