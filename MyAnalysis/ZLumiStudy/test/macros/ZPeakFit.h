
#ifndef ZPeakFit_H
#define ZPeakFit_H

#include "RooGlobalFunc.h"

#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooCategory.h"
#include "RooArgList.h"
#include "RooDataHist.h"
#include "RooFormulaVar.h"
#include "RooHistPdf.h"
#include "RooGenericPdf.h"
#include "RooAddPdf.h"
#include "RooSimultaneous.h"
#include "RooGaussian.h"
#include "RooNLLVar.h"
#include "RooConstVar.h"
#include "RooMinuit.h"
#include "RooFitResult.h"
#include "RooExponential.h"
#include "RooFFTConvPdf.h"
#include "RooWorkspace.h"
#include "RooPlot.h"
#include "TCanvas.h"

class ZPeakFit {
public:
	ZPeakFit(TH1* h);


	RooPlot* fitVExpo(std::string title);
	RooPlot* fit2VExpo(std::string title);
	RooPlot* fit2VExpoMin70(std::string title);
	
	RooFitResult* getResult();


	void save(RooPlot* frame);

private:
	RooRealVar mass;
	RooDataHist data;
	RooFitResult* result;
	RooWorkspace w;

	RooPlot* fit(std::string title);
};
#endif