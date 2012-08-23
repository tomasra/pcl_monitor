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
#include "ZPeakFit.h"
#include <TH2.h>
#include <TProfile.h>
#include <TCanvas.h>
#include <TGraphErrors.h>
#include <TStyle.h>
#include <TROOT.h>
#include <iostream>
#include <string>
#include <sstream>
#include <string>

using namespace std;

int nBins = 16;
float minBin = 1.;
float maxBin = 5.;

const double M_Z = 91.2;
const double Cross_Section = 1.1; // nb
const double Cross_Section_Error = 0.03; // nb 

int beforeCuts = 0;
int cutPt = 0;
int cutEta = 0;
int cutSIP = 0;
int cutIsolation = 0;
int cutZMass = 0;

int withoutIso = 0;
int withIso = 0;
int eta_withoutIso = 0;
int eta_withIso = 0;

// functions to convert into other types
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

// function to calculate the luminosity in other units
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

// function which generate the histograms
TH1F* CreateHist(string name, string htitle, string xtitle, string unit, size_t nbins, float xmin, float xmax)
{
	TString title;

	float binSize = (xmax-xmin) / nbins;

	// want to write: 1 or nothing
	if (binSize == 1) {
		if (unit.c_str() == string("")) {
		  title.Form("%s;%s; Events", htitle.c_str(), xtitle.c_str());
		}
		else {
			title.Form("%s;%s [%s];Events / %2.0f %s", htitle.c_str(), xtitle.c_str(), unit.c_str(), binSize, unit.c_str());
		}	
	}

	// want to write: 0.??
	else if (binSize < 1) {
			if (unit.c_str() == string("")) {
			title.Form("%s;%s; Events / %1.2f", htitle.c_str(), xtitle.c_str(), binSize);
		}
		else {
			title.Form("%s;%s [%s];Events / %1.2f %s", htitle.c_str(), xtitle.c_str(), unit.c_str(), binSize, unit.c_str());
		}	
	}

	// want to write: ??
	else {
		if (unit.c_str() == std::string("")) {
			title.Form("%s;%s; Events / %2.0f", htitle.c_str(), xtitle.c_str(), binSize);
			}
		else if (unit.c_str() == std::string("cm^{-2}s^{-1}")) {
			binSize = binSize / pow(10., 33);
			title.Form("%s; %s; Events / %g #times 10^{33} %s", htitle.c_str(), xtitle.c_str(), binSize, unit.c_str());
		}
		else {
			title.Form("%s;%s [%s];Events / %2.0f %s", htitle.c_str(), xtitle.c_str(), unit.c_str(), binSize, unit.c_str());
		}	
	}

	
	TH1F* a = new TH1F(name.c_str(), title, nbins, xmin, xmax);
	a->Sumw2();
	return a;
}


// different cut possibilities
static std::string PER_CUT_TITLE[] = {
	"no cut",
    "standard cut",
    "isolation cut",
    "no isolation cut",
    "eta and isolation cut",
    "eta and no isolation cut",
};

void ZlumiTreeReader::CreatePerCutHists()
{
    for (size_t i=0; i < NUM_CUTS; ++i) {
        string index_str = "_cut_" + to_string(i);

        histsPerCut[i].ptZ = CreateHist("ZPt" + index_str, "Z Pt (" + PER_CUT_TITLE[i] + ")", "P_{Z, T}", "GeV", 50, -1, 200);
        histsPerCut[i].massZ_selected = CreateHist("selectedZMass" + index_str, "Z Mass (" + PER_CUT_TITLE[i] + ")", "M_{Z}", "GeV", 60, 60, 120);
        histsPerCut[i].numZPerEvent = CreateHist("ZCount" + index_str, "#Z (" + PER_CUT_TITLE[i] + ")", "#Z", "", 10, -0.5, 9.5);

        histsPerCut[i].ptL1 = CreateHist("AntimuonPt" + index_str, "Antimuon Pt (" + PER_CUT_TITLE[i] + ")", "P_{#bar{#mu}, T}", "GeV", 80, 0, 160);
        histsPerCut[i].etaL1 = CreateHist("AntimuonEta" + index_str, "Antimuon Eta (" + PER_CUT_TITLE[i] + ")", "#eta_{#bar{#mu}}", "", 80, -2.5, 2.5);
        histsPerCut[i].phiL1 = CreateHist("AntimuonPhi" + index_str, "Antimuon Phi (" + PER_CUT_TITLE[i] + ")", "#varphi_{#bar{#mu}}", "rad", 80, -3.3, 3.3);
        histsPerCut[i].isoL1 = CreateHist("AntimuonIsolation" + index_str, "Antimuon Isolation (" + PER_CUT_TITLE[i] + ")", "Isolation / P_{#bar{#mu}, T}", "GeV^{-1}", 80, -0.5, 20);
        histsPerCut[i].sipL1 = CreateHist("AntimuonSIP" + index_str, "Antimuon SIP (" + PER_CUT_TITLE[i] + ")", "SIP_{#bar{#mu}}", "", 60, -1.5, 60);

        histsPerCut[i].ptL2 = CreateHist("MuonPt" + index_str, "Muon Pt (" + PER_CUT_TITLE[i] + ")", "P_{#mu, T}", "GeV", 80, 0, 160);
        histsPerCut[i].etaL2 = CreateHist("MuonEta" + index_str, "Muon Eta (" + PER_CUT_TITLE[i] + ")", "#eta_{#mu}", "", 80, -2.5, 2.5);
        histsPerCut[i].phiL2 = CreateHist("MuonPhi" + index_str, "Muon Phi (" + PER_CUT_TITLE[i] + ")", "#varphi_{#mu}", "rad", 80, -3.3, 3.3);
        histsPerCut[i].isoL2 = CreateHist("MuonIsolation" + index_str, "Muon Isolation (" + PER_CUT_TITLE[i] + ")", "Isolation / P_{#mu, T}", "GeV^{-1}", 80, -0.5, 20);
        histsPerCut[i].sipL2 = CreateHist("MuonSIP" + index_str, "Muon SIP (" + PER_CUT_TITLE[i] + ")", "SIP_{#mu}", "", 60, -1.5, 60);  

    	histsPerCut[i].hAll = new HistoZ("all" + index_str, "Z Mass (" + PER_CUT_TITLE[i] + ")");
    	float stepBin = (maxBin - minBin) / nBins;
    	for (int bin = 0; bin < nBins; ++bin) {
			stringstream histoName;
			float binLowEdge = minBin + bin * stepBin;
			float binUpEdge = binLowEdge + stepBin;
			hByBinLimits.push_back(make_pair(binLowEdge, binUpEdge));

			histoName << "bin " << binLowEdge << " to " << binUpEdge;
			string histoNameStr = histoName.str();

			histsPerCut[i].hByBin.push_back(new HistoZ(to_string(bin).c_str() + index_str, "Z Mass (" + PER_CUT_TITLE[i] + ") for " + histoNameStr));
		}

		histsPerCut[i].xSection_fit = new TH1F(("XSection_fit" + index_str).c_str(), ("XSection calculated by fitting (" + PER_CUT_TITLE[i] + "); inst. luminosity [#mub^{-1}]; x-section [nb]").c_str(), nBins, minBin, maxBin);
		histsPerCut[i].xSection_count = new TH1F(("XSection_count" + index_str).c_str(), ("XSection calculated by counting (" + PER_CUT_TITLE[i] + "); inst. luminosity [#mub^{-1}]; x-section [nb]").c_str(), nBins, minBin, maxBin);

		histsPerCut[i].nVtx_delLumi = new TProfile(("NVtx_delLumi" + index_str).c_str(), ("#vertices vs. luminosity (" + PER_CUT_TITLE[i] + "); #vertices; luminosity per BX [cm^{-2}s^{-1}]").c_str(), 15, 0, 30);
		histsPerCut[i].ls_delLumi = new TProfile(("ls_delLumi" + index_str).c_str(), ("lumisection vs. luminosity (" + PER_CUT_TITLE[i] + "); lumisection; luminosity per BX [cm^{-2}s^{-1}]").c_str(), 40, 0, 1600);
    
	}
}

void ZlumiTreeReader::FillPerCutHist(size_t index, int index_Z, RunLumiBXIndex lumiBXIndex)
{
	histsPerCut[index].ptZ->Fill(ZPt->at(index_Z));
	histsPerCut[index].massZ_selected->Fill(ZMass->at(index_Z));
	histsPerCut[index].numZPerEvent->Fill(ZMass->size());

	histsPerCut[index].ptL1->Fill(Lep1Pt->at(index_Z));
	histsPerCut[index].etaL1->Fill(Lep1Eta->at(index_Z));
	histsPerCut[index].phiL1->Fill(Lep1Phi->at(index_Z));
	histsPerCut[index].isoL1->Fill((Lep1chargedHadIso->at(index_Z) + Lep1neutralHadIso->at(index_Z) + Lep1photonIso->at(index_Z)) / Lep1Pt->at(index_Z));
	histsPerCut[index].sipL1->Fill(Lep1SIP->at(index_Z));

	histsPerCut[index].ptL2->Fill(Lep2Pt->at(index_Z));
	histsPerCut[index].etaL2->Fill(Lep2Eta->at(index_Z));
	histsPerCut[index].phiL2->Fill(Lep2Phi->at(index_Z));
	histsPerCut[index].isoL2->Fill((Lep2chargedHadIso->at(index_Z) + Lep2neutralHadIso->at(index_Z) + Lep2photonIso->at(index_Z)) / Lep2Pt->at(index_Z));
	histsPerCut[index].sipL2->Fill(Lep2SIP->at(index_Z));

	float weight = 1.;
	float bestZMass = ZMass->at(index_Z);
	histsPerCut[index].hAll->Fill(bestZMass, weight);

	float avgLumi = lumiReader[RunNumber].getAvgInstLumi(lumiBXIndex);

	for (int bin = 0; bin < nBins; bin++) {
		if (avgLumi >= hByBinLimits[bin].first && hByBinLimits[bin].second > avgLumi) {
			histsPerCut[index].hByBin[bin]->Fill(bestZMass, weight);
			break;
		}

	}
	float delLumiPerBX = lumiReader[RunNumber].getDelLumi(lumiBXIndex);

	histsPerCut[index].nVtx_delLumi->Fill(Nvtx, calcLumi(delLumiPerBX));
	histsPerCut[index].ls_delLumi->Fill(LumiNumber, calcLumi(delLumiPerBX));

}


void ZlumiTreeReader::DrawPerCutHists()
{
	for (size_t i = 0; i < NUM_CUTS; i++) {
		histsPerCut[i].ptZ->Write();
		histsPerCut[i].massZ_selected->Write();
		histsPerCut[i].numZPerEvent->Write();

		histsPerCut[i].ptL1->Write();
		histsPerCut[i].etaL1->Write();
		histsPerCut[i].phiL1->Write();
		histsPerCut[i].isoL1->Write();
		histsPerCut[i].sipL1->Write();

		histsPerCut[i].ptL2->Write();
		histsPerCut[i].etaL2->Write();
		histsPerCut[i].phiL2->Write();
		histsPerCut[i].isoL2->Write();
		histsPerCut[i].sipL2->Write();

		histsPerCut[i].hAll->hMass->Write();
		for (int bin = 0; bin < nBins; bin++) {
			histsPerCut[i].hByBin[bin]->hMass->Write();
		}
		histsPerCut[i].xSection_fit->Write();
		histsPerCut[i].xSection_count->Write();

		histsPerCut[i].nVtx_delLumi->Write();
		histsPerCut[i].ls_delLumi->Write();
	}
} 

void ZlumiTreeReader::DeletePerCutHists()
{
	for (int i = 0; i < NUM_CUTS; i++) {
		delete histsPerCut[i].ptZ;
		delete histsPerCut[i].massZ_selected;
		delete histsPerCut[i].numZPerEvent;

		delete histsPerCut[i].ptL1;
		delete histsPerCut[i].etaL1;
		delete histsPerCut[i].phiL1;
		delete histsPerCut[i].isoL1;
		delete histsPerCut[i].sipL1;

		delete histsPerCut[i].ptL2;
		delete histsPerCut[i].etaL2;
		delete histsPerCut[i].phiL2;
		delete histsPerCut[i].isoL2;
		delete histsPerCut[i].sipL2;

		delete histsPerCut[i].nVtx_delLumi;
		delete histsPerCut[i].ls_delLumi;

		delete histsPerCut[i].hAll->hMass;
		for (int bin = 0; bin < nBins; bin++) {
			delete histsPerCut[i].hByBin[bin]->hMass;
		}
		delete histsPerCut[i].xSection_fit;
		delete histsPerCut[i].xSection_count;
	}
}

// write and delete one hist
void writeAndDeleteHist(TH1* hist) {
	hist->Write();
	delete hist;
}

// looks whether one event survive the cut or not
bool ZlumiTreeReader::analyseCut(/*SIP*/ float sip, /*pt*/ float pt, /*eta*/ float eta, /*Iso*/ float iso, /*ZMass*/ float massZ_min, float massZ_max, int index_Z) {
	if (!(Lep1SIP->at(index_Z) < sip && Lep2SIP->at(index_Z) < sip))
		return false;
	if (!(Lep1Pt->at(index_Z) > pt && Lep2Pt->at(index_Z) > pt))
		return false;
	if (!(abs(Lep1Eta->at(index_Z)) < eta && abs(Lep2Eta->at(index_Z)) < eta))
		return false;
	if (!((Lep1chargedHadIso->at(index_Z) + Lep1neutralHadIso->at(index_Z) + Lep1photonIso->at(index_Z)) / Lep1Pt->at(index_Z) < iso && (Lep2chargedHadIso->at(index_Z) + Lep2neutralHadIso->at(index_Z) + Lep2photonIso->at(index_Z)) / Lep2Pt->at(index_Z) < iso))
		return false;
	if (!(ZMass->at(index_Z) > massZ_min && ZMass->at(index_Z) < massZ_max))
		return false;
	// all values are correct
	return true;
}

void ZlumiTreeReader::ParseOption(const std::string& opt)
{
	if (opt.find(':') != opt.npos) {
		size_t pos = opt.find(':');

		useSingleRun = false;
		processName = opt.substr(0, pos);
		std::string runList = opt.substr(pos+1);

		size_t cpos = runList.find(',');
		while (cpos != runList.npos) {
			std::string thisPart = runList.substr(0, cpos);
			int thisRun = to_int(thisPart);
			runsToUse.insert(thisRun);

			runList = runList.substr(cpos+1);
			cpos = runList.find(',');
		}
		int lastRun = to_int(runList);
		runsToUse.insert(lastRun);

		std::cout << "Process: " << processName << " for runs:" << std::endl;
		for (std::set<int>::iterator it = runsToUse.begin(); it != runsToUse.end(); it++) {
			std::cout << " " << *it;
		}
		std::cout << endl;
	}
	else {
		useSingleRun = true;
		singleRun = to_int(opt);
		processName = opt;
		runsToUse.insert(singleRun);
	}
}

void ZlumiTreeReader::Begin(TTree* /*tree*/)
{
	// The Begin() function is called at the start of the query.
	// When running with PROOF Begin() is only called on the client.
	// The tree argument is deprecated (on PROOF 0 is passed).

	string option = GetOption();
	ParseOption(option);

	cout << "start the Begin-function for process " << processName << endl;

	string file_name = "data/ZLumiStudy_" + processName + ".root";
	cout << file_name << endl;
	myFile = new TFile(file_name.c_str(), "RECREATE");

	CreatePerCutHists();

	wholeMassZ_selected = CreateHist("selectedZ_wholeMassRange", "", "M_{#mu#bar{#mu}}", "GeV", 100, 0, 200);

	cutflow = CreateHist("cutflow", "", "", "", 9, -0.5, 8.5);

	bool first = true;
	for (std::set<int>::iterator it = runsToUse.begin(); it != runsToUse.end(); it++) {
		int run = *it;

		lumiReader.insert(make_pair(run, LumiFileReaderByBX("/data1/ZLumiStudy/CalcLumi/Version0/")));
		lumiReader[run].readFileForRun(run);

		if (first) {
			hLumiIntegralsByBin = lumiReader[run].getRecLumiBins(nBins, minBin, maxBin);
		}
		else {
			TH1F *tmp = lumiReader[run].getRecLumiBins(nBins, minBin, maxBin);
			hLumiIntegralsByBin->Add(tmp);
		}
		hLumiIntegralsByBin->SetName("hRec");

		first = false;
	}	

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

	ZlumiTreeReader::GetEntry(entry);

	RunLumiBXIndex lumiBXIndex = RunLumiBXIndex(RunNumber, LumiNumber, BXNumber);

	if (runsToUse.count(RunNumber) == 0)
		return kTRUE;

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

	// no cut
	FillPerCutHist(NO_CUT, index_Z, lumiBXIndex);

	// analyse cutflow
	beforeCuts++;
	bool survive_sip = analyseCut(0.4, 0, 10, 400, 0, 200, index_Z);
	if (survive_sip) {
		cutSIP++;
		bool survive_pt = analyseCut(0.4, 20, 10, 400, 0, 200, index_Z);
		if (survive_pt) {
			cutPt++;
			bool survive_ZMass = analyseCut(0.4, 20, 10, 400, 55, 120, index_Z);
			if (survive_ZMass) {
				cutZMass++;
			}
		}
	}
	
	// check different cut possibilities
	bool survive_cut = analyseCut(/*SIP*/ 0.4, /*pt*/ 20, /*eta*/ 10, /*Iso*/ 0.4, /*ZMass*/ 55, 120, index_Z);
	if(survive_cut) {
		FillPerCutHist(FIRST_CUT, index_Z, lumiBXIndex);
	}
	bool survive_withoutIso = analyseCut(0.4, 20, 10, 400, 55, 120, index_Z);
	bool survive_withIso = analyseCut(0.4, 20, 10, 0.4, 55, 120, index_Z);
	bool survive_eta_withoutIso = analyseCut(0.4, 20, 1.2, 400, 55, 120, index_Z);
	bool survive_eta_withIso = analyseCut(0.4, 20, 1.2, 0.4, 55, 120, index_Z);

	if (survive_withoutIso) {
		withoutIso++;
		FillPerCutHist(NO_ISOLATION_CUT, index_Z, lumiBXIndex);
	}
	if (survive_withIso) {
		withIso++;
		FillPerCutHist(ISOLATION_CUT, index_Z, lumiBXIndex);
	}
	if (survive_eta_withoutIso) {
		eta_withoutIso++;
		FillPerCutHist(ETA_AND_NO_ISOLATION_CUT, index_Z, lumiBXIndex);
	}
	if (survive_eta_withIso) {
		eta_withIso++;
		FillPerCutHist(ETA_AND_ISOLATION_CUT, index_Z, lumiBXIndex);
	}

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

	writeAndDeleteHist(wholeMassZ_selected);

	cutflow->SetBinContent(1, beforeCuts);
	cutflow->GetXaxis()->SetBinLabel(1, "before cuts");
	cutflow->SetBinContent(2, cutSIP);
	cutflow->GetXaxis()->SetBinLabel(2, "after SIP cut");
	cutflow->SetBinContent(3, cutPt);
	cutflow->GetXaxis()->SetBinLabel(3, "after Pt cut");
	cutflow->SetBinContent(4, cutZMass);
	cutflow->GetXaxis()->SetBinLabel(4, "after Z mass cut");

	//cutflow->GetXaxis()->SetBinLabel(5, "-> SIP cut, written cut, Z mass cut");
	cutflow->SetBinContent(6, withoutIso);
	cutflow->GetXaxis()->SetBinLabel(6, "without isolation cut");
	cutflow->SetBinContent(7, withIso);
	cutflow->GetXaxis()->SetBinLabel(7, "with isolation cut");
	cutflow->SetBinContent(8, eta_withoutIso);
	cutflow->GetXaxis()->SetBinLabel(8, "with |#eta| < 1.2 and without isolation cut");
	cutflow->SetBinContent(9, eta_withIso);
	cutflow->GetXaxis()->SetBinLabel(9, "with |#eta| < 1.2 and with isolation cut");


	writeAndDeleteHist(cutflow);


	vector<ZPeakFit> fit;
	vector<RooPlot*> frame;

	
	for (size_t i = 0; i < NUM_CUTS; i++) {
		// actually compute the Xsection
		for (int bin = 0; bin < nBins; bin++) {
			ZPeakFit fit_ZMass(histsPerCut[i].hByBin[bin]->hMass);
			fit.push_back(fit_ZMass);
			RooPlot* frame_ZMass = fit_ZMass.fitVExpo("Mass_bin" + to_string(bin) + "_" + to_string(i));
			frame.push_back(frame_ZMass);
			fit_ZMass.save(frame_ZMass);

			RooFitResult* result = fit_ZMass.getResult();
			RooRealVar* par1 = (RooRealVar*) result->floatParsFinal().find("numTot");
			double value = par1->getVal();
			RooRealVar* par2 = (RooRealVar*) result->floatParsFinal().find("fSigAll");
			double value2 = par2->getVal();

			double nZInBin_count = histsPerCut[i].hByBin[bin]->hMass->Integral(histsPerCut[i].hByBin[bin]->hMass->GetXaxis()->FindBin(70.), histsPerCut[i].hByBin[bin]->hMass->GetXaxis()->FindBin(110.));
			cout << nZInBin_count << endl;
			double nZInBin_fit = value * value2;
			double lumiInBin = hLumiIntegralsByBin->GetBinContent(bin);

			double xSectionInBin_count = 0;
			double xSecErrorInBin_count = 0;
			double xSectionInBin_fit = 0;
			double xSecErrorInBin_fit = 0;

			if (lumiInBin != 0) {
				xSectionInBin_fit = nZInBin_fit * 1000 / lumiInBin;
				xSecErrorInBin_fit = sqrt(nZInBin_fit) * 1000 / lumiInBin;
				xSectionInBin_count = nZInBin_count * 1000 / lumiInBin;
				xSecErrorInBin_count = sqrt(nZInBin_count) * 1000 / lumiInBin;
			}
			histsPerCut[i].xSection_fit->SetBinContent(bin, xSectionInBin_fit);
			histsPerCut[i].xSection_fit->SetBinError(bin, xSecErrorInBin_fit);
			histsPerCut[i].xSection_count->SetBinContent(bin, xSectionInBin_count);
			histsPerCut[i].xSection_count->SetBinError(bin, xSecErrorInBin_count);
		}
		// fit the ZPeak
		ZPeakFit fit_hAll(histsPerCut[i].hAll->hMass);
		fit.push_back(fit_hAll);
		RooPlot* frame_hAll = fit_hAll.fitVExpo("all_Mass" + to_string(i));
		frame.push_back(frame_hAll);
		fit_hAll.save(frame_hAll);
	}



	writeAndDeleteHist(hLumiIntegralsByBin);

	DrawPerCutHists();
	DeletePerCutHists();

	// do not close the file before deleting all objects, otherwise it will crash!
	myFile->Close();
}
