#define ZlumiTreeReader_cxx
// The class definition in ZlumiTreeRader.h has been generated automatically
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
// Root > T->Process("ZlumiTreeRader.C")
// Root > T->Process("ZlumiTreeRader.C","some options")
// Root > T->Process("ZlumiTreeRader.C+")
//

#include "ZlumiTreeReader.h"
#include <TH2.h>
#include <TStyle.h>
#include <iostream>
#include <string>

using namespace std;


TFile* myFile;

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

TH1F* cutflow;
int beforeCuts;
int cutL1;
int cutL2;
int cutZMass;


const double M_Z = 91.2;

TH1F* CreateHist(string name, string xtitle, string unit, size_t nbins, float xmin, float xmax)
{
	TString title;

	float binSize = (xmax-xmin) / nbins;

	// want to write 1 or nothing
	if (binSize == 1) {
		if (unit.c_str() == string("")) {
		  title.Form(";%s; Events", xtitle.c_str());
		}
		else {
			title.Form(";%s [%s];Events / %2.0f %s", xtitle.c_str(), unit.c_str(), binSize, unit.c_str());
		}	
	}

	// want to write 0.??
	else if (binSize < 1) {
			if (unit.c_str() == string("")) {
			title.Form(";%s; Events / %1.2f", xtitle.c_str(), binSize);
		}
		else {
			title.Form(";%s [%s];Events / %1.2f %s", xtitle.c_str(), unit.c_str(), binSize, unit.c_str());
		}	
	}

	// want to write ??
	else {
			if (unit.c_str() == std::string("")) {
			title.Form(";%s; Events / %2.0f", xtitle.c_str(), binSize);
		}
		else {
			title.Form(";%s [%s];Events / %2.0f %s", xtitle.c_str(), unit.c_str(), binSize, unit.c_str());
		}	
	}

	
	TH1F* a = new TH1F(name.c_str(), title, nbins, xmin, xmax);
	a->SetFillColor(kAzure+2);
	a->SetLineColor(1);
	a->SetLineWidth(2);
	return a;
}

void SetStyle()
{
	gStyle->SetOptStat("nemrou");
}


void ZlumiTreeReader::Begin(TTree* /*tree*/)
{
	// The Begin() function is called at the start of the query.
	// When running with PROOF Begin() is only called on the client.
	// The tree argument is deprecated (on PROOF 0 is passed).

	SetStyle();

	TString option = GetOption();

	myFile = new TFile("test.root", "RECREATE");

	massZ = CreateHist("ZMass", "M_{Z}", "GeV", 60, 60, 120);
	wholeMassZ = CreateHist("wholeMassRange", "M_{#mu#bar{#mu}}", "GeV", 100, 0, 200);
	ptZ = CreateHist("ZPt", "P_{Z, T}", "GeV", 50, 0, 200);
	massZ_selected = CreateHist("selectedZMass", "M_{Z}", "GeV", 60, 60, 120);
	wholeMassZ_selected = CreateHist("selectedZ_wholeMassRange", "M_{#mu#bar{#mu}}", "GeV", 100, 0, 200);

	ptL1 = CreateHist("AntimuonPt", "P_{#bar{#mu}, T}", "GeV", 80, 0, 160);
	etaL1 = CreateHist("AntimuonEta", "#eta_{#bar{#mu}}", "", 80, -3, 3);
	phiL1 = CreateHist("AntimuonPhi", "#varphi_{#bar{#mu}}", "rad", 80, -3.3, 3.3);
	isoL1 = CreateHist("AntimuonIsolation", "Isolation / P_{#bar{#mu}, T}", "GeV^{⁻1}", 20, -1.5, 20);
	sipL1 = CreateHist("AntimuonSIP", "SIP_{#bar{#mu}}", "", 60, -1.5, 60);
	
	ptL2 = CreateHist("MuonPt", "P_{#mu, T}", "GeV", 80, 0, 160);
	etaL2 = CreateHist("MuonEta", "#eta_{#mu}", "", 80, -3, 3);
	phiL2 = CreateHist("MuonPhi", "#varphi_{#mu}", "rad", 80, -3.3, 3.3);
	isoL2 = CreateHist("MuonIsolation", "Isolation / P_{#mu, T}", "GeV^{-1}", 20, -1.5, 20);
	sipL2 = CreateHist("MuonSIP", "SIP_{#mu}", "", 60, -1.5, 60);

	numZPerEvent = CreateHist("ZCount", "#Z", "", 10, -0.5, 9.5);

	ptLeptons = new TH2F("PtLepton", "; P_{#mu, T} [GeV]; P_{#bar{#mu}, T} [GeV]", 80, 0, 160, 80, 0, 160);

	cutflow = CreateHist("cutflow", "cut", "", 4, -0.5, 3.5);

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

	numZPerEvent->Fill(ZMass->size());

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

	// find the Z-paricle with least mass difference
	double m_diff = 1000;
	int index_Z = 0;
	for(size_t i=0; i < ZMass->size(); i++) {
		double m_temp = fabs(ZMass->at(i) - M_Z);
		if (m_temp <= m_diff) {
			m_diff = m_temp;
			index_Z = i;
		}
	}
	massZ_selected->Fill(ZMass->at(index_Z));
	wholeMassZ_selected->Fill(ZMass->at(index_Z));

	// analyse cutflow with selected Z index
	beforeCuts ++;
	if (Lep1Pt->at(index_Z) > 25 and Lep1Eta->at(index_Z) < 2.1) {
		cutL1 ++;
		if (Lep2Pt->at(index_Z) > 25 and Lep2Eta->at(index_Z) < 2.1) {
			cutL2 ++;
			if (ZMass->at(index_Z) > 66 and ZMass->at(index_Z) < 116) {
				cutZMass ++;
			}
		}
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
	cutflow->GetXaxis()->SetBinLabel(1, "before Cuts");
	cutflow->SetBinContent(2, cutL1);
	cutflow->GetXaxis()->SetBinLabel(2, "after Lep1 cut");	
	cutflow->SetBinContent(3, cutL2);
	cutflow->GetXaxis()->SetBinLabel(3, "after Lep2 cut");
	cutflow->SetBinContent(4, cutZMass);
	cutflow->GetXaxis()->SetBinLabel(4, "after Z Mass cut");
	cutflow->Write();

	myFile->Close();

}
