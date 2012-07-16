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

TH1F* ptL1;
TH1F* etaL1;
TH1F* phiL1;

TH1F* ptL2;
TH1F* etaL2;
TH1F* phiL2;

TH2F* ptLeptons;

TH1F* numZPerEvent;

TH1F* CreateHist(string name, string xtitle, string einheit, size_t nbinbs, float xmin, float xmax)
{
	TString title;

	float binSize = (xmax-xmin) / nbinbs;

	// want to write 1 or nothing
	if (binSize == 1) {
		if (einheit.c_str() == string("")) {
		  title.Form(";%s; Events", xtitle.c_str());
		}
		else {
			title.Form(";%s [%s];Events / %2.0f %s", xtitle.c_str(), einheit.c_str(), binSize, einheit.c_str());
		}	
	}

	// want to write 0.??
	else if (binSize < 1) {
			if (einheit.c_str() == string("")) {
			title.Form(";%s; Events / %1.2f", xtitle.c_str(), binSize);
		}
		else {
			title.Form(";%s [%s];Events / %1.2f %s", xtitle.c_str(), einheit.c_str(), binSize, einheit.c_str());
		}	
	}

	// want to write ??
	else {
			if (einheit.c_str() == std::string("")) {
			title.Form(";%s; Events / %2.0f", xtitle.c_str(), binSize);
		}
		else {
			title.Form(";%s [%s];Events / %2.0f %s", xtitle.c_str(), einheit.c_str(), binSize, einheit.c_str());
		}	
	}

	
	TH1F* a = new TH1F(name.c_str(), title, nbinbs, xmin, xmax);
	a->SetFillColor(kAzure+2);
	a->SetLineColor(1);
	a->SetLineWidth(2);
	return a;
}


void ZlumiTreeReader::Begin(TTree* /*tree*/)
{
	// The Begin() function is called at the start of the query.
	// When running with PROOF Begin() is only called on the client.
	// The tree argument is deprecated (on PROOF 0 is passed).

	TString option = GetOption();

	myFile = new TFile("test.root", "RECREATE");

	massZ = CreateHist("ZMass", "M_{Z}", "GeV", 60, 60, 120);
	wholeMassZ = CreateHist("wholeMassRange", "M_{#mu#bar{#mu}}", "GeV", 100, 0, 200);
	ptZ = CreateHist("ZPt", "P_{Z, T}", "GeV", 50, 0, 200);

	ptL1 = CreateHist("MuonPt", "P_{#mu, T}", "GeV", 80, 0, 160);
	etaL1 = CreateHist("MuonEta", "#eta_{#mu}", "", 80, -3, 3);
	phiL1 = CreateHist("MuonPhi", "#varphi_{#mu}", "rad", 80, -3.3, 3.3);

	ptL2 = CreateHist("AntimuonPt", "P_{#bar{#mu}, T}", "GeV", 80, 0, 160);
	etaL2 = CreateHist("AntimuonEta", "#eta_{#bar{#mu}}", "", 80, -3, 3);
	phiL2 = CreateHist("AntimuonPhi", "#varphi_{#bar{#mu}}", "rad", 80, -3.3, 3.3);

	numZPerEvent = CreateHist("ZCount", "#Z", "", 10, -0.5, 9.5);

	ptLeptons = new TH2F("PtLepton", "; P_{#mu, T} [GeV]; P_{#bar{#mu}, T} [GeV]", 80, 0, 160, 80, 0, 160);

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
	}

	// goes through the L2-vector and fill the histograms
	for(size_t i=0; i < Lep2Pt->size(); i++) {
		ptL2->Fill(Lep2Pt->at(i));
		etaL2->Fill(Lep2Eta->at(i));
		phiL2->Fill(Lep2Phi->at(i));
		ptLeptons->Fill(Lep1Pt->at(i), Lep2Pt->at(i));
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

	ptL1->Write();
	etaL1->Write();
	phiL1->Write();

	ptL2->Write();
	etaL2->Write();
	phiL2->Write();

	numZPerEvent->Write();

	ptLeptons->Write();

	myFile->Close();

}
