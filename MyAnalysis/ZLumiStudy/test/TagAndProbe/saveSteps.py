
import sys
import os
from ROOT import *

from pprint import pprint

gROOT.SetBatch(True)

stats = {
	"B_steps_EtaFirst": {
		"file": "not used",
	}
}

file_name = "Run2012B_inSteps_etaFirst.root"

color = [kBlack, kGreen+1, kRed+1, kCyan+1, kBlue+1, kOrange+10, kMagenta+1, kYellow-4, kViolet-6, kGray+2, kGreen+4] 

nBins = 16
minBin = 1.
maxBin = 5.


def GetKeyNames(file, dir = "" ):
	file.cd(dir)
	return [key.GetName() for key in gDirectory.GetListOfKeys()]

def rememberHistInDict(theIndex, name, obj):
    if theIndex.has_key(name):
        theIndex[name].append(obj)
    else:
        theIndex[name] = [obj]

hists = {}
saveLegs = []
saveHist = []

def allPlots(hists, count):
	canv = TCanvas("all" + str(count), "allSteps", 800, 800)

	leg = TLegend(0.1,0.1,0.55,0.5)

	hists[0].SetStats(False)
	hists[0].SetTitle("")
	hists[0].GetYaxis().SetRangeUser(0.65, 1.02)
	leg.AddEntry(hists[0], hists[0].GetName()[:-9], "L")
	hists[0].SetLineColor(color[0])
	hists[0].SetLineWidth(2)
	hists[0].Draw("E")

	for i in range(1, count):
		leg.AddEntry(hists[i], hists[i].GetName()[:-9], "L")
		hists[i].SetLineColor(color[i])
		hists[i].SetLineWidth(2)
		hists[i].SetLineStyle(2)
		hists[i].Draw("E same")

	leg.SetFillColor(kWhite)
	leg.Draw("same")
	saveLegs.append(leg)

	canv.Update()
	return canv


print file_name

myFile = TFile(file_name)

if not myFile.IsOpen():
	print "Failed to open", myFile
	sys.exit(0)

folders = GetKeyNames(myFile, "tpTree")

for folder in folders:
	print folder
	gROOT.cd() # create the histogram in the gROOT directory and not in a file that gets unloaded later on, otherwise it will be deleted
	if "Pt" in folder:
		pass
	else:
		hist = TH1F(folder, folder + "; inst. lumi per BX [Hz#times#mub^{-1}]; Efficiency", nBins, minBin, maxBin)
		rememberHistInDict(hists, folder, hist)
		saveHist.append(hist)
	subfolders = GetKeyNames(myFile, "tpTree/" + folder)
	for subfolder in subfolders:
		if subfolder[0:7] != "fit_eff" and subfolder[0:7] != "cnt_eff":
			for bin in range(2, nBins - 2):
				if ("bxInstLumi_bin" + str(bin) + "_") in subfolder:
					folderPerBin = GetKeyNames(myFile, "tpTree/" + folder + "/" + subfolder)
					for stuffPerBin in folderPerBin:
						obj = myFile.Get("tpTree/" + folder + "/" + subfolder + "/fitresults")
					par = obj.floatParsFinal().find("efficiency")
					val = par.getVal()
					err = par.getError()
					hist.SetBinContent(bin + 1, val)
					hist.SetBinError(bin + 1, err)
					

print "after loading files"

canv = []
print len(hists)
for i in range(1,len(hists)+1):
	canv.append(allPlots(saveHist, i))

outfile_name = "Run2012"
for run in stats:
	outfile_name += "_" + run

rf = TFile("plots_Eff/" + outfile_name + ".root", "RECREATE")

for c in canv:
	c.Write()

rf.Write()
rf.Close()

outpath = "plots_Eff/" + outfile_name
if not os.path.exists(outpath):
	os.makedirs(outpath)

counter = 1
cmax = len(canv)
for i in range(len(canv)):
	if counter == 1:
		canv[i].Print("plots_Eff/" + outfile_name + ".pdf(")
		counter +=1
	elif counter == cmax:
		canv[i].Print("plots_Eff/" + outfile_name + ".pdf)")
	else:
		canv[i].Print("plots_Eff/" + outfile_name + ".pdf")
		counter +=1
	canv[i].Print(outpath + "/" + canv[i].GetName() + ".png")




