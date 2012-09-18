
import sys
import os
from ROOT import *

from pprint import pprint

gROOT.SetBatch(True)

stats = {
	"A": {
		"file": "data/plots/ZLumiStudy_run2012A.root",
	},
	"B": {
		"file": "data/plots/ZLumiStudy_run2012B.root",
	}
}


color = [kBlack, kGreen, kRed, kCyan, kBlue]

nBins = 16
minBin = 1.
maxBin = 5.


def GetKeyNames(file, dir = "" ):
	file.cd(dir)
	return [key.GetName() for key in gDirectory.GetListOfKeys()]

def drawRatio(hists):
	canvs = TCanvas("cutflow", "cutflow")

	
	for h in range(len(hists)):
		binContent = hists[h].GetBinContent(2)
		for bin in range(1, hists[h].GetNbinsX() + 1):
			hists[h].SetBinContent(bin, hists[h].GetBinContent(bin) * 1.0 / binContent)
	
	for bin in range(1, hists[0].GetNbinsX() + 1):
		if hists[1].GetBinContent(bin) != 0:
			hists[0].SetBinContent(bin, hists[0].GetBinContent(bin) * 1.0 / hists[1].GetBinContent(bin))
		else:
			hists[0].SetBinContent(bin, 0)

	hists[0].GetYaxis().SetRangeUser(0.8, 1.2)
	hists[0].GetYaxis().SetTitle("normalized ratio 2012A/2012B")
	hists[0].SetMarkerStyle(2)
	hists[0].SetMarkerSize(3)
	hists[0].Draw("P")

	line = TLine(hists[0].GetXaxis().GetXmin(), 1.0, hists[0].GetXaxis().GetXmax(), 1.0)
	line.SetLineStyle(2)
	line.SetLineWidth(2)
	line.Draw("same")
	lines.append(line)

	return canvs
 


saveHist = []
lines = []


counter = 0
for run in stats:
	file_name = stats[run]["file"]

	print file_name, "(", counter, ")"

	myFile = TFile(file_name)

	if not myFile.IsOpen():
		print "Failed to open", myFile
		sys.exit(0)

	folders = GetKeyNames(myFile, "")
	for folder in folders:
		if folder == "cutflow":
			obj = myFile.Get(folder)
			print obj.IsA().GetName()
			listPrimitives =  obj.GetListOfPrimitives()
			for prim in listPrimitives:
				if prim.IsA().InheritsFrom("TH1"):
					saveHist.append(prim)


print "after loading files"

canv = []
print len(saveHist)
canv.append(drawRatio(saveHist))

outfile_name = "ratio_Run2012"
for run in stats:
	outfile_name += "_" + run

rf = TFile("data/plots/" + outfile_name + ".root", "RECREATE")

for c in canv:
	c.Write()

rf.Write()
rf.Close()

outpath = "data/plots/" + outfile_name
if not os.path.exists(outpath):
	os.makedirs(outpath)

counter = 1
cmax = len(canv)
for i in range(len(canv)):
	if counter == 1:
		canv[i].Print("data/plots/" + outfile_name + ".pdf(")
		counter +=1
	elif counter == cmax:
		canv[i].Print("data/plots/" + outfile_name + ".pdf)")
	else:
		canv[i].Print("data/plots/" + outfile_name + ".pdf")
		counter +=1
	canv[i].Print(outpath + "/" + canv[i].GetName() + ".png")




