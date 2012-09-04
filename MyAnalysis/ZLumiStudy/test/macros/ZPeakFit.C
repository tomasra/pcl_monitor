#include "ZPeakFit.h"
#include <string>
#include <sstream>
#include <TPaveText.h>

using namespace RooFit;

template <typename A, typename B>
static A lexical_cast(const B& b)
{
  std::stringstream sstr;
  sstr << b;
  A a;
  sstr >> a;
  return a;
}


// Constructor
ZPeakFit::ZPeakFit(TH1* h, std::string title)
: mass("mass", "mass", 55, 120) , data("data", "data", mass, h), w("w","w")
{ 
	massframe = mass.frame(Bins(100),Title(title.c_str()));
	massframe->SetName(title.c_str());
	massframe->SetXTitle("Z Mass [GeV]");
	massframe->SetYTitle("Events"); 

	fit_VExpo = false;
	fit_2VExpo = false;
	fit_2VExpoMin70 = false;

	w.import(data);
}

// fit with one voigtian as signal and an exponential background
void ZPeakFit::fitVExpo(std::string title) {
	w.factory("Voigtian::signal_VExpo(mass, mean_VExpo[90,80,100], width_VExpo[2.495], sigma_VExpo[3,1,20])");
	w.factory("Exponential::background_VExpo(mass, lp_VExpo[0,-5,5])");

	w.factory("expr::nSignal_VExpo('fSigAll_VExpo*numTot_VExpo', fSigAll_VExpo[.9,0,1],numTot_VExpo[1,0,1e10])");
	w.factory("expr::nBkg_VExpo('(1-fSigAll_VExpo)*numTot_VExpo', fSigAll_VExpo,numTot_VExpo)");

	w.factory("SUM::pdfSigPlusBackg_VExpo(nSignal_VExpo*signal_VExpo, nBkg_VExpo*background_VExpo)");
	pdf_VExpo = w.pdf("pdfSigPlusBackg_VExpo");
	//data.plotOn(massframe, DataError(RooAbsData::SumW2));
	result_VExpo = pdf_VExpo->fitTo(data, Save(), PrintLevel(-1), Verbose(kFALSE));
	result_VExpo->SetName(("fitResult_VExpo_" + title).c_str());

	fit_VExpo = true;
}

// fit with two voigtian as signal and an exponential background
void ZPeakFit::fit2VExpo(std::string title) {
	w.factory("Voigtian::signal1_2VExpo(mass, mean1_2VExpo[90,80,100], width_2VExpo[2.495], sigma1_2VExpo[2,1,3])");
	w.factory("Voigtian::signal2_2VExpo(mass, mean2_2VExpo[90,80,100], width_2VExpo, sigma2_2VExpo[4,2,10])");
	w.factory("SUM::signal_2VExpo(vFrac_2VExpo[0.8,0,1]*signal1_2VExpo, signal2_2VExpo)");
	w.factory("Exponential::background_2VExpo(mass, lp_2VExpo[-0.1,-1,0.1])");

	w.factory("expr::nSignal_2VExpo('fSigAll_2VExpo*numTot_2VExpo', fSigAll_2VExpo[.9,0,1],numTot_2VExpo[1,0,1e10])");
	w.factory("expr::nBkg_2VExpo('(1-fSigAll_2VExpo)*numTot_2VExpo', fSigAll_2VExpo,numTot_2VExpo)");

	w.factory("SUM::pdfSigPlusBackg_2VExpo(nSignal_2VExpo*signal_2VExpo, nBkg_2VExpo*background_2VExpo)");
	pdf_2VExpo = w.pdf("pdfSigPlusBackg_2VExpo");
	//data.plotOn(massframe, DataError(RooAbsData::SumW2));
	result_2VExpo = pdf_2VExpo->fitTo(data, Save(), PrintLevel(-1), Verbose(kFALSE));
	result_2VExpo->SetName(("fitResult_2VExpo_" + title).c_str());

	fit_2VExpo = true;
}

void ZPeakFit::fit2VExpoMin70(std::string title) {
	w.factory("Voigtian::signal1_2VExpoMin70(mass, mean1_2VExpoMin70[90,80,100], width_2VExpoMin70[2.495], sigma1_2VExpoMin70[2,1,3])");
	w.factory("Voigtian::signal2_2VExpoMin70(mass, mean2_2VExpoMin70[90,80,100], width_2VExpoMin70, sigma2_2VExpoMin70[4,3,10])");
	w.factory("SUM::signal_2VExpoMin70(vFrac_2VExpoMin70[0.8,0.5,1]*signal1_2VExpoMin70, signal2_2VExpoMin70)");
	w.factory("Exponential::background_2VExpoMin70(mass, lp_2VExpoMin70[-0.1,-1,0.1])");
	
	w.factory("expr::nSignal_2VExpoMin70('fSigAll_2VExpoMin70*numTot_2VExpoMin70', fSigAll_2VExpoMin70[.9,0,1],numTot_2VExpoMin70[1,0,1e10])");
	w.factory("expr::nBkg_2VExpoMin70('(1-fSigAll_2VExpoMin70)*numTot_2VExpoMin70', fSigAll_2VExpoMin70,numTot_2VExpoMin70)");

	w.factory("SUM::pdfSigPlusBackg_2VExpoMin70(nSignal_2VExpoMin70*signal_2VExpoMin70, nBkg_2VExpoMin70*background_2VExpoMin70)");
	pdf_2VExpoMin70 = w.pdf("pdfSigPlusBackg_2VExpoMin70");
	//data.plotOn(massframe, DataError(RooAbsData::SumW2));
	result_2VExpoMin70 = pdf_2VExpoMin70->fitTo(data, Save(), PrintLevel(-1), Verbose(kFALSE));
	result_2VExpoMin70->SetName(("fitResult_2VExpoMin70_" + title).c_str());

	fit_2VExpoMin70 = true;
}


// plot all used fits into one frame (with parameter box and chi^2)
RooPlot* ZPeakFit::plot() {
	data.plotOn(massframe, DataError(RooAbsData::SumW2));
	if (fit_VExpo) {
		pdf_VExpo->plotOn(massframe);
		double chi2 = massframe->chiSquare();
		std::string label = "VExpo (chi2 = " + lexical_cast<std::string>(chi2) + ")";
		pdf_VExpo->paramOn(massframe, Label("VExpo"), Layout(0.7, 0.9, 0.9), Label(label.c_str()));
		massframe->getAttText()->SetTextSize(0.02);
		TPaveText* box = (TPaveText*)massframe->findObject(Form("%s_paramBox",pdf_VExpo->GetName()));
		// do not use SetY1NDC, because NDC coordinates are not yet initialized. The y1 value will be used as the ndc value.
		box->SetY1(0.65); 
		massframe->getAttLine(Form("%s_paramBox",pdf_VExpo->GetName()))->SetLineColor(kBlue);
	}
	if (fit_2VExpo) {
		pdf_2VExpo->plotOn(massframe, LineColor(kRed));
		double chi2 = massframe->chiSquare();
		std::string label = "2VExpo (chi2 = " + lexical_cast<std::string>(chi2) + ")";
		pdf_2VExpo->paramOn(massframe, Layout(0.7, 0.9, 0.5), Label(label.c_str()));
		massframe->getAttText()->SetTextSize(0.02);
		TPaveText* box = (TPaveText*)massframe->findObject(Form("%s_paramBox",pdf_2VExpo->GetName()));
		box->SetY1(0.2);
		massframe->getAttLine(Form("%s_paramBox",pdf_2VExpo->GetName()))->SetLineColor(kRed);
	}
	if (fit_2VExpoMin70) {
		pdf_2VExpoMin70->plotOn(massframe, LineColor(kGreen), LineStyle(2));
		double chi2 = massframe->chiSquare();
		std::string label = "2VExpoMin70 (chi2 = " + lexical_cast<std::string>(chi2) + ")";
		pdf_2VExpoMin70->paramOn(massframe, Layout(0.15, 0.4, 0.9), Label(label.c_str()));
		massframe->getAttText()->SetTextSize(0.02);
		TPaveText* box = (TPaveText*)massframe->findObject(Form("%s_paramBox",pdf_2VExpoMin70->GetName()));
		box->SetY1(0.55);
		massframe->getAttLine(Form("%s_paramBox",pdf_2VExpoMin70->GetName()))->SetLineColor(kGreen);
	}

	return massframe;
}


// gives the fitresults back
RooFitResult* ZPeakFit::getResult(std::string fit) {
	if (fit == "VExpo" && fit_VExpo) {
		result_VExpo->Print();
		return result_VExpo;
	}
	if (fit == "2VExpo" && fit_2VExpo) {
		result_2VExpo->Print();
		return result_2VExpo;
	}
	if (fit == "2VExpoMin70" && fit_2VExpoMin70) {
		result_2VExpoMin70->Print();
		return result_2VExpoMin70;
	} 
	else {
		cout << "no fit is selected!" << endl;
	}
	return 0;
}


// saves the frame and the fitresults into the selected file
void ZPeakFit::save(RooPlot* frame) {
	frame->Write();
	if (fit_VExpo) {
		result_VExpo->Write();
	}
	if (fit_2VExpo) {
		result_2VExpo->Write();
	}
	if (fit_2VExpoMin70) {
		result_2VExpoMin70->Write();
	}
}
