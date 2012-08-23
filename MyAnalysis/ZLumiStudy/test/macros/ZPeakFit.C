#include "ZPeakFit.h"

using namespace RooFit;


// Constructor
ZPeakFit::ZPeakFit(TH1* h)
: mass("mass", "mass", 0, 200) , data("data", "data", mass, h), w("w","w")
{ 
	
}

// TODO: Namen uebergeben
RooPlot* ZPeakFit::fitVExpo(std::string title) {
	w.import(data);

	w.factory("Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])");
	w.factory("Exponential::background(mass, lp[0,-5,5])");

	return fit(title);
}

RooPlot* ZPeakFit::fit2VExpo(std::string title) {
	w.import(data);

	w.factory("Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])");
	w.factory("Voigtian::signal2(mass, mean2[90,80,100], width, sigma2[4,2,10])");
	w.factory("SUM::signal(vFrac[0.8,0,1]*signal1, signal2)");
	w.factory("Exponential::background(mass, lp[-0.1,-1,0.1])");
	
	return fit(title);
}

RooPlot* ZPeakFit::fit2VExpoMin70(std::string title) {
	w.import(data);

	w.factory("Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])");
	w.factory("Voigtian::signal2(mass, mean2[90,80,100], width, sigma2[4,3,10])");
	w.factory("SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)");
	w.factory("Exponential::background(mass, lp[-0.1,-1,0.1])");
	
	return fit(title);
}

RooPlot* ZPeakFit::fit(std::string title) {
	w.factory("expr::nSignal('fSigAll*numTot', fSigAll[.9,0,1],numTot[1,0,1e10])");
	w.factory("expr::nBkg('(1-fSigAll)*numTot', fSigAll,numTot)");
	w.factory("SUM::pdfSigPlusBackg(nSignal*signal, nBkg*background)");

	w.pdf("pdfSigPlusBackg")->Print();

	w.Print();
  
	result = w.pdf("pdfSigPlusBackg")->fitTo(data, Save());
	result->SetName(("fitResult_" + title).c_str());

	RooPlot* massframe = mass.frame(Bins(100),Title(title.c_str()));
	massframe->SetName(title.c_str());
	massframe->SetXTitle("Z Mass [GeV]");
	massframe->SetYTitle("Events");
	data.plotOn(massframe, DataError(RooAbsData::SumW2));
	w.pdf("pdfSigPlusBackg")->paramOn(massframe, Layout(0.55, 0.99, 0.9)); // begin left edge, end right edge, high
	w.pdf("pdfSigPlusBackg")->plotOn(massframe);

	return massframe;
}


RooFitResult* ZPeakFit::getResult() {
	result->Print();
	long fitnll = result->minNll();
	cout << "nll " << fitnll << endl;

	return result;
}


void ZPeakFit::save(RooPlot* frame) {
	frame->Write();
	result->Write();
}
