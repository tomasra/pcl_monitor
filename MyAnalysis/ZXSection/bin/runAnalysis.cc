#define WebVersion 2

#include <iostream>
#include <fstream>
#include <stdio.h>
#include <errno.h>
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

#include "TStyle.h"
#include "TSystem.h"
#include "TKey.h"
#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TLegendEntry.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TProfile.h"
#include "TNtuple.h"
#include "TLorentzVector.h"
#include "TMath.h"
#include "THStack.h"
#include "TList.h"
#include "TText.h"
#include "TLatex.h"
#include "TGraph.h"
#include "TGraphErrors.h"

using namespace std;

TFile *hOutputFile;
TFile *hInputFile;
TCanvas *MyCanvas;
ZSummaryHandler LeavesCutter;
ofstream hRunReport;

Int_t ColorCount;
TString LumiDBPath;
TString InputPath;
TString OutputPath;
TString OutputDir;
TString JobFilePath;
TString RootFileDirName;
TCanvas *TempCanvas[100];
Double_t OutputLumi;

Bool_t DebugMode = kFALSE;
Bool_t LowQuality = kFALSE;
Bool_t SkipMC = kFALSE;
Bool_t LimitedLumi = kFALSE;
Bool_t SetupOnly = kFALSE;

ifstream LumiBinFile[2];
ofstream MissingLumiFile[2];
ofstream Locomotives[2];

float rescaleFactor;
int evStart, evEnd;


#include "MyAnalysis/ZXSection/bin/Lists.cc"
#include "MyAnalysis/ZXSection/bin/Parser.h"
#include "MyAnalysis/ZXSection/bin/Jobs.h"
#include "MyAnalysis/ZXSection/bin/Luminosity.h"

#include "MyAnalysis/ZXSection/bin/Colors.cc"
#include "MyAnalysis/ZXSection/bin/ParserLoader.cc"
#include "MyAnalysis/ZXSection/bin/Parser.cc"
#include "MyAnalysis/ZXSection/bin/Luminosity.cc"
#include "MyAnalysis/ZXSection/bin/Web.cc"
#include "MyAnalysis/ZXSection/bin/Jobs.cc"
#include "MyAnalysis/ZXSection/bin/Physics.cc"
#include "MyAnalysis/ZXSection/bin/Config.cc"

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
  //if (DebugMode) if (evEnd > 20000) evEnd = 20000;
  return kTRUE;
}

Bool_t CloseOutputFile()
{
  //hOutputFile -> cd();
  hOutputFile -> Close();
  return kTRUE;
}

Bool_t AnalyzeFile(TString fPath, FGJob *Job)
{
  if (!OpenInputFile(fPath))
  {
    cout << "Fallita apertura file: " << fPath;
    return kFALSE;
  }

  //cout << "\n\nApertura file: " << fPath << "\n";
  //cout << "Entries: " << evEnd << "\n";
  //evEnd = Job -> SampleCount;
  //cout << "Entries: " << evEnd << "\n";
  
  Bool_t Errore = kFALSE; 
  Int_t Codice, MissingLumi[2];
  char Progress[8] = "";

  MissingLumi[0] = 0;
  MissingLumi[1] = 0;
  
  cout << "Analisi file: " << fPath << " [0.000000%]";
  for(int i = evStart; i < evEnd; i++)
  {
    if (i % 100 == 0)
    {
      sprintf(Progress, "%f", ((float)i - evStart) / (evEnd - evStart) * 100);
      for (int j = 0; j < 10; j++) cout << "\b";
      for (int j = 0; j < 8; j++) cout << Progress[j];
      cout << "%]";
      cout.flush();
    }

    Codice = LeavesCutter.getEntry(i);
    if (Codice < 1)
    {
      if (!Errore)
      {
        Errore = kTRUE;
        cout << "Primo errore: " << i << "\n";
      }
    }
    else
    {
      ZZ2l2nuSummary_t &Event = LeavesCutter.getEvent();
      PhysicsEvent_t Physics = getPhysicsEventFrom(Event);
      float Weight = Event.weight;

      if (!(Job -> isMC))
      {
        Weight = 1;

	FGLumiEntry *TempLumi = GetLuminosity(0, Physics.Run, Physics.LumiSection);

	if (TempLumi == 0 || TempLumi -> Delivered < 0.1 or TempLumi -> Recorded < 0.1)
	{
	  MissingLumi[0]++;
	  MissingLumiFile[0] << Physics.Run << " " << Physics.LumiSection << " " << Physics.BXId << "\n";
	  Physics.isLocomotive[0] = kFALSE;
	}
	else
	{
	  Physics.Delivered[0] = TempLumi -> Delivered;
	  Physics.Recorded[0] = TempLumi -> Recorded;
	  Physics.isLocomotive[0] = PartOfIntList(TempLumi -> Locomotive, Physics.BXId);
	}
	Physics.BXDelivered[0] = GetBXLuminosity2(0, Physics.Run, Physics.LumiSection, Physics.BXId);

	//if (Physics.BXDelivered[0] == -1) cout << "Lumi mancante: " << Physics.Run << " " << Physics.LumiSection << " " << Physics.BXId << "\n";

        TempLumi = GetLuminosity(1, Physics.Run, Physics.LumiSection);
	if (TempLumi == 0 || TempLumi -> Delivered < 0.1 or TempLumi -> Recorded < 0.1)
	{
	  MissingLumi[1]++;
	  MissingLumiFile[1] << Physics.Run << " " << Physics.LumiSection << " " << Physics.BXId << "\n";
	  Physics.isLocomotive[1] = kFALSE;
	}
	else
	{
	  Physics.Delivered[1] = TempLumi -> Delivered;
	  Physics.Recorded[1] = TempLumi -> Recorded;
	  Physics.isLocomotive[1] = PartOfIntList(TempLumi -> Locomotive, Physics.BXId);
	}
	Physics.BXDelivered[1] = GetBXLuminosity2(1, Physics.Run, Physics.LumiSection, Physics.BXId);
	
	//.Run, Physics.LumiSection, Physics.Delivered, Physics.Recorded);
      }
      FillHistograms(&Physics, Weight, Job);
    }
  }

  for (int j = 0; j < 10; j++) cout << "\b";
  cout << "DONE]     \n";
  if (MissingLumi[0] > 0) cout << MissingLumi[0] << " luminosità mancanti da lumicalc.\n";
  if (MissingLumi[1] > 0) cout << MissingLumi[1] << " luminosità mancanti da lumicalc2.\n";

  hInputFile -> Close();
  return kTRUE;
}

Bool_t CreateHistogramUnionEx()
{
  TList *ElencoChiavi, *NomiIstogrammi = new TList();
  TDirectory *TempDir;
  FGJob *Hook;
  Float_t TotalSum = 0;

  hOutputFile -> Cd(OutputPath + ":/");
  hOutputFile -> mkdir("Synopsis");

  cout << "\nInizio creazione sinossi.\n";
  TempDir = hOutputFile -> GetDirectory(OutputPath + ":/" + (JobQueue -> FileName));
  if (TempDir == 0) {cout << "Impossibile aprire la cartella //Synopsis, sinossi abortita.\n"; return kFALSE;}
  
  ElencoChiavi = TempDir -> GetListOfKeys();
  for (Int_t i = 0; ElencoChiavi -> At(i) != 0; i++)
  {
    TKey *TempKey = 0;
    TempKey = (TKey *)ElencoChiavi -> At(i);
    if (TempKey == 0) {cout << "Chiave non valida.\n"; return kFALSE;}

    TObject *TempObj = TempKey -> ReadObj();
    if (TempObj == 0) {cout << "Chiave non valida.\n"; return kFALSE;}

    TString *TempStr = new TString(TempObj -> GetName());
    TempStr -> Append(";1");
    NomiIstogrammi -> Add((TObject *)TempStr);
    
  }

  Hook = JobQueue;
  while (Hook != 0) {if (Hook -> toSynopsis) TotalSum += Hook -> ContentSum; Hook = Hook -> Next;}

  cout << "Copiati nomi istogrammi.\n";
  for (Int_t i = 0; NomiIstogrammi -> At(i) != 0; i++)
  {
    THStack *HSMontecarlo = new THStack();
    TH1F *HDatiReali = 0, *TempHist = 0;
    TLegend *Legenda = new TLegend(.7, .70, .95, .95);
    //TLegend *Legenda2 = new TLegend(.05, .05, .95, .95);
    TLegendEntry *TempEntry = 0;
    Double_t IntegralSum = 0;

    Hook = JobQueue;
    while (Hook != 0)
    {
      hOutputFile -> cd(OutputPath + ":/" + (Hook -> FileName));
      TempDir = hOutputFile -> GetDirectory(OutputPath + ":/" + (Hook -> FileName));
      if (TempDir == 0) {cout << "Impossibile aprire cartella, sinossi abortita.\n"; return kFALSE;}

      TempHist = (TH1F*)(TempDir -> Get(((TString *)NomiIstogrammi -> At(i)) -> Data()));
      if (TempHist == 0){cout << "Impossibile aprire istogramma, sinossi abortita.\n"; return kFALSE;}

      if (Hook -> toSynopsis)
	  {
	    char Content[16];
	    TString TempStr = TString("");
            TempStr.Append(Content);

            //TempHist -> Scale(OutputLumi);
            sprintf(Content, "%f", TempHist -> Integral());
	    IntegralSum += TempHist -> Integral();
	    Hook -> ContentSum = TempHist -> Integral();
	    TempStr = TString(Content);

            HSMontecarlo -> Add(TempHist, "HIST");
            TempEntry = Legenda -> AddEntry(TempHist, Hook -> Label -> Data(), "F");
	  }
          else if (HDatiReali == 0) HDatiReali = new TH1F(*TempHist); 
	  else HDatiReali -> Add(TempHist);
     
      Hook = Hook -> Next; 
    }

    TAxis *TempAxis = 0;
    TCanvas *TempCanvas = new TCanvas(TempHist -> GetName(), TempHist -> GetTitle(), 550, 400);

    HSMontecarlo -> SetName(TempHist -> GetName());
    TempCanvas -> SetName(TempHist -> GetName());
    TempCanvas -> SetTitle(TempHist -> GetTitle());

    char Content[16];
    TString TempStr = TString("");

    sprintf(Content, "%f", HDatiReali -> Integral());
    TempStr = TString(Content);

    HDatiReali -> SetFillStyle(4000);
    HDatiReali -> SetMarkerColor(kBlack);
    TempEntry = Legenda -> AddEntry(HDatiReali);    
    TempEntry -> SetLabel("Collected data");

    HSMontecarlo -> Draw("HIST");
    TempAxis = TempHist -> GetXaxis();
    if (TempAxis == 0) cout << "Errore nel caricamento dell'asse X\n"; 
    else
    {
      TAxis *TempAxis2;
      TempAxis2 = HSMontecarlo -> GetXaxis();
      if (TempAxis2 == 0) {cout << "Errore nel caricamento dell' asse X destinazione\n"; break;}
      TempAxis2 -> SetTitle(TempAxis -> GetTitle());
    }

    TempAxis = TempHist -> GetYaxis();
    if (TempAxis == 0) cout << "Errore nel caricamento dell'asse Y\n"; 
    else
    {
      TAxis *TempAxis2;
      TempAxis2 = HSMontecarlo -> GetYaxis();
      if (TempAxis2 == 0) {cout << "Errore nel caricamento dell' asse X destinazione\n"; break;} 
      TempAxis2 -> SetTitle(TempAxis -> GetTitle());
    }

    HSMontecarlo -> SetMinimum(HSMontecarlo -> GetMaximum() / 100000);
    HSMontecarlo -> Draw("HIST");
    HDatiReali -> Draw("SAME E1");
    Legenda -> Draw();
    
    //Legenda2 -> Draw();
    hOutputFile -> cd(OutputPath + ":/Synopsis");
    TempCanvas -> Write();

    hOutputFile -> Flush();
  }

  cout << "Sinossi completa\n";
  return kTRUE;
}

Bool_t DrawEventCountReport()
{
  hOutputFile -> cd(OutputPath + ":/");
  Int_t JobCount = 0, JobIndex = 0;
  Float_t IntegralSum = 0;
  FGJob *Hook;

  Hook = JobQueue;
  while (Hook != 0)
  {
    if (Hook -> toSynopsis)
    {
      JobCount++;
      IntegralSum += Hook -> ContentSum;
    }
    Hook = Hook -> Next;
  }

  TCanvas *TempCanvas = new TCanvas("Event count", "Conteggio eventi", 550, 400);
  Hook = JobQueue;
  while (Hook != 0)
  {
    if (Hook -> toSynopsis)
    {
      char Content[16];
      TString TempStr = TString("000000000");
      TString TempStr2 = TString("");

      sprintf(Content, "%i", (Int_t)((Hook -> ContentSum / IntegralSum) * 1000000000));
      cout << (Int_t)((Hook -> ContentSum / IntegralSum) * 1000000000);
      TempStr.Append(Content);

      for (Int_t i = 0; i < 10; i++) 
      {
        TempStr2.Append(TempStr.Data()[TempStr.Length() - 9 + i]);
        if (i % 3 == 2) TempStr2.Append(' ');
      }

      sprintf(Content, "%f", Hook -> ContentSum);
      TempStr = TString(Content);
      TempStr = *(Hook -> Label) + "  -  " + TempStr + "  (" + TString(TempStr2 + " ppb)  ");
      cout << TempStr << "\n";
   
      TLatex *TempText = new TLatex(0, (float)(JobIndex + 2) / (JobCount + 4), TempStr.Data());
      TempText -> Draw();
      JobIndex++;
    }
    Hook = Hook -> Next; 
  }
  TempCanvas -> Write();
  return kTRUE;
}

int main(int argc, char* argv[])
{
  // load framework libraries
  gSystem -> Load( "libFWCoreFWLite" );
  AutoLibraryLoader::enable();
  
  for (Int_t i = 1; i < argc; i++)
  {
    if (strcmp(*(argv + i), "debug") == 0) DebugMode = kTRUE;
    if (strcmp(*(argv + i), "lq") == 0) LowQuality = kTRUE;
    if (strcmp(*(argv + i), "nomc") == 0) SkipMC = kTRUE;
    if (strcmp(*(argv + i), "limitlumi") == 0) LimitedLumi = kTRUE;
    if (strcmp(*(argv + i), "suonly") == 0) SetupOnly = kTRUE;    
  } 

  gStyle -> SetOptFit(111);
  gStyle -> SetOptStat("nemr");

  cout << "Caricamento configurazione... \n";
  LoadConfiguration();
  LoadFamilyNames();
  LoadParsers();
  //PrintParsers();

  if (SetupOnly) return 0;

  cout << "Caricamento database luminosità... \n";
  //LumiBinFile.open ("/afs/cern.ch/user/f/fguatier/LumiDB/LumiBXRed.bin", ios::in | ios::binary);
  LumiBinFile[0].open ("/data/fguatier/LumiBX.bin", ios::in | ios::binary);
  LumiBinFile[1].open ("/data/fguatier/LumiBX2.bin", ios::in | ios::binary);
  MissingLumiFile[0].open ("MissingLumi1.txt", ios::out);
  MissingLumiFile[1].open ("MissingLumi2.txt", ios::out);  
  Locomotives[0].open ("Locomotives1.txt", ios::out);
  Locomotives[1].open ("Locomotives2.txt", ios::out);  

  LoadFullLuminosityDB();
  PrintParsers();

  cout << "Caricamento Job Queue...\n\n";
  LoadJobQueue(JobFilePath);
  if (DebugMode) PrintJobQueue();

  OpenOutputFile();

  //Ciclo sulla job queue
  ColorCount = 0;
  FGJob *Hook = JobQueue;
  while (Hook != 0)
  {
    if (strcmp(Hook -> FinalState.Data(), "ee") == 0 && (!SkipMC || !(Hook -> isMC)))
    {
      InitializeHistograms(Hook);
      AnalyzeFile(TString(TString(InputPath) + Hook -> FileName + ".root"), Hook);
      SaveHistograms(Hook);
      ColorCount++;
    }
    Hook = Hook -> Next;
  }

  ComputeParserCoords();
  PrintParsers();

  //CreateHistogramUnionEx();
  //DrawEventCountReport();
  //PrintParsers();
  ExportParsers();

  CloseOutputFile();
  LumiBinFile[0].close();
  LumiBinFile[1].close();

  MissingLumiFile[0].close();
  MissingLumiFile[1].close();

  Locomotives[0].close();
  Locomotives[1].close();

  cout << "\nInizio esportazione web\n";
  FullWebExport(TString(OutputPath));
}  

