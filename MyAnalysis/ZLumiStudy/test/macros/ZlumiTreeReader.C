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

float cut_SIP = 3;
float noCut_SIP = 400;
float cut_pt = 20;
float noCut_pt = 0;
float cut_eta = 1.2;
float noCut_eta = 2.4;
float cut_iso = 0.4;
float noCut_iso = 400;
float cut_ZMass_min = 55;
float cut_ZMass_max = 120;

// eff
vector<vector<pair<double, double> > > eff;

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
float calcLumiPerBX(float lumiBarn) { // ub^-1 -> cm^-2 * s^-1
	float my_barn = pow(10.0, -30);
	int bunch = 1;

	return lumiBarn / (my_barn * LENGTH_LS) * bunch;
}

float calcLumi_avgInst(float lumiBarn) { // Hz * ub^-1 -> cm^-2 * s^-1
	float my_barn = pow(10.0, -30);
	int bunch = 1440;

	return lumiBarn / (my_barn) * bunch;
}

float calcPileUp(float lumi)
{
	float sigma_pp = 69.3;
	float frequency = 11246.;

	return lumi * sigma_pp * 1e-27 / frequency;
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


// different eff folder per cut
static string PER_CUT_FOLDER_Mu17[] = {
	"Track_To_DoubleMu17Mu8_Mu17_lumi_for_Run2012", 
	"OurMuonID_To_DoubleMu17Mu8_Mu17_lumi_Eta2P4_Iso_for_Run2012",
	"OurMuonID_To_DoubleMu17Mu8_Mu17_lumi_Eta2P4_for_Run2012", 
	"OurMuonID_To_DoubleMu17Mu8_Mu17_lumi_Eta1P2_Iso_for_Run2012", 
	"OurMuonID_To_DoubleMu17Mu8_Mu17_lumi_Eta1P2_for_Run2012", 
};

vector<pair<double, double> > getEffEntries(TFile* eff_File, string canv_Mu17)
{
	vector<pair<double, double> > entries(nBins, make_pair(-1, -1));
	vector<pair<double, double> > entries_Mu17 (nBins, make_pair(-1,-1));

	// load the correct trigger eff with muon id
	TObject* obj = eff_File->Get((canv_Mu17).c_str());

	TCanvas* canv = dynamic_cast<TCanvas*>(obj);
	if (canv) {
		TList* list = canv->GetListOfPrimitives();
		for (int i = 0; i < list->GetSize(); i++) {
			TH1F* hist = dynamic_cast<TH1F*>(list->At(i));
			if (hist) {
				for (int bin = 0; bin < hist->GetNbinsX(); ++bin) {
    				double y, err;
    				y = hist->GetBinContent(bin + 1);
    				err = hist->GetBinError(bin + 1);
    				entries_Mu17[bin] = make_pair(y, err); // first: value, second: error
				}
				break;
			}
		}
	}

	// calculate the eff = 1 - (1-eff_{trigger, muonId})^2
	for (int i = 0; i < nBins; i++) {
		if (entries_Mu17[i].second == -1) {
			entries[i].first = -1;
			entries[i].second = -1;
		}
		else {
			entries[i].first = pow(entries_Mu17[i].first, 2);
			entries[i].second = sqrt(2.0 * pow(entries_Mu17[i].first * entries_Mu17[i].second, 2));
			//entries[i].second = 2.0 * entries_Mu17[i].second * (1 - entries_Mu17[i].first);
		}
	}
	return entries;		
}



vector<pair<double, double> > saveEff(vector<pair<double, double> > entries)
{
	vector<pair<double, double> > effPerCut (nBins, make_pair(-1, -1));
	for (size_t bin = 0; bin < entries.size(); bin++) {
		if (entries[bin].second == 0 or entries[bin].first == 0) {
			effPerCut[bin] = make_pair(-1, -1);
			}
		else {
			effPerCut[bin].first = entries[bin].first;
			effPerCut[bin].second = entries[bin].second;
		}
	}
	return effPerCut;
}

double calculateXSecError(double countZ, double lumi, pair<double, double> effi)
{
	return (1000.0 / lumi) * sqrt(pow(sqrt(countZ) / effi.first, 2) + pow(effi.second * countZ / pow(effi.first, 2), 2));
}

double calculateXSecError(double countZtot, double countZtot_err, double fraction, double fraction_err, double effi, double effi_err, double lumi)
{
	double countZ = countZtot * fraction;
	double countZ_err = sqrt(pow(fraction * countZtot_err, 2) + pow(countZtot * fraction_err, 2));

	double xSecErr = (1000.0 / lumi) * sqrt(pow(countZ_err / effi, 2) + pow(effi_err * countZ / pow(effi, 2), 2));

	return xSecErr;
}


// different cut possibilities
static std::string PER_CUT_TITLE[] = {
	"no cut",
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
        histsPerCut[i].sipL1 = CreateHist("AntimuonSIP" + index_str, "Antimuon SIP (" + PER_CUT_TITLE[i] + ")", "SIP_{#bar{#mu}}", "", 60, -0.5, 20);

        histsPerCut[i].ptL2 = CreateHist("MuonPt" + index_str, "Muon Pt (" + PER_CUT_TITLE[i] + ")", "P_{#mu, T}", "GeV", 80, 0, 160);
        histsPerCut[i].etaL2 = CreateHist("MuonEta" + index_str, "Muon Eta (" + PER_CUT_TITLE[i] + ")", "#eta_{#mu}", "", 80, -2.5, 2.5);
        histsPerCut[i].phiL2 = CreateHist("MuonPhi" + index_str, "Muon Phi (" + PER_CUT_TITLE[i] + ")", "#varphi_{#mu}", "rad", 80, -3.3, 3.3);
        histsPerCut[i].isoL2 = CreateHist("MuonIsolation" + index_str, "Muon Isolation (" + PER_CUT_TITLE[i] + ")", "Isolation / P_{#mu, T}", "GeV^{-1}", 80, -0.5, 20);
        histsPerCut[i].sipL2 = CreateHist("MuonSIP" + index_str, "Muon SIP (" + PER_CUT_TITLE[i] + ")", "SIP_{#mu}", "", 60, -0.5, 20);  

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

		histsPerCut[i].xSection_fitVExpo = new TH1F(("XSection_fit_VExpo" + index_str).c_str(), ("XSection calculated by fitting with VExpo (" + PER_CUT_TITLE[i] + "); inst. luminosity [Hz#times#mub^{-1}]; x-section [nb]").c_str(), nBins, minBin, maxBin);
		histsPerCut[i].xSection_fit2VExpo = new TH1F(("XSection_fit_2VExpo" + index_str).c_str(), ("XSection calculated by fitting with 2VExpo (" + PER_CUT_TITLE[i] + "); inst. luminosity [Hz#times#mub^{-1}]; x-section [nb]").c_str(), nBins, minBin, maxBin);
		histsPerCut[i].xSection_fit2VExpoMin70 = new TH1F(("XSection_fit_2VExpoMin70" + index_str).c_str(), ("XSection calculated by fitting with 2VExpoMin70 (" + PER_CUT_TITLE[i] + "); inst. luminosity [Hz#times#mub^{-1}]; x-section [nb]").c_str(), nBins, minBin, maxBin);
		histsPerCut[i].xSection_count = new TH1F(("XSection_count" + index_str).c_str(), ("XSection calculated by counting (" + PER_CUT_TITLE[i] + "); inst. luminosity [Hz#times#mub^{-1}]; x-section [nb]").c_str(), nBins, minBin, maxBin);

		histsPerCut[i].nVtx_delLumi = new TProfile(("NVtx_delLumi" + index_str).c_str(), ("#vertices vs. luminosity (" + PER_CUT_TITLE[i] + "); #vertices; luminosity per BX [cm^{-2}s^{-1}]").c_str(), 15, 0, 30);
		histsPerCut[i].nVtx_pileUp = new TProfile(("NVtx_pileUp" + index_str).c_str(), ("#vertices vs. pileUp (" + PER_CUT_TITLE[i] + "); #vertices; pileUp").c_str(), 15, 0, 30);
		histsPerCut[i].ls_delLumi = new TProfile(("ls_delLumi" + index_str).c_str(), ("lumisection vs. luminosity (" + PER_CUT_TITLE[i] + "); lumisection; luminosity per BX [cm^{-2}s^{-1}]").c_str(), 40, 0, 1600);
    
    	histsPerCut[i].eff = new TH1F(("eff per bin" + index_str).c_str(), ("eff per bin (" + PER_CUT_TITLE[i] + "); inst. luminosity [Hz#times#mub^{-1}]; eff").c_str(), nBins, minBin, maxBin);
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

	histsPerCut[index].nVtx_delLumi->Fill(Nvtx, calcLumiPerBX(delLumiPerBX));
	histsPerCut[index].nVtx_pileUp->Fill(Nvtx, calcPileUp(calcLumiPerBX(delLumiPerBX)));
	histsPerCut[index].ls_delLumi->Fill(LumiNumber, calcLumiPerBX(delLumiPerBX));

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
		histsPerCut[i].xSection_fitVExpo->Write();
		histsPerCut[i].xSection_fit2VExpo->Write();
		histsPerCut[i].xSection_fit2VExpoMin70->Write();
		histsPerCut[i].xSection_count->Write();

		histsPerCut[i].nVtx_delLumi->Write();
		histsPerCut[i].nVtx_pileUp->Write();
		histsPerCut[i].ls_delLumi->Write();

		histsPerCut[i].eff->Write();
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
		delete histsPerCut[i].nVtx_pileUp;
		delete histsPerCut[i].ls_delLumi;

		delete histsPerCut[i].hAll->hMass;
		for (int bin = 0; bin < nBins; bin++) {
			delete histsPerCut[i].hByBin[bin]->hMass;
		}
		delete histsPerCut[i].xSection_fitVExpo;
		delete histsPerCut[i].xSection_fit2VExpo;
		delete histsPerCut[i].xSection_fit2VExpoMin70;
		delete histsPerCut[i].xSection_count;

		delete histsPerCut[i].eff;
	}
}

// write and delete one hist
void writeAndDeleteHist(TH1* hist) {
	hist->Write();
	delete hist;
}

// looks whether one event survive the cut or not
bool ZlumiTreeReader::analyseCut(/*SIP*/ float sip, /*pt*/ float pt, /*eta*/ float eta, /*Iso*/ float iso, /*ZMass*/ float massZ_min, float massZ_max, int index_Z) {
	if (!(ZMass->at(index_Z) > massZ_min && ZMass->at(index_Z) < massZ_max))
		return false;
	if (!(Lep1Pt->at(index_Z) > pt && Lep2Pt->at(index_Z) > pt))
		return false;
	if (!(Lep1SIP->at(index_Z) < sip && Lep2SIP->at(index_Z) < sip))
		return false;
	if (!(fabs(Lep1Eta->at(index_Z)) < eta && fabs(Lep2Eta->at(index_Z)) < eta))
		return false;
	if (!((Lep1chargedHadIso->at(index_Z) + Lep1neutralHadIso->at(index_Z) + Lep1photonIso->at(index_Z)) / Lep1Pt->at(index_Z) < iso && (Lep2chargedHadIso->at(index_Z) + Lep2neutralHadIso->at(index_Z) + Lep2photonIso->at(index_Z)) / Lep2Pt->at(index_Z) < iso))
		return false;
	
	// all values are correct
	return true;
}

// convert the given string into the filename and the run number list
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

	// FIXME: all the caching logic should be moved to the LumiFileReaderByBX class
	for (std::set<int>::iterator it = runsToUse.begin(); it != runsToUse.end(); it++) {// loop over all the runs to be used
	  int run = *it;

	  LumiFileReaderByBX lumiReaderForRun("/data1/ZLumiStudy/CalcLumi/Version0/");
	  lumiReaderForRun.readFileForRun(run);

	  if(lumiReaderForRun.isGood()) {
	    if (first) {
	      hLumiIntegralsByBin = lumiReaderForRun.getRecLumiBins(nBins, minBin, maxBin);
	      hLumiIntegralsByBin->SetName("hRec");
	      first = false;
	    } else {
	      TH1F *tmp = lumiReaderForRun.getRecLumiBins(nBins, minBin, maxBin);
	      hLumiIntegralsByBin->Add(tmp);
	    }
	    lumiReader[run] = lumiReaderForRun;

	  } else {
	    runNotFound.insert(run);
	    cout << "Run " << run << " not found." << endl;
	  }
	}

	cout << "Approx. integrated luminosity for this run selection: " << hLumiIntegralsByBin->Integral() << " [1/ub]" << endl;

	for (int i = 0; i < NUM_CUTS; i++) {
		vector<pair<double, double> > tmp (nBins, make_pair(-1, -1));
		eff.push_back(tmp);
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

	if (runsToUse.count(RunNumber) == 0 || runNotFound.count(RunNumber) != 0) {
	  
	  return kTRUE;
	}
	// find the Z-particle with least mass difference
	double m_diff = 99999;
	int index_Z = -1;
	for(size_t i=0; i < ZMass->size(); i++) {
		double m_temp = fabs(ZMass->at(i) - M_Z);
		if (m_temp <= m_diff) {
			m_diff = m_temp;
			index_Z = i;
		}
	}
	if (index_Z == -1) {
	  cout << "Warning: no best Z out of " << ZMass->size() << " candidates" << endl;
	  return kTRUE;
	}

	wholeMassZ_selected->Fill(ZMass->at(index_Z));

	// no cut
	FillPerCutHist(NO_CUT, index_Z, lumiBXIndex);

	// analyse cutflow
	beforeCuts++;
	bool survive_ZMass = analyseCut(noCut_SIP, noCut_pt, noCut_eta, noCut_iso, cut_ZMass_min, cut_ZMass_max, index_Z);
	if (survive_ZMass) {
		cutZMass++;
		bool survive_pt = analyseCut(noCut_SIP, cut_pt, noCut_eta, noCut_iso, cut_ZMass_min, cut_ZMass_max, index_Z);
		if (survive_pt) {
			cutPt++;
			bool survive_sip = analyseCut(cut_SIP, cut_pt, noCut_eta, noCut_iso, cut_ZMass_min, cut_ZMass_max, index_Z);
			if (survive_sip) {
				cutSIP++;
			}
		}
	}
	
	// check different cut possibilities
	bool survive_withoutIso = analyseCut(cut_SIP, cut_pt, noCut_eta, noCut_iso, cut_ZMass_min, cut_ZMass_max, index_Z);
	bool survive_withIso = analyseCut(cut_SIP, cut_pt, noCut_eta, cut_iso, cut_ZMass_min, cut_ZMass_max, index_Z);
	bool survive_eta_withoutIso = analyseCut(cut_SIP, cut_pt, cut_eta, noCut_iso, cut_ZMass_min, cut_ZMass_max, index_Z);
	bool survive_eta_withIso = analyseCut(cut_SIP, cut_pt, cut_eta, cut_iso, cut_ZMass_min, cut_ZMass_max, index_Z);

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

	// load the eff root files and remember eff for every cut
	vector<pair<double, double> > graphEntries (nBins, make_pair(-1, -1));

	TFile* eff_File = 0;
	if (processName == "run2012A")
		eff_File = new TFile("../TagAndProbe/plots_Eff/Run2012_A.root");
	else if(processName == "run2012B" || processName == "presentationRuns")
		eff_File = new TFile("../TagAndProbe/plots_Eff/Run2012_B.root");
	else if(processName == "run2012B_1")
		eff_File = new TFile("../TagAndProbe/plots_Eff/Run2012_B1.root");
	else if(processName == "run2012B_2")
		eff_File = new TFile("../TagAndProbe/plots_Eff/Run2012_B2.root");
	else 
		eff_File = new TFile("../TagAndProbe/plots_Eff/Run2012_B3.root");

	for (size_t cut = 0; cut < NUM_CUTS; cut++) {
		if (eff_File->IsZombie())
			cout << "could not open file " << eff_File << endl;
		else {
			// get TGraph, save them for eff
		 	//graphEntries = getEntries(eff_File, PER_CUT_FOLDER_Mu17[cut], PER_CUT_FOLDER_Mu8[cut]);
		 	graphEntries = getEffEntries(eff_File, PER_CUT_FOLDER_Mu17[cut]);
		}
		eff[cut] = saveEff(graphEntries);

		for (int bin = 2; bin < nBins - 2; bin++) {
			histsPerCut[cut].eff->SetBinContent(bin + 1, eff[cut][bin].first);
			histsPerCut[cut].eff->SetBinError(bin + 1, eff[cut][bin].second);
		}
	} 



	myFile->cd();

	writeAndDeleteHist(wholeMassZ_selected);

	cutflow->SetBinContent(1, beforeCuts);
	cutflow->GetXaxis()->SetBinLabel(1, "before cuts");
	cutflow->SetBinContent(2, cutZMass);
	cutflow->GetXaxis()->SetBinLabel(2, "after Z mass cut");
	cutflow->SetBinContent(3, cutPt);
	cutflow->GetXaxis()->SetBinLabel(3, "after Pt cut");
	cutflow->SetBinContent(4, cutSIP);
	cutflow->GetXaxis()->SetBinLabel(4, "after SIP cut");

	//cutflow->GetXaxis()->SetBinLabel(5, "-> Z Mass cut, Pt cut, SIP cut, written cut");
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
		for (int bin = 2; bin < nBins - 2; bin++) {
			string fit_name = "Mass_bin" + to_string(bin) + " (" + PER_CUT_TITLE[i] + ")";
			ZPeakFit fit_ZMass(histsPerCut[i].hByBin[bin]->hMass, fit_name);
			fit.push_back(fit_ZMass);
			fit_ZMass.fitVExpo(fit_name);
			fit_ZMass.fit2VExpo(fit_name);
			fit_ZMass.fit2VExpoMin70(fit_name);

			RooPlot* frame_ZMass = fit_ZMass.plot();
			fit_ZMass.save(frame_ZMass);

			// get the fit results for the different fits
			RooFitResult* result_VExpo = fit_ZMass.getResult("VExpo");
			RooRealVar* par1_VExpo = (RooRealVar*) result_VExpo->floatParsFinal().find("numTot_VExpo");
			double numTot_VExpo = par1_VExpo->getVal();
			double numTot_Err_VExpo = par1_VExpo->getError();
			RooRealVar* par2_VExpo = (RooRealVar*) result_VExpo->floatParsFinal().find("fSigAll_VExpo");
			double fSigAll_VExpo = par2_VExpo->getVal();
			double fSigAll_Err_VExpo = par2_VExpo->getError();

			RooFitResult* result_2VExpo = fit_ZMass.getResult("2VExpo");
			RooRealVar* par1_2VExpo = (RooRealVar*) result_2VExpo->floatParsFinal().find("numTot_2VExpo");
			double numTot_2VExpo = par1_2VExpo->getVal();
			double numTot_Err_2VExpo = par1_2VExpo->getError();
			RooRealVar* par2_2VExpo = (RooRealVar*) result_2VExpo->floatParsFinal().find("fSigAll_2VExpo");
			double fSigAll_2VExpo = par2_2VExpo->getVal();
			double fSigAll_Err_2VExpo = par2_2VExpo->getError();

			RooFitResult* result_2VExpoMin70 = fit_ZMass.getResult("2VExpoMin70");
			RooRealVar* par1_2VExpoMin70 = (RooRealVar*) result_2VExpoMin70->floatParsFinal().find("numTot_2VExpoMin70");
			double numTot_2VExpoMin70 = par1_2VExpoMin70->getVal();
			double numTot_Err_2VExpoMin70 = par1_2VExpoMin70->getError();
			RooRealVar* par2_2VExpoMin70 = (RooRealVar*) result_2VExpoMin70->floatParsFinal().find("fSigAll_2VExpoMin70");
			double fSigAll_2VExpoMin70 = par2_2VExpoMin70->getVal();
			double fSigAll_Err_2VExpoMin70 = par2_2VExpoMin70->getError();


			// get luminosity and Z counts
			double lumiInBin = hLumiIntegralsByBin->GetBinContent(bin+1); // load the first bin (not the underflow bin!)
			
			double nZInBin_count = histsPerCut[i].hByBin[bin]->hMass->Integral(histsPerCut[i].hByBin[bin]->hMass->GetXaxis()->FindBin(70.), histsPerCut[i].hByBin[bin]->hMass->GetXaxis()->FindBin(110.));
			double nZInBin_fit_VExpo = numTot_VExpo * fSigAll_VExpo;
			double nZInBin_fit_2VExpo = numTot_2VExpo * fSigAll_2VExpo;
			double nZInBin_fit_2VExpoMin70 = numTot_2VExpoMin70 * fSigAll_2VExpoMin70;
			
			// calculate cross section
			double xSectionInBin_count = 0;
			double xSecErrorInBin_count = 0;
			double xSectionInBin_fitVExpo = 0;
			double xSecErrorInBin_fitVExpo = 0;
			double xSectionInBin_fit2VExpo = 0;
			double xSecErrorInBin_fit2VExpo = 0;
			double xSectionInBin_fit2VExpoMin70 = 0;
			double xSecErrorInBin_fit2VExpoMin70 = 0;

			if (lumiInBin != 0 && eff[i][bin].first != 0 && eff[i][bin].second) {
				xSectionInBin_fitVExpo = nZInBin_fit_VExpo * 1000 / (lumiInBin * eff[i][bin].first);
				xSecErrorInBin_fitVExpo = calculateXSecError(numTot_VExpo, numTot_Err_VExpo, fSigAll_VExpo, fSigAll_Err_VExpo, eff[i][bin].first, eff[i][bin].second, lumiInBin);
				xSectionInBin_fit2VExpo = nZInBin_fit_2VExpo * 1000 / (lumiInBin * eff[i][bin].first);
				xSecErrorInBin_fit2VExpo = calculateXSecError(numTot_2VExpo, numTot_Err_2VExpo, fSigAll_2VExpo, fSigAll_Err_2VExpo, eff[i][bin].first, eff[i][bin].second, lumiInBin);
				xSectionInBin_fit2VExpoMin70 = nZInBin_fit_2VExpoMin70 * 1000 / (lumiInBin * eff[i][bin].first);
				xSecErrorInBin_fit2VExpoMin70 = calculateXSecError(numTot_2VExpoMin70, numTot_Err_2VExpoMin70, fSigAll_2VExpoMin70, fSigAll_Err_2VExpoMin70, eff[i][bin].first, eff[i][bin].second, lumiInBin);
				xSectionInBin_count = nZInBin_count * 1000 / (lumiInBin * eff[i][bin].first);
				xSecErrorInBin_count = calculateXSecError(nZInBin_count, lumiInBin, eff[i][bin]);
			}

			histsPerCut[i].xSection_fitVExpo->SetBinContent(bin+1, xSectionInBin_fitVExpo); // wrote in the first and not in the underflow bin!
			histsPerCut[i].xSection_fitVExpo->SetBinError(bin+1, xSecErrorInBin_fitVExpo);
			histsPerCut[i].xSection_fit2VExpo->SetBinContent(bin+1, xSectionInBin_fit2VExpo);
			histsPerCut[i].xSection_fit2VExpo->SetBinError(bin+1, xSecErrorInBin_fit2VExpo);
			histsPerCut[i].xSection_fit2VExpoMin70->SetBinContent(bin+1, xSectionInBin_fit2VExpoMin70);
			histsPerCut[i].xSection_fit2VExpoMin70->SetBinError(bin+1, xSecErrorInBin_fit2VExpoMin70);
			histsPerCut[i].xSection_count->SetBinContent(bin+1, xSectionInBin_count);
			histsPerCut[i].xSection_count->SetBinError(bin+1, xSecErrorInBin_count); 
		}
		// fit the ZPeak
		string fit_name_hAll = "all_Mass (" + PER_CUT_TITLE[i] + ")";
		ZPeakFit fit_hAll(histsPerCut[i].hAll->hMass, fit_name_hAll);
		fit.push_back(fit_hAll);
		fit_hAll.fitVExpo(fit_name_hAll);
		fit_hAll.fit2VExpo(fit_name_hAll);
		fit_hAll.fit2VExpoMin70(fit_name_hAll);

		RooPlot* frame_hAll = fit_hAll.plot();
		frame.push_back(frame_hAll);
		fit_hAll.save(frame_hAll);
	}

	writeAndDeleteHist(hLumiIntegralsByBin);

	DrawPerCutHists();
	DeletePerCutHists();



    set<int>::iterator iter;
    cout << "RunList for which no csvt file or no filling scheme was found:" << endl;
    for(iter=runNotFound.begin(); iter!=runNotFound.end(); ++iter)
    {
        cout << *iter << endl;
    }
    cout << endl;



	// do not close the file before deleting all objects, otherwise it will crash!
	myFile->Close();
}
