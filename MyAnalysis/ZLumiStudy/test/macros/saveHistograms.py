
import sys
import os
from math import sqrt
from ROOT import *

gROOT.SetBatch(True)

#file_name = "ZLumiStudy_presentationRuns"
file_name = "ZLumiStudy_run2012A_2"
#file_name = "ZLumiStudy_run2012B"
#file_name = "ZLumiStudy_run2012B_1"
#file_name = "ZLumiStudy_run2012B_2"
#file_name = "ZLumiStudy_run2012B_3"
#file_name = "ZLumiStudy_allRuns"
#file_name = "ZLumiStudy_" + runnumber

myFile = TFile("data/" + file_name + ".root")


def GetKeyNames(file, dir = "" ):
	file.cd(dir)
	return [key.GetName() for key in gDirectory.GetListOfKeys()]

def drawXSec(hist, cname):
	canv = TCanvas(cname, cname, 950, 600)

	histClone = hist.Clone()
	for bin in range(3, hist.GetNbinsX()-1):
		xs_err = hist.GetBinError(bin)
		xs = hist.GetBinContent(bin)
		err_withLumi = sqrt(pow(xs_err, 2) + pow(xs * 0.045, 2))
		histClone.SetBinError(bin, err_withLumi)

	print cname
	if cname[-1] == "3" or cname[-1] == "4":
		print "barrel"
		histClone.GetYaxis().SetRangeUser(0.12, 0.2)
	elif cname[-1] == "5" or cname[-1] == "6":
		print "eta0P8"
		histClone.GetYaxis().SetRangeUser(0.06, 0.1)
	else:
		histClone.GetYaxis().SetRangeUser(0.32, 0.55)
	histClone.SetFillColor(kGreen+1)
	histClone.Draw("E5")
	histClones.append(histClone)

	hist.SetLineColor(kBlack)
	hist.Draw("E same")

	canv.Update()
	return canv


def drawTH1F(hist, cname):
	hist.SetStats(False)
	if cname[0] == "X":
		canv = drawXSec(hist, cname)
	elif cname[0:3] != "eff":
		canv = TCanvas(cname, cname, 950, 600)
		hist.SetLineColor(1)
		hist.SetFillColor(kAzure+2)
		hist.SetLineWidth(2)
		if cname == "cutflow":
			hist.GetXaxis().SetLabelSize(0.05)
		hist.Draw("hist")
	else:
		canv = TCanvas(cname, cname, 950, 600)
		hist.GetYaxis().SetRangeUser(0.6, 1.005)
		hist.SetLineColor(1)
		hist.SetLineWidth(1)
		hist.Draw("E")

	if cname == "cutflow" or cname[:6] == "ZCount":
		canv.SetBottomMargin(0.2)
		canv.SetRightMargin(0.15)
		canv.SetLogy()

	canv.Update()
	return canv

def drawTProfile(prof, cname):
	canv = TCanvas(cname, cname, 950, 600)
	prof.SetStats(False)
	prof.SetLineColor(1)
	prof.SetLineWidth(1)
	prof.Draw("E")

	if cname[0:12] == "NVtx_delLumi":
		myfit = TF1("linearFit", "[0] * x + [1]", 0, 30)
		myfit.SetParameter(0, 1.0e29)
		myfit.SetParameter(1, 1.5e30)
		myfit.SetParName(0, "slope")
		myfit.SetParName(1, "constant")

		prof.Fit("linearFit")
		chi2_Ndf = myfit.GetChisquare() / myfit.GetNDF()

		canv.cd()
		#text = TLatex(0.55, 0.4, "#splitline{slope: " + ("%g" % myfit.GetParameter(0)) + "}{constant: " + ("%g" % myfit.GetParameter(1)) + "}")
		text = TLatex(0.55, 0.4, "#splitline{slope: " + ("%g" % myfit.GetParameter(0)) + "}{#splitline{constant: " + ("%g" % myfit.GetParameter(1)) + "}{chi^{2}/NDF: " + str(chi2_Ndf) + "}}")
		text.SetNDC()
		text.SetTextSize(0.04)
		text.Draw("same")
		fitText.append(text)

	if cname[0:11] == "NVtx_pileUp":
		myfit = TF1("linearFit", "[0] * x + [1]", 0, 30)
		myfit.SetParameter(0, 1)
		myfit.SetParameter(1, 0)
		myfit.SetParName(0, "slope")
		myfit.SetParName(1, "constant")

		prof.Fit("linearFit")
		chi2_Ndf = myfit.GetChisquare() / myfit.GetNDF()

		canv.cd()
		#text = TLatex(0.55, 0.4, "#splitline{slope: " + ("%g" % myfit.GetParameter(0)) + "}{constant: " + ("%g" % myfit.GetParameter(1)) + "}")
		text = TLatex(0.55, 0.4, "#splitline{slope: " + ("%g" % myfit.GetParameter(0)) + "}{#splitline{constant: " + ("%g" % myfit.GetParameter(1)) + "}{chi^{2}/NDF: " + str(chi2_Ndf) + "}}")
		text.SetNDC()
		text.SetTextSize(0.04)
		text.Draw("same")
		fitText.append(text)

	canv.Update()
	return canv

def drawRooPlot(plot, cname):
	canv = TCanvas(cname, cname, 950, 600)

	plot.Draw()
	return canv



if not myFile.IsOpen():
	print "Failed to open", myFile
	sys.exit(0)

canv = []
fitText = []
histClones = []

print "get names"
keys = GetKeyNames(myFile)
for i in range(len(keys)):
	obj = myFile.Get(keys[i])

	obj_type = obj.IsA().GetName()
	if obj_type == "TH1F":
		if keys[i][:4] == "Mass":
			print keys[i]
		else:
			canv.append(drawTH1F(obj, keys[i]))

	elif obj_type == "TProfile":
		canv.append(drawTProfile(obj, keys[i]))
	elif obj_type == "RooPlot":
		canv.append(drawRooPlot(obj, keys[i]))

	else:
		print obj_type



rf = TFile("data/plots/" + file_name + ".root", "RECREATE")

for c in canv:
	c.Write()

rf.Write()
rf.Close()

outpath = "data/plots/" + file_name
if not os.path.exists(outpath):
	os.makedirs(outpath)

counter = 1
cmax = len(canv)
for i in range(len(canv)):
	if counter == 1:
		canv[i].Print("data/plots/" + file_name + ".pdf(")
		counter +=1
	elif counter == cmax:
		canv[i].Print("data/plots/" + file_name + ".pdf)")
	else:
		canv[i].Print("data/plots/" + file_name + ".pdf")
		counter +=1
	canv[i].Print(outpath + "/" + canv[i].GetName() + ".png")




