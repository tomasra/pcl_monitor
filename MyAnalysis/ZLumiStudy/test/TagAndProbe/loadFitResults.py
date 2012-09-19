
import sys
import os
from ROOT import *

from pprint import pprint

gROOT.SetBatch(True)

stats = {
	"A": {
		"file": "Run2012A_save_allCuts_noVBTFbutPF.root",
	},
	"B": {
		"file": "Run2012B_save_allCuts_noVBTFbutPF.root",
	}
}

#stats = {
#	"B1": {
#		"file": "Run2012B_save_allCuts_1of3_sorted.root",
#	},
#	"B2": {
#		"file": "Run2012B_save_allCuts_2of3_sorted.root",
#	},
#	"B3": {
#		"file": "Run2012B_save_allCuts_3of3_sorted.root",
#	}
#}


color = [kBlack, kGreen+1, kRed+1, kCyan+1, kBlue+1]

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

def draw_TH1F(histos, name):
	canv = TCanvas(name, name, 600, 600)

	leg = TLegend(0.1,0.1,0.2,0.3)
	leg.AddEntry(histos[0], "A", "L")
	histos[0].SetStats(False)
	#histos[0].SetTitle("")
	histos[0].GetYaxis().SetRangeUser(0.85, 1.0)
	histos[0].SetLineWidth(1)
	histos[0].SetLineColor(kBlack)
	histos[0].SetLineWidth(2)
	histos[0].Draw("E")


	for i in range(1, len(histos)):
		leg.AddEntry(histos[i], "B", "L")
		#if i == 1:
		#	leg.AddEntry(histos[i], "B2", "F")
		#if i == 2:
		#	leg.AddEntry(histos[i], "B3", "F")
		histos[i].SetLineColor(color[i])
		histos[i].SetLineWidth(2)
		histos[i].Draw("E same")

	leg.SetFillColor(kWhite)
	leg.Draw()
	saveLegs.append(leg)
	canv.Update()
	return canv

counter = 0
for run in stats:
	file_name = stats[run]["file"]

	print file_name, "(", counter, ")"

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
			hist = TH1F(folder[:-13] + "_" + str(counter), folder[:-13] + "; inst. lumi per BX [Hz#times#mub^{-1}]; Efficiency", nBins, minBin, maxBin)
			rememberHistInDict(hists, folder[:-1], hist)
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
	counter += 1
						


print "after loading files"

canv = []
print len(hists)
for hist in hists:
	canv.append(draw_TH1F(hists[hist], hist))

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




