#include <iostream>
#include <fstream>
#include <stdio.h>
#include <string>
#include <boost/shared_ptr.hpp>

#include "MyAnalysis/ZXSection/interface/ZSummaryHandler.h"
#include "MyAnalysis/ZXSection/interface/ZPhysicsEvent.h"

#include "Math/LorentzVector.h"
#include "Math/VectorUtil.h"


#include "CondFormats/JetMETObjects/interface/JetResolution.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TSystem.h"
#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TProfile.h"
#include "TNtuple.h"
#include "TLorentzVector.h"

using namespace std;

struct FGJob
{
public :
  Int_t ProgressiveId;
  TString FinalState;
  TString FileName;
  Int_t SampleCount;
  Float_t XSection;
  Double_t BranchingRatio;
  FGJob *Next;
};

bool isMC;
TFile *hOutputFile;
TFile *hInputFile;
TCanvas *MyCanvas;
ZSummaryHandler LeavesCutter;

TString InputPath;
TString OutputPath;
TString OutputDir;
TString JobFilePath;
TString RootFileDirName;
FGJob *JobQueue;

TH1F *HistPx, *HistPy, *HistPz;

float rescaleFactor;
int evStart, evEnd;

//Computes the Delta phi: the result is between 0 and pi 
double computeDeltaPhi(double phi1, double phi2) { 
  double deltaPhi = phi1 - phi2; 
  while(deltaPhi >= TMath::Pi()) deltaPhi -= 2*TMath::Pi(); 
  while(deltaPhi < -TMath::Pi()) deltaPhi += 2*TMath::Pi(); 
  return fabs(deltaPhi); 
} 

Bool_t LoadJobQueue(TString fPath)
{
  FILE *hFile;
  char Buffer[255];
  Int_t LineLen;
  string sss;
  TString ss1;
  Int_t ElabState, Progressive = 0;
  FGJob *Job;
  FGJob **Tail;

  hFile = fopen(fPath, "r");
  Tail = &JobQueue;

  while (!feof(hFile))
  {
    fgets (Buffer, 255, hFile);
    if (Buffer[0] != '#')
    {
      for (LineLen = 0; Buffer[LineLen] != '\n'; LineLen++);
      sss = string(Buffer, LineLen);
    
      Job = new FGJob;

      ss1.Clear();
      ElabState = 0;
      Job -> ProgressiveId = Progressive;
      *Tail = Job;
      Tail = &(Job -> Next);
      Job -> Next = 0;
      Progressive++;

      for (UInt_t k = 0; k < sss.length(); k++)
      {
	if (sss.at(k) == ' ')
	{
	  if (ss1.Length() > 0)
	  {
            cout << ss1 << "\n";
	    switch (ElabState)
	    {
	    case 0: Job -> FinalState = ss1;
	    case 1: Job -> FileName = ss1;
	    case 2: Job -> SampleCount = ss1.Atoi();
	    case 3: Job -> XSection = ss1.Atof();
	    case 4: Job -> BranchingRatio = ss1.Atof();  
	    }
	    ElabState++;
	    ss1.Clear();
	  }
       	} else ss1.Append(sss.at(k));
      }
    }
  }
  fclose(hFile);
  return kTRUE;
}

void PrintJobQueue()
{
  FGJob *Hook;

  Hook = JobQueue;
  while (Hook != 0)
  {
    cout << "Progressive id: " << (Hook -> ProgressiveId) << "\n";
    cout << "Final state: '" << (Hook -> FinalState) << "'\n";
    cout << "File name: '" << (Hook -> FileName) << "'\n";
    cout << "Sample count: " << (Hook -> SampleCount) << "\n";
    cout << "Cross section: " << (Hook -> XSection) << "\n";
    cout << "Branching ratio: " << (Hook -> BranchingRatio) << "\n\n\n";

    Hook = Hook -> Next;
  }
}

Bool_t OpenOutputFile()
{
  OutputPath = TString(OutputDir);

  gSystem -> Exec("mkdir -p " + OutputPath);
  //OutputPath += gSystem -> BaseName(InputPath);

  hOutputFile = new TFile(OutputPath, "recreate");
  return kTRUE;
}

Bool_t OpenInputFile(TString fPath)
{
  hInputFile = TFile::Open(fPath);

  if (hInputFile == 0)
  {
    cout << "Errore: file non aperto.\n";
    return kFALSE;
  }

  if (hInputFile -> IsZombie())
  {
    cout << "Errore: file zombie.\n";
    return kFALSE;
  }

  if (!LeavesCutter.attachToTree( (TTree *)hInputFile -> Get(RootFileDirName) ) )
  {
    hInputFile -> Close();
    cout << "Errore: impossibile agganciare LeavesCutter.\n";
    return kFALSE;
  }

  // set event range
  evStart = 0;
  evEnd = LeavesCutter.getEntries();

  // Solo per debug, eliminare:
  if (evEnd > 2000) evEnd = 2000;
  return kTRUE;
}

Bool_t CloseOutputFile()
{
  //hOutputFile -> cd();
  hOutputFile -> Close();
  return kTRUE;
}

Bool_t AnalyzeFile(TString fPath)
{
  if (!OpenInputFile(fPath))
  {
    cout << "Fallita apertura file: " << fPath;
    return kFALSE;
  }
   
  cout << "Analisi file: " << fPath << "\n";
  for( int iev=evStart; iev<evEnd; iev++) {
    if(iev%1000==0) {
      //cout << "[" << int(100*float(iev-evStart)/float(evEnd)) << "/100 ]" << endl;
    }
    
    // get the event
    LeavesCutter.getEntry(iev);
    ZZ2l2nuSummary_t &ev=LeavesCutter.getEvent();
    PhysicsEvent_t phys=getPhysicsEventFrom(ev);
    
    // get the event wwight
    float weight = ev.weight;
    if(!isMC) weight=1;

    LorentzVector zll = phys.leptons[0] + phys.leptons[1];
    HistPx -> Fill(zll.X());
    HistPy -> Fill(zll.Y());
    HistPz -> Fill(zll.Z());
  }
  hInputFile -> Close();
  return kTRUE;
}

Bool_t InitializeHistograms(FGJob *Job)
{
  hOutputFile -> cd();
  hOutputFile -> mkdir(Job -> FileName);
  hOutputFile -> cd(OutputPath + ":/" + (Job -> FileName));

  HistPx = new TH1F("Momentum X", "Momentum X Distribution", 200, -5, 5);
  HistPy = new TH1F("Momentum Y", "Momentum Y Distribution", 200, -5, 5);
  HistPz = new TH1F("Momentum Z", "Momentum Z Distribution", 200, -5, 5); 
 
  return kTRUE;
}

Bool_t SaveHistograms(FGJob *Job)
{
  hOutputFile -> cd(OutputPath + ":/" + (Job -> FileName));
  TObjArray *HistogramStack = new TObjArray(TCollection::kInitCapacity, 0);

  HistogramStack -> Add(HistPx);
  HistogramStack -> Add(HistPy);
  HistogramStack -> Add(HistPz);
  HistogramStack -> Write();

  return kTRUE;
}

int main(int argc, char* argv[])
{
 // load framework libraries
  gSystem -> Load( "libFWCoreFWLite" );
  AutoLibraryLoader::enable();

  //check arguments
  if ( argc < 2 ) {
    std::cout << "Usage : " << argv[0] << " parameters_cfg.py" << std::endl;
    return 0;
  }
  
  // ============================================================================
  // configure
  const edm::ParameterSet &runProcess = edm::readPSetsFrom(argv[1])->getParameter<edm::ParameterSet>("runProcess");
  InputPath = runProcess.getParameter<std::string>("input");
  OutputDir = runProcess.getParameter<std::string>("outdir");
  isMC = runProcess.getParameter<bool>("isMC");
  RootFileDirName = runProcess.getParameter<std::string>("dirName");
  JobFilePath = runProcess.getParameter<std::string>("jobfile");

  //Carico la JobQueue
  LoadJobQueue(JobFilePath);
  PrintJobQueue();

  OpenOutputFile();

  //Ciclo sulla job queue
  FGJob *Hook;  
  Hook = JobQueue;
  while (Hook != 0)
  {
    if ((Hook -> FinalState) == "ee")
    {
      InitializeHistograms(Hook);
      AnalyzeFile(InputPath + (Hook -> FileName) + ".root");
      SaveHistograms(Hook);
    }

    Hook = Hook -> Next;   
  }
  
  CloseOutputFile();
}  

