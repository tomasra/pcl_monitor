#define ZlumiTreeReader_cxx
// The class definition in ZlumiTreeReader.h has been generated automatically
// by the ROOT utility TTree::MakeSelector(). This class is derived
// from the ROOT class TSelector. For more information on the TSelector
// framework see $ROOTSYS/README/README.SELECTOR or the ROOT User Manual.

// The following methods are defined in this file:
//    Begin():        called every time a loop on the tree starts,
//                    a convenient place to create your histograms.
//    SlaveBegin():   called after Begin(), when on PROOF called only on the
//                    slave servers.
//    Process():      called for each event, in this function you decide what
//                    to read and fill your histograms.
//    SlaveTerminate: called at the end of the loop on the tree, when on PROOF
//                    called only on the slave servers.
//    Terminate():    called at the end of the loop on the tree,
//                    a convenient place to draw/fit your histograms.
//
// To use this file, try the following session on your Tree T:
//
// Root > T->Process("ZlumiTreeReader.C")
// Root > T->Process("ZlumiTreeReader.C","some options")
// Root > T->Process("ZlumiTreeReader.C+")
//

#include "ZlumiTreeReader.h"
#include "HistoZ.h"
#include <TH2.h>
#include <TProfile.h>
#include <TCanvas.h>
#include <TGraphErrors.h>
#include <TStyle.h>
#include <iostream>
#include <string>
#include <sstream>
#include <string> 

using namespace std;

int run_number;

TFile* myFile;

HistoZ* hAll = 0;
vector<HistoZ *> hByBin;
TH1F* hLumiIntegralsByBin;
int nBins = 100;
float minBin = -1;
float maxBin = 10;
vector<pair<float,float> > hByBinLimits;

TH1F* massZ;
TH1F* wholeMassZ;
TH1F* ptZ;
TH1F* massZ_selected;
TH1F* wholeMassZ_selected;

TH1F* ptL1;
TH1F* etaL1;
TH1F* phiL1;
TH1F* isoL1;
TH1F* sipL1;

TH1F* ptL2;
TH1F* etaL2;
TH1F* phiL2;
TH1F* isoL2;
TH1F* sipL2;

TH2F* ptLeptons;

TH1F* numZPerEvent;

int countZ;


TH1F* cutflow;
int beforeCuts;
int cutPt;
int cutEta;
int cutSIP;
int cutIsolation;
int cutZMass;

bool survive_withoutIso;
int withoutIso;
bool survive_withIso;
int withIso;
bool survive_eta_withoutIso;
int eta_withoutIso;
bool survive_eta_withIso;
int eta_withIso;

const double M_Z = 91.2;
const double Cross_Section = 1.1; // nb
const double Cross_Section_Error = 0.03; // nb  

//LumiFileReaderByBX lumiReader("./");
LumiFileReaderByBX lumiReader("/data1/ZLumiStudy/CalcLumi/Version0/");
TProfile* pileUp_delLumi;
TProfile* pileUp_lumiPerBX;

int runTest = -1;

float delLumiPerBX = -1;

vector<TH1F* > histPerLumi;
TH1F* lumiPerBX;

TProfile* ls_delLumi;
TProfile* lumi_crossSection;
TProfile* ls_crossSection;


map<int,int> ls_Zcount;

template <typename A, typename B>
static A lexical_cast(const B& b)
{
  std::stringstream sstr;
  sstr << b;
  A a;
  sstr >> a;
  return a;
}

int to_int(string str)
{
    stringstream sstr(str);
    int res = -1;
    sstr >> res;
    return res;
} 

string to_string(int i)
{
    stringstream sstr;
    sstr << i;
    return sstr.str();
} 

TH1F* CreateHist(string name, string xtitle, string unit, size_t nbins, float xmin, float xmax)
{
	TString title;

	float binSize = (xmax-xmin) / nbins;

	// want to write: 1 or nothing
	if (binSize == 1) {
		if (unit.c_str() == string("")) {
		  title.Form(";%s; Events", xtitle.c_str());
		}
		else {
			title.Form(";%s [%s];Events / %2.0f %s", xtitle.c_str(), unit.c_str(), binSize, unit.c_str());
		}	
	}

	// want to write: 0.??
	else if (binSize < 1) {
			if (unit.c_str() == string("")) {
			title.Form(";%s; Events / %1.2f", xtitle.c_str(), binSize);
		}
		else {
			title.Form(";%s [%s];Events / %1.2f %s", xtitle.c_str(), unit.c_str(), binSize, unit.c_str());
		}	
	}

	// want to write: ??
	else {
		if (unit.c_str() == std::string("")) {
			title.Form(";%s; Events / %2.0f", xtitle.c_str(), binSize);
			}
		else if (unit.c_str() == std::string("cm^{-2}s^{-1}")) {
			binSize = binSize / pow(10., 33);
			title.Form("; %s; Events / %g #times 10^{33} %s", xtitle.c_str(), binSize, unit.c_str());
		}
		else {
			title.Form(";%s [%s];Events / %2.0f %s", xtitle.c_str(), unit.c_str(), binSize, unit.c_str());
		}	
	}

	
	TH1F* a = new TH1F(name.c_str(), title, nbins, xmin, xmax);
	return a;
}

float calcLumi(float lumiBarn) {
	float my_barn = pow(10.0, -30);
	int bunch = 1440;

	return lumiBarn / (my_barn * LENGTH_LS) * bunch;
}

float calcLumi_avgInst(float lumiBarn) {
	float my_barn = pow(10.0, -30);
	int bunch = 1440;

	return lumiBarn / (my_barn) * bunch;
}



bool ZlumiTreeReader::analyseCut(/*SIP*/ float sip, /*pt*/ float pt, /*eta*/ float eta, /*Iso*/ float iso, /*ZMass*/ float massZ_min, float massZ_max, int index_Z) {

	beforeCuts ++;
	
	if (Lep1SIP->at(index_Z) < sip && Lep2SIP->at(index_Z) < sip) { 
		cutSIP ++;
		if (Lep1Pt->at(index_Z) > pt && Lep2Pt->at(index_Z) > pt) {
			cutPt ++;
			if (abs(Lep1Eta->at(index_Z)) < eta && abs(Lep2Eta->at(index_Z)) < eta) {
				cutEta ++;
				if ((Lep1chargedHadIso->at(index_Z) + Lep1neutralHadIso->at(index_Z) + Lep1photonIso->at(index_Z)) / Lep1Pt->at(index_Z) < iso && (Lep2chargedHadIso->at(index_Z) + Lep2neutralHadIso->at(index_Z) + Lep2photonIso->at(index_Z)) / Lep2Pt->at(index_Z) < iso) {
					cutIsolation ++;

					if (ZMass->at(index_Z) > massZ_min && ZMass->at(index_Z) < massZ_max) {
						cutZMass ++;
						ls_Zcount[LumiNumber] ++;
						return true;
					}
				}
			}
		}
	}
	return false;
}




int getIndex(float lumi) { // look for lumi Per BX
	if (lumi < 40) return 0;
	if (lumi < 45) return 1;
	if (lumi < 50) return 2;
	if (lumi < 55) return 3;
	if (lumi < 60) return 4;
	if (lumi < 65) return 5;
	if (lumi < 70) return 6;
	if (lumi < 75) return 7;
	if (lumi < 80) return 8;
	return 9;
}

string getLumiPerBXRegion(int index) {
	if (index == 0) return "Luminosity per BX is lower than " + lexical_cast<string>(calcLumi(40) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1}";
	if (index == 1) return "Luminosity per BX is between " + lexical_cast<string>(calcLumi(40) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1} and " + lexical_cast<string>(calcLumi(45) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1}";
	if (index == 2) return "Luminosity per BX is between " + lexical_cast<string>(calcLumi(45) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1} and " + lexical_cast<string>(calcLumi(50) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1}";
	if (index == 3) return "Luminosity per BX is between " + lexical_cast<string>(calcLumi(50) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1} and " + lexical_cast<string>(calcLumi(55) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1}";
	if (index == 4) return "Luminosity per BX is between " + lexical_cast<string>(calcLumi(55) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1} and " + lexical_cast<string>(calcLumi(60) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1}";
	if (index == 5) return "Luminosity per BX is between " + lexical_cast<string>(calcLumi(60) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1} and " + lexical_cast<string>(calcLumi(65) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1}";
	if (index == 6) return "Luminosity per BX is between " + lexical_cast<string>(calcLumi(65) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1} and " + lexical_cast<string>(calcLumi(70) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1}";
	if (index == 7) return "Luminosity per BX is between " + lexical_cast<string>(calcLumi(70) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1} and " + lexical_cast<string>(calcLumi(75) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1}";
	if (index == 8) return "Luminosity per BX is between " + lexical_cast<string>(calcLumi(75) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1} and " + lexical_cast<string>(calcLumi(80) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1}";
	return "Luminosity per BX is higher than " + lexical_cast<string>(calcLumi(80) / pow(10., 33)) + " #times10^{33} cm^{-2}s^{-1}";
}


void ZlumiTreeReader::Begin(TTree* /*tree*/)
{
	// The Begin() function is called at the start of the query.
	// When running with PROOF Begin() is only called on the client.
	// The tree argument is deprecated (on PROOF 0 is passed).

	string option = GetOption();
	run_number = to_int(option);
	cout << "start the Begin-function for Run " << run_number << endl;

	if (run_number == -1) {
		myFile = new TFile("data/test.root", "RECREATE");
	}
	else {
		string file_name = "data/ZLumiStudy_RunNumber_" + to_string(run_number) + ".root";
		cout << file_name << endl;
		myFile = new TFile(file_name.c_str(), "RECREATE");
	}

	massZ = CreateHist("ZMass", "M_{Z}", "GeV", 60, 60, 120);
	wholeMassZ = CreateHist("wholeMassRange", "M_{#mu#bar{#mu}}", "GeV", 100, 0, 200);
	ptZ = CreateHist("ZPt", "P_{Z, T}", "GeV", 50, -1, 200);
	massZ_selected = CreateHist("selectedZMass", "M_{Z}", "GeV", 60, 60, 120);
	wholeMassZ_selected = CreateHist("selectedZ_wholeMassRange", "M_{#mu#bar{#mu}}", "GeV", 100, 0, 200);

	ptL1 = CreateHist("AntimuonPt", "P_{#bar{#mu}, T}", "GeV", 80, 0, 160);
	etaL1 = CreateHist("AntimuonEta", "#eta_{#bar{#mu}}", "", 80, -2.5, 2.5);
	phiL1 = CreateHist("AntimuonPhi", "#varphi_{#bar{#mu}}", "rad", 80, -3.3, 3.3);
	isoL1 = CreateHist("AntimuonIsolation", "Isolation / P_{#bar{#mu}, T}", "GeV^{-1}", 80, -0.5, 20);
	sipL1 = CreateHist("AntimuonSIP", "SIP_{#bar{#mu}}", "", 60, -1.5, 60);
	
	ptL2 = CreateHist("MuonPt", "P_{#mu, T}", "GeV", 80, 0, 160);
	etaL2 = CreateHist("MuonEta", "#eta_{#mu}", "", 80, -2.5, 2.5);
	phiL2 = CreateHist("MuonPhi", "#varphi_{#mu}", "rad", 80, -3.3, 3.3);
	isoL2 = CreateHist("MuonIsolation", "Isolation / P_{#mu, T}", "GeV^{-1}", 80, -0.5, 20);
	sipL2 = CreateHist("MuonSIP", "SIP_{#mu}", "", 60, -1.5, 60);

	numZPerEvent = CreateHist("ZCount", "#Z", "", 10, -0.5, 9.5);

	ptLeptons = new TH2F("PtLepton", "; P_{#mu, T} [GeV]; P_{#bar{#mu}, T} [GeV]", 80, 0, 160, 80, 0, 160);

	cutflow = CreateHist("cutflow", "cut", "", 10, -0.5, 9.5);


	// Read the lumi CSVT/Root files and store the number by BX
	lumiReader.readFileForRun(run_number);

	hLumiIntegralsByBin = lumiReader.getRecLumiBins(nBins, minBin, maxBin);

	hAll = new HistoZ("All");

	float stepBin = (maxBin - minBin)/nBins;
	for(int bin = 0; bin <= nBins; ++bin) {
	  stringstream histoName;
	  float binLowEdge = minBin + bin*stepBin;
	  float binUpEdge = binLowEdge + stepBin;
	  hByBinLimits.push_back(make_pair(binLowEdge, binUpEdge));

	  histoName << "bin" << binLowEdge << "_" << binUpEdge;
	  string histoNameStr = histoName.str();
	  hByBin.push_back(new HistoZ(histoNameStr));
	}

	


	pileUp_delLumi = new TProfile("PileUp_delLumi", "; PileUp; delivered luminosity per BX [cm^{-2}s^{-1}]", 15, 0, 30);
	pileUp_lumiPerBX = new TProfile("PileUp_RecLumiPerBX", "; PileUp; recorded luminosity per BX [cm^{-2}s^{-1}]", 15, 0, 30);
	ls_delLumi = new TProfile("ls_delLumi", "; lumisection; delivered luminosity per BX [cm^{-2}s^{-1}]", 40, 0, 1600);

	for (size_t i = 0; i < 10; i++) {
		histPerLumi.push_back(new TH1F(("Luminosity" + to_string(i)).c_str(), (getLumiPerBXRegion(i) + "; M_{Z} [GeV]; Events").c_str(), 60, 60, 120));
	}

	lumiPerBX = CreateHist("Luminosity", "Luminosity per BX", "cm^{-2}s^{-1}", 100, pow(10., 33), 8*pow(10.,33));

	lumi_crossSection = new TProfile("lumi_crossSection", "; luminosity [#mub^{-1}]; crossSection [nb]", 60, 35000, 125000);
	ls_crossSection = new TProfile("ls_crossSection", "; lumisection; crossSection [nb]", 40 , 0, 1600);
	
	ls_Zcount.clear();

	cout << " all histograms are created" << endl;

}

void ZlumiTreeReader::SlaveBegin(TTree * /*tree*/)
{
   // The SlaveBegin() function is called after the Begin() function.
   // When running with PROOF SlaveBegin() is called on each slave server.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();

}

Bool_t ZlumiTreeReader::Process(Long64_t entry)
{
	// The Process() function is called for each entry in the tree (or possibly
	// keyed object in the case of PROOF) to be processed. The entry argument
	// specifies which entry in the currently loaded tree is to be processed.
	// It can be passed to either ZlumiTreeReader::GetEntry() or TBranch::GetEntry()
	// to read either all or the required parts of the data. When processing
	// keyed objects with PROOF, the object is already loaded and is available
	// via the fObject pointer.
	//
	// This function should contain the "body" of the analysis. It can contain
	// simple or elaborate selection criteria, run algorithms on the data
	// of the event and typically fill histograms.
	//
	// The processing can be stopped by calling Abort().
	//
	// Use fStatus to set the return value of TTree::Process().
	//
	// The return value is currently not used.


	//cout << "Process: " << entry << endl;

	ZlumiTreeReader::GetEntry(entry);

	//if (runTest == -1 || runTest != RunNumber) {
	//	cout << RunNumber << endl;
	//	runTest = RunNumber;
	//}

	//cout << "vor Aufruf: " << RunNumber;
	float weight = 1.;
	RunLumiBXIndex lumiBXIndex = RunLumiBXIndex(RunNumber, LumiNumber, BXNumber);
	//int runTest = lumiBXIndex.run();
	//cout << " ---- nach Aufruf: " << runTest << endl;
	//float delLumi = lumiReader.getDelLumi(lumiBXIndex);
	//cout << "LumiNumber : BXNumber " << LumiNumber << " : " << BXNumber << endl;
	//cout << "del Lumi: " << delLumi << endl;

	//pair<float,float> lumi = lumiReader.getLumi(lumiBXIndex);
	//cout << "Lumisection : BXNumber " << LumiNumber << " : " << BXNumber << endl << " --- del : rec lumi: " << lumi.first << " : " << lumi.second << endl;

	if (run_number != -1 and run_number != RunNumber) {
		return kTRUE;
	}


	// get the instLumi for the BX -> this defines the bin
	// find the Z-particle with least mass difference
	double m_diff = 1000;
	int index_Z = -1;
	for(size_t i=0; i < ZMass->size(); i++) {
		double m_temp = fabs(ZMass->at(i) - M_Z);
		if (m_temp <= m_diff) {
			m_diff = m_temp;
			index_Z = i;
		}
	}

	if (index_Z == -1) {
		return kTRUE;
	}

	wholeMassZ_selected->Fill(ZMass->at(index_Z));
	
	float bestZMass = ZMass->at(index_Z);
	bool survive_cut = ZlumiTreeReader::analyseCut(/*SIP*/ 0.4, /*pt*/ 20, /*eta*/ 5, /*Iso*/ 0.4, /*ZMass*/ 66, 116, index_Z);

	if(survive_cut) {
		hAll->Fill(bestZMass, weight);
		massZ_selected->Fill(ZMass->at(index_Z));

		float avgLumi = lumiReader.getAvgInstLumi(lumiBXIndex);

		for (size_t bin = 0; bin < hByBinLimits.size(); bin++) {
			if (avgLumi >= hByBinLimits[bin].first && hByBinLimits[bin].second > avgLumi) {
				hByBin[bin]->Fill(bestZMass, weight);
				break;
			}

		}

	}



	
	

	numZPerEvent->Fill(ZMass->size());

	countZ ++;

	// goes through the Z-vector and fill the histograms
	for(size_t i=0; i < ZMass->size(); i++) {
		//cout << "Z Mass: " << ZMass->at(i) << endl;
		massZ->Fill(ZMass->at(i));
		wholeMassZ->Fill(ZMass->at(i));
		ptZ->Fill(ZPt->at(i));
	}

	// goes through the L1-vector and fill the histograms
	for(size_t i=0; i < Lep1Pt->size(); i++) {
		ptL1->Fill(Lep1Pt->at(i));
		etaL1->Fill(Lep1Eta->at(i));
		phiL1->Fill(Lep1Phi->at(i));
		isoL1->Fill((Lep1chargedHadIso->at(i) + Lep1neutralHadIso->at(i) + Lep1photonIso->at(i)) / Lep1Pt->at(i));
		sipL1->Fill(Lep1SIP->at(i));
	}

	// goes through the L2-vector and fill the histograms
	for(size_t i=0; i < Lep2Pt->size(); i++) {
		ptL2->Fill(Lep2Pt->at(i));
		etaL2->Fill(Lep2Eta->at(i));
		phiL2->Fill(Lep2Phi->at(i));
		ptLeptons->Fill(Lep1Pt->at(i), Lep2Pt->at(i));
		isoL2->Fill((Lep2chargedHadIso->at(i) + Lep2neutralHadIso->at(i) + Lep2photonIso->at(i)) / Lep2Pt->at(i));
		sipL2->Fill(Lep2SIP->at(i));
	}


	// check different cut possibilities
	survive_withoutIso = ZlumiTreeReader::analyseCut(0.4, 20, 10, 400, 66, 116, index_Z);
	survive_withIso = ZlumiTreeReader::analyseCut(0.4, 20, 10, 0.4, 66, 116, index_Z);
	survive_eta_withoutIso = ZlumiTreeReader::analyseCut(0.4, 20, 1.2, 400, 66, 116, index_Z);
	survive_eta_withIso = ZlumiTreeReader::analyseCut(0.4, 20, 1.2, 0.4, 66, 116, index_Z);

	if (survive_withoutIso) withoutIso++;
	if (survive_withIso) withIso++;
	if (survive_eta_withoutIso) eta_withoutIso++;
	if (survive_eta_withIso) eta_withIso++;


	delLumiPerBX = lumiReader.getDelLumi(lumiBXIndex);

	pileUp_delLumi->Fill(Nvtx, calcLumi(delLumiPerBX));
	pileUp_lumiPerBX->Fill(Nvtx, calcLumi(lumiReader.getRecLumi(lumiBXIndex)));
	ls_delLumi->Fill(LumiNumber, calcLumi(delLumiPerBX));


	// get Lumi per Event, look in which range (between 45 and 65 (some bins)), do something
	
	if (delLumiPerBX == -1) cout << "Problem in calculating delLumi" << endl;
	else {
		histPerLumi[getIndex(delLumiPerBX)]->Fill(ZMass->at(index_Z));
	}
	lumiPerBX->Fill(calcLumi(delLumiPerBX));

	//cout << delLumiPerBX << " : " << lumiReader.getRecLumi(lumiBXIndex) << endl << "end process "<< endl;

	return kTRUE;
}


void ZlumiTreeReader::SlaveTerminate()
{
   // The SlaveTerminate() function is called after all entries or objects
   // have been processed. When running with PROOF SlaveTerminate() is called
   // on each slave server.

}

void ZlumiTreeReader::Terminate()
{
	// The Terminate() function is the last function to be called during
	// a query. It always runs on the client, it can be used to present
	// the results graphically or save the results to file.

	cout << " write the histograms in the root-file and calculate the crossSection" << endl;

	myFile->cd();

	massZ->Write();
	wholeMassZ->Write();
	ptZ->Write();
	massZ_selected->Write();
	wholeMassZ_selected->Write();

	ptL1->Write();
	etaL1->Write();
	phiL1->Write();
	isoL1->Write();
	sipL1->Write();

	ptL2->Write();
	etaL2->Write();
	phiL2->Write();
	isoL2->Write();
	sipL2->Write();

	numZPerEvent->Write();

	ptLeptons->Write();

	cutflow->SetBinContent(1, beforeCuts);
	cutflow->GetXaxis()->SetBinLabel(1, "before cuts");
	cutflow->SetBinContent(2, cutSIP);
	cutflow->GetXaxis()->SetBinLabel(2, "after SIP cut");
	cutflow->SetBinContent(3, cutPt);
	cutflow->GetXaxis()->SetBinLabel(3, "after Pt cut");
	cutflow->SetBinContent(4, cutIsolation);
	cutflow->GetXaxis()->SetBinLabel(4, "after isolation cut");
	cutflow->SetBinContent(5, cutZMass);
	cutflow->GetXaxis()->SetBinLabel(5, "after Z mass cut");

	cutflow->GetXaxis()->SetBinLabel(6, "-> SIP cut, written cut, Z mass cut");
	cutflow->SetBinContent(7, withoutIso);
	cutflow->GetXaxis()->SetBinLabel(7, "without isolation cut");
	cutflow->SetBinContent(8, withIso);
	cutflow->GetXaxis()->SetBinLabel(8, "with isolation cut");
	cutflow->SetBinContent(9, eta_withoutIso);
	cutflow->GetXaxis()->SetBinLabel(9, "with |#eta| < 2.1 and without isolation cut");
	cutflow->SetBinContent(10, eta_withIso);
	cutflow->GetXaxis()->SetBinLabel(10, "with |#eta| < 2.1 and with isolation cut");


	cutflow->Write();

	pileUp_delLumi->Write();
	pileUp_lumiPerBX->Write();
	ls_delLumi->Write();

	for (size_t i = 0; i < 10; i++) {
		histPerLumi[i]->Write();
	}
	lumiPerBX->Write();

	map<int,int>::iterator it = ls_Zcount.begin();
	for (; it != ls_Zcount.end(); ++it) {
		int lsec = it->first;
		int nZ = it->second;

		RunLumiIndex li(run_number, lsec);
		if (!lumiReader.check_LSFound(li)) {
        	cout << "LS " << lsec << " for run " << run_number << " not found" << endl;
        	continue;
    	}

    	float lumi = lumiReader.getRecIntegral(li);

    	float xs = nZ/lumi * 1000;
  
    	ls_crossSection->Fill(lsec, xs);
    	lumi_crossSection->Fill(lumi, xs);

		//cout << "ls " << lsec << ": sigma_Z = " << xs << " +/- " << xs_err << " nb" << endl;
	}

	ls_crossSection->Write();
	lumi_crossSection->Write();

	TH1F *hXSection = new TH1F("hXSection", "X-section; inst. lumi (1/ub); x-section (ub)", nBins, minBin, maxBin);

	// actually compute the Xsection
	for (size_t bin = 0; bin < hByBin.size(); bin++) {
	  double nZInBin = hByBin[bin]->hMass->Integral();
	  double lumiInBin = hLumiIntegralsByBin->GetBinContent(bin);
	  double xSectionInBin = 0.;
	  if(lumiInBin != 0) {
	    xSectionInBin = nZInBin/lumiInBin;
	  }
	  hXSection->SetBinContent(bin, xSectionInBin);
	}
	hXSection->Write();

	hAll->Write();
	hLumiIntegralsByBin->Write();
	for (size_t bin = 0; bin < hByBin.size(); bin++) {
		hByBin[bin]->Write();
	}


// 	ZPeakFit fit_hAll(hAll->hMass);
// 	RooPlot* frame_hAll = fit_hAll.fitVExpo();
// 	fit_hAll.save(frame_hAll);

	myFile->Close();

	//gROOT->Reset("a");
	delete pileUp_delLumi;
	delete pileUp_lumiPerBX;
	delete ls_delLumi;
	delete lumiPerBX;
	delete ls_crossSection;
	delete lumi_crossSection;

	for (size_t i = 0; i < 10; i++) {
		delete histPerLumi[i];
	}
	histPerLumi.clear();

}
